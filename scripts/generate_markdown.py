#!/usr/bin/env python3
"""Generate the searchable skill list source page from data/skills.json."""
import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
NAMES = {"coding": "Coding", "research": "Research", "writing": "Writing", "data": "Data & Automation", "devops": "DevOps", "creative": "Creative", "other": "Other"}


def date(value):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except (ValueError, AttributeError):
        return str(value)[:10]


def main():
    source = json.loads((ROOT / "data/skills.json").read_text(encoding="utf-8"))
    groups = {}
    for skill in source.get("skills", []):
        groups.setdefault(skill.get("category", "other"), []).append(skill)
    lines = ["# Awesome Agent Skills", "", f"> Last updated: **{date(source.get('last_updated', ''))}** | Total skills: **{source.get('total', 0)}**", "", "A curated list of reusable skills for Codex, Claude Code, Cursor, OpenCode, and other AI coding agents.", ""]
    if groups:
        lines += ["## Categories", ""] + [f"- [{NAMES.get(key, key.title())}](#{key})" for key in sorted(groups)] + ["", "---", ""]
    for key in sorted(groups):
        lines += [f"## {NAMES.get(key, key.title())}", ""]
        for index, skill in enumerate(sorted(groups[key], key=lambda item: item.get("stars", 0), reverse=True), 1):
            lines += [f"### {index}. [{skill['name']}]({skill['url']})", "", f"⭐ **{skill.get('stars', 0):,}** | 🔤 **{skill.get('language', 'N/A')}** | 📅 **{date(skill.get('updated_at', ''))}**", "", skill.get("description", "").strip(), ""]
            if skill.get("topics"):
                lines += ["**Tags:** " + " ".join(f"`{tag}`" for tag in skill["topics"][:8]), ""]
            lines += ["---", ""]
    lines += ["## Contributing", "", "Add a quality, reusable Agent Skill by opening a pull request. See [CONTRIBUTING.md](../../CONTRIBUTING.md).", ""]
    target = ROOT / "docs/en/projects.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    shutil.copyfile(target, ROOT / "docs/zh/projects.md")
    shutil.copyfile(ROOT / "data/skills.json", ROOT / "docs/data/skills.json")
    print(f"Generated {target}")


if __name__ == "__main__":
    main()
