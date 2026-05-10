# Review of ASN-0067

## REVISE

### Issue 1: Elementary decomposition (Case 1) misapplies K.μ~ and violates D-CTG

**ASN-0067, Elementary Decomposition, Case 1**: "Steps 1–2 together effect the K.μ~ reordering."

**Problem**: Steps 1–2 do not constitute K.μ~. Three independent failures:

(a) **K.μ~-FIX violated.** K.μ~-FIX (ASN-0047) establishes `dom(M'(d)) = dom(M(d))` — the bijection is a permutation of a fixed domain. After step 1 (remove B_post) and step 2 (add shifted B_post at displaced V-positions), the domain changes: pre-state `V_S(d) = {[S,k] : 1 ≤ k ≤ N}`, post-state `V_S(d) = {[S,k] : 1 ≤ k < v_m} ∪ {[S,k] : v_m + w ≤ k ≤ N + w - 1}`. The sets have equal cardinality but are not equal.

(b) **K.μ⁺ postcondition D-CTG violated.** K.μ⁺ (ASN-0047) requires "M'(d) satisfies D-CTG and D-MIN" as a precondition on the result. The step 2 K.μ⁺ produces a gap `[v, v + w)` in V_S(d). D-CTG is not satisfied.

(c) **K.μ~ precondition D-CTG violated.** K.μ~ itself requires "M'(d) satisfies S8-depth, D-CTG, D-MIN." The gapped result fails D-CTG, so K.μ~ is not applicable.

The ASN attempts to justify this with: "D-CTG is thus not an invariant of all reachable states — it is a design constraint that complete operations are expected to preserve at their endpoints." This contradicts ExtendedReachableStateInvariants (ASN-0047), which lists D-CTG as an invariant of every reachable state, and contradicts ValidCompositeExtended, which requires each elementary step to satisfy its transition kind's precondition.

**Required**: Replace the 4-step decomposition with a valid 3-step decomposition:

- Step 1 (K.μ⁻): Remove B_post from M(d). Result: V_S(d) = [v₀, v), satisfying D-CTG and D-MIN.
- Step 2 (K.μ⁺): Add placed blocks AND shifted B_post blocks simultaneously. Result: V_S(d) = [v₀, v₀ + N + w), satisfying D-CTG and D-MIN.
- Step 3 (K.ρ): Record provenance.

No K.μ~ is needed. COPY is K.μ⁻ + K.μ⁺ + K.ρ (or just K.μ⁺ + K.ρ when B_post = ∅). Remove the D-CTG reinterpretation paragraph entirely — it contradicts the foundation and is unnecessary once the decomposition is corrected.

---

### Issue 2: P.7 is too weak to restrict COPY to the content subspace

**ASN-0067, Preconditions**: "P.7: v₁ ≥ 1 (text subspace). COPY places content — it does not create links."

**Problem**: `v₁ ≥ 1` does not restrict to the content subspace. From ASN-0047 SubspaceIdentifiers: `s_C ≥ 1` and `s_L ≥ 1`. Both subspace identifiers satisfy `v₁ ≥ 1`, so P.7 admits `v₁ = s_L` (the link subspace). This creates two conflicts:

(a) The K.μ⁺ amendment (ASN-0047) requires `subspace(v) = s_C` for new V-positions. Placed blocks have subspace `v₁` (ordinal shift preserves the first component). If `v₁ = s_L`, placed blocks violate the amendment.

(b) Shifting link-subspace V-positions (in B_post when `v₁ = s_L`) would disrupt the link subspace ordering maintained by K.μ⁺_L and could violate CL-OWN.

P.7 as stated is vacuous given S8a (`v₁ ≥ 1`).

**Required**: Replace `v₁ ≥ 1` with `subspace(v) = s_C`. Update the Properties Table accordingly.

---

### Issue 3: Link subspace identifier stated as 0

**ASN-0067, Effects**: "all subspaces other than S — including the link subspace (v₁ = 0) and any other text subspaces"

**Problem**: The parenthetical `(v₁ = 0)` is wrong. ASN-0047 derives `s_L ≥ 1` (from L1, T4, S7b). ASN-0036 S8a requires `v₁ ≥ 1` for all V-positions. There is no subspace with identifier 0.

**Required**: Replace `(v₁ = 0)` with `(v₁ = s_L)` or remove the parenthetical.

---

### Issue 4: C3 omits extended-state invariants

**ASN-0067, C3**: "The COPY composite preserves every foundational invariant."

**Problem**: The ASN works with `Σ = (C, E, M, R)` and checks invariants from ReachableStateInvariants (the non-extended theorem). ASN-0047's ExtendedReachableStateInvariants — the complete framework for systems with links — additionally requires: S3★, S3★-aux, P3★, P4★, P5★, L0, L1, L1a, L3, L12, L14, CL-OWN. None are checked.

All are trivially preserved (L is in the frame, C' = C, E' = E), but the claim "every foundational invariant" is not substantiated without them. Specifically:
- S3★ (GeneralizedReferentialIntegrity) replaces S3 in the extended framework — the ASN checks S3 but not S3★.
- P4★ (ProvenanceBoundsContent) replaces P4 — the ASN checks P4 but not P4★.
- CL-OWN (LinkSubspaceOwnership) — must hold after COPY, which is true because link-subspace V-positions are in B_other (unchanged), but this should be stated.

**Required**: Either (a) extend C3 to cover ExtendedReachableStateInvariants (stating that L' = L places all L-related invariants in the frame), or (b) narrow the claim to the non-extended invariants and note that extension to the full framework follows from L being in the frame.

---

## OUT_OF_SCOPE

### Topic 1: Concurrency model
**Why out of scope**: The ASN correctly identifies (under C13) that "Formalizing the requirement that intermediate states are invisible to other operations requires a concurrency model not yet present in the foundation." This belongs in a future ASN defining serialization semantics.

VERDICT: REVISE
