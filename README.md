# Computational Design Skill for Claude.ai

A Claude.ai user skill for computational design in Architecture, Engineering and Construction (AEC).

Consolidated from [Amanbh997/Claude-skills-for-Computational-Designers](https://github.com/Amanbh997/Claude-skills-for-Computational-Designers) and tailored for:

- **GraphML / GNN research** — Bridge-to-GNN framework (Categories A–D), IFC as heterogeneous graph, PyTorch Geometric patterns, PRISMA search methodology
- **Topologic + IFC spatial reasoning** — CellComplex from IFC, fire egress shortest path, RL evacuation agent
- **Grasshopper teaching** — Student error catalog (10 most common errors), explanation scaffolds for data trees, attractors, Graft
- **Hot-arid / Riyadh climate** — ASHRAE 90.1 targets, Riyadh EPW benchmarks, glazing SHGC, shading fin depth calculation, UTCI outdoor comfort
- **Robotic fabrication** — UR10e + OnRobot RG6 as primary stack; full multi-brand coverage (ABB, KUKA, Fanuc); URScript, RAPID, KRL; HAL Robotics, KUKA|prc, Robots plugin

## Contents

```
skills/
└── computational-design/
    ├── SKILL.md                          # Main skill file (756 lines)
    └── references/
        ├── gh-component-index.md         # 200+ Grasshopper components
        ├── fabrication-specs.md          # CNC, laser, robotic process parameters
        ├── environmental-benchmarks.md   # Daylight, energy, wind, thermal (hot-arid context)
        ├── structural-rules-of-thumb.md  # Span/depth ratios, load cases, material strengths
        └── scripting-patterns.md         # GhPython, RhinoCommon, pyRevit code patterns
```

## Skills Covered

| # | Skill | Key Topics |
|---|---|---|
| 1 | GraphML for AEC | GNN, heterogeneous graphs, IFC→graph, Bridge-to-GNN A–D, PRISMA |
| 2 | Topologic + IFC | CellComplex, fire egress, shortest path, RL evacuation |
| 3 | Parametric Modeling | Grasshopper teaching, data trees, student error catalog |
| 4 | Generative Design | Galapagos, Octopus, Wallacei, NSGA-II, Kangaroo form-finding |
| 5 | Environmental Simulation | Ladybug/Honeybee, hot-arid benchmarks, Riyadh EPW, shading calc |
| 6 | Structural Computation | Karamba3D, Kangaroo, form-finding, SIMP topology optimization |
| 7 | Facade Computation | Panelization, PQ mesh, hot-arid shading strategy |
| 8 | BIM Scripting | pyRevit, IfcOpenShell, Revit API |
| 9 | Scripting Reference | GhPython, RhinoCommon, C# Grasshopper |
| 10 | Robotic Fabrication | UR10e (primary), ABB, KUKA, Fanuc; URScript, RAPID, KRL; HAL, KUKA\|prc |
| 11 | ML for AEC | XGBoost surrogates, SAM/GroundedSAM, LLM task planning, PointNet++ |
| 12 | Optimization Methods | NSGA-II, Bayesian opt, SIMP, pymoo |
| 13 | Interoperability | Speckle, Rhino.Inside, IFC pipelines, format matrix |
| 14 | Mesh Processing | Subdivision schemes, half-edge, mesh quality |
| 15 | Data-Driven Design | GIS, space syntax, Elk, Heron |
| 16 | Design Automation | Rule-based layout, drawing automation |

## Installation

### Option 1 — Claude.ai User Skills (claude.ai interface)

Copy `skills/computational-design/` into your Claude user skills directory:

```bash
cp -r skills/computational-design/ /path/to/claude/skills/user/
```

The skill auto-activates based on topic detection. Trigger keywords include: Grasshopper, parametric, GraphML, GNN, Topologic, Karamba, Ladybug, Honeybee, IFC, Revit API, fabrication, UR10e, robotic, facade, panelization, NSGA-II, and many more.

### Option 2 — Claude Code CLI

```bash
claude --plugin-dir "/path/to/this-repo"
```

## Usage

Once installed, just ask Claude about computational design topics — the skill loads automatically:

```
"How do I build a heterogeneous GNN on an IFC building model?"
→ Skill 1 (GraphML) activates

"Set up a fire egress graph from a Topologic CellComplex"
→ Skill 2 (Topologic) activates

"My students are confused about Grasshopper data trees"
→ Skill 3 (Parametric + Teaching) activates

"What glazing SHGC should I use for a west-facing facade in Riyadh?"
→ Skill 5 (Environmental / hot-arid) activates

"URScript for a pick-and-place sequence on UR10e"
→ Skill 10 (Robotic Fabrication) activates
```

## Context

Built for research at **CM-iTAD Lab, Alfaisal University, Riyadh** — GraphML for AEC, robotic fabrication, and computational design education.

Base plugin: [Amanbh997/Claude-skills-for-Computational-Designers](https://github.com/Amanbh997/Claude-skills-for-Computational-Designers) (MIT License)

## License

MIT
