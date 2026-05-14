# Review of ASN-0043

## REVISE

### Issue 1: L11b proof uses example-specific "-6" arithmetic in a general derivation
**ASN-0043, L11b — NonInjectivity proof, "Conformance of Σ'" verification of L1b**: "L1b because TA5(c)/T10a.1 (UniformSiblingLength, ASN-0034) gives `#a' = #a`, so `#E(a) ≥ 2` (L1b on Σ) yields `#E(a') = #a' − 6 = #a − 6 = #E(a) ≥ 2`"
**Problem**: The constant "-6" is the offset for the worked example's document tumbler `1.0.1.0.1` (length 5, +1 separator = 6). For a document whose owner identifiers occupy more than one component each (e.g., `N = [1, 2]`, giving a document tumbler of length 6), `#E(a) = #a − (#h(a) + 1) ≠ #a − 6`. The L11b proof is general, so the algebraic step does not justify the conclusion in general.
**Required**: Replace the numeric arithmetic with a structural argument: since `a'` is a sibling of `a` produced by `inc(·, 0)`, positions 1..#a−1 are preserved (citing TA5(b) for k=0 + TA5-SigValid + T10a.4), hence `h(a') = h(a)` and `#h(a') = #h(a)`; combined with `#a' = #a` (T10a.1), this yields `#E(a') = #a' − (#h(a') + 1) = #a − (#h(a) + 1) = #E(a) ≥ 2`.

### Issue 2: Chain-prefix-preservation argument cites lemmas that give length-only preservation for inc(·, 0)
**ASN-0043, Home and Ownership section**: "Each subsequent step operates at length > #d, so inc(·, 0) sibling advances preserve positions 1..#t − 1 ⊇ 1..#d (TA5(c)/T10a.1, UniformSiblingLength)"
**Problem**: TA5(c) supplies `#t' = #t` and `t'_{sig(t)} = t_{sig(t)} + 1` (length preservation and the single modified position). T10a.1 supplies `#a = #b` for all siblings (length uniformity). Neither lemma directly establishes that positions 1..#t−1 are preserved. The position-preservation conclusion requires TA5(b) for k=0 — `(A i : 1 ≤ i ≤ #t ∧ i ≠ sig(t) : t'ᵢ = tᵢ)` — combined with TA5-SigValid (sig(t) = #t for T4-valid t) and T10a.4 (every chain step is T4-valid). The conclusion is correct but the citation chain is incomplete.
**Required**: Replace "TA5(c)/T10a.1, UniformSiblingLength" with "TA5(b) for k=0 + TA5-SigValid + T10a.4" (or list the three lemmas inline). The same fix applies to the parallel citation in the L11b verification of L1b (Issue 1).

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage's structural home
**Why out of scope**: The lemma is introduced inline in this ASN but is a fact about tumbler algebra/span coverage, not about links. Its formal residency belongs in a tumbler-algebra ASN (per the project's span-algebra-gap memory). Acceptable to use here while that ASN is pending.

### Topic 2: Self-referential and cyclic link structures
**Why out of scope**: The invariants permit a link to reference its own address (L4 + L13) and permit cycles among links (no acyclicity invariant). The semantics of such configurations belong with compound link structure analysis, listed in the Open Questions.

### Topic 3: The empty-docuverse case for L9
**Why out of scope**: L9 is restricted to states with `dom(Σ.M) ≠ ∅`. The empty case (`dom(Σ.M) = ∅`) requires constructing a fresh document, which depends on carrier-root properties of the allocator tree 𝒯 not constrained by current L- or S-invariants. The ASN explicitly addresses and justifies this restriction.

VERDICT: REVISE
