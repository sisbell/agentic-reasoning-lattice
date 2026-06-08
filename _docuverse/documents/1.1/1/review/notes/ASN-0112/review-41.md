# Review of ASN-0112

## REVISE

### Issue 1: Tight's wp derivation misattributed to V5/V6
**ASN-0112, Preconditions and well-definedness**: "Reasoning backward from `Tight`, exactly as the `Exact` factoring ran through V5 and V6: if `O(d)` is empty... if `O(d) ≠ ∅` and `#origin_d ≤ #reach_d`, then D1 closes the round-trip..."
**Problem**: The phrase "exactly as the `Exact` factoring ran through V5 and V6" is wrong. `Exact`'s wp factors through subspace count (V5 single-subspace ⟹ exact, V6 two-subspace ⟹ not). `Tight`'s wp factors through *endpoint depth* via D1/D0, as the very next clauses make explicit (`#origin_d ≤ #reach_d` ⟹ D1; `>` ⟹ D0). These are orthogonal axes — the text even calls them "the orthogonal endpoint axis." The V5/V6 reference is a phrase pattern-matched from the preceding `Exact` paragraph and misdirects the reader to the wrong premises.
**Required**: Replace "exactly as the `Exact` factoring ran through V5 and V6" with a reference to D0/D1 (or "by the same two-direction exhaustive method, here on endpoint depth via D1/D0").

### Issue 2: V-ReachTight duplicates V2's own reach-equality clause
**ASN-0112, Claims table / V2 / V-ReachTight**: V2 states "the actual reach `r⋆ = origin_d ⊕ extent_d ≥ reach_d`... with equality `r⋆ = reach_d` iff `#origin_d ≤ #reach_d`." V-ReachTight states "`reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d`."
**Problem**: Since `reach(σ_d) = origin_d ⊕ extent_d = r⋆` by definition (σ.reach, ASN-0053), V-ReachTight is *literally* V2's equality clause relabeled as a separate claim. The same biconditional is asserted twice. This is claim duplication — two labeled statements saying the same thing in different words.
**Required**: Either fold the iff entirely into V2 (drop the standalone V-ReachTight label), or strip the equality clause from V2 and let V-ReachTight carry it alone. Do not state it as two claims.

### Issue 3: wp digression computing `wp(…, V-ReachTight) = true` only to discard it
**ASN-0112, Preconditions and well-definedness**: "The companion reach property factors the same way along the orthogonal endpoint axis, but we must take care which property we put under the wp. V-ReachTight is the *universally-valid biconditional*... A property that holds in all reachable states is, as a postcondition, always satisfied, so `wp(RETRIEVEDOCVSPAN(d), V-ReachTight) = true` — the entire pre-state space, which tells the caller nothing."
**Problem**: This is methodological essay content in a structural slot — it computes a wp expressly to reject it, explaining the reviser's choice of postcondition rather than advancing the specification. The carried by `review-mode.anti-bloat`: meta-prose the precise reader must skip past. The contingent `Tight` property and its wp can be stated directly without first walking through the unsuitable candidate.
**Required**: Cut the V-ReachTight=true digression. Introduce `Tight` as the contingent property and give its wp directly. If a one-line contrast is wanted, it belongs in at most a single clause, not a paragraph.

## OUT_OF_SCOPE

(none — the ASN confines itself to the boundary query; content delivery, per-subspace reporting, link counting, and version comparison are correctly deferred to the Open Questions and not given claims here.)

VERDICT: REVISE
