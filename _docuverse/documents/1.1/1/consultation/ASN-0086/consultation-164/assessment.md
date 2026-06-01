# Channel Assignment — ASN-0086 review-164

**Date:** 2026-06-01 06:09

## Issue 1: Definition — Nullify elaborates a case its own precondition excludes
Reason: Purely a prose-pruning fix: the off-P1 path is excluded by Nullify's own stated precondition, so dropping the elaboration is derivable from the ASN's existing condition statements. No design-intent or implementation evidence is at stake.

## Issue 2: Definition — Nullify previews its proof and justifies precondition structure rather than stating it
Reason: Internal structural edit — convert preview/justification meta-prose into plain condition statements. The role assignments (P0 gates emission, P1 the postcondition, P2 scope) are already proved downstream in the ASN, so no external channel is needed.

## Issue 3: Unit-depth-discipline definition and relational-layer definition state the same P1-confinement commitment twice
Reason: Pure deduplication — collapse two restatements into one statement plus a cross-reference. Both passages already exist in the ASN; choosing the canonical location is internal.

## Issue 4: WP section preamble duplicates Case 1's own "not the weakest precondition" framing
Reason: Internal redundancy trim — the substantive distinction lives in the Case 1 body; reducing the preamble requires only the ASN's own text.

## Issue 5: relational-layer reduction corollary invokes R7a and then declares the invocation unnecessary
Reason: Internal coherence fix — the corollary's own argument shows Emit_K *is* K.λ, making the R7a invocation self-cancelling; deciding whether to drop it or justify R7a's placement is derivable from the ASN's stated lemma uses.
