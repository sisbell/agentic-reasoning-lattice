# Review of ASN-0102

This note is substantively strong — the displacement tiling (X16), the within/across-reference merge analysis (X8), the snapshot-resolution treatment of self-transclusion (X10b/X15), and the worked examples are rigorous and the boundary cases (empty copy, empty subspace, append, coalescing) are genuinely exercised. My findings are confined to the prose-accretion patterns the `review-mode.anti-bloat` classifier flags, plus one over-reaching proof step.

## REVISE

### Issue 1: J1'★ discharge reasons about other transitions' range behavior — surplus to COPY's obligation
**ASN-0102, X14 (coupling discharge, J1'★ paragraph)**: "A stranded pair `(a, d) ∈ R_clo ∖ R_B` with `a ∉ ran_{s_C}(Σ_clo.M(d))` can arise only from a later K.μ⁻ removing `a` from range — the sole content-subspace range-shrinking transition (P0, M1, K.μ⁺'s monotone extension, K.μ~'s range-invariance J3, and COPY's own X7-displacement all preserve or extend the range) — which makes the composite invalid at that contraction step."
**Problem**: This sentence enumerates the entire transition vocabulary to argue range-shrink exhaustiveness — reasoning that ValidComposite★ and the *other* steps own, not COPY. The very next sentence ("COPY records `(a, d)` only with `a` resident at `Σ'`, so its own step never grounds a J1'★ violation") is the whole of what COPY needs to discharge its own contribution under the "each step discharges its own" framing. The enumeration is accretion that drifts into a composite-wide property argument.
**Required**: Delete the stranded-pair exhaustiveness sentence; retain only the own-step residency conclusion.

### Issue 2: PC3 carries proof-routing and rationale prose in a precondition slot
**ASN-0102, PC3**: "a definitional choice, consistent with placing content, since `dom(Σ'.C) ∩ dom(Σ'.L) = ∅` (store disjointness, ASN-0093 SD) means a content image cannot route to an `s_L` slot. The S3★ obligation over the inserted mappings is discharged once in the `wp` computation below."
**Problem**: Two non-precondition fragments sit in a precondition. The first explains *why* `S = s_C` is chosen (rationale for a definitional choice) rather than stating the precondition; the second is a forward deferral to the wp computation that advances nothing about PC3. The precondition is simply `S = s_C`.
**Required**: Reduce PC3 to the precondition. The store-disjointness rationale and the wp-deferral note do not belong in the precondition statement.

### Issue 3: X2 closes with use-site commentary, not its claim
**ASN-0102, X2**: "The cost of copying fragmented content is borne entirely in the arrangement (in the number of blocks, X8), never in the content store."
**Problem**: X2's claim is NoFreshAllocation (the next allocation frontier is unchanged). This trailing sentence is essay commentary pointing forward to X8's fragmentation count; it does not advance or establish X2. Same shape recurs as bare `(Gregory Q…)` use-site pointers scattered through X1/X5/X9/X12/X14 that tag rather than demonstrate.
**Required**: Drop the trailing cost-commentary sentence; the X8 cross-reference is not needed to state NoFreshAllocation.

## OUT_OF_SCOPE

### Topic 1: The four Open Questions (displacement-after-copy discoverability, transitive containment, time-varying views, identity under unreachable allocator)
**Why out of scope**: These are correctly placed in an Open Questions slot and name genuinely future territory (later operations, cross-server reachability), not gaps in COPY's own contract. No action required.

VERDICT: REVISE
