# kecbigmt's Agent Plugins

A collection of plugins for Claude Code and Codex.

## Installation

### Claude Code marketplace

```bash
# Add the marketplace
/plugin marketplace add kecbigmt/agent-plugins

# Install the story-driven plugin
/plugin install story-driven@kecbigmt-plugins

# Install the review-diagrams plugin
/plugin install review-diagrams@kecbigmt-plugins
```

### Codex 0.162+ marketplace

```bash
codex plugin marketplace add kecbigmt/agent-plugins
codex plugin add review-diagrams@kecbigmt-plugins
```

The verified Codex catalog is `.agents/plugins/marketplace.json`. It points to `plugins/review-diagrams`, whose `.codex-plugin/plugin.json` declares `"skills": "./skills/"`. Claude Code uses `.claude-plugin/marketplace.json` and the plugin's `.claude-plugin/plugin.json`; both hosts load the same `skills/review-diagrams/SKILL.md`.

Codex supports project plugin enabling for trusted repos through `.codex/config.toml`:

```toml
[plugins."review-diagrams@kecbigmt-plugins"]
enabled = true
```

Set `enabled = false` to disable it for that project. The marketplace and plugin still need to be installed once using the commands above. See the [official Codex plugin documentation](https://developers.openai.com/plugins/build/plugins#enable-or-disable-a-plugin-for-a-repo).

## Plugins

### story-driven

Story-driven Development workflow plugin for Claude Code. Provides skills and commands for user story creation, acceptance criteria, verification, and story log management.

### review-diagrams

The shared `review-diagrams` skill creates SVG decision diagrams for ADRs and change diagrams for substantial PRs. It checks claims against the source, labels flows, and makes before/after changes easy to review. Tiny PRs can skip a diagram.

### codex

Codex CLI integration for autonomous code analysis, reviews, and codebase queries. Executes the codex tool with real-time execution visibility for deep codebase understanding.

## Testing Locally

To test plugins during development:

```bash
git clone https://github.com/kecbigmt/agent-plugins.git
claude --plugin-dir ./agent-plugins/plugins/story-driven
```

Restart Claude Code after making changes to pick up updates.

## story-driven Usage

```
/story-driven:start                    # Start workflow (interactive)
/story-driven:start <free text>        # Start with intent
```

Examples:
```
/story-driven:start
/story-driven:start add login feature
/story-driven:start verify
```

## codex Usage

The codex plugin provides the `codex-exec` skill that automatically activates when you request code analysis or reviews.

Examples:
```
"Review the authentication module for security vulnerabilities"
"Analyze the database query patterns for performance issues"
"Explain how the user registration flow works"
"Find potential bugs in error handling code"
```

Claude will automatically execute the codex CLI tool with appropriate parameters.

## Skills

Skills are model-invoked and activate based on workflow phase.

| Skill | Phase |
|-------|-------|
| `defining-stories` | Define |
| `implementing-stories` | Implement |
| `verifying-stories` | Verify |
| `accepting-stories` | Accept |
| `publishing-stories` | Publish |

## Workflow

1. **Define** → User story with acceptance criteria (in story log)
2. **Implement** → TDD inner loop (red-green-refactor)
3. **Verify** → Developer self-testing
4. **Accept** → Product owner testing (timing flexible)
5. **Publish** → Commit, push, optionally create PR

## Acceptance Testing Flexibility

The timing of acceptance testing adapts to your workflow:

| Workflow | Flow |
|----------|------|
| Pre-commit | Verify → Accept → Commit → Push |
| Pre-push | Verify → Commit → Accept → Push |
| Post-PR | Verify → Commit → Push → Draft PR → Accept → Ready |

## Example Usage

Ask Claude naturally:

- "Help me create a user story for adding dark mode"
- "I need to implement the login feature from this story"
- "Run developer verification on my changes"
- "Let's do acceptance testing for the sync-init story"
- "Commit these changes and create a draft PR"

Claude will automatically use the relevant skill.

## story-driven Plugin Structure

```
plugins/story-driven/
  commands/
    start.md                # /story-driven:start command
  skills/
    defining-stories/
    implementing-stories/
    verifying-stories/
    accepting-stories/
    publishing-stories/
```

## License

MIT
