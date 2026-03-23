# Review of ASN-0067

## REVISE

### Issue 1: C3 claims completeness but omits S1 and S8
**ASN-0067, C3 — InvariantPreservation**: "The COPY composite preserves every foundational invariant."
**Problem**: The derivation enumerates specific invariants but omits S1 (StoreMonotonicity) and S8 (FiniteSpanDecomposition), both of which appear in ExtendedReachableStateInvariants (ASN-0047). S1 follows trivially from C' = C (dom(C') = dom(C) ⊇ dom(C)). S8 follows from its prerequisites (S8-fin, S8a, S2, S8-depth, D-CTG, D-MIN), all of which are verified. The gap is cosmetic but the claim of completeness demands either explicit mention or a note that these are derived consequences.
**Required**: Add one-line derivations for S1 and S8, or add a blanket note that corollaries of verified invariants are inherited.

### Issue 2: State declaration omits L; effects block incomplete
**ASN-0067, intro**: "We work with system state Σ = (C, E, M, R) per ASN-0047."
**Problem**: ASN-0047's extended state is Σ = (C, L, E, M, R). The COPY definition's preconditions reference extended-state concepts (s_C, s_L in P.4a and P.7), and C3 verifies extended-state invariants (L0–L14, S3★, CL-OWN). Yet L is absent from both the state declaration and the effects block. The C3 derivation later states "By the frame conditions of K.μ⁻, K.μ⁺, and K.ρ (each holds L in its frame): L' = L" — but the frame conditions as stated in ASN-0047 do not explicitly list L for these transitions (they were defined for the non-extended state; their amendments add preconditions but not frame entries for L). The correct reasoning is that these transitions have no effect on L, so L is unchanged — but this should be stated in the effects, not derived later from frame conditions that don't actually mention L.
**Required**: Either (a) declare Σ = (C, L, E, M, R) in the intro and add `L' = L` to the effects block, or (b) note in the intro that L is omitted from the state because COPY has no L-modifying transitions and add a sentence deriving L' = L before the extended-state invariant verification.

### Issue 3: Per-subspace verification gap at intermediate states
**ASN-0067, Elementary Decomposition, Case 1, Step 1**: "Postcondition: M₁(d) satisfies D-CTG — by D-SEQ, the remaining positions form a contiguous range [v₀, v), and D-MIN holds since min(V_S(d₁)) = v₀ = [S, 1, ..., 1] is unchanged."
**Problem**: The K.μ⁻ amendment (ASN-0047) requires "D-CTG and D-MIN postconditions extend to the two-subspace case: contraction must satisfy D-CTG and D-MIN for each subspace independently." The derivation verifies D-CTG and D-MIN only for the target subspace S = s_C. The link subspace (s_L) is unchanged by the contraction (only B_post ⊆ B_S entries are removed), so D-CTG and D-MIN are inherited trivially — but this is not stated. The same gap recurs in Step 2 (K.μ⁺): the derivation verifies D-CTG and D-MIN for subspace s_C but not s_L.
**Required**: Add one sentence in each step noting that non-target subspaces are unchanged, satisfying the per-subspace amendment.

### Issue 4: J1★/J1'★ equivalence argument incomplete
**ASN-0067, C3 extended-state invariants**: "The coupling constraints J1★ and J1'★ (ASN-0047) are equivalent to J1 and J1' for COPY, since COPY creates only content-subspace V-positions (P.7)."
**Problem**: P.7 alone does not establish the equivalence. J1★ considers I-addresses appearing in content-subspace positions of M'(d) but absent from content-subspace positions of M(d). J1 considers I-addresses in ran(M'(d)) \ ran(M(d)). These differ when an I-address appears in a link-subspace position of M(d) but not a content-subspace position. The equivalence additionally requires that no I-address in dom(C) can appear in a link-subspace position — which follows from S3★ (link-subspace maps to dom(L)) and L14 (dom(C) ∩ dom(L) = ∅). Without L14, the argument has a gap.
**Required**: Cite L14 and S3★ alongside P.7 in the equivalence justification, or expand to two sentences showing that content I-addresses cannot reside in link-subspace positions.

### Issue 5: V-ordering citation incorrect
**ASN-0067, Source Resolution**: "This is a consequence of the block decomposition being V-ordered (B1, ASN-0058)."
**Problem**: B1 (Coverage) states that every V-position appears in exactly one block — it is a uniqueness/coverage property, not an ordering property. The V-ordering of the resolved sequence comes from the Resolution definition (ASN-0058), which specifies "⟨β₁, ..., βₖ⟩ ordered by V-start."
**Required**: Replace "(B1, ASN-0058)" with "(Resolution, ASN-0058)" or cite the V-start ordering from the resolution definition directly.

## OUT_OF_SCOPE

### Topic 1: Link discoverability after transclusion
**Why out of scope**: The ASN correctly notes that COPY places content I-addresses, and links reference I-addresses via endsets. Whether links attached to the source content become discoverable at the target is a link-semantics question, not a COPY-definition question. The ASN explicitly scopes out link semantics.

### Topic 2: Concurrent COPY serialization
**Why out of scope**: The ASN notes that ValidComposite provides sequential correctness only and correctly identifies concurrent access as requiring a concurrency model not yet in the foundation. This is a future-ASN concern, flagged in the open questions.

VERDICT: REVISE
