# Review of ASN-0131

## REVISE

### Issue 1: The "full taxonomy" of stability omits K.δ and K.ρ

**ASN-0131, Stability section (RE-EDIT)**: "The full taxonomy of what moves the answer is then: an arrangement edit to `d` changes `RE` *through the image*; creating a link (`K.λ`) ... may *add* a pair ...; a retraction may *remove* pairs ...; and `K.α`, together with edits to documents other than `d`, leaves `RE` fixed."

And the RE-EDIT claim itself: "edits to other documents leave the answer fixed (LP5, ASN-0098), as does content allocation `K.α` (LP6, ASN-0098)."

**Problem**: The transition vocabulary (ASN-0047) is {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ} plus the composite K.μ~. The "leaves fixed" bucket as written covers only K.α and "edits to documents other than `d`." Two transition kinds that demonstrably leave `RE` fixed are unaccounted for:
- **K.δ** (EntityCreation / document registration): for a fresh `e ≠ d`, frame gives `C'=C`, `L'=L`, and `M'(d)=M(d)` (only `e`'s empty arrangement is added; `M'=M` for node/account). So the image and `Σ.L` are unchanged ⟹ `RE` unchanged. Creating a *node* or *account* is not an "edit to a document" at all, so it is not covered. The cited lemma for "edits to other documents," LP5 (CrossDocumentIndependence), is about K.μ on `d' ≠ d` — not registration. The foundation has a dedicated lemma, **LP8 (DocumentRegistrationInvariance)**, for exactly this.
- **K.ρ** (ProvenanceRecording): frame gives `C'=C`, `L'=L`, `E'=E`, `M'=M`; only `Σ.R` changes. By RE-LOC, `RE` never reads `Σ.R` ⟹ `RE` unchanged. K.ρ is neither K.α nor a "document edit." The foundation has **LP14 (ProvenanceRecordingInvariance)** for exactly this.

A "full taxonomy" that omits two of the kinds in the vocabulary is not full.

**Required**: Add K.δ (citing LP8) and K.ρ (citing LP14) to the "leaves `RE` fixed" category, in both the prose taxonomy and the RE-EDIT claim — or drop the word "full."

### Issue 2: Retraction is a K.λ; RE-RET and the taxonomy do not account for the emitted retraction link entering addressable(Σ')

**ASN-0131, RE-RET / Stability prose**: "Retracting `ℓ` removes `ℓ` from `addressable(Σ)` permanently (R6a); ... a pair `(i, e)` that `ℓ` contributed leaves the answer **iff `ℓ` was its sole addressable bearer**."

**Problem**: A retraction is realized as `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` (ASN-0086), which is a **K.λ** transition: it emits a *new* link `b` with `Σ'.L(b) = (∅, {(a, δ(1,#a))}, R)`. A retraction step therefore does not merely *remove* `ℓ` from addressability — it simultaneously *adds* the emitter `b` to `dom(Σ'.L)`, and `b ∉ nullified(Σ')` ⟹ `b ∈ addressable(Σ')`. Two consequences:
- (a) The editing taxonomy's split — "creating a link (K.λ) may add" vs "a retraction may remove" — presents retraction and K.λ as distinct transition kinds, when retraction *is* a K.λ; the same transition both adds (the emitter) and removes (the target's addressability).
- (b) The precise condition for a pair `(i, e)` to leave `RE` across a retraction `Σ → Σ'` is: `ℓ` bears it, `ℓ` is its sole addressable Σ-bearer, **and** the emitter `b` (added in the same step) does not re-witness it in `Σ'`. RE-RET's "iff `ℓ` was its sole addressable bearer" drops the third conjunct. RE-RET does discuss re-introduction "via a freshly emitted ... link (R6c)" but only as a *separate future action* — overlooking that the retraction's own emitter `b` is added within the very transition whose stability is being characterized. For a content region `b` cannot re-witness (its endsets are `∅`, a link-address-targeting to-endset, and a type endset — none touch content), but the ASN never states this, and it is precisely what makes the "iff" hold; it fails for link-subspace `W` (Issue 3), where the emitter's to-endset can touch.

**Required**: State that `Nullify = Emit_R = K.λ`, so a retraction emits an addressable link `b` in the same step; reconcile the taxonomy; and either restrict to content regions with the explicit reason that `b`'s endsets target link/type addresses and so are never surfaced by a content-region query, or add the emitter conjunct to RE-RET's "iff."

### Issue 3: The domain of W is left unspecified; the unconditional claims hold only for content regions

**ASN-0131, "The region, and what it resolves to"**: "a region is a pair `(W, d)` with `d ∈ dom(Σ.M)` a document and `W ⊆ T` a set of V-positions (typically the V-positions of a span in `d`'s text)."

**Problem**: RE-DEF admits arbitrary `W ⊆ T`, but several claims are stated unconditionally while only holding for `W` that selects *content* (text-subspace) positions. When `W` contains link-subspace positions, `image(W, d, Σ)` contains *link* addresses (by S3★, ASN-0047: link-subspace positions map into `dom(Σ.L)`), and `RE` then surfaces link-targeting anchoring — retraction-emitter to-endsets and any endset whose spans cover link addresses become surfacable. This is well-defined, but it makes:
- "content-image" a misnomer,
- RE-CMP's "whether reached by native or transcluded content" narrower than the operation,
- RE-RET's exactness fail (Issue 2),

all without qualification. The narrative ("what anchoring touches this passage/content") is content-centric; the formal definition is not, and the gap is never resolved.

**Required**: Decide and state whether `W` is restricted to content-subspace V-positions (matching the narrative) or ranges over all V-positions. If the latter, the claims that lean on "content" (RE-RET's exactness, RE-CMP's content phrasing, the "content-image" terminology) must be re-stated or qualified so they hold for link-subspace regions.

### Issue 4: Worked example — the `coverage(e₃) ∩ dom(Σ.C) = ∅` step rests on an overgeneralized claim and a misapplied T7 citation

**ASN-0131, "A worked instance"**: "every address extending `θ` carries `θ`'s element-subspace identifier — not the content identifier `s_C` — so none is a content address (T7, ASN-0034)."

**Problem**: The intermediate claim "every address extending `θ` carries `θ`'s element-subspace identifier" is false as stated: an extension `t ≽ θ` with extra zero components (e.g. `θ.0.x`) has `zeros(t) > 3`, is T4-invalid, and has no well-defined `subspace_I(t) = E(t)₁` at all (T4b's `E`-projection is defined only on T4-valid `zeros=3` tumblers). The fact the example actually needs is narrower: a *content* address `c` (T4-valid, `zeros(c)=3`, `E(c)₁ = s_C`) cannot satisfy `θ ≼ c`, because `θ ≼ c` with both at `zeros=3` forces `E(c)₁ = E(θ)₁ = s_type ≠ s_C` by field-segment agreement on positions `1..#θ`. T7 (SubspaceDisjointness) asserts that two element-level addresses with differing `E₁` are distinct; it does not supply "extension preserves `E₁`," which is the load-bearing step here.

**Required**: Replace the overgeneralized sentence with the `zeros=3` field-structure argument restricted to content addresses (the only addresses intersected with `coverage(e₃)`), citing the positional-agreement / parse facts (T4b, TA5-SigValid-style) rather than T7, or state the T7 application precisely.

## OUT_OF_SCOPE

The ASN appropriately defers the genuinely new territory via its own open questions: whole-endset vs touching-spans surfacing (OQ1), multiplicity preservation (OQ2), the rendered V-position mode and footprint fragmentation (OQ3, ASN-0082 layer), intersection-distributivity (OQ4), non-co-resident link stores (OQ5, replication), and type-slot-against-content semantics (OQ6). These are correctly future work, not defects in this note.

VERDICT: REVISE
