# Channel Assignment — ASN-0086 review-76

**Date:** 2026-05-19 18:01

## Issue 1: R0's misleading forward reference to R2
Reason: Pure structural fix — the proof body already shows L12/L12a/L12b/L-fin are preserved by K.λ's effect directly, so removing the unused R2 reference is derivable from inspecting the existing discharge text.

## Issue 2: R6b's framing conflates Definition consequence with separate claim
Reason: A presentation/restructuring choice between two options the review itself articulates (fold into Definition vs. restructure body to lead with non-fixpoint semantics). All substantive content is already present in R6b's Justification and the Worked Sketch's Step 3.

## Issue 3: R7a's substrate-conforming Definition is partially formal
Reason: The two catalogs are already enumerated in the existing Definition and per-step discharge block; the fix is reorganization into two named clauses with the `a* = [d.0.s_L.1.1]` example (already cited in the chain-discipline extension paragraph) promoted to motivate clause (b).

## Issue 4: R5's proof structure buries the existence/admissibility claim
Reason: Reordering existing Steps 1–5 and citing R5-Cor for L-invariant verification — the load-bearing admissibility argument (L4(c) + L13 + Endset well-formedness) is already in Steps 1–3, and R5-Cor already exists as the generic invariant-preservation result.

## Issue 5: Implementation Notes' informal introduction of layer-level commitment
Reason: Relocation of an already-stated commitment to a top-level Definition near Three Operations. The scope statement and downstream consumers (WP Case 2, relational layer Definition) are already named in the ASN.

## Issue 6: R0a-Cor1 framing as Corollary vs re-expression
Reason: Framing choice between Definition-with-notation-translation vs. adding substantive content. The mathematical question (whether the empty-homed-set case `J_d^Σ = -1` carries additional structure beyond ChainMembershipForOrigin) is answerable by inspecting R0a, R0a-Cor2, and the chain-discipline lemmas already in the ASN.
