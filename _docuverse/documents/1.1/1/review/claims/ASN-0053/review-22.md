Reading ASN-0053 as a system, the canonical standalone claim blocks (S0–S11d with Formal Contracts) are largely sound — recent revisions correctly added the `reach ∈ T` carrier discharges via TumblerAdd, and the SC/WF/WR precondition chains close. The issues I found are cross-claim: a citation that a foundation claim explicitly disclaims, and drift between the running-narrative proofs and the standalone claim cards.

### S3b (narrative) cites S3a for span identity that S3a explicitly disclaims
**Class**: REVISE
**Foundation**: S3a (MergeCommutativity); S3 (MergeEquivalence)
**ASN**: Narrative S3b, Case B: "By S3a (merge commutativity) the merge of α and β equals the merge of β and α, which is the Case A configuration with the roles of α and β exchanged. Applying Case A to the pair ⟨β, α⟩..."
**Issue**: The step needs the *constructed span* merge(α,β) to equal merge(β,α) — identity of (start, width) pairs — so that Case A applied to ⟨β,α⟩ reproduces the Case B merge. But S3a establishes only denotational equality (⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧). The standalone S3a's own contract states this exactly: "The equality is denotational... not that the merge constructs an identical (start, width) pair... that the constructed pairs coincide is a separate fact, owed to the symmetry of S3's min/max endpoint formula, and is not what this lemma establishes." So the narrative justifies the step with the one lemma that disclaims it. (The conclusion is true — S3's min/max formula is symmetric — but the cited evidence does not support it.) The standalone S3b block avoids this by deriving Case B directly from S3's merge formula; the two copies have diverged.
**What needs resolving**: The narrative S3b Case B must justify merge(α,β) = merge(β,α) from S3's symmetric min/max endpoints (as the standalone version does), not from S3a — or the duplicate narrative proof should be removed in favor of the standalone.

### Narrative proofs omit the WF carrier-membership step the standalone versions add
**Class**: OBSERVE
**Foundation**: WF (preconditions `s, r ∈ T`); TumblerAdd (carrier postcondition `a ⊕ w ∈ T`)
**ASN**: Narrative S1, S3, S4, S8, S11, S11c each invoke WF on an endpoint pair whose reach endpoint is a sum `reach(σ) = start(σ) ⊕ width(σ)` — e.g. narrative S1: "with s' < r', WF gives that the pair γ = (s', r' ⊖ s')..." — without first placing `r' ∈ T`.
**Issue**: WF requires both endpoints in T. For the reach endpoints this is not immediate (they are computed sums) and requires the TumblerAdd carrier postcondition. The standalone blocks (S1, S3, S4, S8, S11, S11c) all now discharge this explicitly; the running-narrative copies do not. The two presentations of each proof have drifted, and the narrative copies carry the older gap.
**What needs resolving**: Reconcile the narrative proofs with the corrected standalone versions, or eliminate the duplication so a single authoritative proof of each S-claim exists.

### D0 listed as "cited" but never invoked
**Class**: OBSERVE
**Foundation**: D0 (DisplacementWellDefined)
**ASN**: Properties Introduced table: "D0 | Displacement well-definedness... | cited"; reach-function section: "WF and WR below discharge the conditions under which it round-trips."
**Issue**: WF round-trips via D1 and WR via D2; no proof in the ASN invokes D0. The "cited" status overstates the dependency.
**What needs resolving**: Either cite D0 where it is actually used or drop it from the cited list / declared dependencies.

### Proof content occupying Axiom and other structural slots
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: Standalone S1 *Axiom* slot ("By S6, level-uniformity... forces all four boundary tumblers... WF yields well-formedness of γ"); standalone S11 *Axiom* slot (a full paragraph of the proof's carrier/length derivation); S6 Depends→TumblerAdd ("This is the sole source of the addition result-length: the in-scope foundations supply only the subtraction length... neither of which yields #(s ⊕ ℓ) = #ℓ"); S2 Depends→T12 ("T12 does not supply S2's preconditions...").
**Issue**: The *Axiom* slots hold derived reasoning, not posited axioms, and the Depends entries hold use-site inventories and "why this foundation is needed" essays rather than "what it supplies." This is the reviser-drift pattern (explaining need vs. content, defensive justification) the precise reader must read past to find the claim.
**What needs resolving**: Move derivations out of Axiom slots into the proof; trim Depends entries to state what each foundation provides.

VERDICT: REVISE