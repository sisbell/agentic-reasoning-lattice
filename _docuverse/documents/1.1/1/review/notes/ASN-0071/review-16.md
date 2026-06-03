# Review of ASN-0071

I checked the subspace-confinement proof, the resolve-equivalence derivation, the worked scenario, and the finiteness induction. The core proofs are sound — the TumblerAdd prefix-copy argument for `t₁ = u₁`, the `dom(C)/dom(L)` disjointness routing, and the K.δ-counts-only finiteness step all hold. The issues below are about the worked example failing to exercise the claims it asserts, plus one premise misattribution.

## REVISE

### Issue 1: Worked example verifies F-PART vacuously
**ASN-0071, "A worked scenario" → "What this verifies"**: "F-PART. A single shared I-address (`a₁`) is sufficient for inclusion. The result does not require a document to reference any particular portion of the queried span."
**Problem**: The query resolves to `iaddrs(Q)(Σ) = {a₁}` — a singleton. When the resolved set has exactly one element, "references a partial portion" and "references the whole query" are indistinguishable: any non-empty intersection is the entire set. The example therefore cannot exercise F-PART ("partial overlap suffices"), which is precisely the claim that a document sharing a *proper subset* of a multi-address query still qualifies. The bullet asserts F-PART but the scenario proves only the singleton case.
**Required**: Extend the scenario so `|iaddrs(Q)(Σ)| ≥ 2` (e.g., a two-position content span, or a vspec-set resolving to `{a₁, a₂}`) and a returned document references only one of the two — so the empty/non-empty intersection distinction is genuinely tested.

### Issue 2: Resolve-equivalence (multi-block case) never checked against a concrete state
**ASN-0071, "Resolution"**: "`iaddrs_one(d_s, σ)(Σ)` equals the set-flattening of ASN-0058's `resolve(d_s, σ)` … By C1a, `resolve(d_s, σ)` is read off the unique maximally merged block decomposition `⟨β₁, ..., β_K⟩` …"
**Problem**: This is a non-trivial derived result spanning C1a, B1, B3 and the set-flattening/dedup argument over multiple blocks. The only worked state has `M(d_A) = {v_A ↦ a₁}` — a single width-1 entry, hence `K = 1`, a degenerate one-block decomposition. The multi-block machinery (where `resolve` yields `⟨(a₁,n₁),...,(a_K,n_K)⟩` with `K ≥ 2`, and where dedup of shared I-addresses across blocks actually matters per M14) is asserted but never verified against any concrete arrangement. Per standard #6, a key derived claim needs a concrete example exercising it.
**Required**: Add (or extend) a scenario with a `d_s` whose `⟦σ⟧ ∩ dom(M(d_s))` decomposes into at least two maximal runs, and check `iaddrs_one` equals the set-flattening of the resulting `resolve` sequence — including a case where two blocks carry the same I-address so the dedup step is exercised.

### Issue 3: `m ≥ 2` misattributed to C0
**ASN-0071, "The query"**: "well-formedness implies `actionPoint(ℓ) = m ≥ 2` via C0, and we lift this consequence into an explicit precondition…"
**Problem**: ASN-0058's C0 establishes only `k = m` (action point equals common depth). The `m ≥ 2` bound is not from C0 — it comes from the S8a lower bound on subspace depth (equivalently stated as a precondition in C0a, not derived in C0). Standard #6 requires named premises for derived guarantees; citing C0 for the `≥ 2` half is a premise error.
**Required**: Attribute `actionPoint(ℓ) = m` to C0 and `m ≥ 2` to S8a / S8-depth (or C0a) separately.

## OUT_OF_SCOPE

### Topic 1: Historical-containment query over the provenance relation `R`
**Why out of scope**: The ASN correctly identifies (Open Questions; "Permanence and currency reconciled") that an `R`-based "ever-contained" query is a distinct operation. Specifying it is a future ASN, not a gap in this one.

### Topic 2: Replica freshness and visibility-filtering
**Why out of scope**: Explicitly deferred in "What we do not specify" and logged as Open Questions; these are separable policy/distribution layers.

VERDICT: REVISE
