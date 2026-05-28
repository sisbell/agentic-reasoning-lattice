# Review of ASN-0102

I checked each of X1–X16 against its derivation, the precondition P1–P4, the full five-component frame, the invariant discharges in X14, the worked example, and the boundary cases (empty subspace, append position `p = n_S+1`, small vs. large `W`, cross-origin, self-transclusion).

## REVISE

*(none)*

Key verifications performed:

- **Tiling (X16).** The three post-state classes occupy last-component ranges `[1,p)`, `[p,p+W)`, `[p+W,n_S+W]`, which partition `[1,n_S+W]` with no gap/overlap for `1 ≤ p ≤ n_S+1`. D-SEQ★/D-MIN★ and S2/S8a discharges are sound; the empty-subspace case correctly specialises to `p=1`.
- **No-overwrite (X7).** The freed-vs-occupied distinction is correct: the conclusion rests on disjointness of copied last-components `[p,p+W)` and displaced-image `[p+W,n_S+W]`, not on `[v,v+W)` having been fully populated. The small-`W` proper-subset case is handled.
- **wp(COPY, S3★).** The reduction to the copied region (unmoved + displaced discharged by X1 and the link-frame) is valid, and the equality (not containment) form is justified by P3 fixing `subspace(v+c)=s_C`. Discharge via C1 is correct, and P1's `subspace(u_i)=s_C` is the right hypothesis under which C1 concludes `dom(C)` — the ASN correctly reads ASN-0058's C1 as content-subspace-conditional rather than over-claiming.
- **Run fragmentation (X8).** The within-reference two-step argument (V-contiguity from well-formedness + S8-depth, then maximality ⇒ non-I-adjacency) is genuinely two-step and avoids the maximality/pair conflation. Canonical `≤ k` with equality-iff-no-I-adjacent-boundary is correct; no merge cascade is possible since within-reference runs are non-I-adjacent.
- **Coupling discharge (X14).** The New/Old split is correct. J1'★ case (b) properly routes `Old` addresses through S3★+L14 (content address ⇒ referenced at an `s_C` position) and P4★ at the pre-state, so `R'∖R = {(a,d):a∈New}`. P7/P4★/P4a/P7a and the vacuous link/entity discharges are sound; P6 is correctly separated out as a content-store (not link/entity) obligation.
- **Atomicity & self-transclusion (X10, X15).** Both correctly derive from SequentialTransitionAxiom applied to COPY-as-elementary, pinning `resolve_Σ` to the pre-state; the elementary-vs-composite distinction is the right justification for the strong "no intermediate state" form.

## OUT_OF_SCOPE

The four Open Questions (re-displacement of copied content, transitive containment records, time-varying views, identity under unreachable allocator) are correctly deferred — they touch DELETE-class mechanics, version derivation, and reachability, all outside this ASN. The implementation evidence (Gregory's POOM coalescing, spanfilade entries) is explicitly fenced as "a property of which concrete index one inspects, not a guarantee the abstract specification imposes," so no implementation-mechanics drift.

VERDICT: CONVERGED
