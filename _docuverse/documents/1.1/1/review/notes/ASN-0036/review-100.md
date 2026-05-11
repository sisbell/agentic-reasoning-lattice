# Review of ASN-0036

## REVISE

(no items)

## OUT_OF_SCOPE

(no items)

The ASN is unusually rigorous for its scope. I worked through the central proofs carefully:

- **S8's existence + uniqueness argument**: The within-subspace incompatibility lemma (Cases j < m and j = m) correctly uses T1(i), NAT-discrete, and trichotomy disjointness. The boundary `m = 2` is explicitly handled (forces j = m). Cross-subspace uniqueness via T5 + T10 is sound — the application of T10 with a = b = w to derive contradiction is correct.
- **Auxiliary lemma (subspace + field-structure preservation)**: The three conclusions are correctly ordered ((ii) → (iii) → (i)). The chain `1 + 1 ≤ aⱼ_{#aⱼ} + 1 ≤ aⱼ_{#aⱼ} + k` via NAT-addcompat's left and right order compatibility, closed by NAT-order's ≤-transitivity, is explicit. The δⱼ ≥ 2 supplied by S7c correctly licenses position #aⱼ − δⱼ + 1 < #aⱼ.
- **OrdAddHom**: The three-region component analysis, including boundary regimes at k = 2 and k = m (empty ranges), is verified component-by-component.
- **OrdAddS8a**: Both the displacement-tail characterization and the ord-membership equivalence are established directly, not by appeal to similarity.
- **D-CTG-depth**: The infinitely-many-intermediates construction via T0(a) correctly contradicts S8-fin. S8a is verified on the constructed witness.
- **D-SEQ**: All four steps (shared prefix, minimum k, k-contiguity, finiteness) are explicit. Both m = 2 and m ≥ 3 cases are dispatched.
- **Worked example**: Σ₁ exhibits a non-singleton (length 5) correspondence run at k = 3, verifying the auxiliary lemma's k ≥ 1 cases with concrete tumblers `[1,4]` and `[1,0,1,0,1,0,1,4]`.

Edge cases (empty V_1(d), depth m = 2 vs m ≥ 3, k = 0 in shift, action-point boundary regimes, single-state vacuous transitions) are all addressed. The Frame on S5 honestly delimits what the construction does and does not establish. The S8 auxiliary lemma is correctly noted as vacuous on the singleton existence witness, load-bearing only for nⱼ ≥ 2.

VERDICT: CONVERGED
