# Review of ASN-0075

## REVISE

### Issue 1: D-RECONS leans on P4a without noting it is composite-boundary-scoped — and this, not P4★, is the substantive reason D-BOUND must be in the operation's contract

**ASN-0075, "State-Functional Independence" (D-RECONS)**: "P4a (historical fidelity, ASN-0047) ensures that whenever the operation reports `DELETED(a, d)`, there really was a past state where `a` was in `d`'s arrangement."

**Problem**: In ASN-0047, P4a is a *composite-boundary property* (`ExtendedReachableStateInvariants` lists `P4★ ∧ P4a ∧ P7a` only at composite boundaries), not a per-state invariant. At an intermediate state inside a composite, P4a may fail, so `(a, d) ∈ R` need not witness any prior arrangement — and `DELETED(a, d)` could fire without the content ever having been included. D-RECONS invokes P4a as if unconditionally available. Moreover, this is the genuine reason `DELETED` carries its intended meaning (and hence the real reason D-BOUND belongs in the operation's contract), yet the ASN justifies D-BOUND only through D-EXH/P4★ (clean three-state partition). The stated rationale for D-BOUND understates its necessity.

**Required**: In D-RECONS, note that P4a is composite-boundary-scoped and that the historical-fidelity claim therefore holds only at composite-boundary states (supplied by D-BOUND); and in the D-BOUND discussion, state that D-BOUND is required not merely for D-EXH's partition but for P4a to give `DELETED` its meaning.

### Issue 2: The `d_A = d_B` edge case mis-attributes an unconditional contradiction to D-EXH

**ASN-0075, "Edge Cases"**: "If `d_A = d_B`, then for each `a`, `DELETED(a, d_A) ∧ CURRENT(a, d_A)` is contradictory (by D-EXH)."

**Problem**: The contradiction is direct and unconditional — `DELETED(a, d_A)` requires `a ∉ ran(M(d_A))` and `CURRENT(a, d_A)` requires `a ∈ ran(M(d_A))`. It needs neither D-EXH nor the composite-boundary hypothesis. This is the same kind of range-membership contradiction the ASN elsewhere correctly flags as unconditional ("the disjointness is unconditional — it needs neither D-EXH nor any composite-boundary hypothesis"). Citing D-EXH here is both unnecessary and slightly wrong, since D-EXH carries a boundary precondition this case does not require.

**Required**: Replace "(by D-EXH)" with the direct observation that the two `ran(M(d_A))`-membership conditions are contradictory, mirroring the unconditional disjointness argument.

### Issue 3: Repeated composite-boundary / P4★ justifications accreted across sections (anti-bloat)

**ASN-0075, D-EXH paragraph, "Supplementary lemma," and D-DISCR discrimination-obligation closing**: the same fact — that P4★ is a composite-boundary property and not a per-state invariant — is re-explained three times:
- D-EXH: "it activates P4★ ... not as a per-state invariant ... At intermediate states inside a composite, P4★ may fail...";
- Supplementary lemma: "The boundary hypothesis is load-bearing because the argument invokes P4★ (a composite-boundary property); D-BOUND supplies it at every invocation.";
- D-DISCR closing: "it does not invoke P4★, so the discrimination holds at every reachable state, not merely at composite boundaries."

**Problem**: The note carries `review-mode.anti-bloat`. Three separate passages restate the same scoping fact about P4★; the reader must re-absorb it at each occurrence. This is defensive meta-prose that has compounded across cycles.

**Required**: State the P4★ composite-boundary scoping once (naturally at D-EXH, where the boundary hypothesis is first introduced) and let the later proofs cite it without re-deriving the scoping rationale.

## OUT_OF_SCOPE

### Topic 1: Restoration/recovery operation that consumes SHOWDELETIONS output
The final Open Question (a restoration operation reintroducing deleted content while preserving origin and link-resolvability) defines a new operation on state and belongs in a future ASN, not here.

### Topic 2: Generalization to families of >2 documents and span-presentation of the deletion set
The witness-structure for n-ary comparison and the conditions for finite span presentation are new territory, correctly deferred to Open Questions.

VERDICT: REVISE
