# Review of ASN-0131

I worked through the definition, the worked instance, and each derived claim (RE-UDIST, RE-SEL, RE-CWP, RE-RET) line by line. The mathematics is in good shape: the `e₃`/`R` field-segment-agreement arguments for content-disjointness are correct and carefully scoped (the note rightly distinguishes the coverage-level claim from `θ ∉ dom(Σ.C)` and rightly flags that the "every extension carries the identifier" reading fails on T4-invalid extensions); the worked instance verifies RE-OVL/CLIP/WHOLE/UNIT against concrete tumblers; RE-CWP is a genuine non-trivial weakest-precondition and is strictly finer than D-CWP as claimed; the retraction discipline is honestly marked an imposed convention rather than a derivation. One internal inconsistency remains.

## REVISE

### Issue 1: The "full taxonomy" claims retraction is the sole pair-remover, contradicting the ASN's own deletion result

**ASN-0131, "Stability: the answer as the document is edited" (the "full taxonomy" paragraph)**: "a link emission (`K.λ`) whose coverage meets the present image may *add* a pair *through `Σ.L`* (a new live link enters `sel`) — and a retraction, being itself a `K.λ` ..., **is the one transition that may *remove* pairs**: it marks its target nullified, dropping it from the addressable population ..."

**Problem**: Read at face value this is false, and it is contradicted twice within the same ASN.

- Four sentences earlier, the deletion bullet states: "*Deletion* of region content ... endsets that touched only through the departed content **cease to be surfaced**." That is a removal of pairs.
- RE-CWP later proves "`RE` is monotone-decreasing under contraction (`RE(W, d, Σ') ⊆ RE(W, d, Σ)`)", with strict drops realizable — a content-subspace `K.μ⁻` removes pairs through the *image* channel.

So content-subspace contraction `K.μ⁻` demonstrably removes pairs from `RE`; retraction is not "the one transition that may remove pairs." The intended (and correct) statement is narrower: retraction is the only transition that removes pairs by *shrinking the addressable population* — i.e. through the `Σ.L` channel. (This narrower claim is sound: `dom(Σ.L)` only grows by L12a and `nullified` only grows by R6a, so `addressable = dom(Σ.L) ∖ nullified` can lose a member only when a retraction enlarges `nullified`.) The asymmetry in the prose — the *add*-clause carries the qualifier "through `Σ.L`" but the parallel *remove*-clause drops it — is what produces the over-broad reading.

A related imprecision sits in the same taxonomy: it lists "deletion `K.μ⁻`" uniformly among edits that "change `RE` through the image," but ASN-0047's per-subspace `K.μ⁻` permits link-subspace-only contraction (`n'_{s_C} = n_{s_C}`, `n'_{s_L} < n_{s_L}`), which leaves the content image — and hence a content-region answer — fixed, exactly as `K.μ⁺_L` does (and exactly as RE-CWP yields when `Δ = ∅`). The taxonomy carves out `K.μ⁺_L` as the arrangement edit that leaves a content answer fixed but does not carve out this `K.μ⁻` case.

**Required**: Scope the remove-clause to "the one transition that may remove pairs *via the addressable population* (the `Σ.L` channel)," and add a clause noting that a link-subspace-only `K.μ⁻` (like `K.μ⁺_L`) leaves a content-region answer fixed, so that the billed "full taxonomy ... every member now classified" is consistent with the deletion bullet and RE-CWP.

## OUT_OF_SCOPE

### Topic 1: Intersection-distributivity of region queries (the note's OQ4)
**Why out of scope**: The note correctly derives the *union* law (RE-UDIST) and shows the intersection law fails because the forward image does not distribute over intersection under a non-injective arrangement (M13/M14, ASN-0058); the counterexample structure (two distinct V-positions sharing an I-address) is right. Settling what intersection-composability *can* guarantee is genuinely new territory, correctly deferred.

### Topic 2: Link-subspace regions and cross-store completeness (OQ5, OQ7)
**Why out of scope**: The content-subspace restriction `W ⊆ s_C` is a stated caller obligation; resolving the guarantees a link-subspace region must carry (where the emitter's to-set re-enters the analysis, as the note flags) and the completeness guarantee under a non-co-resident link store (replication/BEBE) are future operations, not defects here.

### Topic 3: Whole-endset vs touching-spans surfacing (OQ1)
**Why out of scope**: The ASN legitimately commits to whole-endset surfacing in RE-DEF and marks RE-WHOLE provisional with the alternative flagged; RE-CLIP is correctly shown universal across both readings. Committing to one reading and deferring the debate is acceptable — this is not an unresolved gap in the present ASN.

VERDICT: REVISE
