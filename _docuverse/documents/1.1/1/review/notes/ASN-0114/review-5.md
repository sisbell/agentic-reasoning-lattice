# Review of ASN-0114

I read the note in full and checked each of F0–F8 against its stated derivation, the foundation contracts it cites, and the boundary cases the rubric demands.

## REVISE

(none)

## Verification performed

**Cross-ASN references.** All citations are to foundation ASNs (0034 T4/T12/OrdinalShift, 0043 L3/L4/L5/L6/L8/L9/L12, 0053 S0/S2, 0093 link store, 0098 coverage/LP13/LP-Fin). No non-foundation ASN is invoked except in the Scope exclusion list, where the references are correctly flagged as out-of-scope siblings. Standard 7 satisfied.

**F1/F2/F3** — Exactness witness (the recorded endset is its own span-set) is valid; F2's disconnectedness argument correctly invokes span convexity (S0) and rules out both singleton and empty `R`; F3 follows directly from F1. Sound.

**F5** — The single-step L12 fact is correctly composed to the reflexive-transitive closure via LP13 (ASN-0098), not asserted. The load-bearing analysis (coverage-permanence needs only L12; material-permanence is the stronger content-identity reading F5 does *not* formally claim) is precise and avoids overstatement.

**F6** — The home-document disclosure is correctly restricted to the `zeros ≥ 2` document-bearing slice, with explicit acknowledgment that L4/L9 admit node-level, user-level, and non-T4-valid interior tumblers carrying no document field.

**F7** — The uniqueness of `⟨⟩` as the sole empty-coverage span-set is correctly grounded in S2. The empty-vs-invalid distinction is a genuine obligation, and the note honestly records that the one implementation traced *fails* it — exactly the kind of obligation an abstract spec should expose.

**Worked instance** — Verified the arithmetic: `d = 1.0.1.0.5` has `zeros = 2`; `aₖ` has `zeros = 3`, `s_C = 1`; `(a₃, δ(2,#a₃))` denotes `[a₃, a₅)`; disconnectedness witness `a₃ < a₅ < a₇` holds under T1; F2 and F7 both discharged concretely.

**Edge cases** — empty end (F7), invalid selector in all three forms (F7), discontiguous coverage (F2), absent content/orphaned link (F8), and multi-document coverage (Open Question) are all addressed. The wp analysis (F0, valid/invalid boundary) is present and non-vacuous.

The note defines an abstract operation by domain, coverage relationship, frame, and admissible/forbidden results — stated so an alternative implementation must satisfy them. It keeps the recorded-endset / resolution boundary sharp and defers resolution, normal form, and multi-document reporting to Open Questions. No drift.

META: not applicable.

VERDICT: CONVERGED
