# Review of ASN-0131

## REVISE

### Issue 1: RE-RET's "unconditional" core result is falsified by retraction of a Θ-typed retraction link

**ASN-0131, *Under retraction* / RE-RET row**: "The core stability result below does not rest on it: the emitter's only possible content-region contribution is the single pair `(3, Θ)`, carrying the retraction type — *a value distinct from any anchoring endset a retracted link bears* — so `b` can re-witness no pair `(i, e)` that `ℓ` itself bore." And the table: "the emitter `b` cannot rescue a dropped pair, its sole possible contribution being the fresh pair `(3, Θ)`, distinct from any anchoring endset a retracted link bears."

**Problem**: The forward half of the iff ("sole bearer ⟹ the pair drops") rests on the premise that `(3, Θ)` is **distinct from every pair `ℓ` bore**. That premise fails exactly when the retracted link `ℓ` itself carries `Θ` in a region-touching slot — and the note's own development makes this reachable:

- The note establishes (correctly) that `coverage(Θ) ∩ dom(Σ.C) = ∅` is **not** furnished by ASN-0086 ("a property the retraction layer must furnish... not secured by start-placement alone"). So the regime `coverage(Θ) ∩ I ≠ ∅` — `Θ` touching the content region — is a live case the note explicitly admits ("absent it, a `Θ` meeting the image would surface the emitter as the fresh pair `(3, Θ)`").
- A retraction link is itself retractable (ASN-0086 R6b/R6c, retraction-of-retraction). Every retraction link bears slot-3 `= Θ` (the fixed `Emit_R` type). So `ℓ` can be a Θ-typed retraction link.

Minimal counterexample, using the note's own assertion that the emitter is addressable (`b ∉ nullified(Σ')`):
Let `ℓ` be the only Θ-typed link in `Σ`, addressable, with `coverage(Θ) ∩ I ≠ ∅`. Then `ℓ` is the **sole addressable bearer** of `(3, Θ)`, and `(3, Θ) ∈ RE(W, d, Σ)`. Retract `ℓ`: the step emits a fresh, addressable retraction link `b` with slot-3 `= Θ`; the `K.λ` step frames `Σ.M(d)` (`M' = M`), so the image and `touch_W(Θ)` are unchanged, hence `(3, Θ) ∈ RE(W, d, Σ')` via `b`. The pair did **not** drop although `ℓ` was its sole addressable bearer. The "unconditional" forward direction is false for `(i, e) = (3, Θ)`.

The result is salvageable — and the note already has the right hypothesis in hand. Under `coverage(Θ) ∩ dom(Σ.C) = ∅` (so `coverage(Θ) ∩ I = ∅`, since `I ⊆ dom(Σ.C)`), `Θ` never touches a content region, so `(3, Θ)` is never a pair any link bears in `RE`, and the sole-bearer characterization is clean. So the core result **does** rest on that hypothesis, contrary to the claim that it "does not rest on it."

Note this is not excused by Open Question 6 (type-slot meaningfulness): OQ6 may defer *what such a match means*, but RE-DEF formally surfaces every slot `1 ≤ i ≤ |Σ.L(a)|`, so `(3, Θ)` is a genuine member of `RE`, and RE-RET makes a false formal claim about it.

**Required**: Either (a) condition the core sole-bearer result on `coverage(Θ) ∩ I = ∅` (equivalently the content-region net-removal hypothesis), retracting "does not rest on it"; or (b) explicitly carve the pair `(3, Θ)` out of the forward direction when `Θ` touches the region, stating that the fresh emitter re-witnesses it. Secondarily: `b ∉ nullified(Σ')` is asserted without justification — it is true only under ASN-0086's unit-depth/`R0a` discipline (the vacuity of `wp` Case 2's third conjunct, ASN-0086); cite that, since the counterexample above turns on `b` being addressable.

### Issue 2: Use-site inventory in "Why confine W to the content subspace?"

**ASN-0131, *Why confine W*** : "Confining `W` to `s_C` ... keeps the whole development — the worked instance, the exactness of retraction stability (below), the completeness phrasing — on content."

**Problem**: The clause "— the worked instance, the exactness of retraction stability (below), the completeness phrasing —" is a downstream-consumer inventory of the kind the anti-bloat pass exists to catch: it enumerates where the restriction is later used rather than advancing the reason for the restriction. The substantive content — the arrangement maps `s_L` positions to link addresses (S3★), so an `s_C` restriction keeps "content-image" accurate — stands without it. The paragraph also restates the OQ7 deferral already carried by Open Question 7.

**Required**: Delete the use-site inventory clause; keep the S3★ motivation and the one-line OQ7 pointer.

### Issue 3: Redundant "full taxonomy" recap paragraph in Stability

**ASN-0131, *Stability*** : "The full taxonomy of what moves the answer is then: a *content-subspace* arrangement edit to `d` ... changes `RE` *through the image*; ... Finally `K.α`, `K.δ`, `K.ρ`, together with edits to documents other than `d`, leave `RE` fixed."

**Problem**: This paragraph re-states, in summary form, the per-motion prose immediately preceding it (insertion/deletion/rearrangement; the `K.α`/`K.δ`/`K.ρ`/other-document paragraph; the `K.μ⁺_L` paragraph) — and the same taxonomy is then stated a third time in the RE-EDIT claim row. Three statements of one classification is exactly the forward-reference accretion the `review-mode.anti-bloat` classifier targets. The derivation (per-motion prose) and the canonical summary (claim row) already cover it; the middle recap layer adds nothing.

Relatedly, RE-WHOLE's provisional-pending-OQ1 status is asserted three times (faithfulness prose, worked-example read-off, claim row) — a single same-location deferral repeated across sections.

**Required**: Remove the "full taxonomy" recap paragraph (the per-motion prose plus the RE-EDIT row carry it). Collapse the OQ1-provisional restatements to the claim row plus one prose mention.

## OUT_OF_SCOPE

### Topic 1: Type-slot matches against content regions (OQ6) and link-subspace regions (OQ7)
**Why out of scope**: The note correctly defers, via its own Open Questions, the *meaningfulness* of a type-slot match against content (OQ6) and the entire link-subspace region query (OQ7, where the image lands in `dom(Σ.L)` and the retraction-emitter's to-set re-enters the analysis). These are genuinely separate queries, not defects here. Caution only: the OQ6 deferral does not cover the Issue-1 overclaim — RE-RET makes a concrete false formal claim about the `(3, Θ)` pair, which must be fixed in this ASN regardless of OQ6's resolution.

VERDICT: REVISE
