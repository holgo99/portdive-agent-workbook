# Reference: The Unified `pd` CLI & Autonomous Governance

> [!NOTE]
> This document outlines the unified **`pd`** CLI interface and autonomous cost-governance model introduced under the **FEAT-047**, **FEAT-048**, and **FEAT-049** blueprints. Refer to this specification when operating the local CLI once the monorepo integration has landed.

The local CLI binary name is **`pd`** (with a `portdive` → `pd` symlink automatically installed on the system `$PATH` for backwards compatibility). It serves as the primary command-line interface for the PortDive ecosystem, backed by the shared Rust `portdive-commands` crate. 

---

## 1. Architectural Foundations

*   **Exit Code Contract**: Command failures map to stable system exit codes for robust scripting:
    *   `1` — **Validation** (e.g., malformed syntax, out-of-range scoring).
    *   `2` — **Backend** (e.g., gRPC communication failure, database constraints).
    *   `4` — **NotFound** (e.g., missing thesis ID, unknown instrument).
    *   `5` — **Conflict** (e.g., allocation sum violation, unique key collision).
    *   `70` — **Internal** (e.g., unhandled system error, `EX_SOFTWARE`).
    *   `127` — **Auth** (e.g., missing, invalid, or expired Personal Access Token).
*   **Alternate Identifiers**: To simplify local scripting, all commands accepting a numeric `--instrument-id <N>` also accept `--isin <X>` as a mutually-exclusive alternate. The CLI performs local resolution against the server before running the core command handler.

---

## 2. Command Surface Catalog

### A. Thesis Management (`pd thesis`)
Manages the investment thesis life cycle. Syncs local long-form Markdown narratives to the database.

| Command | Action | Flags Worth Knowing |
|---|---|---|
| `pd thesis list` | Browse owned or public theses. | `--status ACTIVE\|WATCH\|CLOSED`, `--limit N` |
| `pd thesis show <id>` | Retrieve full details for a single thesis. | `--include signals,performance,history,health,skills` |
| `pd thesis create` | Scaffold a new server thesis. | `--title <t>`, `--catalyst N`, `--tradability N`, `--sizing N`, `--macro N` |
| `pd thesis update <id>` | Perform partial metadata or rubric updates. | `--title <t>`, `--gist <g>`, `--rubric-catalyst N`, `--rubric-tradability N` |
| `pd thesis delete <id>` | Retire a thesis permanently. | None |
| `pd thesis templates` | Enumerate starter scaffolding templates. | None |
| `pd thesis signals` | Check for active proxy-staleness warnings. | `--unread`, `--since ISO` |
| `pd thesis signals ack <id>`| Acknowledge an advisory staleness signal. | None |

#### Idempotent Bidirectional Syncing (`pd thesis sync`)
The core operational loop for research agents. Synchronizes the local `THESIS.md` files with the Postgres database:
```bash
pd thesis sync --root <path> [--dry-run] [--push-only | --pull-only] [--strategy <strategy>]
```
*   **Identity Resolution**: Parses the document header line `- **Server Thesis:** N` (or `<!-- thesis_id: N -->`). If set to the default placeholder (`(not yet created — run create_thesis to pair)` or `No PortDive equivalent...`), the sync automatically creates the database entry and writes the new ID back into the file header.
    *   *Curated Link Form (Option 2)*: If the header carries a shared link form like `- **Server Thesis:** [PortDive #N — Title](url) (share slug `slug`)`, the parser must **not** treat `#N` as the database ID (as it is merely a display ordinal from the public web interface). Instead, the parser must extract the `share slug` and perform a server-side query via `get_shared_thesis` to resolve the true local database `thesis_id`. If resolved, it pairs; otherwise, it treats it as a draft to prevent writing to a mismatched local ID.
*   **Conflict Strategies (`--strategy`)**:
    *   `prefer-disk`: Disk values override server values (ideal for bulk local updates).
    *   `prefer-server`: Server values override disk (ideal for resetting a corrupted workspace).
    *   `prompt` (default): Prompt in the terminal for case-by-case resolution.
    *   *Omitted strategy tiebreaker*: Server-rubric wins on `rubric_updated_at` timestamp; disk wins on `title`/`gist`/`status`.

---

### B. Baskets & Portfolio Positions (`pd basket`)
Handles the composition of health baskets and tradable proxies.

| Command | Action | Flags Worth Knowing |
|---|---|---|
| `pd basket add` | Create a strategic bucket under a thesis. | `--thesis <id>`, `--name <n>`, `--allocation-pct N` |
| `pd basket update <id>` | Mutate basket parameters. | `--name <n>`, `--allocation-pct N` |
| `pd basket items list <id>`| Enumerate positions in a basket. | None |
| `pd basket items add <id>` | Add a proxy or signal position to a basket. | `--symbol <s>`, `--exchange <e>`, `--instrument-id <N>` \| `--isin <X>` |
| `pd basket items remove <id>`| Strip a position from a basket. | `--instrument-id <N>` \| `--isin <X>` |

---

### C. Alpha Log Timeline (`pd alpha-log`)
Maintains the high-signal narrative audit trail. Analyst entries represent structural thesis annotations.

*   ** ergonomic positional body**:
    ```bash
    pd alpha-log add --thesis <id> --kind REBALANCE "Trimmed Ajinomoto to 20% to fund Bloom Energy baseload grid buffers."
    ```

| Command | Action | Flags Worth Knowing |
|---|---|---|
| `pd alpha-log add` | Log a thesis-level structural annotation. | `--thesis <id>`, `--kind SIGNAL\|REBALANCE\|EXIT`, `--attach <path>` |
| `pd alpha-log list` | Browse timeline events. | `--thesis <id>`, `--since ISO`, `--kind <k>` |
| `pd alpha-log show <id>` | Retrieve full log entry. | None |
| `pd alpha-log attach` | Upload research attachments to an entry. | `--path <file>`, `--mode direct\|presigned-url` |
| `pd alpha-log attach-rm` | Remove an attachment by ID. | None |

---

### D. Skill Execution & DAGs (`pd skill`)
Authors and manages the 32 registered PortDive research and analysis skills.

| Command | Action | Flags Worth Knowing |
|---|---|---|
| `pd skill run <slug>` | Resolve a skill/playbook prompt (instructions only — see below). | `--step-id <id>`, `--params <json>`, `--json` |
| `pd skill list` | Enumerate available analysis skills. | `--category <c>`, `--scope <s_scope>` |
| `pd skill get <id>` | Load skill instructions and inputs. | `--include history,resources,assets` |
| `pd skill create` | Register a new research skill. | `--name <n>`, `--slug <s>`, `--category <c>` |
| `pd skill update <id>` | Mutate skill code or template parameters. | None |
| `pd skill delete <id>` | Delete a skill. | None |
| `pd skill clone <id>` | Clone an existing skill to a new slug. | `--name <n>`, `--slug <new_s>` |
| `pd skill attach <id>` | Bind an analysis skill to a thesis. | `--thesis <id>` |
| `pd skill detach <id>` | Detach an analysis skill from a thesis. | `--thesis <id>` |
| `pd skill resources <op>`| Manage structured API resource bounds. | `<op> = list \| add \| delete`, `--skill-id <id>` |
| `pd skill assets <op>` | Manage binary/script assets for a skill. | `<op> = list \| upload \| delete`, `--mode direct\|presigned-url` |

> **`pd skill run` is instructions-only — _you_ are the execution engine.**
> `pd skill run <slug>` (and `--step-id <id>` for one playbook step) returns the
> **assembled prompt / DAG structure / per-step instructions**. It does **not**
> perform the research or produce the artifact. The flow is: call `pd skill run`
> to read what to do → do the actual research yourself → build the schema-valid
> JSON → validate it with `pd skill validate-artifact` (loop until 0 errors) →
> write the envelope to `$PORTDIVE_ARTIFACT_PATH`. `pd watch` is the **sole
> completer** — never call a complete/finish command yourself.

---

### E. Market Data & Feeds (`pd ticker`)
High-performance market-data query surface. Inputs accept `--symbol/--exchange` or alternate `--isin/--wkn/--figi/--cusip` flags.

| Command | Action | Flags Worth Knowing |
|---|---|---|
| `pd ticker search <q>` | Look up tradable symbols. | `--exchange <e>`, `--limit N` |
| `pd ticker resolve` | Map symbols/ISINs to canonical IDs. | `--isin <X>`, `--symbol <s>`, `--exchange <e>` |
| `pd ticker get <id>` | Retrieve general ticker details. | `--include today-digest,availability` |
| `pd ticker list-available` | Inspect all tracked tickers for freshness. | `--stale-only` |
| `pd ticker candles <id>` | Query raw historical OHLCV data. | `--timeframe <tf>`, `--since ISO`, `--limit N` |
| `pd ticker ohlcv <id>` | Stream indicator-injected OHLCV. | `--timeframe <tf>`, `--with-indicators` (Returns columnar matrix) |
| `pd ticker signals <id>` | Retrieve current STA/MTA indicator signals. | `--timeframe <tf>` |
| `pd ticker mta <id>` | Retrieve multi-timeframe aggregated grades. | `--include history` |
| `pd ticker digest [<id>]` | Read the today-market macro summary. | None |

---

### F. REST Schemas (`pd schemas`)
Fetches and validates public JSON schemas directly via the REST surface, bypassing the MCP layer.

```bash
pd schemas list
pd schemas get wave-counts-v5 --file ~/.portdive/schemas/wave-counts.json
```

---

## 3. Autonomous Loop & Cost Governance (`pd watch`)

The `pd watch` command runs as a background wake-on-event daemon (supported via macOS `launchd` and Linux `systemd`). It continuously listens to `StreamEvents` and spawns a fresh agent process on `SkillExecutionRequested` payloads.

### A. The Spawning Flow
When a skill execution is requested:
1.  `pd watch` intercepts the event, validates target PAT presence, and reserves an execution slot.
2.  `pd watch` reads local budget states from the `client-db` SQLite `governance` namespace (FEAT-048).
3.  If no budget thresholds are violated, it spawns the configured agent process, injecting:
    *   `PORTDIVE_ACCESS_TOKEN` — the dedicated agent PAT.
    *   `PORTDIVE_EXECUTION_ID` — the database tracker ID.
    *   `PORTDIVE_USAGE_PATH` — path to a temporary JSON file.

### B. The Cost-Reporting Contract
Before exiting, the spawned agent process **must** write its token usage and pricing summary to `$PORTDIVE_USAGE_PATH`:
```json
{
  "execution_id": "12345",
  "model": "claude-opus-4-7",
  "input_tokens": 8420,
  "output_tokens": 1340,
  "cache_read_input_tokens": 2100,
  "cost_usd": 0.1832,
  "duration_ms": 47200,
  "completion_status": "success"
}
```
*   **Safety Net Fallback**: If the agent crashes or does not write this file, `pd watch` falls back to the **`estimated`** policy: parsing raw input prompt characters and captured execution output characters (1 token ≈ 4 characters) to calculate costs against the pricing table.

### C. The Artifact-Handoff Contract
To prevent valuable structured analysis from being stranded in the agent's transient directory, `pd watch` injects a dedicated path variable for analytical outputs:
*   `PORTDIVE_ARTIFACT_PATH` — Path to a temporary target file where the agent must write its structured JSON artifact.

Before exiting with code `0`, the agent must write its schema-valid structured JSON result (e.g., conforming to `investment-analysis.v1.schema.json`) directly to the file at `$PORTDIVE_ARTIFACT_PATH`.

Upon a successful exit code `0`, the orchestrator (`pd watch`) automatically:
1. Detects and reads the file at `$PORTDIVE_ARTIFACT_PATH`.
2. Packages the JSON content as an official, typed skill artifact (e.g., of type `valuation` or `wave_count`).
3. Submits it to the PortDive server via the `complete_skill_execution` RPC, securely anchoring it to the target context ticker in the database.

This keeps `pd watch` as the sole transaction completer (resolving double-complete risks) while ensuring the rich structured intelligence surfaces immediately in the PortDive desktop and mobile interfaces (`artifact_count` > 0).

### D. Telemetry & Budgets (`~/.portdive/pd.toml`)
Users configure strict spending guardrails inside the local configuration file:
```toml
[limits]
max_executions_per_day = 50
max_cost_usd_per_day = 5.00
max_cost_usd_per_execution = 0.50          # Runway circuit-breaker

[limits.per_skill]
"investment-analysis" = { max_cost_usd_per_run = 0.30 }
"fundamental-valuation" = { max_cost_usd_per_run = 0.10 }

[limits.per_thesis]
"ABF/CPO Substrates" = { max_cost_usd_per_month = 12.00 }
"MLCC AI Squeeze"   = { max_cost_usd_per_month = 8.00 }

[limits.fallback]
usage_reporting_required = "estimated"     # "strict" | "lenient" | "estimated"
day_boundary_tz = "UTC"                    # Default boundary
```

*   **Introspection**: Users and agents can audit current periods and spend allocations:
    *   `pd watch status` — Returns current daily spend, execution counts, and budget throttle distance.
    *   `pd watch report --by thesis` — Summarizes spend aggregates per thesis key to calculate research ROI.
*   **Model Prices Update**: `pd` fetches fresh API pricing from the server via `GET /api/v0/model-prices` and caches it at `~/.portdive/model-prices.toml` with a 24-hour TTL check. Offline systems fallback safely to the cached copy or compile-time embedded pricing tables.
