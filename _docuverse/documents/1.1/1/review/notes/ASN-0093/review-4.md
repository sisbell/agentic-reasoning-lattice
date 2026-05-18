# Review of ASN-0093

## REVISE

### Issue 1: T10a chain-lemma applicability remark mis-attributes T4-validity dependency to T10a.1 and T10a.7

**ASN-0093, "Remark — T10a chain-lemma applicability to non-tree-embedded chains"**: "Inspection of the proofs of T10a.1, T10a.7, and T10a.8 in ASN-0034 confirms that they depend only on per-step structure of an inc(·, 0) chain together with chain-wide T4-validity preservation (so TA5-SigValid pins `sig(t_n) = #t_n` at every chain element) and the foundation-level claims T1 (LexicographicOrder), TA5(a), and NAT-* axioms."

**Problem**: Per ASN-0034's dependency lists, T10a.1 depends only on T10a + TA5(c) (length preservation), with no T4-validity requirement. T10a.7 depends on T10a + TA5(a) + T1(c) + T1(a) + NAT-* axioms, again with no T4-validity requirement. Only T10a.8 transitively requires T4-validity (through its T10a.4 citation). The remark conflates T10a.8's specific T4-related needs with T10a.1 and T10a.7, which do not require T4-validity.

**Required**: Either correct the remark to specify which lemmas need T4-validity (only T10a.8) and which don't (T10a.1, T10a.7), or — if there's a hidden dependency this review missed — exhibit where T10a.1 or T10a.7 invokes TA5-SigValid or any T4-dependent foundation.

### Issue 2: K.α and K.λ subsequent-emit freshness derivations skip the max-comparison step

**ASN-0093, K.α (ContentAllocation) precondition / K.λ (LinkAllocation) precondition**: "Freshness against dom(C) is discharged by T10a.7 (EnumerationInjectivity) applied to A_C(d)'s chain (per SubAllocatorAxiom.ChainDiscipline); cross-document collisions within dom(C) are ruled out by the Cross-document disjointness lemma."

**Problem**: T10a.7 alone gives "distinct chain indices produce distinct addresses" (strict monotonicity along the chain). The full freshness derivation requires combining T10a.7's strict monotonicity with the max-property of `a_prev`: (i) `a_prev = max{a' ∈ dom(C) : origin(a') = d}` is at some chain index `n`; (ii) by ChainMembershipForOrigin, every element of `dom(C)_d` is in `A_C(d)`, hence at some chain index; (iii) by T10a.7's strict monotonicity composed with `max`, every element of `dom(C)_d` is at a chain index `≤ n`; (iv) `a = inc(a_prev, 0)` is at chain index `n + 1 > n`, hence distinct from every element of `dom(C)_d`. Steps (i)–(iv) are not "discharged by T10a.7" in one step — the max-comparison is what bridges the strict monotonicity to the freshness conclusion.

**Required**: Spell out the max-comparison step in the discharge. The current "discharged by T10a.7" is exactly the "X follows from Y + Z" pattern the review standards flag as a claim rather than a proof.

### Issue 3: ChainMembershipForOrigin lemma's "partition" wording oversells the proved subset claim

**ASN-0093, ChainMembershipForOrigin lemma statement**: "At every reachable state `Σ`, the entries of `dom(C)` and `dom(L)` partition by origin into the sub-allocator chains: `(A d ∈ dom(M) :: dom(C) ∩ {a' ∈ T : origin(a') = d} ⊆ A_C(d))` ..."

**Problem**: The formal statement is two subset inclusions, not a partition. A partition would additionally establish (a) covering — every `a ∈ dom(C)` is in some `A_C(origin(a))` — and (b) disjointness of `A_C(d) ∩ A_C(d') = ∅` for `d ≠ d'`. Both follow from substrate machinery (covering from C2; disjointness from Cross-document disjointness at the first-emission anchors), but neither is established by the proof body, which only inducts the subset claim.

**Required**: Either restate the conclusion as "subset inclusion of dom(C)-by-origin into A_C-chains" (with partition listed as a corollary derivable from C2 + Cross-document disjointness), or extend the proof body to establish the two missing partition components.

### Issue 4: L1c invariant statement uses `a` for the link address, breaking convention with K.λ

**ASN-0093, L1c (LinkAllocatorConformance)**: "Every link address `a ∈ dom(L)` has a *structural inc-chain* from its home document to `a`: a finite sequence `(t₀, t₁, …, tₙ)` with `t₀ = origin(a)` and `tₙ = a` ..."

**Problem**: The L1c invariant uses `a` for the link address, but K.λ uses `ℓ` and the L1c chain exhibition in the discharge section also uses `ℓ`. This appears to be a copy-paste from C1c. Variable-naming inconsistency between an invariant statement and its discharge is a clarity concern: a reader cross-referencing the L1c invariant statement against the chain exhibition has to mentally rename.

**Required**: Use `ℓ` consistently in L1c's statement to match K.λ and the chain exhibition.

### Issue 5: T7 alias "SubspaceDisjointness" diverges from ASN-0034's canonical name

**ASN-0093, Cross-document disjointness chain closure / Properties Introduced table**: "T7 (SubspaceDisjointness, ASN-0034)"

**Problem**: ASN-0034 names T7 "FirstElementFieldDistinction." Renaming it to "SubspaceDisjointness" without a notational note creates a minor citation hazard for anyone tracing the lemma to its source. The semantic content is consistent (different `E(·)₁` ⟹ distinct tumblers), but the label diverges.

**Required**: Use ASN-0034's canonical name "FirstElementFieldDistinction" (or "T7 (FirstElementFieldDistinction)") or add an inline note that "SubspaceDisjointness" is this ASN's chosen alias.

### Issue 6: Subsequent emissions implicitly form a contiguous initial segment of the sub-allocator chain, but the substrate never states or proves this

**ASN-0093, K.α emission rule / K.λ emission rule**: "Subsequent emission ... a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0) (TA5(c)), the next sibling on A_C(d)'s inc(·, 0) chain."

**Problem**: ChainMembershipForOrigin proves `dom(C)_d ⊆ A_C(d)`, but not that `dom(C)_d` is a contiguous prefix `{c_1, ..., c_n}` of the chain. The contiguity follows operationally (each K.α emission to `d` extends by exactly one chain step from the prior max), but the substrate never states this as a property and the freshness argument in Issue 2 implicitly relies on it (or at least implicitly relies on the chain index of `a_prev` being the maximum chain index occupied by `dom(C)_d`). A reader cannot reconstruct the freshness argument without this implicit fact.

**Required**: Either state contiguity as an explicit invariant maintained inductively by K.α/K.λ, or note in the freshness derivation that contiguity is unnecessary because the max-property of `a_prev` alone (combined with T10a.7's strict monotonicity) suffices for freshness regardless of whether `dom(C)_d` is contiguous.

## OUT_OF_SCOPE

None — the ASN's deferral of arrangement mutation, entity stratification, provenance, link withdrawal, and higher-arity links to higher-layer ASNs is explicit in Scope and Open Questions.

VERDICT: REVISE
