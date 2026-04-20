# Review of ASN-0063

## REVISE

### Issue 1: CL0 proof ends ∎ before establishing the element-level equality claim
**ASN-0063, Lemma CL0 — BlockProjection**: "the image of their overlap through β is representable by a single well-formed I-span — that is, it is contained in the denotation of a span whose element-level members are exactly the image."
**Problem**: The lemma claims both containment and element-level exactness ("whose element-level members are exactly the image"). The ∎-delimited proof establishes containment and states "with equality at element level (depth #a_β). ∎" — but the element-level equality argument appears only in a separate paragraph *after* the ∎ marker ("The coverage *is* tight at element level..."). In a formal specification, the ∎-delimited proof must establish every claim in the lemma statement, not merely assert it. The proof content is present but structurally misplaced.
**Required**: Either move the element-level equality argument (the I-address discreteness proof) into the ∎-delimited proof before the QED marker, or separate CL0 into a containment lemma (proved within ∎) and a corollary for element-level tightness (proved separately).

### Issue 2: CL0 proof applies "convex" to a non-convex intersection
**ASN-0063, CL0 proof**: "Their non-empty intersection is therefore convex and of the form {v_β + k : c ≤ k < c'} for some 0 ≤ c < c' ≤ n."
**Problem**: The intersection V(β) ∩ ⟦σ_v⟧ is not convex in T. Between consecutive elements v_β + k and v_β + (k+1), there exist deeper tumblers (e.g., extensions of v_β + k at depth > #v_β) that lie in ⟦σ_v⟧ by T1(ii) and S0 but are *not* in V(β) and hence not in the intersection. What the proof actually establishes — correctly — is that the intersection is a *contiguous sub-range of V(β)*: if v_β + c and v_β + (c'-1) are both in ⟦σ_v⟧, then every intermediate v_β + k (c ≤ k ≤ c'-1) is also in ⟦σ_v⟧, by M1 (order preservation within V(β)) and S0 (convexity of ⟦σ_v⟧). The underlying reasoning is sound; the intermediate claim is false.
**Required**: Replace "Their non-empty intersection is therefore convex" with "Their non-empty intersection is therefore a contiguous sub-range of V(β)" or equivalent phrasing that correctly characterizes the index-level structure without claiming convexity in T.

### Issue 3: ExtendedReachableStateInvariants base case omits D-CTG and D-MIN
**ASN-0063, Extended initial state / ExtendedReachableStateInvariants proof**: "The extended invariants hold vacuously at Σ₀: L0, L1, L1a, L12, L14 are satisfied by empty L; S3★'s link-subspace clause is vacuous..."
**Problem**: The ExtendedReachableStateInvariants theorem adds D-CTG and D-MIN to the invariant conjunction (they do not appear in ASN-0047's ReachableStateInvariants). The base case verification enumerates L0, L1, L1a, L12, L14, S3★, P4★, and S3★-aux but does not mention D-CTG or D-MIN. Both hold vacuously at Σ₀ (M₀(d) = ∅ for all d, so V_S(d) = ∅ for every subspace S), but the verification should be explicit. The theorem's invariant set is the primary deliverable of this ASN; every new conjunct requires a stated base-case check.
**Required**: Add explicit base-case verification for D-CTG and D-MIN at Σ₀ (vacuous, since all arrangements are empty).

## OUT_OF_SCOPE

### Topic 1: Type-endset stability across arrangement changes
The canonical decomposition (M12) is state-dependent — INSERT, DELETE, or COPY on a source document can split or merge blocks, changing the span-set that resolve produces for a given V-selection. Two CREATELINKs with the same V-selection in different states may produce structurally different type endsets, failing L8 (TypeByAddress) comparison. The ASN correctly identifies this as an open question ("What must resolution guarantee when the arrangement changes...").
**Why out of scope**: This concerns cross-state consistency semantics for type comparison, which requires defining a type-equivalence relation beyond L8's span-set equality — new territory, not an error in the CREATELINK definition.

### Topic 2: Link withdrawal mechanism
The ASN identifies that link-subspace K.μ⁻ is constrained by D-CTG to suffix truncation, and that K.μ~ cannot close gaps (link-subspace fixity). Nelson's "deleted links" concept (LM 4/9) suggests a status mechanism rather than arrangement removal.
**Why out of scope**: The withdrawal mechanism requires defining link lifecycle states — active, withdrawn, historically recoverable — which is a new invariant domain.

### Topic 3: Composition of K.μ⁻ amendment with future operations
The D-CTG/D-MIN postcondition on K.μ⁻ constrains contraction to suffix truncation per subspace. DELETE of an interior position would require a composite (K.μ⁻ suffix removal + K.μ⁺ re-insertion), not a single K.μ⁻. This is an architectural consequence, not an error.
**Why out of scope**: DELETE, INSERT, COPY, and REARRANGE mechanics are explicitly out of scope.

VERDICT: REVISE
