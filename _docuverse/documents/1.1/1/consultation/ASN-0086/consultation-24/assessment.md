# Channel Assignment — ASN-0086 review-24

**Date:** 2026-05-17 02:44

## Issue 1: Phantom foundation citations
Reason: The fix requires reading ASN-0034 to identify the actual names and labels for what the ASN calls T2, T10a, and TA5(d). This is foundation citation correction internal to the ASN system; the source ASNs already contain the authoritative labels.

## Issue 2: "Element-field depth" used as a primitive structural concept without formal definition
Reason: The reviewer's proposed definition (`zeros(t) − zeros(s)`) is derivable from T4's separator semantics in ASN-0034. The fix is purely internal/definitional.

## Issue 3: R0 Step 4's L11a verification is too terse
Reason: The required discharge uses T10a's at-most-once axiom and T10a.7 (already cited throughout R0) plus ASN-0043's L11a content. All ingredients are present in the foundation ASNs and the existing R0 proof.

## Issue 4: ASN length and density obstructs verification
Reason: Editorial restructuring (moving sections to appendices, grouping orthogonal L-invariant bullets). Pure exposition fix internal to the document.

## Issue 5: R6c is not concretely exercised in the worked sketch
Reason: Extending the worked sketch with another transition and verifying `a₁ ∉ A_K^{Σ_4}` uses R6a-chained applications and the R6c-Corollary, both already proved in the ASN. Internal/derivable.

## Issue 6: Discipline-conditionality of R0a should be flagged earlier and more visibly
Reason: Pure exposition fix — restating the discipline-conditional scope in the abstract opening and R6 consequence (d) where it is currently implicit. No external facts needed.

## Issue 7: Definition of `Emit_K` should make discipline binding visible in the signature
Reason: The two proposed options (rename or add postcondition line) are exposition choices about how to surface the already-established discipline binding. The substantive content — that `Emit_K` is bound to R0 Step 2's sibling-frontier construction — is already stated in the Definition and is implementation-evidenced by `findisatoinsertmolecule` (cited in the ASN). Internal.
