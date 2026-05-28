# Review of ASN-0069

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Concurrent fork semantics
**Why out of scope**: ASN's first Open Question. SequentialTransitionAxiom forecloses true concurrency at the foundation level; richer concurrency semantics belong in a separate ASN.

### Topic 2: Snapshot vs. living fork semantics
**Why out of scope**: ASN's third Open Question. V11's "transitive identity along unedited fork chains" implicitly stakes out the snapshot model; a living-fork alternative would require additional structure.

### Topic 3: Discoverability of forks from source
**Why out of scope**: ASN's second Open Question. R supports the query "which documents contain a?" but discoverability of descendants from `d_src`'s vantage is a separate concern beyond the FORK operation itself.

## Notes on rigor (no REVISE)

The verification was thorough enough that the following non-trivial items were addressed:

- **V2 nested induction explicit**: The length-equation induction inside V2's prefix-relation induction is correctly distinguished as a nested induction over the same enumeration with a distinct inner goal.
- **V4b as a separate design commitment**: Domain equality is correctly identified as not derivable from V4 alone or J4 alone; consumed by V6a(⊇) and V12(d) in exactly the places where V4 is insufficient.
- **V11 premise scope**: Both remarks (non-immediate-source modifications discharged by V5a Corollary 2; `d_src` modifications after step 1 discharged by conclusion anchoring at Σ) correctly distinguish operational discharge from anchoring.
- **K.ρ phase verification**: The R'-equality claim is verified by step-by-step composition over n elementary K.ρ invocations, not asserted as inclusion.
- **K.δ freshness discharge**: Three independent steps cover (i) at-most-once-per-(t,k'), (ii) other (t,k') variants, (iii) cross-allocator T10a.6 — the discharge addresses every K.δ event in the system's history that could have placed `inc(d_src, 1)` or `inc(d_prev, 0)` into E.
- **V8b non-monotonicity**: Each elementary transition (K.α, K.λ, K.ρ, K.δ, K.μ⁺_L on any document, K.μ⁻/K.μ⁺/K.μ~ on third documents) is explicitly examined; only K.μ⁻/K.μ⁺/K.μ~ on `d_src` or `d_new` can shift Π_g.
- **V7 extension flagged**: K.δ-alone composite is correctly identified as not a J4 composite; J0/J1★/J1'★ vacuous discharge at (Σ, Σ^{(1)}) is verified.
- **Notation convention**: Distinction between sibling superscript-after (`d_new²`) and chain superscript-before (`d²_new`) is documented and consistently used.
- **ASN-0040 unused**: Correctly identified as removable from depends set.

VERDICT: CONVERGED
