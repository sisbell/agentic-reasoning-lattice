# Review of ASN-0087

## REVISE

### Issue 1: Weakest precondition statements omit document-membership precondition

**ASN-0087, "Weakest Precondition for Discoverability" and claim M-WP**: "Case 1: d_target ≠ d... `wp(MAKELINK, discoverable_from(ℓ, d_target, ·)) ≡ (E i :: coverage(eᵢ) ∩ ran(Σ.M(d_target)) ≠ ∅)`"

**Problem**: `discoverable_from(a, d, Σ)` is defined in ASN-0098 only "when `a ∈ dom(Σ.L) ∧ d ∈ dom(Σ.M)`". The wp for both Case 1 (`d_target ≠ d`) and Case 2 (`d_target = d`) is implicit about the precondition `d_target ∈ dom(Σ.M)`. Without it, the post-state predicate is undefined and the wp is malformed. The same gap appears in claim M-WP itself.

**Required**: Conjoin `d_target ∈ dom(Σ.M)` explicitly in each wp branch, or qualify the wp as conditional on this membership. For Case 1, note also that MAKELINK preserves `dom(M)`, so `d_target ∈ dom(Σ.M) ⟺ d_target ∈ dom(Σ'.M)`.

### Issue 2: "Caller knowledge" framing in Reflexive Endsets misrepresents substrate behavior

**ASN-0087, "Reflexive Endsets"**: "The substrate does not expose A_L(d)'s next emission to the caller. Endsets are chosen without knowledge of ℓ."

**Problem**: A_L(d)'s next emission is fully deterministic from the current state — `[d.0.s_L.1]` for first emission, `inc(max{ℓ' : origin(ℓ') = d}, 0)` otherwise. A client with state access can compute `ℓ` before invoking MAKELINK; the substrate provides no architectural barrier against this. The real defense — that under standard authoring, K.λ's freshness `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)` combined with `coverage(eᵢ) ⊆ dom(Σ.C) ∪ dom(Σ.L)` forces `ℓ ∉ coverage(eᵢ)` — is correctly identified two paragraphs later, but the initial framing suggests a structural protection where none exists. The follow-up "Note on caller knowledge" partially clarifies this but does not retract the misleading earlier statement.

**Required**: Lead the section with the structural defense (standard authoring). Demote the caller-knowledge observation to a parenthetical about typical client behavior, or remove it entirely — it is informal protocol-level context, not a substrate guarantee.

### Issue 3: Bidirectional coupling between dom(M) and E_doc is a framework reconciliation done within an operation ASN

**ASN-0087, "Inputs"**: "The combined substrate (ASN-0093 + ASN-0047) reconciles these by imposing the bidirectional coupling `d ∈ dom(M) ⟺ d ∈ E_doc` as an *additional invariant of the combined model* — a constraint not present in either foundation ASN alone."

**Problem**: This introduces a framework-level invariant within an operation specification. While the ASN carefully presents two reconciliation readings ((a) supersede K.σ by K.δ-IsDocument, (b) extend K.σ with `E' = E ∪ {d}`) and notes MAKELINK is valid under either, the coupling itself is a substrate-level concern that affects every operation in the combined model. Downstream operation ASNs building on MAKELINK would each independently need to either assume the coupling or rebuild the reconciliation. The principle "one ASN does one job" suggests this belongs in a dedicated reconciliation ASN. The ASN does too much framework-establishment work.

**Required**: Either cite an existing substrate-reconciliation source, or note explicitly that MAKELINK's analysis is *modulo* a not-yet-written reconciliation, and reduce the inline treatment to a pointer rather than a justification of the coupling.

### Issue 4: L1c uniqueness derivation is correct but unnecessarily dense

**ASN-0087, "Per-State Invariants at Σ'"**: The argument that the inc-chain `(d, b_C(d), b_L(d), t_1^L(d), …, ℓ)` is unique forces `k_1 = 2`, `k_2 = 0`, `k_3 = 1`, `k_j = 0` for `j ≥ 4` through four prose paragraphs of structurally parallel case analysis.

**Problem**: Each paragraph repeats the same pattern (enumerate admissible `k` values by TA5a; eliminate each non-target choice by `origin(ℓ) = d` or `E(ℓ)₁ = s_L` or `#ℓ = #d + 3`). Readers must reconstruct the argument's symmetry from scratch. The argument is correct but the presentation hides what is essentially a tabular structural derivation.

**Required**: Present the uniqueness as a table — one row per chain position, columns for "TA5a-admissible k values" and "non-target k excluded by which constraint". Or state uniqueness as a corollary with one compact structural argument: the conjunction of L1c's `#tᵢ > #d`, L0's `E(ℓ)₁ = s_L`, L1's `zeros(ℓ) = 3`, and ChainUniformLength's `#ℓ = #d + 3` jointly determines a unique `k`-sequence at each step.

## OUT_OF_SCOPE

The ASN's eight open questions — endset well-formedness for forward-reaching spans, composite-level atomicity protocol mechanism, semantic distinctness of identical endset values, deferred-consistency models, post-allocation transclusion discoverability, link V-position migration semantics, allocation-vs-placement distinction, limiting-case type-endset discoverability — are correctly deferred. Each names a topic that belongs in a future operation ASN, protocol-layer ASN, or type-semantics ASN.

VERDICT: REVISE
