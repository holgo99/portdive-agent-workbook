# Reference: PortDive MCP

The PortDive MCP at `https://mcp.portdive.app/mcp` is the primary operating surface for this repo. This page catalogs the tools by subsystem with a one-line "when to reach for this" each. For full schemas, call the tool's `--describe` equivalent or inspect the response — descriptions evolve.

## Data freshness rule

`list_available_tickers` returns per-exchange staleness flags. **Stale data degrades every downstream signal** — OHLCV indicators, MTA snapshots, skill outputs. When stale: suggest an alternative exchange to the user, flag the quality concern in the analysis, or skip the ticker. Don't silently consume stale data.

## Theses (server-canonical)

The server thesis is canonical for structure (see [doctrine/server-is-canonical-for-theses](../doctrine/server-is-canonical-for-theses.md)). Disk `THESIS.md` pairs by `thesis_id`.

| Tool | When to reach for it |
|---|---|
| `list_theses` | Browse own / official / public theses; resolve `thesis_id` for a disk pair. Output can exceed token limits — page or filter. |
| `get_thesis` | Load full thesis structure (baskets + items + allocations + attached skills) before edits. |
| `create_thesis` | Spin up a new thesis, optionally from a `list_thesis_templates` scaffold. |
| `update_thesis` | Change top-level metadata: title, status, gist, horizon, epicenter. |
| `delete_thesis` | Retire a thesis permanently. |
| `suggest_thesis_structure` | LLM-side structural suggestion when scaffolding a new thesis. |
| `list_thesis_templates` | The 5 starter templates: `thematic-equity`, `factor-style`, `macro-hedge`, `sector-rotation`, `income-dividend`. Each ships a `gist_scaffold` + `suggested_baskets`. |
| `get_thesis_health` | Aggregated health card: structure + signals + performance + freshness warnings. Use for cold-start audit of an existing thesis. |
| `get_thesis_performance` | Equal-weight returns since creation across all items. |
| `get_thesis_signals` | Current STA/MTA signal reads per item. |
| `get_thesis_history` | Version history of structural changes. |
| `list_thesis_skills` | Skills attached to the thesis. |
| `attach_skill_to_thesis` | Bind a skill (typically an analysis playbook) to a thesis for one-tap running. |

## Baskets + items

Baskets group items within a thesis with a strategic role, allocation, and entry/exit rules.

| Tool | When to reach for it |
|---|---|
| `add_basket` | Add a basket to a thesis. |
| `update_basket` | Change basket-level fields (name, description, allocation %, entry/exit rules). |
| `manage_basket_items` | Add / update / remove items in a basket. **Always** pass the `exchanges` array per item (primary exchange first); without it, OHLCV ingestion can't run. |

## Alpha log

The alpha log is the timeline. STA/MTA auto-emits `SIGNAL` / `SNAPSHOT` / `DRIFT` events at ~hourly cadence per tracked ticker. Analyst-authored entries should be thesis-level annotations only (see [doctrine/log-thesis-events](../doctrine/log-thesis-events.md)).

| Tool | When to reach for it |
|---|---|
| `add_alpha_log_entry` | Record a thesis-scope structural event: status change, rebalance, exit trigger, major intel. |
| `list_alpha_log_entries` | Browse the timeline; filter by scope (`thesis` / `ticker` / `skill` / `standalone`), event type, or limit + offset. |
| `get_alpha_log_entry` | Load one entry by ID. |
| `share_alpha_log_entry` | Generate a public link for a curator's share. |
| `get_shared_alpha_log_entry` | Read a curator's shared entry by share code. |
| `list_curator_alpha_log_entries` | Browse a specific curator's timeline. |
| `generate_alpha_log_upload_url` | Pre-signed upload URL for attachments. |
| `upload_alpha_log_attachment` | Upload via the pre-signed URL. |
| `delete_alpha_log_attachment` | Remove an attachment. |

## Market data

| Tool | When to reach for it |
|---|---|
| `get_ohlcv_with_indicators` | OHLCV + indicators (RSI, MACD, SMAs, etc.) for one or more timeframes. **Use `analysis_mode` (e.g. `"swot-analysis"`, `"fundamental-valuation"`), not `limit=N`** — the server picks the right candle window for the analysis. Multi-timeframe in one call. |
| `list_available_tickers` | Discover tradable tickers; check staleness flags per exchange. |
| `bs_implied_vol_from_price` | Black-Scholes implied vol from an option price. For options skills + scenario work. |
| `get_mta_snapshot` | Multi-timeframe-aggregated snapshot for one ticker — the same engine that emits `MTA` alpha-log events. |
| `list_mta_snapshots` | Browse historical MTA snapshots. |

## Skills

The PortDive Skills library: 32 registered skills today across analysis / strategy / risk categories. See [skills-catalog](skills-catalog.md) for the annotated index.

| Tool | When to reach for it |
|---|---|
| `list_skills` | Discover skills by scope / category / tags / language. |
| `get_skill` | Load full skill body + parameters + (for playbooks) the `steps` DAG. |
| `run_skill` | Execute a skill. For playbooks: omit `step_id` to run the whole DAG, or pass `step_id` to resolve one step at a time. |
| `get_skill_history` | Version history for a skill. |
| `validate_playbook_dag` | Validate a multi-step DAG before publishing (cycles, missing deps, schema drift). |

### Skill execution lifecycle (tandem-experience flow)
A dispatched skill claims work with `claim_pending_skill_execution`, runs the body, then must call either:
- `complete_skill_execution(execution_id, output_markdown, artifacts: [{kind, payload_json, anchor_ticker, anchor_exchange}])` — structured artefacts go in `artifacts[]`, **not** embedded in `output_markdown`.
- `fail_skill_execution(execution_id, error_message)` — clear, user-facing reason.

## Curator network

| Tool | When to reach for it |
|---|---|
| `list_public_curators` | Discover curators with at least one public artefact, optionally sorted by followers. |
| `list_followed_curators` | Curators the current user follows. |
| `subscribe_to_curator` | Follow a curator (broad subscription). |
| `subscribe_to_curator_for_anchor` | Subscribe specifically to a curator's artefacts on a single anchor (ticker / thesis). |
| `unsubscribe_from_curator`, `unsubscribe_from_curator_for_anchor` | Inverse of the above. |
| `count_followers` | Followers of a given curator. |
| `list_curator_artifacts` | Browse a curator's published artefacts. |

Self-follow is rejected at the server.

## Sharing

| Tool | When to reach for it |
|---|---|
| `share_artifact` | Generate a public share link for any artefact. |
| `get_shared_artifact` | Read a shared artefact by share code. |

## Push (operational; rarely used in research)

`register_push_token` / `revoke_push_token` are for mobile push registration. Out of scope for research workflows here.
