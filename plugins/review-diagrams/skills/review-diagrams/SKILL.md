---
name: review-diagrams
description: Draw accurate SVG diagrams for an ADR decision or a substantial PR change, so reviewers can see the design and behavior.
---

# Review diagrams

Read the ADR or PR diff first; skip tiny PRs (one-file fix, pin bump). Save location: where the project's `AGENTS.md` says. Otherwise follow the project's existing pattern of committed diagrams or records: keep its layout and naming scheme, derive file stems from its record names, and name that pattern in the PR body. Use the defaults below only if neither exists.

Before drawing, read the matching sample beside this file (`examples/decision.svg` for an ADR, `examples/change.svg` for a PR) and keep its palette, theme switch and notation unless the project's existing diagrams use another. If the host offers an `artifact-diagramming` skill, load it for technique; still commit an SVG file to the repository, never publishing it as an Artifact or any hosted page.

For an ADR, draw the chosen option, responsibility boundaries and labeled data flow. Include rejected alternatives, deferred work, and superseded decisions only when the ADR states them, each with a distinct status label. Save `docs/adr/assets/<adr-name>-<slug>.svg` and embed it in the ADR by relative path.

For a PR, draw base (before) and head (after), marking added, changed, and removed parts with distinct colors and text labels, plus a labeled flow if behavior changes. Save `docs/history/changes/<PR>-<slug>/overview.svg`.

Break lines with explicit `tspan`s, never collapsed whitespace. Label every arrow with what crosses it. Depict no claim absent from the source text or diff. Add an accessible title and description.

Open the PR body with `## Overview`, embedding each diagram as `https://github.com/<owner>/<repo>/blob/<full-commit-SHA>/<path>?raw=true`, which renders in private repositories. Refresh after every push.

Before sharing, review: Are all claims supported? Are chosen, rejected, deferred, and superseded states distinct? Are boundaries clear and every arrow labeled, with no crossings or clipped labels? Are before/after and add/change/remove labels correct? Is text legible at normal zoom in both themes? Is each diagram saved where this project keeps diagrams? Do paths, `?raw=true` embeds, and pinned PR URLs resolve?
