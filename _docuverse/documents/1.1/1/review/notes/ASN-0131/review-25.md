# Review of ASN-0131

I checked the operation definition, every proof, the worked instance, the union-distributivity argument, the contraction weakest-precondition, and the full stability analysis (every ASN-0047 transition kind, plus emission and retraction). **The technical content is sound — I found no correctness or completeness gap.** The retraction analysis in particular is airtight: the backward direction (R-Scope confining the nullification to the named target, L12 fixing the surviving bearer's value) is unconditional, and the forward direction is honestly fenced behind the `coverage(Θ) ∩ dom(Σ.C) = ∅` hypothesis with its exception routed to an Open Question. The worked instance exercises every distinctive postcondition and computes correctly (the `e₃` subspace-disjointness argument via field-separator agreement holds; the width-2 span straddling check is right).

The findings below are anti-bloat / precision, in line with this note's `review-mode.anti-bloat` classifier — accreted argumentation in structural slots and re-derivation of foundation machinery.

## REVISE

### Issue 1: Claims-table rows carry argument, caveats, and proof-structure — not claims
**ASN-0131, Claims Introduced table (RE-EDIT, RE-RET; also RE-UDIST, RE-CWP)**: The RE-RET row reads "...forward (sole bearer ⟹ drops) under the net-removal-only hypothesis ... routed to Open Question 6. Link-level permanence (R6a) is not pair-value-level permanence — an identical pair re-enters only via a separately identified live link (R6c, ASN-0086)." The RE-EDIT row reads "...so their non-monotone image swing is grounded in the displacement directly (content at shifted positions both enters and leaves a fixed region's image), not in F-IMG-SWING. A region-local contraction is *not* the global orphaning/resurrection of LP17/LP18 (ASN-0098)."

**Problem**: These rows embed *why*-grounding ("grounded in the displacement directly because..."), distinctions ("link-level permanence is not pair-value-level permanence"), and proof structure ("backward unconditional; forward conditional") that duplicate the Stability section verbatim-in-substance. A claim table states the claim; the argument is body material and is already in the body. Compare the terse rows of the foundation ASNs (e.g., ASN-0058 M0–M16, ASN-0082's cited table). Two specific accretions:
- The RE-EDIT row asserts "link-subspace-only K.μ⁻" as a flatly *fixed* transition, but the body's explicit fixed-transitions enumeration ({other-doc, K.α, K.δ, K.ρ, K.μ⁺_L}) never isolates this sub-case — it is only implicitly covered by the body's "fixed region within the retained prefix → unchanged" clause under the K.μ⁻ *mover* discussion. The table introduces a categorization the body does not walk.

**Required**: Reduce RE-EDIT and RE-RET (and trim RE-UDIST's intersection-failure derivation and RE-CWP's "strictly finer than D-CWP" comparison) to the claim itself; leave the grounding, the distinction, and the conditionality where the body already proves them. If "link-subspace-only K.μ⁻ leaves a content-region answer fixed" is to be a stated fixed-case, isolate it once in the body's fixed-transitions enumeration rather than only in the table.

### Issue 2: Decidability paragraph re-walks foundation span-membership and double-cites S8-fin
**ASN-0131, "When does an endset touch the region?"**: "We settle `touch_W(e) ≡ coverage(e) ∩ I ≠ ∅` by testing each of the finitely many members of `I` ... Membership `t ∈ coverage(e)` is decidable span-by-span: `coverage(e)` is a finite union of half-open T1-intervals (T12, ASN-0034), so `t ∈ [s, s ⊕ ℓ)` is the two intrinsic comparisons `s ≤ t < s ⊕ ℓ` (T2, IntrinsicComparison, ASN-0034)."

**Problem**: The T2 interval-membership recipe is foundation-standard (used identically in ASN-0086's CoverageEqualityDecidable and across ASN-0127); re-walking it here rebuilds rather than cites, which the Scope note flags for the image machinery. `I`'s finiteness is also cited to S8-fin twice in the same paragraph ("whose domain is finite (S8-fin, ASN-0036)" and again "With `I` finite (S8-fin, ASN-0036)..."). The *new* content — that RE as a whole is finite and computable — is worth one sentence; the per-step re-derivation is not.

**Required**: Condense to a citation-level statement: the touch test and the addressability filter are decidable over finite sets (`I` finite by S8-fin; `coverage`-membership by T2; `nullified(Σ)` computable per ASN-0086; `dom(Σ.L)` finite by L-fin), so RE is a finite computable object. Drop the redundant S8-fin cite and the span-by-span T2 walk.

## OUT_OF_SCOPE

The note makes no out-of-scope claims: RE-UNIT explicitly withholds link identity (so it does not trespass on FINDLINKSFROMTOTHREE, counting, or pagination), it reads by region not by address (not READLINK), and it neither creates nor traverses links. The deferrals to future territory — whole-endset vs touching-spans (OQ1), V-rendered answers (OQ3), intersection-composition (OQ4), non-co-resident link stores (OQ5), type-slot-against-content (OQ6), link-subspace regions (OQ7) — are correctly placed as Open Questions rather than smuggled in as claims. Nothing to flag here.

VERDICT: REVISE
