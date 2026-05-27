# Channel Assignment — ASN-0100 review-7

**Date:** 2026-05-27 14:24

## Issue 1: Forced-ordering enumeration omits K.μ⁻ → K.μ⁺
Reason: The fix is derivable from K.μ⁺'s functional extension precondition in ASN-0047 (already cited extensively in the ASN). The forced ordering follows directly from the precondition-violation argument the reviewer supplies.

## Issue 2: "Permanently" overstates the m_C invariant
Reason: The fix is a language softening that aligns the claim with what ValidComposite★ (ASN-0047) actually guarantees, given K.μ⁻'s ability to shrink V_{s_C}(d) to ∅. Both the relevant operator semantics and S8-depth's per-state form are already in the ASN's cited substrate.

## Issue 3: Relationship between I3 and INSERT's post-state could be sharper
Reason: The fix is a clarification comparing ASN-0082's I3 clauses (already cited) with INSERT's specification. The Insertion region's exclusion from ASN-0082's shift-only model is a direct textual comparison between the two ASNs.

## Issue 4: Cross-subspace D-CTG★ at K.μ⁻ intermediate state for link subspace
Reason: The fix completes the per-state invariant audit using the link-subspace full-retention property (n'_{s_L} = n_{s_L}) already established in the ASN's K.μ⁻ analysis. Preservation under full retention is immediate.

## Issue 5: Worked example does not verify all key postconditions
Reason: The fix extends the worked example with a concrete link/endset trace and J1★ discharge using the ASN's own abstract machinery (LP3★, LP9, LP10, LP14, J1★ — all already cited). No external evidence needed to construct a synthetic link example.

## Issue 6: Open Question conflates already-resolved scope
Reason: The fix is to remove or restate the open question; the resolution (chunking changes observable substrate-level behaviour) is already established by the ASN's existing composite-atomicity discussion.
