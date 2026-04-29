# Review of ASN-0040

## REVISE

### Issue 1: Bop proof overstates B7's coverage for B1 preservation in other namespaces

**ASN-0040, Bop (Baptism), B1 preservation**: "For every other namespace (p', d'), B7 ensures a ∉ S(p', d'), so children(Σ'.B, p', d') = children(Σ.B, p', d'), and their contiguous prefix property is undisturbed."

**Problem**: B7's precondition requires *both* pairs to satisfy B6: "provided both parents satisfy T4 and both depths satisfy B6." The universally quantified claim "for every other namespace" exceeds what B7 alone establishes. There exist non-B6 namespaces where B7's precondition is unmet — specifically, when p' has a trailing zero as its sole T4 defect and d' = 1, the stream S(p', 1) coincides with a valid stream S(p'', 2), so the new element *does* belong to that stream. The conclusion (B1 is preserved in all namespaces) is correct — the B1 proof below gives the complete three-sub-case argument — but the Bop proof presents itself as a complete "Proof of well-definedness and correctness" while citing reasoning that is insufficient for the claim.

**Required**: Either (a) qualify the B7 citation ("For every other B6-valid namespace, B7 ensures...") and add a forward reference to B1's proof for the remaining cases, or (b) incorporate the brief two-case extension into the Bop proof: non-B6 namespaces with all-T4-violating streams are handled by a satisfying T4, and the sole-defect trailing-zero case collapses to an already-handled valid namespace via stream identity.

### Issue 2: Properties table shows apparent circular dependency between B1 and Bop

**ASN-0040, Properties Introduced table**: B1 lists "Bop" in its Status/follows-from column; Bop lists "B1" in its Status/follows-from column.

**Problem**: This presents as a logical cycle: B1 depends on Bop, Bop depends on B1. The actual proof structure has no circularity — B1 is proved by induction over transitions, and its inductive step *is* the Bop correctness argument. B1's proof uses the *definition* of the baptism operation (the next function, the S(p,d) stream, the inc operations) but does not depend on the *correctness theorem* of Bop. Conversely, Bop's correctness is a consequence of B1 holding as an invariant. A reader encountering the apparent cycle in the table may distrust the logical structure or attempt to break the cycle incorrectly.

**Required**: Replace "Bop" in B1's dependency list with the specific definitions B1's proof actually uses (e.g., "next definition, B0a, B6"), or add a note to the table clarifying that B1 and Bop's correctness are established in a single induction — B1 depends on the baptism mechanism definition, and Bop's correctness follows from B1 as invariant.

VERDICT: REVISE
