# Review of ASN-0121

I traced every named claim and could not find a rigor gap. Summary of what I verified:

- **FL-DEF**: The soundness/completeness "no slack" derivation genuinely *forces* the result set; the addressability conjunct is shown load-bearing via the `R_min`/`R_max` ambiguity that retraction closes. Frame (`reads Σ.L`, writes nothing) is consistent throughout.
- **FL-DEC**: Decidability reduces correctly to ASN-0086 CoverageEqualityDecidable (intersection-nonemptiness form), and the `nullified`/`addressable` filter is shown computable from finite `L_R^Σ`. The `findlinks ⊆ dom(Σ.L)` finiteness rests on L-fin (ASN-0093).
- **`nullified` monotonicity**: The structural argument ("`nullified` is a function of `Σ.L` alone, K.λ is the only `Σ.L`-changing operation, R6a covers it") is airtight and correctly avoids a fragile per-operation enumeration. The vocabulary enumeration matches ASN-0047 exactly.
- **FL-WP** (the contested claim from review-26): all three cases check out. The (a)/(c) partition by retraction-relation membership `L_R^{Σ'}` (arity-3 ∧ slot-3 coverage equality) — not coverage alone — is correct and exhaustive over the fresh-link space. The ghost-pre-coverage conjunct in (a) and the self-retraction conjunct in (c) are each derived by splitting the existential over the singleton `L_R` extension, and Trace 7 exhibits both as non-vacuous. Case (b)'s `dom(Σ.L)`-slice equation is now correct, and the parenthetical correctly explains why the full-index simplification fails. The `enabled(K.λ)` scope convention mirrors ASN-0086 wp Case 2.
- **Traces 1–7**: I recomputed the tumbler arithmetic. Disjointness of the `x`/`y`/`p`/`τ`/`σ` subtrees, the `d`/`d'` non-nesting residence flip (Trace 6), the wide-element-rooted `athome` non-vacuity example (`p⊕ℓ = [1,0,1,0,2,1,1,1]` containing document `[1,0,1,0,2]`), and the Trace-7 ghost/self-retraction witnesses all hold.
- **FL-REACH(d)**: The ASN correctly *declines* the tempting "superset of the discoverable union" overclaim, restricting containment to *satisfying* links and proving strictness via satisfying orphans — exactly right given `discoverable_from` is request-independent.
- **FL-DIR/FL-EMP/FL-TYP/FL-WILD**: the unit-vs-zero distinction (`∗` drops, `∅` annihilates), the link-side empty-endset symmetry, and address-only type matching are each defined and witnessed.

No improper cross-ASN references: every cited ASN (0034, 0036, 0043, 0047, 0053, 0086, 0093, 0098) is a foundation ASN; non-foundation references (0110/0111/0114/0120 etc.) appear only in the scope exclusion list. No reinvented foundation notation — request components are cast as `Endset` precisely to reuse `coverage`.

The deferred topics (version/time-qualified inquiry, V-spec↔I-address correspondence, federation reach) are correctly held as Open Questions rather than asserted, and the two implementation divergences (home-set ignored; all-wildcard returning ∅) are flagged as obligations on an alternative implementation, not specification claims.

The ASN defines query state-reads, the operation, and its guarantees abstractly enough that an alternative back end must satisfy them. No drift; no META.

VERDICT: CONVERGED
