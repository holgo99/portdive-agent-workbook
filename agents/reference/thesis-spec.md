# Reference: THESIS.md specification

The standardised structure for `theses/<slug>/THESIS.md` files. Companion to [research-log-spec](research-log-spec.md).

## Why

To ensure investment research is durable, visually anchored, paired to a server-canonical thesis, and actionable for both the user and the next agent picking up the case cold.

## How to apply

Every `THESIS.md` follows this structure. Style is locked — see formatting rules below; consistency across theses matters as much as the content.

### Metadata block

A bulleted list at the top of the file. Fields:

- **Status** — `ACTIVE` / `WATCH` / `CLOSED`.
- **Confidence** — 0–100% per the 4-dimension rubric in [patterns/confidence-scoring](../patterns/confidence-scoring.md). Optional inline sub-score comment: `<!-- catalyst:22 tradability:24 sizing:23 macro:17 -->`.
- **Target Horizon** — e.g. `2H 2026`, `2H 2026 – 2028`.
- **Epicenter** — one-line statement of the core bet.
- **Server Thesis** — server `thesis_id` from `list_theses` (e.g. `Server Thesis: 1`). If not yet created, `Server Thesis: (not yet created — run create_thesis to pair)` or `No PortDive equivalent...`. If carrying a shared link form like `[PortDive #N — Title](url) (share slug `slug`)`, the sync tool resolves identity via the `share slug` lookup (Option 2) rather than treating `#N` as a database ID.
- **Updated** — ISO date `YYYY-MM-DD`. Bump on every structural edit.

### Sections (in order)

1. **Visual Anchor** — image(s) in `./assets/<ingestion_quarter>/` (adopting the versioned layout format of portfolio assets, e.g. `2026_q2/`). Every image has an `*Source: ...*` attribution line directly below it.
2. **Core Architecture** — the technical "why." Bottleneck identification, supply chain, key catalysts. Cross-link to [doctrine/bottleneck-first-analysis](../doctrine/bottleneck-first-analysis.md) where relevant.
3. **Tradable Proxies** — table with `Weight | Asset | Exchange Symbol | WKN | ISIN | Strategic Role`. Always include WKN alongside ISIN — German brokers (TR/DKB) look up by WKN faster than ISIN. Include the primary exchange symbol (e.g. `TSE`) to track the lead market. If a security has no WKN, leave the cell as `—`. Allocation typically follows [patterns/triple-lock-allocation](../patterns/triple-lock-allocation.md).
4. **Health Basket** — non-tradable leaders + KPIs per [patterns/health-basket-construction](../patterns/health-basket-construction.md).
5. **Risk Management** — exit triggers, stop losses, contingency plans, macro baseline.

## Formatting rules (locked)

To keep theses visually consistent:

- **Metadata block:** bullet list (`*` or `-`), not a `>` blockquote. Bold the field name: `**Status:** ACTIVE`.
- **Section headings:** `##` for top-level sections. **No** number prefixes (`## Tradable Proxies`, not `## 2. TRADABLE PROXIES`).
- **Dividers:** `---` between major sections.
- **Image captions:** `*Source: ...*` (italicised) on its own line directly after the image, before the next paragraph.
- **Tables:** standard Markdown. Right-align the Weight column.
- **Cross-links:** link to `agents/` files by relative path from `theses/<slug>/` (i.e. `../../agents/patterns/...`).

## Location

Store every thesis under `theses/<slug>/`:
- `THESIS.md` — this spec.
- `RESEARCH_LOG.md` — [research-log-spec](research-log-spec.md).
- `assets/<ingestion_quarter>/` — versioned image + visual anchors.

Match `<slug>` to the server thesis slug when possible.

---

## Skeleton (copy-paste this)

```markdown
# Thesis: <Title>

- **Status:** <ACTIVE | WATCH | CLOSED>
- **Confidence:** <0–100>%
- **Target Horizon:** <e.g. 2H 2026>
- **Epicenter:** <one-line statement of the core bet>
- **Server Thesis:** <thesis_id from list_theses, or: (not yet created — run create_thesis to pair)>
- **Updated:** <YYYY-MM-DD>

## Visual Anchor
![<caption>](./assets/<ingestion_quarter>/<filename>)
*Source: <attribution>*

---

## Core Architecture
<The technical "why." Bottleneck identification, supply chain, key catalysts. Sub-sections via `###` headings as needed.>

### Key Catalysts
- **<Catalyst 1>:** <one-line description with date or quarter>
- **<Catalyst 2>:** <...>

---

## Tradable Proxies
*<One-line framing: e.g. Focus on the "Triple-Lock" of material and manufacturing monopolies accessible via German brokers.>*

| Weight | Asset | Exchange Symbol | WKN | ISIN | Strategic Role |
| ---: | --- | --- | --- | --- | --- |
| **40%** | **<Name>** | `<Symbol>` | `<WKN>` | `<ISIN>` | **<Role.>** <One-line rationale.> |
| **30%** | **<Name>** | `<Symbol>` | `<WKN>` | `<ISIN>` | **<Role.>** <One-line rationale.> |
| **20%** | **<Name>** | `<Symbol>` | `<WKN>` | `<ISIN>` | **<Role.>** <One-line rationale.> |
| **10%** | **<Name>** | `<Symbol>` | `<WKN>` | `<ISIN>` | **<Role.>** <One-line rationale.> |

---

## Health Basket
*Non-tradable leaders / KPIs that validate the upstream thesis. Monitor; do not hold.*

- **<Name (Identifier)>** — <one-line role>. <What to watch.>
- **<Name (Identifier)>** — <one-line role>. <What to watch.>

---

## Risk Management

### Exit Triggers
- **Exit Trigger A:** <event-based — e.g. confirmed catalyst hits>.
- **Exit Trigger B (Invalidation):** <thesis-invalidating signal>.

### Stop Losses
- <Per-position SL — e.g. >15% drawdown in <name> indicates structural disruption>.

### Macro Baseline
<Macro regime assumptions; conditions under which the case breaks.>
```

## Cross-references

- [research-log-spec](research-log-spec.md) — the companion `RESEARCH_LOG.md` format.
- [patterns/triple-lock-allocation](../patterns/triple-lock-allocation.md) — the canonical allocation pattern.
- [patterns/confidence-scoring](../patterns/confidence-scoring.md) — the `Confidence:` rubric.
- [patterns/health-basket-construction](../patterns/health-basket-construction.md) — picking Health Basket names.
- [doctrine/bottleneck-first-analysis](../doctrine/bottleneck-first-analysis.md) — identifying the upstream constraint.
- [doctrine/server-is-canonical-for-theses](../doctrine/server-is-canonical-for-theses.md) — pairing rule.
- [pitfalls/proxy-market-liquidity](../pitfalls/proxy-market-liquidity.md) — broker-liquidity check.
