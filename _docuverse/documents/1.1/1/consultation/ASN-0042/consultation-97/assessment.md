# Channel Assignment — ASN-0042 review-97

**Date:** 2026-05-30 02:31

## Issue 1: O10 invokes ASN-0040 reachability of the registry without a base case
Reason: The fix is to add a bootstrap axiom (or O14 clause) stipulating that `Σ₀.B` conforms to ASN-0040's already-cited B₀ conf.; once stated, O17b's per-transition coupling lifts to full reachability by induction. Adding the grounding axiom is a formalization decision derivable from the ASN's own structure and ASN-0040's referenced definitions.

## Issue 2: O6 forward direction applies `fields`, T4b, T4c to `a` without discharging T4(a)
Reason: O17 (AllocatedAddressValidity) is already present in the ASN and is cited for the same purpose in O9 and AccountPrefix; the fix is to cite it once at the head of the forward direction. Purely internal.

## Issue 3: `odom` naming paragraph is notational defense, not reasoning
Reason: Editorial pruning of justification prose; the definition `odom(π) = {a ∈ T : pfx(π) ≼ a}` stands on its own. No external input needed.

## Issue 4: "Summary of the Model" carries reviser-drift / honesty meta-prose
Reason: Editorial rewrite to state the axiom dependency directly without the self-correcting arc; the load-bearing content is already in the ASN. Internal.
