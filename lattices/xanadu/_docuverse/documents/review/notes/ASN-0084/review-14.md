# Review of ASN-0084

## REVISE

### Issue 1: "Canonical decomposition" used without definition
**ASN-0084, Worked Examples (both)**: "The canonical decomposition has two blocks", "The new canonical decomposition has four blocks", "Canonical decomposition: {…}"
**Problem**: The term "canonical decomposition" appears six times across both worked examples but is never defined. In context it means the maximally merged block decomposition — the partition into maximal correspondence runs where no two V-adjacent, I-adjacent blocks remain unmerged. Uniqueness of this decomposition (each V-position belongs to exactly one maximal run, and maximal runs are either identical or disjoint) is relied upon implicitly but not established.
**Required**: Either (a) add a definition: "The *canonical block decomposition* is the unique decomposition into maximal correspondence runs — blocks where no two V-adjacent and I-adjacent blocks remain unmerged. Uniqueness follows from the arrangement being a function: each V-position has a unique maximal run containing it, determined by extending the run in both directions until the correspondence condition M(d)(v + k) = a + k fails." Or (b) replace "canonical decomposition" with "the block decomposition" in the worked examples and drop the uniqueness claim.

## OUT_OF_SCOPE

### Topic 1: Generalization to arbitrary V-position depth
**Why out of scope**: The ASN explicitly restricts to depth-2 V-positions and correctly notes the generalization is structurally identical by D-CTG-depth. Proving the generalization belongs in a future ASN or a revision that lifts the depth-2 restriction. The current treatment is internally consistent.

### Topic 2: Composition of rearrangements
**Why out of scope**: Whether the composition of two cut-point rearrangements is expressible as a single rearrangement is a natural next question (noted in Open Questions) but is new territory — no claim about composition appears in this ASN.

### Topic 3: Block count bounds after rearrangement
**Why out of scope**: R-BLK establishes that a valid decomposition exists after rearrangement but deliberately does not bound the block count change. The open question about increase conditions is appropriate for a future ASN that characterizes the complexity of rearrangement.

VERDICT: REVISE
