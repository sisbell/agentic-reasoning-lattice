# Channel Assignment — ASN-0094 review-51

**Date:** 2026-05-24 01:18

## Issue 1: NAT-card additivity walkthrough mislabels a sub-case
Reason: The fix is purely mechanical — trace the recursion correctly and relabel the sub-cases. The ASN's own NAT-card derivation prescribes the case-split (`m ∈ S₁` vs `m ∈ S₂` at each level); applying it to the worked example yields the correct label sequence. No design intent or implementation evidence needed.

## Issue 2: Generality witness counterfactual obscures what the general additivity argument actually buys
Reason: This is an expository decision about how much weight to give a counterfactual example whose regime the substrate never reaches. The reviewer's suggested fix (compress to a one-line note acknowledging the trivial substrate-reachable case + citation-purity rationale) is derivable from the proof's own structure — Step II.1's additivity is trivial at substrate-reachable inputs by inspection of the preamble. Internal presentation choice.

## Issue 3: Empty-`S_d` baseline computation buried in additional worked examples
Reason: This is a structural/placement question — move the empty-`S_d` evaluation table adjacent to the `latest_K_for_addr` template definition in NonIdempotentDirectedPair. The content is already present in the ASN; the fix is purely relocation. No external consultation needed.
