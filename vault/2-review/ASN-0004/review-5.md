# Review of ASN-0004

## REVISE

### Issue 1: P0 derivation is circular as stated
**ASN-0004, "The permanence context"**: "P0 follows from S1 (I-space immutability) together with the append-only property of I-space: addresses can be added to `dom.ispace` but never removed."
**Problem**: The "append-only property" described after the colon — addresses can be added but never removed — IS P0. The sentence reads "P0 follows from S1 together with P0." The correct derivation exists but is unstated: S1 requires `ispace'.a = ispace.a` for all `a ∈ dom.ispace`; if `a ∉ dom.ispace'`, then `ispace'.a` is undefined (partial function), making the equation false and violating S1; therefore `dom.ispace ⊆ dom.ispace'`. This is a two-step argument through partial function semantics. The ASN skips it and substitutes the conclusion as a premise.
**Required**: Either make the partial function argument explicit (2-3 sentences), or elevate P0 to axiomatic status as was done for P2 — which faces the identical single-state-vs-transition gap and is handled cleanly.

## OUT_OF_SCOPE

### Topic 1: Version model interaction
The ASN treats INSERT as modifying `poom(d)` in place, while the vocabulary defines versions as "immutable snapshots." Whether INSERT implicitly creates a new version entry in the DAG, or operates on a mutable working copy that is later snapshot, is not addressed. This is a version management question, not an INSERT specification error.
**Why out of scope**: Version lifecycle semantics belong in a future ASN on CREATENEWVERSION or the version DAG model.

VERDICT: CONVERGED
