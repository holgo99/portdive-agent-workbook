# Onboarding for any agent picking up research here

Read this once. It's distilled. Deeper detail lives in the four buckets:

- **[doctrine/](doctrine/)** — inviolable rules. If a doctrine and a temptation conflict, the doctrine wins.
- **[patterns/](patterns/)** — how to solve recurring problems correctly.
- **[pitfalls/](pitfalls/)** — things that look right but bite. Each has symptom → why → fix.
- **[reference/](reference/)** — factual / topology / "where does X live."

See [../AGENTS.md](../AGENTS.md) for the full index.

---

## 1. What this repo is

`deep-dives/` is an **investment-research workbook** for the PortDive ecosystem. Its purpose: drive PortDive end-to-end to research, write, and maintain investment theses with long-form narrative + assets.

Two integration surfaces:

1. **PortDive MCP** at `https://mcp.portdive.app/mcp` — primary surface for everything structured: theses, baskets, items, signals, performance, alpha log, market data, the Skills library. See [reference/portdive-mcp.md](reference/portdive-mcp.md).
2. **`portdive` CLI** installed locally on the user's OS — second surface for batch / scripted / file-system work. See [reference/portdive-cli.md](reference/portdive-cli.md).

The ecosystem ships **32 skills** + **5 thesis templates** today. See [reference/skills-catalog.md](reference/skills-catalog.md).

---

## 2. The research loop

The standard eight-step pipeline (full doctrine in [patterns/research-loop.md](patterns/research-loop.md)):

0. **Branch Isolation (When spawned)** — Immediately checkout to a dedicated branch `exec/{execution_id}-{slug}` before modifying any repository files per [patterns/isolated-branch-execution.md](patterns/isolated-branch-execution.md).
1. **Catalyst spot** — primary source verified, captured in `RESEARCH_LOG.md`.
2. **Bottleneck-first** — identify the physical / material constraint before any proxy.
3. **Liquidity verification** — resolve symbol/ISIN; if missing from server, register it via `pd ticker create` per [patterns/robust-ticker-resolution.md](patterns/robust-ticker-resolution.md).
4. **Skill-chain validation** — `run_skill("investment-analysis-playbook")` or per-step.
5. **Server thesis creation** — `create_thesis` (optionally from a template) + baskets + items (always with `exchanges`).
6. **Local artefacts** — write `theses/<slug>/THESIS.md` + `RESEARCH_LOG.md` paired by `Server Thesis: <thesis_id>`.
7. **Monitor** — `get_thesis_health` / `get_thesis_signals` / `get_thesis_performance`; alpha-log thesis-level events.
8. **Session closeout** — update `CHANGELOG.md` and commit all modifications atomically in a single semantic commit per [patterns/session-closeout-discipline.md](patterns/session-closeout-discipline.md).

Quick reference cards: [reference/role.md](reference/role.md) (analyst mandate), [reference/research-workflow.md](reference/research-workflow.md) (workflow mapping), and [reference/analyst-handover.md](reference/analyst-handover.md) (cold-start checklist).

---

## 3. The seven doctrines you must internalise

If you remember nothing else, remember these:

1. **[Boil the ocean](doctrine/boil-the-ocean.md)** — completeness over speed. No deferred threads. The bar is *"holy shit, that's done."*

2. **[Bottleneck-first analysis](doctrine/bottleneck-first-analysis.md)** — always identify the physical or material bottleneck before recommending a proxy. Ajinomoto > Foxconn. Sakai Chemical > Murata (then proxy-substitute because Sakai is non-tradable).

3. **[The server thesis is canonical](doctrine/server-is-canonical-for-theses.md)** — disk `THESIS.md` is the long-form narrative paired by `thesis_id` to a server thesis. Server first, disk follows. Never let disk drift from server allocations.

4. **[Log thesis-level events](doctrine/log-thesis-events.md)** — structural events (status change, rebalance, exit-trigger fire) go to the alpha log via `add_alpha_log_entry`. Per-finding research stays in `RESEARCH_LOG.md`. Don't pollute the timeline.

5. **[Maintain the portfolio risk ledger](doctrine/maintain-portfolio-ledger.md)** — track cross-thesis risks (like JPY FX exposure or Blackwell/Rubin delay correlations) and active overrides in `portfolio/PORTFOLIO_LOG.md` to prevent "phantom hedges."

6. **[Workbook linting and global consistency](doctrine/workbook-lint-discipline.md)** — enforce workbook-wide consistency checks, link integrity, multiple freshness, and source-attribution to keep the knowledge base pristine.

7. **[Beyond the LLM Wiki](doctrine/beyond-the-wiki-roadmap.md)** — transition from a passive knowledge compiler (Karpathy's LLM Wiki) to an active, sovereign adversarial risk engine and capital custodian.

---

## 4. The PortDive ecosystem at a glance

| Surface | What it gives you |
|---|---|
| [reference/portdive-mcp.md](reference/portdive-mcp.md) | All MCP tools by subsystem: theses, baskets + items, alpha log, market data, skills, curators, sharing. Includes the data-freshness rule and OHLCV `analysis_mode` convention. |
| [reference/skills-catalog.md](reference/skills-catalog.md) | The 32 skills + 5 thesis templates, annotated. Composable frameworks (Elliott Wave, Wyckoff, Bayesian) vs standalone vs playbooks. Loop-step → skill mapping table. |
| [reference/portdive-cli.md](reference/portdive-cli.md) | The local CLI binary. Use for batch / scripted / file-system work. |

---

## 5. Where things live

```
deep-dives/
├── AGENTS.md                       — repo root: master AI index & ruleset
├── README.md                       — repo root: human architectural blueprint & decisions log
├── IDENTITY.md                     — repo root: global unique node identity & agent registration
├── agents/                         — AI analyst knowledge base sub-assets (our Brain)
│   ├── ONBOARDING.md               — you are here
│   ├── SOUL.md                     — the full statement of boil-the-ocean
│   ├── glossary.md
│   ├── doctrine/
│   ├── patterns/
│   ├── pitfalls/
│   └── reference/
├── theses/
│   └── <slug>/
│       ├── THESIS.md               — long-form thesis (paired by Server Thesis: <id>)
│       ├── RESEARCH_LOG.md         — dated research entries with sources
│       └── assets/                 — images + visual anchors
└── ingest/                         — LOCAL-ONLY drop zone (gitignored)
                                      User stages files here; agent analyses
                                      and routes into theses/<slug>/assets/
                                      or consumes inline. See
                                      reference/ingest-workflow.md.
```

`<slug>` is kebab-case or snake_case; match the slug used in the server thesis when possible. `ingest/` is gitignored — files there are transient and env-specific. See [reference/ingest-workflow.md](reference/ingest-workflow.md).

---

## 6. Glossary

If a term feels project-specific, it probably is. See [glossary.md](glossary.md) for: Investor / Curator / Follower, Tradable Proxy, Health Basket, Bottleneck, Epicenter, Triple-Lock, Skill / Playbook / Artefact, Alpha Log, STA / MTA, and the rest.

---

## 7. Memory vs docs

The agent host has a per-user persistent memory under `~/.claude/projects/`. That memory is:

- **Session state** — what's in flight, ephemeral context.
- **Per-user preferences** — collaboration style with this specific user.

This `agents/` directory is:

- **Doctrine + durable rules** — survive any thesis / session / user.
- **Repo-versioned + reviewable** — every contributor sees the same thing.
- **Environment-independent** — no machine-specific paths anywhere in here.

Migration rule: *if a different agent on a different machine working from a fresh clone would benefit, it belongs here.* If only this user's future sessions benefit, it stays in agent memory.

---

## 7.1. Human-Targeted Documentation (Ignored by Agents)

- **The root-level `README.md`** contains human-targeted meta-documentation detailing workbook architecture, historical decisions, and qualitative insights for human analysts.
- **Agent Rule:** AI agents must treat the root-level `README.md` as read-only human-managed space. AI agents must **never** modify or edit `README.md`, leaving it entirely as human-managed space.

---

## 8. When you're stuck

- **Don't know which skill to run for an analysis?** → [reference/skills-catalog.md](reference/skills-catalog.md) → loop-step → skill mapping table.
- **Server thesis structure unclear before edits?** → `get_thesis(thesis_id)` first; never edit the disk pair against stale knowledge of the server.
- **Liquidity check flagged stale data?** → suggest an alternative exchange to the user, flag the data quality concern in the analysis, or skip the ticker. Don't silently consume stale OHLCV.
- **Unresolved ticker or asset not on the server?** → Register it idempotently using `pd ticker create` before adding to baskets per [patterns/robust-ticker-resolution.md](patterns/robust-ticker-resolution.md).
- **Bottleneck leader is non-tradable?** → vertical-proxy substitution via [patterns/health-basket-construction.md](patterns/health-basket-construction.md).
- **Tracker has open questions you can't resolve from sources?** → ask the user with concrete options via `AskUserQuestion`. Don't guess.
