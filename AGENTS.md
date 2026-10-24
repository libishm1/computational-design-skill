# AGENTS.md

Shared instructions for coding and research agents working in this repository. Claude Code reads `CLAUDE.md`, which points here. Codex and local agents read this file.

## What this repository is

A set of agent skills. Each skill is `skills/<name>/SKILL.md` plus optional `references/`, `templates/` and `scripts/`.

## Rules for editing skills

1. Keep the frontmatter `name` equal to the folder name. Give `description` at least 80 characters, and say when to use the skill.
2. Write procedures, checklists and templates. Do not write findings, results or conclusions about a field.
3. Do not add file paths from a personal machine, personal names, client or collaborator names, contact details or credentials. Use placeholders such as `<project-dir>`.
4. Link every file a skill refers to, using backtick paths such as `references/x.md`. The validator checks the links.
5. Run `python scripts/validate_skills.py` and `python -m unittest discover -s tests -v` before a commit. Both must pass.
6. Work on a branch. Do not merge to `main` without review.

## Routing

| Task | Skill |
|---|---|
| Grasshopper, GraphML, Topologic, simulation, fabrication | `skills/computational-design/SKILL.md` |
| A crash, exception, hang or load failure in native or managed code | `skills/ai-debugging/SKILL.md` |
| A literature review, gap analysis or cross-disciplinary synthesis | `skills/research-synthesis/SKILL.md` |
| Saving or summarising past agent sessions | `skills/conversation-handoff/SKILL.md` |

## Multi-agent use

A multi-agent run splits the work in this order:

1. Planner reads the task and the routing table, then names the skill and the files.
2. Researcher collects sources under the protocol in `skills/research-synthesis/templates/protocol.md`.
3. Debugger follows `skills/ai-debugging/SKILL.md` and records the reproduction and evidence.
4. Reviewer checks the output against the checklist in the skill it used.

One agent may play several roles when the tool has no subagents. Keep the roles separate in the output.

## Human approval

Agents draft, check and propose. A person approves merges, publication, installs that change the machine, and any claim that will go to a reviewer.
