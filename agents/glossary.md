# Glossary

Project-specific vocabulary for investment research in the PortDive ecosystem. If a term feels unfamiliar, look here first.

## Roles

- **Investor** — end user of the PortDive mobile app. Captures positions, browses theses, follows curators.
- **Curator** — user who has claimed a public handle (e.g. `@holgo99-curator`) and publishes analyses. In this repo, the analyst working on `theses/<slug>/` is the curator.
- **Follower** — Investor or Curator subscribed to another Curator's shared content via `subscribe_to_curator`. Self-follow rejected at the server.

## Thesis structure

- **Thesis** — the unit of work. Has a Status (ACTIVE / WATCH / CLOSED), Confidence %, Target Horizon, Epicenter. Lives canonically on the server; paired by `thesis_id` to a long-form `THESIS.md` on disk.
- **Server thesis** — the structured representation at `mcp.portdive.app`. Source of truth for status, baskets, items, allocations. See [doctrine/server-is-canonical-for-theses](doctrine/server-is-canonical-for-theses.md).
- **Disk thesis** — `theses/<slug>/THESIS.md` — the long-form narrative + visual + research depth. Paired to a server thesis via the `Server Thesis: <thesis_id>` line in its metadata block.
- **Epicenter** — one-line statement of the core bet. Goes in the thesis metadata block.
- **Bottleneck** — the physical / material / capacity constraint that anchors the case. Identified before any proxy selection. See [doctrine/bottleneck-first-analysis](doctrine/bottleneck-first-analysis.md).
- **Tradable Proxy** — a position in a basket. Confirmed tradable on the user's brokers (TR/DKB primary), with a documented strategic role.
- **Vertical Proxy** — when a bottleneck leader is non-tradable, a tradable name with deep exposure to the same upstream. E.g., Sakai Chemical (Health) → Murata + TDK (Tradable). See [patterns/health-basket-construction](patterns/health-basket-construction.md).
- **Health Basket** — non-tradable signal-only names attached to a thesis. Validate (or invalidate) the upstream claim without contributing to allocation.
- **Triple-Lock** — the 40/30/20/10 allocation pattern: Monopoly Material + Tech Leader + Hidden Component + Proxy Torque. See [patterns/triple-lock-allocation](patterns/triple-lock-allocation.md).

## PortDive ecosystem

- **MCP** — Model Context Protocol. The PortDive MCP at `https://mcp.portdive.app/mcp` is the primary tool surface for this repo. See [reference/portdive-mcp](reference/portdive-mcp.md).
- **CLI** — the locally-installed `portdive` binary. Second operating surface for batch / scripted work. See [reference/portdive-cli](reference/portdive-cli.md).
- **Skill** — a registered template in the Skills library. Kebab-case slug. Single-prompt or multi-step DAG. Invoked via `run_skill(slug)`.
- **Playbook** — a skill with multi-step DAG semantics (`type: "playbook"`). Has a `steps` array with dependencies, gates, and read-first optimization. E.g., `investment-analysis-playbook`, `long-strategy-playbook`.
- **Composable framework** — a skill marked `composable: true`, embedded in other skills via `{include:slug}` substitution. E.g., `elliott-wave-rules`, `bayesian-framework`.
- **Artefact** — a typed output of a skill execution: `investment_analysis`, `valuation`, `catalyst_analysis`, `options_playbook`, `mean_reversion_trade_plan`, `position_import`, etc. Delivered via `complete_skill_execution(artifacts: [...])`.
- **Thesis template** — a starter scaffold for `create_thesis`. The 5 templates: `thematic-equity`, `factor-style`, `macro-hedge`, `sector-rotation`, `income-dividend`.

## Alpha log + signals

- **Alpha Log** — the time-ordered event stream on the server. Auto-populated by STA/MTA engines with SIGNAL / SNAPSHOT / DRIFT entries per tracked ticker; supplemented by analyst-authored thesis-level entries per [doctrine/log-thesis-events](doctrine/log-thesis-events.md).
- **STA** — Single-Timeframe Analysis engine. Emits per-timeframe signal events (`1H`, `4H`, `1D`, `1W`) with grade A–F and a score.
- **MTA** — Multi-Timeframe Aggregated. Emits composite snapshots across timeframes with an overall grade. `get_mta_snapshot` returns the current MTA read for a ticker.
- **DRIFT / SNAPSHOT / SIGNAL** — alpha-log event types. `SIGNAL` = a specific indicator threshold cross. `SNAPSHOT` = a periodic state read. `DRIFT` = a score change between snapshots.

## Market data

- **OHLCV** — Open / High / Low / Close / Volume. Fetched via `get_ohlcv_with_indicators` with multiple timeframes in one call.
- **`analysis_mode`** — parameter on `get_ohlcv_with_indicators`. Use this (e.g. `"swot-analysis"`, `"fundamental-valuation"`) instead of `limit=N` — the server picks the right candle window for the analysis.
- **ISIN** — International Securities Identification Number. Each item in a basket carries one; used for unambiguous broker matching.
- **TR / DKB** — Trade Republic and Deutsche Kreditbank, the user's primary German retail brokers. Liquidity verification targets these by default.

## Workflow

- **Cold start / cold pickup** — a new agent or session opens this repo with no prior context. The knowledge base must support cold pickup without external lookups.
- **Boil the ocean** — completeness over speed. No deferred threads. See [doctrine/boil-the-ocean](doctrine/boil-the-ocean.md).
- **Research loop** — the seven-step pipeline from catalyst to monitored thesis. See [patterns/research-loop](patterns/research-loop.md).

## When a term is missing

If you encounter vocabulary not here, add it. The glossary is a working document.
