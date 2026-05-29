# Review of ASN-0036

This ASN carries the `review-mode.anti-bloat` classifier. The mathematics is sound — I checked S1, S4, S5 (both constructions), S7, S8 (within- and cross-subspace uniqueness, including the m=2 collapse), D-CTG-depth, and D-SEQ, and found no correctness gaps, no missing boundary cases (empty arrangement is handled vacuously in S8 and D-CTG), and no improper non-foundation cross-references. The findings below are accreted meta-prose: the same claims restated across cycles.

## REVISE

### Issue 1: "attribution is structural, not detachable metadata" asserted three times
**ASN-0036, S7 (prose and proof)**: The same point appears as (intro) "It is not metadata that can be stripped or forged — it IS the address."; (S7a) "The address IS the provenance"; (proof, Permanence) "The attribution cannot be severed because it is not a separate datum attached to the content — it is a structural property of the address itself."
**Problem**: One claim, three near-identical statements in different words. This is the "two paragraphs say the same thing" pattern the anti-bloat pass targets — essay reinforcement, not advancing reasoning.
**Required**: State the structural-not-metadata point once (it belongs in the proof's Permanence step, where it is load-bearing) and remove the intro and S7a restatements.

### Issue 2: S7 body prose pre-proves the proof's "Uniqueness across documents" step
**ASN-0036, S7 body**: "Since document creation is an allocation event within a system conforming to T10a, GlobalUniqueness (ASN-0034) directly guarantees that distinct documents have distinct tumblers, and therefore distinct document-level prefixes."
**Problem**: This is the identical derivation (allocation event → GlobalUniqueness → distinct prefixes) carried out formally in the proof's "Uniqueness across documents" paragraph and already asserted in S7d's postcondition. The fact now appears three times: S7d postcondition, S7 body, S7 proof. The body sentence justifies the result before the proof establishes it.
**Required**: Let S7d's postcondition state it and the proof establish it; drop the pre-proof from the body prose.

### Issue 3: S8 conjunct (b) "definition, not a theorem" stated four times
**ASN-0036, S8**: "Conjunct (b) is a definition of the labeled partition, not a theorem." (statement) / "this is the labeled partition of conjunct (b), well-defined precisely because..." (proof) / "yielding the labeled partition (b) — a definition, not a proved postcondition." (postconditions) / "(b) definition" (table).
**Problem**: The status clarification accreted across cycles (the recent S8 "clarify labeled partition" revision). Asserting the same status four times is noise the reader must skip past.
**Required**: State the status once, in the S8 statement. The proof and Formal Contract can treat (b) as a labeling without re-litigating its theorem/definition status.

### Issue 4: ValidInsertionPosition postcondition (b) asserted without derivation
**ASN-0036, ValidInsertionPosition non-empty case, postcondition (b)**: "v satisfies S8a: zeros(v) = 0 and all components positive."
**Problem**: The prose gives the explicit form `v = [1, 1, ..., 1+j]` but never connects it to (b) — the reader must observe that all leading components are 1 and the last is `1+j ≥ 1`, hence `zeros(v)=0`. A one-line derivation is owed, since postconditions stated without their derivation are exactly what the depth standard rejects.
**Required**: Add the one-step derivation: from the explicit form, every component is ≥ 1, so `zeros(v)=0` and S8a's positivity hold.

## OUT_OF_SCOPE

### Topic 1: Operation preservation of D-CTG, D-MIN, S2 under INSERT/DELETE at a ValidInsertionPosition
**Why out of scope**: The ASN correctly defers this to the operations layer (Open Questions), and operation frame/postconditions are listed as out of scope. ValidInsertionPosition is framed as a state-derived predicate, not an operation contract, so it stays in scope; its preservation obligations do not.

VERDICT: REVISE
