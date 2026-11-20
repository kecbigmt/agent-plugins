---
name: review-diagrams
description: Draw accurate SVG diagrams for an ADR decision or a substantial PR change, so reviewers can see the design and behavior.
---

# Review diagrams

Read the ADR or PR diff first; skip tiny PRs. Save location: per the project's `AGENTS.md`. Otherwise follow the existing pattern of committed diagrams or records (layout, naming scheme, file stems from record names), naming it in the PR body; else the defaults below.

First read the sample beside this file (`examples/decision.svg` for an ADR, `examples/change.svg` for a PR) and reuse its palette, theme switch and notation unless the project's diagrams differ. If the host offers an `artifact-diagramming` skill, load it for technique; still commit an SVG file to the repository, never publishing it as an Artifact.

For an ADR, draw the chosen option, responsibility boundaries and data flow. Show rejected, deferred, and superseded options only when the ADR states them, each with a distinct status label. Save `docs/adr/assets/<adr-name>-<slug>.svg` and embed it in the ADR by relative path.

For a PR, draw one picture of the head structure. Boxes are real components (process, service, module, store, session): a name, at most a short qualifier, no sentences; explain in the PR body. Mark the diff: added and changed parts in distinct colors with text labels, removed parts as faded dashed ghosts in their old place. Draw a before picture only if the structure's shape changes; say why. Save `docs/history/changes/<PR>-<slug>/overview.svg`.

Label every arrow with what crosses it (message, event, file, call). Break lines with explicit `tspan`s. Add `<title>` and `<desc>`.

Open the PR body with `## Overview`, embedding each diagram as `https://github.com/<owner>/<repo>/blob/<full-commit-SHA>/<path>?raw=true` (renders in private repositories); refresh per push.

Before sharing, review: Is every claim in the source or diff? Could a bullet list replace the diagram without losing information? If so, redraw. Are statuses distinct and correctly labeled? No crossings or clipped labels? Is text legible in both themes? Is each diagram saved where this project keeps diagrams? Do paths, `?raw=true` embeds, and pinned PR URLs resolve?
