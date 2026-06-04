# Review of ASN-0087

I checked the composite decomposition, the precondition reductions, the worked example arithmetic, the weakest-precondition cases, the side-effect characterization, and full invariant coverage. I found no technical defects, no skipped boundary cases, and no egregious meta-prose.

**Verification performed:**

- *Worked example arithmetic.* `d = [1,0,1,0,1]` (len 5, zeros 2); `a₁ = [1,0,1,0,1,0,1,1]`, `a₂ = […,1,2]`, `ℓ = [1,0,1,0,1,0,2,1]` (all len 8). Prefix tests check out: `a₁ ⋠ a₂` (disagree at pos 8), `a₁ ⋠ ℓ` (disagree at pos 7). Discoverability intersections correct. The `τ ⋠ x` constraint over `{a₁,a₂,a₃,ℓ}` is exactly what's needed to keep `e₃` non-contributing.

- *`ℓ ∉ ran(M(d))` derivation.* The S3★-aux + S3★ + K.λ-freshness chain is complete in both subspace cases.

- *Hardest invariant (D-CTG★).* The full-slice contiguity proof at arbitrary depth `m ≥ 2` is genuinely rigorous — the "least interior position `j` with `z_j > 1`" T1-case-(i) argument correctly forces interior components to 1, and the positive-component (ℕ⁺) slice domain rules out `z_j = 0`. Not hand-waved.

- *Invariant completeness.* Every conjunct of ASN-0047's `ExtendedReachableStateInvariants` is addressed (proved or frame-inherited), the composite-boundary trio P4★/P4a/P7a is discharged with the J0/J1★/J1'★ coupling shown vacuous, and the transition invariants reduce correctly to P3 = P0∧P1∧P2∧L12. S2's two-part exclusion (within-subspace via D-SEQ★, cross-subspace via SC-NEQ) is the right shape.

- *Boundary cases.* Empty link subspace (re-pin at m=2), non-empty extension, empty endset `eᵢ=∅` for `i≠3`, empty home-document arrangement (reflexive-only route), and the reflexive variant (`e₁'` covering `ℓ`, correctly noted as non-standardly-authored) are all handled.

I specifically examined the patterns the anti-bloat classifier targets — labeled "Scope/Why the axiom is needed" sub-paragraphs, document-ordering justifications, downstream-consumer inventories in definitions, and cross-section deferral chains. The note is clean of these; the remaining narrative framings ("We are looking for…") are corpus house-style, and the lone Atomicity→WP back-reference advances reasoning (it justifies not re-deriving the delta) rather than padding. The D-CTG★/D-SEQ★ treatment of generic `m_L(d)` is defensive completeness against the invariant *as stated*, not dead generality.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets (Open Question 1)
**Why out of scope**: Constraints on spans referencing never-allocated addresses are new territory; the note correctly handles the *allocated-substrate* discipline (StandardAuthoring) and defers the rest.

### Topic 2: Protocol-layer atomicity / Σ_mid visibility (Open Questions 3–4)
**Why out of scope**: The note correctly locates composite-level atomicity above the substrate; the substrate guarantees (component atomicity, intermediate-state invariant inheritance) are fully discharged here.

VERDICT: CONVERGED
