# Review of ASN-0040

## REVISE

### Issue 1: B6 necessity proof does not cover the zero-count T4 violation
**ASN-0040, B6 (⟹) Necessity, sub-case (a)**: "By TA5(b), inc(p, d) preserves positions 1 through #p, so each defective position of p survives unchanged into c₁ at the same index... every stream element carries the defect."
**Problem**: The partition routes any non-trailing-zero T4 violation into sub-case (a), described as "a defect at position 1 (leading zero) or some interior position (adjacent zeros or other interior violation)." But T4 also fails when `zeros(p) > 3` with no positional/boundary defect — e.g. `p = [1,0,1,0,1,0,1,0,1]` (four non-adjacent interior zeros, `p₁ = p_{#p} = 1`). No single position is "defective" here, so the stated propagation mechanism ("each defective position survives") does not apply. The correct argument is different: TA5(b) preserves the interior zeros, so `zeros(c₁) ≥ zeros(p) > 3` (strictly greater at d = 2), violating T4's `zeros(t) ≤ 3` clause. The proof never states this. The only worked example is a leading zero, so the count-only case is genuinely unshown, and "other interior violation" mischaracterizes a global count as a positional defect.
**Required**: Add an explicit clause to sub-case (a) handling `zeros(p) > 3`: position preservation (TA5(b)) carries the zero count into c₁ undiminished, so `zeros(c₁) ≥ zeros(p) > 3`; sibling increments add no zeros (B5a), so every stream element exceeds the budget. Then the partition is exhaustive over all four T4 clauses.

### Issue 2: Defensive meta-prose and document-ordering justification in B6 necessity
**ASN-0040, B6 Necessity**: "*Disjointness motivation — trailing-zero parents at d = 1 (not a step of the T4-necessity proof).*" and earlier "For T4-necessity the load-bearing case is d = 2, treated immediately below; the d = 1 case is handled afterward as a separate disjointness motivation."
**Problem**: The disjointness content (S2-based namespace injectivity) advances reasoning, but its framing is reviser-drift the anti-bloat classifier targets: a roadmap sentence inside the proof pointing forward two paragraphs, then a paragraph header whose parenthetical "(not a step of the T4-necessity proof)" justifies its own placement, repeated in the closing line. A reader must skip past these disclaimers to follow the necessity argument. This is "prose justifies document ordering" plus a forward pointer to a downstream location in the same proof.
**Required**: Lift the trailing-zero/S2 injectivity material out of the necessity proof into its own short claim or remark adjacent to S2, and delete the two placement disclaimers and the roadmap sentence. The necessity proof should then state only condition (i)–(iii) necessity.

### Issue 3: Bop well-definedness re-derives NextAddress; B0b carries a structural-justification sentence
**ASN-0040, Bop (Well-definedness)**: "whose Justification of well-definedness (NextAddress) already establishes next(s.B, p, d) ∈ T ... — the empty branch yielding inc(p, d) ∈ T and the non-empty branch yielding inc(max(children(s.B, p, d)), 0) ∈ T."
**Problem**: This re-enumerates both conditional branches that NextAddress's own justification already proved — two paragraphs saying the same thing. Citing NextAddress and discharging only the finiteness premise (via B_fin) suffices. Separately, **B0b**'s lead sentence ("which we isolate once here so each proof presents only its own per-invariant argument") justifies why the corollary exists rather than stating it; the corollary is useful, the framing sentence is not.
**Required**: In Bop, replace the branch re-enumeration with a one-line citation of NextAddress plus the B_fin finiteness discharge. Drop B0b's structural-justification clause.

## OUT_OF_SCOPE

### Topic 1: Content storage (Occupied predicate)
B3 introduces `Occupied` only as a forward requirement constraining future content-storage ASNs, and ghost elements are intrinsic to baptism. This is the correct way to handle the baptism/content boundary — not flagged as an error or as improper scope creep.

VERDICT: REVISE
