# Review of ASN-0075

## REVISE

### Issue 1: K.δ notation ambiguity in histories and worked example

**ASN-0075, "Why the Provenance Relation Is Load-Bearing" and "A Worked Example"**: Histories begin with `Σ_0 →* K.δ(d)` and `Σ_0 →* K.δ(d_A)` treating each as a single composite producing a document.

**Problem**: K.δ case (ii) k = 2 (descent) requires `t ∈ E ∧ zeros(t) ≤ 1`. From Σ_0 with only `n_0 ∈ E` (zeros = 0), a single elementary K.δ produces at most an account (zeros = 1). Creating a document (zeros = 2) requires a precursor account-creation step — e.g., `inc(n_0, 2) = [1, 0, 1]` for an account, then `inc(account, 2) = [1, 0, 1, 0, 1]` for the document. The ASN's notational convention says "each `→*` arrow denotes one valid composite" but doesn't address whether a labeled K.δ composite includes the precursor entity creations.

**Required**: Either clarify explicitly that "K.δ(d_A)" denotes a composite containing necessary precursor K.δ steps (account, then document), or expand the histories to show the precursor account creation. As stated, the proofs assume reachability of (d_A, d_B) without verifying the predecessor structure satisfies K.δ's preconditions.

### Issue 2: D-EXH proof relies on P4★ without explicit reachability assumption

**ASN-0075, "Lemma D-EXH (Three-State Exhaustion)"**: The proof concludes "the pair `(a, d)` belongs to `Contains_C(Σ)` by definition, and `Contains_C(Σ) ⊆ R` by P4★".

**Problem**: P4★ is a Class (b) composite-boundary property in ASN-0047, discharged at composite boundaries by J1★/J1'★. It is not asserted as a per-state invariant — within a composite's intermediate states, P4★ may not hold. The lemma states three-state exhaustion universally for any state Σ matching the precondition, but the proof step is only valid when Σ is a reachable state (composite boundary). The fourth row "(a ∈ ran(M(d)), (a, d) ∉ R)" could in principle arise mid-composite without P4★.

**Required**: State explicitly in D-EXH's precondition that Σ is reachable from Σ_0 (equivalently, at a composite boundary), or note in the proof that SHOWDELETIONS is only meaningful at reachable states. Without this, the lemma's universal quantification overreaches what the proof establishes.

### Issue 3: Q0 vacuity explanation is logically incomplete

**ASN-0075, *Vacuity of both report halves***: "Documents with completely disjoint histories — no shared R-projection on the content subspace — satisfy Q0 vacuously: no `a` has `(a, d_A) ∈ R`, so no `a` is DELETED from `d_A`."

**Problem**: "Disjoint R-projections" (d_A's and d_B's R-projections share no elements) does not imply "d_A's R-projection is empty". The supporting argument describes a specific subcase (one or both projections empty), not the general disjoint-histories case where both projections are nonempty but disjoint. The "so" connects premises that don't chain in the general case: from "no shared projection" the proof should argue: for any `a` with `(a, d_A) ∈ R`, disjointness gives `(a, d_B) ∉ R`; for `DELETED(a, d_A) ∧ CURRENT(a, d_B)` to hold, CURRENT requires `a ∈ ran(M(d_B))`, which by P4★ forces `(a, d_B) ∈ R` — contradiction.

**Required**: Either replace the narrow argument with the general one (chaining through P4★), or restrict the disjoint-histories claim to the empty-projection subcase explicitly. As written, the prose elides the load-bearing step.

### Issue 4: D-DISCR conclusion understates the witness's strength

**ASN-0075, "Lemma D-DISCR" conclusion**: "any system supporting SHOWDELETIONS must maintain state components `C*` (in addition to `C` and `M`)".

**Problem**: The exhibited witnesses Σ_1 and Σ_2 agree on (C, L, E, M) — the comparison table shows agreement on dom(C), C(a), E_doc, M(d), and M(d'), and the prose notes both have L = ∅. The lemma actually establishes that no function of (C, L, E, M) alone can discriminate. The conclusion's "in addition to C and M" is a conservative restatement that doesn't reflect what the witnesses prove: L and E are also insufficient.

**Required**: Either note in the conclusion paragraph that the witnesses establish a sharper result (insufficiency extends to (C, L, E, M)), or rephrase the lemma's statement to match the witness's strength. The motivational force of D-DISCR for R specifically is stronger when the full insufficiency is acknowledged.

## OUT_OF_SCOPE

### Topic 1: Restoration operation consuming SHOWDELETIONS output

**Why out of scope**: The "Composability with Restoration" section explicitly defers this to future work, noting only that the output's form makes restoration possible without specifying the operation. Listed in Open Questions.

### Topic 2: Concurrent state transitions and consistency model

**Why out of scope**: ASN-0075 operates within ASN-0047's sequential transition model. The Open Question "if the system supports concurrent state transitions, what consistency model must SHOWDELETIONS observe" appropriately defers this.

### Topic 3: n-ary SHOWDELETIONS over families of more than two documents

**Why out of scope**: Listed as an Open Question. The current operation is binary by design; n-ary generalizations and their witness-structure replacements need separate specification.

### Topic 4: Cross-document link-subspace deletion comparison

**Why out of scope**: D-SUBSP argues this is structurally not well-formed given CL-OWN (links are owned by their home document). A separate per-document link-deletion analysis is mentioned but not specified — appropriately deferred to a future ASN.

### Topic 5: Three-document witness scenarios

**Why out of scope**: The Open Question "how should SHOWDELETIONS report content that was deleted from both compared documents but remains current in a third document" is explicitly deferred.

### Topic 6: Distinguishing past arrangement witnesses from sibling witnesses

**Why out of scope**: The Open Question on "deleted with a witness in a prior arrangement of the same document" vs "deleted with a witness in a sibling document" is appropriately deferred.

VERDICT: REVISE
