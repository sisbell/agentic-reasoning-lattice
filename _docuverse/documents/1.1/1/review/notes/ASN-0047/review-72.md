# Review of ASN-0047

## REVISE

### Issue 1: Cross-document disjointness chain Case B sub-case enumeration is incomplete

**ASN-0047, "Allocator hierarchy under documents" section, Cross-document disjointness chain (Lemma) proof, Case B**: The proof enumerates three sub-cases for Case B (prefix-incomparable documents): (i) same-allocator siblings (any T10a allocator), (ii) cross-account documents (from "document sub-allocators rooted under different parent accounts"), (iii) mixed version/sibling configurations within a common ancestor. The closure asserts: "any pair of distinct documents with `d₁ ⋠ d₂ ∧ d₂ ⋠ d₁` falls into at least one of them by S7d's guarantee."

**Problem**: Consider `d_a.1` vs `d_b.1` where `d_a` and `d_b` are top-level documents under different accounts. These versions are emitted by *version* sub-allocators `A_v(d_a)` and `A_v(d_b)`, not by document sub-allocators. They fit none of the listed sub-cases literally: not (i) (different allocators), not (ii) (sub-case (ii) is restricted to outputs of document sub-allocators), not (iii) (no shared ancestor in lineage). The underlying T10a.5 machinery does handle this configuration (the two version sub-allocators are non-lineage relative to each other), but the case enumeration as written does not name this dispatch path.

**Required**: Either expand sub-case (ii) to cover any non-lineage pair of allocators producing document-level outputs (not just document sub-allocators), or add a fourth sub-case explicitly for cross-account version configurations. The closure step (suffix-extension from the Case B premise) is correct as written and does not need to change — only the enumeration of dispatch strategies needs to match the exhaustiveness claim it asserts. Alternatively, weaken the assertion from "falls into at least one of them" to "is dispatched by some combination of T10a.2, T10a.5, T10a.6 acting at the appropriate ancestor level," which more accurately describes what S7d + T10a's full machinery actually delivers.

### Issue 2: ExtendedReachableStateInvariants S5 omission unexplained

**ASN-0047, "Extended reachable-state invariants" section**: The per-state invariant conjunction enumerates S2, S3★, S3★-aux, S4, S7a–d, S8a, S8-fin, S8-depth, S8, D-CTG★, D-MIN★, D-SEQ★, P4★, P4a, P6–P8, NodeLineage, L0, L1, L1a, L1b, L3, L14, L-fin, CL-OWN, CL-UNIQ. ASN-0036 S0 and S1 are explicitly stated as subsumed by P0; S9 is explicitly retained as a per-transition conjunct. But ASN-0036 S5 (UnrestrictedSharing — `(∀N ∈ ℕ :: (∃Σ :: ...))`) is not mentioned in either the per-state or per-transition theorem.

**Problem**: S5 is a foundation property of the strand model; if it is not preserved in the extended state, that should be stated; if it carries through automatically as a derived corollary of the existing invariants, that should be cited. Leaving it silent makes a future reader unsure whether its omission from the conjunction is intentional or accidental.

**Required**: Add one sentence to the ExtendedReachableStateInvariants section noting either (a) "S5 is preserved at every reachable state as a derived consequence of S2 + S3★ + the absence of any injectivity constraint on M(d)," or (b) cite where the analog is established for the extended state.

## OUT_OF_SCOPE

None — the ASN's scope statement is well-bounded, and the issues identified above are within the scope of this ASN's transition model.

VERDICT: REVISE
