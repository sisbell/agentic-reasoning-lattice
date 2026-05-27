# Review of ASN-0069

## REVISE

### Issue 1: V12(d) derivation parenthetical mis-states the one-sided containment

**ASN-0069, V12(d) derivation**: "V4 alone supplies only the one-sided containment `ran(M'(d_new)|_{V_{s_C}(d_src)}) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})`; V4b is needed to rule out V-positions outside `V_{s_C}(d_src)` in `dom(M'(d_new))` that would otherwise contribute I-addresses outside `ran(M(d_src)|_{V_{s_C}(d_src)})`."

**Problem**: The formula has the restriction `|_{V_{s_C}(d_src)}` applied on both sides. With this restriction, V4 alone supplies **equality**, not just ⊆: V4's pointwise equality `M'(d_new)(v) = M(d_src)(v)` for every `v ∈ V_{s_C}(d_src)` directly yields `ran(M'(d_new)|_{V_{s_C}(d_src)}) = ran(M(d_src)|_{V_{s_C}(d_src)})`. The "only the one-sided containment" qualifier is therefore inaccurate — V4 already gives equality on the restriction.

The actual gap V4b fills is at the *unrestricted* level: V4 alone supplies `ran(M(d_src)|_{V_{s_C}(d_src)}) ⊆ ran(M'(d_new))` (the reverse direction, without the LHS restriction), since the inherited positions contribute their I-addresses to `ran(M'(d_new))`. V4b is needed to close this to equality by establishing `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})` via `dom(M'(d_new)) = V_{s_C}(d_src)`.

The subsequent prose ("V4b is needed to rule out V-positions outside `V_{s_C}(d_src)`...") describes the correct gap, but the formula written above it has the wrong directionality/restrictions to match that prose.

**Required**: Either drop the LHS restriction to read `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})` (which is the containment V4b establishes, complementing V4's reverse containment), or rephrase the parenthetical to state explicitly that V4 supplies equality on the restriction `M'(d_new)|_{V_{s_C}(d_src)}` but leaves `dom(M'(d_new)) \ V_{s_C}(d_src)` unconstrained, which V4b closes.

VERDICT: REVISE
