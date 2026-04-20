# Review of ASN-0082

I have read the ASN in full and checked every postcondition, frame condition, consistency argument, structural preservation proof, span-level derivation, and boundary case against the foundations (ASN-0034, ASN-0036, ASN-0053).

## Analysis

**I3 and its eight clauses.** The postcondition, vacating clause, frame conditions, and domain closures are mutually consistent. The consistency verification is explicit and complete — pairwise disjointness of the three assignment regions (shifted, left, cross-subspace) is established via TS4 (shifted > original ≥ p > left), TS2 (injectivity among shifted), and subspace separation. I3-V and I3-CS agree: vacated positions are exactly those excluded by the closure clause's disjunction. No double-assignment is possible (I3-S2).

**Structural preservation.** I3-VD (S8-depth), I3-VP (S8a), I3-S3 (referential integrity), I3-S2 (functionality), and I3-fin (finiteness) are each derived with explicit case analysis over the three regions (left, shifted, cross-subspace). Every case traces back to the relevant foundation property on the pre-state plus the shift's structural guarantees (result-length identity, component copying, injectivity). No case is elided.

**Span-level derivation (I3-S).** The commutativity argument in I3-S(a) is correct: since both δₙ and ℓ have action point m (the ordinal-level precondition), both are of the form [0, ..., 0, x], making δₙ ⊕ ℓ = ℓ ⊕ δₙ by commutativity of natural-number addition. The two TA-assoc applications have their preconditions verified (actionPoint ≤ length at each step). The chain reach(σ') = (s ⊕ δₙ) ⊕ ℓ = s ⊕ (δₙ ⊕ ℓ) = s ⊕ (ℓ ⊕ δₙ) = (s ⊕ ℓ) ⊕ δₙ = shift(reach(σ), n) is sound. The S6 application for the final step (#reach(σ) = m) is valid since σ is level-uniform. The restriction to ordinal-level spans is necessary — I verified that commutativity fails when action points differ.

**Boundary cases.** Insert at start (I3-L vacuous, all positions shift), insert past end (I3 vacuous, all positions preserved), empty document (both vacuous), and the overlap case ([1,5] as both original and shifted destination) are all traced explicitly. The I3-V trace in the overlap case correctly identifies that [1,5] ∈ shifted-image-set prevents vacating, and I3 governs its post-state value.

**Invariants not preserved.** The ASN correctly identifies D-CTG, D-MIN, and D-SEQ as violated by the shift, demonstrates the D-CTG violation concretely ({[1,1], [1,2], [1,5], [1,6], [1,7]} has a gap), and defers restoration to the INSERT ASN. This is the right separation of concerns.

**Foundation citations.** All references are to ASN-0034, ASN-0036, or ASN-0053 — all listed foundations. No non-foundation ASN references.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Composability of shifts
Multiple insertions at different positions in the same subspace would require reasoning about how shifts compose (shift₁ followed by shift₂). This is operation-sequence territory for the INSERT ASN or a dedicated composition result.
**Why out of scope**: I3 specifies a single shift; composition is new territory.

### Topic 2: Lifting I3-S beyond ordinal-level spans
The ordinal-level restriction (actionPoint(ℓ) = m) is necessary for the commutativity argument. Whether a weaker result holds for general level-uniform spans (perhaps with a width-transformation formula instead of width preservation) is an open algebraic question.
**Why out of scope**: This would extend the span algebra, not fix an error in this ASN.

VERDICT: CONVERGED
