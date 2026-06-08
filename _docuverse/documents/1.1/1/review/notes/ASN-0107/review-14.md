# Review of ASN-0107

## REVISE

### Issue 1: R6's retention set is characterized as an arbitrary subset, not K.μ⁻'s canonical form
**ASN-0107, R6 (CountedLinkPreservationWP)**: "a K.μ⁻ contraction on d_q with retention set `R ⊆ dom(Σ.M(d_q))`, so the post-state `Σ' = K.μ⁻[d_q, R](Σ)` satisfies `Σ'.M(d_q) = Σ.M(d_q) ↾ R`"
**Problem**: K.μ⁻ (PerSubspaceContractionScope, ASN-0047) does not admit an arbitrary retention subset. Its retention is a per-subspace *prefix* set `R := ⋃_S {[S,1,…,1,k] : 1 ≤ k ≤ n'_S}` derived from retention counts. Writing `K.μ⁻[d_q, R]` for an arbitrary `R ⊆ dom(Σ.M(d_q))` names operations the substrate cannot realize (e.g. retaining `[1,2]` while dropping `[1,1]` violates D-MIN★/D-CTG★). The mirrored lemma it cites — LP12a — correctly defines `R` as the canonical retention set, so R6 is looser than its own model.
**Required**: Restrict `R` to the admissible per-subspace prefix retention set exactly as K.μ⁻ and LP12a define it, rather than an arbitrary subset.

### Issue 2: The "no store-level retraction / k=1 specialization" point is restated across four claims
**ASN-0107, retraction-section intro, R1, R2, R5**: the substrate-has-no-link-removal fact appears in the section opener ("never from the store … no link-removal transition (L12), and udanax-green confirms…"), again in R1 ("No transition removes a link from dom(Σ.L), so num registers no 'retraction'…"), again in R2 ("There is no separate per-link retraction operation that subtracts exactly one…"), and again in R5 ("there is no subtractive term: the store never loses an address (L12)…"). Separately, the "R1 is the k=1 case of R2" relationship is asserted three times (R1 table entry, R2 body, R6 body).
**Problem**: Under the `review-mode.anti-bloat` classifier this is redundant restatement — the same fact carried by L12 is re-derived in each claim's prose, and the k=1 cross-link is announced from both ends. The reader must reconcile four phrasings of one invariant.
**Required**: State the no-removal consequence once (it is just L12 + E2), and let R1/R2 cite it rather than re-argue it; assert the k=1/k=general relationship in one location.

### Issue 3: Defensive parenthetical referencing prior "concerns"
**ASN-0107, "State and the Counting Request"**: "A zero is a legitimate answer, not a fault (this discharges the well-formedness concerns of the empty-specset and no-match cases)."
**Problem**: The surrounding text already establishes totality and the `num = 0` cases positively. The parenthetical adds nothing to the argument — it points back at review concerns rather than advancing the claim, the defensive-justification pattern the anti-bloat classifier targets.
**Required**: Drop the parenthetical; the positive statement of totality and the degenerate cases suffices.

## OUT_OF_SCOPE

### Topic 1: Independently-anchored, separately-evolving request parts
**Why out of scope**: The first Open Question (different documents' arrangements per slot) is genuinely new territory — multi-document anchoring is not what this single-document count operation specifies. Correctly deferred, not an error here.

### Topic 2: Relationship between the count and the retrieval operation's returned set
**Why out of scope**: The count-vs-FINDLINKS staleness relationship belongs to ASN-0099 (FINDLINKS), explicitly listed out of scope. The ASN correctly raises it only as an Open Question.

VERDICT: REVISE
