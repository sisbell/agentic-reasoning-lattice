# Review of ASN-0099

This ASN carries the `review-mode.anti-bloat` classifier. The mathematical core is sound — the two-phase factoring, the conformance obligations (F2–F3 and variants), the determinism/inertness chain (F8/F9/F9-λ), and the worked example all hold up under checking, and boundary cases (empty query, empty store, empty constraint set/target, empty scope) are covered in a dedicated section. My findings are accreted meta-prose, matching the patterns the classifier directs me to surface.

## REVISE

### Issue 1: "Predicate domain" paragraph imagines a case the definitions already exclude
**ASN-0099, Completeness**: "*Predicate domain.* `matches(a, I, Σ)` is defined only for `a ∈ dom(Σ.L)`. The scoped form's `a ∈ dom(Σ.L) ∩ S` clauses ... keep every invocation inside the domain; F2-V and F3-V respect the convention ... The boundary case `a ∈ S ∖ dom(Σ.L)` is operationally excluded by F3-sco."

**Problem**: This is the reviser-drift pattern "a paragraph imagines a case the claim's carrier or precondition already excludes." `findlinks_scoped` is *defined* as `{a ∈ dom(Σ.L) ∩ S : matches(a, I, Σ)}` (F14); the quantifier in every form already restricts to `dom(Σ.L)`, so `matches` is never invoked outside its domain by construction. Worrying about `a ∈ S ∖ dom(Σ.L)` and re-asserting that each form "respects the convention" is bookkeeping over a guarantee the definitions enforce structurally.

**Required**: Delete the paragraph. The domain restriction is visible in the definitions; nothing downstream depends on the prose.

### Issue 2: The F2-X ∧ F3-X paragraph restates the displayed conformance equations
**ASN-0099, Completeness**: immediately after the block displaying `F2-filt ∧ F3-filt: result_filtered(C, Σ) = findlinks_filtered(C, Σ)` etc., the prose "Each labeled pair `F2-X ∧ F3-X` conjoins the completeness containment ... with the soundness containment ..., the predicate adjusted to the operation: the universal ... for the filtered form, the intersection ... for the scoped form, and the I-image ... for the V-side form. The conjunction forces the equality stated above."

**Problem**: "Two paragraphs say the same thing in different words." The displayed equations already state each equality; the analogue of "F2 ∧ F3 force `result(I, Σ) = findlinks(I, Σ)`" was already given one paragraph earlier for the base case. Re-walking each predicate adjustment (universal / intersection / I-image) duplicates content the reader can read off the equation block and the corresponding definitions.

**Required**: Collapse to a single clause noting the same conjunction-forces-equality argument applies per form, or drop entirely — the labeled equations carry the claim.

### Issue 3: Implementation/index commentary in the Completeness obligation
**ASN-0099, Completeness**: "No early termination, sampling, or remote-latency exclusion. Soundness's dual force: no false positives from stale indexes. A conforming implementation's index, if any, remains in lockstep with the link store. The mechanism is unspecified: any implementation whose `result(I, Σ)` differs from the comprehension is non-conforming, regardless of cause."

**Problem**: Essay content in a structural slot. The abstract obligation is already pinned by `F2 ∧ F3 ⟹ result = findlinks`. The added prose about "stale indexes" and an index "in lockstep" is implementation-flavored elaboration of a mechanism the ASN explicitly disclaims ("Caching" and "The procedure by which the operation is computed" are listed under *What We Have Not Specified*). The "regardless of cause" rhetoric restates the set equality a third time.

**Required**: Reduce to the load-bearing sentence — any `result(I, Σ)` differing from the comprehension is non-conforming — and drop the index/lockstep commentary, which trades on the very implementation notions the ASN leaves open.

## OUT_OF_SCOPE

None. The ASN correctly confines INSERT/DELETE/COPY/REARRANGE, versioning, and replication to foundation operations used only in the worked example, and lists them (plus caching, access control, the inverse direction) under *What We Have Not Specified* rather than defining mechanics.

VERDICT: REVISE
