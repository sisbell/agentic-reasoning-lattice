# Review of ASN-0075

I've worked through the proofs of D-EXH, D-DISCR, D-ACT, and the worked example in detail, and verified the major chains step-by-step.

## REVISE

(none)

## OUT_OF_SCOPE

(none — the eight open questions correctly identify future territory without falling into it within this ASN)

## Notes from the review (not REVISE items)

For my own bookkeeping, the spots I scrutinized hardest and accepted:

**D-EXH "impossible row" chain.** The L14 → S3★-aux → S3★-contrapositive → P4★ chain correctly excludes the `(a ∈ ran(M(d)), (a,d) ∉ R)` cell. The composite-boundary scoping of the lemma is correctly stated and necessary (P4★ is a Class (b) invariant in ASN-0047).

**D-DISCR witnesses.** Both histories are valid composites: K.α/K.μ⁺/K.ρ bundling discharges J0 and J1★ at the boundary; the K.δ shorthand correctly accounts for required precursors; the first-emission rule of K.α gives the same `a = [d.0.s_C.1]` in both histories, making C-values agree once both invocations pass the same `v_a`. Component-by-component (C, L, E, M) equality is established; R differs by `(a, d)`. Argument is sharp.

**D-ACT decomposition uniqueness.** The transitive-closure-of-I-adjacency equivalence relation, the no-intermediate-content lemma's four-case split (with cases 2–3 correctly vacuous via universal `#E = 2` for K.α emissions, and case 4's three prefix-relation sub-cases each producing T1 case (i) divergence at a separator position), and the bijection between equivalence classes and witness runs all check out. The argument that consecutive elements `c_i, c_{i+1}` of an equivalence class are shift-adjacent (chain element `a_1` must equal `c_{i+1}` by no-intermediate-content within the class) is sound, though implicit; the structure carries.

**Worked example.** The classification table, the K.μ~/K.μ⁻ retention semantics (n'_{s_C} = 2 retains positions [1,1] and [1,2]), and the resulting output ({b}, {c}) all check against ASN-0047's K.μ⁻ precondition and D-SEQ★ enumeration.

**D-ORD injectivity.** The `vpos_B` minimum is well-defined under S8-fin + T1 well-ordering; injectivity from S2's functionality is correct.

VERDICT: CONVERGED
