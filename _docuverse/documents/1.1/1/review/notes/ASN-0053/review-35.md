# Review of ASN-0053

## REVISE

### Issue 1: "Denotation, not encoding" section is scope-defense essay that drifts out of scope

**ASN-0053, "Denotation, not encoding"**: "a V-dimension width of 11 characters may appear as [0, 11] (action point at position 2) while the corresponding I-dimension width appears as [0,0,0,0,0,0,0,0,11] (action point at position 9). Both denote the same advance".

**Problem**: Three faults compound here. (a) The section is a defensive justification ("the properties above quantify over ⟦σ⟧, so they are blind to this distinction") — meta-prose explaining what the algebra does *not* govern, not advancing any claim. (b) It invokes the V-dimension/I-dimension distinction, which is explicitly OUT OF SCOPE (I-space/V-space distinction). (c) The substantive assertion is imprecise: [0,11] acts at depth 2 and [0,…,11] acts at depth 9; they apply to starts of different lengths and are not level-uniform within one span. Calling them "the same advance" has no meaning inside this algebra, which requires level-uniformity for displacement recovery.

**Required**: Delete the section, or reduce to a one-line statement that span properties quantify over denotations and are insensitive to width tumbler-length, without the V/I example.

### Issue 2: S2's ghost-element discussion is content-layer essay the ASN itself declares out of scope

**ASN-0053, S2 (EmptyDistinction)**: the three-row populated/unpopulated/empty table and the "ghost elements" Nelson quotes, followed by "Whether a span's positions are populated is a content-layer concern, outside this algebra."

**Problem**: The substantive claim of S2 is one sentence — the empty set is not a span, so an empty intersection is the absence of a span, not a zero-width span. The surrounding paragraph and table elaborate the populated-vs-unpopulated distinction, then concede it is a content-layer concern outside the algebra. That is essay content about an admittedly out-of-scope topic occupying a structural slot.

**Required**: Keep the empty-set-is-not-a-span statement and its TA-strict justification. Drop the ghost-element table and populated/unpopulated digression.

### Issue 3: Repeated "load-bearing" defensive assertions

**ASN-0053, intro / S6 / S4a**: "The algebra is not merely convenient — it is load-bearing." (intro); "The level constraint is load-bearing." (S6); "The level-uniformity constraint is 'load-bearing'." (S4a).

**Problem**: The same defensive flourish appears three times across sections, asserting importance rather than advancing reasoning. This is the kind of meta-prose that compounds across cycles.

**Required**: Retain at most one, attached to where the constraint actually does work (S4a's exactness argument), and state the consequence, not the adjective.

### Issue 4: WR is listed as an introduced property but never stated as one

**ASN-0053, Properties Introduced table**: "WR | Width recovery (span-level consequence)… derived here from DisplacementUnique (D2, ASN-0034) | introduced".

**Problem**: The body derives `reach(σ) ⊖ start(σ) = width(σ)` in prose under "The reach function" but never gives it a labeled contract/claim block. The table promotes it to a named introduced property "WR" that has no formal statement, unlike S0–S11. Either it is a property (label it) or it is inline derivation (drop the table row).

**Required**: Add a labeled WR claim block with preconditions/postcondition, or remove WR from the table and keep the derivation inline.

### Issue 5: S6's divergence example is imprecise and imagines a precondition-excluded case

**ASN-0053, S6**: "An interior point at a deeper level, such as [1, 3, 0, 1] relative to start [1, 3], diverges at position 3 (after zero-padding)".

**Problem**: The ordinary `divergence([1,3],[1,3,0,1])` is 3 (prefix case, min+1). But the *zero-padded* comparison ([1,3,0,0] vs [1,3,0,1]) first disagrees at position 4, not 3 — so "(after zero-padding)… position 3" is internally inconsistent. Separately, S6's carrier already requires `level_compat(s, p)`, so a deeper-level point is excluded by precondition; the paragraph illustrates a case the claim cannot reach.

**Required**: Drop the parenthetical "(after zero-padding)" (the relevant quantity is ordinary divergence vs #s), and either trim the deeper-level illustration or mark it explicitly as motivating the precondition rather than a case of the claim.

### Issue 6: S4 cites an out-of-scope operation as a downstream consumer

**ASN-0053, S4 (SplitPartition)**: "The REARRANGE operation's three-cut semantics depend on this: 'cut 2 is simultaneously the boundary of both regions…' (Q2)."

**Problem**: REARRANGE (operations and their effects on spans) is OUT OF SCOPE. This sentence is a use-site/downstream-consumer justification for S4, not content advancing the partition claim.

**Required**: Remove the REARRANGE reference; the partition is justified by the total order alone.

## OUT_OF_SCOPE

### Topic 1: Span-set difference bound and cross-level intersection
The tight bound on `|normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)|` and well-formed representation of intersections across hierarchical levels are genuine future work — and already correctly parked in Open Questions. No action needed; flagged only to confirm their absence from the proved claims is not a defect.

VERDICT: REVISE
