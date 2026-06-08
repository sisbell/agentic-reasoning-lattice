# Review of ASN-0102

## REVISE

### Issue 1: The self-transclusion worked example never exercises X10(b) where it is load-bearing
**ASN-0102, "A self-transclusion scenario (`Old ≠ ∅`)" and X10(b)**: The example sets source span over `[1,1],[1,2]` while copying at `v = [1,3]`, and cites "`resolve_Σ(R)` ... (X10(b) snapshot resolution, X15 atomicity)."

**Problem**: The source positions `[1,1],[1,2]` lie strictly below `v = [1,3]`, so they fall in the *unmoved* class — their image is identical in `Σ` and `Σ'`. Reading `resolve` against the pre-state therefore yields exactly the same result as reading it against the post-state: the snapshot/pre-state distinction is vacuous in this example. X10(b)'s distinctive content is precisely the hard case — copying positions at or after `v`, which the operation itself will displace ("the copied span is read against `Σ` *before the displacement opens the gap*"). That hazard is the whole reason X10(b) and X15 exist for self-transclusion, and no scenario in the ASN demonstrates it. Per the depth standard, a key postcondition with a non-trivial subtlety must be verified against a scenario where the subtlety bites; here the cited property is asserted, never exercised.

**Required**: Add (or convert) a self-transclusion example in which at least one source position satisfies `u ≥ v` (i.e., the copied span overlaps the displaced region). Show `resolve_Σ` extracting the pre-state image of those positions, the original content shifting to `[v+W, …)`, and the copied content landing at `[v, v+W)` — so that reading the post-state would give a different (circular) result. This makes X10(b)/X15 load-bearing rather than decorative.

## OUT_OF_SCOPE

### Topic 1: Discoverability of copied content after later displacement
**Why out of scope**: The first Open Question (what ties origin to continued discoverability when copied content is displaced again) concerns link projection under subsequent operations — future-ASN territory, not a gap in COPY's own contract.

### Topic 2: Time-varying / divergent views of the same referenced content
**Why out of scope**: The third Open Question (whether two references may be required to resolve to differing views across time) introduces versioning/temporal semantics beyond the single-transition COPY contract.

VERDICT: REVISE
