# Reference: RESEARCH_LOG.md specification

Companion to [thesis-spec](thesis-spec.md). Every thesis ships a `RESEARCH_LOG.md` next to its `THESIS.md`. The thesis is the durable case; the research log is the chain of evidence behind it.

## Why

The research log is what a cold-start agent reads to understand **how the thesis was constructed** — which sources confirmed the catalyst, which alternatives were considered, which liquidity checks were run, which macro assumptions were tested. Without it, the thesis is unaudited belief.

It is **not** an implementation plan. It is **not** a checklist. It is **not** a place for status / tasks / TODOs. Those belong elsewhere (agent memory, conversation, the thesis itself, the alpha log per [doctrine/log-thesis-events](../doctrine/log-thesis-events.md)).

## Structure

```markdown
# Research Log: <Thesis Title>

## <Topic> (YYYY-MM-DD)
- **Source:** <primary source — interview, filing, report, with author/issuer + date>
- **Finding:** <what you learned from this source>
- **Implication:** <how this affects the thesis: bottleneck, allocation, risk, exit>

## <Next Topic> (YYYY-MM-DD)
...
```

### Rules

1. **H1 title** matches the thesis title.
2. **Dated section headers** in `## <Topic> (YYYY-MM-DD)` form. Use ISO dates. One section per discovery / research event.
3. **Every claim cites a source.** A `**Source:**` line is mandatory. Prefer primary sources (management interviews, SEC filings, industry reports). Secondary sources (X threads, blog summaries) are allowed only when they reference a primary source you've verified — cite both.
4. **Findings, not plans.** Past-tense observations, not future commitments. "Identified Sakai Chemical as Barium Titanate monopolist" — yes. "Will check Sakai's Q3 capacity" — no, that's a TODO; if it's important, schedule it in the alpha log or as a thesis-level monitoring item.
5. **Implication tied to the thesis.** Every finding should connect to one of: bottleneck identification, proxy selection, allocation weight, health-basket membership, exit trigger, macro sensitivity. Findings with no implication get cut.
6. **Append, don't rewrite.** Older entries stay; revisions add a new dated entry that supersedes earlier conclusions explicitly (e.g., `## Revised Liquidity Verification (2026-08-01)`).
7. **Long-form OK, but trim ruthlessly.** A research log can grow to 200+ lines for a complex thesis. Repetitive entries get merged; speculative entries that didn't pan out get removed.

## Recommended topic headings

Useful categories (use what applies; don't force structure):

- `Catalyst Identification` — the primary event / development driving the case.
- `Bottleneck-First Analysis` — the physical / material / capacity constraint.
- `Macro Sensitivity Analysis` — JPY/USD, rates, sector regime, geopolitical.
- `Liquidity Verification` — tradability of each proxy on TR/DKB with ISIN.
- `Competitive Landscape` — peer mapping, market share, moat assessment.
- `Risk Reassessment` — when new info updates the risk picture.
- `Source Triage` — when secondary sources turn out to misrepresent the primary; record so the next agent doesn't fall into the same trap.

## Minimal example

```markdown
# Research Log: MLCC AI Squeeze

## Catalyst Identification (2026-05-17)
- **Source:** Murata Manufacturing President interview (Nikkei, 2026-05-17)
- **Finding:** Order inquiries for AI-grade MLCCs are running at 2× current supply capacity. Full-scale discussions on price increases initiated.
- **Implication:** Margin-expansion regime, not just volume-growth. Supports thesis ACTIVE status.

## Bottleneck-First Analysis (2026-05-17)
- **Source:** Industry mapping (Murata + Sakai Chemical IR materials)
- **Finding:** Sakai Chemical (4078.T) is the global leader in Barium Titanate, the ceramic powder required for sub-0.5μm MLCC dielectric layers.
- **Implication:** Upstream material bottleneck identified — primary; AT&S substrate/ECP is secondary.

## Liquidity Verification (2026-05-17)
- **Source:** `list_available_tickers` MCP call + Trade Republic broker check
- **Finding:**
  - Sakai Chemical (4078.T) — NON-tradable on TR/DKB. Health Basket only.
  - Murata Mfg. (JP3914400001) — tradable. Primary exchange OK.
  - TDK Corp (JP3538800008) — tradable.
  - Samsung GDR (US7960508882) — tradable, proxy for SEMCO.
  - AT&S (AT0000969985) — tradable.
- **Implication:** Vertical proxy substitution per [patterns/health-basket-construction](../patterns/health-basket-construction.md): Sakai → Murata + TDK.
```

## Counter-example

```markdown
# Investment Plan: ABF/CPO Super-Bottleneck

## Objective
Capitalize on the structural supply-demand imbalance...

## Implementation Steps
### Phase 1: Research & Discovery
- [x] Identify tradable tickers
- [x] Verify upstream bottlenecks
### Phase 2: Tactical Accumulation
- **Action:** Scale into positions during volatility around May 20 earnings
```

This is a tactical plan, not a research log. Plans live in conversation / agent memory / tracker tooling — they're transient, action-shaped, and they go stale. Research is durable, source-anchored, and survives the next agent.
