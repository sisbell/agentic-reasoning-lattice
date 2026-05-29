# Review of ASN-0053

## REVISE

### Issue 1: Foundation recap duplicates content used (and discharged) at site

**ASN-0053, opening + "The reach function"**:
- Opening: "ASN-0034 gave us the tumbler space T with its total order (T1) and its arithmetic… It defined a span σ = (s, ℓ) as a well-formed pair satisfying T12: ℓ is positive, the action point of ℓ falls within #s, and σ denotes the half-open interval ⟦σ⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ}."
- Reverse-displacement paragraph: "ASN-0034 answers this directly: the displacement from a to b is w = b ⊖ a (TumblerSub, ASN-0034), well-defined and round-tripping (a ⊕ w = b) exactly when a < b, divergence(a, b) ≤ #a, and #a ≤ #b (D1, ASN-0034), with uniqueness by D2 (ASN-0034)."

**Problem**: This is foundation restatement. T12, the span definition, and the denotation are ASN-0034 material; the reverse-displacement paragraph restates D1's three preconditions verbatim and previews D2 — yet WF and WR re-state and *discharge* exactly those preconditions at their use sites ("Since s < r and #s = #r, the divergence k is of type (i)… By D1…"). The preview advances no reasoning that the at-site discharges don't already carry. Under the note's `review-mode.anti-bloat` classifier this is the targeted pattern: foundation prose that a precise reader skips to reach the actual lemma. These compound if not trimmed at source.

**Required**: Keep only what establishes *this ASN's* new notation — start/width/reach, the ⟦σ⟧ bracket, and "every span is non-empty (TA-strict)." Drop the T12/denotation recap (foundation, available unrestated per the self-containment rule's foundation exception) and collapse the reverse-displacement paragraph to the one sentence this ASN actually adds: that the displacement recovering b from a is b ⊖ a. Let WF/WR carry the precondition detail where they discharge it.

## OUT_OF_SCOPE

### Topic 1: Span-set difference bound and cross-level intersection
**Why out of scope**: The Open Questions correctly defer `|normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)|` and intersection of spans at differing hierarchical levels. These are genuinely new territory (level_compat is a standing hypothesis throughout S1/S3/S8/S11), not gaps in the present claims. No action.

Verification spot-checks passed: WF→D1, WR→D2, S5's TA-assoc/TA-LC precondition discharges, S8 N1/N2 strictness, S9's five-way divergence cases (including the unequal-length 1b/3b branches), and S11's convexity-based tightness are all complete and the worked arithmetic is correct.

VERDICT: REVISE
