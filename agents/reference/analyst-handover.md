# Reference: Analyst's Handover & Cold-Start Checklist

> [!IMPORTANT]
> **Rule.** Cold-start agents and fresh sessions must verify database sync, comply with the `PORTDIVE_USAGE_PATH` cost contract, and audit JPY currency risk parameters before modifying any local or server workbook states.

## Why

Ephemeral sessions lose local context and agent memory. Without a structured, low-friction handover checklist, a new agent picking up the workbook cold will inevitably drift local markdown allocations from the server database, trigger budget throttles on the watch loop, or violate exchange-specific listing constraints.

---

## The Checklist

### 1. Verification & Sync Integrity
*   **The Constraint**: The server thesis is canonical for structure and allocations. The markdown files in `theses/<slug>/THESIS.md` must never diverge.
*   **Action**: Before making any narrative edits, run `get_thesis` on the associated ID. Once your edits are complete, run:
    ```bash
    pd thesis sync --root theses/ --push-only
    ```
*   **The Metadata Anchor**: The sync command parses the document header `- **Server Thesis:** N` (or `<!-- thesis_id: N -->`) as the single binding thread. **Do not modify or delete this ID line manually.**

### 2. Cost-Governance & Spawner Compliance
*   **The Constraint**: Under `FEAT-049`, autonomous agent processes are spawned with strict budget circuit-breakers.
*   **Action**: Before your process exits, you **must** write your exact token usage and completion status to the temporary JSON file provided in the `PORTDIVE_USAGE_PATH` environment variable:
    ```json
    {
      "execution_id": "12345",
      "model": "your-model-name",
      "input_tokens": 12000,
      "output_tokens": 800,
      "completion_status": "success"
    }
    ```
*   **Mitigant**: Failing to write this report forces the daemon to calculate costs based on raw character-count heuristics (`estimated` fallback), which can artificially exhaust the user's daily budget cap.

### 3. Exchange-Specific Position Mutations
*   **The Constraint**: When adding or updating a tradable proxy using alternate identifier lookups (e.g., `--isin`):
    ```bash
    pd basket items add <basket_id> --isin <X> --exchange <E>
    ```
    The `--exchange` flag is **non-optional**. 
*   **Why**: Staking positions without an exchange forces the quote feed to stall. This triggers automatic server-side proxy staleness warnings, which degrades the *Tradability* axis of the thesis's confidence rubric.

### 4. Point-Fetch Deferral Awareness
*   **The Constraint**: Point-fetch CLI tools (like `pd ticker valuation` or `pd ticker wave-count`) **do not exist** (deferred to a future consolidated-artefact interface).
*   **Action**: Do not attempt to call them. However, the underlying analysis *skills* (like `fundamental-valuation`) remain fully valid and runnable via the autonomous loop. You can query the associated schemas using `pd schemas get valuation-v2`.

### 5. Systemic Currency Risk Integrity
*   **The Constraint**: The €25k master portfolio has a **57.0% JPY currency concentration** due to our material bottleneck anchors (Ajinomoto and Mitsubishi Gas Chemical).
*   **Action**: When scoring or rebalancing any thesis, you must verify that its **Macro Sensitivity (0-25)** axis evaluates robustness against a rapid Japanese Yen strengthening shock (below JPY 130/USD). Offset new JPY exposure with geographical hedges (like Euro-listed Soitec).

---

## Counter-Example

An agent editing the status or baskets of the ABF/CPO thesis on disk, but skipping the `pd thesis sync` command. The disk markdown claims a new allocation weight, while the database continues to calculate performance, alerts, and follower feeds against the old weights, causing silent structural drift.
