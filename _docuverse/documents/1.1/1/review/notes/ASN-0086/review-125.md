# Review of ASN-0086

I checked the proofs (R0–R7a), the wp analysis, and the worked examples. The mathematics is careful and I found no correctness defect: R0a's cross-home zero-counting argument, R0a-Cor1's single-key contiguity induction, R0a-Cor2's zero-position-stability argument, the R0 freshness discharges over the state-local-conforming domain, R7a's interleaved replay, and both worked examples all check out arithmetically (including the nested-document case, where ASN-0093's anchor separator preserves prefix-incomparability). The findings below are the forward-reference/anti-bloat accretion the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Circular deferral between Nullify and WP Case 1
**ASN-0086, Definition — Nullify ("Single-tuple scope under R0a") and Weakest-Precondition Analysis, Case 1**: Nullify says "(The Weakest-Precondition Analysis, Case 1, cites this paragraph as the single-tuple-scope derivation site and analyzes the bare-vs-conforming-domain split there; we do not restate it here.)" WP Case 1 says "...is exactly the result proved under R0a in the Definition of Nullify (paragraph *Single-tuple scope under R0a*)... We cite that derivation here rather than repeat the antichain argument."
**Problem**: The two sections point at each other. To assemble the single-tuple-scope claim the reader bounces between them; neither is self-contained. This is exactly the flagged "multiple paragraphs in different sections defer to the same downstream location" pattern, here in its sharpest circular form.
**Required**: Put the full single-tuple-scope derivation (antichain plus bare-vs-conforming split) in one location and have the other cite it once, without the reciprocal "we do not restate it here / we cite that here" bookkeeping.

### Issue 2: Single-tuple-scope claim restated three times
**ASN-0086, Nullify Definition, WP Case 1, and Properties table (Nullify row)**: The same claim — "single-tuple scope holds at every conforming Σ from R0a; for the bare operation `P0 ∧ P1 ∧ PC` is sufficient but not weakest" — appears in all three slots in different words.
**Problem**: "Two paragraphs ... say the same thing in different words" (here three). The table row reproduces the wp-grade nuance rather than indexing the lemma.
**Required**: State the result once (Issue 1's consolidated site); reduce the table entry to a one-line pointer.

### Issue 3: Audit-vs-active quantification point developed with a deferral annotation, then restated
**ASN-0086, Definition — Nullified, and R6b**: The `nullified` definition carries "(The existential here quantifies over the *audit* slice `L_R^Σ` rather than the active subset `A_R^Σ`; the non-fixpoint consequence of that choice is developed once, in R6b ..., and cited from there rather than re-argued.)" R6b's statement and its proof then each restate the same audit-vs-active distinction.
**Problem**: The parenthetical is a use-site/deferral annotation that does not advance the definition's meaning ("developed once ... cited from there"), and the substantive point is then said a second and third time in R6b. The annotation is the bloat; the definition only needs to state *which slice the existential ranges over*.
**Required**: Drop the "developed once / cited from there" meta-sentence; keep the bare quantification fact at the definition and the consequence at R6b.

### Issue 4: at-most-one-key-per-home discipline re-explained at each use
**ASN-0086, Definition — substrate-conforming state; R0a-Cor1 proof; R7a discharge (4)(iii); Definition — substrate-conforming layer**: Each location re-explains, in its own words, that a step "deposits at most one fresh link key per home per step."
**Problem**: The discipline is defined once (clause (b)); the three downstream sites legitimately *cite* it but each re-narrates its content rather than referencing it. The re-narration is the accretion the classifier targets.
**Required**: State the discipline once; have R0a-Cor1, R7a, and the layer definition reference clause (b) by name without re-describing it.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Observe vs Emit, and the `nullified(Σ)` cardinality bound
**Why out of scope**: These are genuinely new territory (a consistency model and a structural-ratio guarantee), already correctly parked in Open Questions rather than asserted here.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
**Why out of scope**: The restriction to standard triples is stated and consistently maintained; the n-ary projection question is future work, not a gap in this note.

VERDICT: REVISE
