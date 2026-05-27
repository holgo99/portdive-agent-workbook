# Doctrine: Workbook Linting & Global Consistency

**Rule.** Periodically run workbook-wide linting to enforce macro consistency, link integrity, multiple freshness, and strict source-attribution across all active investment theses.

---

## Why

In a rapidly changing technology and hardware capex cycle, individual thesis pages and risk matrices can easily drift:
*   **Assumption Drift:** Thesis A might assume a Blackwell GPU launch in H1 2026, while Thesis B assumes a delay to 2H 2026. This creates a logical contradiction.
*   **Multiple/Staleness Decay:** An active position (e.g., Murata) might be evaluated based on a 20x P/E ratio, while recent supply-chain followups indicate industry-wide multiple compression to 7.5x.
*   **Orphaned Nodes:** Tickers can be registered on the server Postgres database but remain entirely unreferenced in local narratives, violating the [Server-Is-Canonical](server-is-canonical-for-theses.md) doctrine.

Automated and agentic linting audits the workbook as a single, highly integrated codebase, ensuring absolute systemic reliability.

---

## How to Apply

Execute the linting process periodically (or programmatically via `pd watch` loops) against these four core categories:

### 1. Macro-Level Consistency (The Baseline)
Ensure that all active investment theses share a unified macro baseline inside `Risk Management` and `Macro Baseline` sections:
*   **Currency Bands:** Consistent JPY/USD projections (e.g., JPY/USD target band of 130–150).
*   **Bond Yields:** Identical US10Y and JP10Y baseline yields.
*   **Platform Timelines:** Aligned deployment dates for major hardware platforms (e.g., GB200 shipping in Q2 2026, Vera Rubin Ultra shipping in 2H 2027).

### 2. Link Integrity & Obsidian Graph-View Alignment
The workbook must remain a fully browseable, semantic knowledge graph.
*   **Markdown Relative Paths:** All cross-thesis references (e.g., `theses/mlcc_ai_squeeze/` linking to `theses/ai_power_grid_bottleneck/`) must use direct, clickable relative paths (e.g., `[MLCC AI Squeeze](../mlcc_ai_squeeze/THESIS.md)`).
*   **Asset References:** All images, PDFs, and data sheets must be routed to versioned `assets/<ingestion_quarter>/` subdirectories and referenced relatively. Never reference a staged file inside `ingest/`.
*   **Obsidian-Friendly Formats:** Standardize on markdown-compatible relative file paths that Obsidian parses natively to populate the **Graph View** and establish clean associative trails.

### 3. Multiple & Valuation Freshness (90-Day TTL)
All valuation snap-shots, forward P/E estimates, and broker targets carry a strict **90-day time-to-live (TTL)**:
*   Identify any thesis whose target multiples or price targets have not been bumped or re-verified in over 90 days.
*   Flag these positions for active re-evaluation against recent sell-side research (Bernstein, BofA, JPM) and company filings.

### 4. Source-Attribution Auditing
*   Every discovery or catalyst logged in `RESEARCH_LOG.md` must have a corresponding, explicit `Source:` line.
*   The linter will flag any research entry lacking a verified primary source link (SEC filing, IR deck, official memo) or citing a secondary source without primary verification.

---

## Counter-Example

An agent updates the *HBM Late-Cycle Capture* thesis with raised TOWA margins due to an SK Hynix HBM5 order book, but forgets to update the *AI Memory Supercycle* thesis. Because the two files are unlinked and un-audited, the overall portfolio risk ledger remains blind to the combined SK Hynix capex exposure, violating the [Maintain the Portfolio Risk Ledger](maintain-portfolio-ledger.md) doctrine.
