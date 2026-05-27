# Reference: Skills catalog

Annotated index of the PortDive Skills library, scoped to what's useful for investment-research workflows. Discover live state with `list_skills` (filterable by `category`, `tags`, `scope`, `language`). Pull a full skill body + parameters with `get_skill(slug)`.

For composition rules (standalone vs playbook vs composable), see [patterns/skill-chain-composition](../patterns/skill-chain-composition.md).

---

## Composable frameworks (`{include:slug}`)

These are rule-sets embedded in other skills, not invoked directly. Use them inside skills you author so framework versions stay in sync.

| Slug | What it provides |
|---|---|
| `elliott-wave-rules` | Full Elliott Wave principle: motive (impulse, diagonal) + corrective (zigzag, flat, triangle, combinations) rules and guidelines. |
| `wyckoff-method-rules` | Wyckoff method: three laws, Composite Man, accumulation/distribution schematics (PS, SC, AR, ST, Spring, SOS, LPS, PSY, BC, SOW, LPSY, UTAD), five phases (A–E), nine buy / nine sell tests. |
| `technical-indicators-rules` | Interpretation thresholds + decision weights for RSI(14), MACD(12/26/9), Williams %R(14), Stochastic(14/3/3), ADX(14)+DI, volume. |
| `signal-decision-matrix` | Buy/sell signal thresholds with weighted rules, Elliott-context adjustments, Fibonacci-context adjustments, contradiction-resolution hierarchy. |
| `long-strategy-rules` | LONG-STRATEGY framework: core thesis, entry rules (Tier 1–3 scaling), exit rules (Trim 1–3, Exit 1–2, Emergency), position sizing, kill switches. |
| `bayesian-framework` | Structured scenario framework with prior/posterior probabilities, evidence weighting, action derivation. |
| `classical-pattern-detection` | Edwards & Magee / Bulkowski taxonomy: wedges, triangles, head-and-shoulders, flags, channels from OHLCV. |

---

## Verification / data

| Slug | Type | When to reach for it |
|---|---|---|
| `data-verification` | standalone | Multi-source price + fundamentals triangulation (P/E, P/S, EV/EBITDA, 52w range, technicals, insider/institutional flows). Run before any analysis when source quality is uncertain. |
| `macro-risk-overlay` | standalone | Eight-step macro regime read: VIX (CBOE), USDJPY (FX), US10Y (TVC), BTCUSD (COINBASE), XAUUSD (FX), USOIL (FX), calendar risks, geopolitical tail risks. Emits kill-switch proximity (None / Watch / Alert / Triggered). Run before any position decision and on regime-change days. |

---

## Analysis (standalone)

| Slug | When to reach for it |
|---|---|
| `swot-analysis` | Evidence-based SWOT for a ticker. OHLCV (`analysis_mode: "swot-analysis"`) + web research budget of 30s. Each bullet must cite evidence. Output: structured 4-quadrant + synthesis paragraph. |
| `fundamental-valuation` | 4-method valuation: comparables (P/S, EV/EBITDA), DCF with sensitivity, TAM projection, analyst consensus. Emits a typed `valuation` artefact strictly conforming to `valuation.v2.schema.json` — read the schema from the MCP resources first, build the v2 payload, deliver via `complete_skill_execution(artifacts: [{kind: "valuation", payload_json: ...}])`. |
| `catalyst-peer-analysis` | Company-specific catalyst mapping (past + upcoming), analyst consensus + targets, peer-group identification + comparative multiples, sector relative strength, catalyst timeline with dead-catalyst rules. Emits a `catalyst_analysis` artefact (free-form JSON, no strict schema yet). |
| `warren-buffett-lens` | Buffett-style balance-sheet stress test + Sum-of-the-Parts decomposition for conglomerates. Inventory obsolescence, customer concentration, ROE sustainability, moat risks. Use for value-investing audits, deep dives on conglomerates. |
| `elliott-wave-analysis` | 7-phase OHLCV-driven wave-count: data ingest, trend detection, mode classification, wave extraction, indicator confirmation, Fibonacci roadmap, scenario generation. |
| `wyckoff-analysis` | 7-phase Wyckoff analysis: data ingest, structure assessment, three-laws application, VSA, schematic identification, event mapping with the Nine Tests, phase determination + trade setup. |
| `bayesian-risk-assessment` | Multi-signal risk scoring with Bayesian probability across scenarios. Aggregates market data + indicators + wave counts + signals. |

---

## Playbooks (multi-step DAGs)

Invoke with `run_skill(slug)` end-to-end, or `run_skill(slug, step_id=<id>)` per step.

### `investment-analysis-playbook` (id=41, 6 steps)
The flagship comprehensive analysis. Produces a single typed `investment_analysis` artefact with 9 card sections: Executive Summary, Company Overview, Core Business Thesis, Key Catalysts, Sector Market Overview, Competitive Landscape, Sector Sentiment, SWOT, Thesis Verdict.

Steps (from `get_skill` `steps`):
1. `company-overview` (always runs)
2. `catalysts` — read-first via `catalyst-peer-analysis`
3. `valuation` — read-first via `fundamental-valuation`
4. `sector-context` — macro regime + sector dynamics
5. `swot` — barrier; depends on 1–4 via `swot-analysis`
6. `synthesis` — emits the final artefact via `investment-verdict-synthesis`

Scopes: `ticker` (default) / `thesis` (loads thesis structure, aggregates across items) / `basket` (focuses on one basket).

### `long-strategy-playbook` (9 steps, PREMIUM tier)
End-to-end LONG-STRATEGY DAG with parallel analysis phases and read-first optimization. Combines data verification, macro overlay, catalysts, Elliott Wave, valuation, Bayesian scenarios, then synthesizes via `long-strategy-synthesis`. Use for high-conviction position-build cases.

### `event-driven-options-playbook` (6 steps)
Event-driven options DAG: T0 `event-context` → T1 parallel (`catalyst-intel`, `technical-state`, `macro-overlay`) → T2 Bayesian scenarios → T3 `options-strategy-synthesis`. Emits typed `options_playbook` artefact. Supports ticker / basket / thesis scope (multi-ticker emits one artefact per underlying).

### `200ma-mean-reversion-playbook`
Long-only DAG for blue-chip equity mean reversion to the 200-period MA on 1D / 1W. Grades four variables (V1 capitulation, V2 basing structure, V3 extension from 200-MA, V4 trigger freshness + multi-TF confirm) → A+/A/B+/B/C/F. Macro kill-switch gates entry. Emits `mean_reversion_trade_plan`.

### `rate-options-portfolio` (2 steps)
Rates all open options positions on a ticker, detects behavioral patterns, recommends per-position. Step 2 is `rate-options-portfolio-synthesize`.

---

## Synthesizers (terminal steps in playbooks)

These are usually invoked indirectly as the final step of a playbook, but are listable + invocable standalone when scenarios + context are already in the conversation.

| Slug | Parent playbook |
|---|---|
| `investment-verdict-synthesis` | `investment-analysis-playbook` |
| `long-strategy-synthesis` | `long-strategy-playbook` |
| `options-strategy-synthesis` | `event-driven-options-playbook` |
| `rate-options-portfolio-synthesize` | `rate-options-portfolio` |
| `event-context` | T0 step of `event-driven-options-playbook` |
| `rate-options-trade` | Per-position options rating (used inside `rate-options-portfolio`). |

---

## Utilities

| Slug | When to reach for it |
|---|---|
| `capture-broker-position` | Extract an open options/warrant position from a broker screenshot; imports into "My Positions." iOS share-to-PortDive flow. |
| `portdive-v5-pdf-exporter` | Generate print-ready PDF report using PortDive V6.2 design tokens (Geist + Lora Italic typography, four-color data semantics). Use as the export step after any analysis artefact is finalized. |

---

## Thesis templates (for `create_thesis`)

`list_thesis_templates` returns 5 starters. Each ships a `gist_scaffold` (markdown skeleton) + `suggested_baskets` (name + description).

| Template ID | Use when |
|---|---|
| `thematic-equity` | The case is anchored on a sector / technology theme (AI, semis, renewables). Suggested baskets: *Kernpositionen* / *Wachstumswerte* / *Zulieferer*. Default for bottleneck-driven theses. |
| `factor-style` | The case is anchored on a factor: Quality, Value, Momentum, Low Vol. Suggested baskets: *Quality* / *Value* / *Momentum*. |
| `macro-hedge` | Defensive positioning for a macro scenario (recession, inflation, geopolitical). Suggested baskets: *Defensive Aktien* / *Sachwerte* / *Anleihen-Proxys*. |
| `sector-rotation` | Cyclical-driven over/underweighting by sector. Suggested baskets: *Übergewichten* / *Neutral* / *Untergewichten*. |
| `income-dividend` | Dividend income / capital return focus. Suggested baskets: *Dividendenaristokraten* / *Hohe Rendite* / *Dividendenwachstum*. |

Templates are scaffolds; populate baskets via `add_basket` + `manage_basket_items` after creation.

---

## Loop-step → skill mapping

Quick map from each step of the [research-loop](../patterns/research-loop.md) to the skills typically used:

| Loop step | Primary skills |
|---|---|
| 1. Catalyst spot | (manual) — primary source reading |
| 2. Bottleneck-first | (manual) — but `catalyst-peer-analysis` supports supply-chain mapping |
| 3. Liquidity verification | `list_available_tickers` (MCP, not a skill) |
| 4. Skill-chain validation | `investment-analysis-playbook` end-to-end; or `data-verification` → `catalyst-peer-analysis` → `swot-analysis` → `fundamental-valuation` → `macro-risk-overlay` |
| 5. Server thesis creation | `list_thesis_templates` + `create_thesis` (MCP); optionally `suggest_thesis_structure` |
| 6. Local artefacts | (manual) — write `THESIS.md` + `RESEARCH_LOG.md` |
| 7. Monitor | `get_thesis_health`, `get_thesis_signals`, `get_thesis_performance`; alpha log via [doctrine/log-thesis-events](../doctrine/log-thesis-events.md) |
