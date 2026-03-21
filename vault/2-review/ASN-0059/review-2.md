# Review of ASN-0059

## REVISE

### Issue 1: I9 proof sketch asserts shifted contiguity without justification

**ASN-0059, Contiguity / I9**: "the shifted region covers [p + n, v_max + n] by I3, since the shift is order-preserving (I6) and injective (I7)"

**Problem**: Order preservation (I6) and injectivity (I7) establish that the shifted set is a set of the correct cardinality with correct min and max, but they do not establish that the shifted set is *contiguous*. An order-preserving injection can map {1, 2, 3} to {5, 7, 9} — preserving order, injective, yet gapped. The missing step is that ordinal shift distributes over ordinal increment: `shift(v + j, n) = shift(v, n) + j`. This identity IS proven in the I10 verification (the paragraph beginning "We verify shift(v, n) + j = shift(v + j, n)"), but I9 does not reference it. Without this fact, the claim that {shift(p, n), shift(p+1, n), ..., shift(v_max, n)} = {p+n, p+n+1, ..., v_max+n} is unsubstantiated.

**Required**: Add one sentence to the I9 argument establishing that shift maps contiguous positions to contiguous positions, by referencing the `shift(v + j, n) = shift(v, n) + j` identity (proven in I10) or deriving it inline from commutativity of ℕ addition at position m.

### Issue 2: P8 (EntityHierarchy) omitted from invariant preservation

**ASN-0059, Invariant Preservation section**: The section checks P0, P1, P2, S0, S2, S3, S8a, S8-depth, S8-fin, P4, P6, P7, P7a — every invariant from ASN-0047's ReachableStateInvariants theorem except P8.

**Problem**: P8 requires `(A e ∈ E : ¬IsNode(e) : parent(e) ∈ E)`. Since `E' = E`, preservation is trivial. But P1 (`E' ⊇ E`) is equally trivial under `E' = E` and IS listed. The omission of P8 — the sole gap in an otherwise complete enumeration — reads as an oversight rather than a deliberate choice.

**Required**: Add P8 to the invariant preservation list with the one-line justification: `E' = E`, so the predicate is unchanged.

## OUT_OF_SCOPE

### Topic 1: Composition of multiple INSERTs
**Why out of scope**: Whether INSERT(d, p₁, vals₁) followed by INSERT(d, p₂, vals₂) commutes (or how p₂ must be adjusted to account for the first insertion's shift) is a property of operation sequencing, not of the single-operation postcondition specified here. This belongs in a future ASN on operation composition or editing sessions.

### Topic 2: INSERT inverse
**Why out of scope**: Whether the pre-INSERT state can be reconstructed from the post-INSERT state (given knowledge of p and n) is a question about reversibility. The DELETE operation (out of scope per the ASN) is the natural candidate for this, not a revision of INSERT.

VERDICT: REVISE
