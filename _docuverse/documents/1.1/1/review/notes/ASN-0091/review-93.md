# Review of ASN-0091

I read the ASN as a self-contained derivation of REARRANGE as a Vstream-only operation, checked the abstract-class definition, the REARRANGE_K realisation (clauses (i)–(v), frame discharge, reachability), every RE-* derivation, the five worked examples, and the multi-step composition section against the foundation claim statements. The mathematics is sound: the shape-package discharge (clause (i) holds because S8a/S8-depth/D-CTG★/D-MIN★ are all dom-only predicates and RA-dom fixes dom), the net-effect split with its collapse branch, the L-chain lemma, the run-cardinality witnesses (fragmentation/coalescence/equality all recompute correctly), and the bijection-non-uniqueness uniformity argument all hold. I found no correctness or missing-depth defects.

The note carries `review-mode.anti-bloat`. The residual findings below are accretion, not errors.

## REVISE

### Issue 1: Worked-example composite-boundary bullet re-derives the section it should cite
**ASN-0091, Worked Example, "Composite-boundary properties (P4★, P4a, P7a)" bullet**: "These are not per-state invariants and so fall outside RA-adm. Taking the pre-state Σ to be a composite boundary (RA-bndy), the K.μ~ realiser carries Σ to a post-state Σ' that is again a reachable composite boundary, so ASN-0047's ExtendedReachableStateInvariants delivers P4★ ∧ P4a ∧ P7a at Σ' in one citation..."
**Problem**: The first two sentences reproduce the entire argument of the dedicated "Composite-Boundary Properties" section verbatim in substance. A worked-example slot should *verify concretely*, not re-argue the general claim. Only the following sentence ("Concretely one may read off the witnesses... `Contains_C(Σ')` ... for P4★, and `(b₁,d),(a₁,d'),(a₂,d')∈Σ'.R` for P7a") belongs here. The reader must skip past the re-derivation to reach the witnesses.
**Required**: Replace the re-derivation with a one-clause back-reference to the Composite-Boundary Properties section and keep only the concrete witness read-off.

### Issue 2: Identity-case derivation restates the RA-frame conjuncts
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "The *identity case* π = id is admitted, with `Σ' = Σ` derived in two steps: first, RA-π under π = id reads ... second, RA-frame preserves every other state component verbatim — `Σ'.C = Σ.C`, `Σ'.L = Σ.L`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`, `dom(Σ'.M) = dom(Σ.M)`, and `Σ'.M(d') = Σ.M(d')` for every `d' ≠ d` — so the only component left to pin is `Σ.M(d)` itself..."
**Problem**: The "two steps" prose re-lists every RA-frame conjunct to conclude the obvious fact that `π = id` forces `Σ' = Σ`. The frame conjuncts are stated in full at RA-frame; re-enumerating them here is bookkeeping, not reasoning.
**Required**: Compress to a single sentence: under `π = id`, RA-π with RA-dom gives `Σ'.M(d) = Σ.M(d)`, and RA-frame fixes all other components, so `Σ' = Σ`.

## OUT_OF_SCOPE

### Topic 1: Whether fragments of a split same-source transclusion jointly reconstitute the original span
This is correctly flagged in the body ("Whether the two fragments *jointly reconstitute* the original source span ... is not established here") and routed to the first Open Question. New territory, not an error here.

### Topic 2: Link-subspace rearrangement semantics, observational equivalence by discoverability, and run-cardinality bounds
Appropriately deferred to the Open Questions section rather than forced into this ASN.

VERDICT: REVISE
