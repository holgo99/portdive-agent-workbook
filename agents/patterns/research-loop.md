# Pattern: The PortDive research loop

A reusable seven-step pipeline for going from "I have a hypothesis" to a paired server + disk thesis that the PortDive ecosystem can monitor.

## The loop

### 1. Catalyst spot
Narrative hypothesis grounded in a **primary source** — a management interview, a SEC filing, a regulator publication, a TrendForce / GF Overseas report. Not a viral X thread that summarizes one. Capture the source verbatim in the research log; the catalyst is not real until you've read the original.

### 2. Bottleneck-first
What physical, material, or capacity constraint anchors the case? Apply [doctrine/bottleneck-first-analysis](../doctrine/bottleneck-first-analysis.md). Identify the upstream monopoly (e.g. Ajinomoto ABF film, Sakai Chemical Barium Titanate) before any proxy selection. If you can't name the bottleneck, the case isn't ready.

### 3. Liquidity verification
For each candidate proxy, confirm tradability via `list_available_tickers` on the PortDive MCP. Note `exchanges` and any **staleness flags** the server returns — stale data degrades downstream signals. A bottleneck leader that isn't tradable on the user's brokers goes to the **Health Basket** (signal-only), and a vertical proxy is substituted. See [pitfalls/proxy-market-liquidity](../pitfalls/proxy-market-liquidity.md) and [pitfalls/sakai-chemical-liquidity](../pitfalls/sakai-chemical-liquidity.md). The substitution logic lives in [patterns/health-basket-construction](health-basket-construction.md).

### 4. Skill-chain validation
Run the analysis suite against the candidate tickers. The fast path is `run_skill` on `investment-analysis-playbook` (a 6-step DAG: company overview → catalyst-peer-analysis → fundamental-valuation → sector-context → swot-analysis → investment-verdict-synthesis). Per-step invocation is also available — see [patterns/skill-chain-composition](skill-chain-composition.md). Cross-check against `macro-risk-overlay` for the regime read.

### 5. Server thesis creation
The server is canonical ([doctrine/server-is-canonical-for-theses](../doctrine/server-is-canonical-for-theses.md)). Create via `create_thesis`, picking a template from `list_thesis_templates` when one fits (`thematic-equity` for most bottleneck cases, `sector-rotation` for cyclical setups, `factor-style` for style tilts). Add baskets via `add_basket` and items via `manage_basket_items` — **always** pass the `exchanges` array on each item (per MCP server instructions).

### 6. Local artefacts
Write `theses/<slug>/THESIS.md` per [reference/thesis-spec](../reference/thesis-spec.md). Include `Server Thesis: <thesis_id>` in the metadata block (linkback to the server). Companion `RESEARCH_LOG.md` per [reference/research-log-spec](../reference/research-log-spec.md). Place visual anchors in `theses/<slug>/assets/` with `*Source: ...*` attribution under each image.

### 7. Monitor
Going forward, the case lives on:
- `get_thesis_health` for the aggregated rubric.
- `get_thesis_signals` for current STA/MTA reads on each item.
- `get_thesis_performance` for equal-weight returns since creation.
- The alpha log surfaces auto-emitted system events plus the analyst-authored thesis events you add per [doctrine/log-thesis-events](../doctrine/log-thesis-events.md).

A loop iteration closes when the thesis transitions ACTIVE → WATCH or WATCH → CLOSED, an exit trigger fires, or the underlying bottleneck dissolves.

## Where it diverges

- **Skip step 5** if the disk thesis is still draft. Don't create on the server until the bottleneck + liquidity work is done.
- **Skip step 4** for already-validated cases (e.g. an update to an existing thesis). Skill chain is for net-new ideas.
- **Reorder steps 1↔2** for opportunistic finds: sometimes a screen surfaces an unfamiliar name and the bottleneck identification follows the discovery rather than preceding it. Either order works; both steps must happen.

## What this pattern replaces

The old "feature-rollout" / "tracker-branch" / "submodule pointer bump" workflow from the PortDive app monorepo does not apply here. This is a research workbook, not a code repo.
