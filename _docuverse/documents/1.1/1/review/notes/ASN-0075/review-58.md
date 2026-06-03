# Review of ASN-0075

## REVISE

### Issue 1: The K.δ-precursor shorthand is explained twice, in full, in two sections
**ASN-0075, D-DISCR and "A Worked Example"**: In D-DISCR — "producing the *first* document (`zeros = 2`) requires a precursor account-creation step. We therefore write `K.δ(d) ≡ K.δ(A); K.δ(d)` as shorthand *for that first document only*, where `A = inc(n_0, 2)`..." — and again in the worked example — "As in D-DISCR, the first document cannot be minted by a single elementary K.δ from `Σ_0` — that produces at most an account... We therefore write `K.δ(d_A)` as shorthand for the precursor bundle `K.δ(A); K.δ(d_A)`...".
**Problem**: The same shorthand (and the same `zeros`-counting justification for why it is needed) is derived from scratch in two places. This is duplicated meta-prose of the kind the anti-bloat classifier targets — two paragraphs in different sections saying the same thing.
**Required**: Establish the `K.δ(d) ≡ K.δ(A); K.δ(d)` shorthand once (at first use), and have the worked example simply reuse it by name without re-deriving the account-precursor argument.

### Issue 2: "A second bundling" has no antecedent first bundling, and the surrounding discharge prose is protocol mechanics
**ASN-0075, D-DISCR**: "A second bundling concerns document creation. K.δ case (ii) with `k = 2` (descent)..." followed later by "Throughout both histories, each content-introduction composite follows a fixed *bundle pattern*: K.α allocates `a`... discharging the freshness obligation; K.μ⁺ places `a`... discharging J0; and because K.μ⁺'s frame leaves `R` unchanged... the bundled K.ρ is what records the provenance pair, discharging J1★ and J1'★."
**Problem**: (a) The text introduces "A *second* bundling" before any first bundling has been named — the content "bundle pattern" it implicitly contrasts against is introduced in the *following* paragraph, so the reader meets "second" before "first." (b) The discharge inventory (naming J0, J1★, J1'★, freshness per step) is protocol-validity rationale; the actual content of D-DISCR is only that `R` differs while `(C, L, E, M)` agree. The discharge bookkeeping needed to assert reachability can be stated in one terse sentence rather than an itemized obligation-by-obligation walk.
**Required**: Drop the "second" framing (or name the first bundling explicitly), and compress the validity justification to the minimum needed to assert the two histories are valid composite sequences.

## OUT_OF_SCOPE

### Topic 1: Multi-document generalization, restoration, and concurrency
The Open Questions about families of more than two documents, restoration operations consuming SHOWDELETIONS output, and concurrent-transition consistency models are correctly deferred. They are new territory, not gaps in this binary, observational specification.

The core results are sound: D-WIT, D-EXH (the impossible (Yes,No) row is correctly excluded via D-WIT under `a ∈ dom(C)`), the D-DISCR two-history construction (states genuinely agree on `(C,L,E,M)` and differ only on `R`), D-DISJ's three-group partition, and the worked example's `({b},{c})` computation all check out. The wp analysis is non-trivial (Q0/Q1) and consequences are derived (D-IDENT, D-ORIG, D-ORD). The findings above are prose accretion, not logic errors.

VERDICT: REVISE
