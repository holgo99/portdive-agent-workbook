# Doctrine: Maintain the Portfolio-Level Risk Ledger

> [!IMPORTANT]
> **Rule.** Cross-thesis risk overrides, JPY/USD FX exposure, sizing mismatches, and structural flaws must be continuously logged as active flags in `portfolio/PORTFOLIO_LOG.md`. The ledger must serve as the absolute source of truth for portfolio-level vulnerabilities.

## Why

Sizing and structural risks (e.g., currency concentration, technological correlation, counterparty counter-hedging) span multiple investment features. If these risks are only addressed in conversational sessions or scattered across individual `THESIS.md` narratives, the master capital pool becomes fragile.

Furthermore, "phantom hedges" occur when risk analyses claim a mitigant (e.g., merchant power hedging a grid freeze) that is not actually sized or held in the active capital ledger (`portfolio/PORTFOLIO.md`). Maintaining a continuous, chronological portfolio ledger ensures absolute transparency between risk claims and active ledger realities.

---

## How to Apply

1.  **Identify Cross-Thesis Risks**: 
    If a vulnerability affects multiple allocations (e.g., a Blackwell/Rubin delay exposing 66.5% of our capital, or Kyoto tech exporters representing 57.0% Yen exposure), it belongs in the portfolio-level ledger, not individual theses.
2.  **Log Chronologically**: 
    Log the risk immediately in `portfolio/PORTFOLIO_LOG.md` using the format `FLAG-YYYYMMDD-NN-SLUG`. Specify:
    *   **Date Logged** and **Severity** (`CRITICAL` / `HIGH` / `MEDIUM` / `LOW`).
    *   **Category** and a concise **Description** of the structural flaw.
    *   A concrete **Mitigation Pathway** (e.g., option collar triggers, proxy swaps, or capital reallocations).
3.  **Prevent Phantom States**: 
    Never document a portfolio mitigant or hedge in `PORTFOLIO_ANALYSIS.md` without verifying that the position is explicitly sized in `PORTFOLIO.md` and created on the server database.
4.  **Audit on Rebalances**: 
    Before performing an asset rebalance or deploying satellite cash, review active portfolio flags to verify the action does not exacerbate an existing vulnerability.

---

## Counter-Example

Listing Delta Electronics (Thailand) as an active 1.8% portfolio mitigant to our grid queue freeze in the risk matrix, while keeping our master capital pool 100% deployed elsewhere in the matrix. This creates a "phantom mitigant" that falsely reassures stakeholders and leaves the portfolio exposed to unhedged drawdowns.
