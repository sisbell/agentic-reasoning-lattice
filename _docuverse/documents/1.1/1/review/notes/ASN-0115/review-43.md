# Review of ASN-0115

## REVISE

### Issue 1: Forward-reference deferral pointer in the V-spec definition
**ASN-0115, §"What a spec-set is, and what delivery is" (V-spec definition)**: "The depth conjunct is therefore re-evaluated at each consulting state, not fixed at mint; how that re-evaluation bears on delivery is settled where `act` is defined (below) and by its R6 consequence."
**Problem**: This is a pure deferral pointer of the flagged kind. The depth-compatibility phenomenon is then introduced a *second* time in the `act` definition (the "bites"/"vacuous no-op" analysis) and re-derived a *third* time inside R6's proof (the depth-incompatible / `V_S=∅` / `#s=m_S` case split). One concept is spread across three sites, and this sentence's only function is to point forward to two of them. The reader reaches `act` and R6 regardless; the clause carries no content of its own.
**Required**: Drop the "how that re-evaluation bears on delivery is settled where `act` is defined (below) and by its R6 consequence" clause. Keep the substantive observation (the conjunct is re-evaluated per state because `m_S(d)` is mutable) once, and let `act`/R6 do the work without the signpost.

### Issue 2: Non-advancing provenance enumeration in the `act` definition
**ASN-0115, §"What a spec-set is, and what delivery is" (`act` prose)**: "In the override branch — any consulting-state depth mismatch, `V_S(d) ≠ ∅ ∧ #s ≠ m_S(d)`, whatever its provenance (a start depth-matched at mint but whose subspace has since been re-pinned to a different depth, or one minted against an empty subspace and never depth-matched) — the active set is forced empty..."
**Problem**: The sentence states that provenance is irrelevant to the behavior ("whatever its provenance … the active set is forced empty"), then enumerates two provenances anyway. The override fires on `#s ≠ m_S(d)` and on nothing else; the parenthetical is a use-site inventory that does not advance the definition's meaning, and the same provenance story is already told once in the V-spec re-evaluation paragraph above. This is the "skip past it to follow the claim" pattern.
**Required**: Cut the parenthetical. The condition `V_S(d) ≠ ∅ ∧ #s ≠ m_S(d)` is the whole content of the override branch.

### Issue 3 (minor): R2's justification imports a temporal invariant the single-state claim does not use
**ASN-0115, §"Faithfulness, and where the invariant stops" (R2 proof)**: "The value at the resolved address is fixed for all time because `Σ.C` is immutable (S0): the byte at an I-address never changes after creation." — and the claims table's "(from S2 + S0)".
**Problem**: R2 is a single-state denotational equality, `item(v, ρ, Σ).val = Σ.C(Σ.M(d)(v))`, which holds by the definition of `item` once resolution is single-valued (S2) and lands in the store (S3★). "Fixed for all time" (S0) is a cross-state property — it is precisely what R7 (Repeatability) and R11 (PermanentSourcing) discharge. Importing S0 into R2 is a defensive justification that duplicates R7/R11 and blurs which invariant carries which guarantee.
**Required**: Scope R2's justification to S2 (resolution is single-valued) and the `item` definition (optionally S3★ for store membership). Attribute permanence-across-time to R7/R11 where it is actually load-bearing, and drop the "(+ S0)" credit from R2.

## OUT_OF_SCOPE

None. The note stays on content delivery; the genuinely future-ASN topics (inline provenance, failure-instead-of-partial, dangling references under relaxed S3★, channel faithfulness, subspace-straddling spans) are correctly held as Open Questions rather than claimed.

VERDICT: REVISE
