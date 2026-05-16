# Review of ASN-0086

## REVISE

### Issue 1: T10a sub-lemma misattribution in R0

**ASN-0086, R0 proof Step 3**: "By T10a.4 (NoReuse, ASN-0034), the allocator never returns an address already in `dom(Σ.L)`... By T10a.5 (FreshnessGuarantee, ASN-0034), the allocator's output for the current call is permitted to be `a`... By T10a.6 (DeterministicExtension, ASN-0034), the allocator's choice extends to a fresh subspace position without conflict."

**Problem**: The foundation lists T10a.4 = T4PreservationUnderDiscipline, T10a.5 = CrossAllocatorIncomparability, T10a.6 = DomainDisjointness. There is no "NoReuse", "FreshnessGuarantee", or "DeterministicExtension" lemma in T10a. None of T10a's stated postconditions includes "the allocator can be made to produce any unallocated address." T10a constrains *how* allocators allocate (sibling/child structure), not *which* choices they make from admissible ones.

**Required**: Reconstruct R0's freshness argument from actual T10a properties — likely needs T10a's at-most-once spawning constraint plus T0(a)/T0(b)/L-fin to show the unallocated valid-address set is non-empty. The "allocator chooses `a`" step needs different justification (or R0 should weaken to assert existence of a valid extension without invoking an allocator's choice mechanism).

### Issue 2: Undefined notation `s_L(d)`

**ASN-0086, R0 Step 1 and Worked Sketch**: "the substrate contains... `d` is a document address whose link subspace `s_L(d)` is well-defined"; "We further assume `a₁` is sited in some document subspace `s_L(d)`"

**Problem**: L0 (ASN-0043) introduces `s_L` as a **constant** subspace identifier (`subspace_I(a) = s_L` for all link addresses). It is not a function of `d`. The ASN uses `s_L(d)` throughout R0 and the worked sketch as if it were a function — apparently confusing the subspace identifier (a natural number) with "the set of link-subspace addresses under document d's prefix" (a set).

**Required**: Either define `s_L(d)` explicitly (e.g., `{a ∈ T : home(a) = d ∧ subspace_I(a) = s_L}`) or rewrite the proof in terms of the link subspace identifier `s_L` together with the document prefix `d`.

### Issue 3: R4 proof — `s_C ≠ s_L` not established

**ASN-0086, R4 proof**: "By T7 (FirstElementFieldDistinction, ASN-0034), `s_C ≠ s_L` are distinct tumbler subspaces, and addresses in distinct subspaces are themselves distinct as tumblers."

**Problem**: T7 says "different first element-field components imply distinct tumblers" — it does not establish `s_C ≠ s_L`. The Setup introduces `s_C` as the (free) subspace identifier for content; L0 introduces `s_L` for links. Their distinctness needs an argument, but the proof asserts it as a T7 consequence. If `s_C = s_L` were admissible, disjointness would have to come from L14 directly (and only in its scoped form).

**Required**: Either cite the convention fixing `s_L ≠ s_C` (e.g., text subspace = 1 from ASN-0036's D-CTG, link subspace = 2), or restructure the proof to derive R4 from L14 + Setup directly without going through subspace distinctness. Also discharge T7's preconditions explicitly (T4-validity and zeros = 3 for both `a` and `a'`).

### Issue 4: L-property misattributions in R5's Stage 2 check

**ASN-0086, R5 Stage 2**: enumerates ASN-0043's invariants as "L2 (ZeroEndsetExclusion)", "L5 (EndsetSpanWellFormedness)", "L6 (OrderingLaws)", "L7 (EndsetEquality)", "L10 (Owner)", "L11 (LinkPermanence)".

**Problem**: The foundation lists L2 = OwnershipEndsetIndependence, L5 = EndsetSetSemantics, L6 = SlotDistinction, L7 = DirectionalFlexibility, L10 = TypeHierarchyByContainment, L11a = LinkUniqueness (no "L11"). Six of the labels in R5's "exhaustive" check don't match the foundation. The enumeration also conflates L11/L11a and silently omits L0a and L14a.

**Required**: Re-enumerate against the actual L-properties. Verify that each is genuinely orthogonal to or compatible with the self-targeting construct — the renaming doesn't necessarily change the conclusion, but it does mean the current check is unreliable.

### Issue 5: R0's invariant verification hand-waved

**ASN-0086, R0 Step 4**: "L1a–L1c hold (`a ∈ s_L(d)` by construction, allocator-conformant by Step 3)"

**Problem**: L1b requires `#E(a) ≥ 2` — not addressed. L1c requires the existence of a complete T10a-conforming chain from a document-level seed to `a` — only "allocator-conformant" is asserted, with no chain exhibited. The pattern is the "by similar reasoning" shortcut for a multi-clause check.

**Required**: Show each L1a/L1b/L1c clause is satisfied by the chosen `a`. For L1c specifically, exhibit (or argue existence of) the chain `t₀, ..., tₙ` with the required `k_i` values.

### Issue 6: Worked Sketch repeats Issue 1's misattributions

**ASN-0086, Worked Sketch Step 1**: "By T10a.5 (FreshnessGuarantee, ASN-0034) the allocator's discipline supplies such a position... T10a.6 extends the allocator's choice deterministically to a sibling position"

**Problem**: Same misattribution as in R0. Also: T10a doesn't guarantee that an allocator-extension can be invoked to produce a *specific* sibling position; T10a constrains which positions are admissible *outputs*, but the choice mechanism is not in T10a.

**Required**: Reformulate the sketch to either cite actual T10a properties or weaken the claim to "exists a valid extension state producing such an address."

### Issue 7: R0's countable-infinity argument is loose

**ASN-0086, R0 Step 2**: "By T0(a) (UnboundedComponentValues), each tumbler component admits unbounded values, so the set of valid link addresses within `s_L(d)` is countably infinite."

**Problem**: T0(a) gives unbounded component values, but countability of *valid* link addresses (subject to L1, L1a, L1b, L1c) requires more — at minimum T0(b) (UnboundedLength) and that the L1b depth constraint admits infinitely many witnesses. The single-sentence inference skips this work.

**Required**: Cite both T0(a) and T0(b), and argue (briefly) that the L1 constraints — in particular `#E(a) ≥ 2` and the subspace-residence requirement — leave infinitely many valid candidates within the link subspace under `d`.

### Issue 8: T7 misapplied in R4

**ASN-0086, R4 proof**: Even granting `s_C ≠ s_L`, the conclusion "addresses in distinct subspaces are themselves distinct as tumblers" follows from T3 (CanonicalRepresentation), not T7. T7's statement requires both arguments T4-valid with zeros = 3 and is the wrong size of hammer for componentwise inequality.

**Required**: Either replace T7 with T3 (componentwise distinctness implies distinct tumblers), or discharge T7's preconditions explicitly (`a` from S7b ⟹ T4-valid + zeros = 3; `a'` from L1 + L1c via T10a.4 ⟹ T4-valid + zeros = 3).

### Issue 9: R5's L11b citation overreaches

**ASN-0086, R5 Stage 1**: "The L11b (NonInjectivity, ASN-0043) witness shows that an emission carrying such a span as an endset component preserves all L-invariants."

**Problem**: L11b establishes that *value duplication* at fresh addresses is invariant-preserving. It does not directly establish that *new endset content with self-targeting spans* is invariant-preserving — that requires a separate construction (one whose existing endset values weren't already in the substrate). The cited witness covers a narrower case than the claim.

**Required**: Either construct the invariant-preserving extension explicitly for the self-targeting case, or weaken the claim to "the construct is admissible by L4(c) + L13, with no opposing invariant" without leaning on L11b as the witness.

### Issue 10: Active subset / Nullify on multi-arity links

**ASN-0086, Worked Sketch and operation definitions**: The development restricts attention to standard-triple links, but `Nullify(Σ, a)` accepts any `a ∈ A_rel^Σ`. A multi-arity link's address is in `A_rel` and can be the target of a retraction tuple, but `A_K^Σ` is only defined for `K` indexing the (arity-3) `L_K`.

**Problem**: Nullifying a multi-arity link puts its address in `nullified(Σ)`, but no `A_K` records that link in the first place, so the operational/audit distinction is undefined for it.

**Required**: Either restrict `Nullify`'s precondition to addresses in some `L_K` (i.e., arity-3 links), or extend `A_K^{(n)}` to cover the multi-arity case. The current definitions leave the semantics ambiguous.

### Issue 11: Observe pattern semantics underspecified

**ASN-0086, Observe definition**: "Observe_K : Σ × ℘_fin(A) × ℘_fin(A) × View → ℘_fin(L_K^Σ)" with matching by `F̂ ⊆ coverage(F) ∧ Ĝ ⊆ coverage(G)`.

**Problem**: The choice of "subset of coverage" as the match relation is arbitrary — equality, intersection, span-set identity are all candidates. The ASN doesn't justify why subset, what queries this enables/excludes, or whether higher layers can extend the pattern language.

**Required**: Either state that subset-on-coverage is the *sole* match relation at the substrate level (with rationale), or admit that Observe is parameterized over a family of pattern predicates and specify the family.

### Issue 12: State transition relation left implicit

**ASN-0086, throughout**: The ASN invokes "state transitions Σ → Σ'" without specifying what counts as a valid transition. R0's "Define Σ' by extending Σ.L with..." assumes any invariant-preserving extension is a valid transition.

**Problem**: ASN-0043 and ASN-0036 also leave the transition relation abstract, but R0 needs to *construct* a transition, not just observe one. Without an explicit transition relation, R0 is asserting the existence of an extension state without specifying what extension primitives are available.

**Required**: State (even as an axiom or convention) that any state satisfying all relevant invariants is reachable from any prior state by some sequence of transitions, or specify the primitive transitions and verify R0's construction is one of them.

## OUT_OF_SCOPE

### Topic 1: Concurrency, atomicity, and Observe ordering
The Open Questions appropriately flag these. The single-writer setting suffices for R0–R7; concurrent semantics belongs in a downstream ASN.

### Topic 2: Multi-arity typed relations `L_K^{(n)}` for n > 3
Standard-triple restriction is explicit. Generalizing to n-ary relations is downstream work.

### Topic 3: Dynamic type-catalog coordination across layers
Listed as Open Question. R0/R5 don't require it.

### Topic 4: Cardinality bounds on `nullified(Σ)`
Listed as Open Question. Not a property the present ASN claims.

VERDICT: REVISE
