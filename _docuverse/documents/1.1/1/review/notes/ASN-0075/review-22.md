# Review of ASN-0075

## REVISE

### Issue 1: "The deletion set" scope in D-ACT is ambiguous

**ASN-0075, §Actionability**: The witness run definition reads:

> "*Coverage.* Every address in `{i_start, shift(i_start, 1), …, shift(i_start, ℓ − 1)}` (which is `{i_start}` when `ℓ = 1`) belongs to the deletion set;
> ...
> *Right-maximality.* `shift(i_start, ℓ)` is not in the deletion set;
> *Left-maximality.* ... is not in the deletion set."

**Problem**: SHOWDELETIONS returns a pair `(DeletedFromAWithB, DeletedFromBWithA)`, not a single "deletion set." The decomposition is structurally different under the two possible readings:

- *Per-half (intended).* Decompose each half separately. An address `[d.0.s_C.1]` in `DeletedFromAWithB` and `[d.0.s_C.2]` in `DeletedFromBWithA` yield two length-1 runs.
- *Union (literal).* Treat both halves as one deletion set. The same two addresses are I-adjacent (same origin, shift-1 apart) and form a single length-2 run — silently merging two semantically distinct deletions and losing the "deleted-from-which-document" distinction.

The mathematical argument (bijection between I-adjacency equivalence classes and witness runs) is correct for any single set, but the per-half scope is load-bearing for faithful representation of the output.

**Required**: State explicitly that the decomposition applies to `DeletedFromAWithB` and `DeletedFromBWithA` independently (or define what "the deletion set" refers to in this section's scope). One sentence near the definition would resolve it, e.g., "*The deletion set refers to either half of the SHOWDELETIONS output; the decomposition is applied to each half independently to preserve the per-half distinction.*"

## OUT_OF_SCOPE

None — the Open Questions section appropriately defers multi-document generalization, concurrent execution semantics, recovery operation mechanics, and link-subspace deletion comparison to future ASNs.

VERDICT: REVISE
