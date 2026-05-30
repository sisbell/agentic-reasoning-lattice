# Channel Assignment — ASN-0042 review-121

**Date:** 2026-05-30 05:09

## Issue 1: Editorial/revision meta-prose in O17b
Reason: Pure editorial deletion — the sentence narrates revision history, not axiom content. Removing it requires no design intent or implementation evidence; the axiom stands on its own branches.

## Issue 2: Document-organization meta-prose in O7(c)
Reason: Internal. Dropping the placement-narration clause while keeping the substantive (iii)/(v)-bind classification is a pure prose edit derivable from the ASN itself.

## Issue 3: O7(c) proof establishes satisfiability only at entry state, but the contract quantifies over arbitrary prospective states
Reason: Internal. The scope mismatch is resolved by the ASN's own formal machinery — either narrow the contract to the entry state or re-run the (ii)/(iv) discharge over the then-current `Π_Σ` using the already-stated longest-match and NestingByDelegation results. No external intent or evidence is needed to pick and justify either framing.

## Issue 4: `ω` declared a "partial function" with domain `Σ.B`, then proved total on `Σ.B`
Reason: Internal terminology consistency. Choosing one framing ("partial on `T` with domain `Σ.B`" vs. "total on `Σ.B`") is derivable from the ASN's own definitions.

## Issue 5: Overlapping freshness statements remain across the O17b / Freshness-(v) / O18 / NamespacePrincipalExclusivity cluster
Reason: Internal deduplication. Designating O18 as the single material-baptism result and having the others cite it is a structural edit fully derivable from the existing derivations.

## Issue 6: Forward-reference deferral from Freshness-(v) to O17b
Reason: Internal reordering. Moving O17b before Freshness-(v) to remove the "stated below" pointer requires only the ASN's own dependency structure.

## Issue 7: Duplicated "discharge T4 once here by O17" prose in O6 and O9
Reason: Internal. Factoring the repeated remark into a single stated convention referenced by both proofs is a prose-consolidation choice needing no external input.

## Issue 8: Notation drift `Π` vs `Π_Σ` in the summary table
Reason: Internal notation consistency. Aligning the table rows with the body's state-relativized convention is derivable from the ASN alone.
