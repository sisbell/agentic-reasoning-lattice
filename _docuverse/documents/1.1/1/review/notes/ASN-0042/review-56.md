# Review of ASN-0042

This ASN is a thorough and well-constructed treatment of tumbler ownership. The proofs generally show their work, case analyses are typically exhaustive, and the worked example concretely verifies a wide swath of the claimed properties. I have a small number of substantive concerns and a few presentational gaps to flag.

## REVISE

### Issue 1: O7(c) postcondition only addresses condition (ii), not condition (vi)

**ASN-0042, O7 Postcondition (c) and its proof**: "the delegation relation is satisfiable with `π'` as delegator for any sub-prefix `p''` ... at every state at which `π'` remains the most-specific covering principal for `p''` — equivalently, no existing sub-delegate `π''' ∈ Π` with `pfx(π') ≺ pfx(π''') ≼ p''` has already been introduced."

**Problem**: The "equivalently" clause translates the conditional to condition (ii) re-checking only. But full delegation requires all six conditions; condition (vi) — no existing principal has prefix strictly extending `p''` — is also subject to invalidation by later sub-delegations. Concrete failure: if `π_A` (pfx `[1,0,2]`) first delegates `[1,0,2,3,5]` to `π*`, then attempts to delegate `p'' = [1,0,2,3]`, condition (ii) still holds (π_A remains the most-specific covering principal of `p''` since `pfx(π*) ⋠ p''`), but condition (vi) fails because `p'' ≺ pfx(π*)`. The chain-construction proof later does check both (ii) and (vi) per link, but the abstract postcondition's wording suggests only (ii) matters.

**Required**: Either broaden (c) to "satisfiable when both (ii) and (vi) continue to hold", or explicitly note that (vi) is a separate re-checking obligation distinct from most-specific-covering status.

### Issue 2: O8 single-step "trajectory must pass through Σ_d^post" argument conflates two readings of `delegated_Σ`

**ASN-0042, O8 proof, Step "The delegate persists with an unchanged prefix"**: The argument treats `delegated_{Σ_d}(π, π')` as witnessing the specific introducing transition `Σ_d → Σ_d^post`, but the relation's definition is also used elsewhere as the satisfaction of the six conditions at a given source state.

**Problem**: The proof's bootstrap-exclusion step argues "By O15, each introduction event is either bootstrap or a delegation transition. Bootstrap is excluded... The remaining clause of O15 supplies an existing principal..." — this only excludes bootstrap, but does not establish that the specific delegator named in `delegated_{Σ_d}` is the actual introducing delegator. The argument works because condition (i) — `pfx(π) ≺ pfx(π')` — pins down the length inequality unconditionally, regardless of which delegator actually performed the introduction. But the formal contract should make explicit whether `delegated_Σ` is (a) a witness to an actual transition or (b) a satisfaction of conditions at `Σ`.

**Required**: A single sentence in the Delegation definition clarifying which reading is intended ("witness to actual transition" vs. "satisfaction at state"). The proofs are sound under the witness reading, but the ambient ambiguity makes the trajectory argument harder to verify than necessary.

### Issue 3: AccountField definition is stated in the prose, but Postcondition (c) (`acct(a) = a` when `zeros(a) ≤ 1`) is not separately verified against the `zeros(a) = 1` branch of the definition

**ASN-0042, AccountField Postconditions (c)**: "When `zeros(a) ≤ 1`: `acct(a) = a`."

**Problem**: The definition reads `acct(a) = a` for `zeros(a) = 0`, but `acct(a) = N(a) ++ [0] ++ U(a)` for `zeros(a) ≥ 1`. Postcondition (c) implicitly claims that when `zeros(a) = 1` the second branch reduces to `a`. The justification is given inline in the AccountPrefix proof (Case `zeros(a) = 1`: "since `a` has exactly one zero separator and only node and user fields, `a = [N₁, …, Nα, 0, U₁, …, Uβ] = acct(a)`") but not in the AccountField specification itself.

**Required**: One-line justification in AccountField's *Definition* slot noting that when `zeros(a) = 1`, the formula `N(a) ++ [0] ++ U(a)` reconstructs `a` because `a` has no fields beyond the user field; alternatively, fold the verification into the Postcondition (c) prose. Right now (c) reads like an axiom but is actually a derived fact about the definition.

### Issue 4: Inductive preservation arguments for O1a, O1b, T4 are sketched but not laid out with explicit base/step over reachability

**ASN-0042, *Delegation* section, after stating the six conditions**: Three short paragraphs sketch that delegation preserves O1a, T4, and O1b. Each paragraph names a condition (iv/v) plus O12/O13 and concludes "is maintained across the transition" or "is maintained across all state transitions."

**Problem**: The full claim — that O1a, O1b, T4 hold in every reachable state — requires induction over the transition sequence with base case from O14 and inductive step from the conditions. The paragraphs handle only the inductive step for delegation transitions; non-delegation transitions (Bop without introducing principals) trivially preserve the invariants, but this is not noted. A reader who is not already convinced of the standard induction-over-transitions pattern has to reconstruct it.

**Required**: A single closing sentence per preservation paragraph: "Combined with O14's [iii/iv/v] base case and the trivial preservation under non-delegation transitions (Π unchanged, prefixes unchanged by O13), induction over the transition sequence gives the invariant in every reachable state." This matches the explicit structure given for FiniteRegistry and PrefixBaptismCoupling.

### Issue 5: SelfOwnershipAtPrefix verification at `a_6 = pfx(π_A)` references the general property but the *Worked Example* prose suggests it is being established there

**ASN-0042, *Worked Example*, "Self-ownership at the prefix"**: The paragraph traces the longest-match outcome at `[1, 0, 2]` concretely, then concludes "The general statement `(A Σ, π ∈ Π_Σ : ω_Σ(pfx(π)) = π)` is established as the derived property SelfOwnershipAtPrefix in the *Exclusivity Invariant* section above (from O1b, O2, and PrefixBaptismCoupling); the present paragraph exhibits the concrete witness rather than re-derive the general fact."

**Problem**: The phrasing is correct but the paragraph layout invites the reader to take it as a derivation. The general property is derived earlier in the *Exclusivity Invariant* section (in two sentences). It would help to mark the worked-example paragraph more clearly as a verification scenario rather than a partial argument, or to move the concrete witness adjacent to the derivation so the relationship is unambiguous.

**Required**: A presentational fix — either rename the worked-example paragraph (e.g., "Concrete witness for SelfOwnershipAtPrefix") or insert a sentence at the top stating "We verify the already-derived property SelfOwnershipAtPrefix at the concrete boundary..." (the current concluding sentence covers this but only after the trace).

### Issue 6: The Worked Example's Fork trajectory verification convention is stated, but at least one Bop call's preconditions are not exhibited in the running narrative

**ASN-0042, *Worked Example*, "Trajectory" under Fork (O10)**: The "*Verification convention*" paragraph says "We do not trace each intermediate state along the trajectory `Σ_0 → ⋯ → Σ_pre`; instead we record the cumulative baptismal registry and note, in aggregate, which B6/B1 obligations were discharged by which Bop call."

**Problem**: Two of three Bop calls list both B6 and B1 checks; one (call (3) producing `a_2`) lists B6 ("at the bound, but satisfied") and B1 (vacuous, first member of stream) — but the *Sub-account namespaces* paragraph's two namespace baptisms (producing `[1, 0, 2, 1]` and `[1, 0, 2, 2]`) defer to "*Sub-account namespaces* below — producing `[1, 0, 2, 1]` and `[1, 0, 2, 2]` in `S([1, 0, 2], 1)` — are likewise verified there." The cross-paragraph deferral is fine, but a reader following the trajectory linearly cannot confirm the cumulative Σ_2.B claim without jumping ahead and back.

**Required**: Either inline the namespace-baptism B6/B1 verifications at the trajectory site or restate the verification convention to make the cross-paragraph deferral explicit before the cumulative Σ_2.B claim is made.

## OUT_OF_SCOPE

None. The ASN's scope restrictions are appropriate, and the open questions list addresses topics that genuinely belong to future ASNs (ownership transfer, content accessibility under principal removal, cross-node federation).

VERDICT: REVISE
