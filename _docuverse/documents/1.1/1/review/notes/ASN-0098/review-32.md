# Review of ASN-0098

## REVISE

### Issue 1: Cross-ASN reference to ASN-0058 (non-foundation)
**ASN-0098, "Boundary and Width Behaviour", parenthetical at start of "Achievability" subsection**: "The action-point identification `k_ℓ = #s` used throughout the case analyses below is therefore a *consequence of the construction's specification* (the canonical construction picks ordinal-displacement spans), not a property derivable from C0 of ASN-0058 (C0 governs well-formed content references, which require additional preconditions not in force here for arbitrary endset spans)."
**Problem**: ASN-0058 is not in the listed foundation set (ASN-0034, ASN-0036, ASN-0043, ASN-0047, ASN-0093). The reference is contrastive and not load-bearing for any proof, but it violates the self-containment standard. The action-point identification is in fact discharged directly from OrdinalDisplacement (ASN-0034), which is foundation.
**Required**: Remove the parenthetical naming ASN-0058 by number, or restate the contrast using only foundation properties (e.g., "not a consequence of generic well-formed-content axioms").

### Issue 2: LP18 omits K.δ-IsDocument from its transition vocabulary
**ASN-0098, "Ghost Projection and Resurrection", LP18**: "the transition sequence may include K.σ (registering a new document), K.μ⁺ or K.μ⁺_L (extending an existing arrangement, possibly via fork), or any other combination of operations that preserves the link store."
**Problem**: LP8 explicitly unifies K.σ (ASN-0093) and K.δ-IsDocument (ASN-0047) as document-registration operations with structurally identical effects on Σ.M. LP18's enumeration mentions only K.σ. A resurrection scenario could legitimately involve K.δ-IsDocument registering a document whose subsequent K.μ⁺ re-introduces a coverage I-address (e.g., via fork composite, where K.δ is the entity-creation step). The "any other combination" clause technically subsumes it, but the asymmetric enumeration suggests K.σ is special, contradicting LP8's unification.
**Required**: Add K.δ-IsDocument alongside K.σ in LP18's transition vocabulary list, or rephrase to "any document-registration operation (LP8) followed by K.μ⁺ or K.μ⁺_L".

## OUT_OF_SCOPE

### Topic 1: Link-canonical companion case to LP12b
**Why out of scope**: ASN-0098 explicitly flags this — for the content-canonical class wp evaluates to false on the n'_{s_C} = 0, n'_{s_L} > 0 retention pattern, but the symmetric link-canonical class (every span canonical with s = [d_s, 0, s_L, k_s]) yields wp value unsettled because LP-Fin Corollary at X = s_L places F-candidates within dom(L)-eligible addresses. The asymmetry is a genuine result, and its full resolution is a natural future-ASN topic.

### Topic 2: Non-canonical span finitude for #ℓ > #s
**Why out of scope**: ASN-0098 explicitly says "the finitude question is not analysed here and is genuinely unsettled by this ASN" for #ℓ > #s. The tightness predicate's definitional canonical-form requirement rejects this regime before quantifier evaluation, so decidability is preserved. A future ASN could investigate whether non-canonical spans with specific structural forms admit finite intersections.

### Topic 3: Reverse-discovery primitive invariants
**Why out of scope**: Listed in Open Questions. A future ASN could specify a primitive that, given a V-position in a document, returns the set of links whose projections contain that V-position, and characterise its invariants.

### Topic 4: V-order preservation across K.μ~
**Why out of scope**: Listed in Open Questions. Whether the V-order of projected positions reflects the I-order of their underlying I-addresses, and under what arrangement-shape conditions this is preserved by K.μ~, is a separate design question.

### Topic 5: Cross-document equivalence of editing trajectories
**Why out of scope**: Listed in Open Questions. The question of whether two documents undergoing "the same" sequence of editing operations must commit to identical projections is a separate semantic question about operation equivalence across documents.

VERDICT: REVISE
