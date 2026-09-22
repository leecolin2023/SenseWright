#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("frontmatter is not closed")
    data = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"unsupported frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        if key in data:
            raise ValueError(f"duplicate field: {key}")
        data[key] = value.strip()
    return data

def main():
    paths = [ROOT / "SKILL.md", *sorted((ROOT / "skills").glob("*/SKILL.md"))]
    errors = []
    for path in paths:
        try:
            meta = parse_frontmatter(path)
            if path == ROOT / "SKILL.md" and meta.get("name") != "sensewright":
                errors.append(f"{path.relative_to(ROOT)}: root skill name must be sensewright")
            if set(meta) != {"name", "description"}:
                errors.append(f"{path.relative_to(ROOT)}: frontmatter must contain only name + description")
            if not NAME_RE.fullmatch(meta.get("name", "")):
                errors.append(f"{path.relative_to(ROOT)}: invalid skill name")
            if len(meta.get("description", "")) < 40:
                errors.append(f"{path.relative_to(ROOT)}: description must explain capability and trigger")
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: validated {len(paths)} SKILL.md files")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
