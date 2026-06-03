# Channel Assignment — ASN-0102 review-17

**Date:** 2026-06-03 16:37

## Issue 1: The grounding sentence for P4★ at COPY's pre-state cites the wrong composite endpoint
Reason: The fix is purely internal — it corrects a logical mischaracterization of which endpoint a length-1 composite terminates at, and the ASN already states the correct version in X14 ("its pre- and post-states Σ, Σ' are composite boundaries… P4★ holds at Σ"). Regrounding Σ's boundary status on trace position (initial state of the composite / terminus of the preceding one) requires only the ValidComposite★ machinery already cited, no design intent or implementation evidence.
