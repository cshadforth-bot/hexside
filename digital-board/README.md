# Hexside digital board

A playable, single-file HTML/JS implementation of the Base Game rules (human vs. CPU) —
kickoff draft, Command Card hand and deck, dice-based Pass/Dribble/Shot/Tackle resolution,
Save-retention, Discipline/sin-bin, and all 12 optional Character Skins.

**Live at:** https://claude.ai/artifact/WCguFDkgtjzfBDuXxSghSs (private; version 16 as of
2026-09-22)

## This is a snapshot, not the source of truth

The live Artifact is what's actually playable and is updated independently of this repo.
`hexside-board.html` here is a **copy of the page as last published**, tracked so it shows
up in `git log`/diffs like everything else — but editing this file directly does nothing
until it's re-published.

**To make a change:**
1. Read the live page back into a local file (`Artifact({action:"read", url:"..."})` from
   a Claude session) rather than trusting this copy is current — the Artifact may have
   been republished from a different session since this file was last updated here.
2. Edit that fresh copy.
3. Publish it back to the same URL (`Artifact({action:"publish", url:"...", file_path:...})`)
   so the change goes live.
4. Copy the same file over `hexside-board.html` here and commit, so this snapshot catches up.

## Independent from the print/engine build

This is its own, 3rd implementation of the Hexside rules (alongside `engine/` +
`playtest-ai/`'s Python drivers) — nothing here is shared or auto-generated from those, and
a fix or feature in one does **not** propagate to the others. If you change a rule anywhere,
check whether it also needs to change here (see `project_hexside_duplicated_logic_bug_check`
and `project_hexside_digital_board_bounce_vision_geometry` in memory for two real examples
of this surfacing bugs).

Deliberately **not** wired into `build-pdfs.sh` — it's an interactive app, not a print
layout, so it isn't a `source/*.html` file and headless print-to-PDF wouldn't produce
anything meaningful from it.
