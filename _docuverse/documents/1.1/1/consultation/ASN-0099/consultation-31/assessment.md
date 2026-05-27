# Channel Assignment — ASN-0099 review-31

**Date:** 2026-05-27 04:42

## Issue 1: F10's well-orderedness terminology overstates the requirement
Reason: Pure terminology/citation fix. The ASN already has L-fin establishing finiteness and T1's strict total order; the correction is to invoke finiteness + totality (or NAT-wellorder via bijection to an initial segment) rather than the stronger "well-orderedness of T1's restriction". Derivable from the ASN's own foundation citations.

## Issue 2: A1b relies on Nelson and Gregory as load-bearing premises
Reason: Methodological framing choice internal to the author. The reviewer's recommended fix is to *remove* the load-bearing dependence on external sources (option a: restate as adopting the closed-world convention purely as a methodological choice; option b: defer to foundation revision). Neither option requires more evidence from Nelson or Gregory — the fix restructures the argument so their material becomes supplementary rather than load-bearing.

## Issue 3: F4 strengthening/weakening framing is imprecise about which conformance contract is being violated
Reason: Pure rephrasing for clarity. The intended meaning (conformance evaluated against F2 ∧ F3 with `matches := F1`) is already present in the framing paragraph and the weakening direction; the strengthening direction needs to be matched to that explicitness. Internal editorial work.

## Issue 4: The chain-index argument in F10 cites SubAllocatorAxiom.ChainDiscipline at A_doc, but the axiom covers only A_C and A_L
Reason: Citation correction against the foundation ASNs. The reviewer has already identified the correct target (T10a.7 EnumerationInjectivity in ASN-0034), and verifying the substitution is a matter of reading ASN-0034 and ASN-0093 — no design intent or implementation evidence is at stake.

## Issue 5: F10's "between" claim for version-extension blocks is asserted but the general (n > 3) iteration is only gestured at
Reason: Mathematical proof structure. The fix is either a formal inductive argument chaining the C(n,2) pairwise inequalities by T1's transitivity (machinery already present in the ASN) or restriction of the claim to pairs. Neither design intent nor implementation evidence is relevant to whether the induction is properly discharged.
