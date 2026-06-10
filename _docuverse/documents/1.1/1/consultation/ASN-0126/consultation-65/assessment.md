# Channel Assignment — ASN-0126 review-65

**Date:** 2026-06-09 19:16

## Issue 1: R-Scope frame argument closes with a redundant, misdirected exhaustiveness claim
Reason: Internal. The note already establishes the within-branch wrapper-vs-Nullify transfer via `a_emit` F-blindness two sentences earlier, and already states that `a_emit(Σ, d_retr)` does not depend on the named target `a` — both the deletion and the optional one-clause self-reference remark are derivable from the note's own reasoning.

## Issue 2: Projection bridge names a lemma no use-site invokes
Reason: Internal. The conservative fix (drop L-ContiguousPrefix from the apposition) is pure citation hygiene, and deciding whether the worked illustration's `inc(ℓ_prev, 0)` enumeration rests on the lemma is a question about the note's own argument structure plus the already-stated ASN-0086 lemma conclusion — no design intent or fresh implementation evidence is required.

## Issue 3: C0 re-states the well-formedness characterization verbatim from Registration entries
Reason: Internal. The fix is pure deduplication — replace C0's restated characterization with a reference to Registration entries plus the one novel finiteness clause `|Σ_init.registry| < ∞`, all sourced from text already in the note.
