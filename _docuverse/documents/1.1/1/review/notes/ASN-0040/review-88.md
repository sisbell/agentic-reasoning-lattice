# Review of ASN-0040

## REVISE

### Issue 1: B7 "non-nesting prefixes" illustration uses reasoning foreign to B7's proof

**ASN-0040, "B7 illustrated — non-nesting prefixes"**: "We now exhibit two namespaces whose elements share a length yet remain disjoint because their parents are non-nesting. From state B₂ above, the parents [1, 0, 1] and [1, 0, 2] are both length 3, distinct, and neither is a prefix of the other..."

**Problem**: This case (`#p = #p' = 3`, `d = d' = 1`) is exactly B7's **equal-length-parents** sub-case, which B7 closes by: "The first #p components of x equal both p and p', so p = p' by T3, whence (p, d) = (p', d') — contradicting (p, d) ≠ (p', d')." B7's proof never cases on nesting; it splits on element length, then parent length. The illustration instead attributes disjointness to non-nesting and re-derives it via "T1's lexicographic comparison resolving at the first position of disagreement" — a mechanism B7 does not employ. The non-nesting/nesting dichotomy set up by the two illustrations is reviser drift (a T10-style partition-independence taxonomy) that does not match the theorem it claims to illustrate. A reader who maps the illustration back to B7 will not find the "non-nesting" reasoning there.

**Required**: Align the illustration with B7's actual case structure — relabel it as the equal-length-parents case and show the p = p' contradiction — or drop the "because their parents are non-nesting" causal claim. Keep the "nesting prefixes" illustration (it correctly tracks B7's unequal-length-parents / T4-last-nonzero case).

### Issue 2: Forward-reference meta-prose deferring to B3

**ASN-0040, "baptismal registry" / binary-character paragraph**: "Whether anything is *stored* at that position is a separate question, which we address below as the ghost validity property."

**Problem**: This is a bare forward pointer to B3 that advances no reasoning at its site; the ghost/occupied distinction is then stated again in the B3 section and again in the Open Questions. Three locations defer to or restate the same downstream content — the deferral pattern the anti-bloat pass targets.

**Required**: Remove the forward pointer; let B3 stand on its own where it is introduced.

### Issue 3: Essay commentary in B6 that does not advance the proof

**ASN-0040, B6**: "At most three level crossings can occur in a valid address chain: node → user, user → document, document → element. This is the four-field structure of T4, now visible as a consequence of baptism depth arithmetic rather than an independent syntactic constraint."

**Problem**: This is interpretive commentary contrasting "consequence of arithmetic" vs "independent syntactic constraint." It restates T4's content already established by the foundation and adds no step to B6's necessity/sufficiency argument. The table immediately above already conveys the level-crossing structure.

**Required**: Cut, or compress to the single factual line ("d = 2 crosses one level; the four-field cap follows from condition (iii)").

## OUT_OF_SCOPE

### Topic 1: B3's Occupied predicate and the content-permission requirement

**ASN-0040, B3**: introduces `Occupied : T × 𝒮 → {⊤, ⊥}` and the requirement that "content is permitted only at baptized addresses."

**Why out of scope**: Content storage and retrieval are explicitly out of scope (deferred). The ghost-element *motivation* (a baptized position need not carry content) is legitimate baptism context, but the formal predicate and the operational requirement on future Occupied-introducing operations are content-storage obligations that belong in that future ASN. B3 as a "forward requirement" reaches into deferred territory; the binding constraint should be stated where Occupied is actually defined.

VERDICT: REVISE
