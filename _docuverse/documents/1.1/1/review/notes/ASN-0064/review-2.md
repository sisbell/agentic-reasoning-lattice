# Review of ASN-0064

## REVISE

### Issue 1: Cross-ASN reference to ASN-0067
**ASN-0064, Cross-Document Discovery**: "COPY creates no new content — ASN-0067, C0"
**Problem**: ASN-0067 is not a foundation ASN. Rule 7 requires self-containment except for foundation references.
**Required**: The claim that transclusion preserves I-address identity is derivable from foundations alone: arrangements map V-positions to existing I-addresses (S3, ReferentialIntegrity), and K.μ⁺ (ArrangementExtension, ASN-0047) adds V→I mappings without modifying C (its frame holds C' = C). No content is allocated; no I-addresses are created. Replace the ASN-0067 citation with this derivation from S3 and K.μ⁺.

### Issue 2: FINDLINKS operation return value is ambiguous between F4 and F7
**ASN-0064, Completeness / Visibility**: F4 states "result(Q) = findlinks(Q)"; F7 states "visible(Q, u) = {ℓ ∈ findlinks(Q) : accessible(home(ℓ), u)}"
**Problem**: The ASN defines two distinct output sets — findlinks(Q) (unfiltered) and visible(Q, u) (filtered) — but does not specify which one the FINDLINKS operation returns. F4 equates result(Q) with the unfiltered set. The prose then says "the completeness guarantee applies to the visible result," contradicting the formal F4. The symbol `result(Q)` is introduced in F4 without prior definition, then never reconciled with `visible(Q, u)`. Is the operation parameterized by Q alone or by (Q, u)?
**Required**: Define the operation signature once. Either (a) FINDLINKS takes Q alone and returns findlinks(Q), with visibility filtering as a separate, explicitly defined post-processing step, and the prose about "completeness of the visible result" reformulated as a derived corollary of F4 + F7; or (b) FINDLINKS takes (Q, u) and returns visible(Q, u), with F4 restated accordingly. The user-level completeness guarantee — `(A ℓ : satisfies(ℓ, Q) ∧ accessible(home(ℓ), u) : ℓ ∈ visible(Q, u))` — should be stated and derived explicitly from whichever formulation is chosen.

### Issue 3: F7(b) prose exceeds its formalization
**ASN-0064, Visibility and Access Control**: "No link whose home document is inaccessible appears in the result, **nor is any information about such links revealed**"
**Problem**: The formal property captures only set-membership exclusion: `(A ℓ : ¬accessible(home(ℓ), u) : ℓ ∉ visible(Q, u))`. The stronger claim — that no *information* about inaccessible links is revealed (count, existence, timing) — is an information-flow property that the set-membership formalization does not capture. The prose promises more than the formalism delivers.
**Required**: Either (a) weaken the prose to match the formalization: "No link whose home document is inaccessible appears in the result set," dropping the information-flow claim; or (b) acknowledge explicitly that the information-flow guarantee exceeds what the formal model captures and requires implementation-level assurances (e.g., constant-time filtering, no count disclosure).

### Issue 4: F6 formal statement is not formal
**ASN-0064, Endset Symmetry**: "the mechanism for testing overlaps(Σ.L(ℓ).e₁, Q) is identical to that for overlaps(Σ.L(ℓ).e₂, Q)"
**Problem**: "The mechanism... is identical" is natural language inside a universal quantifier. This is not a formal statement. Moreover, the property is trivially true from the function signature — `overlaps` is defined on `(Endset, Set)` uniformly, so applying it to different endset slots is the same function call by construction. The formal notation adds nothing beyond what the type already guarantees. The substantive claim — that all three endsets must be searchable with *the same performance and completeness guarantees* — is stated in the surrounding prose but not captured by the formula.
**Required**: Either (a) remove the formal notation and state the design commitment in prose (all endsets are equally searchable, with identical completeness and performance guarantees), or (b) formalize the actual content: state that completeness (F4) applies independently to each endset constraint, and that the performance commitment ("QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH") applies equally to from-, to-, and type-constrained queries.

### Issue 5: F1 proof cites S0 for a three-step derivation
**ASN-0064, From Positions to Identity**: "The intersection V(βⱼ) ∩ ⟦σ_V⟧ is contiguous by S0 (Convexity, ASN-0053)."
**Problem**: S0 establishes that a *span denotation* is convex: `(A p, q, r : p ∈ ⟦σ⟧ ∧ r ∈ ⟦σ⟧ ∧ p ≤ q ≤ r : q ∈ ⟦σ⟧)`. This gives the convexity of ⟦σ_V⟧. But the proof requires two additional steps that are not stated: (a) V(βⱼ) = {vⱼ + k : 0 ≤ k < nⱼ} is convex, which follows from the mapping block definition and the fact that ordinal increments produce consecutive tumblers (D-SEQ, ASN-0036); (b) the intersection of two convex sets in a total order is convex, a standard property of total orders that the ASN does not cite or derive. The proof collapses a three-step argument into a single citation.
**Required**: State all three steps: (1) ⟦σ_V⟧ is convex by S0; (2) V(βⱼ) is convex by construction (consecutive ordinal increments from vⱼ); (3) the intersection of two convex sets in a total order is convex.

## OUT_OF_SCOPE

### Topic 1: Version identity and home-set interaction
**Why out of scope**: When a document is versioned, the new version receives a new address. Links created against the old version have `home(ℓ)` equal to the old address. Document-scoped search via the new address misses these links. This interaction — noted in the implementation observations section — is a versioning semantics question. Version creation is excluded from this ASN's scope.

### Topic 2: Integration of Σ.L into the ASN-0047 state model
**Why out of scope**: The link store Σ.L (ASN-0043) is not a component of SystemState Σ = (C, E, M, R) as defined in ASN-0047. The ASN correctly identifies this gap through the LinkEntityCoherence assumption and notes that a link-creation transition (analogous to K.α) is needed. Full integration is a future foundation ASN.

VERDICT: REVISE
