# Channel Assignment — ASN-0076 review-25

**Date:** 2026-06-03 08:15

## Issue 1: Citations to a non-existent foundation claim "SubAllocatorAxiom"
Reason: This is a citation-retargeting task internal to the spec — the reviewer already names the correct foundation claims (`SubAllocatorBundle`/`AllocatorHierarchy` in ASN-0047) and the question of whether the emission rule lives only in ASN-0093 is resolved by reading the foundation ASNs, not by design intent or implementation evidence.

## Issue 2: E7 "LineageDiscoverability" diverges from the foundation's discoverability notion without reconciliation
Reason: Reconciling `covers` against ASN-0098's `discoverable_from`/LP12/LP17 is internal cross-ASN consistency work — both predicates and the orphaned-link classification are already defined in the cited dependency, so the fix is derivable from existing spec content.

## Issue 3: Worked-example E4 verification conflates span-membership with coverage
Reason: Pure proof-logic correction — the main E4 proof already supplies the correct singleton-membership/L6 chain, so the worked example just needs to mirror it; entirely derivable from the ASN's own content.
