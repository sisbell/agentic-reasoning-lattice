# Review of ASN-0131

## REVISE

### Issue 1: RE-RET removes "every endset it contributed" — false for shared and re-emittable pairs

**ASN-0131, RE-RET / "Under retraction"**: "when a link is retracted, every endset it contributed leaves `RE` on the next inquiry — its anchoring disappears from the answer" and the claims-table form "withdrawing a link removes every endset it contributed from the next and all subsequent answers, permanently".

**Problem**: The answer is a *deduplicated set of `(i, e)` pairs* with link identity discarded (RE-UNIT). A pair `(i, e)` is present iff *some* addressable link bears `e` in slot `i` and `e` touches. So retracting one link does **not** remove a pair that another addressable link still bears. This directly contradicts the ASN's own worked example, where `ℓ₁` and `ℓ₂` both carry `e₁` in slot 1 and collapse to one pair `(1, e₁)`: retracting `ℓ₁` leaves `(1, e₁)` in the answer because `ℓ₂` is live. The "permanently" clause is also overstated at the pair-value level: by the trailing parenthetical's own admission, an identical value can re-enter via a freshly emitted link (R6c), so the *value* is not permanently gone — only the *specific link's* membership in `addressable` is (R6a). The claim conflates link-level permanence (R6a) with pair-value-level removal.

**Required**: Restate at the pair level: retraction permanently removes link `ℓ` from `addressable(Σ)` (R6a), so a pair `(i, e)` leaves the answer **iff `ℓ` was its sole addressable bearer**; a pair borne by another addressable link persists; and a value `(i, e)` may re-enter via a freshly emitted, distinctly-identified link (R6c). Reconcile explicitly with RE-UNIT's deduplication and the two-link worked example.

### Issue 2: Content allocation (K.α) listed as a way the answer grows without an arrangement edit

**ASN-0131, "Stability" / "Under editing of the queried document"**: "Allocating content or creating a link with coverage meeting the present image *adds* touching anchoring (a new link can enter `sel`), the one direction in which the answer grows without an arrangement edit; everything else that changes the answer changes it through the image."

**Problem**: K.α leaves both `Σ.M` and `Σ.L` unchanged (frame `L'=L; M'=M`, ASN-0093). RE reads only `(Σ.M, Σ.L)` (RE-LOC). Therefore K.α leaves `RE(W, d, Σ)` *invariant* — a freshly allocated `a_new` is not in `image(W, d, Σ)` (no V-position maps to it without a separate K.μ⁺), so no endset newly touches, and `Σ.L` is untouched so no pair enters `Avail`. Only **link creation (K.λ)** grows the answer without an arrangement edit. The trailing "everything else changes through the image" is also wrong: K.λ growth is `Σ.L`-mediated and retraction is population-mediated — neither goes through the image.

**Required**: Drop "allocating content" from the answer-growing operations (it is consistent with LP6 ContentAllocationInvariance that K.α changes no projection). State the accurate taxonomy: arrangement edits to `d` change RE through the image; K.λ may add a pair (via `Σ.L`); retraction may remove pairs (via the addressable population); K.α and edits to other documents leave RE fixed.

### Issue 3: RE-EDIT cites whole-document projection lemmas (ASN-0098) for region-image behavior

**ASN-0131, RE-EDIT and "Under editing of the queried document"**: "the image grows (the projection extends, LP9, ASN-0098)"; claims table: "insertion surfaces newly-reachable anchoring (LP9), deletion orphans anchoring whose content departs the region (LP10, LP17) ... rearrangement swings the *membership* of surfaced `(i,e)` pairs via the image swing (LP11)".

**Problem**: LP9/LP10/LP11 (ASN-0098) govern `project(e, d, Σ)` — the V-positions across the **whole document** that reach an endset — i.e. discoverability-from-`d`. RE's touch test is region-restricted: `coverage(e) ∩ image(W, d, Σ)`. The lemmas that govern the region image under editing are F-IMG-MONO, F-IMG-CONTR, and F-IMG-SWING (ASN-0127). An endset can stay discoverable from `d` (LP9 territory) yet stop touching `W`, so the cited projection lemmas do not establish the region-restricted surfacing claims they are attached to. This is also internally inconsistent: RE-CWP correctly cites **F-IMG-CONTR** for exactly the contraction image-shrink that RE-EDIT attributes to LP10.

**Required**: Cite F-IMG-MONO / F-IMG-CONTR / F-IMG-SWING (ASN-0127) for the region-image growth / shrink / swing (matching RE-CWP's own use of F-IMG-CONTR), with the touch test composing on top. Keep LP17/LP18 for the orphan/resurrection observations, where they are apt.

### Issue 4: Decidability mischaracterizes `I` as a finite union of half-open intervals

**ASN-0131, "When does an endset touch the region?"**: "`coverage(e)` and `I` are finite unions of half-open T1-intervals (T12, ASN-0034), and intersection-nonemptiness is settled by the cell-decomposition of ASN-0086 (CoverageEqualityDecidable) run for overlap rather than equality."

**Problem**: `I = image(W, d, Σ)` is a finite **set of points** (and the ASN says so two paragraphs later: "The image `I` is finite (S8-fin, ASN-0036)"). It is *not* a finite union of half-open T1-intervals: every span-interval `[s, s⊕ℓ)` with `Pos(ℓ)` contains the entire subtree of `s` and is infinite, so a singleton `{a₂}` is not such an interval. The "finite union of intervals" reading is therefore both wrong and in tension with `I` finite. Running CoverageEqualityDecidable's cell decomposition "for overlap" presumes both operands are interval unions, which `I` is not.

**Required**: Justify decidability directly: `I` is finite (S8-fin), so test each of its finitely many members for membership in `coverage(e)` by T2 (IntrinsicComparison). The cell-decomposition machinery (ASN-0086) applies to `coverage(e)` alone; it need not — and cannot — be run against `I` as if `I` were an interval union.

### Issue 5: The symbol `R` carries three meanings

**ASN-0131, throughout**: `touch_R(e)` (subscript = the fixed *region*), `K.μ⁻[d, R]` / `I_R` / `W ∩ R` in RE-CWP (`R` = the *retention set*), and `Σ.R` (the provenance relation, ASN-0047). The same section also switches between `touch_R` and `touch_W` for one predicate.

**Problem**: Three unrelated referents for `R` plus a dual subscript convention for one predicate is a clarity hazard, even though each local context is individually parseable.

**Required**: Disambiguate — e.g., name the region predicate `touch_W` uniformly (it already does so in RE-UDIST "to make the region explicit"), and either rename the retention set or annotate the collision where both `touch`/region-`R` and retention-`R` appear near each other.

## OUT_OF_SCOPE

(none — the operation is defined abstractly over system state, cites the image/anchoring machinery rather than rebuilding it, and withholds link identity, so it does not stray into ASN-0121/0108/0111/0114/0120/0125 territory.)

VERDICT: REVISE
