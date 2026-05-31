# Review of ASN-0093

## REVISE

### Issue 1: ChainUniformLength is introduced but never used
**ASN-0093, "Per-chain disciplines" + Properties Introduced table**: "**ChainUniformLength.** For each `d ∈ dom(M)`, all elements of `A_C(d)` (resp. `A_L(d)`) have length `#d + 3`."
**Problem**: This discipline gets a dedicated bullet *and* a Properties-table row, but no proof, lemma, or matrix entry ever cites it. The worked example computes lengths directly rather than through it. An introduced-but-unused property is exactly the accretion the anti-bloat classifier asks to surface.
**Required**: Either cite ChainUniformLength where it is load-bearing, or remove the bullet and the table row.

### Issue 2: Applicability enumeration lists results that are not load-bearing
**ASN-0093, "Sub-allocator chains are ASN-0040 sibling streams"**: "Consequently every ASN-0040 result whose precondition is B6(p, d) — B6(a)'s stream-T4-validity conclusion, the SiblingStream postconditions, S0 (StreamOrdering), S1 (StreamPrefix), B5a (SiblingZerosPreservation), B7 (NamespaceDisjointness), B1 (ContiguousPrefix), and B9 (UnboundedExtent) — applies to A_C(d) and A_L(d) directly."
**Problem**: This is a use-site inventory. B9 (UnboundedExtent) is never used anywhere in the note; B1 (ContiguousPrefix) appears only as a comparison ("The contiguity matches ASN-0040's B1") rather than as a discharge. Enumerating "every result that could apply" rather than the ones the argument actually consumes degrades the argument. The adjacent "Permanence of activation — once `d ∈ dom(M)`, the chain stays active... follows from M1" in *Active sub-allocator chains* is similarly an unused claim (no proof relies on activation-permanence; monotonicity proofs cite M1 directly).
**Required**: Cite only the ASN-0040 results actually used (B6(a), the relevant SiblingStream postconditions, S0, S1, B5a, B7); drop B1/B9 from the enumeration and drop the permanence sentence unless a downstream proof depends on it.

### Issue 3: L14 body derivation omits T7's preconditions
**ASN-0093, "Link store invariants," L14**: "Derived from L0 + SC-NEQ + T7 (SubspaceDisjointness, ASN-0034): every content address has `E(·)₁ = s_C`, every link address has `E(·)₁ = s_L`, and `s_C ≠ s_L`, so the domains are disjoint."
**Problem**: T7's preconditions are `zeros(a) = zeros(b) = 3` *and* T4-valid field structure. The body's one-line derivation invokes T7 without establishing either premise. The Properties-table row for L14 correctly lists "L0 + SC-NEQ + StoreT4Validity + T7," and the discharge matrix spells out "T4-validity from StoreT4Validity." The body and the table therefore disagree on the premise set, and as written the body cannot apply T7.
**Required**: Make the body derivation cite the zeros-3 source (C1/L1) and T4-validity (StoreT4Validity), matching the table.

### Issue 4: Cross-document disjointness lemma states its corollary twice
**ASN-0093, "Cross-document disjointness chain"**: lemma statement — "The chain-level corollary ... is ASN-0040's B7 (NamespaceDisjointness) directly, cited once here; the T10 any-extension claim above is the strictly stronger form." Proof — "Chain-level disjointness of `A_·(d_i) = S(p_i, 1)` is ASN-0040's B7 (NamespaceDisjointness), not re-derived here."
**Problem**: The "B7 gives chain-level disjointness, not re-derived; T10 gives the strictly stronger any-extension form" content appears in both the lemma statement and the proof body in nearly identical words. Two paragraphs saying the same thing.
**Required**: State the B7-corollary-vs-T10-stronger-form relationship once.

## OUT_OF_SCOPE

### Topic 1: Concurrent emission across allocators
**Why out of scope**: The substrate commits to atomic, totally-ordered transitions (SequentialTransitionAxiom). The concurrency discipline is correctly listed under Open Questions and belongs to a higher-layer ASN.

### Topic 2: Third subspace (`s ≥ 3`) sub-allocators
**Why out of scope**: SubspaceConventionAxiom pins exactly two subspaces. Stratification beyond `A_C(d)`/`A_L(d)` is new territory, correctly deferred.

VERDICT: REVISE
