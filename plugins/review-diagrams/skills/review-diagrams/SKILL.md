---
name: review-diagrams
description: Draw accurate SVG diagrams for an ADR decision or a substantial PR change, so reviewers can see the design and behavior.
---

# Review diagrams

Read the ADR or PR diff before drawing. For a tiny PR such as a one-file fix or pin bump, skip the diagram. Follow placement overrides in the target project's `AGENTS.md`.

For an ADR, draw the chosen option, responsibility boundaries and labeled data flow. Include rejected alternatives, deferred work, and superseded decisions only when the ADR states them; give each a distinct status label. Save `docs/adr/assets/<adr-name>-<slug>.svg` and embed it in the ADR with a relative image path.

For a PR, compare the base and head. Draw before and after, marking added, changed, and removed parts with distinct colors and explicit text labels. Add a labeled before/after flow if behavior changes. Save `docs/history/changes/<PR>-<slug>/overview.svg`.

Use SVG text elements with deliberate line breaks; do not rely on collapsed whitespace. Use high-contrast text and fills that remain readable in light and dark themes. Label every arrow with what crosses it. Never depict a claim absent from the source text or diff. Use an accessible title and description.

Put `## Overview` at the top of the PR body, embedding each diagram through a `raw.githubusercontent.com/<owner>/<repo>/<full-commit-SHA>/<path>` URL. Refresh the SHA and URLs after every push.

Before sharing, review: Are all claims supported? Are chosen, rejected, deferred, and superseded states distinct? Are boundaries and every arrow clear? Are before/after and add/change/remove labels correct? Is text legible at normal zoom in both themes? Do paths, embeds, and pinned PR URLs resolve?
