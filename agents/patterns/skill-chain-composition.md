# Pattern: Composing skills

PortDive skills come in three shapes. Knowing which is which lets you compose them efficiently and avoid redundant work.

## The three shapes

### 1. Standalone skill
A single-prompt skill that does one thing. Invoke via `run_skill(slug)` with the skill's parameters. Returns either an artefact directly (when run synchronously) or an `execution_id` to claim via the tandem-experience flow.

Examples: `swot-analysis`, `fundamental-valuation`, `catalyst-peer-analysis`, `data-verification`, `macro-risk-overlay`, `warren-buffett-lens`.

### 2. Playbook (DAG)
A multi-step DAG. The skill metadata has `type: "playbook"` and a `steps` array describing dependencies (`depends_on`), gates (`none` / `confirm`), and read-first optimisation (`read_first: true` checks for an existing artefact before re-running an expensive step).

Invoke the whole playbook with `run_skill(slug)`. Or resolve one step at a time with `run_skill(slug, step_id=<id>)` — useful when you want to inspect intermediate output before committing to the next step, or when a long-running step needs explicit confirmation.

Examples: `investment-analysis-playbook` (6 steps, see its `steps` field for the DAG: `company-overview` → parallel(`catalysts`, `valuation`, `sector-context`) → `swot` → `synthesis`), `long-strategy-playbook` (9 steps), `event-driven-options-playbook` (6 steps), `200ma-mean-reversion-playbook`, `rate-options-portfolio` (2-step).

### 3. Composable framework
Skills with `composable: true` aren't meant to be invoked directly. They're rule-sets embedded inside other skills via `{include:slug}` substitution.

Examples: `elliott-wave-rules`, `wyckoff-method-rules`, `technical-indicators-rules`, `signal-decision-matrix`, `long-strategy-rules`, `bayesian-framework`, `classical-pattern-detection`.

If you find yourself manually reproducing the rules from one of these inside a prompt, use the include instead — it stays in sync as the framework version bumps.

## Composition rules

- **Read-first when available.** Playbook steps marked `read_first: true` (e.g. `catalysts`, `valuation` in `investment-analysis-playbook`) check the server for an existing artefact before re-running. Trust the optimisation; don't bypass it.
- **Respect gates.** Steps with `gate: "confirm"` block on user confirmation. In an agent loop, surface the gate to the user — don't auto-confirm.
- **Validate before publishing.** When you author or edit a playbook (out of scope for this repo — see "Skills hosting" decision), `validate_playbook_dag` before pushing. Catches cycles, missing dependencies, schema drift.
- **Synthesizer steps cap each playbook.** Names like `investment-verdict-synthesis`, `long-strategy-synthesis`, `options-strategy-synthesis`, `rate-options-portfolio-synthesize` are the **only** step that emits the typed final artefact. Other steps emit intermediate state consumed by the synthesizer.
- **Tandem-experience lifecycle.** When a skill is claimed via `claim_pending_skill_execution`, the dispatched agent runs the body, then must call `complete_skill_execution` with structured artefacts in the `artifacts[]` parameter (not embedded in `output_markdown`). On unrecoverable failure: `fail_skill_execution` with a clear error message.

## When to reach for which

- Need one analysis on one ticker? → standalone skill.
- Want the full nine-card composite? → `investment-analysis-playbook` end-to-end.
- Want a specific stage with control over inputs? → playbook with `step_id`.
- Authoring a new analysis prompt that needs Elliott Wave / Wyckoff / Bayesian rules? → `{include:slug}` to the matching composable framework. Don't paste the rules inline.

## See also

- [reference/skills-catalog](../reference/skills-catalog.md) for the full annotated catalog.
- [reference/portdive-mcp](../reference/portdive-mcp.md) for the underlying tool surface.
