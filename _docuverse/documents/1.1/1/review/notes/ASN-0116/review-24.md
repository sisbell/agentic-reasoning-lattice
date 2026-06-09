# Review of ASN-0116

This is a careful, rigorous specification — the two-layer split is maintained cleanly, the I3-family citations are correctly restricted to arrangement facts (and the non-transferring lemmas I3-S3/I3-S7/D-SEQ-post are flagged and discharged directly), boundaries are covered (append, empty subspace, front-insert), and the wp (P6) is genuinely non-trivial. The findings below are anti-bloat (the note carries `review-mode.anti-bloat`) plus one claim redundancy.

## REVISE

### Issue 1: The interval/disjointness argument is stated three times
**ASN-0116, "The document remains one coherent sequence"**: The same consecutive-disjoint-union computation over the index intervals `{1,…,J-1}`, `{J,…,J+n-1}`, `{J+n,…,N+n}` appears:
- opening paragraph: "These are consecutive integer intervals with no gap and no overlap; their union is `{1, …, N+n}`. Therefore `V_S(d') = {q_1, …, q_{N+n}}`…";
- "Contiguity of the filled post-state": "These are consecutive integer intervals — no gap — and pairwise disjoint — no double assignment — with union `{1, …, N+n}`. Therefore `V_S(d') = {q_1, …, q_{N+n}}`…";
- "Single-valuedness" bullet: "the three integer intervals are pairwise disjoint (shown below)."

**Problem**: Three statements of one argument in a single section, with a forward "(shown below)" tying the bullet to the contiguity paragraph. This is the "two paragraphs say the same thing" / "multiple paragraphs defer to the same downstream location" pattern. The contiguity claim is genuinely load-bearing, but it should be proved once.
**Required**: Give the interval computation once (the "Contiguity of the filled post-state" paragraph is the natural home, since it carries the D-SEQ/D-MIN/D-CTG conclusion), and have the opening I-DOM statement and the single-valuedness bullet cite it rather than re-derive it.

### Issue 2: P3 (AddressPermanence) restates P2 ∧ P0 with no new formal content
**ASN-0116, "Invariants the operation must preserve"**: P3 reads "No I-address in `dom(C)` is removed or rebound by INSERT: `(A b : b ∈ dom(C) : b ∈ dom(C') ∧ C'(b) = C(b))`, and every new binding is at a fresh address (P0)."
**Problem**: P2 (ContentAppendOnly) already gives `dom(C) ⊆ dom(C')` and `C'(b) = C(b)`, which entails P3's first conjunct verbatim; P3's second conjunct is P0. So P3 ≡ P2 ∧ P0, contributing no new formal statement. The "Position permanence" narrative (distinguishing permanent I-address from impermanent V-position) is valuable, but the boxed claim duplicates two existing claims.
**Required**: Fold the I-address-permanence point into the prose and drop the redundant boxed claim, or have P3 state something P2 ∧ P0 does not (e.g., the V-position impermanence half, which the prose argues but no claim captures).

## OUT_OF_SCOPE

None. The Open Questions (transclusion at a shared position, concurrent insertion freshness, transcluded-content provenance, post-edit fragmentation) are correctly deferred to future ASNs and are not stated as claims here.

VERDICT: REVISE
