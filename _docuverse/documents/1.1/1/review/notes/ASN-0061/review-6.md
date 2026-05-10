# Review of ASN-0061

## REVISE

*No issues identified.*

Every proof in this ASN is complete. Every edge case is handled. Every invariant conjunct is addressed with explicit justification. I subjected the ASN to an exhaustive check — each of the items below was verified:

**Proofs verified:**
- D-SEP (gap closure) correctly applies TA4 at depth-1 ordinals with vacuous zero-prefix condition.
- D-BJ (shift bijectivity) correctly applies TA3-strict; all preconditions (equal depth, both ≥ w) hold.
- D-DP (contiguity preservation) covers all four cases (L=∅/R=∅ combinations). Case 3's adjacency argument — max(L) has ordinal ord(p)−1, min(Q₃) has ordinal ord(p) — is valid by D-CTG on the pre-state and D-SEP.
- D-BLK's six-case partition of blocks against the cut points is exhaustive (verified by case analysis on v vs p and v\_end vs r). B1/B2/B3 each verified: B2 between B\_left and shifted B\_right follows from ordinals < ord(p) vs ≥ ord(p); B3 for shifted blocks uses σ(v)+j = σ(v+j), which the ASN proves by commutativity of natural-number arithmetic at depth 1.
- The composite transition decomposition correctly identifies when K.μ⁺ applies (R≠∅) and when it reduces to K.μ⁻ alone (R=∅), with the strict-superset precondition of K.μ⁺ justified by |Q₃|≥1 and Q₃ ∩ (Q₁∪L) = ∅.
- All three coupling constraints (J0, J1, J1') verified vacuous for both R=∅ and R≠∅ cases, with the critical observation ran(M'(d)) ⊆ ran(M(d)) justified explicitly.

**Invariants verified:** P0, P1, P2, P3, P4, P4a, P5, P6, P7, P7a, P8, S0, S2, S3, S8a, S8-depth, S8-fin — all with explicit justification referencing D-CF, D-XD, D-SHIFT, and the domain-completeness argument.

**Boundary cases covered:** deletion at the first position (Case 2), deletion at the last position (Case 4), deletion of the entire subspace (Case 1), single-position deletion (w\_ord=[1]), block straddling both cut points (case f, verified in the worked example).

**Worked example verified:** The five-position document with DELETE at p=[1,2], w=[0,2] correctly produces B'={([1,1],b,1),([1,2],b+3,2)}, with contiguity [1,1]..[1,3] and width 5−2=3.

**Design decisions well-justified:** D-CTG as a "DESIGN" constraint rather than an INV is a deliberate, coherent choice — bare K.μ⁻ can violate it, so it cannot be a reachable-state invariant, but the ASN proves DELETE preserves it. The depth-2 restriction (D-PRE(iv)) is honestly stated with the key dependency identified: TA4's zero-prefix condition is vacuous at k=1 but non-trivial at deeper depths.

## OUT_OF_SCOPE

### Topic 1: Generalization to ordinal depths > 1
**Why out of scope**: The depth-2 restriction is this ASN's stated scope boundary. Extending D-SEP's round-trip, D-DP's contiguity preservation, and D-BLK's σ(v)+j = σ(v+j) to deeper ordinals requires new algebraic machinery (TA4's zero-prefix condition is no longer vacuous; D-CTG becomes unsatisfiable when intermediate positions span different penultimate components). The ASN correctly flags this as an open question.

### Topic 2: Cross-operation D-CTG preservation
**Why out of scope**: Whether INSERT, COPY, and REARRANGE preserve D-CTG is each operation's verification obligation. This ASN establishes the invariant and proves DELETE's half of the contract.

### Topic 3: Link endset behavior after deletion
**Why out of scope**: Links attach to I-addresses, which persist through DELETE (P0/S0). The interaction between orphaned I-addresses and link discoverability is link-layer semantics.

### Topic 4: Version reconstruction from post-deletion state
**Why out of scope**: Recovery of prior arrangements from system history is version-management territory, not a property of the DELETE operation itself.

### Topic 5: Exact containment queries vs superset reporting
**Why out of scope**: D-PSTALE establishes that provenance is a superset of current containment after deletion. Whether the query layer must support exact filtering is a query-semantics decision.

VERDICT: CONVERGED
