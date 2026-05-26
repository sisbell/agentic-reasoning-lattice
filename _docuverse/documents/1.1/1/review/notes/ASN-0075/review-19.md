# Review of ASN-0075

## REVISE

### Issue 1: D-ACT bijection argument elides a non-trivial step

**ASN-0075, D-ACT, witness-run partition proof**: "by the no-intermediate-content lemma proved below, any T1-consecutive pair of same-origin addresses in dom(C) is shift-adjacent, so within each class consecutive elements (under T1) are shift-adjacent"

**Problem**: The "so" performs multi-step work without showing it. The lemma establishes that consecutive `A_C(d)` emissions are T1-consecutive *in dom(C)*. The conclusion concerns T1-consecutiveness *within C* (a subset of dom(C)) — a different and weaker relation, because intermediate dom(C) elements outside C may exist between two C-members. The bridge requires:

1. Sequential emission of `A_C(d)`: all indices `1, …, k` are in `dom(C)` once index `k` is emitted (from T10a, `inc(·, 0)`-only sibling stream).
2. I-adjacency path-connectivity: for `a, a' ∈ C` connected by I-adjacency path through deletion set, the path must traverse every index in `[index(a), index(a')]` (paths in shift-±1 graphs cover convex closures); if some intermediate index is not in deletion set, the path is blocked.
3. Therefore class members have contiguous indices, and T1-consecutive elements within a class are shift-adjacent.

Without this chain, the reader cannot derive the conclusion from the lemma alone. "T1-consecutive in dom(C) → shift-adjacent" (the lemma's converse) does not entail "T1-consecutive in C → shift-adjacent" by direct substitution.

**Required**: Either expand the implicit path-based argument (showing that an index gap in C breaks I-adjacency connectivity, forcing each class to occupy a contiguous index range), or restructure the argument: first prove "I-adjacency classes have contiguous indices within their allocator's stream" directly from I-adjacency closure plus shift-±1 path structure; then conclude "consecutive indices ⟹ shift-adjacent" trivially; then the forward-then-inverse composition of the bijection is immediate.

## OUT_OF_SCOPE

### Topic 1: Restoration operation specification

**Why out of scope**: The ASN mentions restoration as a downstream consumer of SHOWDELETIONS output (D-ACT, "Composability with Restoration") but appropriately does not specify the restoration operation itself. The transitions K.μ⁺ already exist for arrangement extension, and a formal restoration operation that consumes deletion witness runs is a separate concern.

### Topic 2: Multi-document and concurrent SHOWDELETIONS

**Why out of scope**: Listed as open questions. The binary, sequential operation is fully specified; n-ary generalizations and concurrency models belong in future work.

VERDICT: REVISE
