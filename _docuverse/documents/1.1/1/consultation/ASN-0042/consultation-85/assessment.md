# Channel Assignment — ASN-0042 review-85

**Date:** 2026-05-30 00:29

## Issue 1: Near-verbatim duplicate deferral within the same section
Reason: Purely editorial deduplication — three copies of the same transfer-deferral sentence collapse to one. The Open Questions already record the deferral; no design-intent or implementation evidence is needed to drop redundant prose.

## Issue 2: O6 corollary re-derives what the main biconditional already gives
Reason: Internal proof-structure fix — the O6 body already proves the biconditional for any principal with `zeros ≤ 1`, and `ω(a)` is such a principal, so the corollary is a one-line instantiation. Derivable from the ASN alone.

## Issue 3: Forward-pointer use-site inventory in BootstrapContainment
Reason: Editorial deletion of a sentence that inventories future call sites; the lemma and its one-line proof are self-contained. No external channel needed.

## Issue 4: O10 branch analysis fully duplicated between proof and worked example
Reason: Internal restructuring — the worked example should witness the proof's two `next`-branches on concrete tumblers rather than re-prove them with parallel O5/B6 checks. The branch lemma is already discharged in the Construction; no channel input is required to trim the example.

## Issue 5: DelegatorAllocatesPrefix closes with a restatement of its own conclusion
Reason: Editorial removal of a sentence that restates the just-proven postcondition in prose; the following Gregory evidence sentence stays. Derivable from the ASN alone.
