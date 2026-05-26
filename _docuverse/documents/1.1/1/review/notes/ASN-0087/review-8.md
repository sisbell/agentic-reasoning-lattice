# Review of ASN-0087

## REVISE

### Issue 1: Notation drift between substrate (ASN-0093) and transition model (ASN-0047)
**ASN-0087, Inputs and Preconditions sections**: The ASN says "A *home document* `d ∈ dom(Σ.M)`" and recapitulates `d ∈ dom(M)` as K.μ⁺_L's first precondition, but K.μ⁺_L (defined in ASN-0047) literally requires `d ∈ E_doc`.
**Problem**: ASN-0093 uses `dom(M)`; ASN-0047 uses `E_doc`. The ASN mixes vocabularies without explicit bridging, leaving the reader to infer that `d ∈ dom(M) ⟹ d ∈ E_doc` in the combined model. The K.μ⁺_L precondition discharge is incomplete: showing `d ∈ dom(M)` does not literally discharge `d ∈ E_doc`.
**Required**: Add a brief note establishing the equivalence in the combined ASN-0093 + ASN-0047 model (K.δ IsDocument and K.σ both register `d` into both `dom(M)` and `E_doc` simultaneously, and ASN-0047 preserves the equivalence as an invariant). Either use one vocabulary consistently or state the equivalence at first use.

### Issue 2: S2 verification omits cross-subspace exclusion argument
**ASN-0087, Invariant Preservation, Per-State Invariants at Σ'**: "S2: M'(d) remains a partial function — v_ℓ ∉ dom(Σ.M(d)) by K.μ⁺_L positioning + D-SEQ★ at Σ (V_{s_L}(d) = {[s_L, k] : 1 ≤ k ≤ n_L}, v_ℓ = [s_L, n_L + 1] outside this set)..."
**Problem**: The cited argument establishes only `v_ℓ ∉ V_{s_L}(d)`. S2 preservation requires `v_ℓ ∉ dom(M(d))` entirely, including `V_{s_C}(d)`. The cross-subspace exclusion — subspace(v_ℓ) = s_L ≠ s_C precludes v_ℓ from equalling any element of V_{s_C}(d) — is load-bearing but left implicit.
**Required**: Make the cross-subspace argument explicit. Add: by S3★-aux, `dom(M(d)) = V_{s_C}(d) ∪ V_{s_L}(d)`; since `(v_ℓ)₁ = s_L` while `(v)₁ = s_C` for every `v ∈ V_{s_C}(d)` and `s_L ≠ s_C` by SC-NEQ, `v_ℓ ∉ V_{s_C}(d)`. Combined with `v_ℓ ∉ V_{s_L}(d)`, `v_ℓ ∉ dom(M(d))`.

### Issue 3: Boundary case — empty non-type endset not addressed
**ASN-0087, Inputs section and Worked Example**: Inputs admits L3-compliant endsets (`eᵢ ∈ Endset` for all i, `e₃ ≠ ∅`), so `e₁` or `e₂` may legitimately be empty. The worked example uses three non-empty endsets only.
**Problem**: Empty endset is a mandatory boundary case. With `eᵢ = ∅`, `coverage(eᵢ) = ∅` (empty union), `project(ℓ, i, d, Σ') = ∅` for every d, and the wp's i-disjunct collapses to false. This boundary is not exercised, noted, or referenced anywhere in the ASN. A reader cannot tell from the analysis alone whether the wp formula `(E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)` degrades gracefully when slots have empty coverage.
**Required**: Either extend the worked example with an empty `e₁` or `e₂` (showing the link is still allocated, S3★ holds, and discoverability proceeds only via non-empty slots), or add a brief paragraph confirming that empty non-type endsets are permitted by L3, yield `coverage = ∅` trivially, and contribute zero to LP12-based discoverability.

### Issue 4: L1c chain step k₃ admissibility threshold not flagged as tight
**ASN-0087, Invariant Preservation, L1c chain table**: "t₃ = inc(b_L(d), 1) = t_1^L(d) ... TA5a's `k = 1` admissibility requires `zeros(b_L(d)) ≤ 3`; from step t₂ we have `zeros(b_L(d)) = 3`, so the bound holds with equality."
**Problem**: The k=1 step at position 3 saturates the zero-count bound exactly (zeros(b_L(d)) = 3 = limit). Similarly the k=2 step at position 1 saturates `zeros(d) = 2 = limit`. The author notes "the bound holds with equality" but does not call out that *both* admissibility bounds are saturated simultaneously, making this the unique structural path with no slack. A reader reconstructing the chain may not realise that a hypothetical alternative path (e.g., two consecutive k=2 steps from d) is mathematically impossible because the second would require zeros ≤ 2 against a state already at zeros = 3.
**Required**: Add one sentence noting that both admissibility bounds saturate, and that the chain is therefore the *unique* structural inc-derivation of any `ℓ ∈ dom(L)` from its home document. This strengthens the L1c discharge from "a chain exists" to "the chain is canonical".

## OUT_OF_SCOPE

### Topic 1: Protocol-layer composite atomicity mechanism
**Why out of scope**: M-CompAtomicity correctly identifies that substrate-level atomicity does not apply to the K.λ ; K.μ⁺_L composite. The mechanism by which a protocol layer enforces external atomicity (request-response transactionality, batching, distributed locking) is a layering concern outside the substrate.

### Topic 2: BREAKLINK / link deletion semantics
**Why out of scope**: The substrate vocabulary provides no link-deletion operation, only K.λ (allocation) and K.μ⁻ (arrangement contraction). The composite for "remove a link from a document's arrangement" or "destroy a link entirely" belongs to a future ASN.

### Topic 3: Endset well-formedness when spans reference unallocated I-addresses
**Why out of scope**: L4 (EndsetGenerality, ASN-0043) explicitly permits endsets to reference arbitrary tumblers in T, including those not currently allocated. Whether additional well-formedness should be imposed at endset-formation time is a foundation-level design question raised in Open Questions, not a MAKELINK-specific concern.

### Topic 4: Symmetric type-endset hierarchy semantics
**Why out of scope**: The ASN treats slot 3 uniformly with other slots beyond the non-empty constraint. Richer type-hierarchy treatment (using L10's containment lemma or domain-specific link-type semantics) belongs to a future ASN focused on link typing.

### Topic 5: MAKELINK arity > 3
**Why out of scope**: The wp formula and per-slot invariants quantify over all `i ∈ {1, …, N}`, so the analysis is general in N. The worked example uses N = 3 (the minimum). Demonstration of N ≥ 4 cases would not test new behaviour and would not surface new invariants — the per-slot analysis is uniform.

VERDICT: REVISE
