```ascii 
                          
                      ########                      
                    ############                    
                   ##############                   
                  ################                  
                  ################                  
                   ###############                  
                    ##  #########                   
                    #############                   
                    #############                   
                   ###############                  
  #              ###################             #  
 ##            #######################           ## 
###        ######## ############### ######       ###
 ################ ##### ############# ############# 
  ###########   ########### ##### #####   #######   
       ##     ###### #####   ##### #####    ###     
      ##     #### ######      ####   ####    ##     
      ###   #########         #####   ####  ###     
        ########               ####    ######       
            ###        #       ###     ###          
              ##        #     ####    ###           
                         #######
```

# PortDive Workbook: Architectural Blueprint & Decisions (Human Reference)

This repository serves as the **durable, collaborative investment-research workbook** for the PortDive ecosystem. It is a version-controlled journal and capital ledger designed to drive research, narrative drafting, and risk-management across all active investment theses.

> [!NOTE]
> **Human Reference & Architecture:** This `README.md` file is strictly human-targeted meta-documentation detailing workbook architecture, historical decisions, and system alignment. 
> 
> **AI Agent Reference:** AI agents use the standardized [AGENTS.md](AGENTS.md) file at the repository root as their primary command-oriented index and ruleset, and are instructed to treat this file as read-only.

---

## 1. Architectural Mapping: Our Current Alignment

The workbook organically implements the three-layer personal knowledge base architecture outlined by Andrej Karpathy's "LLM Wiki" pattern, customized for institutional-grade equity research and active portfolio risk management:

```
                      ┌──────────────────────────────────────────┐
                      │              THE BRAIN (🧠)              │
                      │         AGENTS.md, agents/doctrine/*     │
                      └────────────────────┬─────────────────────┘
                                           │ Enforces Rules & Workflows
                                           ▼
     ┌──────────────────────┐    ┌──────────────────┐    ┌─────────────────────────┐
     │   THE LIBRARY (📥)   │    │  THE ENGINE (💖) │    │   THE GOVERNMENT (⚖️)   │
     │ Ingested Assets &    │───>│ theses/<slug>/   │───>│ CHANGELOG.md,           │
     │ Immutable Briefings  │    │ THESIS.md        │    │ portfolio/PORTFOLIO.md  │
     └──────────────────────┘    └──────────────────┘    └─────────────────────────┘
```

* **🧠 The Brain (`AGENTS.md` & `agents/`)**: Includes the root-level [AGENTS.md](AGENTS.md), [agents/ONBOARDING.md](agents/ONBOARDING.md), and individual doctrines (e.g., `boil-the-ocean.md`, `beyond-the-wiki-roadmap.md`). These serve as the AI's core instructions, forcing absolute research quality, maintaining baseline macro consistency, and preventing "vibe-scoring" in favor of strict mathematical confidence rubrics.
* **📥 The Library (`ingest/` & `briefings/`)**: Represents our immutable ground-truth. The `ingest/` directory serves as the initial, gitignored landing zone for supply-chain assets, raw PDFs, and briefings. Once processed, they are converted into immutable local briefings (e.g., `briefings/2026_q2/`) and linked relatively.
* **💖 The Engine (`theses/`)**: Long-form narrative thesis files (`theses/<slug>/THESIS.md`) act as persistent, compounding entity pages. They compile qualitative and quantitative research once and keep it current, rather than forcing the agent to re-derive knowledge from raw text at query time.
* **⚖️ The Government (`portfolio/` & `CHANGELOG.md`)**: `CHANGELOG.md` acts as the append-only, chronological log of accomplishments. The `portfolio/` namespace acts as our dynamic, content-oriented index, tracking allocations (`portfolio/PORTFOLIO.md`), portfolio-level aggregates (`portfolio/PORTFOLIO_ANALYSIS.md`), currency bands (`portfolio/RISK_MATRIX.md`), and risk overrides (`portfolio/PORTFOLIO_LOG.md`).
* **🛠️ The Hands (Tooling & Integration)**: The Python sync toolkit (`scripts/`) and local `pd` CLI act as our custom programmatic search, scaffolding, and database-synchronization engine, communicating with the PortDive Ecosystem.

---

## 2. Key Architectural Decisions

To maintain a clean division of labor between AI agents and human analysts, the following structural decisions were implemented:

### A. The Agent Firewall (`AGENTS.md` at the root)
Originally, `agents/README.md` was the entry point for agents. However, using `README.md` for AI instructions creates a conflict: humans expect a folder-level `README.md` to be human-oriented orienting documentation, while agents expect it to contain structured, strict schema rules.
* **Decision:** We established a standardized, root-level [AGENTS.md](AGENTS.md) file (which AI agents natively parse as their primary command-oriented index), freeing up `README.md` at the root for human-targeted, preprocess orientation.
* **Doctrine:** Agents are explicitly instructed to treat `README.md` as read-only orienting docs and focus their operational execution strictly on the parameters defined in `AGENTS.md`.

### B. Moving Beyond the Passive "LLM Wiki"
A standard LLM Wiki is a passive compiler—it organizes text but doesn't act. For an active capital ledger, passivity introduces extreme lag.
* **Decision:** We established the seventh doctrine [beyond-the-wiki-roadmap.md](agents/doctrine/beyond-the-wiki-roadmap.md), mandating that the agent acts as an active, adversarial stress-testing engine—generating Anti-Theses, red-teaming tail risks, calculating parametric margin impacts, and employing autonomous watchdogs to alert humans to rebalance opportunities.

#### 1. The Passive LLM Wiki vs. Sovereign Risk Engine Paradigm

Karpathy’s LLM Wiki pattern models the agent as a tireless bookkeeper (reactive indexing, markdown cross-linking, syntax-checking, and indexing under a unified schema).

In contrast, an investment-research workbook governed by the `SOUL.md` mandate must treat the agent as an active custodian of capital. A passive librarian compiles bullish facts; a sovereign risk engine actively stress-tests tail risks, models quantitative parameter shifts, and drives autonomous execution.

| Attribute | Karpathy "LLM Wiki" (Passive Compiler) | PortDive Sovereign Risk Engine (Active Custodian) |
| :--- | :--- | :--- |
| **Operational Stance** | Passive & Reactive: Waits for the human to stage files in `ingest/` and query the system. | Active & Autonomous: Employs background watchdogs (`pd watch`) to proactively monitor supply chain signals and draft PR branches. |
| **Cognitive Bias** | Coherence Seeker: Standardizes text and resolves contradictions to build a clean, unified bullish narrative (confirmation bias). | Adversarial Auditor: Actively writes the Bear Case (Anti-Thesis) and runs tail-risk simulations for every holding. |
| **Analytical Output** | Qualitative Prose: Synthesizes high-level summaries and text bulletins ("rising capex, high demand"). | Quantitative Simulation: Connects physical supply-chain shifts directly to margin adjustments and multiple compressions. |
| **Siloing vs. Systems** | Linked Nodes: Connects markdown pages but evaluates their financial allocations in isolation. | Systemic Risk Ledger: Manages cross-thesis dependencies (FX shocks, packaging bottlenecks) in a central ledger (`portfolio/PORTFOLIO_LOG.md`). |

#### 2. The Four Fundamental Gaps & Pushing Beyond

To push beyond the boundaries of standard cataloging, our workbook must adopt and implement four active sovereign pillars:

*   **A. Active Adversarial Stress-Testing (The Anti-Thesis)**
    *   **The Gap:** The LLM Wiki seeks narrative harmony. By resolving contradictions into a clean synthesis, it obscures systemic dissent.
    *   **The Push:** The agent must never allow the workbook to become a bullish echo chamber. Every major investment thesis page must contain or link to an active Anti-Thesis (Bear Case).
    *   **Red-Team Execution:** The agent must proactively simulate tail-risk triggers:
        *   What if Rubin Ultra Blackwell shipments collapse by 40% due to decoupling capacitor or thermal spacer yield failures?
        *   What if JPY/USD surges rapidly to 125, compressing domestic margins for Murata and Towa?
        *   What if silver prices spike by 200%, destroying high-spec chip resistor margins for Fenghua and Holy Stone?
*   **B. Parametric Supply-Chain-to-Valuation Mapping**
    *   **The Gap:** A passive wiki relies on qualitative prose, which is a lagging indicator for asset pricing.
    *   **The Push:** Physical supply-chain disruptions must connect directly to financial math. For instance, when analyzing Fenghua's order suspension, the agent must not stop at a text summary. It must map the physical shortage to expected average selling price (ASP) spikes, calculate downstream margin impacts for proxies (Sakai Chemical vs. Murata), and enforce a strict 90-day time-to-live (TTL) on all forward valuation multiples (e.g., SNDK, MU, Samsung) to prevent baseline decay.
*   **C. Autonomous Sentinel Networks (`pd watch`)**
    *   **The Gap:** The human acts as the primary sensor, clipping articles and triggering the ingestion loop.
    *   **The Push:** The agent must operate background watchdogs. When an anomalous supply-chain catalyst is detected (e.g., an Infineon price-hike notification letter), the agent should autonomously spin up an isolated execution branch (e.g., `exec/infineon-price-hikes`), draft the updated thesis, re-run the confidence rubric, construct the trade order adjustments, and present the completed PR to the human portfolio manager.
*   **D. Consolidated Systemic Portfolio Risk Ledger**
    *   **The Gap:** The wiki links separate nodes but treats individual stock picks in structural isolation.
    *   **The Push:** All active theses must share a perfectly synchronized macro baseline (currency bands, bond yields, Blackwell rollout timelines) enforced via workbook linting. Cross-thesis dependencies must be continuously audited inside [portfolio/PORTFOLIO_LOG.md](portfolio/PORTFOLIO_LOG.md) to prevent invisible concentration risks.

---

### C. Folder-Based Ingestion & Relative Linking
Obsidian compatibility was selected as a hard requirement to enable browseable, visual **Graph View** relationships of our holding concentrations.
* **Decision:** All visual stimulus and data sheets are strictly sorted under version-controlled, quarter-based directories (`assets/<ingestion_quarter>/`) and linked using native markdown relative paths rather than absolute paths, ensuring that the entire workbook remains robust and portable across clones and Obsidian.

---

## 3. Session Accomplishments & Workspace Integrity

Pursuant to the **Session Closeout & Commit Discipline**, the following actions have been executed in this session:

1. **Authored Seventh Doctrine:** Created the durable, repo-versioned doctrine document: [beyond-the-wiki-roadmap.md](agents/doctrine/beyond-the-wiki-roadmap.md) detailing the complete strategic blueprint.
2. **Updated Master Indices:** Integrated and linked the seventh doctrine inside the master orienting index [AGENTS.md](AGENTS.md) and the core onboarding protocol [agents/ONBOARDING.md](agents/ONBOARDING.md) (The seven doctrines section).
3. **Changelog Maintenance:** Documented the accomplishments under the `## [2026-05-27]` section of [CHANGELOG.md](CHANGELOG.md).
4. **Structured Git Commit:** Staged all changes and committed atomically to `main`:
   ```bash
   git add -A
   git commit -m "docs(doctrine): establish sovereign risk engine doctrine pushing beyond passive llm wiki"
   ```
5. **Workspace Audit:** Verified the workspace via `git status`; the local working tree is 100% clean and fully synchronized.

---

## 4. The Fork & Clone Workflow (Standard Distribution)

To use this workbook for your own sovereign investment research, follow the gold-standard distribution workflow:

### Step 1: Fork on GitHub
1. Navigate to the central template repository: `https://github.com/YOUR_ORGANIZATION/portdive-agent-workbook`.
2. Click the **Fork** button in the top-right corner to create a copy of the template under your personal or organizational GitHub account.
3. **Privacy Protection:** If you plan to manage real capital or private portfolio allocations, ensure that you set your fork's visibility to **Private** on GitHub to safeguard your assets, sizing configurations, and transaction logs.

### Step 2: Clone Your Fork
Clone your personal, private fork to your local development environment:
```bash
# Clone your private fork or pristine local bare template
git clone https://github.com/YOUR_USERNAME/portdive-agent-workbook.git my-research-workbook

# Change directory
cd my-research-workbook
```

### Step 3: Initialize Workbook Identity
Every cloned instance of the workbook must be initialized with a unique world-wide identification card. This establishes a unique global UUID, custom user-defined name, and cryptographic SHA-256 signature to authorize background agents and identify nodes:
```bash
python3 scripts/initialize_workbook.py
```
Follow the interactive prompts to assign a name and commit the credentials into the root-level `IDENTITY.md` file.

### Step 4: Run Sizing Initializer
Execute the multi-tier reporting script for your targeted wallet size (e.g., standard `25k` or `100k` HNW Tier) to generate the baseline analysis:
```bash
python3 scripts/generate_portfolio_analysis.py 25k
```

---

## 5. Pulling Upstream Template Upgrades

As the core PortDive template evolves—adding new Python sync utilities, advanced doctrines, and reference manuals—you can pull these updates into your active portfolio fork without overwriting your private theses or custom capital allocations:

```bash
# 1. Register the original parent template repository as remote upstream
git remote add upstream https://github.com/YOUR_ORGANIZATION/portdive-agent-workbook.git

# 2. Fetch all upstream developments
git fetch upstream

# 3. Merge the new doctrines/scripts into your local workspace
git merge upstream/main --allow-unrelated-histories
```
