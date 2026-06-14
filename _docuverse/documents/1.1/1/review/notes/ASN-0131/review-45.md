# Review of ASN-0131

I checked the operation definition, the decidability argument, both union/intersection composition claims, RE-SEL's factoring through `findlinks_V`, RE-CWP, RE-RET, the two cross-model lifts (ASN-0082 shifts, ASN-0086 retraction lemmas), and the worked instance. The technical content is sound: the biconditional soundness/completeness are correct reads of RE-DEF; the `Avail`/`touch_W` factoring that drives RE-UDIST is valid; RE-CWP's weakest precondition correctly captures "no pair dropped" and its `R = ∅` boundary; RE-RET's forward/backward halves hold under the stated `coverage(Θ) ∩ dom(Σ.C) = ∅` hypothesis (which is correctly flagged as a construction hypothesis, not a theorem, and deferred to OQ6); and the worked instance computes correctly and exercises each distinctive postcondition. I found no correctness, missing-case, or depth defect in the proofs.

The two issues below are a missing derived consequence and a prose-accretion duplication the anti-bloat pass targets.

## REVISE

### Issue 1: Intersection-composability left wholly open when the `⊆` half is immediately derivable

**ASN-0131, "Composing regions: union-distributivity" (intersection paragraph) and RE-UDIST**: "The forward image does not distribute over intersection: in general `image(W₁ ∩ W₂, d, Σ) ⊆ image(W₁, d, Σ) ∩ image(W₂, d, Σ)`, but the inclusion can be strict … Intersection-composability is therefore a genuinely separate question, and we leave it open." (RE-UDIST table: "Intersection-distributivity does *not* follow (Open Question 4).")

**Problem**: The note proves union-distributivity by factoring through `Avail(Σ)` and `touch_W`, and it states the image `⊆` law for intersection — but then declares the *entire* intersection question open. One direction is a one-step consequence of facts already in this ASN: from `image(W₁∩W₂) ⊆ image(W₁) ∩ image(W₂)`, for any `(i,e) ∈ Avail` we get `touch_{W₁∩W₂}(e) ⟹ touch_{W₁}(e) ∧ touch_{W₂}(e)`, hence `RE(W₁∩W₂, d, Σ) ⊆ RE(W₁, d, Σ) ∩ RE(W₂, d, Σ)` unconditionally (no injectivity needed). Only equality/the `⊇` direction is genuinely blocked by non-injective `Σ.M` (M13/M14, ASN-0058). Leaving the derivable half unstated is exactly the "consequences not explored" gap — the note establishes the prerequisite and stops short of deriving it.

**Required**: State `RE(W₁∩W₂, d, Σ) ⊆ RE(W₁, d, Σ) ∩ RE(W₂, d, Σ)` (one line from the image `⊆` law) and narrow OQ4 to the `⊇`/equality direction that non-injectivity genuinely defeats.

### Issue 2: The OQ1 / whole-endset provisionality is stated three times

**ASN-0131, "Extent…" section, RE-DEF entry, and RE-WHOLE entry**:
- Extent prose: "Whether entirety is demanded, or only the touching spans, is reopened as Open Question 1; we therefore hold RE-WHOLE **provisional** pending its resolution…"
- RE-WHOLE entry: "not forced by RE-CLIP, held **provisional** pending Open Question 1".
- RE-DEF entry: "the returned `e = Σ.L(a).eᵢ` is the *whole* slot endset only by the adopted RE-WHOLE convention, so this returned-endset extent is as provisional as RE-WHOLE (Open Question 1)".

**Problem**: The same provisional status (whole-endset surfacing is a convention, not forced by RE-CLIP, provisional pending OQ1) is asserted in the body prose and again in two claims-table entries, with the RE-DEF entry duplicating RE-WHOLE's content. This matches the flagged patterns "two paragraphs say the same thing in different words" and "multiple paragraphs defer to the same downstream location" (all three defer to OQ1). The RE-DEF entry is the central definition; to read what `RE` *is*, one must skip past a re-litigation of which sub-parts are provisional — meta-prose in a structural slot. The RE-DEF entry carries this caveat because the provisionality is being restated, not because the definition needs it.

**Required**: State the provisional status once (the Extent section establishes it; RE-WHOLE records it). RE-DEF's entry should state the definition and, at most, point to RE-WHOLE for the returned-endset extent — not re-explain the convention and OQ1.

## OUT_OF_SCOPE

### Topic 1: The deferred questions (OQ3 rendered-answer, OQ4 intersection equality, OQ6 type-vs-content, OQ7 link-subspace regions)
**Why out of scope**: These are genuinely new territory (a rendered/V-order answer mode, intersection equality under non-injectivity, type endsets that reach content, link-subspace regions resolving into `dom(Σ.L)`), correctly handled as open questions rather than as defects in this note. The RE-RET hypothesis `coverage(Θ) ∩ dom(Σ.C) = ∅` is appropriately carried as an explicit construction hypothesis with its exception routed to OQ6 — a conditional result, not an unproven claim.

VERDICT: REVISE
