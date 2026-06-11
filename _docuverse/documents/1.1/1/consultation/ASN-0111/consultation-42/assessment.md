# Channel Assignment — ASN-0111 review-42

**Date:** 2026-06-10 23:32

## Issue 1: RL5's caching discipline contradicts the permanence families the same paragraph establishes
Reason: The contradiction is internal — both permanence derivations (depth via ChainMembershipForOrigin, lineage via NodeLineage) are already proved in the ASN's own text, and the fix is a restatement of the caching discipline to match what those derivations actually establish. No new design intent or implementation evidence is required.

## Issue 2: The depth-family argument derives "element-field depth exactly 2" from length preservation alone
Reason: The fix is a missing proof step discharged entirely by already-cited foundation facts (TA5(b)/(c), TA5-SigValid from ASN-0034) — single-position modification at the terminal position, nonzero-to-nonzero, hence zeros and the element-field boundary unchanged. Purely a citation-chain completion within the existing formal material.

## Issue 3: The worked read stipulates an allocated-but-unarranged state without exhibiting its reachability
Reason: The review itself supplies the reachability route, and every operation it invokes (J0-coupled K.α + K.μ⁺ composites, K.μ⁻ contraction, K.λ chain allocation) is defined in foundations the ASN already cites (ASN-0047, ASN-0093); writing the one-to-two-sentence construction needs neither design intent nor implementation evidence.
