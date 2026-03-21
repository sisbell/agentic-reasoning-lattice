# Review of ASN-0059

## REVISE

### Issue 1: Composite transition step (ii) is not well-defined when the shift is vacuous

**ASN-0059, INSERT as Composite Transition**: "The composite Σ → Σ' consists of: ... (ii) *Arrangement reordering* — K.μ~ on document d: for V-positions ≥ p in subspace S, the bijection π : v ↦ shift(v, n) reindexes the existing mappings."

**Problem**: K.μ~ is defined in ASN-0047 as a distinguished composite of K.μ⁻ + K.μ⁺, where K.μ⁻ requires `dom(M'(d)) ⊂ dom(M(d))` (strict subset) and K.μ⁺ requires `dom(M'(d)) ⊃ dom(M(d))` (strict superset). When the set `{v ∈ dom(M(d)) : subspace(v) = S ∧ v ≥ p}` is empty — which occurs when inserting into an empty subspace (`M(d) = ∅` or no positions in subspace S) or appending past all existing positions (`p > v_max`) — the bijection π is the identity on dom(M(d)). K.μ⁻ cannot strictly contract an empty domain, and cannot strictly contract a domain only to restore it identically via K.μ⁺. Step (ii) is therefore inapplicable in these cases, but the ASN presents it unconditionally.

The postcondition (I1–I5) is correct regardless — I3 ranges over the empty set, so the effect is I0 + I2 + I1/I4 holding vacuously. The gap is in the composite structure that establishes INSERT as a valid composite transition per ASN-0047.

**Required**: Make step (ii) conditional: "When `{v ∈ dom(M(d)) : subspace(v) = S ∧ v ≥ p} ≠ ∅`, apply K.μ~ with bijection π...; when this set is empty, step (ii) is omitted." Then verify that the reduced composite (steps i, iii, iv only) still satisfies J0, J1, J1'. The argument is straightforward — the same coupling reasoning applies since K.μ~ contributes no new content or provenance — but it must be stated.

### Issue 2: Elementary preconditions at intermediate states not verified

**ASN-0059, INSERT as Composite Transition**: "(i) *Content allocation* — n applications of K.α: each allocates one I-address aᵢ with C' = C ∪ {aᵢ ↦ valᵢ}. Precondition: IsElement(aᵢ) ∧ origin(aᵢ) ∈ E_doc."

**Problem**: ASN-0047's ValidComposite requires "each step Σᵢ → Σᵢ₊₁ satisfies the precondition of its elementary transition kind, evaluated at the intermediate state Σᵢ." K.α's effect specification includes `a ∉ dom(C)`, which must hold at each intermediate state, not just the initial state. The second K.α step requires `a₂ ∉ dom(C ∪ {a₁ ↦ val₁})`, not just `a₂ ∉ dom(C)`. The derivation is one line — I0(ii) gives `a₂ = a₁ + 1 > a₁` by TA-strict, so `a₂ ≠ a₁`, combined with I0(i) giving `a₂ ∉ dom(C)` — but it should be stated. Similarly, the K.μ⁺ precondition that new V-positions are not already in the post-K.μ~ domain is asserted implicitly (the shift vacated them) but not derived.

**Required**: Add a paragraph after the composite step listing that verifies elementary preconditions at intermediate states. For K.α: "Each aᵢ is fresh with respect to the intermediate content store: aᵢ ∉ dom(C) by I0(i), and aᵢ ∉ {a₁, ..., aᵢ₋₁} since I0(ii) gives aⱼ < aⱼ₊₁ for all j." For K.μ⁺: "The new V-positions {p + k : 0 ≤ k < n} are not in dom(M(d)) after step (ii): positions in subspace S at or beyond p have been shifted to positions ≥ p + n, and positions in other subspaces have different subspace identifiers."

## OUT_OF_SCOPE

### Topic 1: Contiguity as system invariant vs. caller precondition

**Why out of scope**: The ASN correctly identifies this as an open question and provides the conditional guarantee (I9). Resolving whether VContiguity should be enforced by I8 (adding `v_min ≤ p ≤ v_max + 1` as a precondition) or left to callers affects the INSERT precondition but is a system-level design decision that may depend on DELETE and REARRANGE semantics — topics explicitly out of scope.

### Topic 2: Canonical starting position for empty documents

**Why out of scope**: When `M(d) = ∅`, I8 permits any valid text-subspace V-position as p. The choice of first insertion position establishes the V-space's origin and depth. Whether the system should prescribe a canonical starting position (e.g., `[1, 1]`) is a convention question that affects no invariant in this ASN.

VERDICT: REVISE
