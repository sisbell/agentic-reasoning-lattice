# Channel Assignment — ASN-0042 review-32

**Date:** 2026-05-14 01:46

## Issue 1: O10's fork postcondition relies on sub-delegate cooperation but doesn't elevate this to a stated limitation
Reason: The "denial as fork" architecture is a design-intent claim about what the boundary mechanism *guarantees*, and the implementation's baptism path determines whether unilateral forking is actually achievable when sub-delegates occupy adjacent slots.
Nelson question: Did the "denial as fork" design intend that a principal can always unilaterally produce an owned address as the architectural answer to non-ownership, or was cooperation with sub-delegates an acceptable mode of forking in the multi-tier (node-with-accounts) case?
Gregory question: When a node-level session invokes `docreatenewdocument`/`docreatenewversion` and the immediate user-field slots `1..hwm` under its node prefix have been allocated to delegated accounts, does the allocator produce a fresh address by advancing past those slots unilaterally, or does it require coordination with the sub-account sessions?

## Issue 2: Trajectory step count in O10 inconsistent with starting state's `hwm`
Reason: The fix is a re-indexing of the trajectory proof relative to `hwm(Σ.B, pfx(π), 2)` — derivable from the existing `next` semantics already cited and ASN-0040's sequential baptism model.

## Issue 3: Sub-lemma FirstDelegatorIsπ has a restrictive hypothesis and unclear role
Reason: This is an internal proof-structure question — whether the Sub-lemma is cited or can be demoted to a remark. The ASN's own derivations show whether anything depends on its stronger conclusion.

## Issue 4: Informal "T4(a)" notation conflates multiple foundation properties
Reason: The fix is mechanical citation precision against the foundation's T4/T4a/T4b/T4c labels, which the ASN already references directly.

## Issue 5: Worked example presents fork as a single allocation, eliding the multi-step trajectory it claims O10 produces
Reason: The trajectory is already fully specified in the O10 proof; extending the worked example traces existing material. The cooperative-vs-unilateral exposition depends on Issue 1's resolution but adds no new external consultation.

## Issue 6: O15 condition (vi) preservation is asserted but not fully derived
Reason: The non-nesting invariant is derivable from O14's base case plus O15(vi), O12, and O13 already stated — an internal induction the ASN can carry out without external input.

## Issue 7: `acct(a)` definition introduction is internally inconsistent
Reason: A pure wording fix to align the prose introduction with the formal contract's `zeros(acct(a)) ≤ 1` postcondition.
