# Channel Assignment — ASN-0108 review-13

**Date:** 2026-06-05 05:22

## Issue 1: W9a's "finite total tail inflow" is not sufficient for termination without a state-stable key
Reason: The fix is internal — the counterexample is supplied, W5 is already defined in the ASN, and the correction is to add the state-stable-key hypothesis to W9a's sufficiency claim. No design intent or implementation evidence is needed; the gap and its repair are purely a matter of the ASN's own proof structure.

## Issue 2: W9 conflates "recoverable cursor key" with "state-stable (W5)"
Reason: The fix is internal — it is a definitional correction reconciling W9's derivation (which uses only cut-point recoverability) with W5's two-clause condition, both already stated in the ASN. The required weakening to recoverability-alone is derivable from the ASN's existing text.
