# Review of ASN-0111

## REVISE

### Issue 1: RL4 witness construction leaves the extension step's enablement undischarged
**ASN-0111, "Faithful disclosure of nesting" (RL4 witness paragraph)**: "This step's precondition consults only `dom(L)` (the frontier maximum) and `dom(M)`, on which the branches agree, so it is enabled identically in both"
**Problem**: K.λ's precondition (ASN-0093) has a third conjunct beyond the home and binding clauses: the value-shape condition `N ≥ 3 ∧ (A i : eᵢ ∈ Endset) ∧ e₃ ≠ ∅`. The same paragraph acknowledges this two sentences earlier for the branching values ("K.λ's precondition constrains the value only through L3, never through its content"), then drops it for `ℓ_c`. As specified, `ℓ_c` is pinned down only by its slot-2 endset `{(a', δ(1, #a'))}`; nothing in the construction gives it a non-empty type slot. If `ℓ_c.e₃ = ∅`, the extension step is disabled in *both* branches and the witnessing pair `(Σ₁, Σ₂)` does not exist. The identical-enablement conclusion would survive (the value is shared across branches), but existence of the step is undischarged, and the quoted sentence is false as a statement of K.λ's precondition. The worked example's parenthetical `(∅, G_c, Θ)` discharges it for the instance, but the abstract construction must stand on its own.
**Required**: Specify `ℓ_c` as an L3-conforming triple — e.g. `ℓ_c = (∅, {(a', δ(1, #a'))}, Θ₀)` with `Θ₀ ≠ ∅` — and restate the sentence: the *state-dependent* conjuncts of K.λ's precondition consult only `dom(L)` and `dom(M)`, on which the branches agree; the value-shape conjunct is branch-independent and discharged by `ℓ_c`'s form.

### Issue 2: The "exactly one attainable" claim in RL0 is supported by a fact too weak to deliver it
**ASN-0111, "Deriving the read" (paragraph after RL0's wp display)**: "at each `(a, Σ)` exactly one of them is attainable: by the definition, every invocation returns either the stored value entire or `⊥` — `readlink(a, Σ) ∈ {Σ.L(a), ⊥}` when `a ∈ dom(Σ.L)`, and `readlink(a, Σ) = ⊥` otherwise."
**Problem**: To establish that "result = ⊥" is *unattainable* on the success branch, the argument needs `readlink(a, Σ) = Σ.L(a)` there — which the definition gives directly, and which RL0's biconditional (`readlink(a, Σ) = ⊥ ⟺ a ∉ dom(Σ.L)`) asserts one display earlier. The disjunction `∈ {Σ.L(a), ⊥}` offered as the support leaves `⊥` attainable on allocated addresses, i.e. it fails to support the exclusivity it is cited for, and on its face contradicts the adjacent biconditional's spirit. The displayed justification is wrong-shaped even though the conclusion is true.
**Required**: Cite the equality (`readlink(a, Σ) = Σ.L(a)` when `a ∈ dom(Σ.L)`) or the RL0 biconditionals as the support for exclusivity. The no-partial-success observation (the operation never returns a proper sub-value, though such fragments inhabit the codomain) can then stand separately as it does.

### Issue 3: The cross-reference to the worked example overstates what it instantiates
**ASN-0111, "Faithful disclosure of nesting" (closing parenthetical)**: "(The worked read below instantiates exactly this pair: `a' = inc(a, 0)` and `c = inc(a', 0)` on `d₁`'s link sub-allocator.)"
**Problem**: "This pair" in the RL4 paragraph is the *state* pair `Σ₁, Σ₂` — two branched histories agreeing at `c` and disagreeing at `a'`. The worked nested instance exhibits a single state `Σ`, never assigns `Σ.L(a')` any value at all, and verifies the unflattened-disclosure corollary (the read returns `G_c` with `a'` as an address). It instantiates the address pattern, not the two-state witness. As written, the parenthetical claims a verification the worked example does not perform.
**Required**: Either reword the parenthetical to say the worked example instantiates the address scaffolding and the corollary, or extend the worked example to actually exhibit the two branched states with `v₁ ≠ v₂` at `a'`.

### Issue 4: Forward-deferral and deduplication meta-prose around the structural screen
**ASN-0111, "Deriving the read" and the screen paragraph**: "The deciding observation is the insufficiency of address-only tests, stated and discharged once with the structural screen following RL0: …"; "The structural screen now does its honest work; we state it, with its necessity and its insufficiency, once here."; "Two separate facts now carry the section."
**Problem**: Two paragraphs in different sections point at the same downstream location, and both insist the argument appears "once" — this is document-organization justification, not specification content. "Does its honest work" and "Two separate facts now carry the section" are sectional commentary the reader must skip past to reach the screen itself. The substantive material (the four conjuncts, their per-conjunct necessity citations, the left-to-right evaluability guard, the `Σ₀` insufficiency witness) is all present and is what should carry these paragraphs.
**Required**: In "Deriving the read," keep the insufficiency fact (already stated after the colon) and delete the locational clause "stated and discharged once with the structural screen following RL0." In the screen paragraph, delete the "honest work"/"once here" framing and the "Two separate facts now carry the section" sentence; lead directly with the screen, its necessity, and the `Σ₀` witness.

## OUT_OF_SCOPE

### Topic 1: Protocol-level encoding of the `⊥` result and of returned link values
**Why out of scope**: The note cites Gregory's distinguished failure reply as evidence for totality, but the wire representation of `⊥` and of returned endset structure belongs to the inter-server protocol (BEBE), which is explicitly outside this ASN's scope.

VERDICT: REVISE
