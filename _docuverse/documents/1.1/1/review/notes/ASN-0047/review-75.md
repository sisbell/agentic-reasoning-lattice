# Review of ASN-0047

## REVISE

### Issue 1: Loose attribution in worked example
**ASN-0047, "Worked example: fork with subsequent insertion"**: "The address falls under d₂'s prefix (S7a): origin(a₃) = 1.0.1.0.2 = d₂. By GlobalUniqueness, a₃ is fresh."
**Problem**: For the *first emission* of d₂'s content sub-allocator (which is exactly what a₃ = 1.0.1.0.2.0.1.1 is, since J4 transcluded a₁, a₂ from d₁ rather than allocating under d₂), T10a's GlobalUniqueness within a single frontier does *not* apply — there is no prior inc-produced address on d₂'s frontier to chain from. The ASN itself distinguishes this in K.α's precondition: "By the axiom or by GlobalUniqueness (depending on case)". The first-emission case routes through SubAllocatorAxiom's namespace property, with cross-document disjointness (T10a.{2,5}→T10) ensuring distinctness from addresses under d₁.
**Required**: Replace "By GlobalUniqueness" with a precise attribution: "By SubAllocatorAxiom (namespace property at first emission of d₂'s content sub-allocator) and the Cross-document disjointness lemma (distinctness from addresses under d₁)".

### Issue 2: Awkward presentation of K.δ zeros formula
**ASN-0047, K.δ case (ii) tumbler-depth extension cases**: "Combined: `zeros(e) = zeros(t) + max(0, k − 1)`... The earlier 'Combined: `zeros(e) = zeros(t) + (k − 1)`' expression — which would give `zeros(t) − 1` at k = 0 — is corrected here by the `max(0, ·)` clamp..."
**Problem**: The prose documents a correction to a formula that does not appear elsewhere in the ASN. It reads as an artifact of revision history, not as a clean specification. The per-case identities `zeros(e) = zeros(t)` for k ∈ {0, 1} and `zeros(e) = zeros(t) + 1` for k = 2 are the operative statements; the closed form with `max(0, ·)` is a convenience that needs no historical justification.
**Required**: Remove the "earlier formula" correction commentary. Present the per-case identities as primary; if retaining the closed form, present it directly without referring to a superseded version.

### Issue 3: Redundancy between P3★ and P5★ in ExtendedTransitionInvariants
**ASN-0047, ExtendedTransitionInvariants statement**: "Every valid composite transition `Σ → Σ'` between reachable states satisfies: P0 ∧ P1 ∧ P2 ∧ P3★ ∧ P5★ ∧ S9 ∧ L12"
**Problem**: P3★ (`dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R' ∧ value preservation on C and L`) and P5★ (`dom(C') ⊇ dom(C) ∧ values fixed; dom(L') ⊇ dom(L) ∧ values fixed; E' ⊇ E; R' ⊇ R; only M can lose information`) are semantically equivalent statements. The proofs of both in the per-transition section both reduce to "each conjunct is one of P0, L12, P1, P2." Listing both alongside P0, P1, P2, L12 is triple-counting the same monotonicity content.
**Required**: Either (a) remove one of P3★/P5★ from the per-transition theorem (the qualitative-vs-quantitative distinction the ASN draws does not survive into the per-transition form, where both are formal conjunctions of identical content), or (b) explicitly note the equivalence and explain why both names are retained (the ASN does so for S9-vs-P0 traceability but not for P3★-vs-P5★).

### Issue 4: K.α freshness mechanism in worked example for first-emission case
**ASN-0047, same fork example as Issue 1**: The precondition discharge for K.α's first-emission case under a freshly created document is implicit. The worked example does not exhibit *how* freshness is established for `a₃` against the cross-document case where d₁ has prior content addresses.
**Problem**: A reader would benefit from seeing the explicit chain: SubAllocatorAxiom underwrites `a₃ ∉ dom(C)` and `a₃ ∉ dom(L)` *intrinsically* (the axiom's namespace property), and the Cross-document disjointness lemma is what would handle distinctness *if* d₂ had inherited content via fork — but here the transclusion of a₁, a₂ from d₁ is at d₁'s I-addresses, so they don't enter d₂'s sub-allocator frontier, and the freshness chain reduces to the axiom alone.
**Required**: Either spell out the discharge mechanism explicitly in the worked example, or add a footnote clarifying that the worked example treats "By GlobalUniqueness" as shorthand for the umbrella discipline (axiom for first emission within a sub-allocator, T10a for subsequent emissions within a frontier, cross-document disjointness lemma for cross-document pairs).

## OUT_OF_SCOPE

### Topic 1: Tombstone-style link withdrawal
The Step 5 counterfactual exhibits that D-CTG★ + D-MIN★ rule out interior link-subspace removal, and Nelson's "not currently addressable" mechanism is not expressible. The ASN names this as a deferred open question.
**Why out of scope**: A separate withdrawal mechanism (status flag, tombstone marker, retraction link) requires state-model extension; appropriately deferred.

### Topic 2: Version-management semantics
Arrangement-transition invariants between successive versions, content-allocator linkage, version-lineage acyclicity.
**Why out of scope**: Belongs to a subsequent version-management ASN, which the open questions section names.

### Topic 3: Account-level k = 1
Whether depth-1 tumbler extension at account level should be admitted.
**Why out of scope**: Deliberate scope exclusion; deferred to future ASN if the design admits account "version" semantics.

### Topic 4: Non-T10a allocators
Admissibility of allocators that do not conform to T10a's inc discipline.
**Why out of scope**: Would require lifting the GlobalUniqueness chain that closes `e ∉ E`, `a ∉ dom(C)`, `ℓ ∉ dom(L)`; deferred.

### Topic 5: Link-subspace correspondence-run structure
The link-subspace analogue of ASN-0036's S8 correspondence-run partition.
**Why out of scope**: ASN explicitly defers this to a downstream link-operations ASN with documented Nelson/Gregory evidence for the deferral.

VERDICT: REVISE
