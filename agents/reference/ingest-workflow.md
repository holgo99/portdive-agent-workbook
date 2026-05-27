# Reference: The `ingest/` workflow

`ingest/` is a **local-only drop zone** at the repo root. The user puts files there — PDFs, screenshots, transcripts, earnings decks, charts — and asks the agent to analyse them, build something from them, or route them into a thesis. The agent consumes the content and/or moves the file(s) to the right thesis's `assets/` folder. **Nothing stays in `ingest/` permanently.**

## Rule

**`ingest/` is not tracked in git.** It's listed in `.gitignore`. Files there are transient — env-specific user inputs that don't belong in the shared knowledgebase. Never commit them, never reference them by path from `theses/` or `agents/` docs.

## How the workflow runs

When the user references files in `ingest/`:

1. **Inspect what's there.** `ls ingest/` (or a more specific subdirectory like `ingest/<TICKER>/`). The user typically organises by ticker / topic, but not always.

2. **Read / analyse the file inline.**
   - **PDFs:** use `Read` with the `pages` parameter for large docs (mandatory >10 pages).
   - **Images / screenshots:** `Read` the image; the multimodal model sees it directly.
   - **Markdown / text:** `Read` straight through.
   - **Other formats:** convert or extract via `Bash` (e.g. `pdftotext`, `magick`).

3. **Decide the destination.** Four outcomes:
   - **Pure analysis** — the file was the input to a question; no artefact needs to land. Summarise in conversation; the file can stay in `ingest/` (the user will clean up) or be deleted with explicit confirmation.
   - **Becomes a thesis asset** — the image or doc anchors a specific single thesis. **Move** (don't copy) to `theses/<slug>/assets/<ingestion_quarter>/` (adopting the versioned layout format of portfolio assets, e.g. `2026_q2/`), reference from the thesis with a relative path + `*Source: ...*` attribution per [thesis-spec](thesis-spec.md). Update `Updated:` on the thesis.
   - **Becomes a shared portfolio asset** — the asset (e.g. rack BoMs, industry-wide roadmaps) is referenced by *multiple* theses. **Move** to `portfolio/assets/<technology_domain>/<ingestion_quarter>/<filename>`, using Option 1's domain-first versioned layout. Add the asset to the catalog in [PORTFOLIO.md](../../portfolio/PORTFOLIO.md), and reference relatively via `../../portfolio/assets/<domain>/<quarter>/<filename>` in all dependent theses.
   - **Becomes an alpha-log attachment** — for one-off intel that lands in the timeline, use `generate_alpha_log_upload_url` + `upload_alpha_log_attachment` and then delete the local copy with explicit confirmation.

4. **Confirm before deleting.** Even though files in `ingest/` are local-only, deleting is irreversible from the agent's side — always confirm with the user before `rm`ing.

5. **Source attribution survives the move.** When a file moves into `theses/<slug>/assets/`, the filename should still let the user trace the source (or you record the source in the `*Source: ...*` line under the image in `THESIS.md`). Don't rename to opaque slugs.

## File-handling guidance

- **Shared portfolio assets domain routing** — Shared assets must be categorized under one of the defined technology domains in `portfolio/assets/`:
  * `rack_architectures/` (e.g. system level BoM comparison charts, node layouts)
  * `substrate_materials/` (e.g. ABF build-up film, glass core substrate roadmaps)
  * `passives_components/` (e.g. high-capacitance MLCCs, inductors)
  * `networking_photonics/` (e.g. CPO modulators, light sources, silicon photonics timeline charts)
  * `data_storage/` (e.g. NAND flash controller roadmaps, database engines)
  * `geopolitics_macro/` (e.g. supply chain localization timelines, currency hedging matrices)
- **Subdirectory by ticker / topic** — the user typically organises `ingest/<TICKER>/...`. Respect the structure when looking for context (e.g., `ingest/NVO/` is Novo Nordisk material). Don't flatten when moving — the per-thesis `assets/` folder is flat.
- **Preserve dates in filenames** when meaningful — e.g. `LMIA-Q1-earnings-transcript.md` already encodes the period. Keep that signal when moving.
- **Strip cache-bust / hash suffixes** — names like `LMIA-urn_slides_quartr.com_3320412-4df6bf058502533fbc65f42dc1e3824a_398bb.pdf` should be renamed to something human-readable on the move (e.g. `LMIA-Q1-2026-quartr-slides.pdf`).
- **Image filenames** — names like `HIvnIQoagAAp8R5.png` (a typical Twitter / X image hash) should be renamed by what they show (e.g. `mlcc-supply-bottleneck-chart.png`).

## What does NOT belong in `ingest/`

- Anything that's already in a thesis (`theses/`) or assets folder — move, don't duplicate.
- Anything from a public source you can fetch on demand — link, don't snapshot.
- Anything sensitive (broker account exports with PII, API keys, credentials) — `ingest/` is local but still on the user's disk; broker exports get processed and deleted immediately, never committed anywhere.

## Cold-start cue

When you see this in the repo for the first time and `ingest/` exists with files, the user has likely staged something for you to act on. Either:
- Ask what they'd like done with the files, or
- If the conversation already implies a target (e.g., "look at the LMIA earnings call"), proceed with step 1 above.

`ingest/` being empty means there's nothing pending — that's the steady state.
