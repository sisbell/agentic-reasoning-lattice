# Review of ASN-0058

## REVISE

### Issue 1: `v + k` reinvents OrdinalShift; M-aux re-derives TS3

**ASN-0058, Mapping Block / M-aux**: "Recall that `v + k` for `k ≥ 1` denotes `v ⊕ wₖ` where `wₖ = [0, ..., 0, k]` has length `#v` and action point at position `#v`."

**Problem**: This is exactly `shift(v, k) = v ⊕ δ(k, #v)` (OrdinalShift, ASN-0034). The ASN defines it independently, never names `shift` or OrdinalShift, and then re-derives TS3 (ShiftComposition) from scratch as M-aux via TA-assoc. The `+` notation is locally readable, but the connection to the foundation must be explicit — otherwise the ASN invents its own notation for an operation the foundation already defines with proven properties (TS1–TS5).

**Required**: Introduce `v + k` as shorthand for `shift(v, k)` (ASN-0034), extended to `k = 0` as the identity. Then M-aux follows by citing TS3 (ShiftComposition) directly, with the `k = 0` / `j = 0` boundary cases from the convention. The independent derivation via TA-assoc and `wₖ ⊕ wⱼ = w_{k+j}` can be dropped.

### Issue 2: C1a overclaims required conditions

**ASN-0058, C1a (RestrictionDecomposition)**: "Both proofs require no property of M(d) beyond S2, S8-fin, and S8-depth; they apply to f verbatim."

**Problem**: M12's proof text explicitly invokes S8a: "(Condition 2 is vacuously satisfied when the last component of `v` equals 1: the only candidate `v'` would require a zero last component, placing it outside `dom(f)` by S8a, ASN-0036.)" If the proofs "apply to `f` verbatim," then S8a must hold for `dom(f)`. For the intended application (`f = M(d_s)|⟦σ⟧`), S8a holds because `dom(f) ⊆ dom(M(d_s))`. But the general claim — "any finite partial function `f : T ⇀ T` satisfying S2, S8-fin, and S8-depth" — does not guarantee S8a. The claim and the proof text are inconsistent.

**Required**: Either (a) add S8a to the condition list in the general claim, or (b) note that the S8a reference in M12 is illustrative, not load-bearing — leftward extension terminates by S8-fin regardless of whether any position has last component 1 — and remove the "verbatim" language, or (c) rephrase M12's parenthetical to avoid S8a (e.g., "leftward extension terminates because `dom(f)` is finite").

## OUT_OF_SCOPE

### Topic 1: Lattice structure of equivalent decompositions
**Why out of scope**: The ASN establishes the canonical decomposition as the unique coarsest element. Whether the set of all equivalent decompositions forms a lattice under refinement is a structural question about the algebra that does not affect any property introduced here.

### Topic 2: I-space discontinuity structure at block boundaries
**Why out of scope**: The ASN establishes that canonical block boundaries correspond to I-space discontinuities (M7 failure). Characterizing whether those discontinuities must be forward gaps, backward jumps, or cross-origin transitions is a property of the allocation discipline and operation history — both outside this ASN's scope.

### Topic 3: Tumbler depth relationship between V-starts and I-starts
**Why out of scope**: The block algebra treats V-positions and I-addresses as elements of T with ordinal shift at their respective depths. Whether a structural depth constraint exists between the two is a question about the address space design, not the permutation model.

VERDICT: REVISE
