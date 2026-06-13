# Review of ASN-0108

This note is technically strong. I checked the substantive arguments — the wp analysis in W2 (identity vs. offset cursor, including the nested frozen-prefix / membership-identity / weakest-precondition hierarchy and the empty-window corner), the partition induction in W4, the three sufficiency/necessity walks in W5, the F-LAMBDA bridge in W6a, the per-link charge-injectivity argument in W9b, and the W9a count formula against all four boundary walks (m=0, N>m, exact multiple, non-divisible) — and they hold up. Concrete walks accompany every major claim, the wp analysis is non-trivial, and foundation usage (D-NONMONO, F-V/F-FULL/F-LAMBDA/F-IMG, LP11/LP12/LP13/LP17/LP18, T8/T9/S0) is consistent. All cross-references are to foundation ASNs.

The findings below are anti-bloat: residual forward-reference accretion the classifier asks me to surface at source.

## REVISE

### Issue 1: Match-definition forward pointer with a use-site locator
**ASN-0108, "State, the Matching Set, and What Windowing Operates On"**: "We import two qualitative facts about Match as our standing handles; one further structural fact — the K.λ-increment shape of Match, by which link creation grows the matching set by a single disjoint element — **enters once, in W6a's set-level bridge, and is introduced there**:"
**Problem**: This is the flagged "definition's introduction enumerates downstream consumers / forward pointer to where content lives" pattern. The K.λ-increment fact is *properly* introduced and proved at its use site, W6a's set-level bridge. The Match-definition sentence pre-announces the fact's gist and then carries a purely locational tail ("enters once, in W6a's set-level bridge, and is introduced there"). The reader gains nothing usable here — the fact is neither stated as a standing handle (like M-fin, M-mut, which are given inline immediately after) nor used until W6a. The locator phrase is removable accretion; this is the shape the recent "introduce K.λ-increment fact" commit left behind.
**Required**: Either promote it to a third inline handle stated plainly alongside M-fin/M-mut (no "introduced there" pointer), or drop the announcement entirely and let W6a introduce it. Remove the locational tail regardless.

### Issue 2: Re-glossed "(W8's per-key breakdown)" parenthetical (minor)
**ASN-0108, W9 and W9b**: W9 — "under cursor-key computability alone (which either permanent key supplies, the content-position key not — W8's per-key breakdown)"; W9b(i′) — "so clause 1 is well-defined and applicable at every visited cursor — which either permanent key supplies and the position key does not (W8's per-key breakdown)".
**Problem**: The same content — "either permanent key supplies computability, the position key does not" — originates in W8, is glossed parenthetically in W9, and is glossed again in W9b. The cross-reference "(W8's per-key breakdown)" is appropriate in both places; the *re-statement of the content* on the second occurrence (W9b) duplicates W9's just above. This is the "two paragraphs say the same thing in different words" pattern, in miniature.
**Required**: On the W9b occurrence, keep the pointer "(per W8's per-key breakdown)" and drop the re-gloss, unless self-containment of W9b is judged to require it — in which case it is acceptable as written and may be declined.

## OUT_OF_SCOPE

The note's scope is handled cleanly: the matched-content multi-document key (W6a caveat), the eventual-delivery guarantee for non-allocation-monotone keys, the cross-state completeness invariant, the uncomputable-cursor protocol (the W8/W9 unresolved case), and the progress-sizing correspondence (W10's companion query) are each correctly deferred to the Open Questions rather than half-treated. The declared exclusions (count-only, full-set, MAKELINK, FOLLOWLINK, BEBE) are respected — no claim strays into them. No additions needed.

VERDICT: REVISE
