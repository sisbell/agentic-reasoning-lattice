# Channel Assignment — ASN-0076 review-31

**Date:** 2026-06-03 21:30

## Issue 1: E2 carries two independent proofs of the same conclusion
Reason: Purely editorial deduplication — the ASN already contains both proofs and the task is to keep one. No design intent or implementation evidence is needed; the L11a argument's completeness is established within the ASN itself.

## Issue 2: The `τ_sup` supersession-type convention is deferred in four places
Reason: Consolidation of repeated forward-references already present in the ASN; deciding where to state the deferral once is internal editing requiring no external channel.

## Issue 3: E6's "Informal motivation" is an essay on an unformalized authorization model
Reason: The ASN itself states the authorization model is not formalized and is deferred; compressing the essay to one deferral sentence is internal. No need to consult Nelson on intent, since the ASN already commits to deferring authorization to a future ASN.

## Issue 4: E10 trailing paragraph restates its own proof
Reason: Deleting a self-restatement is purely mechanical and derivable from the ASN's own proof text.

## Issue 5: "Why Editing Cannot Be Otherwise" and "On Identity" are motivational essay
Reason: Trimming rhetorical padding down to the L12-contradiction and the address-identity point both already proved (E2) is internal editorial work; no design or implementation input required.
