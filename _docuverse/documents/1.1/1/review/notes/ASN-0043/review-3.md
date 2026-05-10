# Review of ASN-0043

## REVISE

### Issue 1: Structural attribution gap — missing S7a analog for link addresses

**ASN-0043, Home and Ownership**: "A link at address `a` lives under the document prefix `home(a)`, which identifies who created it and where it resides, by the same structural attribution that governs content (S7, ASN-0036)."

**Problem**: S7 (ASN-0036) derives from S7a (DocumentScopedAllocation), which states: "Every I-space address is allocated under the tumbler prefix of the document that created it. That is, for every `a ∈ dom(Σ.C)`, the document-level prefix of `a` ... identifies the document whose owner performed the allocation that placed `a` into `dom(C)`." S7a applies exclusively to `dom(Σ.C)` — content addresses. No analogous property exists for `dom(Σ.L)`. The `home` function correctly extracts the document prefix from any element-level tumbler (by L1 + T4), but the claim that this prefix identifies the *creating* document — the ownership claim — requires that link addresses are allocated under the creating document's prefix. This allocation relationship is assumed but not stated. Without it, `home(a)` is a well-defined function with no established connection to ownership.

**Required**: Either (a) state a link analog of S7a — e.g., "L1a — LinkScopedAllocation: Every link address is allocated under the tumbler prefix of the document whose owner created it: `(A a ∈ dom(Σ.L) :: origin(a)` identifies the allocating document)" — or (b) derive a link-level analog of S7 from existing properties, showing the derivation chain explicitly, or (c) present the ownership interpretation as a definitional commitment rather than a derivation from S7.

### Issue 2: L11 formal statement — "distinct links" is undefined

**ASN-0043, Link Distinctness and Permanence**: "`(A a₁, a₂ ∈ dom(Σ.L) :: a₁ ≠ a₂ ⟹ Σ.L(a₁) and Σ.L(a₂) are distinct links)`"

**Problem**: "Distinct links" is not defined. The natural mathematical reading of "Σ.L(a₁) and Σ.L(a₂) are distinct" is value-distinctness: `Σ.L(a₁) ≠ Σ.L(a₂)`. But this is NOT what L11 means — L11 means entity-distinctness: two links at different addresses are separate objects *regardless of whether their values coincide*. The prose paragraph clarifies correctly ("Two links with identical endsets ... but different addresses are separate objects"), but the formal statement is ambiguous. Compare with S4 (OriginBasedIdentity, ASN-0036), which states the analogous property for content clearly: "For I-addresses `a₁, a₂` produced by distinct allocation events: `a₁ ≠ a₂` regardless of whether `Σ.C(a₁) = Σ.C(a₂)`." L11 should follow S4's pattern.

**Required**: Restate L11 to make the identity-vs-value distinction explicit. For example: "Link identity is address identity: for link addresses `a₁, a₂ ∈ dom(Σ.L)` produced by distinct allocation events, `a₁ ≠ a₂` regardless of whether `Σ.L(a₁) = Σ.L(a₂)`. The link store is not necessarily injective — multiple addresses may store the same triple of endsets."

### Issue 3: L9 formal statement — permission stated as negated invariant

**ASN-0043, The Type Endset**: "`¬ [(A a ∈ dom(Σ.L), (s, ℓ) ∈ Σ.L(a).type :: coverage({(s, ℓ)}) ⊆ dom(Σ.C))]`"

**Problem**: Every other labeled property in L0–L14 is a universal invariant (holds in all reachable states). L9 is formatted identically but is logically different: it is a negated universal, which in classical logic is an existential (`∃ a, (s,ℓ) such that coverage ⊄ dom(Σ.C)`). Read as a state-level property, this would assert that in *every* reachable state, *some* type span references a non-content address — meaning ghost types would be mandatory, not merely permitted. The intended reading is that the specification does not impose the negated universal as an invariant — ghost types are *permitted*. But the quantifier structure does not distinguish "the specification does not require X" from "every state violates X." Compare with S5 (UnrestrictedSharing, ASN-0036), which expresses a similar permission as an explicit existential with witnesses: "`(A N ∈ ℕ :: (E Σ :: Σ satisfies S0–S3 ∧ ...))`".

**Required**: Reformulate L9 as an explicit permission or existential with a witness. For example: "For any conforming state Σ satisfying L0–L14 and S0–S3: (a) a state Σ' extending Σ with a link whose type endset references an address outside `dom(Σ'.C) ∪ dom(Σ'.L)` is also conforming, and (b) no property of this ASN requires `coverage(Σ.L(a).type) ⊆ dom(Σ.C)`." Alternatively, a witness construction in the pattern of S5.

### Issue 4: No concrete example

**ASN-0043, throughout**

**Problem**: The ASN cites implementation evidence extensively (MARGIN at 1.0.2.6.2, V-addresses 1.1/2.1/3.1, GRANTEXT/GRANORGL constants) but does not construct a specification-level example state — a specific `Σ = (Σ.C, Σ.M, Σ.L)` with specific tumbler addresses — and verify that L0–L14 hold simultaneously. A worked example would verify joint satisfiability and catch implicit contradictions between properties.

**Required**: Construct a minimal example state with at least one content item and one link (with specific tumbler addresses for start, length, and endset spans), and verify each of L0, L1, L3, L4, L5, L6, L11, L12, L14 against it. For L10, the existing MARGIN/FOOTNOTE example is close but should use the ASN's own definitions (coverage, span arithmetic) rather than implementation-level addresses.

## OUT_OF_SCOPE

### Topic 1: Link operations and their postconditions
**Why out of scope**: MAKELINK, FOLLOWLINK, REMOVELINK are operations that transform system state. This ASN defines link ontology (what links ARE), not link dynamics (what operations do to links). The ASN's scope exclusion lists these explicitly.

### Topic 2: Link survivability under editing operations
**Why out of scope**: Whether links survive INSERT, DELETE, COPY, REARRANGE operations on content they reference is a case analysis over operations applied to state containing both Σ.M and Σ.L. The ontological properties (L4: endsets reference I-space; L12: links are immutable) establish the structural preconditions for survivability, but the case analysis belongs in the operations ASN.

### Topic 3: Compound link well-formedness
**Why out of scope**: L13 establishes that link-to-link references are structurally possible and sketches the composition mechanism (three-endset links as CONS cells). What constraints govern chains of such references — acyclicity, depth bounds, type consistency — is new territory requiring its own treatment, correctly identified in the ASN's open questions.

VERDICT: REVISE
