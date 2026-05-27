# Review of ASN-0099

## REVISE

### Issue 1: A1's "Propagation" clause forward-binds future revisions of other ASNs
**ASN-0099, A1 (EffectClauseExhaustivity), Propagation clause**: "If V is extended by future revision — a new operation added, an existing operation replaced — every operation in the revised V inherits the same exhaustivity obligation."

**Problem**: ASN-0099 specifies a read-only operation (FINDLINKS) but uses A1 to impose a binding meta-contract on the specifications of ASN-0047 and ASN-0093, and on all future revisions of the substrate vocabulary. This is overreach for a single-operation ASN. The vocabulary-scope and contract clauses are defensible (A1 is genuinely load-bearing for F9's K.μ⁺/K.μ⁻ case and F9-cor's K.ρ case), but the propagation clause asserts authority over future work in other ASNs.

**Required**: Narrow A1 to the current vocabulary as enumerated, or restate A1 explicitly as a transient assumption pending the ASN-0047 revision that the OQ already proposes. The cleanest fix is the one the ASN's own Open Question identifies: revise ASN-0047 to add `L' = L` to K.μ⁺/K.μ⁻/K.ρ frames, then delete A1 entirely. Until that revision lands, A1 should be framed as a discharge premise, not as a binding interface contract on substrate evolution.

### Issue 2: F19 monotonicity not extended to filtered/scoped variants
**ASN-0099, F19 (ResultSetMonotonicity)**: "For any reachable state sequence Σ →* Σ' and any I ⊆ T: findlinks(I, Σ) ⊆ findlinks(I, Σ')."

**Problem**: The ASN states determinism (F15, F16) and survivability (F17, F18) for both `findlinks_filtered` and `findlinks_scoped`, but states monotonicity F19 only for the unfiltered `findlinks`. Filtered and scoped queries are described as "the operationally common forms" — by that standard, monotonicity belongs in the explicit claims package alongside F17 and F18. The derivation is trivial (LP13 fixes per-slot coverages, so filtered constraints' satisfaction status is monotone; scoped intersection preserves inclusion), but the claim is not stated.

**Required**: Add explicit monotonicity claims for filtered and scoped variants, or add a note immediately after F19 stating that monotonicity follows from F19 + LP13 for the filtered form and from F19 + intersection-preservation for the scoped form.

### Issue 3: F2/F3 formal claims missing for filtered/scoped variants
**ASN-0099, "Completeness" section**: "For the filtered form, the same obligation holds against `findlinks_filtered(C, Σ)`: completeness requires every link satisfying every constraint in `C` to appear in the filtered output, and soundness requires no spurious link."

**Problem**: The completeness/soundness obligation for filtered and scoped forms is stated in prose but not as numbered F-claims. The presentation is asymmetric: F15-F18 give determinism and survivability formally for the variants, but F2/F3 (the conformance contract that makes `result` coincide with the abstract specification) remain implicit for them. An implementer reading the claims table cannot point to a specific clause pinning their filtered implementation's output to `findlinks_filtered(C, Σ)`.

**Required**: State F2/F3 analogues formally for `findlinks_filtered(C, Σ)` and `findlinks_scoped(I, S, Σ)`, or restate F2/F3 in a form general enough to cover all three abstract operations uniformly.

### Issue 4: F4 derivation lacks case-by-case treatment of enumerated strengthenings
**ASN-0099, F4 (MatchFormulaUniqueness)**: "The derivation is immediate from F1 under existential introduction: any singleton overlap at any slot satisfies F1's predicate, so any predicate that fails to recognize at least one such overlap excludes a link that F1 includes."

**Problem**: F4 explicitly enumerates four candidate strengthenings (`coverage(eᵢ) ⊆ I`, `I ⊆ coverage(eᵢ)`, `|∩| ≥ k > 1`, "or any other refinement"), but the derivation collapses all four into one sentence about "any predicate that fails to recognize at least one such overlap". The general statement is true but its application to each enumerated case requires a slightly different argument (e.g., why `coverage(eᵢ) ⊆ I` fails on a non-singleton coverage meeting a singleton query — show the witness pair).

**Required**: Either walk through each enumerated strengthening with a one-line witness exclusion, or remove the enumeration and state F4 as a single general claim about strengthenings.

## OUT_OF_SCOPE

The ASN's "What We Have Not Specified" section appropriately defers phantom addresses (I-addresses outside `dom(Σ.C) ∪ dom(Σ.L)`), partitioning/replication semantics, concurrency model, access-control composition, and the FOLLOWLINK inverse direction. These are correctly scoped out and do not need flagging.

VERDICT: REVISE
