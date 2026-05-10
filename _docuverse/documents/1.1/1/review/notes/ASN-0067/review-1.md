# Review of ASN-0067

## REVISE

### Issue 1: ContentReference span denotation is unsatisfiable over fixed-depth V-positions

**ASN-0067, Source Resolution**: "A *content reference* is a pair (d_s, σ) where d_s ∈ E_doc and σ = (u, ℓ) is a well-formed V-span (T12, ASN-0034) with ⟦σ⟧ ⊆ dom(M(d_s))."

**Problem**: The span denotation ⟦σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)} (T12, ASN-0034; SpanDenotation, ASN-0053) ranges over the full tumbler set T, which includes tumblers of every depth. But dom(M(d_s)) contains only V-positions of a single fixed depth m (S8-depth, ASN-0036). The lexicographic order (T1) places proper-prefix tumblers before their extensions, so for any depth-m span with width ≥ 1, the denotation necessarily includes tumblers of depth > m. Concretely: if u = [S, k] and ℓ = [0, n], then [S, k, 1] satisfies u ≤ [S, k, 1] < u ⊕ ℓ by T1(ii) and T1(i), yet [S, k, 1] has depth 3 and cannot belong to dom(M(d_s)). The containment ⟦σ⟧ ⊆ dom(M(d_s)) is therefore unsatisfiable for any non-trivial span, making the ContentReference definition vacuously true and every claim that depends on it vacuously derived.

The resolution definition itself (restriction M(d_s)|⟦σ⟧) accidentally works — the restriction filters to dom(M(d_s)) ∩ ⟦σ⟧, which picks out the correct depth-m V-positions. But the precondition is wrong.

**Required**: Replace ⟦σ⟧ ⊆ dom(M(d_s)) with a depth-restricted containment. For instance, define the V-position range as {v ∈ dom(M(d_s)) : start(σ) ≤ v < reach(σ)} and require this equals the ordinal range of w consecutive V-positions starting from u. Alternatively, state the content reference directly in ordinal terms: "the V-positions shift(u, 0), shift(u, 1), ..., shift(u, n−1) are all in dom(M(d_s))."

---

### Issue 2: D-MIN not verified; ValidInsertionPosition for empty documents is incomplete

**ASN-0067, Displacement**: "When N = 0, any v satisfying S8a and S8-depth for d's text subspace is valid."

**Problem**: D-MIN (ASN-0036) requires min(V_S(d)) = [S, 1, ..., 1] of depth m whenever V_S(d) is non-empty. After COPY into an empty document (N = 0), the placed blocks start at v, making v the minimum V-position. The ValidInsertionPosition definition constrains v only by S8a (positive, no zeros) and S8-depth (vacuously satisfied — no existing positions to match). It does not require v = [S, 1, ..., 1], so a COPY choosing v = [S, 5] or v = [S, 1, 3] would produce a state violating D-MIN.

Separately, D-MIN preservation for the non-empty case (N > 0) is never stated or checked. It does hold — when v > v₀ the minimum is unchanged; when v = v₀ the placed blocks start at v₀ — but the argument should be explicit, especially given that C2 explicitly verifies D-CTG, the companion invariant.

**Required**: (a) Add to ValidInsertionPosition for N = 0: "v = [S, 1, ..., 1] of depth m for some m ≥ 2." (b) State and verify D-MIN preservation as part of or alongside C2.

---

### Issue 3: C3 claims "every foundational invariant" but verifies a subset

**ASN-0067, Invariant Preservation**: "**C3 — InvariantPreservation (THEOREM).** The COPY composite preserves every foundational invariant."

**Problem**: The derivation verifies P0, P1, P2, S0, S2, S3, S8a, S8-depth, S8-fin, P4, J0, J1. The claim is "every foundational invariant." Missing from the explicit check:

- **P6** (ExistentialCoherence): dom(C') = dom(C) and E' = E, so preserved — but not stated.
- **P7** (ProvenanceGrounding): new provenance pairs (a, d) have a ∈ ran(M'(d)) ⊆ dom(C') by S3 — but not derived.
- **P7a** (ProvenanceCoverage): dom(C) unchanged and R' ⊇ R — but not stated.
- **P8** (EntityHierarchy): E' = E — but not mentioned.
- **J1'** (ProvenanceRequiresExtension): the construction adds (a, d) ∈ R' \ R only when a ∈ ran(M'(d)) \ ran(M(d)), satisfying J1' by construction. The effects section alludes to this ("By J1', this is the only permitted extension") but C3 doesn't verify it.
- **D-CTG**: proven as C2 but not referenced by C3.
- **D-MIN**: not verified at all (see Issue 2).

Most are trivially preserved, but a theorem claiming "every" must verify every. Otherwise, narrow the claim to match the verification.

**Required**: Either (a) add the missing one-line verifications for P6, P7, P7a, P8, J1', and reference C2 for D-CTG, or (b) change the claim to "C3 — InvariantPreservation (THEOREM). The COPY composite preserves P0, P1, P2, S0, S2, S3, S8a, S8-depth, S8-fin, P4, J0, J1" and treat the others separately.

---

### Issue 4: No elementary decomposition for ValidComposite

**ASN-0067, The Fundamental Constraint**: "An operation that modifies arrangement without creating content is, in the framework of ASN-0047, a composite of K.μ⁺ (arrangement extension), K.μ~ (arrangement reordering), and K.ρ (provenance recording)."

**Problem**: ValidComposite (ASN-0047) requires a finite sequence of elementary transitions Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ' where each step satisfies its elementary precondition at the intermediate state Σᵢ. The ASN defines the final state directly and verifies final-state invariants, but never constructs the elementary decomposition or checks intermediate preconditions.

The natural decomposition is: (1) K.μ~ shifting B_post entries, producing an intermediate arrangement with a gap at [v, v + w); (2) K.μ⁺ filling the gap with placed blocks; (3) K.ρ recording provenance. The intermediate state after step 1 has a gap violating D-CTG, but D-CTG is a design constraint, not a K.μ⁺ precondition — so the decomposition works. Step 2's precondition (new I-addresses in dom(C), V-positions satisfying S8a/S8-depth/S8-fin) holds by C1 and the construction. But none of this is shown.

**Required**: Construct the elementary decomposition (K.μ~, K.μ⁺, K.ρ) and verify that each intermediate state satisfies the precondition of the next elementary step.

---

### Issue 5: C13 makes an unsupported concurrency claim

**ASN-0067, Atomicity**: "There is no intermediate state visible to other operations where the arrangement is partially modified."

**Problem**: The ValidComposite framework (ASN-0047) defines correctness of a composite transition as: elementary preconditions hold at each intermediate state, and coupling constraints (J0, J1, J1') hold between initial and final states. It provides no semantics for concurrent access or visibility. The first sentence of C13 — "either completes with all coupling constraints holding at the final state, or does not occur" — follows from ValidComposite. The second sentence — "no intermediate state visible to other operations" — is a concurrency guarantee that the framework does not supply. The Nelson quotes about "canonical operating condition" motivate the property but do not derive it.

**Required**: Separate the two claims. The sequential-correctness claim (ValidComposite) is derivable and should stand. The concurrency/visibility claim should be flagged as a design requirement that needs a concurrency model (not yet in the foundation) to formalize. If the intent is only to state that the composite produces a valid state — not that concurrent access is controlled — then remove the visibility clause.

---

### Issue 6: Resolution applies M11/M12 to a restriction without justification

**ASN-0067, Source Resolution**: "By M11 and M12 (ASN-0058), f admits a unique maximally merged block decomposition."

**Problem**: M11 and M12 are stated for full document arrangements: "Every arrangement M(d) admits a maximally merged block decomposition" (M11); "The maximally merged decomposition is unique" (M12). Here f = M(d_s)|⟦σ⟧ is a restriction to a subset of V-positions — not a full arrangement. The construction underlying M11/M12 (greedy maximal run extraction) does apply to any partial function from V-positions to I-addresses satisfying the relevant properties (S2, S8-depth, S8-fin), and f inherits these from M(d_s). But this step-down argument is not stated.

**Required**: Add one sentence noting that M11/M12's proofs depend only on the function being injective per V-position (S2), finite-domain (S8-fin), and fixed-depth (S8-depth) — properties inherited by any restriction of M(d_s) to a contiguous V-span.

---

## OUT_OF_SCOPE

### Topic 1: Serialization of concurrent COPY operations
**Why out of scope**: The ASN-0047 framework defines sequential composite transitions. A concurrency model (locks, serializability, isolation levels) is a separate concern requiring its own ASN.

### Topic 2: Authorization for cross-document COPY
**Why out of scope**: The ASN correctly observes that Nelson's ownership model prohibits modification of others' documents, and that COPY does not modify the source. Access control for *reading* the source (to resolve content references) is a policy question outside the state-transition framework.

### Topic 3: Version-fixed vs location-fixed transclusion
**Why out of scope**: Listed in the ASN's own open questions. This requires version semantics (not yet formalized) and is a future concern.

### Topic 4: V-position depth for the first content in a new document
**Why out of scope**: This is a system-level design choice (e.g., "text subspace uses depth 2") that constrains COPY's ValidInsertionPosition for N = 0 but belongs in a document-lifecycle or system-configuration ASN, not in the COPY operation definition.

VERDICT: REVISE
