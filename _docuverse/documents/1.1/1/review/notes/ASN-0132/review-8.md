# Review of ASN-0132

I checked the load-bearing parts independently rather than trusting the prose: the well-definedness reduction to L-fin, the four-case unit argument, the CN-MONO weakest-precondition derivation, the transition-space coverage (CN-STAB vs. CN-MONO vs. CN-RETRACT against F-PRES), and the full arithmetic of the worked example. They hold.

A few spot-checks worth recording, since they are where this kind of ASN usually fails:

- **CN-MONO wp.** The derivation correctly isolates the fresh link's contribution, and the self-correction disowning E-INV (ASN-0127) is right — E-INV is about the slot-agnostic `matches`, not `sat`, and is silent on addressability, so it would have delivered neither half. The retained second conjunct `¬(E (b,F',G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))` is genuinely non-free ("ordinary" forbids a *new* retraction but not a *standing* one already naming the fresh address), and the unit-depth collapse via R0a (prefix antichain) → `t = ℓ` → freshness contradiction is sound. This matches FL-WP(a), not a weakening of it.
- **CN-UNIT(d), version-refraction.** The reliance on J4's "no other elementary steps" is correct: the fork's V-to-I step ranges over `V_{s_C}` and reuses I-addresses (sharing, not copying), so `Σ.L` is untouched and refraction reduces to appearance multiplicity (c), already excluded by CN-LOC. The general version-invariance is independently backed by F-PRES (K.δ preserves `Σ.L`), so the conclusion is robust beyond the J4 illustration.
- **Worked example.** `coverage(F) = [1.0.1.0.1.0.1.5, …1.13)` holds ordinals 5..12; a₁/a₂/a₃ touch (6,7,9 / 8 / 11), a₄ diverges at the document component (2 > 1) so is disjoint, a_R's `e₁ = ∅` annihilates via FL-EMP; `nullified = {a₂}` because the equal-length link addresses are prefix-incomparable; count = |{a₁, a₃}| = 2; q\* → |addressable| = 4; q_H' (home d₂) → genuine non-degenerate CN-ZERO since `d₂ ⋠ d₁`. Every figure checks.
- **Transition coverage is exhaustive.** Non-K.λ ⇒ CN-STAB (F-PRES, including K.μ~); K.λ-ordinary ⇒ CN-MONO; K.λ-retraction ⇒ CN-RETRACT. No transition is left unaccounted.

The boundaries the standards demand — empty constrained component (FL-EMP), all-wildcard (max), nullified (excluded yet stored), orphan (counted), reverse-orphan under a home-bound (still counted via the permanent `home(a)`), multi-span endset (counted once), cross-document home mismatch (zero) — are all exercised, most against the concrete store. The cost section's deliberate *non-claim* (value fixed, cost left to the implementation) is correct specification discipline, not an omission.

## REVISE

None. Every claim either derives what is new to counting (CN-UNIT's four-way collapse, CN-ENUM's single-set identity, CN-MONO's increment wp, CN-SNAP/CN-RETRACT's view-vs-store reconciliation) with explicit steps, or delegates inherited semantics (`sat`, `addressable`, `nullified`, `coverage`, `home`) to verified foundations by valid citation. No proof rests on "similarly" or a bare checkmark; no notation is reinvented; no non-foundation ASN is referenced; the operation specifies a system-level guarantee (the cardinality of the satisfying set) abstract enough to bind an alternative implementation, with implementation notes cleanly quarantined as evidence.

## OUT_OF_SCOPE

The ASN's own Open Questions already enumerate and correctly defer the genuinely-future territory — the V-spec-to-address resolution invariant, the concurrency discipline for cross-inquiry count-equals-length, durable caching conditions, fragmentation/dedup of identity, count-vs-enumeration cost as a planning primitive, and federated counting across stores. These are deferred, not mis-handled; the CN-SNAP implementation note touches replication only as a per-vantage observation and routes it to Open Question 6 rather than making a protocol claim. Nothing belonging to a future ASN is smuggled in as a claim here.

VERDICT: CONVERGED
