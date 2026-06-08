# Review of ASN-0102

## REVISE

### Issue 1: Precondition labels P1–P4 collide with foundation invariant labels
**ASN-0102, "Precondition" and X14**: The operation's preconditions are labelled "(P1) Source resolvable", "(P2) Target document", "(P3) Content subspace", "(P4) Valid insertion position." The foundation (ASN-0047) already defines `P1` (EntityPermanence), `P2` (ProvenancePermanence), `P3` (ArrangementMutabilityOnly), and `P4★` (ProvenanceBounds) as named invariants/properties. X14 then discharges foundation properties under the bare labels — e.g. "the separate transition theorem ExtendedTransitionInvariants (ASN-0047), whose sole conjunct is **P3** (`dom(C) ⊆ dom(C')...`)" — immediately after the reader has anchored "P3" to "content subspace."
**Problem**: A precise reader cannot tell, from a bare `P3` (or `P1`/`P2`/`P4`), whether the precondition or the foundation invariant is meant. The disambiguating parenthetical is not always present, and the overload is systematic across all four labels.
**Required**: Rename the COPY-local preconditions to a non-colliding scheme (e.g. `PC1–PC4` or `Pre-1…Pre-4`) and update every internal reference.

### Issue 2: P4a referred to by a name the foundation does not use
**ASN-0102, X14**: "the composite-boundary Class (b) conjuncts beyond P4★ — **P4a (HistoricalFidelity)** and P7a (ProvenanceCoverage)..."
**Problem**: ASN-0047 defines `P4a` as **TraceWitnessing**, not "HistoricalFidelity." Introducing a private name for a foundation property is exactly the reinvention standard 7 prohibits; it also makes cross-checking the discharge against the foundation harder.
**Required**: Use the foundation's name, `P4a (TraceWitnessing)`.

### Issue 3: S3★-aux discharge is folded into the S3★ wp computation without its own argument
**ASN-0102, X14**: "The arrangement-side Class (a) conjuncts are exactly those established above: S2 and S8a (X16), **S3★ and S3★-aux (the wp computation)**..."
**Problem**: The wp computation establishes S3★ (each new mapping is routed to the store its subspace names). It does not establish S3★-aux (SubspaceExhaustiveness: every V-position has subspace `s_C` or `s_L`), which is a distinct claim. Bundling them under "the wp computation" asserts a result the cited argument does not produce.
**Required**: Add the one-line discharge — copied positions are `s_C` by P3 (content-subspace precondition); unmoved and displaced positions carry their pre-state subspace, which is `s_C` or `s_L` by pre-state S3★-aux — so S3★-aux holds at `Σ'`.

## OUT_OF_SCOPE

### Topic 1: Re-displacement, re-reference, cross-time view divergence, and unreachable-allocator identity
**Why out of scope**: The four Open Questions (continued discoverability of copied content under later displacement; containment guarantees when a reference-holder is itself referenced; whether two references must resolve to differing views over time; identity when the allocating document is unreachable) concern operations and survivability properties not defined here. They are correctly posed as future-ASN territory, not deficiencies of COPY.

VERDICT: REVISE
