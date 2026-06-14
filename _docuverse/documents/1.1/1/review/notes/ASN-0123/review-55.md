# Review of ASN-0123

I checked the apparatus and every proof. The rigor is genuinely high: SA, VN-B1, nextv/nextd well-definedness, V-WF (including the protected cross-owner O5(ii) discharge), V8/V9 severance, and both worked instances are all sound — I found no missing cases, no skipped conjuncts, and no hand-waves in the logic. The two worked instances satisfy the concrete-example requirement and the cross-owner one is a well-judged contrast. n=0, |A|<n, the empty/links-only cross-owner source, and the boundary-vs-interior atomicity question are all handled.

This note carries `review-mode.anti-bloat`. The findings below are prose-accretion, not logic errors: facts stated two or three times within or across claims, around the (sound) forward-reference structure.

## REVISE

### Issue 1: V1 restates its own one-line claim three times over
**ASN-0123, V1 (ZeroContentFootprint)**: the claim is `C' = C ∧ L' = L`. The paragraph then carries: "no allocated substance scales with the source"; "allocates zero content and link addresses, **whatever the source's extent**"; "**A source of any size** forks at the same cost in allocated substance: none." It also restates the equation a third time — "the frame equality `C' = C` is that prohibition stated positively" — and re-announces G2's conclusion — "The G2 derivation showed this clause is not an economy but a prohibition."
**Problem**: source-size-independence is stated three times and the frame equality three times; the "block representation compresses … by V2's representation invariance" sentence is implementation detail that recurs in the evidence section; the G2 sentence restates a result already derived. A reader tracking the claim wades past the same fact repeatedly.
**Required**: keep the equation and the genuinely informative `ΔE = {v}` / `ΔM` / `ΔR = A × {v}` characterization; state source-size-independence once; drop the duplicate frame-equality restatement and the G2 re-announcement (a back-cite suffices).

### Issue 2: the node-tier exclusion is fully explained in P-tier, then re-derived in V0
**ASN-0123, contract P-tier scope note**: already gives the complete rationale — "a node-tier non-owner … commands no document-producing namespace — one K.δ off `pfx(π)` at depth 2 yields `inc(pfx(π), 2) = [pfx(π), 0, 1]`, an Account … not a Document — so forking a foreign document there would demand minting both an account and a document under it."
**ASN-0123, V0**: re-explains the same exclusion — "P-tier confines the operation to exactly these two branches — its domain condition restricts the cross-owner case to an account-tier forker, excluding the node-tier non-owner — so no third branch contributes to the count."
**Problem**: V0 legitimately needs to assert "exactly one identity," but it re-derives *why* node-tier is out rather than citing the precondition that already settled it. V-WF and V9 cite P-tier crisply; V0 re-argues it.
**Required**: V0 cites P-tier's resolved domain (owned ∪ account-tier-cross-owner) instead of restating the exclusion logic.

### Issue 3: V7 and VD both state "cross-owner forks are severed, recoverable only via shared content"
**ASN-0123, V7 (NavigationAsymmetry)**: "cross-owner versions are *not* recovered here: a cross-owner fork's result is severed from the source's subtree (V9), so no address-based descendant scan reaches it."
**ASN-0123, VD**: "Such a derivation escapes every address-based descendant scan … and is recoverable only through the shared-content witness (V9w), never the registry."
**Problem**: the same derived fact — V9's severance ⟹ not address-discoverable ⟹ recoverable only via V9w — is developed in two sections in different words. Each section has its own reason to invoke it (navigation completeness; refuting the unrestricted `derives` biconditional), but the shared kernel is stated twice in full.
**Required**: state the kernel once (VD is the natural home, since the severance is load-bearing for the biconditional's failure) and have V7 cite it.

## OUT_OF_SCOPE

The scope boundaries are drawn correctly. The note defines no claim for document creation, comparison, content/link operations, delivery, or replication, and the Open Questions defer the genuinely future topics (windowing-against-evolving-source, withdrawal semantics, concurrent-fork serialization, correspondence under divergence) as questions rather than smuggling them in as claims. No OUT_OF_SCOPE additions are warranted.

VERDICT: REVISE
