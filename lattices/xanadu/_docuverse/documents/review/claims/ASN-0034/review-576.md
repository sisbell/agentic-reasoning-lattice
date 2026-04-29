# Cone Review — ASN-0034/T7 (cycle 2)

*2026-04-25 23:04*

Reading the ASN as a system. The previous T4-Axiom slot-citation issue has been corrected to "T4's Definition" in the current text; the "purely definitional" framing remains and is captured. Below are new findings.

### Defensive double-statement of strict-positivity citation in T7 opening
**Class**: OBSERVE
**Foundation**: —
**ASN**: T7 proof opening: *"By T4's Definition (Canonical written form), every non-separator component is strictly positive: `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` at every position present, with `<` on ℕ supplied by NAT-order. T0 supplies the ambient typing `tᵢ ∈ ℕ` on which T4's positivity clauses are stated, but the strict-positivity fact itself is delivered by T4's Definition (Canonical written form)."*
**Issue**: Two consecutive sentences both route strict-positivity through "T4's Definition (Canonical written form)" with the second adding nothing — it does not introduce a new step or refine the first; it merely restates the Definition citation while explaining why the typing role of T0 stops short of supplying positivity. This reads as reviser drift in response to the prior "T4-Axiom" finding: the contrast it draws (T0 vs. Definition) is not load-bearing for any subsequent step in the proof. The single use-site in sub-case 2b cites T4's Definition cleanly without this preamble, so the opening duplication is local noise rather than scaffolding for later steps.

### Redundant route to `0 < 1` in T4c injectivity
**Class**: OBSERVE
**Foundation**: —
**ASN**: T4c injectivity: *"NAT-addcompat's strict successor inequality `n < n + 1`, instantiated at `n ∈ {0, 1, 2}` — the `n = 0` instantiation licensed by `0 ∈ ℕ` from NAT-zero ... — gives `0 < 1`, `1 < 2`, and `2 < 3`"*.
**Issue**: NAT-closure already exports `0 < 1` as an axiom clause ("distinctness of the two named constants"). The `n = 0` instantiation of NAT-addcompat actually produces `0 < 0 + 1`, which then needs NAT-closure's left additive identity at `k := 1` to rewrite as `0 < 1` — a step the prose skips. Citing NAT-closure's `0 < 1` directly for the base link of the chain would be both shorter and would not need the silent left-identity rewrite. The current routing is sound but overheavy and includes an undeclared rewrite step.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 1799s*
