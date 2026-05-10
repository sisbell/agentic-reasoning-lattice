# Review of ASN-0025

Based on Alloy modeling-1

## SKIP

### Passed properties (12)

J1, J2, P1, P2, P6, P3, UF, P4, Domain preservation, Link-subspace frame, P5, P7 — all checks returned UNSAT (no counterexamples within scope). No issues.

### J0 — VSpaceGrounded (SAT on check): modeling artifact

The Alloy model defines State with `docs in iota.Value` and `(vmap.IAddr).VPos in docs` as sig facts but does not include VSpaceGrounded as a sig fact. The checker correctly finds a State where a document's vmap target falls outside dom(iota). This confirms J0 is not redundant with the other structural constraints — which is expected. J0 is an independently stated invariant that operations must preserve; each operation section in the ASN verifies J0 preservation. The counterexample shows "J0 doesn't follow from the type structure alone," not "J0 is wrong."

### P0 — ISpaceGrowth (SAT on check): modeling artifact

The model creates two unconstrained State atoms with no transition relation and checks `all s, s2: State | ISpaceGrowth[s, s2]`. Two arbitrary states naturally need not satisfy subset inclusion on their allocated sets. P0 is a property of valid state transitions (operations), not of arbitrary state pairs. The counterexample shows two unrelated states — not an operation that shrinks I-space.

### UF-V — UniversalVFrame (SAT on UncheckedPreservesOtherDocs): intentional negative control

The three substantive checks — ModifyPreservesFrame, CreatePreservesFrame, FramePreservesVisibility — all returned UNSAT. The SAT result is on UncheckedPreservesOtherDocs, which is the negative control: it omits the UF-V frame condition and confirms that without it, other documents' vmaps can change. This is the expected outcome of the negative test.

### ExteriorFrame (SAT on UncheckedExteriorPreserved): intentional negative control

The two substantive checks — ExteriorFramePreserved, ExteriorAddressSetPreserved — both returned UNSAT. The SAT result is on UncheckedExteriorPreserved, the negative control that omits the frame postcondition. Expected outcome.

### P8 — ProvenanceNotLocation (SAT on ResolutionEqualsOrigin): intentional negative control

MigratePreservesWF and MigratePreservesContent both returned UNSAT. The SAT result is on ResolutionEqualsOrigin, which intentionally asserts the false claim that resolution must equal origin. The counterexample — an allocated address whose physical location differs from its origin node — is exactly what P8 predicts. This confirms P8's design intent: the address encodes provenance, not current location.

VERDICT: CONVERGED
