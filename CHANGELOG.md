# Changelog

All notable skill releases and repository-level changes are recorded here.

## Repository 1.3.4 - 2026-09-11

- Moved category-specific installation, quick-use, development and validation instructions into the corresponding directory README files.
- Simplified the root README into a project overview and directory navigation entry point.

## Repository 1.3.3 - 2026-09-11

- Added configurable Planner and Executor selection to `model-router`.
- Documented per-request model, reasoning strength and role assignment while retaining the Astra low → Luna high default.

## Repository 1.3.2 - 2026-09-11

- Replaced the root README's flat skill descriptions with a clear top-level directory overview.
- Added directory-level README files for writing skills, tooling skills and model routing, with links to detailed documentation.

### model-router 2.1.0 - 2026-09-11

- Added per-request Planner and Executor selection for models, reasoning strength and role assignment.
- Preserved Astra low → Luna high as the default while requiring unsupported requested combinations to be reported as blocked.

## Repository 1.3.1 - 2026-09-11

- Reorganized README skill introductions by their `skills/writing/` and `skills/tooling/` directory paths.
- Added the Codex tooling directory to the repository overview and installation documentation.

## Repository 1.3.0 - 2026-09-11

- Published the `model-router` Codex tooling skill under `skills/tooling/model-routing/model-router`.
- Added public documentation, registry metadata and installation examples for the Astra low → Luna high two-dialog workflow.

## Repository 1.2.0 - 2026-08-12

- Added four complementary Chinese-fiction skills for reader cold reads, language proofreading, originality auditing and post-publication performance diagnostics.
- Added public documentation, version metadata and standard-library scripts for the new skills.
- Added a repository-level interoperability guide for `worldwonderer/oh-story-claudecode`, including routing, recommended sequencing, handoff contracts and standalone fallback behavior.
- Expanded the personal `$story` routing reference from two to six optional extensions without changing or claiming ownership of the upstream package.

## Skill releases

### story-prose-style 1.0.2 - 2026-08-12

- Expanded the personal `$story` router integration reference to cover all six complementary skills and link the complete interoperability guide.

### story-reader-cold-read 1.0.0 - 2026-08-12

- Added a two-pass blind-reading protocol that isolates author-only materials before comparing reader experience with author intent.
- Added reader knowledge, expectation debt, friction, drop-off and page-turn ledgers.

### story-chinese-proofreading 1.0.0 - 2026-08-12

- Added conservative Chinese-fiction proofreading for objective wording, syntax, reference, punctuation, numbers and proper-name issues.
- Added `chinese_proofread.py` for deterministic formatting and repetition candidates while protecting intentional character voice.

### story-originality-audit 1.0.0 - 2026-08-12

- Added source-aware audits across wording, scene combinations, structural mappings and creative transformation.
- Added `text_overlap.py` for exact normalized n-gram candidates against user-provided sources, with explicit legal and coverage limits.

### story-serial-performance-diagnostics 1.0.0 - 2026-08-12

- Added data-contract checks, funnel localization, reader-feedback coding, competing hypotheses and minimum validation plans for published serial fiction.
- Added `serial_metrics.py` for transparent chapter-level descriptive metrics and explicit ratios.

## Repository 1.1.1 - 2026-08-12

- Updated public clone URLs after the GitHub username changed to `Perry-Lynn`.

## Repository 1.1.0 - 2026-08-12

- Prepared the registry for public use and updated visibility metadata.
- Added the Apache License 2.0.
- Rewrote the repository README with installation, usage, structure, versioning and safety guidance.
- Added public user documentation for every published skill.

### story-prose-style 1.0.1 - 2026-08-12

- Added a complete public-facing guide with trigger examples, modes, review dimensions and script usage.

### story-fanqie-compliance 1.0.1 - 2026-08-12

- Added a complete public-facing guide with trigger examples, modes, grading and script usage.
- Clarified that the bundled platform policy is a dated, unofficial execution summary.

## Repository 1.0.0 - 2026-08-09

- Created the personal skills registry.
- Established category/function directory conventions and semantic-version rules.
- Added `story-fanqie-compliance` version `1.0.0` under `writing/publishing-compliance`.

### story-prose-style 1.0.0 - 2026-08-09

- Added project-specific prose-style extraction, maintenance, application and drift review.
- Added reusable guidance for natural dialogue, restrained literary narration, plot-first prose, character voice and anti-template boundaries.
- Added `style_fingerprint.py` for descriptive sentence, paragraph, dialogue, punctuation and template-risk comparison.
- Added personal `$story` router integration guidance so style and Fanqie compliance skills complement the upstream story toolbox.

### story-fanqie-compliance 1.0.0 - 2026-08-09

- Added Fanqie platform policy guidance and review rubric.
- Added deterministic preflight checks for repeated paragraphs, engineering metadata, symbol-heavy filler, transaction redirects and platform-bypass language.
- Integrated long-form and short-form story workflows, continuity review and post-deslop revalidation.

### model-router 1.0.0 - 2026-09-11

- Added Astra medium planning and Luna xhigh implementation/verification routing.
- Defined bounded handoffs, replanning, host capability checks and transparent fallback.
- Added Codex discovery metadata; leaves global model configuration unchanged.

### model-router 2.0.0 - 2026-09-11

- Changed default workflow to two explicitly authorized Codex conversations with Astra medium and Luna xhigh.
- Added peer binding, deduplicated handoffs, review and replan states, and checkout-aware single-writer ownership.
- Preserved subagent mode as an optional reference; no global configuration changes.

### model-router 2.0.1 - 2026-09-11

- Changed Planner reasoning to Astra low and Executor reasoning to Luna high in conversation and optional subagent modes.
