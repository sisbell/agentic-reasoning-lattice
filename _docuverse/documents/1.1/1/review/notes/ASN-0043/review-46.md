# Review of ASN-0043

## REVISE

### Issue 1: T4-validity citation chain is unsound

**ASN-0043, "Home and Ownership"**: "T4 (HierarchicalParsing, ASN-0034) constrains all tumblers used as addresses to satisfy its format requirements (no adjacent zeros, no leading/trailing zeros, positive non-separator components). Link addresses are tumblers used as addresses — they are keys in `Σ.L` — so T4 applies to them directly."

Also at the L11b proof: "L1/L1a/L1b by allocation (element field depth ≥ 2 by construction)" — assumes T4-validity holds without citation.

**Problem**: T4 is a predicate defining T4-validity, not a mechanism that constrains tumblers. The ASN appeals to T4 as if it were an automatic constraint. The actual derivation chain is: L1c (LinkAllocatorConformance) → T10a → T10a.4 (T4PreservationUnderDiscipline) → T4-validity. This chain is critical because `fields(a)`, `home(a)`, and every projection used in L0–L14 depends on T4-validity.

**Required**: State explicitly that T4-validity of link addresses derives from L1c + T10a.4. Cite T10a.4 in the body where T4-validity is needed (Home and Ownership section, L0's T7 application, L9's construction of ghost g, the verification chains in L9 and L11b proofs).

### Issue 2: L0's T7 application omits the T4-validity precondition

**ASN-0043, L0**: "These satisfy T7's precondition (a, b ∈ T with zeros(a) = zeros(b) = 3), yielding the fundamental disjointness."

**Problem**: T7's precondition is `a, b ∈ T` satisfy *the T4 constraints* AND zeros(a) = zeros(b) = 3. The ASN cites only the zero-count clause. Without T4-validity, T7 does not fire.

**Required**: Add the T4-validity discharge: for `a ∈ dom(Σ.L)`, T4-validity follows from L1c + T10a.4; for `b ∈ dom(Σ.C)`, T4-validity is inherited from ASN-0036's framework (where S7d + T10a + T10a.4 establish the analogous property for content addresses). Then T7's full precondition is satisfied.

### Issue 3: L9 proof does not establish T4-validity of ghost g

**ASN-0043, L9 proof**: "Let g be any element-level tumbler with `fields(g).E₁ = s_X`."

**Problem**: The use of `fields(g)` presupposes g is T4-valid (since T4b's projections are partial functions requiring T4-validity). The proof asserts existence of g but does not construct a T4-valid witness. T0(a) gives same-depth tumblers with arbitrary component values — but T0(a) alone does not preserve T4-validity (it could place a zero where T4 forbids one).

**Required**: Construct g explicitly as a T4-valid tumbler. For example: start from a T4-valid element-level tumbler (existence: any address in `dom(Σ.C)` is T4-valid by ASN-0036's framework, or construct directly from the carrier axioms), then modify its element-field first component to s_X using T0(a). Since the modification changes a positive value to another positive value (s_X ≥ 1, since it differs from s_C ≥ 1 and s_L ≥ 1 — establish this too), no zero is introduced and T4-validity is preserved.

### Issue 4: L6 SlotDistinction is stated only for the standard triple

**ASN-0043, L6**: "A link is a sequence — permuting endset slots produces a different link value when the permuted entries differ. For the standard triple: `(A F, G, Θ :: F ≠ G ⟹ (F, G, Θ) ≠ (G, F, Θ))`."

**Problem**: L3 admits arity N ≥ 2, but L6's formal statement covers only arity 3. For arity 2 or arity ≥ 4, the slot-distinction property is not formally captured. A 4-endset link `(A, B, C, D)` should differ from `(B, A, C, D)` when A ≠ B, but L6 as stated does not assert this.

**Required**: State the invariant generally — for any link of arity N ≥ 2, permuting slot indices yields a different value when the permuted entries differ. The standard-triple instance can remain as a worked-out specialization.

### Issue 5: L8 .type notation is undefined for arity-2 links

**ASN-0043, L8**: "For links following the standard triple convention (`|Σ.L(a)| ≥ 3`), type matching is by *address identity*..."

**Problem**: L3 admits arity 2 links. For such links, `.type` (slot 3) does not exist, so `Σ.L(a).type` is undefined, and `same_type` is not a total predicate on `dom(Σ.L)`. The ASN does not resolve whether arity-2 links should be admitted (untyped connections) or excluded (require N ≥ 3 for typed connection).

**Required**: Either (a) tighten L3 to require N ≥ 3 (if untyped connections are not intended), (b) state that `same_type` is partial, defined only on the arity-≥-3 subset of `dom(Σ.L)`, or (c) define a default type semantics for arity-2 links.

### Issue 6: L9 proof assumes a document prefix d' exists without justification

**ASN-0043, L9 proof**: "Pick any document prefix d'."

**Problem**: The proof must extend an arbitrary conforming Σ, which may have no documents at all (`dom(Σ.L) = ∅`, `dom(Σ.C) = ∅`, `dom(Σ.M) = ∅`). In such a state, no existing document prefix is at hand. The proof needs to either construct a valid document-level tumbler from carrier axioms (T0(b) gives length-≥-5 tumblers; T4-validity needs to be established for the constructed witness), or restrict L9's antecedent to states where at least one document prefix is in use.

**Required**: Explicitly construct d' as a T4-valid document-level tumbler (zeros = 2, no adjacent zeros, positive endpoints). The construction parallels Issue 3 — establish that such a tumbler exists in T independent of state contents.

### Issue 7: L1b justification conflates depth-1 and shift-action-point arguments

**ASN-0043, L1b**: "Sibling allocation via `inc(·, 0)` would advance the only component, producing `[s_L + 1]` — an address in subspace `s_L + 1`, not `s_L`. This is the same degeneracy identified in ValidInsertionPosition (ASN-0036): at depth 1, `shift([s_L], 1) = [s_L + 1]` crosses subspace boundaries because the ordinal displacement `δ(1, 1)` has action point 1..."

**Problem**: The two arguments are conflated. The `inc(·, 0)` advancement applies to the rightmost nonzero (the element field's last component at the full address depth, not within the element field projection). For a link address with element field [s_L] at full address `N.0.U.0.D.0.s_L`, `inc(·, 0)` advances position #t (i.e., position of s_L) to s_L + 1 — yielding `N.0.U.0.D.0.(s_L+1)`, where the element field becomes [s_L + 1]. This is the actual degeneracy. The shift-based argument is a separate concern about how shift behaves on V-positions and is not directly applicable to I-address allocation discipline.

**Required**: Clean separation of the two arguments. The L1b justification should rest on TA5's sibling allocation behavior on element-level addresses, not on shift mechanics from ASN-0036.

### Issue 8: L11b verification cites L11a circularly

**ASN-0043, L11b proof**: "L11a uniqueness for `a'` by GlobalUniqueness (UniqueAddressAllocation, ASN-0034) via L11a."

**Problem**: L11a is one of the invariants being verified for Σ'. Citing L11a "via L11a" is circular phrasing. The verification for the newly-allocated a' should cite GlobalUniqueness directly (since L1c + T10a conformance + freshness of allocation event yields uniqueness via GlobalUniqueness), without naming L11a as the justification.

**Required**: Rewrite the citation to flow: "L11a uniqueness for `a'` by GlobalUniqueness (UniqueAddressAllocation, ASN-0034), applicable since `a'` arises from a fresh allocation event under L1c-conforming allocator."

## OUT_OF_SCOPE

### Topic 1: Formal allocator state in Σ

The proofs of L9 and L11b assume allocators have state that can produce fresh addresses, but the state tuple `Σ = (Σ.C, Σ.M, Σ.L)` does not include allocator state explicitly. Formalizing this belongs to operations work — a future ASN defining MAKELINK and related operations will need to model allocator state evolution.

### Topic 2: Specific subspace identifier values

The ASN treats s_C and s_L as abstract identifiers with s_C ≠ s_L. Whether they take specific values (e.g., 1 and 2 per implementation convention) is convention, not invariant. Specifying values belongs to a profile or implementation ASN.

VERDICT: REVISE
