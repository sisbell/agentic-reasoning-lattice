# Channel Assignment — ASN-0036 review-110

**Date:** 2026-05-28 19:45

## Issue 1: The "k = 0 trivial / k ≥ 1 only load-bearing for nⱼ ≥ 2" message is restated six times across S8
Reason: Pure editorial deduplication — the claim already exists correctly in the proof body; the fix is to remove its five redundant restatements and let contract slots cite dependencies plainly. Derivable from the ASN alone.

## Issue 2: Verbatim "S0 discharges the persistence step" sentence repeated in five Depends blocks
Reason: Editorial deduplication — the S0-persistence bridge is a generic fact already stated in the ASN; collapse to one statement and cite by name. No external channel needed.

## Issue 3: Text-subspace-only / link-subspace-deferred caveat repeated across the contiguity section
Reason: Editorial consolidation — bind the text-subspace restriction once at the section head and drop per-property restatements. The link/text distinction is already established in the ASN's own prose, so no channel is required.

## Issue 4: S7c forward-reference essay explains its placement rather than advancing S7
Reason: Editorial removal — the placement-justification meta-prose duplicates content already in S8's Depends block; deletion is internal.

## Issue 5: S8a is labeled "axiom" but carries a multi-conjunct derivation — which conjuncts are axiomatic is ambiguous
Reason: Internal presentation choice — the ASN already contains both the structural commitment and the derivation of `zeros(v)=0`/positivity; resolving the axiom-vs-definition framing is a coherence fix derivable from existing content without design intent or implementation evidence.
