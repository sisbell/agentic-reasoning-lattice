# Review of ASN-0112

The proofs are sound: V2's two-case covering argument (round-trip closure via D1 for `#origin_d ≤ #reach_d`, direct TumblerAdd computation for `#origin_d > #reach_d`) checks out, the well-formedness/divergence bound `k ≤ #origin_d` is correctly split across single- and cross-subspace, V5/V6 exhaust S3★-aux, and the wp analysis is non-trivial with a concrete worked example. The abstract handling of `m_C ≠ m_L` is legitimate rigor (S8-depth permits distinct per-subspace depths), not imagined cases. My findings are confined to the accretion this cycle's `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Defensive "abstract vs realized `m_C = m_L`" prose duplicated across three sites
**ASN-0112, V-ReachTight body**: "This is strictly weaker than equal endpoint depths: it holds automatically in the single-subspace regime ... and, in the cross-subspace case, throughout `m_C ≤ m_L` — including the abstract `m_C < m_L` case that V2's first covering case admits, not only the realized `m_C = m_L`."
**Problem**: The claim *is* the formal biconditional `reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d`. The trailing clause does not advance it — it defends the "strictly weaker" framing and pre-empts a misreading ("not only the realized `m_C = m_L`"). The implementation-realization point it smuggles in already has a dedicated home: the "Implementation remark (reach tightness)" with its Q2 evidence. The reader must skip past this to reach the next claim.
**Required**: Drop the "abstract vs realized" editorializing from the V-ReachTight body; the formal condition plus the "automatic single-subspace" note suffice. Let the implementation remark carry the `m_C = m_L` realization with its evidence.

### Issue 2: V-LevelUniform body repeats the same essay along the orthogonal axis
**ASN-0112, V-LevelUniform body**: "... strictly non-level-uniform in the abstract case `m_C < m_L` that V2's first covering case admits. Under the implementation-realized discipline `m_C = m_L` (Q2) every returned span is level-uniform."
**Problem**: The "Under the implementation-realized discipline `m_C = m_L` (Q2)..." clause is a third copy of the realization point (after V-ReachTight and the implementation remark). The claim `σ_d level-uniform ⟺ #origin_d ≥ #reach_d` stands on its own; the implementation note belongs in the conformance section, not threaded into the claim statement.
**Required**: Remove the implementation-discipline clause from the V-LevelUniform body; reference the conformance section once if needed.

### Issue 3: Claims-table rows re-argue rather than summarize
**ASN-0112, Claims table, V-ReachTight and V-LevelUniform rows**: e.g. "...strictly weaker than equal endpoint depths; automatic single-subspace, and holding throughout `m_C ≤ m_L` (not only `m_C = m_L`) in the cross-subspace case" and "...always level-uniform in the single-subspace regime and under the realized `m_C = m_L` discipline, strictly non-level-uniform only when `m_C < m_L`."
**Problem**: The summary table reproduces the body's full abstract-vs-realized argument verbatim in spirit. A claims table should state the claim; here it re-litigates the same hedge a fourth and fifth time.
**Required**: Reduce these rows to the formal biconditionals plus a one-clause condition; remove the duplicated `m_C` case discussion.

## OUT_OF_SCOPE

(none — V12's single-subspace count derivation stays a derived consequence of the returned span and is correctly disclaimed for the multi-subspace case in Open Questions, so it does not drift into link-counting/RETRIEVEDOCVSPANSET territory.)

VERDICT: REVISE
