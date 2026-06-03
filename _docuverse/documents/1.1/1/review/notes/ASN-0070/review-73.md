# Review of ASN-0070

## REVISE

### Issue 1: F-canonical Step 1 analyzes a width-shape the canonical-form definition already excludes

**ASN-0070, F-canonical (CanonicalExistenceAndUniqueness), Step 1, Case `1 ≤ k < m_S(d)`**: "by case analysis on `k = actionPoint(ℓ)`... — *Case `1 ≤ k < m_S(d)`.*... so every `k < m_S(d)` is excluded by the same finiteness criterion."

**Problem**: F-canon-form clause (i) is a *definition* stated before the theorem, and it fixes each component width as an ordinal displacement `δ(c, m_S(d))`. An ordinal displacement `[0,…,0,c]` of length `m_S(d)` has action point exactly `m_S(d)`. So `k < m_S(d)` is impossible for any span of the canonical-form shape — the shape the theorem quantifies over. The existence half (Step 3) constructs spans with `δ`-widths directly and never considers `k < m`; the uniqueness half (Steps 4–5) quantifies only over canonical-shape (δ-width) families. Both downstream uses cite "Step 1's case `k = m_S(d)`" explicitly; neither cites the `k < m` subcase. The subcase is therefore not load-bearing for the stated theorem. Its sole function is to justify *why* the definition restricts to `δ`-widths — i.e., it is rationale for a definitional choice, the kind of "why the definition is as it is" prose the anti-bloat pass targets. As written, the note both pre-stipulates the δ-width in F-canon-form *and* re-derives that δ-widths are forced, having it both ways.

**Required**: Pick one. Either (a) drop the width pre-stipulation from F-canon-form clause (i) — let clause (i) require only a level-uniform span at depth `m_S(d)` with positive start — so that Step 1's `k < m` branch genuinely discharges the width restriction and becomes load-bearing for the theorem; or (b) keep the definitional δ-width and remove the `k < m` case from the proof, retaining only the `k = m` characterization (`⟦σ⟧_V = E`, `|⟦σ⟧_V| = c`) that Steps 3–4 actually consume. If the motivation for the δ-width choice is worth keeping, it belongs in a one-line remark on the definition, not as a non-cited case inside the existence/uniqueness proof.

## OUT_OF_SCOPE

### Topic 1: Cross-home resolution relationship and multi-server traversal consistency
**Why out of scope**: Both Open Questions (the `follow(ℓ,d,i)` vs `follow(ℓ,d',i)` relationship across documents transcluding shared homes, and the BEBE replication consistency obligation) are genuinely new territory. The first composes with future operation ASNs; the second is explicitly the replication/inter-server protocol, excluded by scope. Correctly posed as open questions rather than gaps.

VERDICT: REVISE
