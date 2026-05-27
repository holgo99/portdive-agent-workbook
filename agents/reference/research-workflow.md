# Reference: Research workflow (one-page quick reference)

Compact map of the [research-loop](../patterns/research-loop.md) to specific MCP tools, skills, and CLI commands. For the full doctrine, read the pattern. Use this page when you've internalised the loop and just need to remember "what do I call at step 4?"

## At a glance

| Step | What | Surface |
|---|---|---|
| 1 | Catalyst spot | Primary source reading. Capture verbatim in `RESEARCH_LOG.md`. |
| 2 | Bottleneck-first | Manual reasoning; [doctrine/bottleneck-first-analysis](../doctrine/bottleneck-first-analysis.md). |
| 3 | Liquidity verification | `list_available_tickers` (MCP). Check staleness flags per exchange. |
| 4 | Skill-chain validation | `run_skill("investment-analysis-playbook")` end-to-end; or step-by-step per [patterns/skill-chain-composition](../patterns/skill-chain-composition.md). |
| 5 | Server thesis creation | `list_thesis_templates` → `create_thesis` → `add_basket` → `manage_basket_items` (always with `exchanges`). |
| 6 | Local artefacts | Write `theses/<slug>/THESIS.md` + `RESEARCH_LOG.md` + `assets/`. Pair via `Server Thesis: <thesis_id>`. |
| 7 | Monitor | `get_thesis_health`, `get_thesis_signals`, `get_thesis_performance`. Alpha-log thesis events per [doctrine/log-thesis-events](../doctrine/log-thesis-events.md). |

## Surface selection cheatsheet

- **Structured data on the server** (theses, baskets, items, signals, performance, alpha log) → **MCP**.
- **Long-form narrative + visuals** → disk `THESIS.md` + `RESEARCH_LOG.md` + `assets/`.
- **Batch / scripted / file-system work** → `portdive` CLI ([reference/portdive-cli](portdive-cli.md)).
- **Reusable analysis logic** → `run_skill` against the existing [skills catalog](skills-catalog.md). Don't reimplement what `investment-analysis-playbook` already does.

## Common failure modes

- **Disk drift** — disk allocation doesn't match server allocation. Fix: server is canonical ([doctrine/server-is-canonical-for-theses](../doctrine/server-is-canonical-for-theses.md)).
- **Stale OHLCV** — silently using a stale exchange. Fix: read staleness flags from `list_available_tickers`; suggest an alternative exchange or flag the quality concern.
- **Missing `exchanges`** — `manage_basket_items` without an `exchanges` array. Result: OHLCV ingestion can't run for the item.
- **Alpha-log noise** — logging every research finding instead of thesis-level events only. Fix: per-finding goes to `RESEARCH_LOG.md`; alpha log is for structural events.
- **`limit=N` on `get_ohlcv_with_indicators`** — use `analysis_mode` instead so the server picks the right candle window for the analysis.
- **Bypassing read-first** — re-running expensive playbook steps when an artefact already exists. Trust `read_first: true` on `catalysts` and `valuation` steps.
