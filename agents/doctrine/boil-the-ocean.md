# Doctrine: Boil the ocean

**Rule.** Completeness over speed. No deferred threads. No workarounds when the real fix is in reach. The bar is *"holy shit, that's done."*

The full statement of the doctrine lives in [SOUL.md](../SOUL.md) — read it. This file is the operational reading.

This is the highest doctrine. It overrides every other rule below if they ever conflict.

## How to apply

- **No deferred threads.** If a research finding contradicts the current thesis, resolve it in this session — update the thesis, the research log, and the server pair. Don't drop a TODO and move on.
- **No workarounds when the real fix exists.** A health-basket name that just became tradable on TR/DKB → promote it and rebalance (see [patterns/health-basket-construction](../patterns/health-basket-construction.md)). Don't leave the vertical proxy in place just because it ships faster.
- **No "good enough."** A thesis that ships with placeholder WKNs, missing ISIN entries, no Source: lines, or a mismatch between disk allocation and server allocation is unfinished. Finish it.
- **Search before building.** Existing skills, patterns, and pitfalls cover 80% of recurring problems. Read [reference/skills-catalog](../reference/skills-catalog.md) and [patterns/](../patterns/) before authoring something new.
- **Verify before shipping.** Run `get_thesis(thesis_id)` and confirm disk + server match before declaring an edit complete. Run `list_available_tickers` and check staleness flags before signing off on liquidity.
- **One session per slice.** Don't fan a thesis update across multiple half-finished sessions. Land it.

## When the doctrine is hard

Three temptations to resist:

1. **"This is out of scope."** Often it isn't — research surfaces side findings (a new bottleneck, a competing thesis, a macro shift) that materially affect the case. Bundle them into the same update; don't ship a stale thesis with a "see follow-up" note.
2. **"I'll add the Source: line later."** No. Every claim cites its source the moment it lands in `RESEARCH_LOG.md` (see [reference/research-log-spec](../reference/research-log-spec.md)). Source attribution after-the-fact is unreliable.
3. **"I'll sync to the server next session."** No. Server is canonical ([doctrine/server-is-canonical-for-theses](server-is-canonical-for-theses.md)); the sync is part of the work, not after it.

## Related

- [doctrine/server-is-canonical-for-theses](server-is-canonical-for-theses.md) — boil-the-ocean amendments land on the server *and* on disk, in the same session.
- [doctrine/bottleneck-first-analysis](bottleneck-first-analysis.md) — completeness includes naming the upstream constraint, not just identifying proxies.
- [doctrine/log-thesis-events](log-thesis-events.md) — completing a structural change means alpha-logging it, not just editing the files.
