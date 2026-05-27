# Pattern: Confidence scoring

The `Confidence:` field in a thesis metadata block (see [thesis-spec](../reference/thesis-spec.md)) is a 0–100% score. Without a rubric, the number is a vibe. With one, two theses' confidence can be compared.

## The rubric

Each of the four dimensions contributes up to **25 percentage points**. The thesis confidence is the sum.

### Catalyst certainty (0–25)

How load-bearing is the catalyst, and how strong is the evidence?

- **23–25**: Multiple **primary** sources confirm the catalyst (e.g., management guidance + SEC filing + industry report). Concrete date or quarter. Quantified impact.
- **17–22**: One primary source + one or more credible secondary sources. Date range known. Impact directionally clear, magnitude estimated.
- **10–16**: One primary source. Vague timing. Magnitude inferred.
- **5–9**: Secondary sources only. No primary confirmation. Timing speculative.
- **0–4**: Catalyst is structural / inferred from trend; no event-specific evidence.

### Tradability (0–25)

How clean is the access path on the user's brokers (TR / DKB primary)?

- **23–25**: All tradable proxies are confirmed on TR/DKB, fresh OHLCV data (no staleness flags from `list_available_tickers`), tight spreads observed historically.
- **17–22**: All tradable proxies are confirmed. Minor staleness on a non-primary exchange but a primary exchange is fresh.
- **10–16**: One proxy requires an OTC ADR or alternative listing. Or one position is in the basket on faith pending verification.
- **5–9**: Mixed liquidity. At least one proxy has documented staleness or thin volume.
- **0–4**: Bottleneck leader is non-tradable and only vertical proxies are available (see [pitfalls/sakai-chemical-liquidity](../pitfalls/sakai-chemical-liquidity.md)).

### Position-sizing risk (0–25)

How well-calibrated are the weights, and how much idiosyncratic risk does any single name carry?

- **23–25**: Allocations follow a documented pattern (e.g., [triple-lock-allocation](triple-lock-allocation.md)); top position ≤ 40%; basket diversifies across at least two structural drivers; explicit stop-loss per position.
- **17–22**: Triple-lock or analogous structure; top position 40–50%; documented exit triggers but not per-position SLs.
- **10–16**: Concentration > 50% in one name OR no documented allocation pattern.
- **5–9**: Concentration > 60% with no exit plan.
- **0–4**: Single-name bet, no diversification or risk-controls documented.

### Macro sensitivity (0–25)

How robust is the case across plausible macro regimes?

- **23–25**: Case works in 3+ regimes (e.g., rates-up, rates-down, FX shock); `macro-risk-overlay` regime read is supportive or neutral.
- **17–22**: Works in 2 regimes; one specific macro risk identified with a mitigation (FX hedge, vertical diversification).
- **10–16**: Works in current regime; explicit dependency on one macro factor (e.g., JPY weakness, sub-5% 10Y).
- **5–9**: Significant macro tailwind already priced; reverts on regime change.
- **0–4**: Single-macro bet with no diversification.

## Worked example

For the disk **ABF/CPO** thesis (current label: 94%):

- Catalyst certainty: ~22 (multiple sources — TrendForce, GF Overseas; Rubin timing pinned to September 2026; quantified 5–10x ABF demand).
- Tradability: ~24 (Ajinomoto / Ibiden / Nittobo / AT&S all confirmed on TR/DKB).
- Position-sizing: ~23 (triple-lock 40/30/20/10; documented exit triggers + stop loss).
- Macro sensitivity: ~17 (works in AI-capex regime; vulnerable to a hard hyperscaler-capex pullback; partial JPY hedge via AT&S).

Sum ≈ **86**. The 94% label looks ~8 points high; document the actual rubric scores in the metadata block so the next agent can interrogate them.

## How to apply

1. Score each dimension when authoring or updating a `THESIS.md`.
2. Write the four sub-scores into a comment in the metadata block (e.g. `<!-- catalyst:22 tradability:24 sizing:23 macro:17 -->`) so future you / the next agent can audit.
3. Re-score on every status change or weight rebalance — note the new sub-scores in the alpha-log entry per [doctrine/log-thesis-events](../doctrine/log-thesis-events.md).

## What this is not

This rubric is not a probability. A 94% confidence does not mean a 94% chance of positive return. It means: across catalyst evidence, access, sizing discipline, and macro robustness, the case is well-constructed. The expected return is a separate question, addressed by `fundamental-valuation` + `bayesian-risk-assessment`.
