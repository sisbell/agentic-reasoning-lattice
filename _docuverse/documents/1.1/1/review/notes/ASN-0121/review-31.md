# Review of ASN-0121

## REVISE

### Issue 1: Membership inferred from `sat` alone, dropping the addressability conjunct
**ASN-0121, "Directionality is positional, not symmetric" (FL-DIR witness)**: "`lift(e₁, X) = true` and `lift(e₂, Y) = true`, so `sat(a, q, Σ)` holds and `a ∈ findlinks((∗, X, Y, ∗), Σ)`"
**Problem**: The witness hypotheses fix only `a`'s endsets ("its type endset and home are immaterial here"); nothing places `a ∈ addressable(Σ)`. By FL-DEF, `sat` alone does not yield membership — this is precisely the point the ASN itself labors when forcing FL-DEF (the `R_min`/`R_max` slack) and again in FL-CUR ("the addressability half rests on FL-DEF, not FL-SND"), and Trace 7(a) exhibits a `sat`-satisfying link excluded by nullification. The non-membership half (`a ∉ findlinks((∗, Y, X, ∗), Σ)`) is unaffected, but the membership half is underived. The same shortcut appears in FL-CUR's gloss: "Current additions are included (a newly created matching link enters the answer)" — read literally, Trace 7(a) is a counterexample (a newly created link with `sat` true that does not enter).
**Required**: Add `a ∈ addressable(Σ)` (e.g., "and `a ∉ nullified(Σ)`") to the FL-DIR witness hypotheses; amend the FL-CUR gloss to "a newly created *addressable* matching link enters the answer."

### Issue 2: FL-WP case (a)'s `L_R^{Σ'} = L_R^Σ` step omits the value-preservation premise
**ASN-0121, FL-WP case (a)**: "ℓ does not enter `L_R` (either its slot-3 coverage is not the retraction class, or its arity exceeds 3), and ℓ is the only address `Σ.L` acquires, so `L_R^{Σ'} = L_R^Σ`" (and earlier in the same case: "no other tuple enters `L_R` either").
**Problem**: Address-freshness fixes only the new key. Membership of *existing* addresses in `L_R` depends on their stored values (the arity-3 conjunct and the slot-3 coverage-equality test), so "no tuple enters or leaves" additionally requires K.λ's value preservation at existing addresses (L12). Case (c) states this premise explicitly ("every prior tuple persists by L12, and `b` is the only address `Σ.L` gains"); case (a) leaves it implicit — inconsistent with the per-step citation discipline the rest of the section follows.
**Required**: Cite L12 (value preservation across K.λ) in case (a)'s `L_R`-fixity step, at both occurrences.

### Issue 3: FL-WP case labels out of presentation order, with a dangling forward reference
**ASN-0121, FL-WP**: Cases are presented in the order (a), (c), (b). Case (c) says "the term case (b) sets aside by scope, here *live*…" — referencing a scoping move the reader has not yet seen, since case (b) appears after (c). The section intro enumerates the three changes in presentation order (ordinary entry, retraction entry, survival), so the (a)/(c)/(b) labeling reads as insertion residue: a case added in a later cycle with a fresh label rather than renumbering.
**Problem**: Real reader friction; cross-references and the claims-table FL-WP entry inherit the scrambled order.
**Required**: Renumber the cases to match presentation order (or reorder presentation to match labels), repair the (b)/(c) cross-references in both case bodies, and mirror the fix in the claims-table FL-WP entry.

### Issue 4: Duplicated clarifications restated across sections
**ASN-0121, multiple sections** (anti-bloat per the review-mode classifier):
**Problem**: Three clarifications, each settled at its definition site, are restated nearly verbatim downstream:
- "I-address request / the grammar's only kind" appears five times: the request-grammar paragraph ("So the qualifier 'I-address request,' wherever it appears below, is simply every `q` the grammar admits"), the editing-stability intro ("there is no other kind in the grammar"), the FL-STB statement, the FL-REACH statement, and the claims-table FL-STB entry.
- The unit-depth vs. wider home-span treatment is given twice within a page: in the request-grammar paragraph ("The PrefixSpanCoverage citation discharges the subtree reading *only* for the unit-depth case; for a wider `H`, `athome` still bounds residence, now to an order-convex sub-range…") and again at the `athome` definition ("A wider home span bounds residence to an order-convex *sub-range* of a subtree… only the subtree *reading* of the residence bound does").
- The higher-arity rule ("slots `e₄ … eₙ` never enter `sat`") is stated in the grammar paragraph, again in FL-WILD prose, and again in the FL-WILD table entry; likewise "the link model exempts no type from search" is justified twice in the same section (the FL-WP intro via Nelson 4/41 and 4/44–45, then again opening case (c) via consultation Q2).
**Required**: Keep one canonical site per clarification (the `athome` definition for the span-width point; the grammar paragraph for the request-kind and arity points; the FL-WP intro for the no-type-exemption point) and delete the restatements; the claims table may keep its summary.

### Issue 5: Defensive meta-prose in structural slots
**ASN-0121, request-grammar paragraph and FL-WP case (b)** (anti-bloat):
**Problem**: Several passages explain why a claim is safe rather than what it says:
- The orphan sentence "This is the intended semantics for the operation." asserts intent and advances nothing.
- The long element-rooted-`H` parenthetical sits inside the request-type definition, burying one substantive fact (a wide element-rooted span can cover a document-level tumbler — the `p ⊕ ℓ` example) under totality reassurance ("there are no ill-formed inputs to exclude…", "Totality does not depend on vacuity in either case"). The definition of the request tuple is now buried mid-paragraph under roughly ten lines of caveat.
- Case (b)'s closing parenthetical explains at length why an *unasserted* full-index equation would fail ("We do *not* assert the corresponding equation over the full post-state index… the 'exact' simplification fails. Case (b) needs only the `dom(Σ.L)` slice…") — it works the fresh-retractor case that the case's own carrier (`a ∈ dom(Σ.L)`) already excludes.
- The state-introduction paragraph justifies its own placement ("so the monotonicity arguments that underwrite the permanence claims have the same state object to range over…"), and the `home(a)` note forward-points to its use site ("the residence bounding exercised at node granularity in Trace 6").
**Required**: Delete the intent sentence and the placement justification; relocate the wide-span document-tumbler fact to the `athome`/residence discussion and drop the totality framing; trim case (b)'s parenthetical to its first sentence ("This equation is stated and used only on the existing-link slice"), since cases (a)/(c) already own the fresh-`b` terms.

## OUT_OF_SCOPE

### Topic 1: Result ordering and enumeration
Nelson's text says the operation "returns a list"; the ASN specifies a set. The set abstraction is the right spec choice here; ordering, cursoring, and batching belong with FINDNEXTNLINKSFROMTOTHREE, which the scope list explicitly reserves.
**Why out of scope**: Presentation order of results is new territory for the pagination ASN, not an error in the membership semantics specified here.

### Topic 2: Version- and time-qualified inquiry
The ASN scopes FL-RET to current addressability and marks prior-state discoverability of retracted links as an open question.
**Why out of scope**: Version-scoped discovery requires the version graph and a state-indexed query form — a future ASN, correctly not claimed here.

### Topic 3: Federated completeness across stores
The final open question asks what completeness holds when links are homed in stores other than the one receiving the request.
**Why out of scope**: Inter-server protocol (BEBE) is explicitly excluded from this ASN's scope; the single-store guarantee is the right boundary for FL-CMP.

VERDICT: REVISE
