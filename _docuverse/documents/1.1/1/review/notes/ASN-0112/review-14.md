# Review of ASN-0112

## REVISE

### Issue 1: Defensive citation-choice justification plus use-site inventory in the S3★ bullet
**ASN-0112, "The substrate we measure" (S3★ bullet)**: "We use the per-subspace S3★ rather than the content-only S3 (ASN-0036) precisely because this ASN admits link V-positions into `O(d)` (V5 link-only case, V6, the worked example); a link position's image lies in `dom(L)`, not `dom(C)`."
**Problem**: This is meta-prose. The clause "precisely because this ASN admits link V-positions…" defends *which foundation invariant was cited* rather than stating what S3★ says, and the parenthetical "(V5 link-only case, V6, the worked example)" is a downstream use-site inventory — exactly the "definition's introduction enumerates downstream consumers" pattern flagged for this note. The reasoning that link images live in `dom(L)` is already carried where it is used (V14).
**Required**: State the S3★ bullet as what the invariant guarantees. Drop the citation-choice defense and the use-site inventory.

### Issue 2: Forward reference announcing a distinction without advancing it (S6 bullet)
**ASN-0112, "The substrate we measure" (S6 bullet)**: "These two conditions are genuinely different, and the difference is load-bearing in the reach analysis below (V2)."
**Problem**: The sentence advances no reasoning — it only promises that a distinction defined elsewhere will matter later, pointing forward to V2. A reader gains nothing here that V2 does not establish at the point of use. This is the "prose that does not advance reasoning is noise" pattern.
**Required**: Delete the forward-reference sentence; let the level-uniform vs. endpoint-level-compatible distinction earn its keep at V2 where it is actually consumed.

### Issue 3: The level-uniform / endpoint-level-compatible distinction is belabored across sections
**ASN-0112, V2 and V17**: V2: "This is an endpoint condition, genuinely distinct from span level-uniformity, and the two point opposite ways: …"; V17: "by the V2 reach biconditional, the endpoint condition `#origin_d ≤ #reach_d` governs only `reach(σ_d) = reach_d`, not T12 legality."
**Problem**: The same point — that T12 legality/coverage is independent of any endpoint depth relation, and that only the *equality* `reach(σ_d) = reach_d` depends on it — is stated in the S6 bullet, re-explained at length in V2 ("the two point opposite ways"), re-flagged in V17, and replayed in the worked-example variant. The reach biconditional is the single load-bearing fact; the surrounding "genuinely distinct… point opposite ways" framing is restated more often than the argument needs.
**Required**: Establish the reach biconditional and the level-uniformity aside once (in V2); have V17 and the worked example *use* it by reference rather than re-narrate the distinction.

## OUT_OF_SCOPE

### Topic 1: Per-subspace exact extent recovery (span-set report)
**Why out of scope**: V7 and Open Question 1 correctly route exact per-subspace tracing to a span-set operation (RETRIEVEDOCVSPANSET / ASN-0113). Each mention is in a legitimate slot (V7 = structural impossibility for a single span; Open Questions = future work), so no revision is needed — noted only to confirm the deferral is appropriately placed, not duplicated bloat.

VERDICT: REVISE
