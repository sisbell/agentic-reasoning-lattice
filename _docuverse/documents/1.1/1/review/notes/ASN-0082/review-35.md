# Review of ASN-0082

## REVISE

### Issue 1: Undefined lemma reference (typo)
**ASN-0082, link-subspace insertion worked example (concluding paragraph)**: "The wp derivation for I3 (specifically the chain I3-VV → S8a) carries through identically at S = 2 as it does at S = 1: it routes through S8a, S8-depth, and TumblerAdd's action-point identity, all of which are subspace-agnostic."
**Problem**: I3-VV is not defined in the ASN body and does not appear in the Statement Registry. The wp chain "→ S8a" identifies the lemma being referenced as the one that establishes S8a preservation under insertion. The Statement Registry entry for the wp-analyzed S8a lemma is I3-VP ("PostInsertionWellFormedness — S8a preserved post-insertion"). The wp analysis in the body section is explicitly framed around I3-VP. None of the other I3-X family labels (VD, S3, S2, fin, S7, S) connect to an "S8a" target. This is a single-character typo.
**Required**: Replace "I3-VV" with "I3-VP" in the cited sentence.

## OUT_OF_SCOPE

The ASN explicitly defers the following follow-on topics; these are appropriate future ASN territory, not gaps in this one.

### Topic 1: Composition of successive shift operations
**Why out of scope**: How multiple INSERTs and DELETEs compose (and how their displacements interact when the inserts/deletes overlap in V-space) is not addressed. This is a separate concern from specifying a single shift correctly.

### Topic 2: Depth > 2 contraction
**Why out of scope**: The depth-2 scoping axiom for contraction is justified via a careful TA4-necessity argument. Deeper-depth contraction would require either a strengthened TA4 (admitting non-zero prefixes when actionPoint = #a) or a fresh derivation using TumblerAdd/TumblerSub primitives directly; the ASN appropriately defers this rather than attempting it.

### Topic 3: Full INSERT operation including content placement
**Why out of scope**: The ASN scopes itself explicitly to the shift sub-operation of INSERT. Content allocation into gap positions, content-store extension, and re-establishment of D-CTG/D-MIN/D-SEQ across the full post-state are deferred to a composing INSERT ASN.

### Topic 4: Spans crossing region boundaries (L/X/R)
**Why out of scope**: D-S addresses level-uniform spans wholly within R. Spans that straddle the contraction range, or that cross L/Q₃ boundaries, would need separate treatment. This is a natural span-algebra extension.

### Topic 5: Link-subspace deletion via tombstoning
**Why out of scope**: The contraction's subspace scoping axiom (S = 1) restricts the operation to text. The ASN flags that link-subspace mutation uses tombstoning instead of shifting, and defers this to a future ASN.

VERDICT: REVISE
