# Review of ASN-0091

## REVISE

### Issue 1: Phantom foundation invariant "S9 (TwoStreamSeparation)"
**ASN-0091, "Per-Invariant Discharges (ASN-0036 Foundation Invariants)"**: "**S9 (TwoStreamSeparation).** From R-FRAME-P/S(c) directly: two-stream separation reads `Σ'.M(d) ≠ Σ.M(d) ⟹ Σ'.C = Σ.C`, exactly what R-FRAME-P/S(c) supplies."
**Problem**: ASN-0036 (foundation) defines no invariant S9. Its claim set is S0–S5, S7/S7a/S7b/S7d, S8/S8a/S8-fin/S8-depth, D-*. S9 is cited as a load-bearing ASN-0036 invariant and given a specific reading, but it does not exist in the foundation. This is a false foundation citation.
**Required**: Remove S9, or — if the property `Σ'.M(d) ≠ Σ.M(d) ⟹ Σ'.C = Σ.C` is wanted — state it as a local corollary of RE-C rather than attributing it to a nonexistent ASN-0036 invariant.

### Issue 2: Phantom foundation invariant "S7c"
**ASN-0091, "Per-Invariant Discharges (ASN-0036 Foundation Invariants)"**: "**S7a, S7b, S7c, S7d.** Structural attribution and discipline facts on addresses preserved by RA-frame's `Σ'.C = Σ.C` and `Σ'.E = Σ.E`…"
**Problem**: ASN-0036 defines S7a (DocumentScopedAllocation), S7b (ElementLevelIAddresses), S7d (DocumentAllocationDiscipline), and S7 (StructuralAttribution) — but no S7c. ASN-0047's ExtendedReachableStateInvariants likewise lists S7a, S7b, S7d with no S7c. A nonexistent invariant is being "discharged."
**Required**: Drop S7c from the list (discharge S7a, S7b, S7d, and S7).

### Issue 3: Phantom foundation lemma "R-SP (RearrangeSufficientPrecondition)"
**ASN-0091, "R-SP Scope and the Move to Per-Invariant Discharges"**: "ASN-0084's R-SP (RearrangeSufficientPrecondition) is stated as a *whole-package* sufficiency lemma whose hypothesis `R-PRE(K) ∧ ASN-0036-invariants(Σ, d)`… R-SP's sub-lemma R-RI also requires ASN-0036's S3…"
**Problem**: ASN-0084 (foundation) contains no lemma R-SP. (It has R-RI, R-PIV, R-SWP, R-BLK, R-CANON, etc., but no R-SP and R-RI is not a "sub-lemma of R-SP.") An entire subsection — plus the S8a/S8-fin/S8-depth discharge remarks — is framed around extracting discharges "from R-SP's proof structure." The framing rests on a foundation claim that does not exist.
**Required**: Either re-anchor the discussion on lemmas that do exist in ASN-0084, or restate the per-invariant discharges as self-contained without appeal to R-SP.

### Issue 4: Phantom foundation lemma "R-DISP"
**ASN-0091, "Worked Example — 4-cut Swap"**: "The widths are `w_α = 1 ≠ 2 = w_β`, so by ASN-0084's R-DISP the μ-region net displacement is `Δ(μ) = w_β − w_α = +1`."
**Problem**: ASN-0084 defines no claim R-DISP. The displacement value is correct and is computable directly from R-S2 (μ-region maps `c₁ + j ↦ c₀ + w_β + j`, giving net shift `w_β − w_α`), but the citation names a nonexistent foundation claim.
**Required**: Replace the R-DISP citation with the direct R-S2 computation, or remove the `Δ(μ)` framing.

### Issue 5: Renamed foundation invariants/operations
**ASN-0091, "Unified-State Identification" and "P4a Handling"**: "K.δ-IsDocument (ASN-0047)", "`IsDocument(e)`", "**P4a (HistoricalFidelity)**".
**Problem**: ASN-0047 uses the predicate `Document(e)` (and `¬Node(e)`), not `IsDocument(e)`, and names no operation "K.δ-IsDocument." ASN-0047's P4a is **TraceWitnessing**, not "HistoricalFidelity." ASN-0093's M0 reads `T4-valid(d)`, which the discharge restates as "ValidAddress(d)." Per Standard 7, inventing notation for something a foundation already names is a REVISE item.
**Required**: Use the foundation names verbatim — `Document(e)`, P4a (TraceWitnessing), `T4-valid` — and refer to ASN-0047's K.δ Document case rather than a "K.δ-IsDocument" operation.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: CS3 fixes the cut subspace to S = s_C, so REARRANGE_K never reorders the link subspace. What an analogous link-subspace reordering operation would look like, and what invariants it must preserve, is correctly deferred to a future ASN (and already noted in Open Questions).

### Topic 2: Bound on run-decomposition cardinality growth
**Why out of scope**: The ASN proves fragmentation/coalescence/equality are each realizable (RE-frag/coal/eq) but deliberately asserts no upper bound on the per-invocation cardinality increase. Establishing such a bound is new territory, listed in Open Questions, not a defect here.

The mathematics is otherwise sound: the four worked examples (3-cut, 4-cut, interior-cut, shared-I-address) and the two-step composition trace all check out numerically, boundary cases (empty arrangement, identity π, shared I-addresses via S5) are handled, and the abstract/REARRANGE_K provenance split is disciplined. The blocking issues are foundation citations that fail to resolve, not logical gaps.

VERDICT: REVISE
