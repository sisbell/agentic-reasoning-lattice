# Review of ASN-0131

This is a careful, largely rigorous note. The core definition is clean, the worked instance genuinely exercises every distinctive postcondition, and the stability case-analysis covers the whole transition vocabulary. I verified the union law, the intersection ⊆ half, RE-CWP, and both directions of RE-RET by hand and they hold. Three issues remain.

## REVISE

### Issue 1: The intersection ⊇ direction is *refuted* in the body but recorded as "open"

**ASN-0131, "Composing regions" + RE-UDIST + Open Question 4.**

The body constructs a concrete witness defeating `RE(W₁) ∩ RE(W₂) ⊆ RE(W₁ ∩ W₂)`:

> "an endset may meet `image(W₁, d, Σ)` and `image(W₂, d, Σ)` each through a shared I-address carried by positions outside `W₁ ∩ W₂` ... and yet meet `image(W₁ ∩ W₂, d, Σ)` not at all, so the pair is in `RE(W₁, d, Σ) ∩ RE(W₂, d, Σ)` without being in `RE(W₁ ∩ W₂, d, Σ)`."

This is a valid counterexample (realizable by the non-injective arrangement, M13/M14): pick `v₁ ∈ W₁∖W₂`, `v₂ ∈ W₂∖W₁` with `Σ.M(d)(v₁) = Σ.M(d)(v₂) = a`, an endset covering `a`, and no `W₁∩W₂` position mapping to `a`. It **refutes** the universal ⊇.

Yet the same sentence concludes "**and it is that direction we leave open**," RE-UDIST records only that ⊇ "does not follow," and Open Question 4 asks whether ⊇ "must … hold … given that the non-injective arrangement … **so defeats this direction**." A counterexample is a resolved negative result, not an open question — and OQ4 contains its own (negative) answer.

**Problem**: The strongest result the ASN actually establishes (⊇ *fails*) is recorded nowhere as a claim; RE-UDIST under-claims it as "does not follow," and OQ4 mis-files it as open while simultaneously noting it is defeated.

**Required**: Promote the negative result to a stated claim — RE-UDIST-intersection: "⊆ holds unconditionally; ⊇ fails in general (counterexample under non-injective `Σ.M(d)`)." If anything is to remain open, reframe OQ4 to the genuinely unresolved refinement (e.g., "under what arrangement restriction — injectivity? — is equality recovered?"), not the bare ⊇ the body has already refuted.

### Issue 2: The insert/delete `L`/`E`/`R` frame is asserted from a model that has no such stores

**ASN-0131, RE-EDIT, the cross-model lift paragraph.**

> "the remaining components `Σ.L, Σ.E, Σ.R` of the full `(C, L, E, M, R)` state simply lie outside the edit's write-set, so the edit frames them — M-only ⟹ frames `L, E, R` — exactly as every ASN-0047 atomic mover above does, at any content depth."

ASN-0082 models insert/delete over a `(C, M)` state with no `L`, `E`, or `R`, so it establishes only that they write `M` and frame `C` (I3, D-SHIFT, I3-C, D-I). Whether the *lifted* operation writes `L`/`E`/`R` is not determined by ASN-0082 at all — it is determined by how the lift is performed. The phrasing "lie outside the edit's write-set, so the edit frames them" presents as a *derivation* ("so") what is in fact a *stipulation* about the lift (there is no write-set defined over the full state in the cited foundation to "lie outside" of).

**Problem**: The insert/delete stability conclusion (`addressable(Σ)` and `Avail(Σ)` unmoved, only the image moves) rests on a frame that cannot be derived from the foundation it cites; it is this ASN's modeling commitment presented as inherited.

**Required**: State the `L'=L ∧ E'=E ∧ R'=R` frame for the lifted insert/delete as an explicit assumption of *this* ASN (the natural lift of ASN-0082's `(C,M)` primitive to the full state), rather than attributing it to ASN-0082's write-set. The downstream argument is unchanged; only the status of the frame needs honest labeling.

### Issue 3: Transclusion section re-argues a foundation design choice without advancing RE's reasoning

**ASN-0131, "Anchoring reached through borrowed content," the "Transclusion makes concrete a fact the definitions already fix" paragraph.**

RE-TRANS (preceding paragraph) already establishes that surfacing is by content identity — directly from the touch test being document-blind. RE-IDENT (following paragraph) establishes coverage permanence from L12/LP3. The middle paragraph between them restates that endset spans are over content identity (an ASN-0043 fact), argues counterfactually why naming V-positions *would* break ("Were the span to name the borrowing position … the anchoring would fracture …"), and closes with motivation ("This is the property that lets one make a link against borrowed content and have it hold, automatically …").

**Problem**: None of this advances RE's argument; it re-justifies a foundation design decision the note depends on but does not establish. A reader following RE-TRANS → RE-IDENT skips it — the pattern this review mode flags as accreted essay-prose.

**Required**: Compress to at most a one-line pointer ("endset spans name content identity, not borrowing position — ASN-0043"), or remove. The load-bearing content is already carried by RE-TRANS and RE-IDENT.

## OUT_OF_SCOPE

The note's other deferrals are correctly future-ASN territory and properly filed as Open Questions: whole-vs-touching-span return (OQ1), multiplicity preservation (OQ2), V-rendered answers (OQ3), non-co-resident link stores (OQ5), type-slot-against-content semantics (OQ6), and link-subspace regions (OQ7). No revision is needed for these — only OQ4 carries the status defect noted under Issue 1.

VERDICT: REVISE
