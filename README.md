# Computational Design Skills

Agent skills for computational design, AI-assisted debugging, research synthesis and
session handoff. Works with Claude (claude.ai and Claude Code), Codex and local agents
(Qwen, Llama, or any model behind an OpenAI-compatible endpoint). Each skill is a folder with a
`SKILL.md` file and supporting references, scripts, or templates.

## Skills

| Skill | Use it for | Entry file |
|---|---|---|
| `computational-design` | Grasshopper and parametric modelling, GraphML for AEC, Topologic and IFC, environmental simulation (hot-arid examples), structural rules of thumb, fabrication (CNC, laser, UR10e), scripting patterns | `skills/computational-design/SKILL.md` |
| `ai-debugging` | Debugging native and managed code with an agent: C and C++ (gdb, lldb, cdb, sanitizers), C# and .NET (SOS, dotnet-dump, async, binding), RhinoCommon and Grasshopper plugins | `skills/ai-debugging/SKILL.md` |
| `research-synthesis` | Reproducible literature reviews and gap analysis: PRISMA 2020 counts, per-method extraction cards, ROSES-style cross-disciplinary synthesis, gap ranking, counting and honesty rules | `skills/research-synthesis/SKILL.md` |
| `conversation-handoff` | Local dated digests of past agent sessions, for resuming work | `skills/conversation-handoff/SKILL.md` |

The skills describe methods and checklists. They do not state conclusions about any
field. Fill them with your own sources and results.

## Repository layout

```
skills/
├── computational-design/
│   ├── SKILL.md
│   └── references/        gh-component-index, scripting-patterns, fabrication-specs,
│                          environmental-benchmarks, structural-rules-of-thumb
├── ai-debugging/
│   ├── SKILL.md
│   └── references/        cpp-debugger, csharp-debugger, rhinocommon-debugger
├── research-synthesis/
│   ├── SKILL.md
│   ├── references/        gap-analysis
│   └── templates/         protocol, prisma-flow, extraction-card, roses-synthesis
└── conversation-handoff/
    ├── SKILL.md
    └── scripts/           extract_sessions.py (standard library only)
scripts/validate_skills.py  structure, link, and private-marker checks
tests/                      unit tests for the validator
```

## Install

### Claude.ai (user skills)

Copy one skill folder into your Claude user skills directory:

```bash
cp -r skills/computational-design/ /path/to/claude/skills/user/
```

Skills load by topic. Trigger words in each `description` field tell Claude when to use it.

### Claude Code

Point Claude Code at the repository, or copy the skill folders into `.claude/skills/` in
your project:

```bash
mkdir -p .claude/skills && cp -r skills/* .claude/skills/
```

### Codex and local agents

Read `AGENTS.md` at the repository root. It lists the skills and the rules every agent
follows. Load a `SKILL.md` file as a system or context document when a task matches its
description.

## Check the repository

```bash
python scripts/validate_skills.py     # structure, links, private-marker scan
python -m unittest discover -s tests -v
```

Both commands use only the Python standard library.

## Privacy and contributions

- No file paths, personal names, client names, contact details or credentials belong in a
  skill. The validator fails on them.
- Add a new skill as `skills/<name>/SKILL.md` with frontmatter `name` (equal to the folder
  name) and a `description` of at least 80 characters. Run the validator before opening a
  pull request.

## Origin

`computational-design` extends
[Amanbh997/Claude-skills-for-Computational-Designers](https://github.com/Amanbh997/Claude-skills-for-Computational-Designers)
(MIT). Other skills are original to this repository. See `LICENSE`.

## License

MIT. See `LICENSE`.
