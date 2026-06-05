# Review of ASN-0103

## REVISE

### Issue 1: ActivatedEmission for the new document `d` is asserted, not discharged

**ASN-0103, Invariants Maintained / Claims (CND.inv)**: "*Concerning `d` directly, established in Effect One*: S7d ... and ActivatedEmission (`d` is an emission of the activated entity-level sub-allocator `A_doc(A)`)."

**Problem**: ActivatedEmission (ASN-0047) requires, for every non-node entity, an *activated* entity-level sub-allocator whose domain contains it. For `d` this allocator is `A_doc(A)`, so the discharge needs `Activated(A_doc(A))`. Nothing in the ASN establishes that `A_doc(A)` is activated. Effect One only establishes `d ∈ S(A,2)`, its zeros/parent/validity/freshness/monotonicity — none of which is the *activation* of `A_doc(A)`. The ActivatedEmission preservation clause itself reads "each non-node entity enters E only via a T10a inc-step *on an activated sub-allocator*" — i.e. it presupposes `A_doc(A)` already activated rather than supplying it. The cited foundation machinery does not close this: applying ActivatedEmission to the operand `A` yields the *account* sub-allocator (`A_account(N)`) containing `A`, not the activation of `A`'s document sub-allocator. So the parenthetical "established in Effect One" is inaccurate for this conjunct.

**Required**: Either (a) state explicitly that `A ∈ E ∧ Account(A)` carries, as a guarantee owed by (out-of-scope) account provisioning, the activation of `A_doc(A)` — and add it as a precondition or stated assumption — or (b) cite/establish a foundation lemma that the entity-allocation event placing an account into E activates its document sub-allocator (the account-level analogue of SubAllocatorBundle). As written, the ActivatedEmission discharge has a hole.

### Issue 2: GlobalUniqueness invoked with an undischarged T10a-conformance premise, where B7 already suffices

**ASN-0103, Effect One (Freshness)**: "Cross-account collisions are excluded ... GlobalUniqueness (ASN-0034) — with B8 (ASN-0040) — guarantees that every baptismal event yields an address distinct from every other, regardless of which account it sits beneath."

**Problem**: GlobalUniqueness's precondition is "a, b ∈ T produced by distinct allocation events *within a system conforming to T10a*." The ASN never establishes that the entity-set allocations governed by K.δ form a T10a-conforming allocator tree, so the premise is undischarged. Moreover the conclusion is already available without it: for distinct accounts `A ≠ A'`, the namespaces `(A,2)` and `(A',2)` differ, so `S(A,2) ∩ S(A',2) = ∅` directly by B7 (NamespaceDisjointness, ASN-0040) — exactly the unconditional cross-namespace half of B8 the ASN is otherwise leaning on. The GlobalUniqueness appeal is both unverified and redundant.

**Required**: Discharge cross-account distinctness via B7 (`(A,2) ≠ (A',2)`, both B6-valid) directly, or explicitly establish T10a-conformance of the entity allocator before invoking GlobalUniqueness. The same applies to the GlobalUniqueness citation reused in CND.inv for "address permanence/distinctness."

### Issue 3: Ownership precondition mis-cited to O5

**ASN-0103, CND.pre**: "the invoking principal `π` owns the account (`pfx(π) ≼ A`, O5; ASN-0042)."

**Problem**: The ownership predicate `owns(π,A) ≡ pfx(π) ≼ A` is O1 (PrefixDetermination), not O5. O5 (SubdivisionAuthority) is the *allocation-authority* axiom (about `allocated_by`), which is the relevant citation for "π may allocate `d` under `A`," not for the ownership precondition itself. The two are conflated. (Note also that O5 is stated over ASN-0042's registry-bearing state `Σ.B`; the same caution the ASN exercises for the deferred `ω`-claim applies to leaning on O5 here.)

**Required**: Cite O1 for the ownership precondition and reserve O5 for the authorization step, or justify the O5 citation over this state model as the structural derivation in CND.own already does (transitivity `pfx(π) ≼ A ≼ d`), which needs only O1.

## OUT_OF_SCOPE

### Topic 1: Effective-owner equality `ω_{Σ'}(d) = ω_Σ(A)` and the E↔B coupling invariant
**Why out of scope**: The ASN correctly identifies that `ω` is defined over ASN-0042's registry `B`, absent from ASN-0047's state, and defers the registry-coupling invariant `{e ∈ E : Document(e) ∧ parent(e)=A ∧ #e=#A+2} = Σ.B ∩ S(A,2)` to a registry-carrying ASN. This deferral is sound and explicitly flagged as an open question — new territory, not an error here.

VERDICT: REVISE
