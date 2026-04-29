# Formalize — ASN-0036 / D-SEQ

*2026-04-13 12:34*

- `MISSING_PRECONDITION: D-CTG-depth (SharedPrefixReduction) — Step 1 Case m ≥ 3 explicitly invokes "By D-CTG-depth (SharedPrefixReduction), all positions in V_S(d) share components 2 through m − 1." The contract lists D-CTG and D-MIN as dependencies but omits D-CTG-depth, which is a distinct lemma required for the shared-prefix step at depth ≥ 3.`

- `MISSING_PRECONDITION: T1(i) (TumblerOrdering, ASN-0034) — Step 3 invokes "By T1(i) (TumblerOrdering, ASN-0034), v₁ < v₂" and "v₁ < w < v₂" to establish the ordering relations needed for the D-CTG contiguity argument. This dependency is absent from the contract entirely.`
