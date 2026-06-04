# Review of ASN-0101

## REVISE

### Issue 1: Reconstruction reasoning is split across two passages that both defer to out-of-scope versioning
**ASN-0101, D2 (third bullet)**: "Prior versions of `d` can be reconstructed. Reconstructing the pre-DELETE arrangement requires only `M(d)` (which the system retains as a prior version, when versioning is in effect) and `C` (which is unchanged)."

**ASN-0101, "A note on recoverability and historical reconstruction"**: "DEL alone is not sufficient: it does not preserve `M(d)`, and recovering the pre-state arrangement from `M'(d)` alone is impossible... The full versioning mechanism that would close this gap is out of scope here; Open Question 1 carries the rest."

**Problem**: Two passages cover the same reconstruction topic, both pivoting on a versioning mechanism the ASN explicitly puts out of scope. The D2 bullet asserts reconstructability as a positive consequence ("can be reconstructed"); the later section walks it back ("DEL alone is not sufficient"). This is the deferral-to-same-downstream-location pattern, and the D2 bullet's claim is load-bearing only on the out-of-scope versioning component (`M(d)` "retained... when versioning is in effect"), not on anything D2 itself establishes. The genuine in-scope fact — DEL is information-destroying with respect to `M(d)` — is one sentence.

**Required**: Drop the reconstruction bullet from D2 (whose actual content is content-store immutability, `dom(C') = dom(C)`), and reduce the recoverability material to a single statement of the in-scope fact (DEL does not preserve `M(d)`; reconstruction is a versioning concern, out of scope). Do not assert reconstructability as a DEL consequence when the mechanism enabling it is out of scope.

### Issue 2: D9 prose duplicates the LP-family extension that D10 owns
**ASN-0101, paragraph after D9**: "The link itself is never lost; that paragraph confirms LP17 and LP18 carry to the DEL-extended vocabulary."

**Problem**: The forward reference points at D10's *LP-family extension under DELETE* paragraph, which is where LP17/LP18 carry-over is actually discharged (via D3 fixing the link store and LP3★). The D9 prose restates that conclusion rather than advancing D9's own claim (the projection characterisation), and creates a second site asserting the same LP carry-over result.

**Required**: State only D9's projection consequence (discoverability can shrink to zero / rename) and let D10 carry the LP-family extension; remove the duplicated LP17/LP18 assertion from the D9 discussion.

## OUT_OF_SCOPE

### Topic 1: Causal ordering and full reversibility of DELETE
**Why out of scope**: The Open Questions on causal ordering between cross-document DELETEs and on full reversibility relative to an observer's view are genuine future territory, correctly deferred — not gaps in this ASN's frame.

VERDICT: REVISE
