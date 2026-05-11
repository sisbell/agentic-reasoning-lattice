# Review of ASN-0036

I read through the ASN carefully — the strand model with its state components (Σ.C, Σ.M(d)), the invariant chain (S0–S9), the V-position decomposition machinery (ord, vpos, w_ord, OrdAddHom, OrdAddS8a, OrdShiftHom), and the contiguity properties (D-CTG, D-MIN, D-CTG-depth, D-SEQ), culminating in the ValidInsertionPosition predicates and the worked example.

The proof discipline is consistently tight:

- **S5's existence proof** exhibits two concrete state constructions (cross-document and within-document), verifies S0–S3 explicitly on each, and honestly flags in the Frame that the witnesses happen to satisfy S8a/D-SEQ — an "unforced strengthening" rather than a hidden assumption.
- **S7's identification argument** carefully distinguishes S7b (`zeros(a) = 3` strict) from T10a.4 (T4-validity envelope), explaining why both are needed for T4b's projections to apply.
- **S8's existence proof** uses singletons (where k = 0 is the only case), and the auxiliary subspace-and-field-structure-preservation lemma is correctly scoped to k ≥ 1 — vacuous on the exhibited witness, load-bearing for coarser decompositions. The within-subspace incompatibility lemma's two-case analysis (j < m, j = m) closes both branches via T1(i) plus NAT-discrete/NAT-order. The cross-subspace uniqueness uses T5/T10 via the non-nesting prefix argument.
- **D-CTG-depth's infinite-intermediate construction** verifies that the constructed w satisfies S8a (componentwise positivity, depth m, subspace 1) before invoking D-CTG, and uses T0(a) iteratively (with an alternative NAT-closure/NAT-cancel/NAT-addcompat injection) to generate the unbounded family that contradicts S8-fin.
- **OrdAddHom** handles boundary regimes (k = 2 collapses prefix-copy region, k = m collapses tail-copy region) explicitly. **OrdAddS8a** correctly characterizes the conditional positivity condition. **OrdShiftHom** falls out unconditionally because δ(n, m) has empty tail.
- **The worked example** uses a non-singleton 5-run for d₁ to exercise the auxiliary lemma at k = 3, verifying both sides component-by-component and pinning down zeros = 3 and δ = 2 preservation explicitly.

Cross-ASN references are confined to ASN-0034 (foundation, allowed). Boundary cases (empty arrangement, depth 2 vs depth ≥ 3, k = 0 vs k ≥ 1, empty vs non-empty subspace) are all addressed. The deliberate scope choices (subspace alignment deferred to operations, contiguity bound to text subspace S = 1) are flagged explicitly with rationale from Nelson and Gregory.

No REVISE items found.

## REVISE

(none)

## OUT_OF_SCOPE

(none)

VERDICT: CONVERGED
