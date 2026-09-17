#!/usr/bin/env python3
"""Structural and documentation checks for the dev-standards marketplace.

Enforces the three CodeWiki principles (see docs/codewiki.md):

  1. Atomic docs near code - every plugin carries its own README.md, and every
     skill carries a SKILL.md with a real description.
  2. Doc-as-a-constraint    - a plugin or skill that is not documented in
     /docs is a failure, not a warning, so docs cannot lag behind code.
  3. Explicit navigation    - docs/nav.json must describe the repository
     exactly: no missing entries, no orphans, no dead paths.

Dependency-free on purpose: it runs on a bare python3 in CI and locally.

Usage:  python3 scripts/check_repo.py [--quiet]
Exit:   0 all checks pass, 1 otherwise.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
NAV = ROOT / "docs" / "nav.json"
PLUGINS_DIR = ROOT / "plugins"

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)

errors: list[str] = []
checks = 0


def check(condition: bool, message: str) -> bool:
    """Record a check; append `message` to errors when it fails."""
    global checks
    checks += 1
    if not condition:
        errors.append(message)
    return condition


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        errors.append(f"{path.relative_to(ROOT)}: missing")
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON - {exc}")
    return {}


def frontmatter(path: Path) -> dict[str, str]:
    """Parse the flat top-level keys of a YAML frontmatter block."""
    match = FRONTMATTER.match(path.read_text())
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line.startswith((" ", "\t", "#")) or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip("'\"")
    return fields


def body(path: Path) -> str:
    text = path.read_text()
    match = FRONTMATTER.match(text)
    return text[match.end():] if match else text


def main() -> int:
    quiet = "--quiet" in sys.argv

    marketplace = load_json(MARKETPLACE)
    nav = load_json(NAV)
    if not marketplace or not nav:
        report(quiet)
        return 1

    entries = {p["name"]: p for p in marketplace.get("plugins", []) if "name" in p}
    on_disk = sorted(d.name for d in PLUGINS_DIR.iterdir() if d.is_dir()) if PLUGINS_DIR.is_dir() else []
    nav_plugins = nav.get("plugins", {})

    # --- marketplace identity -------------------------------------------------
    check(
        marketplace.get("name") == nav.get("marketplace"),
        f"marketplace name {marketplace.get('name')!r} != docs/nav.json marketplace "
        f"{nav.get('marketplace')!r}",
    )
    check(
        KEBAB.match(marketplace.get("name", "")) is not None,
        f"marketplace name {marketplace.get('name')!r} is not kebab-case",
    )

    # --- every doc page in the nav tree exists --------------------------------
    for page in nav.get("docs", []):
        path = ROOT / page["path"]
        check(path.is_file(), f"nav: doc page {page['path']} is listed but missing on disk")
        check(bool(page.get("summary")), f"nav: doc page {page['path']} has no summary")

    # --- filesystem, marketplace, and nav agree on the plugin set -------------
    for name in on_disk:
        check(name in entries, f"plugins/{name}/ exists but is not listed in marketplace.json")
        check(name in nav_plugins, f"plugins/{name}/ exists but is not listed in docs/nav.json")
    for name in entries:
        check(name in on_disk, f"marketplace.json lists {name!r} but plugins/{name}/ does not exist")
    for name in nav_plugins:
        check(name in on_disk, f"docs/nav.json lists {name!r} but plugins/{name}/ does not exist")

    # --- per-plugin checks ----------------------------------------------------
    for name in on_disk:
        # A plugin missing from marketplace.json or nav.json has already been
        # reported. Keep checking its files anyway so one run surfaces every
        # problem instead of only the first layer.
        entry = entries.get(name) or {}
        nav_entry = nav_plugins.get(name) or {}

        plugin_dir = PLUGINS_DIR / name
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        readme = plugin_dir / "README.md"
        doc = ROOT / nav_entry["doc"] if nav_entry.get("doc") else ROOT / "docs" / "plugins" / f"{name}.md"

        check(KEBAB.match(name) is not None, f"{name}: directory name is not kebab-case")
        check(manifest_path.is_file(), f"{name}: missing .claude-plugin/plugin.json")

        # Atomic docs near code.
        check(readme.is_file(), f"{name}: missing plugins/{name}/README.md (atomic doc near code)")
        # Doc-as-a-constraint.
        check(doc.is_file(), f"{name}: missing docs page {doc.relative_to(ROOT)}")

        # Component directories must not hide inside .claude-plugin/.
        for component in ("skills", "commands", "agents", "hooks"):
            check(
                not (plugin_dir / ".claude-plugin" / component).exists(),
                f"{name}: {component}/ must sit at the plugin root, not inside .claude-plugin/",
            )

        if not manifest_path.is_file():
            continue
        manifest = load_json(manifest_path)
        check(manifest.get("name") == name, f"{name}: plugin.json name is {manifest.get('name')!r}")
        check(bool(manifest.get("description")), f"{name}: plugin.json has no description")
        check(bool(manifest.get("$schema")), f"{name}: plugin.json has no $schema reference")
        if entry:
            check(
                entry.get("name") == manifest.get("name"),
                f"{name}: marketplace entry name != plugin.json name",
            )
            check(
                entry.get("version") == manifest.get("version"),
                f"{name}: version {entry.get('version')!r} in marketplace.json != "
                f"{manifest.get('version')!r} in plugin.json",
            )
            check(
                entry.get("source") == f"./plugins/{name}",
                f"{name}: marketplace source is {entry.get('source')!r}, "
                f"expected './plugins/{name}'",
            )
        if nav_entry:
            check(
                nav_entry.get("manifest") == f"plugins/{name}/.claude-plugin/plugin.json",
                f"{name}: docs/nav.json manifest path is wrong",
            )
            # Optional `reference` block: supporting docs a plugin ships that
            # are not skills. Indexed, so they are checked like everything else.
            for ref_name, ref in (nav_entry.get("reference") or {}).items():
                check(
                    (ROOT / ref.get("path", "")).is_file(),
                    f"{name}: docs/nav.json reference {ref_name!r} points at "
                    f"{ref.get('path')!r}, which does not exist",
                )
                check(
                    bool(ref.get("summary")),
                    f"{name}: docs/nav.json reference {ref_name!r} has no summary",
                )

        # --- skills -----------------------------------------------------------
        skills_dir = plugin_dir / "skills"
        skills_on_disk = sorted(d.name for d in skills_dir.iterdir() if d.is_dir()) if skills_dir.is_dir() else []
        nav_skills = nav_entry.get("skills", {})
        doc_text = doc.read_text() if doc.is_file() else ""
        readme_text = readme.read_text() if readme.is_file() else ""

        for skill in skills_on_disk:
            check(skill in nav_skills, f"{name}/{skill}: skill is not listed in docs/nav.json")
        for skill in nav_skills:
            check(skill in skills_on_disk, f"{name}: docs/nav.json lists skill {skill!r} that does not exist")

        for skill in skills_on_disk:
            skill_md = skills_dir / skill / "SKILL.md"
            check(skill_md.is_file(), f"{name}/{skill}: missing SKILL.md")
            check(KEBAB.match(skill) is not None, f"{name}/{skill}: skill directory is not kebab-case")
            if not skill_md.is_file():
                continue

            fields = frontmatter(skill_md)
            check(bool(fields), f"{name}/{skill}: SKILL.md has no YAML frontmatter")
            description = fields.get("description", "")
            check(bool(description), f"{name}/{skill}: SKILL.md frontmatter has no description")
            check(
                len(description) >= 40,
                f"{name}/{skill}: description is too short to be a useful trigger "
                f"({len(description)} chars); say when to use the skill",
            )
            check(len(description) <= 1024, f"{name}/{skill}: description exceeds 1024 characters")
            if "name" in fields:
                check(
                    fields["name"] == skill,
                    f"{name}/{skill}: SKILL.md frontmatter name {fields['name']!r} "
                    f"!= directory name {skill!r}",
                )
            check(bool(body(skill_md).strip()), f"{name}/{skill}: SKILL.md has no body")

            # Doc-as-a-constraint: a new skill must be documented before it merges.
            check(
                f"### {skill}" in doc_text,
                f"{name}/{skill}: not documented in {doc.relative_to(ROOT)} "
                f"(expected a '### {skill}' section)",
            )
            check(
                skill in readme_text,
                f"{name}/{skill}: not mentioned in plugins/{name}/README.md",
            )
            if skill in nav_skills:
                check(
                    nav_skills[skill].get("path") == f"plugins/{name}/skills/{skill}/SKILL.md",
                    f"{name}/{skill}: docs/nav.json path is wrong",
                )
                check(
                    bool(nav_skills[skill].get("summary")),
                    f"{name}/{skill}: docs/nav.json entry has no summary",
                )

    report(quiet)
    return 1 if errors else 0


def report(quiet: bool) -> None:
    if errors:
        print(f"FAIL  {len(errors)} problem(s) across {checks} checks:\n", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        print(
            "\nSee docs/codewiki.md for the rules these checks enforce.",
            file=sys.stderr,
        )
    elif not quiet:
        print(f"PASS  {checks} checks")


if __name__ == "__main__":
    sys.exit(main())
