# Review of ASN-0102

I checked the operation definition, the weakest-precondition derivation, the post-state tiling, the provenance/coupling discharges, and every worked boundary configuration against the foundations.

## What I verified

- **Post-state arrangement well-formedness (X16).** The three-class tiling `[1,p) ∪ [p,p+W) ∪ [p+W, n_S+W]` exactly partitions `[1, n_S+W]` for all `1 ≤ p ≤ n_S+1`, using D-SEQ to guarantee every `s_C`-position shares the prefix `[s_C,1,…,1]` so last-component disjointness is position disjointness. S2 is discharged within `s_C` by the tiling and across the subspace boundary by T7. S8a is checked independently for copied and displaced positions, not just the anchor.
- **wp(COPY, S3★).** Correctly reduces all three mapping classes to the single copied-class obligation `a_j+i ∈ dom(Σ.C)`, discharged by C1; the equality-vs-containment remark and the `s_L`-routing vacuity are right.
- **Provenance couplings (X14).** The `New`/`Old` split is sound: J1★ fires only on genuine range extensions, J1'★'s `Old`-branch is closed via `Contains_C(Σ) ⊆ R` (P4★ at the pre-state boundary), and the `Old` addresses are correctly pinned to `s_C` positions via L14 + S3★. J0 vacuous by X1; P7/P3 discharged from frame.
- **Self-transclusion ordering (X10(b)/X15).** Pre-state resolution `resolve_Σ(R)` is the load-bearing fact; the worked `x_2`-vs-`x_3` circular-feeding example demonstrates why post-state resolution would be wrong. Atomicity grounded in SequentialTransitionAxiom for a single elementary transition.
- **Fragmentation/merge (X8, X11, X12).** Within-reference no-merge (D-SEQ source contiguity + maximal-merge), cross-origin non-merge (M16), and the two independent boundary candidates are each demonstrated, including the coalescing example where `canonical = k−1` and the leading boundary fires.
- **Boundary configurations.** Empty subspace (`n_S=0`, depth choice), append (`p=n_S+1`, trailing boundary absent), `p=1` (leading boundary absent), self-transclusion overlapping the displaced region, and cross-origin fragmentation are all worked concretely.

The depth requirements (wp analysis on a non-trivial invariant, concrete examples per boundary class, derived consequences X2–X6) are fully met, and every conjunct of ExtendedReachableStateInvariants and ExtendedTransitionInvariants is addressed.

## REVISE

(none)

## OUT_OF_SCOPE

The four Open Questions (later re-displacement, transclusion-of-transclusion containment, time-varying views, identity under unreachable allocator) are correctly deferred to future operation/versioning/GC ASNs and are not defects here.

VERDICT: CONVERGED
