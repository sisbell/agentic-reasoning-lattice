# Channel Assignment — ASN-0071 review-52

**Date:** 2026-06-03 10:25

## Issue 1: Source self-inclusion is an unstated derived consequence
Reason: The fix is fully internal — the issue text itself supplies the one-line derivation from `wp-defined` and the existing `find`/`iaddrs` definitions, and the worked scenario already exhibits it (`d_A ∈ find(Q)`). No design intent or implementation evidence is needed to state a claim derivable from the ASN's own definitions.

## Issue 2: Meta-prose in the finiteness proof
Reason: Pure editorial deletion of an epistemic aside; the load-bearing three-link chain (ExtendedReachableStateInvariants → ValidCompositeAmended → finite concatenation) is already present in the ASN. No channel needed.

## Issue 3: Visibility/access-control out-of-scope statement is deferred twice
Reason: A redundancy removal — the same exclusion is stated in the intro and in *What we do not specify* (iii); consolidating to the scope section is internal restructuring requiring neither design intent nor implementation evidence.

## Issue 4: PC-RANGE — a general claim derived inside the worked-scenario section
Reason: Placement, not existence — PC-RANGE's derivation depends only on PC + T1, both already established in the ASN, so relocating it to the resolution/denotation development is fully internal.
