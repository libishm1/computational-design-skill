"""Validate the skills in this repository.

Checks, for every skills/<name>/SKILL.md:
  1. Frontmatter has name (equal to the folder name) and a description of at
     least 80 characters.
  2. Every relative file reference in the SKILL.md body exists.
  3. No private markers appear in any text file: local drive paths, user
     folder paths, email addresses, personal or client names, and token-like
     strings. The tests/ folder and this script are excluded because the
     tests hold deliberately bad fixtures.

Usage:
    python scripts/validate_skills.py [--root <repo-root>]

Exit code 0 when all checks pass, 1 otherwise.
"""

import argparse
import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".py", ".txt", ".json", ".yml", ".yaml", ".toml"}
MIN_DESCRIPTION = 80

# Private markers. Extend this list when a new personal name or path appears.
PRIVATE_PATTERNS = [
    (re.compile(r"[A-Za-z]:\\"), "local drive path"),
    (re.compile(r"[A-Za-z]:/(?:Users|code_ws|Template)", re.IGNORECASE), "local drive path"),
    (re.compile(r"/c/Users/", re.IGNORECASE), "local user path"),
    (re.compile(r"/Users/[A-Za-z]", re.IGNORECASE), "local user path"),
    (re.compile(r"Template-General/|frahan_stonepack|d--code-ws", re.IGNORECASE), "workspace path"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "email address"),
    (re.compile(r"\blibish\b|\bMurugesan\b", re.IGNORECASE), "personal name"),
    (re.compile(
        r"\bkuppam\b|\balbion\b|\bpoultney\b|\bwardell\b|\bpierre\b|\blupus\b|\bquarra\b|\balfaisal\b",
        re.IGNORECASE), "client or collaborator name"),
    (re.compile(r"\bghp_[A-Za-z0-9]{20,}|\bsk-[A-Za-z0-9]{20,}|\bAKIA[0-9A-Z]{16}"), "token-like string"),
]

LINK_RE = re.compile(r"`((?:references|templates|scripts|assets)/[^`\s]+)`")
FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter(text):
    m = FRONT_RE.match(text)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def check_skill(skill_dir):
    problems = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir.name}: missing SKILL.md"]
    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        problems.append(f"{skill_dir.name}: no frontmatter block")
        return problems
    if fm.get("name") != skill_dir.name:
        problems.append(f"{skill_dir.name}: frontmatter name is {fm.get('name')!r}, expected folder name")
    if len(fm.get("description", "")) < MIN_DESCRIPTION:
        problems.append(f"{skill_dir.name}: description shorter than {MIN_DESCRIPTION} characters")
    for rel in sorted(set(LINK_RE.findall(text))):
        if not (skill_dir / rel).exists():
            problems.append(f"{skill_dir.name}: referenced file missing: {rel}")
    return problems


def scan_private(root):
    problems = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if ".git" in path.parts or "tests" in path.parts or path.name == "validate_skills.py":
            continue
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            for rx, label in PRIVATE_PATTERNS:
                if rx.search(line):
                    problems.append(f"{rel}:{lineno}: {label}")
    return problems


def run(root):
    problems = []
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return [f"no skills/ directory under {root}"], 0
    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir())
    for sd in skill_dirs:
        problems.extend(check_skill(sd))
    problems.extend(scan_private(root))
    return problems, len(skill_dirs)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    args = ap.parse_args(argv)
    problems, count = run(Path(args.root))
    for p in problems:
        print(f"FAIL {p}")
    print(f"{count} skill(s) checked, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
