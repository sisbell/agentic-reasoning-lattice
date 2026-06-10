# Review of ASN-0126

I checked the proofs, the boundary cases, the address arithmetic in the worked illustration, and the prose against the anti-bloat patterns. The note is mature and I could not find a revision-worthy defect. Details below.

## REVISE

None. The specific things I verified and why they hold:

- **The gate-vs-landing separation is genuinely established, not asserted.** P3 (single-step) and P6 (state-level closure by induction over K.σ/K.α/K.λ_sh) each address all three conjuncts — standard-triple shape from (0), registration from (i), conformance from (ii) — and the persistence half of P6 correctly routes the three carried conjuncts to L12, P1, and P4 respectively. No conjunct is skipped.
- **The worked illustration's arithmetic is correct.** I recomputed it: `a_R = inc(ℓ₂,0) = 1.1.0.1.0.1.0.2.3`, `a = a_emit(Σ₁,d) = inc(a_R,0) = 1.1.0.1.0.1.0.2.4 = g`, `coverage(G_rng) = […2.4, …2.7)` so `a_R ∉ coverage(G_rng)` (retractor lands active) but `a = g ∈ coverage(G_rng)` (citation born nullified via the inherited wp third conjunct). The ghost-root counterexample in *Retraction as an attributed Binary* also checks: `a = 1.1.0.1.0.1.0.2` has `zeros=3, #E=1`, fails P-tgt on both disjuncts, and its unit-depth coverage is the entire link subtree — so single-tuple-scope is correctly diagnosed as an app obligation, not a gate guarantee.
- **The projection bridge is used soundly.** π carries each K.λ_sh step to a valid K.λ step (its preconditions are a superset of K.λ's, effect-identity matches the C/M/L action). B2 is correctly fenced ("yields no →_sh-successors"), which is why P5 and the R-Scope re-derivation are done directly rather than transferred. The three-move R-Scope reconstruction — bind via P5, apply R-Scope at the native empty-from transition Ψ, then frame π(Σ′) and Ψ together through the shared `a_emit` (blind to F) — is the load-bearing step and it is valid.
- **The wp refinement is non-trivial and complete.** The guard decomposition `wp(g→S,R) ≡ g ∧ wp(S,R)` is the right reading for a postcondition requiring the emit to fire; dropping (0) (forced by the arity-3 slice) and folding L3 / `K∈T_admissible` into RegisteredAdmissible are justified. The C2/C3 analysis correctly isolates C3 as the *newly live* conjunct under →_sh (it was vacuous under ASN-0086's unit-depth discipline) and supplies witnesses for both C2 (self-nullifying Binary) and C3 (pre-existing range retraction).
- **No cross-ASN violations.** Every citation resolves to ASN-0043 or ASN-0086 (foundations). The note reuses their definitions without reinventing notation.
- **Edge cases covered:** empty registry (substrate inert), `F=∅` (no →_sh image, including Nullify), `N>3` (precondition (0), deferred to OQ6), `G=∅` under Unary vs. Multi (shape-indistinguishable tuples), ghost addresses, self-emit, non-unit retraction.
- **Anti-bloat scan:** the residual roadmap sentences ("we now show it never drifts," the *Gate realizability* opener) are brief orientation, not skip-past meta-prose; the repeated `|F|=1` per shape is the self-contained formal definition; the multiple back-references to *Retraction as an attributed Binary* are backward citations into an established result, not forward deferrals to the same unbuilt location. The "Multi subsumes Unary/Binary" tension is disclosed at the point it arises, and the table's "possibly zero" plus the carefully-scoped "Unary and Binary are mutually exclusive" already signal the overlap.

## OUT_OF_SCOPE

### Topic 1: Additional G-cardinality shapes (e.g., a non-empty Multi requiring `|G| ≥ 1`)
**Why out of scope**: The catalog is a deliberate finite set of three. An app needing "at least one target" is not served by `Multi` (which admits `G=∅`), but adding such shapes is vocabulary extension for a successor note, not a defect here. It is adjacent to OQ6 without being fully captured by it (OQ6 addresses F-arity and N, not G-cardinality variants).

VERDICT: CONVERGED
