# Review of ASN-0131

This is a strong, technically sound note. I checked the core claims and found them correct:

- **RE-DEF / soundness / completeness** are a genuine biconditional read-off; the factoring `RE(W,d,Σ) = { (i,e) ∈ Avail(Σ) : touch_W(e) }` (touch depending only on `e`, not `a`) is valid and underwrites union-distributivity.
- **RE-UDIST and the intersection `⊆` half** check out: forward image distributes over union exactly, and `image(W₁∩W₂) ⊆ image(W₁)∩image(W₂)` carries the `⊆` direction unconditionally; the `⊇` failure under non-injectivity is correctly identified and deferred.
- **RE-CWP** (contraction wp) is correctly derived: post-image `= I_R`, drop-condition `coverage(e)∩Δ≠∅ ∧ coverage(e)∩I_R=∅`, boundary `R=∅ ↦ RE=∅`. This is a real non-trivial wp.
- The **worked example** verifies RE-OVL, RE-CLIP, RE-WHOLE, per-endset, and RE-UNIT against a concrete state; the `coverage(e₃) ∩ dom(Σ.C) = ∅` field-agreement argument (third-zero ⇒ shared subspace position ⇒ `E(c)₁ = s_type ≠ s_C`) is sound.
- **RE-RET** is carefully argued: R-Scope confines the new nullification to `ℓ`, the emitter `b`'s from/to slots are content-disjoint (unit-depth prefix argument), and the "sole addressable bearer" biconditional is correctly split.

The findings below are prose/bloat issues flagged under the `review-mode.anti-bloat` mandate, not correctness defects.

## REVISE

### Issue 1: The M-only-lift paragraph restates two facts three to four times each
**ASN-0131, "Stability" → the paragraph beginning "The user-facing insert and delete that shift content are not these atomic movers..."**

The delete-depth-2 limitation is stated four times: "(D-SHIFT, established there only at text depth #p = 2)"; then "D-SHIFT realises an interior-span deletion only at text depth #p = 2 ... cannot stand in"; then "delete-stability is claimed at text depth #p = 2 ... its existence above depth 2 is not yet foundation-established"; then again "(insert: every text depth #p ≥ 2; delete: text depth #p = 2, where D-SHIFT holds)" in the following paragraph.

The "writes only `Σ.M(d)`, hence frames L/E/R" point is likewise stated three to four times: "an M-only edit, writing no store but the queried document's arrangement"; "the embedded operation frames them — M-only ⟹ frames L, E, R"; "The link store in particular is left fixed (L' = L)"; "frames L, E, R for any M-only edit at any content depth."

**Problem**: This is exactly the forward-reference accretion the classifier targets. The meta-distinction "The lift's reasoning is depth-independent ... not on D-SHIFT's #p = 2 ... What it does not do is supply a delete where the foundation provides none" belabors a single fact (the depth-2 ceiling comes from delete-*existence*, not from the framing) across several sentences.
**Required**: State each fact once — (i) insert is foundation-realized at every text depth `#p ≥ 2`, delete only at `#p = 2` (D-SHIFT), so delete-stability is scoped to `#p = 2`; (ii) the edit writes only `Σ.M(d)`, framing L/E/R, so `Avail(Σ)` is fixed and only the image can move — and excise the remaining restatements.

### Issue 2: Bookend restatement in the link-subspace-confined-edits paragraph
**ASN-0131, "Stability" → the paragraph beginning "Finally, a whole class of arrangement edits to d itself leaves a content-region answer fixed..."**

Opening: *"a whole class of arrangement edits to d itself leaves a content-region answer fixed — by a route particular to the content-subspace restriction."* Closing: *"The content-subspace restriction is what secures the entire class: every link-subspace-confined arrangement edit on d leaves a content-region answer fixed."*

**Problem**: The closing sentence asserts the identical proposition as the opening (class-level stability, attributed to the content-subspace restriction). With "Either edit gives `RE(W, d, Σ') = RE(W, d, Σ)`" already concluding both the `K.μ⁺_L` and link-only `K.μ⁻` cases, the closing adds no content.
**Required**: Drop the closing restatement; the two cases plus "Either edit gives..." already carry the class claim. (Minor.)

## OUT_OF_SCOPE

The note's Open Questions (whole-endset vs touching-spans, multiplicity preservation, V-position rendering, intersection `⊇`, cross-server completeness, type-slot-against-content, link-subspace regions) are all genuinely future territory and are correctly deferred rather than half-answered. The conditional framing of RE-RET on `coverage(Θ) ∩ dom(Σ.C) = ∅`, with its sole exception routed to OQ6, is an honest scoping, not a gap. Nothing to add here.

VERDICT: REVISE
