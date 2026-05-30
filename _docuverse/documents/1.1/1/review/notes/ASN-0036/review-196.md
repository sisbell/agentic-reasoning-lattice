# Review of ASN-0036

## REVISE

### Issue 1: S8a notation bookkeeping enumerates citation behavior

**ASN-0036, "Two components of state" and Properties Introduced table**: The domain-restriction axiom is followed by a *Postcondition (per-component form)* ending "We abbreviate this unfolded form 'S8a' wherever it is cited below," and the table carries a separate row: "S8a (notation) | Not a property — abbreviates the per-component form of the domain-restriction axiom above; every downstream citation of 'S8a' cites that axiom | notational."

**Problem**: "wherever it is cited below" and "every downstream citation of 'S8a' cites that axiom" are use-site inventories — meta-prose about how the abbreviation will be referenced, not content advancing the definition. This is the residue the anti-bloat classifier targets: a definition row that describes its own downstream consumers rather than stating meaning. The reader must skip past the citation-bookkeeping to reach the actual equivalence.

**Required**: Keep the equivalence (`zeros(t)=0 ⟺ all components positive`, by T0) inline at the axiom and define "S8a" in one clause. Delete the "wherever it is cited below" tail and collapse the standalone table row into the domain-restriction row, or drop it entirely.

### Issue 2: ValidFirstInsertionPosition Depends imagines an excluded future state

**ASN-0036, ValidFirstInsertionPosition Depends**: "(D-MIN is not consumed here: its antecedent `V_1(d) ≠ ∅` is false in the empty case. The choice `v = [1, ..., 1]` is made only so that it matches the minimum D-MIN will demand once the subspace becomes non-empty.)"

**Problem**: This is a defensive justification of a *non*-dependency plus a paragraph imagining a case the predicate's own precondition (`V_1(d) = ∅`) excludes — exactly the reviser-drift pattern. A Depends list states what the claim consumes; it does not need to argue why it omits D-MIN, nor narrate a hypothetical later state in which the subspace becomes non-empty.

**Required**: Remove the parenthetical. If the alignment with D-MIN is worth recording at all, it belongs as a one-clause design note where the empty-case choice `v = [1,...,1]` is *made*, not in the dependency list of a predicate whose antecedent forbids the imagined state.

### Issue 3: S8 chain lemma asserted, not shown

**ASN-0036, S8 proof, "Chain decomposition"**: "An injective acyclic partial function on a finite set partitions that set into disjoint maximal chains."

**Problem**: This is the load-bearing combinatorial step that delivers the partition, stated as a bare fact. The surrounding proof carefully establishes `succ` is a partial function (out-degree ≤ 1), injective (in-degree ≤ 1), and acyclic — but the jump from "in/out-degree ≤ 1, finite, acyclic" to "disjoint maximal chains covering the set" is the one inference left to the reader. For the central theorem of the ASN, the one-sentence justification ("follow `succ` forward… and `succ⁻¹` backward") does the work but is not tied back to the asserted lemma.

**Required**: Either state the degree-bound argument explicitly (each vertex has ≤ 1 predecessor and ≤ 1 successor; finite + acyclic rules out cycles; hence the components are simple paths) so the partition claim is discharged from the established facts, or drop the abstract lemma sentence and rely solely on the explicit orbit construction that follows it — having both invites the reader to verify a stated lemma that the text never proves.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG / D-MIN / S2

Whether INSERT/DELETE/COPY/REARRANGE preserve contiguity, the minimum, and functionality is correctly deferred — the ASN's Open Questions already name this, and the Scope section excludes operation frame/postconditions. No revision needed; flagged only to confirm the deferral is appropriate, not a gap.

### Topic 2: Contiguity in non-text subspaces (links, subspace 2)

D-CTG/D-MIN/D-SEQ are stated for `V_1(d)` only. Contiguity properties for the link subspace fall under links/endsets, explicitly out of scope. Correct to omit here.

META: not applicable — the ASN defines state (Σ.C, Σ.M), invariants (S0–S8), and abstract well-formedness conditions stated implementation-independently; it has not drifted into implementation mechanics.

VERDICT: REVISE
