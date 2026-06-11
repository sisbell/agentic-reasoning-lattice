# Channel Assignment — ASN-0121 review-35

**Date:** 2026-06-11 16:07

## Issue 1: FL-JUNK's claims-table row drops the load-bearing no-retraction hypothesis
Reason: Internal — the body's FL-JUNK already carries both hypotheses (`nullified(Σ') = nullified(Σ)` and added links fail the request), and the counterexample is built from the ASN's own case-(c) membership equation; the fix is syncing the table row with the body statement, with the corrected wording already supplied.

## Issue 2: FL-DEC is stated and proven two sections before its ingredients exist
Reason: Internal — this is a placement problem, not a content problem; every ingredient (touch/athome decidability, `sat`, FL-DEF, the addressability filter, L-fin) already exists in the ASN, and the fix is splitting or relocating FL-DEC so each part sits after its definitions.

## Issue 3: "`L_R^Σ ⊆ Σ.L`" is type-incorrect (three occurrences)
Reason: Internal — the correct formulation already appears in the ASN itself: FL-WP case (a) quotes ASN-0086's triple definition of `L_R^Σ`, and the FL-DEC proof already says it is "selected from the finite `dom(Σ.L)` by the slot-3 type-coverage test"; the fix is replacing the bad inclusion with that existing phrasing at all three sites.

## Issue 4: Precedent-defense meta-prose accreted around FL-WP
Reason: Internal — pure editorial deletion with an explicit cut/keep list; the load-bearing content to retain (the no-discipline scoping sentence and the first-class-searchability grounding via 4/41, 4/44–4/45 and consultation Q2) is already present in the text, so no design-intent or implementation fact needs re-establishing.

## Issue 5: FL-CUR is a fourth label on the same set equality
Reason: Internal — the ASN's own sentence concedes FL-CUR is FL-DEF restated, so the fold-and-remove remedy is a structural deduplication; the only candidate for genuinely distinct currency content (version/time-scoped inquiry) is already explicitly deferred to the ASN's open questions, so no channel input is needed to choose the fold over the rework.
