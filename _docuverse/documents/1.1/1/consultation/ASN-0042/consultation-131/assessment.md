# Channel Assignment — ASN-0042 review-131

**Date:** 2026-05-30 06:21

## Issue 1: Delegation condition (v) is redundant with the O17b coupling
Reason: The fix is internal — both condition (v) and O17b's coupling are already stated in the ASN, and *Freshness-(v)* already documents that every consuming theorem uses only `T4(pfx(π')) ∧ pfx(π') ∉ Σ.B`. Deciding which form is primitive and deduplicating is a formal-structuring choice derivable from the ASN's own axioms.

## Issue 2: O17 imports B10 without the reachability that licenses it
Reason: The fix is internal — RegistryReachability is already derived in the ASN and its derivation does not use O17, so O17 can cite it before importing B10. No design intent or implementation evidence is required to insert the licensing step.

## Issue 3: The O1a/O1b/T4 shared induction cannot be checked in reading order
Reason: The fix is internal — it is purely an ordering/presentation matter (relocate the shared induction after its premises, or hoist O12–O15 and O14 ahead). All cited dependencies already exist in the ASN.

## Issue 4: Essay/meta-prose in structural slots
Reason: The fix is internal — dropping the O14 meta-sentence and stating O7(c)'s restriction inline are editorial changes; the actual restriction (next-reachable single-step extension) is already specified in obligation (v) and the Formal Contract.
