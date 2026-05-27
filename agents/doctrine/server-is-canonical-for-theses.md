# Doctrine: The server thesis is canonical

**Rule.** For every thesis with a disk presence in `theses/<slug>/`, the corresponding **server thesis** (queryable via `get_thesis` / `get_thesis_health` on the PortDive MCP) is the source of truth for structure: status, baskets, items, allocations, exchanges, attached skills. The disk `THESIS.md` is the long-form narrative + visual + research depth, paired by `thesis_id` in its metadata block.

## Why

The server thesis is the only representation the PortDive ecosystem can act on. It drives `get_thesis_signals`, `get_thesis_performance`, `get_thesis_health`, `list_thesis_skills`, alpha-log scoping, and the desktop / mobile UIs. A disk-only thesis is invisible to the system — no signals, no performance, no health card, no skill attachment, no curator share surface.

Disk drift is the failure mode: a `THESIS.md` that lists Ajinomoto at 40% while the server basket has 30% means every signal, every alpha-log entry, every health calculation is reasoning against a different allocation than the one in the narrative. Followers see one thing, the analyst writes another.

## How to apply

1. **Start on the server.** Create the thesis via the app or `create_thesis` (use a template from `list_thesis_templates` when one fits). Populate baskets via `add_basket` + `manage_basket_items` — always specify `exchanges` on items.
2. **Then write the disk pair.** The disk `THESIS.md` carries `Server Thesis: <thesis_id>` and `Updated: <YYYY-MM-DD>` in its metadata block (see [thesis-spec](../reference/thesis-spec.md)). Long-form narrative, images, deep "why" go here.
3. **Round-trip on every change.** Weight rebalance, item swap, status change, exit-trigger fire → update server first (`update_thesis` / `update_basket` / `manage_basket_items`), then refresh the disk narrative + bump `Updated:`. Log the structural event to the alpha log per [log-thesis-events](log-thesis-events.md).
4. **Verify before edits.** Before touching disk allocations, `get_thesis(thesis_id)` and confirm the disk version matches. If they diverge, the server wins.

## Counter-example

Editing `theses/abf_cpo_investment_thesis/THESIS.md` to trim Ajinomoto from 40% to 30% without calling `update_basket` / `manage_basket_items` on the server. The disk doc claims the new allocation; the server keeps emitting signals and performance against the old one. Mobile / desktop / curator-share surfaces all show the stale weights. Fix forward: server change first, disk follow.

If the server thesis doesn't exist yet, the disk thesis is **draft**. Don't ship it to followers until the server pair is created and `Server Thesis:` is filled in.
