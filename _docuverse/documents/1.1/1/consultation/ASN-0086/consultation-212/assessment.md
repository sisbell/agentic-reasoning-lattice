# Channel Assignment — ASN-0086 review-212

**Date:** 2026-06-01 16:45

## Issue 1: The "lands on a genuine chain sibling" admissibility argument is restated three times
Reason: This is a purely editorial deduplication — consolidate the chain-sibling-landing argument in R0/L-ContiguousPrefix and replace the two restatements with citations. The content already exists in the ASN; no design intent or implementation evidence is needed.

## Issue 2: Out-of-scope scope caveat repeated across sections
Reason: Dropping a duplicated scope parenthetical that restates the already-fixed `→ ≡ K.σ ∪ K.α ∪ K.λ` boundary is internal to the ASN. The scope is settled in the State-transition section; no external channel bears on this.

## Issue 3: Mutual deferral between the wp Result and Worked Sketch Step 4
Reason: Resolving the circular forward/back references — keeping the proof in *Derivation*, leaving Step 4 as illustration — is a structural edit derivable from the ASN's own proof layout. No design or implementation question is involved.
