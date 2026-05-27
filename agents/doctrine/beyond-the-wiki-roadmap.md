# Doctrine: Beyond the LLM Wiki (The Sovereign Risk Engine)

**Rule.** Do not treat this workbook as a passive library or a standard "LLM Wiki." Transition the workbook from a compiling knowledge catalog into an active, autonomous **adversarial risk engine** and **capital custodian** that stress-tests theses, simulates quantitative impacts, and drives portfolio execution under the aggressive `SOUL.md` mandate.

---

## Why: Pushing Beyond the Karpathy "LLM Wiki"

Andrej Karpathy's "LLM Wiki" pattern defines a highly disciplined, compounding personal knowledge base. The LLM acts as a tireless compiler—organizing files, cross-linking entity pages, resolving contradictions, and maintaining indexes (`index.md`) and logs (`log.md`).

However, in a capital-allocation and hardware supply-chain context, this passive cataloging approach has four severe, high-risk gaps when measured against the absolute standard of **`SOUL.md` (Boil the Ocean)**:

| Attribute | The Karpathy "LLM Wiki" (Passive Compiler) | The PortDive Sovereign Risk Engine (Active Custodian) |
| :--- | :--- | :--- |
| **Operational Stance** | **Passive & Reactive:** Waits for the user to clip an article, drop it in `ingest/`, and prompt for organization. | **Active & Autonomous:** Employs background sentinels (`pd watch`) to sniff raw supply-chain data and draft interventions. |
| **Cognitive Bias** | **Coherence Seeker:** Standardizes text, resolves contradictions to build a clean, unified narrative (confirmation bias). | **Adversarial Auditor:** Generates aggressive bear cases, writes anti-theses, and stress-tests holding assumptions. |
| **Analytical Output** | **Qualitative Prose:** Synthesizes textual bullet points and high-level summaries ("stale multiples, rising demand"). | **Quantitative Simulation:** Connects physical supply-chain events to margin models, multiple compression, and sizing math. |
| **Siloing vs. Systems** | **Linked Nodes:** Connects pages via markdown syntax but evaluates their financial allocations independently. | **Systemic Risk Ledger:** Consolidated portfolio ledger (`PORTFOLIO_LOG.md`) mapping cross-thesis dependencies and JPY/FX exposure. |

---

## The Four Sovereign Pillars

To "boil the ocean" and deliver a workbook that is profoundly complete, agents must implement and enforce these four architectural pillars:

### 1. Active Adversarial Stress-Testing (The Anti-Thesis)
A thesis without an active, rigorous bear case is a structural vulnerability. The agent must never allow the workbook to become a bullish echo chamber.
* **The Counter-Hypothesis:** For every primary investment thesis (e.g., `theses/mlcc_ai_squeeze`), the agent must draft and maintain an active **Anti-Thesis** page or section.
* **Red-Team Simulations:** The agent must actively simulate tail-risk events:
  * *What if Vera Rubin Blackwell Ultra shipments collapse by 40% due to decoupling capacitor failures?*
  * *What if JPY/USD surges rapidly to 125, compressing the domestic margins of Murata and Towa?*
  * *What if silver prices spike by 200%, destroying high-spec chip resistor margins?*
* **Triggering Re-Evaluations:** When supply-chain events are ingested, the agent must update both the bullish case and the adversarial bear case, adjusting the systemic confidence score.

### 2. Parametric & Quantitative Simulation
Prose is a lagging indicator for asset pricing. A premium research engine must bridge physical hardware anomalies directly to financial math.
* **Physical-to-Financial Mapping:** If a manufacturer (e.g., Fenghua Advanced Technology) suspends order intake, the agent must not stop at writing a summary. It must map the physical shortage to:
  * Domestic ASP (Average Selling Price) spikes.
  * Margin squeeze or expansion of downstream proxies (e.g., Sakai Chemical, Murata, TDK).
* **Valuation Multiple Freshness (Strict 90-Day TTL):** All forward P/E estimates (e.g., Sandisk at ~7.4x [2027], SK Hynix at ~5.5x [2027]) carry a strict 90-day time-to-live. Stale multiples must be programmatically flagged and re-verified against live sell-side data via PortDive MCP curators.

### 3. Autonomous Sentinel Networks (`pd watch`)
Waiting for human curation is a failure of speed. The agent must actively patrol the boundaries of the workbook.
* **The Ingestion Pipeline:** Utilize the gitignored `ingest/` folder as a high-velocity drop zone for raw PDFs, visual spreadsheets, and supply-chain images.
* **Background Curators:** The agent must schedule background watch-loops (`pd watch`) that monitor target tickers, regulatory filings (SEC/EDGAR), and industry channels.
* **Proactive Branching:** Upon detecting a critical market event (e.g., Infineon announcing immediate high-power GaN pricing hikes), the agent must autonomously spin up an isolated execution branch (e.g., `exec/{execution_id}-gan-price-hike`), draft the updated thesis and portfolio allocation adjustments, and present the completed PR to the user.

### 4. Consolidated Systemic Portfolio Risk Ledger
Individual stock picking is meaningless if the entire portfolio shares a single, invisible point of failure.
* **Macro Baselines:** All active theses must share a perfectly synchronized macro baseline (currency bands, US10Y yields, GPU rollout timelines) codified in the master linter (`doctrine/workbook-lint-discipline.md`).
* **Cross-Thesis Risk Correlation:** If `theses/mlcc_ai_squeeze` and `theses/ai_power_grid_bottleneck` are both long-bias on Blackwell/Rubin power architecture, their correlated risks must be aggregated and audited in `portfolio/PORTFOLIO_LOG.md`.

---

## Actionable Execution Rules

Every agent operating in this repository must apply these rules in every session:

1. **Write the Anti-Thesis First:** When establishing a new server thesis, never declare it complete until a corresponding `Bear Case & Stress-Test Matrix` is fully authored and linked in the long-form narrative.
2. **Never Ignore Contradictions:** If an ingested asset (e.g., `memory-forward-pe-2026-2027.jpeg`) indicates multiple compression that contradicts a bullish thesis, you must immediately resolve the drift across all affected files. Do not drop a `TODO` for the next session.
3. **Execute the Linting Discipline:** Run global link and baseline consistency checks before committing. The workbook must remain a browseable, highly structured Obsidian knowledge graph with zero broken relative links.
4. **Sovereign Handover:** When closing a session, write a high-signal handover in `CHANGELOG.md` highlighting key stress-test variations and critical alert thresholds, ensuring the successor agent can cold-start and immediately execute the sovereign mandate.
