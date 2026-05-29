# Channel Assignment — ASN-0040 review-67

**Date:** 2026-05-28 23:41

## Issue 1: S2 and B6 necessity restate the same injectivity rationale across two sections
Reason: Pure editorial deduplication — both passages already exist in the ASN; the fix is to keep the injectivity rationale at B6 necessity and reduce S2's closing to the bare structural fact. Derivable from the ASN alone.

## Issue 2: B0b carries defensive "not asserted here" prose with a forward reference to Bop
Reason: Deleting a scope-disclaimer clause whose content (freshness lives in Bop) is already present and correct. No design intent or implementation evidence needed.

## Issue 3: B8 records its scope limitation twice with a forward pointer between them
Reason: Removing a redundant forward-pointing sentence; the substantive scope note and the co-reachable definition both already stand in the ASN. Internal edit.

## Issue 4: Condition (iii)'s "binds only at d=2 / subsumed at d=1" is repeated three times
Reason: Consolidating a binding-depth observation already proved in the necessity argument into a single site. The math is settled within the ASN; purely structural deduplication.

## Issue 5: next's "Justification of well-definedness" re-derives TA5 totality as essay
Reason: Collapsing redundant case-prose to the one load-bearing sentence; the cited axioms (TA5(c)/(d), T1, B_fin) are all already in the contract. No external channel required.

## Issue 6: B9 essay paragraph restates the formal proof's NAT-closure reasoning
Reason: Cutting/trimming motivation prose that duplicates the proof's own mechanism (TA5(c) totality + NAT-closure), both already in the ASN. Internal edit.
