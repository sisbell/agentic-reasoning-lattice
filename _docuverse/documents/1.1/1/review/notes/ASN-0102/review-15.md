# Review of ASN-0102

This is a thorough and largely rigorous note. The wp(COPY, S3★) reduction, the X16 tiling argument, the X7 overwrite analysis, and the X8 fragmentation argument are all carefully done and survive scrutiny. The issues below are completeness/depth gaps in an otherwise strong spec.

## REVISE

### Issue 1: ActivatedEmission is never discharged
**ASN-0102, X14**: The quoted ExtendedReachableStateInvariants list includes `… ∧ NodeLineage ∧ ActivatedEmission ∧ L0 …`, but the discharge prose covers the entity/link/node bucket as "L0, L1, L1a, L1b, L1c, L3, L14, L-fin, CL-OWN, CL-UNIQ, P8, NodeLineage" — **ActivatedEmission is absent**, and it is addressed nowhere else (the arrangement-side and P6/P7/S4 paragraphs do not touch it).
**Problem**: The note's own method is exhaustive per-conjunct discharge; one required conjunct is silently skipped. Every other conjunct of the theorem is named.
**Required**: Add ActivatedEmission to the vacuous bucket with the one-line reason: `Σ'.E = Σ.E` and COPY activates/spawns no entity-level sub-allocator, so the existential witness for each non-node entity carries forward unchanged.

### Issue 2: ExtendedTransitionInvariants (P3) is not discharged
**ASN-0102, X14**: The note discharges ExtendedReachableStateInvariants (per-state) and the composite-boundary properties P4★/P4a/P7a, but never addresses the separate foundation theorem ExtendedTransitionInvariants, whose sole conjunct is **P3** (`dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R' ∧` value-fixity on C, L).
**Problem**: COPY is a transition; the foundation requires P3 of every valid transition. It is trivially satisfied here (C'=C, L'=L, E'=E, R'⊇R), but the obligation is named in the foundation and left unstated.
**Required**: State P3 preservation explicitly, citing the COPY frame (`Σ'.C=Σ.C`, `Σ'.L=Σ.L`, `Σ'.E=Σ.E`, `Σ'.R = Σ.R ∪ {…} ⊇ Σ.R`).

### Issue 3: Worked example does not exercise the subtlest part of X14
**ASN-0102, "A worked example"** and **X14 (New/Old split)**: The example is a cross-origin, distinct-source copy where `Old = A ∩ ran(Σ.M(d))` is empty, so it checks X1/X3/X7/X8/X9/X11/X12/X16 but never the provenance/coupling postcondition.
**Problem**: The most intricate reasoning in the note is the J1'★ discharge for `a ∈ Old` (the case where a pair is *not* added to `R∖R` because `(a,d)` is already in `R` by P4★) — which only arises under self-transclusion or re-copy. This non-trivial branch is never validated against a concrete scenario, and the standards make a concrete example of key postconditions (and a non-trivial wp branch) mandatory.
**Required**: Add (or extend) a worked scenario with `d_s = d` so `Old ≠ ∅`, and trace through `Σ'.R`, showing J1★ records the `New` addresses and J1'★ is vacuous on the `Old` addresses via their pre-state presence in `R`.

## OUT_OF_SCOPE

(none — the note correctly defers INSERT/DELETE displacement mechanics and the Open Questions to future ASNs.)

VERDICT: REVISE
