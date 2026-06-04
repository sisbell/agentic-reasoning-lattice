# Review of ASN-0077

## REVISE

### Issue 1: Redundant pointwise-vs-span framing stated twice

**ASN-0077, opening paragraph and Summary (final paragraph)**: opening — "The permanence we will establish (O5) is the pointwise one; the span-level operations are built on top of it with their own, weaker stability laws." Summary — "Span-level answers are derived from this pointwise invariant rather than sharing it: an I-span's reported set grows monotonically... while a V-span's answer is arrangement-dependent and can shift to an incomparable set under reordering (O14)."

**Problem**: These two paragraphs make the same pointwise-derives-span-level claim in different words, in different sections. This is the "two paragraphs say the same thing" bloat pattern. The intro version is pure forward-reference framing that earns nothing the body does not establish; the Summary version is the load-bearing recap.

**Required**: Drop the framing sentence from the opening; let the body establish the distinction and the Summary recap it once.

### Issue 2: Defensive "m = 2 is not forced" asides

**ASN-0077, O11' derivation, Case (ii) sub-case (b)**: "No claim that `m = 2` is needed — `m` may be any value `≥ 2`." And the worked-example K.μ⁺_L verification: "(by `ValidFirstLinkPosition(d₃, v_{ℓ_a}, 2)`... `m = 2` is one admissible choice of first-link depth, not a forced value)."

**Problem**: Both asides rebut an imagined misreading (that the proof secretly assumes `m = 2`) rather than advancing the argument. They read as relocated responses to a prior finding. The proof already derives `#v_ℓ = m` from S8-depth without ever fixing `m`; the disclaimers are defensive noise repeated in two places.

**Required**: Remove both parentheticals. The depth-coincidence derivation stands on its own.

### Issue 3: O5★ applies the closure schema to a union-membership clause outside the schema's clause grammar

**ASN-0077, O5★ derivation**: "O5 establishes the single-step guarantee `P(Σ, Σ') ≡ [a ∈ dom(Σ'.C) ∪ dom(Σ'.L) ∧ origin'(a) = origin(a)]`, a conjunction of a membership-persistence clause (`a ∈ dom(·.C) ∪ dom(·.L)` carried forward)..."

**Problem**: The Closure schema (★) of ASN-0098 admits membership-persistence clauses of the per-store form `x ∈ dom(Σ.X) ⟹ x ∈ dom(Σ'.X)`. The clause `a ∈ dom(·.C) ∪ dom(·.L)` is a disjunction over two stores, not an instance of that form. The schema's applicability to a union-membership clause is asserted, not shown.

**Required**: Either decompose into the two per-store clauses `a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C)` and `a ∈ dom(Σ.L) ⟹ a ∈ dom(Σ'.L)` (whose conjunction discharges the disjunctive hypothesis), or state explicitly why the union form is an admissible schema instance.

## OUT_OF_SCOPE

### Topic 1: Whether the I-span lift's silent dropping of link addresses is the correct design when a span crosses subspace boundaries

**Why out of scope**: The ASN's definition resolves the mechanics (intersection with `dom(C)` drops link addresses); whether SHOWORIGIN should instead report link origins for cross-subspace I-spans is flagged in the note's own Open Questions and belongs to a future operation specification, not a revision here.

### Topic 2: A complementary operation reporting historical containment from `Σ.R`

**Why out of scope**: The note correctly distinguishes origin from historical containment and defers the latter; specifying that operation and its coupling invariants is new territory.

VERDICT: REVISE
