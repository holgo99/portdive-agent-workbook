# `agents/` — knowledge base for research agents in this repo

**New here? Read [agents/ONBOARDING.md](agents/ONBOARDING.md) first.**

This directory is the durable doctrine + recurring-pattern + known-pitfall corpus for any agent doing investment research in `deep-dives/`. Per-user / per-session memory lives elsewhere; this is what survives a fresh clone.

The companion bucket is [`theses/`](theses/) — the long-form thesis docs + assets paired by `thesis_id` to server-canonical theses on the PortDive MCP. If `agents/` answers *"how do I work in this repo?"*, `theses/` answers *"what's the current set of high-conviction investment cases?"*.

The two integration surfaces this repo operates against:
- The **`portdive` CLI** installed locally on the user's OS (see [agents/reference/portdive-cli.md](agents/reference/portdive-cli.md)).
- The **PortDive MCP** at `https://mcp.portdive.app/mcp` (see [agents/reference/portdive-mcp.md](agents/reference/portdive-mcp.md)).

---

## Files

### Onboarding

| File | What |
|---|---|
| [agents/ONBOARDING.md](agents/ONBOARDING.md) | Read this first. What this repo is, the research loop, the seven doctrines, where things live. |
| [agents/glossary.md](agents/glossary.md) | Project-specific vocabulary. |

### Doctrine — inviolable rules

| File | Rule (one line) |
|---|---|
| [agents/doctrine/boil-the-ocean.md](agents/doctrine/boil-the-ocean.md) | Completeness over speed. No deferred threads. |
| [agents/doctrine/bottleneck-first-analysis.md](agents/doctrine/bottleneck-first-analysis.md) | Always identify the physical/material bottleneck before recommending a proxy. |
| [agents/doctrine/server-is-canonical-for-theses.md](agents/doctrine/server-is-canonical-for-theses.md) | The server thesis is the source of truth for structure; disk `THESIS.md` is the long-form narrative paired by `thesis_id`. |
| [agents/doctrine/log-thesis-events.md](agents/doctrine/log-thesis-events.md) | Thesis-level structural events go to the alpha log; per-finding research stays in `RESEARCH_LOG.md`. |
| [agents/doctrine/maintain-portfolio-ledger.md](agents/doctrine/maintain-portfolio-ledger.md) | Portfolio-level risk flags, JPY FX exposure, and structural flaws must be logged continuously in `portfolio/PORTFOLIO_LOG.md`. |
| [agents/doctrine/workbook-lint-discipline.md](agents/doctrine/workbook-lint-discipline.md) | Enforce workbook-wide linting for macro consistency, link integrity, multiple freshness, and source-attribution. |
| [agents/doctrine/beyond-the-wiki-roadmap.md](agents/doctrine/beyond-the-wiki-roadmap.md) | Transition the workbook from a passive knowledge compiler to an active sovereign risk engine. |

### Patterns — how to solve recurring problems

| File | Pattern |
|---|---|
| [agents/patterns/research-loop.md](agents/patterns/research-loop.md) | The standard seven-step pipeline from catalyst to monitored thesis. |
| [agents/patterns/triple-lock-allocation.md](agents/patterns/triple-lock-allocation.md) | Monopoly Material + Tech Leader + Hidden Component + Proxy Torque (40/30/20/10). |
| [agents/patterns/skill-chain-composition.md](agents/patterns/skill-chain-composition.md) | Standalone vs playbook vs composable framework; when to use which. |
| [agents/patterns/confidence-scoring.md](agents/patterns/confidence-scoring.md) | 4-dimension rubric (catalyst certainty / tradability / sizing / macro) for the `Confidence:` field. |
| [agents/patterns/health-basket-construction.md](agents/patterns/health-basket-construction.md) | Picking non-tradable signal-only names; vertical-proxy substitution. |
| [agents/patterns/robust-ticker-resolution.md](agents/patterns/robust-ticker-resolution.md) | Resolve-or-create pipeline for unregistered assets using `pd ticker create`. |
| [agents/patterns/session-closeout-discipline.md](agents/patterns/session-closeout-discipline.md) | Closeout, changelog, and commit rules for completing agent sessions. |
| [agents/patterns/isolated-branch-execution.md](agents/patterns/isolated-branch-execution.md) | Isolated execution branches using `exec/{execution_id}-{slug}` naming standard. |

### Pitfalls — things that look right but bite

| File | Symptom |
|---|---|
| [agents/pitfalls/proxy-market-liquidity.md](agents/pitfalls/proxy-market-liquidity.md) | A valid bottleneck play is useless if it's not tradable on the user's broker (TR/DKB). |
| [agents/pitfalls/sakai-chemical-liquidity.md](agents/pitfalls/sakai-chemical-liquidity.md) | Sakai Chemical (4078.T) is a bottleneck material leader but non-tradable on retail brokers. |
| [agents/pitfalls/commodity-pricing-power-fallacy.md](agents/pitfalls/commodity-pricing-power-fallacy.md) | Assuming rising ASP indicates raw pricing power, rather than product mix shift. |

### Reference — factual + topology

| File | What |
|---|---|
| [agents/reference/role.md](agents/reference/role.md) | The operational identity, strategic mandate, and intellectual directives of the Systemic Analyst & Portfolio Manager. |
| [agents/reference/analyst-handover.md](agents/reference/analyst-handover.md) | The five-point quick-gotcha checklist for cold-starting sessions and new agents. |
| [agents/reference/thesis-spec.md](agents/reference/thesis-spec.md) | Canonical structure + skeleton for `theses/<slug>/THESIS.md`. |
| [agents/reference/research-log-spec.md](agents/reference/research-log-spec.md) | Canonical structure + skeleton for `theses/<slug>/RESEARCH_LOG.md`. |
| [agents/reference/research-workflow.md](agents/reference/research-workflow.md) | One-page quick reference mapping research-loop steps to MCP tools / skills / CLI. |
| [agents/reference/portdive-mcp.md](agents/reference/portdive-mcp.md) | Annotated catalog of MCP tools by subsystem (theses, baskets, alpha log, market data, skills, curators, sharing). |
| [agents/reference/skills-catalog.md](agents/reference/skills-catalog.md) | Annotated catalog of the PortDive Skills library + thesis templates, mapped to research-loop steps. |
| [agents/reference/portdive-cli.md](agents/reference/portdive-cli.md) | The local `portdive` CLI binary as a second operating surface. |
| [agents/reference/ingest-workflow.md](agents/reference/ingest-workflow.md) | The `ingest/` drop zone — how user-staged files get analysed and routed into thesis `assets/`. |

---

## Quality bar for entries

Every entry has:

1. **Rule** in one sentence at the top (or **What** + **Why** for reference docs).
2. **Why** — the load-bearing reason (often a past incident or trade-off).
3. **How to apply** — when/where the rule kicks in.
4. **Counter-example** when relevant — what NOT to do.

Length cap: ~200 lines per entry. Atomic — one topic per file. **Environment-independent** — no absolute paths, no relative paths to sibling repos, no machine-specific assumptions. The only paths allowed are repo-relative.

## How to add an entry

When a thesis close-out or research session surfaces a durable doctrine, pattern, or pitfall:

1. Decide the bucket (doctrine / patterns / pitfalls / reference).
2. Create the file with a kebab-case name, content following the quality bar.
3. Add the row to this AGENTS.md's index table.
4. If load-bearing enough that every agent should encounter it, link from [agents/ONBOARDING.md](agents/ONBOARDING.md).
5. The closing alpha-log entry on the source thesis points back to this new file.

## How to retire an entry

If the underlying case is gone or the rule was superseded:

1. Delete the file.
2. Remove its row from this AGENTS.md.
3. `grep -r` for inbound links and update.
