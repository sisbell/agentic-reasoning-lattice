# Channel Assignment — ASN-0042 review-72

**Date:** 2026-05-29 22:09

## Issue 1: O8's `delegated_{Σ_d}(π, π')` abbreviation is malformed under the transitive-closure binder
Reason: Internal. The ASN already defines `delegated` as a single-edge 4-place predicate and the proof body already introduces `Σ_d^{post}`; the fix is aligning the contract's notation with the existing definition and proof, derivable from the ASN alone.

## Issue 2: The six delegation conditions are stated in full twice
Reason: Internal. Pure deduplication — keep the normative statement at the Definition of `delegated` and cite by name elsewhere; no design or implementation input needed.

## Issue 3: Meta-prose justifying document structure rather than advancing claims
Reason: Internal. Editorial deletion of non-advancing commentary; the load-bearing distinctions (e.g., baptismal- vs allocator-domain monotonicity) are already stated in the ASN and need only be condensed.

## Issue 4: Repeated deferral chains pointing forward to the same later location
Reason: Internal. Editorial restructuring to present each sub-result once at its point of use; no external evidence required.

## Issue 5: O2 finiteness step relies on O1b before invoking it
Reason: Internal. Both O1b and FiniteRegistry already exist in the ASN; the fix is a citation/ordering correction within the proof, fully derivable from the ASN's own content.
