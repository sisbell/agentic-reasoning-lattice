# Review of ASN-0114

I read the note on its own terms: it specifies FOLLOWLINK as a pure-read projection returning one endset by selector, bound at the level of coverage. I checked every claim's derivation, the boundary cases, and the worked instance.

## REVISE

(none)

The note meets the standards a tough read demands:

- **Every proof shows its work.** F2 is derived from F1 plus span convexity (S0) with the singleton case explicitly contradicted, not asserted. F5's derivation composes L12 along `→*` via LP13 (and offers the induction as an alternative), and carefully separates coverage-permanence (load-bearing: L12 alone) from material-permanence (needs content-identity addressing, *not* needed for the stated claim) — exactly the kind of "what is actually load-bearing" distinction that is usually hand-waved.
- **Boundary cases are all handled.** Empty endset (F7, with `⟨⟩` forced unique via S2), invalid selector (`⊥`), disconnected coverage (F2), n-set arity beyond 3 (F0 selector domain `1 ≤ i ≤ |Σ.L(a)|`), and content-absent/orphaned links (F8). The empty-vs-invalid distinction is sharpened against a real implementation that *fails* it (Q17) — the right use of evidence.
- **The worked instance is concrete and correct.** I verified `a₃ ⊕ δ(2,#a₃) = a₅` (OrdinalShift), the `F`-restricted coverage `{a₃,a₄,a₇,a₈}` (LP-Fin Corollary), the disconnection witness `a₃ < a₅ < a₇` with `a₅ ∉ coverage(e₁)`, and the interior point `a₃.1` showing the interval is a region of all of `T`. F2 and F7 are discharged against it.
- **wp analysis is non-trivial and present** (F0 selector-validity, F7 valid/invalid boundary).
- **Disclosure is precisely scoped.** F6's home-document disclosure is correctly tightened to the T4-valid, document-bearing (`zeros ≥ 2`) slice, explicitly excluding node/user-level and non-T4-valid interior tumblers — coverage being a union of half-open intervals whose interiors need not be valid.
- **Cross-references are foundation-only** (ASN-0034, 0043, 0053, 0093, 0098). No non-foundation ASN is cited; no foundation notation is reinvented.

## OUT_OF_SCOPE

### Topic 1: Resolution of the recorded endset against a document's arrangement
The note correctly fences this off (the "recorded end versus its resolution" section and Open Question 2). Reporting fewer positions after projecting through `Σ.M(d)` and filtering absent addresses is a property of resolution, not of FOLLOWLINK, and belongs with the V-position-resolution operation, not here.

### Topic 2: Normal form / span decomposition of the returned span-set
F3 deliberately leaves representation free and the note flags normal form as an Open Question. Whether the result must be normalized (ASN-0053 S8/S9) is genuinely new territory, not a defect in this note.

VERDICT: CONVERGED
