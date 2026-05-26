# Review of ASN-0076

## REVISE

### Issue 1: E5 proof is compressed and elides precondition verification
**ASN-0076, E5 (DivergentSuccessors) proof**: "For the inductive step, given `Σ_{k-1}` with `k-1` such supersessions, apply EDITLINK to produce a fresh successor `ℓ_new,k` (distinct from all prior successors by L11a) and a fresh supersession link `ℓ_sup,k` (likewise distinct)."
**Problem**: The inductive step says "apply EDITLINK" without verifying its preconditions remain satisfied at `Σ_{k-1}`. Specifically: (a) `ℓ_old ∈ dom(Σ_{k-1}.L)` continues to hold via L12 applied k−1 times — but this is left implicit; (b) a fresh document `d_new,k ∈ E_doc` must be available at each step — the proof doesn't say where these come from (any single `d_new` works repeatedly, but this should be noted); (c) the EDITLINK composite at step k must itself be a valid ValidComposite★ — the proof doesn't cite E0 to discharge this. The distinctness claim relies on "fresh ... by L11a" and "likewise distinct", but pairwise distinctness across all 2k entities requires that all 2k K.λ events be distinct events (by SequentialTransitionAxiom) before L11a applies.
**Required**: Expand the inductive step to: (1) cite L12 explicitly for `ℓ_old` persistence; (2) note that `d_new,k` is chosen from `E_doc` (which is non-empty by P1 once any document exists); (3) cite E0 to confirm the composite is valid at `Σ_{k-1}`; (4) state explicitly that all 2k K.λ events are pairwise distinct by SequentialTransitionAxiom, so L11a delivers pairwise distinctness of all 2k addresses.

### Issue 2: E5 postcondition structure not verified case-by-case
**ASN-0076, E5 proof**: "the resulting state `Σ_k` has the required structure"
**Problem**: The "required structure" (k distinct supersession links each with `ℓ_old` in from-endset, k distinct successors in respective to-endsets) has multiple conjuncts that need verification: prior supersession links must retain their endset values (L12 applied to L-store), prior successor links must persist (L12), the new supersession must have `ℓ_old` in its from-endset (E4 applied to the k-th composite), and the new successor must be distinct from prior successors (L11a). The proof skips this enumeration.
**Required**: Spell out which prior claims (L12, E4, L11a) discharge each conjunct of the required structure.

## OUT_OF_SCOPE

### Topic 1: Chains, cycles, and DAG structure of supersessions
**Why out of scope**: The ASN's Open Questions explicitly defer "what invariants must the supersession relation preserve when chains of supersessions form, and under what conditions can such chains contain cycles?" This is new territory requiring its own ASN — not a gap in EDITLINK's specification.

### Topic 2: Type-endset conventions and τ_sup registry
**Why out of scope**: The ASN explicitly notes that "any registry convention that pins `τ_sup` to a particular tumbler — are deferred to a future ASN on type-endset conventions." The link model alone cannot identify a link as a supersession without external convention; this is honest scope-setting.

### Topic 3: Retraction, counter-claims, and resolution policy
**Why out of scope**: The Open Questions explicitly list "what does it mean abstractly for a supersession claim to be *retracted* or *contradicted*" and "under what guarantees can a reader compute the set of 'current' successors" as future work. EDITLINK establishes the structural witnesses; resolution policy is a separate specification.

### Topic 4: Discovery operation specifications
**Why out of scope**: E7 establishes that the structural witness for discoverability is present in `dom(L)`, defining `covers` as the abstract predicate. The Open Questions defer the actual discovery operation specification (including arrangement-vs-store indexing trade-offs) to future ASNs.

### Topic 5: Many-to-many supersessions and content/link interaction
**Why out of scope**: The Open Questions explicitly list both "may a supersession link relate more than two links" and "the relationship between editing a link and editing the content the link references" as future work.

VERDICT: REVISE
