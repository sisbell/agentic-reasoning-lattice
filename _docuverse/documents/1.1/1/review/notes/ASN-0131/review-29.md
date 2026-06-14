# Review of ASN-0131

I checked every introduced claim against its derivation and the foundations. The core mathematics is sound: RE-UDIST, RE-CWP, RE-SEL, RE-TRANS, RE-IDENT, the worked example, and the transition-by-transition stability survey are all correct, and the soundness/completeness directions are honestly labeled as immediate reads of the defining biconditional. The note is, however, flagged `review-mode.anti-bloat`, and on that axis (plus one genuine overclaim) it needs work.

## REVISE

### Issue 1: One bolded claim is false as stated; RE-RET's "sole exception" understates its assumptions

**ASN-0131, "Stability" → "Under link emission"**: "**any fresh `K.λ` output is addressable in its post-state.**"
**ASN-0131, RE-RET (Claims Introduced)**: "a pair `(i, e)` that `ℓ` bore drops **iff `ℓ` was its sole addressable bearer in `Σ`**, under the net-removal-only hypothesis `coverage(Θ) ∩ dom(Σ.C) = ∅` (its sole exception … routed to Open Question 6)."

**Problem**: The note works in the ASN-0047 transition model, whose `K.λ` admits *arbitrary* link values (`N ≥ 3 ∧ eᵢ ∈ Endset ∧ e₃ ≠ ∅` — no shape constraint on the to-set). Nothing in that vocabulary forbids a `K.λ` that emits an arity-3 link with type-coverage `= coverage(Θ)` and a **wide** slot-2 to-set. Such a "wide retraction" enters `L_R^Σ` with a wide cone, and `nullified(Σ)` would then cover a whole interval — including link addresses not yet allocated. So the bolded claim is false in this model: a pre-existing wide retraction-typed link can pre-nullify a fresh `ℓ_new`, putting `ℓ_new ∈ nullified(Σ')`. The note's own justification concedes this — it holds only "Under ASN-0086's unit-depth retraction discipline … (this is the vacuity of `wp` Case 2's third conjunct, ASN-0086)" — and ASN-0086 itself establishes that vacuity *only* "at a layer-reachable state" under the discipline. Presenting the conclusion as an unconditional bold sentence, then conditioning it in the next clause, is internally inconsistent. The same gap propagates to RE-RET: the discipline (which ASN-0047 does not enforce) is load-bearing for the fresh-output-addressability and single-tuple-scope arguments, so labeling the `coverage(Θ)` hypothesis as the *sole* exception is an overclaim — admitting a non-unit-depth retraction-typed link is a second way the result fails.

**Required**: Declare the unit-depth retraction discipline as a standing assumption of this ASN (e.g., admit retraction-typed links only via `Nullify`, so all retraction to-sets are unit-depth), or otherwise establish it holds at every reachable state of the ASN-0131 model. Then either qualify the bolded claim or remove the bold; and either revise RE-RET's "sole exception" wording or add the discipline to RE-RET's stated hypotheses alongside `coverage(Θ) ∩ dom(Σ.C) = ∅`.

### Issue 2: "Faithfulness of provenance" is identical to Soundness (RE-SND), stated in two sections

**ASN-0131, "Faithfulness…"**: "The first is **faithfulness of provenance**: every `(i, e) ∈ RE(W, d, Σ)` is a genuine slot-`i` endset of some addressable link, with `e` touching the region."
**ASN-0131, "Soundness and completeness…"**: "**Soundness** is the forward direction: if `(i, e) ∈ RE(W, d, Σ)`, then `e` is a genuine slot-`i` endset of an addressable link and `touch_W(e)` holds."

**Problem**: These are the same proposition — the forward direction of the defining biconditional, `(i,e) ∈ RE ⟹ (genuine slot-i endset of an addressable link) ∧ touch_W(e)`. Both are introduced with the identical justification ("immediate from the definition"); they differ only in their trailing gloss ("a reader who receives `(1,e)` may rely…" vs. "a reported overlap is a true overlap…"). Stating, justifying, and elaborating the same claim in two consecutive sections is precisely the accretion the anti-bloat classifier targets, and there is no second proof to warrant the repetition because soundness of a definition is trivial.

**Required**: Keep soundness in one place (the RE-SND-bearing section). Reduce the "Faithfulness" section to the genuinely distinct extent material (RE-CLIP, RE-WHOLE), which is not a restatement of soundness; fold any reader-reliance gloss in there or drop it.

### Issue 3: Minor duplications that should be collapsed

**ASN-0131, "Composing regions…" and "Stability"→contraction-WP**: the full definition `Avail(Σ) = { (i, e) : (∃ a ∈ addressable(Σ) : 1 ≤ i ≤ |Σ.L(a)| ∧ Σ.L(a).eᵢ = e) }` is spelled out verbatim in both places.

**ASN-0131, end of "When does an endset touch the region?" and start of "The unit of the answer…"**: decidability is argued twice — "The touch test is decidable…" and then "The answer just defined is a finite, computable object… With the touch test already decidable (above)…".

**Problem**: `Avail(Σ)` is a single region-independent object; defining it in full twice is redundant. The two decidability paragraphs largely re-establish the same realisability fact. Separately, OQ6 is deferred to from two locations (the retraction-type paragraph and the RE-RET row) and OQ1 from three (the Faithfulness section, the worked-example bullets, and the RE-WHOLE row) — the "multiple paragraphs deferring to the same downstream location" pattern.

**Required**: Define `Avail(Σ)` once (at RE-UDIST) and reference it by name at RE-CWP. Establish decidability once. Trim the duplicate forward-pointers to OQ1/OQ6 to a single deferral each. (The worked example is mandatory and should stay — it is an instantiation, not a restatement.)

## OUT_OF_SCOPE

The note correctly defers link-identity enumeration, counting, pagination, READLINK/FOLLOWLINK/MAKELINK/EDITLINK, rendering into V-order (OQ3), intersection-composability (OQ4), cross-store completeness (OQ5), type-slot-vs-content matching (OQ6), and link-subspace regions (OQ7) to future work without defining claims for them. No scope violations to flag.

VERDICT: REVISE
