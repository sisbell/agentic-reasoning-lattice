# Review of ASN-0084

## REVISE

### Issue 1: R-CS3 unsatisfiability argument does not cover cut sequences whose lower cuts are also in a higher subspace

**ASN-0084, "Redundancy of CS3" / R-CS3**: "every cut sequence that violates CS3 ... renders the precondition unsatisfiable" and "no CS3-violating cut sequence satisfies the rest of R-PRE at all."

**Problem**: The proof establishes only that a CS3 violation forces the *maximal* cut `c_{n−1}` into a higher subspace ("Every CS3-violating cut sits at c_{n−1}"). The unsatisfiability conclusion then relies on R-PRE(iv) quantifying over "infinitely many subspace-1 positions" in `[c₀, c_{n−1})`. But that only happens when `c₀` itself lies in subspace 1. Consider a cut sequence with **every** cut in subspace 2 (admissible: V_S(d) ≠ ∅ in subspace 1, CS1, CS2, CS4 all hold; only CS3 is violated). Then `c₀ ∈` subspace 2, and since every subspace-1 position is `< c₀` under T1, the antecedent `subspace(v) = 1 ∧ #v = 2 ∧ c₀ ≤ v < c_{n−1}` is false for all `v`. R-PRE(iv) is therefore **vacuously true**, not unsatisfiable, and clauses (i)–(iii minus CS3) all hold. The configuration satisfies the rest of R-PRE, directly contradicting the lemma's universal claim. (The resulting REARRANGE_K degenerates to the identity — benign — but the lemma asserts *unsatisfiability*, which is false.)

The proof never discharges the premise it actually needs: `c₀ ∈` subspace 1. The exhaustiveness step pins only the top cut, not the bottom one.

**Required**: Either restrict the redundancy claim to cut sequences with `c₀ ∈` subspace 1 (and handle the all-higher-subspace case separately — e.g., show it produces a vacuous/identity operation that breaks no postcondition, which is a *different* argument than unsatisfiability), or strengthen the exhaustiveness analysis to prove `c₀ ∈` subspace 1 follows from CS2 + R-PRE(iv) + (ii). As written, the lemma statement ("renders the precondition unsatisfiable," "no CS3-violating cut sequence satisfies the rest of R-PRE at all") is false for the all-higher-subspace case.

### Issue 2: Triplicated redundancy/retention meta-prose in the CS3 section

**ASN-0084, "Redundancy of CS3" section intro + R-CS3 statement + R-CS3 "Redundancy, not necessity" paragraph**: the section opening ("This section records that the same-subspace clause CS3 is *redundant* for soundness... an unsatisfiable precondition is benign... The result is therefore a redundancy observation, not a necessity claim"), the lemma's own restatement, and the closing "Redundancy, not necessity" paragraph ("This argument exhibits no necessity witness... CS3 therefore removes no configuration... We retain it as an explicit well-formedness clause for readability... its presence is not load-bearing") all assert the same three points: redundant-not-necessary, partiality-makes-it-benign, retained-for-readability.

**Problem**: Per the note's `review-mode.anti-bloat` classifier, this is duplicated justificatory meta-prose — the same claim stated three times in different words, plus document-rationale prose ("retained for readability," "not load-bearing") that justifies keeping a clause rather than advancing the argument. A precise reader must skip past two restatements to reach the actual proof.

**Required**: State the redundancy claim and the benign-because-partial observation once, in the lemma. Delete the section-intro restatement and the "Redundancy, not necessity" / "retained for readability" rationale paragraph.

### Issue 3: R-NS defers its run-partition consequence forward to R-BLK in two places

**ASN-0084, R-NS prose + Properties table (R-NS row)**: "its consequence for the run partition is discharged in place within R-BLK, where the partition B' and its phases are defined" (R-NS), echoed by "The verbatim carry of non-S runs into B' is discharged in place within R-BLK as (NS-run)" (table).

**Problem**: Two separate locations defer the same content to the same downstream location (R-BLK), a forward-reference-accretion pattern. The deferral note adds no reasoning at either site.

**Required**: Keep the (NS-π) statement in R-NS; drop the "discharged in R-BLK" deferral sentence from both R-NS and the properties table — R-BLK's `(NS-run)` already cites R-NS where it is used.

## OUT_OF_SCOPE

### Topic 1: Generalization beyond depth-2 / m_1 = 2 text subspace
**Why out of scope**: The ASN deliberately scopes to `m_1 = 2`. Whether REARRANGE_K and all lemmas lift to `m_1 > 2` (where the singleton-tumbler identification and width arithmetic must be re-derived over deeper ordinals) is the subject of the note's own open question and belongs to a future ASN, not a defect here.

### Topic 2: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: Raised in Open Questions; characterizing the permutation class of cut-point rearrangements and closure under composition is new territory, not an error in this ASN's 3-/4-cut treatment.

VERDICT: REVISE
