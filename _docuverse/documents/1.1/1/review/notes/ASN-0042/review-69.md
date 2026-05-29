# Review of ASN-0042

## REVISE

### Issue 1: O1a and O1b are simultaneously labeled axioms and proved by induction
**ASN-0042, Properties table / Account-Level Boundary / Delegation**: The summary table lists O1a and O1b as "axiom (`pfx` signature constraint)". The `pfx` Formal Contract says the opposite: "*Related properties (stated separately): injectivity is O1b; the account-level boundary ... is O1a. These constrain `pfx` globally but are postconditions of those properties, not of the present axiom.*" Then the *Delegation* section proves "*Delegation preserves O1a*" and "*Delegation preserves O1b*" by induction, concluding "*By induction on the reachability sequence, O1a holds in every reachable state.*"
**Problem**: The status is genuinely contradictory. If O1a/O1b are axioms constraining the codomain of the primitive `pfx` for all `π ∈ Π`, the inductive preservation proofs are vacuous — no principal can violate them — and condition (iv)/(v) of `delegated` do no work. If they are derived invariants (base case O14 clauses (iii)/(iv), inductive step delegation conditions (iv)/(v)), then the table label "axiom" and the framing "*two structural constraints on the primitive `pfx`*" are wrong. You cannot have it both ways: either the induction is load-bearing (→ derived) or it is redundant (→ cut it).
**Required**: Decide. Because Π grows by O15 and O15 alone does not force `zeros ≤ 1` / injectivity, these must be derived invariants. Relabel O1a/O1b as derived (like FiniteRegistry), state O14(iii)/(iv) as their base cases, and remove the "signature constraint / axiom" framing — or, if they are truly axioms on `pfx`'s codomain, delete the inductive preservation paragraphs as redundant.

### Issue 2: The T8-vs-B0 parenthetical is repeated verbatim across the document
**ASN-0042, O3 / O4 / PrefixBaptismCoupling / O8 / OwnershipDomainPermanence★ / O10**: The same clarification — "*(T8 of ASN-0034 establishes allocator-domain monotonicity `allocated(s) ⊆ allocated(s')`, not baptismal-registry monotonicity; the registry monotonicity needed here is B0's distinct claim.)*" — appears, reworded, at least five times.
**Problem**: "Two paragraphs in the same document say the same thing in different words." The distinction is real and worth stating, but it is restated at every use site, forcing the reader past identical meta-prose.
**Required**: State the T8/B0 distinction once (e.g., in the *State Axioms* notation paragraph) and cite B0 directly thereafter without re-explaining why T8 is the wrong lemma.

### Issue 3: DelegatorAllocatesPrefix duplicates O18's "two views of one act" prose
**ASN-0042, DelegatorAllocatesPrefix invariant**: "*The delegation act is one event recorded in two views, not two independent acts that happen to coincide.*"
**Problem**: This is the same claim as O18's "*the registries are two views of the same act, not independent ledgers that happen to agree*", restated in the contract of a property whose only content is `allocated_by_{Σ'}(π_d, pfx(π'))`. The coupling idea is already carried by O18.
**Required**: Drop the restatement; let DelegatorAllocatesPrefix state its postcondition and cite O18 for the coupling.

### Issue 4: Use-site inventories around axioms and definitions (forward-reference accretion)
**ASN-0042, O14 seventh clause / Reachability convention / MostSpecificCoveringUnique**:
- O14: "*The seventh clause closes that gap and is invoked by the worked example's self-ownership-at-the-prefix argument and by O10's non-coverage analysis (which needs every sub-delegate's prefix ... to sit in `Σ.B` so that `hwm` reflects pre-claimed slots).*"
- Reachability convention: "*This convention is load-bearing for the proofs below: the iterated application of O12 ... underpins the bootstrap-exclusion arguments in O3, O8, and OwnershipDomainPermanence. The reachability hypothesis also underpins the induction in O4 ... and through O4, propagates to O2 ...*"
- MostSpecificCoveringUnique: "*The corollary is the precise content of condition (ii) of the `delegated` relation when read jointly with O1b ...*"
**Problem**: These enumerate downstream consumers rather than advancing the axiom/definition's meaning — exactly the "definition's introduction enumerates downstream consumers" pattern. They rot as consumers change and force the reader to track a dependency ledger embedded in prose.
**Required**: Each property's contract already states what it guarantees; let consumers cite it. Delete the consumer inventories.

### Issue 5: O10's "longer Form B sub-delegates" sub-paragraph re-treats a case already excluded
**ASN-0042, O10 non-coverage analysis**: After establishing "*any Form B sub-delegate of length `> #pfx(π) + 2` is not a prefix of `a'` by length alone*", the proof adds a separate sub-paragraph "*PrefixBaptismCoupling and longer Form B sub-delegates*" that re-examines those same longer sub-delegates and concludes "*This is harmless: even if `U^{(i)}_1 = hwm_0 + 1`, the longer prefix does not prefix `a'`.*"
**Problem**: Reviser drift — the paragraph imagines a case (`U^{(i)}_1 = hwm_0 + 1` for an over-length prefix) that the length argument already excluded from coverage. It reads like a relocated prior finding rather than a step that advances the proof.
**Required**: Remove the sub-paragraph; the one-line length exclusion already discharges these sub-delegates. (Relatedly, the Form B treatment of `pfx(π).0` — "*excluded by T4a's no-trailing-zero clause*" — restates condition (v) validity already in force; trim to a single citation.)

### Issue 6: The worked example's B6/B1/hwm bookkeeping drifts into baptism-mechanism territory
**ASN-0042, Worked Example (Bootstrap seeds table, Trajectory, Sub-account namespaces, Fork)**: The example tabulates bootstrap seeds, traces each `Bop` call's B6 check and B1 contiguity obligation, and tracks `hwm` advances across `S(p,d)` streams in detail.
**Problem**: "Baptism mechanism and allocation invariants" are declared OUT OF SCOPE for this ASN. Verifying that each baptism satisfies B6/B1 is ASN-0040's responsibility; reproducing that verification at this volume is bloat that obscures the ownership claims (O0–O10) the example is meant to witness.
**Required**: Reduce the trajectory to the ownership-relevant facts (which addresses are baptized, who covers them, what `ω` resolves to). Cite ASN-0040 B6/B1 for well-formedness rather than re-deriving each check inline.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer machinery
**Why out of scope**: The ASN correctly records transfer as an open question (the tension between O3/O6 inalienability and Nelson's "bought the document rights"). Specifying a transfer regime and its invariants is new territory for a future ASN, not a defect here.

### Topic 2: Cross-node identity federation
**Why out of scope**: O9 establishes node-locality; the invariants a federation would need to preserve are listed under Open Questions and belong to a later ASN.

META: The model defines ownership state (Π, `pfx`, `allocated_by`), an operation (delegation), and abstract invariants (exclusivity, coverage, refinement) that any conforming implementation must satisfy — it is on-track as a specification; the findings are bloat and a status inconsistency, all fixable.

VERDICT: REVISE
