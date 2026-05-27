# Pattern: Constructing the Health Basket

The **Health Basket** is the set of non-tradable signal-only names attached to a thesis. They validate (or invalidate) the macro / bottleneck claim without contributing to allocation. The Tradable Basket is the position; the Health Basket is the truth-check.

## What belongs in a Health Basket

- **Bottleneck monopolists not tradable on retail brokers.** Canonical example: Sakai Chemical (4078.T) — the Barium Titanate monopolist in the MLCC thesis — is not on TR/DKB. See [pitfalls/sakai-chemical-liquidity](../pitfalls/sakai-chemical-liquidity.md). Watching its capacity guidance + price revisions confirms whether the upstream squeeze is intensifying.
- **Volume / utilization leaders.** E.g., Unimicron (3037.TW) in the ABF/CPO thesis — high-volume substrate manufacturer, monthly revenue + utilization rates serve as a leading indicator for the whole substrate complex.
- **Private or pre-IPO leaders.** Companies whose KPIs leak via press releases or industry reports but aren't directly tradable.
- **Specialist suppliers whose ADR liquidity is thin.** Tradable on paper, but spreads / volume make them ineffective as positions. Watch, don't hold.
- **Component-level metrics published by industry bodies.** SEMI, TrendForce, BloombergNEF — when the metric itself (not a company) is the signal.

## What does NOT belong

- A ticker the user *could* buy on a different broker. If it's available somewhere reasonable, put it in the Tradable Basket and document the broker. Don't relegate it to Health.
- A ticker that's tradable but you don't have a thesis on. The Health Basket is for **named bottleneck validators**, not a watchlist.
- Macro tickers like VIX, USDJPY, US10Y. Those belong to `macro-risk-overlay` ([reference/skills-catalog](../reference/skills-catalog.md)) which runs at portfolio level, not per-thesis.

## The vertical-proxy substitution

When a bottleneck leader can't be in the Tradable Basket, substitute a **vertical proxy** — a tradable name with deep exposure to the same upstream. Document both the original bottleneck and the proxy:

- Sakai Chemical (Health) → Murata, TDK (Tradable) — captures Barium Titanate exposure via the customer with the deepest material integration.
- Shinko Electric, M9 Materials (Health) → Ibiden, AT&S (Tradable) — captures substrate yield improvements via the buyers.
- Unimicron utilization (Health) → AT&S (Tradable) — captures the same complex via a Western alternative.

The proxy is never a perfect 1:1, but it lets the thesis hold an actual position while the Health Basket name confirms the upstream signal.

## When to promote a Health name into Tradable

Periodically check `list_available_tickers` — listings change, ADRs get added, brokerage coverage expands. If a Health name becomes tradable on TR/DKB with non-stale OHLCV and acceptable volume:

1. `manage_basket_items` to add it to the appropriate Tradable Basket on the server.
2. Drop the vertical proxy (or trim it) to make room — don't add capital, redistribute.
3. Log the structural event to the alpha log per [doctrine/log-thesis-events](../doctrine/log-thesis-events.md): "Promoted Sakai Chemical from Health to Tradable (ADR listing added on Trade Republic 2026-XX-XX); trimmed TDK 20% → 15%."
4. Update the disk `THESIS.md` + bump `Updated:`.

## How the Health Basket appears in `THESIS.md`

Per [reference/thesis-spec](../reference/thesis-spec.md), the section sits after Tradable Proxies and before Risk Management. Format:

```
## Health Basket
*Non-tradable leaders / KPIs that validate the upstream thesis. Monitor; do not hold.*

- **Sakai Chemical (4078.T)** — Barium Titanate monopolist. Watch price revisions and Q-on-Q capacity guidance.
- **Unimicron (3037.TW) utilization** — Monthly utilization rates >90% confirm substrate squeeze intensifying.
- **M9 Materials** — Privately held; T-glass capacity expansion gating the entire CPO transition.
```

Each entry: name + identifier, one-line role, one-line "what to watch."
