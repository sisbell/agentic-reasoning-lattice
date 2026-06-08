# Review of ASN-0107

## REVISE

### Issue 1: P1 declares deduplication a settled obligation, but Open Question 4 reopens it as undecided

**ASN-0107, P1 (LinkAtomicity) vs. Open Questions**: P1 states "faithfulness to it is a deduplication obligation, not an optional optimisation. The abstract claim is that the count is of the *set*". Open Question 4 asks: "Must a conformant implementation guarantee set-semantics by deduplicating multi-span matches before sizing, or may idempotence of counting be left as a discipline on the query layer?"

**Problem**: These contradict. P0/P1 fix `num` as set cardinality and the P1 prose asserts the dedup obligation as already decided ("not optional"). Q4 then frames the same question as open. A reader cannot tell whether the spec mandates set semantics or leaves it open.

**Required**: Resolve one way. Either soften P1's "obligation" language (if the conformance question is genuinely open), or remove/reframe Q4 (since P1 already settles that the count is of the *set*, and any conformant implementation must therefore honor it — the *mechanism* of dedup being below the spec).

### Issue 2: E2 cites single-step L12a for a multi-step monotonicity claim

**ASN-0107, E2 (ExistenceMonotonicity)**: "`Σ →* Σ' ⟹ num(Q, Σ) ≤ num(Q, Σ')`. The store grows (L12a)".

**Problem**: L12a (LinkStoreMonotonicity) is a single-step lemma (`Σ → Σ'`). E2 quantifies over the reflexive-transitive closure `Σ →* Σ'`. E1 — one claim earlier — correctly cites the multi-step form (LP3★). The note is otherwise meticulous about ★-closures, so the bare L12a citation here is an inconsistency, not a convention.

**Required**: Cite the multi-step closure (ASN-0098's Store Monotonicity★, or an explicit transitive-closure step over L12a), matching E1's treatment.

### Issue 3: R1's closing paragraph is reviser-drift meta-prose

**ASN-0107, R1 (MinimalDecrementNoStoreRetraction)**: "The `−1` is the minimal *non-trivial single-link* effect, not a floor on contraction effects in general: a contraction may equally leave the count unchanged (`Δ = 0`, the partial-survival situation of R3) or, when the deleted endpoint is shared, drop it by more than one (`Δ = −k`, R2)."

**Problem**: This sentence imagines a misreading of the claim ("not a floor") and then restates R2 and R3 to rebut it. The carrier already states `Δnum_disc ∈ {−1, 0}` under explicit preconditions; defending against a generalization the claim never made, and re-deriving R2/R3's content here, is noise the reader must skip past. The preceding sentence ("A link is a single unit... severing it does not cascade") likewise re-states P1.

**Required**: Delete the defensive "not a floor" sentence; R2 and R3 carry those cases. Keep only the no-cascade fact if it is load-bearing, stated once.

### Issue 4: "consultation evidence is emphatic" — provenance prose that does not advance the argument

**ASN-0107, "Two Anchorings" intro**: "The crux of the operation's meaning is *how the three address sets are obtained* ... and the consultation evidence is emphatic that they differ precisely in monotonicity."

**Problem**: The appeal to "consultation evidence" is meta-commentary about the note's own development, not a step in the reasoning. The monotonicity difference is established by E2 and D2 directly; the sentence adds only sourcing flavor.

**Required**: Drop the "consultation evidence is emphatic" clause; let E2/D2 carry the distinction.

## OUT_OF_SCOPE

### Topic 1: Independently anchored, separately evolving request parts (Open Question 1)
**Why out of scope**: This is correctly listed as an open question — it asks for invariants under multi-document anchoring not defined here, genuine future territory, not a gap in the present count semantics.

### Topic 2: Agreement between `num` and the cardinality the retrieval operation returns (Open Question 3)
**Why out of scope**: Returning the matching links is FINDLINKS / ASN-0099 (explicitly out of scope). Cross-operation cardinality agreement belongs there, and the note properly defers it.

VERDICT: REVISE
