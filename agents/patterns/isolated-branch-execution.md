# Pattern: Isolated Branch Execution & Review Discipline

**Rule.** When spawned under an active execution environment (such as `pd watch`), the agent must never operate directly on the `main` branch. It must immediately branch off into a dedicated execution branch named `exec/{execution_id}-{slug}`, perform all narrative and ledger modifications in isolation, and push the branch to remote for human review.

---

## Why

* **Main Branch Protection**: Modifying investment narratives and capital matrix parameters directly on `main` introduces drift, uncoordinated risk rebalances, and potential formatting breaks.
* **Human-in-the-Loop Gatekeeping**: Investment decisions (allocations, sizing, exit triggers) represent real capital allocations. Forcing agents to work in isolated branches allows a senior human portfolio manager to review the raw git diffs, run sanity checks, and approve the PR before merging to `main`.
* **Execution Traceability**: Using the naming convention `exec/{execution_id}-{slug}` binds every repository change directly to a specific backend execution log (`execution_id`) and target investment thesis (`slug`), making debugging and compliance audits instantaneous.

---

## How to Apply

When spawned in an execution session, follow this bootstrap and commit sequence:

### Step 1: Resolve the Environment
At the start of the session, detect the environment variables injected by the orchestrator (`pd watch`):
* `$PORTDIVE_EXECUTION_ID` — The canonical execution ID tracker.
* `$PORTDIVE_THESIS_SLUG` (or resolve it from the skill parameter JSON).

### Step 2: Establish the Isolated Branch
Before making **any** file modifications, execute a checkout to a new branch adopting the standardized naming convention:
```bash
git checkout -b exec/$PORTDIVE_EXECUTION_ID-$PORTDIVE_THESIS_SLUG
```
* *Example*: If the execution ID is `66` and the target is `novo-nordisk`, checkout to `exec/66-novo-nordisk`.
* If the checkout fails (e.g. branch already exists), switch to it safely and pull any upstream changes.

### Step 3: Scaffolding and In-Branch Work
Perform all narrative, research log, and visual asset additions as usual within the isolated branch. Run the `pd thesis sync` pipeline from within this branch to link server resources.

### Step 4: Staging, Pushing, and Handover
Once the work is complete:
1. Update `CHANGELOG.md` inside the isolated branch to document the accomplishments.
2. Stage and commit atomically:
   ```bash
   git add -A
   git commit -m "feat(theses): initial ingest under exec $PORTDIVE_EXECUTION_ID"
   ```
3. Push the branch to the remote origin:
   ```bash
   git push origin exec/$PORTDIVE_EXECUTION_ID-$PORTDIVE_THESIS_SLUG
   ```
4. Output the branch name and Git diff summary clearly in your final session exit report so the human reviewer can perform the merge.

---

## Counter-Example

An autonomous agent spawned under execution `74` for the `mlcc_ai_squeeze` thesis makes direct edits to `main` for `PORTFOLIO_ANALYSIS.md`, introducing a math error in the currency exposures. Because the changes landed directly on `main`, the error is deployed instantly to the portfolio ledger, triggering false risk flags across the entire system before a human reviewer can verify the diff.
