# Pitfall: Proxy Market Liquidity

**A valid bottleneck play is useless if it's not tradable on the user's broker (TR/DKB).**

## Symptom
The agent identifies **Unimicron** as the #1 play for ABF substrates, but the user cannot execute the trade on Trade Republic or DKB. The agent spends 3 turns researching a non-tradable asset, wasting context and user time.

## Why
Many top-tier semiconductor suppliers are listed in Taiwan (TWSE) or Japan (TSE) without liquid ADRs or secondary listings on the Lang & Schwarz (LS) exchange used by Trade Republic.

## How to avoid
1.  **Verify First:** Before doing a deep dive into a company's financials, check its ISIN against German exchanges (Frankfurt/Tradegate/L&S).
2.  **Search Tickers:** Use `google_web_search` for "[Company] ticker Trade Republic" or "[Company] ISIN Lang & Schwarz".
3.  **Provide Proxies:** If the leader is missing, immediately offer the closest tradable alternative (e.g., AT&S for Unimicron).
4.  **ETF Fallback:** Use the `iShares MSCI Taiwan` or `VanEck Semiconductor` ETFs as a way to "capture" the non-tradable leaders.
