# Personal Codex Skills

Private registry for personal Codex skills. Skills are organized by category and function, with independent semantic versions.

## Repository layout

```text
skills/
  <category>/
    <function>/
      <skill-name>/
        SKILL.md
        VERSION
        agents/
        references/
        scripts/
registry.yaml
CHANGELOG.md
```

## Categories

| Category | Purpose |
|---|---|
| `writing` | Fiction writing, review, publishing and visual storytelling |
| `data` | Data analysis, SQL, dashboards and platform configuration |
| `project` | Project-specific engineering and knowledge-base workflows |
| `creative` | Image, mascot, cover and creative-production workflows |
| `tooling` | Skill creation, installation, validation and automation |

Use a stable functional subgroup below each category, such as `publishing-compliance`, `knowledge-base`, `workflow-development`, or `visual-storytelling`. Do not place skills directly under `skills/`.

## Versioning rules

Every skill must contain a `VERSION` file using Semantic Versioning:

- `PATCH`: wording fixes, rule clarifications and backward-compatible bug fixes.
- `MINOR`: new checks, references, scripts or backward-compatible capabilities.
- `MAJOR`: breaking workflow, output-contract or directory changes.

For every release:

1. Validate the skill with Codex `skill-creator`'s `quick_validate.py`.
2. Update the skill's `VERSION`.
3. Update `registry.yaml` with category, function, version and date.
4. Add a concise entry to `CHANGELOG.md`.
5. Commit only the intended skill and registry changes.
6. Tag releases as `<skill-name>/v<version>` and push the commit and tag.

The repository itself may use `repo-vX.Y.Z` tags when the registry format or repository-wide conventions change.

## Current skills

See [registry.yaml](registry.yaml) for the authoritative inventory.
