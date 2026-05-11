# Review of ASN-0036

I read through the ASN end-to-end, checked all proofs for boundary cases, verified the within-subspace and cross-subspace uniqueness arguments in S8, validated the OrdAddHom/OrdAddS8a/OrdShiftHom component-by-component derivations at boundary regimes (k = 2 and k = m), checked D-CTG-depth's infinite-intermediate construction, verified the worked example's k = 3 case exercises the auxiliary lemma's k ≥ 1 branch, and confirmed all cross-references are to ASN-0034.

## REVISE

(no items)

The proofs hold up:

- **S1, S4, S6, S9** are direct corollaries of S0/GlobalUniqueness with one-paragraph justifications appropriate to their content.
- **S5** exhibits explicit, verifiable cross-document and within-document witnesses; the constructions parametrize on N correctly.
- **S7** decomposes into S7a/S7b/S7c/S7d with each axiom's role made explicit in S7's proof (well-definedness, identification, uniqueness, permanence).
- **S8**'s existence argument uses singletons and is honest about what's needed; the auxiliary lemma is correctly marked as vacuous at k = 0 and load-bearing only at k ≥ 1 (where S7c kicks in). The within-subspace incompatibility lemma's two-case analysis (j < m and j = m) is exhaustive, and the cross-subspace argument correctly chains TS4, T5, T10.
- **OrdAddHom/OrdAddS8a** handle the k = 2 and k = m boundary collapses explicitly.
- **D-CTG-depth** constructs infinitely many intermediates via either T0(a) iteration or NAT-closure injection, then contradicts S8-fin — both arguments are sound.
- **D-SEQ**'s four-step proof splits m = 2 (vacuous shared-prefix) from m ≥ 3 (uses D-CTG-depth) correctly.
- **ValidInsertionPosition** splits into binary (non-empty) and ternary (empty) predicates, eliminating the previous ambiguous third argument; distinctness, depth preservation, subspace identity, and S8a consistency are all verified.

Scope-relevant deferrals (D-CTG/D-MIN to text subspace only, subspace alignment to operations layer, displacement mechanisms to operations layer, exact depth choice for empty subspace to operations) are explicitly stated with architectural justification.

## OUT_OF_SCOPE

(none — the ASN's Scope and Open Questions sections already enumerate appropriately deferred items)

VERDICT: CONVERGED
