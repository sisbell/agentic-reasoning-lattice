# Review of ASN-0053

## REVISE

### Issue 1: Width-recovery identity is load-bearing but unnamed, and mislabeled in the merge-split argument

**ASN-0053, "The reach function"**: "reach(σ) ⊖ start(σ) = width(σ)       (level-uniform spans)"

**ASN-0053, paragraph after S5**: "The merged width is reach(σ) ⊖ s = ℓ, by D1 applied to σ (level-uniformity gives #s = #reach(σ))."

**Problem**: The width-recovery identity is proved by direct component-by-component construction in the "reach function" section but given no label. It is then cited as "by D1" in the merge-split inverse argument. D1 establishes `s ⊕ (reach(σ) ⊖ s) = reach(σ)` — not `reach(σ) ⊖ s = ℓ`. To bridge from D1's conclusion (`s ⊕ (reach ⊖ s) = s ⊕ ℓ`) to the needed claim (`reach ⊖ s = ℓ`) requires either LeftCancellation (proved later in the ASN) or the direct width-recovery computation (proved earlier). Neither is cited. A reader following only the stated reference reaches `s ⊕ x = s ⊕ ℓ` and has no stated justification for stripping the `s`.

The properties table lists `σ.reach` (start ⊕ width → reach) but not the reverse direction (reach ⊖ start → width). The forward direction has a name; the inverse does not.

**Required**: Name the width-recovery identity (natural label: D2 or a corollary of D1 + LeftCancellation). In the merge-split inverse argument, cite it correctly. The identity is the mechanism by which start-and-reach determines width — the second of the "two of three pairings" the ASN discusses — and downstream ASNs that construct spans from endpoint pairs will depend on it.

### Issue 2: Merge-split inverse is a key structural result with no property label

**ASN-0053, paragraph after S5**: "So γ = (s, ℓ) = σ — the original span is recovered exactly."

**Problem**: The paragraph after S5 establishes that splitting σ at p and merging the two parts recovers σ identically. This is the fundamental round-trip guarantee of the algebra — it shows S3 (merge), S4 (split), S5 (width composition), and the width-recovery identity form a coherent system. Yet the result has no property label and does not appear in the "Properties Introduced" table. The converse direction (merge two adjacent spans, then split at the original boundary, recovering the original pair) is implicit but also unnamed.

A downstream ASN that needs to assert "rearranging spans in V-space preserves span-set denotation" would have no label to cite for the fact that split-then-merge is lossless.

**Required**: Name the split-merge round-trip as a property (e.g., S4a — SplitMergeInverse) and include it in the properties table. State the preconditions explicitly: level-uniform span σ, level-compatible interior point p.

## OUT_OF_SCOPE

### Topic 1: LeftCancellation belongs in ASN-0034
**Why out of scope**: The lemma is purely about tumbler addition — it makes no reference to spans. It is correctly proved locally as a dependency for S5. Promoting it to ASN-0034 in a future revision would let downstream ASNs cite a tumbler-arithmetic fact from the tumbler algebra, rather than from the span algebra.

### Topic 2: Span operations across hierarchical levels
**Why out of scope**: S6 restricts all non-trivial operations to same-depth operands. Operations involving spans at different depths would require a theory of cross-level displacement. The ASN correctly identifies this as open.

### Topic 3: Span-set intersection and general difference
**Why out of scope**: S1 gives single-span intersection; S11 gives single-span containment difference. Generalizing to arbitrary span-set intersection and span-set difference follows from combining these primitives with S8 normalization, but the explicit construction and proof belong in a future ASN.

VERDICT: REVISE
