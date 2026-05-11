# Review of ASN-0040

## REVISE

### Issue 1: TA5a restatement adds a constraint absent from the foundation

**ASN-0040, B6 sufficiency proof and B10 baptismal-transition Case 1**: "TA5a (IncrementPreservesT4, ASN-0034) states that for any t satisfying T4, inc(t, k) satisfies T4 iff `k = 0`, or `k = 1 ∧ zeros(t) ≤ 3`, or `k = 2 ∧ zeros(t) ≤ 2`."

**Problem**: The foundation TA5a's Guarantee reads "inc(t, k) satisfies T4 iff `k ∈ {0, 1}`, or `k = 2 ∧ zeros(t) ≤ 2`" — there is no `zeros(t) ≤ 3` constraint on the k = 1 case. The ASN's restatement is equivalent under the precondition (T4-validity automatically gives zeros(t) ≤ 3 via T4(i)) but presents a three-case structure that doesn't match TA5a's two-case structure. A reader checking the foundation could be misled into thinking TA5a literally writes the three cases as stated. This restatement appears in both B6's sufficiency proof and B10's Case 1.

**Required**: Restate TA5a accurately as "iff `k ∈ {0, 1}` or `k = 2 ∧ zeros(t) ≤ 2`", and then explicitly note that under T4-validity the case structure can be uniformized via the bound `zeros(t) + (k − 1) ≤ 3` (which reads as the vacuous `zeros(t) ≤ 3` for k = 1 and the active `zeros(t) ≤ 2` for k = 2). The uniformization is sound; the restatement should not silently introduce it as part of TA5a's content.

### Issue 2: B7 precondition wording conflates T4 and B6

**ASN-0040, B7 Formal Contract**: "Preconditions: (p, d) ≠ (p', d') with p, p' satisfying T4 and d, d' satisfying B6."

**Problem**: B6 is a predicate on the pair (p, d) — `p satisfies T4 ∧ d ∈ {1, 2} ∧ zeros(p) + (d − 1) ≤ 3`. The phrase "d, d' satisfying B6" therefore either subsumes the T4 requirement (making "p, p' satisfying T4" redundant) or splits B6 across two clauses (treating only the d-relative conditions as "B6"). Either reading leaves the contract ambiguous about whether B6(i) is being asserted twice or only by one clause.

**Required**: Phrase the precondition as "(p, d) and (p', d') both satisfy B6, with (p, d) ≠ (p', d')". This eliminates the ambiguity without weakening the assumptions consumed by the proof.

### Issue 3: B0's status caption conflicts with its presentation

**ASN-0040, Properties Introduced table**: B0 listed as "derivable from B0a; retained as a primitive label for proof legibility (cited by B1, B10)".

**Problem**: The inline derivation in the discussion paragraph ("B0a's partition of Op forces `op(Σ).B = Σ.B ∪ {next(Σ.B, p, d)}` ... and therefore `Σ.B ⊆ Σ'.B` for every transition") is given as motivational prose, but B0 itself is then stated without a *Proof* heading and without a *Depends* line. Every other "derived" claim in this ASN has a structured proof block; B0 is the lone exception. The "primitive for proof legibility" rationale (which is reasonable) clashes with the "derivable" status label.

**Required**: Either give B0 the same structured presentation as B5, B8, etc. (Preconditions / Proof / Postconditions / Depends, where Depends = {B0a}), or mark B0 explicitly as a labelled primitive (Status: primitive, with the B0a-derivation as commentary). The current hybrid leaves a reader uncertain whether B0 is being claimed without proof or proved without structure.

## OUT_OF_SCOPE

(None — the Scope section appropriately defers ownership, content storage, parent prerequisite enforcement, replication, and operation-specific effects to future ASNs. The forward-requirement framing of Bridge1, Bridge2, and B3 keeps cross-ASN obligations explicit without prematurely entangling those ASNs.)

VERDICT: REVISE
