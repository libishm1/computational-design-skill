---
name: rhino-grasshopper-authoring
description: Procedure for building, loading, solving, validating and presenting Rhino and Grasshopper work with an AI agent, including MCP control of a running Rhino, plugin loading guards, component solve rules, synchronous versus asynchronous components, self-presenting examples, versioned saves, and canvas validation. Use when an agent drives Rhino or Grasshopper, writes or debugs a Grasshopper component, prepares an example definition, or captures results from a live Rhino session. Rhino and Grasshopper run on Windows or macOS only.
compatibility: Claude, Codex, local models, Herdr and Omarchy as clients. Rhino 8 and Grasshopper run on Windows or macOS. Ubuntu can drive a remote Rhino host.
license: see repository LICENSE
---

# Rhino and Grasshopper authoring

Procedure only. Apply it to your own plugins, definitions, and fixtures. Keep results and
findings out of shared files.

## Platform

Rhino and Grasshopper run on Windows or macOS. From Ubuntu or Omarchy, use a remote Rhino host.
See `references/platform-compatibility.md`.

## 1. Drive a live Rhino through MCP

- Run one MCP server for scripts inside Rhino (the official router) and one bridge for the
  Grasshopper canvas. Do not mix them up.
- Check which Python the script host runs. Use the host's document object, not a global.
  Results come back on standard output.
- Activate the session with the plugin's start command in Rhino. A dialog that only shows
  configuration does not start anything. Confirm the slot appears in the slot list before the
  first call.
- Never make a call without a slot to force one open. A slot-less call can launch a clean Rhino
  with none of your plugins loaded.
- After you change the MCP configuration, restart the agent client. Do not expect a new server to
  appear in the running session.

## 2. Load and deploy plugins safely

- Before a fix counts as failed, restart Rhino. The process keeps the old assembly in memory.
  Disabling a component or a solver does not unload it.
- Check what is loaded, not what is on disk: list the loaded libraries and look up the component
  GUID through the component server.
- Load guard. Call the library scan only when the library count is zero. Scanning again while
  libraries are loaded re-registers every component and causes ID conflicts. On a normal
  relaunch, do nothing.
- Keep one copy of each plugin in the scanned folders. Scanning is recursive, so a duplicate loads
  twice and fails with ID conflicts.
- Disable third-party plugins that break wiring. Disable every copy: the library copy and any
  package-manager copy.
- Confirm the deployed file's size and modification time after each copy. Ask for a full restart
  before you conclude a fix failed.
- Deploy with a command that is not piped into a tool that stops early. An early stop can kill the
  child process mid-copy. Verify the file afterwards.

## 3. Author and solve

- Decide the data match before wiring: item, list, or tree, and the matching type. Grasshopper
  grafts silently when the match is wrong.
- Solve once, then read the outputs. Keep Run inputs off by default, so opening a definition runs
  nothing.
- A component skips its solve when a non-optional input is empty. For either-or inputs, mark the
  alternatives optional, or the second path never runs and only a warning appears.
- Read the red runtime message in full before you change code. Log every failure in the handoff.
- Use absolute paths only.

## 4. Component design

- One canonical type per concept at each component boundary. If you must accept both a custom
  type and a native type, use a generic parameter with a dual-unwrap helper, and report the actual
  type when neither matches.
- Accept the native form and convert internally. The user should not need an extra step.
- Use one ribbon tab per plugin. Group with sub-categories.
- Use meshes, not Breps, for convex polyhedra with planar faces. Triangulate fan-style from the
  first vertex, then compute normals and compact.
- A large one-click component is a facade over the published primitives. It calls the same
  primitives with the same defaults. Keep the primitives available for reuse.
- Before building a component that overlaps a mature external tool, check the tool first. Prefer
  an example workflow that hands the job to it.
- Reuse components. Fork only when tolerances or behaviour differ.
- Put each algorithm's citation in the component's structured attribute and in its hover text.
- Each component serves one named design problem with a stated tolerance and a real fixture. Do
  not ship a demonstration that has no design problem behind it.

## 5. Synchronous or asynchronous

- Default to synchronous.
- Use a background task only for a source or terminal node that loads once and waits, for example a
  large file read or a native solver. Drive it with a Run gate, default false.
- The background task touches plain data only (numeric arrays and point structs). Build every
  geometry object, and run every mesh topology or normal operation, on the UI thread when results
  are emitted.
- Turning Run off cancels the task. The result is discarded when it returns.
- Do not combine a background task with a second full-document solve on each completion. It cascades
  on any upstream change.

## 6. Heavy geometry

- Decimate or remesh a large mesh once, upstream of any heavy operation. Do not loop a reduction
  inside one script; it can exceed the tool's time limit while the work continues on the host.
- For many-cut decomposition, route the cuts through a native CGAL or Geogram backend. Do not fan
  out many RhinoCommon boolean calls on a large mesh.
- Any native entry point that does floating-point work must mask exceptions, or the host crashes.

## 7. Units and tolerances

- Check the document's unit setting before you place anything. Use metres for site, quarry, and
  masonry scale. Use millimetres for shop-scale pieces. Do not mix them in one file.
- Derive tolerances from the characteristic size of the object. A fixed number that works at one
  scale fails at another. The document's default tolerance can be too loose for small parts.
- Keep three quantities separate: numeric epsilon (scaled to size, with a floor), process kerf
  (the tool's cut width), and clearance (a function of size and process).
- Express parameters as fractions of object size, so results compare across scales. Report errors
  as fractions, not raw units.

## 8. Presentation and examples

- The final form appears on the canvas. Use custom preview and gradient components for colour,
  and move, rotate, or orient components for layout. Hide the raw component previews so the custom
  previews own the look.
- Scripts are for headless capture only: baking copies, capturing images, or setting persistent
  data. They are never the step that creates the final visible form.
- Acceptance check: reopen the file cold. Does the capture appear without any script?
- Validate live. Open the file, solve it, confirm the preview has geometry, and confirm no runtime
  errors. Wiring alone does not count.
- Wire every output to every plausible input on a real canvas before you call a plugin finished.
  Headless tests cannot catch conversion failures.
- Do not auto-wire the preview to "the first mesh output". Pick the terminal geometry output and
  check that it carries data on solve.
- Do not add a stability or verification component blindly. On an unsettled input it can report a
  spurious failure that looks like a broken example.

## 9. Captures and saves

- Hide component previews before a viewport capture. Otherwise baked geometry picks up preview
  colours.
- Use shaded display for flat or uncoloured fixtures. Use a light background for diagnostic views.
- Keep image width below the tool's payload limit (about 620 pixels wide, if the JSON cap applies).
  Read downscaled images, not full-resolution ones.
- Show intermediate results often, not only at the end. Bake, capture, and read after each
  substantive solver result, and colour by the metric.
- Save each build as a new numbered file with a short companion note: what changed, layer counts,
  key parameters, and remaining gaps. Never overwrite or delete a working build.
- Save through the document I/O object. Before saving, copy the document and remove the bridge
  component from the copy, so the file has no missing-component placeholder. Do not remove the
  bridge from the live document.

## 10. Checklist before a plugin or example ships

- [ ] Loaded version verified in the running process, not only on disk.
- [ ] One copy of each plugin in the scanned folders.
- [ ] Every component solves from a cold open with Run off.
- [ ] Every output wired to every plausible input on a real canvas.
- [ ] Final form visible without a script; reopened cold.
- [ ] Units set and checked; tolerances derived from size.
- [ ] Algorithm citation in the hover text.
- [ ] Numbered save written with its note.
- [ ] Visual check by the owner on a real Rhino canvas.

## Files

- `references/platform-compatibility.md` - where each step runs.
