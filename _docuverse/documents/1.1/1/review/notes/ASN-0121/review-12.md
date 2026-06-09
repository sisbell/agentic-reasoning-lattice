# Review of ASN-0121

I read the ASN as a specification of the `findlinks` query: its state-frame (read-only over `Σ`), its result set, and the guarantees (soundness, completeness, non-impedance, directionality, type-by-address, wildcard/empty asymmetry, currency, editing-stability, retraction-absence, cross-document reach) that an alternative implementation must meet. I checked each claim's derivation and the worked instance against the foundation contracts.

## What I verified

- **FL-DEF "forced" derivation** is clean: soundness *permits* `addressable ∧ sat`, completeness *forces* it, the two coincide, R is unique. The justification for folding addressability into soundness (otherwise `R_min` and `R_max` both qualify) is honestly identified as the one design choice, grounded in Nelson 4/9.
- **The `→`-vocabulary mismatch with ASN-0086 is handled correctly.** ASN-0086's R6a is stated only over `→ ≡ K.σ ∪ K.α ∪ K.λ`, but ASN-0121 redefines `→` as the full ASN-0047 vocabulary. The structural argument — `nullified` is a function of `Σ.L` alone (via `L_R^Σ ⊆ Σ.L`), so every non-`Σ.L`-touching op holds it constant, and R6a is invoked *only* across K.λ — closes the gap rigorously. The per-operation frame enumeration (K.α→C, K.δ→E/M, K.μ*→M, K.ρ→R) checks out against ASN-0047.
- **FL-DIR witness** is explicit and correct: `x=[…,5]`, `y=[…,9]` are equal-length non-nesting, subtrees disjoint, and the reversed request flips `{a₁}`↔`{a₂}`.
- **FL-EMP** correctly separates the unit (`∗`, drops out) from the zero (`∅`, annihilates), and extends the symmetry to the link's own empty `e₁`/`e₂` (L3 permits these).
- **FL-REACH(d)** carefully avoids the over-claim: it does *not* assert superset of the request-independent `discoverable_from` union (LP12), restricts to *satisfying* links, and proves strictness via satisfying orphans (sat is arrangement-independent, so a satisfying orphan can exist). The containment direction is trivially correct since the `discoverable_from` conjunct only narrows the RHS.
- **Worked instance (6 traces)** exercises each headline claim. I re-parsed every address: `a₁=[1,0,1,0,1,0,2,1]` → `home=[1,0,1,0,1]=d`, `a₅` → `home=d'`, both document-level (zeros=2), `d`/`d'` equal-length non-nesting, `[1] ≼ d` and `[1] ≼ d'` for the node-granularity case. Trace 6 genuinely varies residence with endpoints held byte-for-byte fixed and flips `{a₅}`↔`{a₁}`, witnessing FL-RES.

## On scope and drift

The repeated appeals to Gregory's back end and consultation Q-numbers are used to *confirm* abstract guarantees and to record divergences ("home-set ignored," "all-wildcard returns empty") as obligations on a conforming implementation — not as mechanism. The ASN defines result state and its invariants abstractly. No drift; no META.

No out-of-scope claims are asserted (creation, counting, pagination, FOLLOWLINK, etc. are absent; version-scope and federation appear only as Open Questions, not claims).

## Assessment

I attempted to break the hard claims — the `nullified`-monotonicity bridge, the orphan strictness in FL-REACH, the empty/wildcard asymmetry, the residence/endpoint orthogonality witness — and each holds. Boundary cases (empty store, all-wildcard, all-empty, empty link endsets, retracted links, orphans) are all explicitly covered. Derivations name their premises and chains; the worked example checks the principal postconditions against concrete addresses. I found no hand-wave, no missing case, and no under-derived claim.

VERDICT: CONVERGED
