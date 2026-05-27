# Doctrine: Log thesis-level events to the alpha log

**Rule.** Structural events at the thesis layer — status change, weight rebalance, basket add / drop, item swap, exit-trigger fire — get an `add_alpha_log_entry` on the thesis scope. Per-finding research (catalyst spot from a source, bottleneck analysis, liquidity verification) stays in `theses/<slug>/RESEARCH_LOG.md`.

## Why

The alpha log already auto-fills with STA/MTA `SIGNAL` / `SNAPSHOT` / `DRIFT` events at roughly hourly cadence per tracked ticker — tens of thousands of entries across the user's universe. To stay useful, analyst-authored entries have to be **high-signal, thesis-level annotations**: the why behind a decision the system can't infer from price + indicators alone.

The other end of the spectrum — fine-grained research findings — belongs in `RESEARCH_LOG.md` because:
- It needs source citations + long-form context. The alpha-log surface is timeline-oriented and trims long text.
- It rarely needs sharing or notification. RESEARCH_LOG is for the next agent picking up the thesis cold.
- Per-finding noise drowns the high-signal events when followers / curators view the alpha log timeline.

## How to apply

**Alpha log (`add_alpha_log_entry`, scope = thesis):**
- Status change: `ACTIVE → WATCH`, `WATCH → CLOSED`, etc.
- Weight rebalance: e.g. "Trimmed Ajinomoto 40% → 30%; redistributed to Nittobo + AT&S after Q3 capacity guidance."
- Basket / item changes: added a basket, dropped a name from a basket, swapped a vertical proxy.
- Exit-trigger fire: "SL hit on Ajinomoto −15%; thesis closed per Risk Management §B."
- Major intel that materially shifts the case: a confirmed delay, a competitor announcement, a key source publication.

**RESEARCH_LOG.md:**
- Catalyst identification with source citation.
- Bottleneck-first analysis (which physical/material constraint, why).
- Macro sensitivity work.
- Liquidity verification per proxy (TR/DKB checks, ISIN confirmation).
- Anything that informs the thesis but isn't itself an action.

See [reference/research-log-spec](../reference/research-log-spec.md) for the file format.

## Counter-example

Calling `add_alpha_log_entry` on every paragraph of a Murata interview summary, every TrendForce report bullet, every page of a SEC filing read. The alpha log becomes a research dump; the actual thesis-level decisions get buried; followers' notifications are noisy. Fix: keep the discovery in RESEARCH_LOG with `Source:` lines; log only the resulting allocation decision or status change.

Inverse counter-example: rebalancing weights in the THESIS.md and on the server (`update_basket`) but skipping the alpha-log entry. The system has the new state but no annotation explaining the why — when the next agent or follower asks "why did this move from 40 to 30?", there's nothing in the timeline.
