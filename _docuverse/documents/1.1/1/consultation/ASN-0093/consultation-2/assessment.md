# Channel Assignment — ASN-0093 review-2

**Date:** 2026-05-18 13:59

## Issue 1: Cross-document disjointness lemma Case B argument lacks case analysis
Reason: Pure proof-structure fix — spelling out three length-subcases using the Prefix definition from ASN-0034. Derivable from the ASN's own content.

## Issue 2: L1c/C1c chain exhibition for subsequent emission depends on an undeclared inductive property
Reason: Internal structural lemma — adding `dom(L) ∩ {ℓ' : origin(ℓ') = d} ⊆ A_L(d)` with inductive proof using K.σ/K.α/K.λ frame conditions. Derivable from the ASN's own transition definitions.

## Issue 3: Transfer of T10a.7/T10a.1/T10a.8 to non-tree-embedded chains needs explicit justification
Reason: Requires inspecting the proofs of T10a.7/T10a.1/T10a.8 in ASN-0034 to confirm they depend only on `inc(·,0)` chain structure and T4-validity. Derivable from ASN-0034's existing proofs — no new design intent or implementation evidence needed.

## Issue 4: SubAllocatorAxiom contains derivable content
Reason: Pure derivation cleanup — Disjoint follows from FirstEmission + ChainDiscipline + TA5-SigValid + SC-NEQ; freshness follows from the first-emit predicate + L0 + Cross-doc lemma. All machinery is already in the ASN.

## Issue 5: Worked example doesn't exercise cross-document case
Reason: Mechanical extension of the example with a second document — exercises the Case A position-divergence path of the Cross-document lemma. No external input needed.

## Issue 6: "Active" terminology in SubAllocatorAxiom.Exists is informal
Reason: Terminology cleanup — either define "active" against `dom(M)` or replace the term with explicit "admissible emission source" phrasing. Pure ASN-internal wording fix.
