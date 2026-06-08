# Review of ASN-0102

## REVISE

### Issue 1: X8 states boundary absorption as definite when it is conditional

**ASN-0102, X8 (RunFragmentation)**: "The whole-arrangement maximal merge (M12 of `Σ'.M(d)`) reduces this further still, additionally absorbing the leading copied block into the unmoved predecessor and the trailing copied block into the first displaced block (X12)."

**Problem**: This sentence asserts the whole-arrangement merge *reduces* the count and *absorbs* both boundary blocks unconditionally. But X12 makes both absorptions conditional on I-adjacency ("each may absorb, both may, or neither"), and the first worked example explicitly states "generically neither fires." The earlier half of X8 is correctly hedged ("with equality exactly when no inter-reference boundary is I-adjacent"); this sentence drops the hedge and contradicts X12 and the examples. The Claims-table row for X8 repeats the same overstatement ("whole-arrangement merge reduces further at the two boundaries").

**Required**: Condition the claim — the whole-arrangement merge absorbs the leading block iff the predecessor is I-adjacent and the trailing block iff the first displaced block is I-adjacent (X12), and generically reduces nothing. Align the table row.

### Issue 2: Duplicated pre-state-resolution / atomicity prose and repeated evidence citation

**ASN-0102, X10(b), X15, and the self-transclusion example**:
- X10(b): "the precondition — including the resolution `resolve_Σ(R)` — is evaluated against the pre-state `Σ` in one indivisible step … Gregory's trace exhibits the same ordering concretely (`specset2ispanset` precedes `insertpm`, Q15)."
- Self-transclusion example: "X15's atomicity (the precondition, including `resolve_Σ(R)`, is read against `Σ` in one indivisible step) … Gregory's ordering (`specset2ispanset` precedes `insertpm`, Q15) exhibits the same discipline."

**Problem**: The same fact — resolution reads the pre-state in one indivisible step, witnessed by `specset2ispanset` preceding `insertpm` (Q15) — is stated three times (X10b, X15, example) with the Q15 citation appearing verbatim in two of them. The worked example's role is to *exercise* X10(b)/X15, not to re-derive and re-cite them.

**Required**: State the pre-state-snapshot discipline once (X10b/X15 own it) and let the example demonstrate the consequence (the circular `x_2`-vs-`x_3` outcome) without re-citing Q15 or re-explaining the atomicity rule.

### Issue 3: X14 "Premise (boundary B)" reads as framework rationale

**ASN-0102, X14**: "`ValidComposite★` reads each coupling and composite-boundary property at a *composite boundary* `B` … Standalone, COPY is a length-1 composite: `B = Σ` … Embedded, COPY carries `Σ_i → Σ_{i+1}` … `B = Σ_0`, `Σ_clo = Σ_n`."

**Problem**: This paragraph explains *how* `ValidComposite★` reads its properties (the standalone-vs-embedded boundary enumeration) before any COPY-specific obligation is discharged. The single load-bearing fact COPY needs is that P4★ and the composite-boundary properties are evaluated at a boundary where P4★ already holds. The standalone/embedded case-enumeration is meta-prose about the framework's reading discipline, the pattern the anti-bloat classifier targets.

**Required**: Reduce to the one fact COPY uses — the boundary `B` at which P4★/P2/monotonicity supply `R_B ⊆ Σ'.R` and `dom(B.C) ⊆ dom(Σ.C)` — and drop the standalone-vs-embedded exposition.

## OUT_OF_SCOPE

### Topic 1: The four Open Questions (displacement-after-copy, further-reference containment, time-varying views, unreachable allocator)
**Why out of scope**: These name genuinely new territory (subsequent displacement, transitive reference-of-reference, temporal view divergence, reachability) that COPY itself does not need to settle. They are correctly posed as future work, not errors in this ASN.

VERDICT: REVISE
