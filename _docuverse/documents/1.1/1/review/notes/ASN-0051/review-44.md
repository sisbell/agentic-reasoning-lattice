# Review of ASN-0051

## REVISE

### Issue 1: SV14(d) witness construction is implicit on two fronts

**ASN-0051, SV14(d) Witness**: "Take the Worked Example's post-removal state... Consider any link a' with coverage(Σ.L(a').s) = {a₃} (a singleton endset on a₃)."

**Problem**: Two distinct gaps in the witness:

(a) *Link construction.* The witness invokes "any link a' with coverage = {a₃}" without showing such a link exists in the relevant state. The Worked Example only contains the named link b with from-endset F = {(a₂, ℓ)}. The candidate span (a₃, δ(1, #a₃)) has denotation `{t ∈ T : a₃ ≤ t < a₄}`, which includes child-depth tumblers between a₃ and a₄ — so coverage ⊋ {a₃} as a subset of T. The witness needs to either construct an actual link (specifying its span and the K.λ step that allocates it) or weaken to the property actually used: `coverage(Σ.L(a').s) ∩ ran(M_int(d)) = {a₃}` and `coverage ∩ ran(M'(d)) = ∅`.

(b) *Elementary K.μ⁻ identification.* SV14(d)'s formal statement is `Σ →_{K.μ⁻} Σ'` — an elementary K.μ⁻ transition. The witness presents the composite K.μ~ + K.μ⁻ acting on the pre-removal arrangement. The actual elementary K.μ⁻ step is from Σ_int (after K.μ~, with v₅↦a₃ established) to Σ' (with v₅ removed), and that's where the strict shrinkage occurs. The witness should explicitly identify this elementary step rather than presenting composite endpoints.

**Required**: Construct the link a' explicitly via K.λ in the witness chain (specifying its span and demonstrating the relevant ran-intersection property), and identify Σ_int → Σ' as the elementary K.μ⁻ transition the witness exhibits.

### Issue 2: SV6 precondition list omits T12

**ASN-0051, SV6 Precondition**: "s, b ∈ T; zeros(s) = 3 ∧ zeros(b) = 3; s, b are T4-valid; origin(b) ≠ origin(s); k > p₃"

**Problem**: The precondition list does not include T12 (SpanWellDefinedness) — the well-formedness of (s, ℓ). The proof uses `k = actionPoint(ℓ) ≤ #s` (from T12) repeatedly (e.g., establishing `j < k ≤ #s` in the prefix exclusion sub-lemma, and `j < #(s ⊕ ℓ)` from `k ≤ #ℓ = #(s ⊕ ℓ)` via TA0). T12 is implicit because (s, ℓ) is an endset span and Definition — Endset (ASN-0043) restricts to T12-well-formed spans, but a formal precondition list should be complete.

**Required**: Add T12 (or equivalently `Pos(ℓ) ∧ actionPoint(ℓ) ≤ #s`) to the precondition list, or add a sentence noting that (s, ℓ) is an endset span and therefore T12-well-formed by L4 + Definition — Endset.

### Issue 3: CrossDocumentDecoupling witness — Step 1's prefix-existence precondition

**ASN-0051, CrossDocumentDecoupling Witness, Step 1**: "Step 1 — K.δ allocates d₂ under a node/account prefix yielding origin(d₂) ≠ O... K.δ's preconditions are therefore satisfied."

**Problem**: Step 1 allocates d₂ = 1.0.1.0.2 under account 1.0.1. K.δ's `¬IsNode` precondition requires `parent(d₂) ∈ E`, i.e., the account at 1.0.1 must be in E. The witness's "Setup precondition" paragraph claims this is assumed pre-Σ (and discharged by InitialState fixing n₀ = 1), but the connection is loose: the account at 1.0.1 was allocated by K.δ to establish d₁ = 1.0.1.0.1 in the SV10 chain, and that account persists by P1 (EntityPermanence). The witness should state this entity-persistence reliance explicitly rather than packaging it inside a setup paragraph that conflates the node (system parameter from InitialState) with the account (transition product whose persistence relies on P1).

**Required**: Add an explicit citation of P1 (EntityPermanence) when claiming the account at 1.0.1 inhabits E throughout the witness chain, or restructure Step 1 to acknowledge that the account's persistence from the SV10 setup is what enables K.δ's prefix-existence precondition at Step 1.

## OUT_OF_SCOPE

### Topic 1: Link-subspace contribution to projection

**Why out of scope**: The ASN explicitly defers "The link-subspace contribution to projection — including links whose endsets reference other link addresses (L13, ReflexiveAddressing)" to a future "Link Subspace ASN". SV11's decomposition is restricted to π_text (content-subspace), and the full π treatment for link-referencing endsets is correctly identified as future work rather than a gap in this ASN.

### Topic 2: Broader-level span survivability

**Why out of scope**: The ASN restricts SV6 and the survivability analysis to element-level spans with action point strictly beyond p₃. Broader-level spans (action point at or before p₃, reaching across document/account/node prefixes) are admitted by L4 but their survivability under owner-gated prefix-region allocator discipline is deferred to ASN-0034's address-hierarchy treatment. This is appropriate scoping — broader-level spans require allocator-discipline machinery not developed here.

### Topic 3: Allocator-discipline conditions for same-origin coverage growth

**Why out of scope**: The "Content Allocation and Coverage Stability" section identifies sequential overshoot and child-depth entry as mechanisms by which same-origin allocations can enter existing endset coverage, but explicitly defers the precise conditions to ASN-0034. This is the right scope boundary — coverage-growth conditions depend on allocator discipline rather than survivability properties.

VERDICT: REVISE
