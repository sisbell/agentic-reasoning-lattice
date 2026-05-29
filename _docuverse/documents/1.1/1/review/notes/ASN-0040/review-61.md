# Review of ASN-0040

## REVISE

### Issue 1: Excess-zero parent not covered by necessity sub-case (a)'s mechanism
**ASN-0040, B6 necessity, sub-case (a)**: "if p violates T4 and the violation is not a pure trailing zero…, then by elimination some defect lies at position 1 (leading zero) or at some interior position 1 < i < #p (adjacent zeros or other interior violation)."
**Problem**: A parent that violates T4 only by `zeros(p) > 3` while having `p₁ > 0`, `p_{#p} > 0`, and no adjacent zeros (e.g. `[1,0,1,0,1,0,1,0,1]`) has no single defective position. Sub-case (a)'s propagation argument is "each defective position of p survives unchanged into c₁" — but here the defect is an *aggregate count*, not localizable to one position. The case enumeration ("defect lies at position 1 or at an interior position") does not classify it, and the "each defective position survives" mechanism does not directly fire. The conclusion still holds (TA5(b) preserves all zeros, so `zeros(c₁) ≥ zeros(p) > 3`), but via a different mechanism than the one written.
**Required**: Add the count-violation configuration explicitly, with the preservation argument `zeros(c₁) ≥ zeros(p) > 3` from TA5(b), rather than folding it under "other interior violation."

### Issue 2: Trailing-zero d=1 exception restated four to five times
**ASN-0040, B6**: The same caveat — "pure trailing-zero parent at d=1 yields a T4-valid stream, excluded for disjointness not T4" — appears in (a) the B6 statement preamble ("One configuration escapes the T4 argument…"), (b) sub-case (b)'s intro ("the d=1 case yields a T4-valid stream and is therefore not a T4-necessity step"), (c) the necessity conclusion ("in every configuration except the pure trailing zero at d=1"), (d) the separate "Disjointness motivation" paragraph, and (e) Postconditions (b).
**Problem**: Reviser drift — multiple paragraphs in different slots saying the same thing. The reader re-reads the same exception five times to follow the argument.
**Required**: State the exception once (in the disjointness-motivation paragraph) and drop the anticipatory restatements in the preamble, sub-case (b) intro, and conclusion.

### Issue 3: "Disjointness motivation" paragraph justifies its own placement
**ASN-0040, B6, disjointness motivation**: "This is design rationale: it presupposes the B6-validity boundary rather than proving it, **which is why it sits outside the necessity proof rather than within it**."
**Problem**: Meta-prose justifying document ordering — explaining where the paragraph sits rather than advancing any claim. The reader does not need the placement rationale; the content stands on its own.
**Required**: Delete the placement justification. Keep the substantive content (S2 identity, namespace collision).

### Issue 4: B6 statement preamble duplicates the necessity proof with same-document forward pointers
**ASN-0040, B6 statement (pre-proof prose)**: "Condition (i) is necessary for T4 preservation by defect propagation… **This is established in the necessity proof's sub-case (a) and in sub-case (b) at d = 2.**"
**Problem**: The preamble previews and partially re-proves what the necessity proof below states in full, then forward-points to it within the same document. This is duplication plus a same-document deferral.
**Required**: Let the proof carry the necessity argument. Trim the preamble to the table and the interpretive reading; remove the sentence-level previews and the "established in sub-case (a)/(b)" pointer.

### Issue 5: Misattributed citation in Bop freshness proof
**ASN-0040, Bop, freshness**: "Therefore a ∉ {c₁, ..., cₘ} = children(s.B, p, d), contradicting the supposition. We conclude a ∉ s.B. **(by B4)**"
**Problem**: Freshness is derived from B1 (contiguous prefix) and S0 (stream ordering / distinct indices), as the preceding sentences show. B4 (atomicity) plays no role in establishing `a ∉ s.B`. The trailing "(by B4)" misattributes the conclusion.
**Required**: Remove "(by B4)" or move it to the read-against-precondition-state claim it actually licenses.

### Issue 6: B0b enumerates its downstream consumers
**ASN-0040, B0b**: "The registry-invariant proofs below — B1, B_fin, B10 — share an induction skeleton… **The three proofs that follow each invoke B0b and argue only the baptismal case.**"
**Problem**: A definition's introduction enumerating its downstream consumers (B1, B_fin, B10). Factoring the shared skeleton is legitimate; the consumer inventory is not — each of B1/B_fin/B10 already cites "by B0b" at use, and the closing sentence ("the three proofs that follow…") adds nothing to B0b's meaning.
**Required**: Keep B0b's statement and the "suffices to (i)/(ii)" reduction; drop the sentence cataloguing which proofs invoke it.

## OUT_OF_SCOPE

### Topic 1: Cross-branch (incomparable-reachability) uniqueness
**Why out of scope**: B8 explicitly scopes itself to co-reachable acts and flags cross-branch uniqueness as unaddressed; the open questions and the scope list (replication / inter-server protocol, BEBE) place concurrent cross-replica baptism in a future ASN. The honest scoping is correct, not a defect — two baptisms on incomparable branches are never jointly observed in one execution.

### Topic 2: Occupied predicate / content storage (B3)
**Why out of scope**: Content storage and retrieval are explicitly out of scope. B3 correctly states the baptism-side constraint as a *forward requirement* on a future content ASN rather than defining storage itself, so it stays inside this ASN's remit (ghost elements are intrinsic to baptism). No revision needed.

VERDICT: REVISE
