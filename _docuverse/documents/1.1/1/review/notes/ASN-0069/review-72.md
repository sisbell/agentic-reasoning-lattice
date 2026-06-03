# Review of ASN-0069

## REVISE

### Issue 1: V8 defers subsequent-fork transitive correspondence to V11, but V11 cannot express the version sibling-stream

**ASN-0069, V8**: "the transitive `d_src ↔ d_new` correspondence for the subsequent-fork case (where `d_op ≠ d_src`) requires an unedited-source premise carrying agreement across the `d_src → d_op → d_new` hops, and is stated and discharged in V11 rather than asserted here."

**Problem**: V11's chain requires *each step to be the first fork of its immediate source* — `dⁱ_new = inc(dⁱ⁻¹_new, 1)`, a strictly deepening chain (V11a proves `#dⁱ_new = #d_src + i`). But a *subsequent fork of `d_src`* produces `d_new = inc(d_prev, 0)` in `A_v(d_src)`'s sibling stream (V1, J4 operand-tracking). Here `d_prev` and `d_new` are **siblings** (both forks of `d_src`, both length `#d_src + 1`), not a first-fork parent/child pair: `d_new` is `A_v(d_src)`'s next emission, *not* `A_v(d_prev)`'s. So the `d_src → d_op` hop is itself a sibling-stream relationship that V11's first-fork chain structure cannot represent — V11 does not discharge this case. The deferral target is wrong: the version stream (repeatedly forking one source) is exactly the configuration V8 punts on, and it is the configuration V11 excludes.

The worked example exposes the dependence: §"Subsequent fork of `d_src`" asserts `M²(d_new²)` holds `a₁,a₂,a₃` "precisely when `d_new` has not been edited," i.e. it composes V8 (`d_src ↔ d_new`, first fork) with V4 (`d_new → d_new²`, second fork) to reach `d_src`-content in `d_new²` — the very transitive correspondence claimed discharged by V11 but not actually established for sibling-stream versions.

**Required**: Either (a) generalize V11 to admit `inc(·, 0)` sibling-stream content hops (not only first-fork `inc(·, 1)` deepening steps), or (b) introduce a separate claim discharging `d_src → d_prev → d_new` transitive correspondence for subsequent forks, or (c) correct V8's deferral to state the subsequent-fork transitive case is not formally established and remove the worked-example reliance on it.

### Issue 2: V4 design-commitment point restated three to four times

**ASN-0069, §"The Arrangement Layer"**: the lead-in before V4 ("a design commitment of this ASN, strengthening J4's clause (ii)... Literal inheritance fixes φ to be the identity"), the V4 box, the "V4 *strengthens* J4's clause (ii). J4 constrains the *range*..." paragraph, and the "V4 commits to *full literal inheritance*... a design commitment of this ASN — not derivable from J4 alone" paragraph each make the same point: V4 = J4 + φ-is-identity, adopted as a design commitment.

**Problem**: Four consecutive passages restate "V4 strengthens J4 by fixing φ to the identity; this is a design commitment, not derivable from J4." This is the "two paragraphs say the same thing in different words" pattern compounded. The precise reader must skip past the repetition to find the two structural-justification subparts ("Why V-positions are not rebased," "Why I-addresses are not rebased") that actually advance the argument.

**Required**: State the design-commitment/φ-identity relationship once (the V4 box or its lead-in), then proceed directly to the two structural justifications. Delete the redundant restatements.

### Issue 3: V6a carries dependency-justification meta-prose

**ASN-0069, V6a preamble**: "These three definitions are local constructs over the foundation vocabulary; no further foundation ASN is consumed."

**Problem**: The clause "no further foundation ASN is consumed" is a defensive justification about dependency usage; it does not advance the meaning of `coverage`, `project`, or `discoverable_from`. Anti-bloat noise.

**Required**: Drop the clause; keep only the definitions themselves.

### Issue 4: V6 counterfactual paragraph imagines a transfer the operation already excludes

**ASN-0069, §"Subspace Selectivity"**: "Suppose, for contradiction, that a fork transferred the content source `d_op`'s link-subspace V-positions to `d_new` under transclusion."

**Problem**: J4's clause (ii) populates `M'(d_new)` only from `V_{s_C}(d_op)` (content subspace); the fork composite never offers link-subspace positions to K.μ⁺. The paragraph reasons about a case the operation's definition excludes. The actual derivation of V6 (K.δ initialises `M'(d_new)=∅`; K.μ⁺ adds only `s_C` positions) is already in the V6 box and suffices.

**Required**: Remove the counterfactual paragraph, or compress its CL-OWN observation into a single sentence noting why the content-subspace restriction is principled rather than arbitrary.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork during source modification
The first Open Question (concurrency beyond the sequential atomic axiom) is correctly future territory, not a gap in this ASN.

### Topic 2: Snapshot vs. living fork semantics
Distinguishing frozen-at-fork-time arrangements from live-tracking forks is a future invariant, appropriately deferred.

VERDICT: REVISE
