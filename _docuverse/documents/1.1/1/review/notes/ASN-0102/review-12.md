# Review of ASN-0102

## REVISE

None. I worked through each claim and could not find a hand-wave, missing case, or unestablished postcondition that requires fixing in this ASN. Specifically:

- **X7 (NonDestructivePlacement)** — the no-overwrite conclusion rests correctly on the disjointness of the copied range (last-components `[p, p+W)`) and the displaced image (`[p+W, n_S+W]`), not on how much of `[v, v+W)` was populated pre-state. The freed-vs-occupied distinction is now stated precisely, and the partition of pre-existing bindings (unmoved / displaced, with the displaced set empty when `p = n_S+1`) is exhaustive.
- **X8 (RunFragmentation)** — the within-reference non-coalescence is given as a genuine two-step argument (V-contiguity ⇒ V-adjacency of maximal runs; maximality ⇒ non-I-adjacency), not an appeal to maximality alone. The constructed count `k` vs. canonical `≤ k` distinction is kept clean, and equality is correctly conditioned on no inter-reference boundary being I-adjacent.
- **X16 (PostStateDensity)** — the tiling `[1,p) ∪ [p,p+W) ∪ [p+W, n_S+W] = [1, n_S+W]` is checked for disjointness and gap-freeness, with the `p=1`, `p=n_S+1`, and empty-subspace (`n_S=0`) boundaries handled. S8a is re-established independently for the interior copied and displaced positions, not just the anchor `v`, so S2 is fully discharged.
- **wp(COPY, S3★)** — the post-state mappings are partitioned into unmoved/displaced/copied; the two preserved classes are discharged by X1 and the link-frame, and the obligation reduces to a non-trivial biconditional on the copied region, discharged at the pre-state by C1 with P1's content-subspace conjunct identified as load-bearing.
- **X14** — J0 is vacuous, J1★/J1'★ are split correctly via `New`/`Old` with the `Old` case resolved through P4★, and P6/P7/P4★/P4a/P7a plus the link/entity Class (a) invariants are accounted for.
- Edge cases the template flags (empty target subspace, append-at-end, self-transclusion via pre-state resolution + atomicity, cross-origin fragmentation, small vs. large `W`) are all addressed, and a concrete worked example verifies X1/X3/X7/X8/X9/X11/X12/X16.

Cross-ASN citations are confined to foundation ASNs (0034, 0036, 0047, 0058, 0093); no non-foundation ASN is referenced by number.

## OUT_OF_SCOPE

### Topic 1: Continued discoverability of copied content under later displacement
**Why out of scope**: The first Open Question (origin/discoverability after a subsequent displacement) cross-cuts REARRANGE/DELETE mechanics and link-projection survivability, which are explicitly out of scope.

### Topic 2: Transitive containment when a referencing document becomes a source
**Why out of scope**: This concerns provenance propagation across a chain of COPYs into distinct documents — a new theorem about the provenance graph, not a guarantee of the single COPY operation specified here.

### Topic 3: Time-varying / version-relative views of the same reference
**Why out of scope**: Differing views across time is version-creation territory, explicitly excluded.

The ASN stays at the state/operation/invariant level throughout; its appeals to Gregory's trace are positioned as confirming evidence, and X8 explicitly disclaims any abstract commitment to block count, so the specification has not drifted into implementation mechanics.

VERDICT: CONVERGED
