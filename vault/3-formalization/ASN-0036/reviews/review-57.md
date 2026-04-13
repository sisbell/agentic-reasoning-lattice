# Contract Review — ASN-0036 (cycle 1)

*2026-04-12 21:11*

### D-CTG

- `MISSING_PRECONDITION: S8-fin` — The derived postcondition (V-positions at depth m ≥ 3 share components 2 through m − 1) is established by a finiteness contradiction: assuming divergence at a non-last component allows unboundedly many distinct V-positions, contradicting S8-fin. The proof cites S8-fin explicitly ("contradicting S8-fin"). The contract has no preconditions section; S8-fin appears only in the postcondition prose ("Combined with S8-fin and S8-depth..."), not as a formally listed precondition.

- `MISSING_PRECONDITION: S8-depth` — The proof invokes S8-depth explicitly ("both depth m by S8-depth") to establish that v₁ and v₂ share the same tumbler depth m. This is load-bearing in two places: (1) the construction of the intermediate witness w requires knowing the common depth m; (2) the postcondition formula uses `#v₁ − 1` as the upper bound for the shared-component range, implicitly treating `#v₂ = #v₁` — which only holds because S8-depth guarantees uniform depth within a subspace. S8-depth appears only in the postcondition prose, not as a formally listed precondition.

### D-MIN

- `INACCURACY: The postcondition's "combined with" clause reads "Combined with D-CTG, S8-fin, and S8-vdepth (for m ≥ 2)", but the proof explicitly derives the general form by stating "By D-CTG combined with S8-fin and S8-depth (when m ≥ 3) or trivially (when m = 2)". S8-depth is explicitly named as a substantive contributor to establishing that all positions share components 2 through m−1 — which is a necessary intermediate step before D-MIN's axiom can pin those shared components to value 1. The contract omits S8-depth from the postcondition's "combined with" clause. Although S8-depth appears as a precondition (so it is in scope), the "combined with" clause is meant to guide readers on which facts combine with D-MIN to yield the full characterization, and omitting an explicitly cited ingredient from that clause is inaccurate. The clause should read "Combined with D-CTG, S8-fin, S8-depth, and S8-vdepth (for m ≥ 2)"`.

### S9

- `MISSING_PRECONDITION: S0 (content immutability) — the proof's sole dependency and the entire basis of the argument — is not listed as a formal precondition. It appears only in the Frame with an oblique "(by S0)" reference, which does not serve the same role as an explicit precondition declaration (compare S3's contract, which lists S1 and the per-operation obligation under "Preconditions:")`.

3 mismatches.
