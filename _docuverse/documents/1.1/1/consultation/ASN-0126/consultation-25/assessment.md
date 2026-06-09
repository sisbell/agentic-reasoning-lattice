# Channel Assignment — ASN-0126 review-25

**Date:** 2026-06-09 08:24

## Issue 1: The gate-vs-landing distinction is restated five times in abstract prose
Reason: Pure consolidation of existing prose — the distinction and its single canonical home (The shape-gated emit) are already in the note. No design intent or implementation evidence is at stake; the fix is deleting redundant restatements and trimming P4/P6 to a back-pointer.

## Issue 2: Repeated downstream deferrals to "The shape-gated emit"
Reason: Editorial deduplication of cross-references to a section that already exists in the note. Deciding which single pointer to keep is internal to the note's structure; no channel needed.

## Issue 3: The "Gate realizability — the liveness dual of P4" lead paragraph is motivational meta-prose
Reason: Removing apologia and opening with P6's existing statement is a presentation change; the lemma and its justification are already present. Derivable from the ASN alone.

## Issue 4: "dom(Σ.L) carries only conforming tuples" rests on an unstated initial condition
Reason: The base condition `Σ_init.L = ∅` is inherited from ASN-0086's initial state, which this note already builds on via `π(Σ_init) = Σ_init^{0086}`; stating it explicitly parallels C0 and is derivable from material already cited in the note.

## Issue 5: Defensive authority-citations accreted around the |F|=1 design choice
Reason: The task is *removing* surplus Nelson/Gregory citations while keeping one anchor per claim — a trimming decision, not a new evidentiary need. The structural arguments (single-source lattice usage, unsatisfiable coverage-singleton) already carry the claims internally.

## Issue 6: The coalescing-divergence paragraph duplicates its own resolution
Reason: State the coalescing rule once, generalized to any single-span slot — a within-section deduplication using content already present. No external input required.
