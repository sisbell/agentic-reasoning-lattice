# Review of ASN-0112

This note is thorough and the core proofs (V1–V2 coverage via D0/D1, the cross-subspace round-trip-failure case, the worked examples) check out. I find no correctness gaps. The note carries the `review-mode.anti-bloat` classifier, and the substantive findings are duplicated justifications and over-elaborated meta-prose that the precise reader must work around.

## REVISE

### Issue 1: Convexity justification duplicated verbatim across two sections
**ASN-0112, V6 and "Preconditions and well-definedness"**: V6 says "*The enclosure is forced rather than incidental: a span denotes one convex region (`⟦σ_d⟧` is order-convex under T1, ASN-0053 S0)*". The wp section repeats: "*V6's convexity justification explains why this dichotomy is forced rather than incidental: a single span is one convex region (ASN-0053 S0), so exact tracing of a separated series is structurally impossible.*"
**Problem**: Two paragraphs in the same document state the same argument in the same words ("forced rather than incidental," "one convex region," ASN-0053 S0). The wp section should cite V6, not re-justify it.
**Required**: Delete the convexity re-justification in the wp section; reference V6 by label for the dichotomy and keep only the wp-specific conclusion.

### Issue 2: Subspace-exhaustiveness claim restated three times
**ASN-0112, substrate list / V6 / wp section**: The S3★-aux exhaustiveness fact appears as "*There is no third subspace, so an arrangement occupies the content subspace, the link subspace, both, or neither*" (substrate), then "*The dichotomy is genuinely binary: by S3★-aux every occupied position carries `subspace = s_C` or `s_L` and nothing else...*" (V6), then "*The two directions exhaust the cases because S3★-aux confines every occupied V-position to one of exactly two subspaces: an arrangement occupies zero, one, or two subspaces and never a third*" (wp).
**Problem**: This is the "exhaustiveness claim" meta-prose pattern flagged for this note — the same fact about S3★-aux is re-asserted in three places to defend a case split. State it once where S3★-aux is introduced; the case-split sites need only the cite.
**Required**: Keep one statement of the binary-subspace fact; at V6 and the wp site, cite S3★-aux without re-explaining "no third subspace."

### Issue 3: V3 over-qualified with the same-depth caveat repeated five-plus times
**ASN-0112, V3**: Within one claim the same-depth qualifier recurs: "*among tumblers of the same depth as `max O(d)`*", "*The same-depth qualifier is load-bearing*", "*the next peer at the same depth*", "*among tumblers at the depth of `max O(d)` (`= #reach_d`)*", "*the same-depth tightness statement applies to `reach_d`, not to `σ_d` itself*" — and the claims table restates it again.
**Problem**: The qualifier is load-bearing once; restating it five times in the body plus the table is the kind of meta-prose the reader must skip past. The defensive "is load-bearing" aside and the closing `σ_d`-vs-`reach_d` disclaimer largely re-tread V2's reach biconditional.
**Required**: State the same-depth condition once, give the `max O(d).0` counterexample once, and drop the repeated reassertions and the V2-overlapping closing caveat.

### Issue 4: `endpoint-level-compatible` reinvents `level_compat` and earns no economy
**ASN-0112, "The substrate we measure"**: "*Following S6's `level_compat`, we call its two endpoints `start(σ)` and `reach(σ)` endpoint-level-compatible when `#start(σ) = #reach(σ)`.*"
**Problem**: This is S6's `level_compat(start(σ), reach(σ))` under a new name. At its sole substantive use (V2: "*the endpoint-level-compatible case `#origin_d = #reach_d`*") the term is immediately glossed by the inequality, so the label adds no economy — it is a reinvented term for a foundation predicate (Standard 7).
**Required**: Drop the coined term; write `level_compat(start, reach)` or `#origin_d = #reach_d` directly at the use site.

## OUT_OF_SCOPE

### Topic 1: Open Question on per-run extent composition
**Why out of scope**: The final Open Question (relating the whole-document span to bounding spans of individual correspondence runs) is genuinely future territory and correctly parked, not an error here. No action needed.

VERDICT: REVISE
