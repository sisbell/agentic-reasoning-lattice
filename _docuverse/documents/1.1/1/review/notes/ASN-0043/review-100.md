# Review of ASN-0043

## REVISE

### Issue 1: "TA5a is unconditional for k ∈ {0, 1}" is false — TA5a is unconditional only for k = 0

**ASN-0043, L9 Witness (Case A, step iii) and Worked Example (L1c verification, step iii)**: "(iii) `inc(d'.0.s_L, 1)` → `d'.0.s_L.1` = `a` — child-spawn to element field depth 2 (`k' = 1`; **TA5a is unconditional for `k ∈ {0, 1}`**; the output has `zeros(a) = 3`)." The identical phrase recurs in the worked example: "`k₃ = 1`; TA5a is unconditional for `k ∈ {0, 1}`."

**Problem**: The foundation TA5a (IncrementPreservesT4) states `inc(t, k)` satisfies T4 iff `k = 0`, *or* `k = 1 ∧ zeros(t) ≤ 3`, *or* `k = 2 ∧ zeros(t) ≤ 2`. Only `k = 0` is unconditional; `k = 1` carries the side condition `zeros(t) ≤ 3`. The claim as written contradicts the cited foundation. The conclusion happens to survive — in both occurrences the input has `zeros = 3 ≤ 3` — but the proof discharges T4-preservation from a false premise. The asymmetry is visible within the same chains: step (i) for `k' = 2` *correctly* cites the bound ("requiring `zeros(d') ≤ 2` by TA5a; satisfied since `zeros(d') = 2`"), while step (iii) for `k' = 1` waves it away as unconditional.

**Required**: Replace "TA5a is unconditional for `k ∈ {0, 1}`" with the actual discharge: `k = 1` with `zeros(input) = 3 ≤ 3`, satisfying TA5a's `k = 1` bound. (`k = 0` may continue to be cited as unconditional; only the `k = 1` half is wrong.)

### Issue 2: L7's proof is a self-referential word-search rather than a structural argument

**ASN-0043, L7 (DirectionalFlexibility), "By inspection"**: "No invariant in L0–L14 or L-fin references slot directionality or the source/target roles: none uses the words 'from,' 'to,' 'source,' 'target,' 'origin,' or 'destination' in any structural role."

**Problem**: The justification is a lexical inventory of the document's own prose. It is fragile (it rots the moment an invariant is reworded) and self-referential rather than structural — and it sits in tension with L3/L6/StandardTriple, which *do* name slots "from-endset" and "to-endset." The hedge "in any structural role" is doing all the work, yet the claim is presented as a mechanical word-scan. The substantive content L7 needs is structural: the invariants quantify over addresses, endset membership, and slot *position* only, and assign no semantics distinguishing slot 1 from slot 2 beyond positional distinctness (L6). That is the argument; the word-search is a proxy for it.

**Required**: Recast the L7 justification as a structural observation — the invariants constrain slot identity only up to positional distinctness (L6) and never predicate on which slot is source vs. target — rather than as an enumeration of words absent from the text.

## OUT_OF_SCOPE

None. The note correctly defers operations, resolution, and transclusion-consistency questions to its Open Questions and the listed scope exclusions.

VERDICT: REVISE
