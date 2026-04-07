# Review of ASN-0047

## REVISE

### Issue 1: J2/J3 formal statements are inconsistent with the composite-transition semantics used throughout the section

**ASN-0047, Coupling and isolation**: J2 states `(A Σ → Σ', d : dom(M'(d)) ⊂ dom(M(d)) : C' = C ∧ E' = E ∧ R' = R)`. J3 states the same for reordering.

**Problem**: Throughout this section, `Σ → Σ'` denotes a composite transition (the text defines this explicitly: "A composite transition is an ordered sequence of elementary transitions"). J0 and J1 use `Σ → Σ'` this way — J0 cannot be read as an elementary-transition constraint because K.α alone never places content in an arrangement, and J1 cannot be read that way because K.μ⁺ alone never modifies R.

Read consistently with J0/J1, J2 asserts: for *every composite transition* where some document's arrangement contracts, C, E, and R are unchanged. This is false. A composite transition that contracts d₁'s arrangement (K.μ⁻) while inserting new content into d₂ (K.α + K.μ⁺ + K.ρ) satisfies the antecedent `dom(M'(d₁)) ⊂ dom(M(d₁))` but violates the consequent `C' = C` (K.α grew C) and `R' = R` (K.ρ grew R).

The wp derivations for J2/J3 clearly analyze the elementary transitions K.μ⁻ and K.μ~ — they say "K.μ⁻ does not touch C," not "no composite containing K.μ⁻ touches C." The intent is that K.μ⁻ and K.μ~ *need no coupling* — they are self-sufficient. This is correct and follows from their frame conditions. But the formal statements assert a stronger, false universal.

**Required**: Restate J2 and J3 as properties of the elementary transitions K.μ⁻ and K.μ~, not as universal constraints on composite transitions. One option: "K.μ⁻ requires no coupling: as an elementary transition it satisfies C' = C ∧ E' = E ∧ R' = R. The wp analysis confirms that no co-occurring transition is needed to maintain P0–P2 or Contains(Σ) ⊆ R." This distinguishes "doesn't need coupling" (true, the actual claim) from "forbids co-occurrence with other changes" (false, what the formal statement says).

### Issue 2: Worked example S8-depth verification is vacuous

**ASN-0047, Worked example (fork step)**: "The V-positions [1] and [2] satisfy S8a (positive components) and S8-depth (uniform depth 1)."

**ASN-0047, Worked example (insert step)**: "V-position [3] has depth 1, matching [1] and [2] (S8-depth)."

**Problem**: S8-depth (ASN-0036) requires uniform depth for V-positions *with the same first component*: `(v₁)₁ = (v₂)₁ ⟹ #v₁ = #v₂`. For single-component V-positions [1], [2], [3], the first components are 1, 2, 3 respectively — all distinct. The antecedent `(v₁)₁ = (v₂)₁` is never satisfied for any pair, so S8-depth holds vacuously regardless of depth. The claim that S8-depth is verified "by depth matching" is misleading — the constraint imposes no requirement on these positions.

The deeper issue: single-component V-positions place each position in its own "subspace" under S8-depth's grouping, making S8-depth trivially satisfied for any collection of such positions. The worked example does not exercise S8-depth at all.

**Required**: Either (a) use multi-component V-positions where S8-depth is non-vacuous — e.g., `[1, 1]`, `[1, 2]`, `[1, 3]` with shared first component 1 (text subspace), giving depth 2 uniformly — and adjust the I-address arithmetic accordingly, or (b) note explicitly that S8-depth is vacuously satisfied for single-component V-positions and that the meaningful constraint in this example is S8a alone.

## OUT_OF_SCOPE

No items. The ASN's scope is well-drawn and the open questions correctly identify deferred topics (fork arrangement constraints, version lineage, transitive transclusion provenance, link discoverability after contraction).

VERDICT: REVISE
