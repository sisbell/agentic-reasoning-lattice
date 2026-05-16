# Review of ASN-0084

## REVISE

(none)

## OUT_OF_SCOPE

(The ASN itself identifies these in its Open Questions section; no additional out-of-scope topics warrant noting.)

VERDICT: CONVERGED

---

The ASN is rigorous and self-contained. Each proof I checked establishes its postcondition with full case analysis rather than appeals to similarity:

- **R-NS** handles non-S invariance with three clauses (NS-π, NS-run, NS-inv), with the forward-reference issue managed explicitly.
- **R-PPERM/R-SPERM** verify each piecewise branch and establish disjointness of image sets directly via ordinal range arithmetic.
- **R-PIV/R-SWP** tile the affected range exactly (the ordinal arithmetic is explicit: half-open intervals checked, w_α + w_μ + w_β = ord(c_{n-1}) − ord(c₀)).
- **Canonical decomposition (a)–(d)** is genuinely rigorous: the helper "existence of a maximum" lemma derives max from NAT-wellorder via the B − s involution; step (b) splits k₁ = k₂ into three sub-cases handling the n = 0 boundary; step (c) constructs explicit mergeable witness pairs from the forward/backward dichotomy.
- **R-BLK** acknowledges that B' may not be maximal (the 4-cut worked example exhibits a B+H merge).
- **R-WP** is honestly labeled as sufficiency only, with two concrete necessity sketches (R-PRE(iv) and R-PRE(iii) counterexamples).

Edge cases I checked: ord(c₀) = 1 (empty left exterior), c_{n-1} > max V_S(d) (empty right exterior, traced explicitly in R-BLK Phase 1), w_α = w_β (μ-displacement zero — third worked example), single-position V_S(d) (excluded by R-PRE), and S5 sharing (uniqueness scope of π handled correctly).

The depth-2 scope restriction, the singleton-tumbler-to-ℕ identification, and the OrdinalShift identity-convention extension are each declared and audited at consumer sites (the catalogue under "OrdinalShift consumers under the identity extension" lists what does and does not extend).

Three worked examples cover 3-cut pivot, 4-cut swap with unequal widths, and 4-cut swap with equal widths — each verifies every postcondition clause, π's bijection property, R-DISP, and the full R-BLK transformation.
