# Review of ASN-0102

## REVISE

### Issue 1: Composite-boundary properties P4★, P4a, P7a are never discharged

**ASN-0102, X14 ("The remaining invariants of ExtendedReachableStateInvariants are discharged below")**: the discharge list covers only the *per-state* conjunction (S2, S3★, S3★-aux, D-CTG★, …, S8★) plus the transition theorem P3.

**Problem**: `ExtendedReachableStateInvariants` (ASN-0047) has two halves — the per-state conjunction *and* "Every state at a composite boundary additionally satisfies the composite-boundary properties: P4★ ∧ P4a ∧ P7a." COPY is a *new* transition added to `ValidComposite★`'s vocabulary, so the theorem must be re-established for it. X14 itself argues that a standalone COPY satisfies the couplings J0/J1★/J1'★ — "Taking this COPY as the whole embedding composite (pre-state Σ = Σ_0)" — which means a single COPY *is* a valid composite and its post-state *is* a composite boundary. That post-state therefore must satisfy P4★, P4a, and P7a. The ASN invokes P4★ as a *premise* at Σ_0 in the coupling argument but never shows `Contains_C(Σ') ⊆ R'` holds at COPY's post-state; P4a (TraceWitnessing) and P7a (ProvenanceCoverage) are not mentioned at all.

**Required**: Discharge all three at COPY's post-state. They appear to follow — P4★ from pre-state P4★ + P2 + COPY's unconditional recording of the copied addresses; P7a from dom(C′)=dom(C) (X1) + pre-state P7a + new records; P4a from the step-local recording fact (SL), which makes each copied `a` content-subspace-resident at Σ′ so Σ′ itself is the witnessing trace state. The material exists in X14 but must be connected to these named obligations.

### Issue 2: Redundant meta-summary in the J1★/J1'★ argument (anti-bloat)

**ASN-0102, X14**: "The split turns on Σ_0-residency alone: P4★ is invoked only where it applies, on genuine Σ_0-residency (second bullet), while pre-state residency that reflects a mid-composite write rather than Σ_0-residency is routed to the first bullet, where range-newness relative to Σ_0 discharges J1'★ directly."

**Problem**: This sentence restates the two preceding bullets in terms of the argument's own organization ("second bullet," "routed to the first bullet"). It is meta-prose describing how the case split is structured rather than advancing the claim; the substantive conclusion is already carried by the immediately preceding sentence ("In neither case does an R-new pair … lack a range-new address"). The reader must skip past it to continue.

**Required**: Delete the sentence; keep the J1'★ conclusion.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of copied content by later operations
The first open question (invariant tying origin to continued discoverability after subsequent displacement) concerns the interaction of COPY's output with later INSERT/DELETE/REARRANGE, which belongs to those operations' ASNs, not this one.

VERDICT: REVISE
