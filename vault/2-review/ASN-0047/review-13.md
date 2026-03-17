# Review of ASN-0047

## REVISE

### Issue 1: Contains(Σ) used before definition in the valid composite definition
**ASN-0047, Coupling and isolation, Definition (Valid composite transition)**: "the final state Σ' satisfies P6, P7, P8, S2, S3, S8a, S8-depth, S8-fin, and Contains(Σ') ⊆ R'"
**Problem**: Contains(Σ) is first defined several paragraphs later, inside the J1 derivation: "Define the *current containment*: Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}." The valid composite definition is the central structural device of the ASN; every term it uses must be available to the reader at point of use. A forward reference in a foundational definition is not acceptable at this level of rigor.
**Required**: Move the definition of Contains(Σ) to before the valid composite definition — either into the state model section (it is a derived quantity of the state, not specific to coupling) or immediately before the valid composite definition with a brief motivation.

### Issue 2: K.μ~ decomposition fails on empty arrangements
**ASN-0047, Elementary transitions, K.μ~**: "It decomposes into K.μ⁻ (removing all mappings) followed by K.μ⁺ (re-adding them at new positions)."
**Problem**: K.μ⁻ requires dom(M'(d)) ⊂ dom(M(d)) — a strict subset, which requires at least one element to remove. K.μ⁺ requires dom(M'(d)) ⊃ dom(M(d)) — a strict superset. When dom(M(d)) = ∅, neither can fire: there is nothing to remove and nothing to re-add. Yet K.μ~ on an empty arrangement is well-defined — the empty bijection π : ∅ → ∅ satisfies the definition, producing the identity. The decomposition claim as stated is false for this boundary case.
**Required**: Qualify the decomposition: "When dom(M(d)) is non-empty, K.μ~ decomposes into K.μ⁻ followed by K.μ⁺. When dom(M(d)) = ∅, K.μ~ is the identity — zero elementary steps." This preserves the completeness argument (the five primitives plus the empty composition cover all cases).

### Issue 3: J1 and J1' quantifier domain unbound
**ASN-0047, Coupling and isolation, J1**: "(A Σ → Σ', d, a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')"
**ASN-0047, Coupling and isolation, J1'**: "(A Σ → Σ', a, d : (a, d) ∈ R' \ R : a ∈ ran(M'(d)) \ ran(M(d)))"
**Problem**: Both formulas universally quantify over d without restricting it. M' is defined as M' : E'\_doc → (T ⇀ T). For d ∉ E'\_doc, M'(d) is undefined — not empty, undefined — making ran(M'(d)) ill-formed. The prose two paragraphs earlier declares "The coupling constraints below quantify over E'\_doc, not E\_doc," but the formal statements do not carry this restriction. J0 does restrict correctly (it writes "d ∈ E'\_doc" inside its existential). J1 and J1' should do the same for their universal quantifiers. Note that for J1' the restriction is derivable (K.ρ requires d ∈ E\_doc, P1 preserves, so d ∈ E'\_doc), but derivable is not the same as stated — the formula must be well-formed before one can derive anything from it.
**Required**: Add "d ∈ E'\_doc" to the quantifier guard in both J1 and J1'. For J1: "(A Σ → Σ', d ∈ E'\_doc, a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')". Likewise for J1'.

## OUT_OF_SCOPE

### Topic 1: Whether J0 should constrain placement to the origin document
J0 requires every freshly allocated I-address to appear in *some* arrangement, but does not require it to appear in origin(a)'s arrangement. Content allocated under d₁'s prefix could be placed only in d₂'s arrangement. The address structure (S7a) still identifies d₁ as the creator; provenance (J1) still records the placement in d₂. Whether the specification should additionally require a ∈ ran(M'(origin(a))) — "content first appears in its creating document" — is a design question for a future ASN on allocation discipline, not an error here.
**Why out of scope**: J0 captures the minimal constraint (no orphan content). The stronger constraint is a separate policy choice.

### Topic 2: Completeness of the five primitives — formal proof
The completeness argument ("Any modification to a finite partial function decomposes into additions and removals") is a structural observation, not a formal proof. A rigorous treatment would show that every reachable state Σ' from Σ is expressible as a finite composition of K.α, K.δ, K.μ⁺, K.μ⁻, K.ρ satisfying the coupling constraints. The argument is convincing but not machine-checkable.
**Why out of scope**: The structural argument is standard and the claim is not controversial. Formalizing it belongs in the proof layer (Dafny/Alloy), not in a revision of the ASN.

VERDICT: REVISE
