# Review of ASN-0131

This is a strong, careful note. The three substantive derivations — RE-UDIST (pulling the region-independent `touch_W(e)` out of the existential and reducing to `{(i,e) ∈ Avail : touch_W}`), RE-SEL (`findlinks_V ∩ addressable`), and RE-CWP (the I-address-level `I_R`/`Δ` partition, which correctly survives the non-injective arrangement and is genuinely strictly finer than D-CWP) — all check out step by step. The decidability argument correctly distinguishes the finite point-set `I` from the infinite interval `coverage(e)`. The RE-RET deduplication subtlety (link-level permanence vs. pair-value-level removal) is handled with real precision. Three issues remain.

## REVISE

### Issue 1: Worked example — the type-endset miss is not entailed by its stated premise

**ASN-0131, "A worked instance"**: "type-endset `e₃ = {(θ, δ(1, #θ))}` — `θ` a classifying address disjoint from content (`θ ∉ dom(Σ.C)`) … `touch_W(e₃) = {t : θ ≼ t} ∩ {a₂} = ∅` — the type address is disjoint from content; it **misses**."

**Problem**: `coverage(e₃) = {t : θ ≼ t}` (PrefixSpanCoverage). The test misses iff `θ ⋠ a₂`. But `θ ∉ dom(Σ.C)` does **not** entail `θ ⋠ a₂`. A `θ` that is, e.g., the document-level prefix of `a₂` satisfies `θ ∉ dom(Σ.C)` (it is document-level, `zeros = 2`, not element-level) yet `θ ≼ a₂`, putting `a₂ ∈ coverage(e₃)` and making the test **hit**. The mandatory concrete example thus asserts a result its stated premise cannot support — the conclusion is true only for an unstated additional assumption on `θ`.

**Required**: Strengthen the premise so the miss follows: place `θ` in a distinct (type) subspace, whence by T7 `coverage(e₃) ∩ dom(Σ.C) = ∅` and `a₂ ∉ coverage(e₃)`; or state `coverage(e₃) ∩ dom(Σ.C) = ∅` directly; or simply assert `θ ⋠ a₂`. (The prose word "disjoint from content" is the property needed at the *coverage* level; the parenthetical formalization `θ ∉ dom(Σ.C)` is about `θ` alone and is too weak.)

### Issue 2: RE-CLIP tabulates a provisional convention as a load-bearing guarantee

**ASN-0131, RE-CLIP (claims table)**: "Unclipped extent — a surfaced endset is reported entire, its spans at their full recorded coverage extent, never truncated to the region boundary" — status **introduced**.

**Problem**: The ASN's own prose, in the "Faithfulness" section, separates two things and explicitly demotes one of them: "That the *whole* endset is surfaced is the faithful reading we adopt here … is discussed under open questions. Either way, no span is *clipped* … **That weaker invariant** [no clipping] **is the one both readings share, and the one we hold load-bearing**." So by the ASN's own account, *entirety* (all spans) is an adopted reading, while only *no-clipping* (no reported span truncated) is load-bearing. Open Question 1 then reopens entirety outright: "Must a surfaced endset be reported in its entirety, or only those of its spans that intersect the region?" RE-CLIP bundles the provisional convention (entire) with the firm invariant (no truncation) into one **introduced** claim, so a downstream reader cannot tell which part is stable. An alternative implementation surfacing touching-spans-only (the alternative the ASN itself flags) would violate RE-CLIP-as-written while honoring everything the ASN calls load-bearing.

**Required**: Give the load-bearing invariant its own claim (no reported span is truncated/clipped — universal across both readings), and state entirety (whole endset surfaced) separately as the adopted convention, marked provisional pending Q1. Alternatively, commit to entirety as a guarantee and close Q1. As tabulated, the claim's status and Q1 contradict.

### Issue 3: LP17/LP18 are cited for region-local unreachability, but their preconditions are global

**ASN-0131, "Stability" (deletion bullet) and RE-EDIT**: "it is merely no longer reachable through `d`. It is *orphaned* from this region (LP17, ASN-0098), not destroyed; should the content be re-arranged into `d`, the endset is surfaced again (resurrection, LP18, ASN-0098)." RE-EDIT repeats: "deletion orphans anchoring whose content departs the region (…; orphaning LP17, resurrection LP18, ASN-0098)."

**Problem**: LP17 (GhostProjection) is a *global* statement — its premise is "(A d ∈ dom(Σ.M), i : … coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) = ∅)" and its conclusion is "not discoverable from *any* document." A K.μ⁻ deletion from one region `W` of one document `d` does not establish that premise: the link may still touch other regions of `d` or be reachable from other documents. The link is "unreachable through this region," which is *not* LP17's orphaning. Symmetrically, LP18's resurrection has precondition "`a` is orphaned at `Σ`" (LP17's global conclusion); region-local re-surfacing on re-arrangement does not require, and is not licensed by, that precondition. The conclusions the ASN draws (the link persists; it re-surfaces when content returns) are correct — but they follow from L12 (persistence) and image growth (F-IMG-MONO) plus the discoverability characterization (LP12), not from LP17/LP18, whose premises a region deletion does not meet.

**Required**: For the region-local case, cite the image-contraction result (F-IMG-CONTR) with the projection/discoverability characterization (LP10/LP12, ASN-0098) for "no longer reachable through `d`," and F-IMG-MONO/LP9 for re-surfacing on re-arrangement; reserve LP17/LP18 for the genuinely global case (departed content reachable from no document). Or restate without the global-orphaning vocabulary.

## OUT_OF_SCOPE

None. The six open questions (entirety vs. touching-spans, multiplicity preservation, rendered V-position mode, intersection-distributivity, cross-store completeness, type-slot-against-content semantics) are correctly deferred rather than answered, and the note does not stray into FINDLINKS*/READLINK/FOLLOWLINK/MAKELINK territory — those are named only for contrast.

VERDICT: REVISE
