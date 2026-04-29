# Local Review — ASN-0034 (cycle 2)

*2026-04-23 20:14*

65 claims (ActionPoint, AllocatedSet, D0, D1, D2, Divergence, GlobalUniqueness, NAT-addcompat, NAT-discrete, NAT-sub, NoDeallocation, OrdinalDisplacement, OrdinalShift, PartitionMonotonicity, Prefix, ReverseInverse, T0(a), T0(b), T1, T10, T10a, T10a-N, T10a.1, T10a.2, T10a.3, T10a.4, T10a.5, T10a.6, T10a.7, T10a.8, T2, T3, T4, T4a, T4b, T4c, T5, T6, T7, T8, T9, TA-LC, TA-MTO, TA-PosDom, TA-RC, TA-assoc, TA-dom, TA1, TA1-strict, TA2, TA3, TA3-strict, TA4, TA5, TA5-SIG, TA5-SigValid, TA5a, TA6, TA7a, TS1, TS2, TS3, TS5, TumblerAdd, TumblerSub)

## REVISE

### ActionPoint

#### Missing component-value typing in T0 Depends entry
**Class**: REVISE
**Issue**: The derivation instantiates NAT-zero's axiom `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` at `n = w_{actionPoint(w)}` and NAT-discrete's `(A m, n ∈ ℕ :: m < n ⟹ m + 1 ≤ n)` at `n = w_{actionPoint(w)}`, both of which require `w_{actionPoint(w)} ∈ ℕ`. This typing comes from T0's commitment `aᵢ ∈ ℕ at each i ∈ {1, …, #a}`, but the Depends entry for T0 only cites "component projection wᵢ, and the commitment that the index domain `{1, …, #w}` of w is a subset of ℕ" — it names the index-domain typing, not the component-value typing that is actually being used.
**Required**: Extend the T0 Depends note to explicitly cite that the component projection delivers ℕ-valued components (i.e., `wᵢ ∈ ℕ` for each `i ∈ {1, …, #w}`), as this is the typing that licenses the NAT-zero and NAT-discrete instantiations at `w_{actionPoint(w)}`.

#### Skipped range check in the `wᵢ = 0 for i < actionPoint(w)` argument
**Class**: REVISE
**Issue**: For `1 ≤ i < actionPoint(w)`, the derivation asserts "otherwise i would be a member of S", but membership in `S = {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}` also requires `i ≤ #w`. This bound is not given directly by the hypothesis `1 ≤ i < actionPoint(w)`; it must be derived by chaining `i < actionPoint(w)` with `actionPoint(w) ≤ #w` (obtained from `actionPoint(w) ∈ S`) — a step the uniqueness paragraph above unfolds with explicit case analysis on `≤` but which is silent here.
**Required**: Make the `i ≤ #w` step explicit. E.g., unfold `actionPoint(w) ≤ #w` as `actionPoint(w) < #w ∨ actionPoint(w) = #w` and combine with `i < actionPoint(w)` (transitivity in the first branch, rewriting in the second) to reach `i < #w`, hence `i ≤ #w`, before concluding `i ∈ S`.

#### Skipped case-analysis to contradict the least-element clause
**Class**: REVISE
**Issue**: The same step concludes by saying `i < actionPoint(w)` "contradicts `(A n ∈ S :: actionPoint(w) ≤ n)`", but the contradiction is not direct. At `n = i`, the universal gives `actionPoint(w) ≤ i`, and combined with `i < actionPoint(w)` the contradiction needs the same two-case unfolding (`actionPoint(w) < i` with transitivity to irreflexivity; `actionPoint(w) = i` with substitution to irreflexivity) that the uniqueness paragraph performs explicitly for `m₁, m₂`. The derivation leaves this collapse to the reader.
**Required**: State the `≤`-unfolding at `n = i` and dispatch both disjuncts by irreflexivity (after transitivity or substitution), matching the level of detail used in the uniqueness case analysis.

### T0(b)

#### Reflexivity derivation from trichotomy is underspecified
**Class**: REVISE
**Issue**: The proof of `(ii)` asserts that NAT-order's "trichotomy clause at `(n, n)` forces `n = n`". Trichotomy at `(n, n)` gives only the disjunction `n < n ∨ n = n ∨ n < n`; it does not by itself "force" the middle disjunct. To isolate `n = n`, the argument additionally needs either (a) NAT-order's irreflexivity clause `¬(n < n)` to eliminate the outer disjuncts, or (b) reflexivity of equality (a logical principle, not supplied by NAT-order) to establish `n = n` directly and bypass trichotomy entirely. As written, the inference step "trichotomy ... forces `n = n`" is not valid from NAT-order's trichotomy axiom alone, and the NAT-order Depends entry's gloss ("reflexivity of `≥` ... via trichotomy at `(n, n)` and the defined converses of `<` and `≤`") inherits the same gap — it omits the auxiliary principle that selects the `n = n` disjunct.
**Required**: Rewrite the reflexivity step to be logically complete. The cleanest route: `n = n` by reflexivity of equality; hence `n < n ∨ n = n`, i.e. `n ≤ n` by NAT-order's definitional clause `m ≤ n ⟺ m < n ∨ m = n`; hence `n ≥ n` by the defined converse. This needs only NAT-order's `≤`/`≥` definitions (no trichotomy, no irreflexivity). Update both the narrative in part `(ii)` and the NAT-order gloss in the Depends list accordingly. If the irreflexivity-elimination route is preferred instead, the narrative must explicitly cite NAT-order's irreflexivity clause alongside trichotomy.

VERDICT: REVISE

### T4

#### `zeros(t)` not defined in the Formal Contract
**Class**: REVISE
**Issue**: The Formal Contract's *Axiom* writes `zeros(t) ≤ 3` and the *Consequence* writes `zeros(t) ∈ {0, 1, 2, 3}`, but the operator `zeros : T → ℕ` is never defined inside the contract. Its definition `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` appears only in the narrative. A downstream consumer reading the Formal Contract in isolation sees an ungrounded symbol — `zeros` is not a primitive of T0, NAT-card, or any other declared dependency, so it must be introduced here. The contract does include an inline stipulative definition of *field separator*, so an analogous treatment of `zeros(t)` is required.
**Required**: Add a *Definition:* slot (or an explicit definitional clause inside the Axiom, parallel to the field-separator stipulation) reading `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|`, with the typing remark that the index set is a subset of `{1, …, #t} ⊆ ℕ` so NAT-card applies.

### T4a

#### Unjustified step: `s_k < #t ⟹ s_k ≤ #t − 1`
**Class**: REVISE
**Issue**: In the Reverse direction's Last-segment argument, the proof concludes `s_k ≤ #t − 1` directly from `s_k ≠ #t` and `s_k ≤ #t`. The Depends block attributes this promotion to NAT-discrete. But NAT-discrete's axiom gives only `s_k < #t ⟹ s_k + 1 ≤ #t`; the passage from `s_k + 1 ≤ #t` to `s_k ≤ #t − 1` is a *different* proposition (the two are equivalent only via +1-monotonicity of `≤`, which is not declared). To cross the gap one must case-split on `≤` and invoke NAT-sub's right-telescoping `(s_k + 1) − 1 = s_k` and strict monotonicity — none of which are cited. The symmetric Forward step for condition (ii) uses `s₁ ≥ 2`, which *is* NAT-discrete directly; only the Last-segment step has this asymmetric form.
**Required**: Either rewrite the Last-segment conclusion as `s_k + 1 ≤ #t` (the direct NAT-discrete output) so that segment non-emptiness `#t ≥ s_k + 1` is stated in its native `+1` form, or spell out the detour through NAT-sub right-telescoping / strict monotonicity and amend the Depends gloss for NAT-sub to mention this role (currently NAT-sub is cited only for `#t − 1 ∈ ℕ`).

#### Unjustified index identification in Forward (i)
**Class**: REVISE
**Issue**: The Forward direction of condition (i) assumes `tᵢ = 0 ∧ tᵢ₊₁ = 0` and writes "say `s_j = i` and `s_{j+1} = i + 1`". That `i + 1` is the *immediate* successor of `i` in the enumeration `s₁ < s₂ < … < s_k` (rather than some later `s_{j'}` with `j' > j + 1`) is not self-evident: it requires that no natural number lies strictly between `i` and `i + 1`, i.e., NAT-discrete's no-interval Consequence `m ≤ n < m + 1 ⟹ n = m`. Additionally, the argument tacitly needs `j ≤ k − 1` (so that `s_{j+1}` is a real zero position rather than the sentinel `#t + 1`) — which follows because `i + 1 ≤ #t`, but is not mentioned.
**Required**: Add one sentence citing NAT-discrete's no-interval form to justify that consecutive zero positions in the enumeration correspond to consecutive integer indices, and note `j + 1 ≤ k` from `i + 1 ≤ #t`.

### T10a.3

#### Dependency descriptions misrepresent actual usage
**Class**: REVISE
**Issue**: Two of the declared dependencies are described in ways that undermine their inclusion. NAT-zero's description says it is "declared as part of the NAT foundation chain underwriting the difference `d_B − d_A`" — but the difference's well-formedness is carried by NAT-sub's conditional closure (cited explicitly), and NAT-zero's minimum-of-ℕ axiom is not invoked anywhere in the proof body. NAT-discrete's description openly states "the local-monotonicity step here cites NAT-sub's strict positivity directly rather than going through discreteness" — i.e., the discreteness axiom is not used. A reader cannot tell whether these are load-bearing dependencies or ceremonial foundation-chain declarations.

If the intended role of NAT-zero + NAT-discrete is to sharpen `k' > 0` to `1 ≤ k'` (as T10a's Consequence 3 does explicitly), the proof body should cite them at the point `1 ≤ k'` is first used — the current text treats `1 ≤ k'` as immediate from `k' ∈ {1, 2}` without citation.
**Required**: Either (a) remove NAT-zero and NAT-discrete from Depends and derive `1 ≤ k'` directly from `k' ∈ {1, 2}` as a set-membership fact, or (b) cite both in the narrative where `k' ∈ {1, 2}` is lifted to `1 ≤ k'` (matching T10a Consequence 3's pattern), and rewrite their Depends descriptions to name that specific role rather than "NAT foundation chain" filler.

### T9

#### Proof duplicates T10a.7's stronger postcondition without citing it
**Class**: REVISE
**Issue**: T10a.7's postcondition is stated as the equivalence `(A m, n ≥ 0 : m < n : tₘ < tₙ)` — this is exactly the conclusion T9 needs. T9 declares T10a.7 as a dependency only for "fixes each index uniquely", then re-proves the strict-monotonicity statement from scratch via induction on `d = j − i`. The induction repeats T10a.7's lemma L verbatim. Either T9 should derive `a < b` in one line by combining T10a.6 (unique witness `A`) + T10a.7 (`i < j ⟹ tᵢ < tⱼ`), or the redundancy must be justified.
**Required**: Replace the inductive proof with a direct citation: by T10a.6, `A` is uniquely fixed by `(a, b)`; by T10a.7's strict-order form, `i < j ⟹ tᵢ < tⱼ`, so `a = tᵢ < tⱼ = b`. Update the *Depends* annotation for T10a.7 to reflect the strict-order use, not just index uniqueness.

#### Index arithmetic (`tⱼ₋₁`, `(j−1)+1 = j`) lacks declared NAT- dependencies
**Class**: REVISE
**Issue**: The inductive step writes `tⱼ₋₁` and then `tⱼ₋₁ < inc(tⱼ₋₁, 0) = tⱼ`, which silently invokes natural-number subtraction (`j − 1`) and the arithmetic identity `(j − 1) + 1 = j` to match T10a's enumeration rule `tₙ₊₁ = inc(tₙ, 0)`. T10a.7 — proving the same kind of statement — was explicit about this, declaring NAT-sub (positivity and left-inverse) and NAT-addassoc, and routing through a `tₘ < t_{m+d}` lemma precisely to avoid forming `n − 1` inside the induction. T9's *Depends* lists neither NAT-sub nor NAT-addassoc nor anything justifying `j − 1 ≥ 0` for `j ≥ i + 2`.
**Required**: Either (preferred) eliminate the issue by deriving T9 from T10a.7 as above, or add NAT-sub and NAT-addassoc (and NAT-order to discharge `j ≥ 1`) to the *Depends* and route the induction through a positive-gap lemma as T10a.7 does.

### AllocatedSet

#### T2 over-restricts spawn point to parent's current frontier without sound justification
**Class**: REVISE
**Issue**: (T2) imposes the precondition `spawnPt(A) = t_{nₛ(parent(A))}` — spawning is admissible only when the parent's realized chain has advanced *exactly* to spawnPt(A). T10a (dep) only requires `spawnPt(A) ∈ dom(parent(A))`, so T10a permits spawning from any element of parent's abstract chain at any later time (e.g., parent's frontier at t₅, spawn a child from t₃). The claim's stated justification — "without pinning spawnPt(A) to that last realized element the transition has no unique argument for inc" — is incorrect: `inc(spawnPt(A), spawnParam(A))` has a unique argument because spawnPt(A) is fixed by A's spawning triple (T10a), independent of parent's current count nₛ(parent(A)). So the restriction is a genuine narrowing of T10a's allocator discipline, not a well-formedness necessity. Counterexample: under T10a, a parent at frontier t₅ retroactively spawning a child whose triple has spawnPt = t₂ is permitted (the pair (t₂, k') has not been used); the claim's (T2) makes this transition inadmissible.
**Required**: Either (a) relax (T2)'s precondition to `spawnPt(A) = tᵢ for some i ≤ nₛ(parent(A))` (requiring only that spawnPt is already realized), or (b) explicitly justify the frontier-only restriction as an *additional* design axiom beyond T10a — state it as a design choice with its own rationale (e.g., sequential spawning discipline), not as forced by well-definedness of inc.

### Divergence

#### Case (ii) entry condition conflates length inequality with sub-case applicability
**Class**: REVISE
**Issue**: Case (ii) is introduced by "If `#a ≠ #b`, NAT-order's trichotomy applied to `(#a, #b)` ... leaves exactly one of `#a < #b` or `#b < #a`." This wording, repeated in the formal contract as "leaves exactly one of: (ii-a) `#a < #b` with `(A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)` ... or (ii-b) ...", asserts that whenever `#a ≠ #b`, exactly one of sub-cases (ii-a)/(ii-b) holds. This is false. Trichotomy on `(#a, #b)` only chooses which length is smaller — it does not establish the prefix-agreement clause that each sub-case requires. Counterexample: take `a = 1.7` and `b = 2.5.9`. Then `#a < #b`, so trichotomy selects the (ii-a) branch, but `a₁ = 1 ≠ 2 = b₁` falsifies `(A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Sub-case (ii-a) does not apply; the pair belongs to case (i). The intended reading — "case (ii) applies iff lengths differ AND shared positions agree, with (ii-a)/(ii-b) further split by which is shorter" — is what the mutual-exclusivity argument relies on, but the stated case-(ii) precondition is just `#a ≠ #b`.
**Required**: Restate case (ii)'s entry condition as the conjunction `#a ≠ #b ∧ (A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` (or equivalently "case (i) does not apply"), then use trichotomy on lengths only to split into (ii-a)/(ii-b). Mirror this fix in the formal-contract Definition slot.

### TumblerSub

#### "Consequence" clause misfiled in Preconditions slot
**Class**: REVISE
**Issue**: The Formal Contract writes `*Preconditions:* a ∈ T, w ∈ T, a ≥ w (T1). Consequence: when zpd(a, w) is defined, aₖ > wₖ at k = zpd(a, w).` The "Consequence:" line is a *derived* fact (the body's headline lemma), not a precondition — a caller does not need to establish `aₖ > wₖ` to invoke TumblerSub; the claim itself proves it from `a ≥ w`. Appending it under "Preconditions" misleads downstream consumers about what they must supply and mixes the call contract with an internal lemma. The review checklist's Formal Contract field set does not include a "Consequence" sub-bullet.
**Required**: Remove the "Consequence: …" tail from the Preconditions bullet. If `aₖ > wₖ` must be stated formally (e.g., because downstream claims cite it), promote it to a Postconditions bullet guarded by "when zpd(a, w) is defined" — alongside Pos and actionPoint — or fold it into the prose derivation and drop it from the contract entirely.

#### NAT-sub strict positivity declared but unused
**Class**: REVISE
**Issue**: The Depends entry for NAT-sub enumerates three clauses including "strict positivity `aₖ − wₖ ≥ 1` under `aₖ > wₖ`", but nowhere in the body is `aₖ − wₖ ≥ 1` invoked. The Pos derivation deliberately takes the longer route through right-inverse plus left identity plus disjointness to reach `rₖ ≠ 0`, despite strict positivity giving `rₖ ≥ 1`, hence (via NAT-zero's `¬(n < 0)` and NAT-order trichotomy) `rₖ ≠ 0` in one step. A dependency named in the contract must be cited in the reasoning or dropped; otherwise the Depends slot ceases to be a precise inventory of what the proof consumes.
**Required**: Either (a) rewrite the Pos step to cite strict positivity directly (`aₖ > wₖ ⟹ rₖ = aₖ − wₖ ≥ 1`, whence `rₖ ≠ 0` by NAT-order/NAT-zero), shedding the right-inverse + left-identity + disjointness chain; or (b) keep the current derivation and delete the strict-positivity clause from the NAT-sub Depends entry (retaining only conditional closure and right-inverse).

#### actionPoint equality asserted without minimum argument
**Class**: REVISE
**Issue**: The claim writes "`k` is a valid existential witness; whence **`Pos(a ⊖ w)`** (TA-Pos). By ActionPoint, **`actionPoint(a ⊖ w) = zpd(a, w)`**." ActionPoint's contract defines `actionPoint(t)` as the *unique minimum* of `S = {i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0}` — not merely any witness. Establishing `rₖ ≠ 0` proves `k ∈ S`, but to conclude `actionPoint(a ⊖ w) = k` the argument must show `k = min S`, i.e., that no `i < k` satisfies `rᵢ ≠ 0`. That follows from the Definition (`rᵢ = 0` for `i < k`), but the body never discharges this step; it jumps from witness to equality.
**Required**: Insert a line between Pos and the ActionPoint conclusion discharging minimality: for `1 ≤ i < k`, `rᵢ = 0` by the Definition, so no such `i` lies in `S`; combined with `k ∈ S`, ActionPoint's uniqueness clause (or the least-element characterization) yields `actionPoint(a ⊖ w) = k = zpd(a, w)`.

#### T1 case selection in Divergence case (i) is unstated
**Class**: REVISE
**Issue**: "Since `w < a` via T1 case (i), `wₖ < aₖ`." The selection of T1 case (i) over T1 case (ii) is not argued. `w < a` could a priori hold via T1(ii) (w a proper prefix of a); that would give `wᵢ = aᵢ` for `1 ≤ i ≤ #w`, directly contradicting Divergence case (i)'s `wₖ ≠ aₖ` with `k ≤ #w`. The argument also relies on T1(i)'s witness coinciding with the divergence index `k`, which needs Divergence's uniqueness clause. Both steps are omitted, leaving the key inequality `wₖ < aₖ` resting on a correspondence the reader must reconstruct.
**Required**: Add a sentence eliminating T1(ii) from the pair `(w, a)` in Divergence case (i) using the shared-position disagreement `wₖ ≠ aₖ`, and cite Divergence's case-(i) uniqueness to identify the T1(i) witness with `k`, before concluding `wₖ < aₖ`.

### T10

#### Dependency name mismatch for T3
**Class**: REVISE
**Issue**: The Depends slot lists `T3 (CanonicalRepresentation)`, but T3's own header and Formal Contract in the provided dependency pack identify it as `T3 (SequenceEqualityIsComponentwise)`. A downstream reader resolving the dependency by name will not find a claim named CanonicalRepresentation. (Note: the Prefix dependency carries the same mismatch, so the problem is systemic, but within T10 the cited name must resolve to an actual claim.)
**Required**: Either rename the citation to `T3 (SequenceEqualityIsComponentwise)` to match the claim's header, or rename T3 and the other dependent citations (Prefix) consistently. Pick one canonical name and use it everywhere.

#### "Reverse direction of T3" misnames the direction used
**Class**: REVISE
**Issue**: T3 is a biconditional `a = b ≡ #a = #b ∧ (∀i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. The proof infers `a ≠ b` from `aₖ ≠ bₖ` (with `1 ≤ k ≤ #a`). That step is the contrapositive of the *forward* direction (`a = b ⟹ RHS`, contrapositively `¬RHS ⟹ a ≠ b`), not the *reverse* direction (`RHS ⟹ a = b`, contrapositively `a ≠ b ⟹ ¬RHS`). The reverse direction runs the wrong way for the inference used.
**Required**: Replace "By the reverse direction of T3" with "By the contrapositive of the forward direction of T3" (or "By T3, since `a, b` differ at position `k ≤ #a`, `a ≠ b`"), and explicitly note that `k ≤ m ≤ #a` places `k` in T3's index domain `{1, …, #a}`.

#### Well-definedness of `aₖ`, `bₖ` not explicit
**Class**: REVISE
**Issue**: The proof writes `aₖ = p₁ₖ` and `bₖ = p₂ₖ` without explicitly justifying that `k` lies in the index domains `{1, …, #a}` and `{1, …, #b}`. One needs `k ≤ m ≤ #a` (from `p₁ ≼ a` giving `#p₁ ≤ #a`) and `k ≤ n ≤ #b` (from `p₂ ≼ b`). This is a silent use of Prefix's length clause and NAT-order transitivity of `≤`.
**Required**: Add an explicit line: "From `p₁ ≼ a`, Prefix gives `#p₁ ≤ #a`, i.e. `m ≤ #a`; with `k ≤ m` and NAT-order transitivity, `k ≤ #a`, so `aₖ` is well-defined. Symmetrically `k ≤ #b`." Then apply Prefix's component clause.

### OrdinalDisplacement

#### Justification of `n ≠ 0` miscites the axiom
**Class**: REVISE
**Issue**: The promotion step concludes "By NAT-order's irreflexivity, `n ≠ 0`" after deriving `0 < n`. Irreflexivity alone (`¬(n < n)`) does not yield `n ≠ 0` from `0 < n` — the conclusion requires either (a) NAT-order's disjointness axiom `(A m, n ∈ ℕ : m < n : m ≠ n)` applied at `(0, n)` giving `0 ≠ n`, hence `n ≠ 0` by symmetry of equality, or (b) a proof-by-contradiction spelled out as "assume `n = 0`; substituting into `0 < n` yields `0 < 0`, contradicting irreflexivity." Every other step in this claim is explicit about substitutions and axiom clauses; this step glosses a substitution/disjointness move behind a single-word citation to the wrong clause. A downstream consumer auditing the Depends slot against the prose would not find disjointness cited, and the reasoning as written does not land the conclusion from the cited clause alone.
**Required**: Rewrite the closing step to either (preferred) cite NAT-order's disjointness clause `(A m, n ∈ ℕ : m < n : m ≠ n)` at `(0, n)` to get `0 ≠ n`, then `n ≠ 0` by symmetry of `=`; or make the irreflexivity-plus-substitution contradiction explicit. The Depends bullet for NAT-order should mirror whichever clauses are actually invoked (disjointness, or irreflexivity + equality substitution).

VERDICT: REVISE

### T5

#### Missing dependency on T1 trichotomy postcondition
**Class**: REVISE
**Issue**: Subcases 1a and 1b close with "This contradicts `a ≤ b`" (resp. `b ≤ c`) after deriving `b < a` (resp. `c < b`). Since `a ≤ b` abbreviates `a < b ∨ a = b`, the contradiction needs T1's trichotomy postcondition — specifically `¬(a < b ∧ b < a)` and irreflexivity (to rule out `a = b ∧ b < a` which substitutes to `b < b`). The Depends list cites only "T1 case (i)" and "T1 case (ii)", which are Definition clauses, not the irreflexivity/trichotomy postconditions the contradictions rely on.
**Required**: Extend the T1 Depends entry (or add a line) to cite T1's irreflexivity and trichotomy postconditions — the (a) and (b) clauses that actually close the contradictions `a ≤ b ∧ b < a` and `b ≤ c ∧ c < b`.

#### Missing NAT-addcompat (or NAT-discrete) dependency
**Class**: REVISE
**Issue**: In Case 2, the proof writes "Case (ii) requires `#a < #b`, contradicting `#a > #b`." T1 case (ii) supplies `k = #a + 1 ≤ #b`. Moving from `#a + 1 ≤ #b` to `#a < #b` requires either NAT-addcompat's `n < n + 1` (combined with `≤`-clause and transitivity) or NAT-discrete's `m + 1 ≤ n ⟹ m < n`. Neither is listed in Depends, and NAT-order alone does not supply the successor inequality. The sibling step "`#a ≥ #p > #b`" similarly relies on NAT-order transitivity across `≤` and `<`, which is fine under NAT-order, but the successor step is not.
**Required**: Add NAT-addcompat (or NAT-discrete) to Depends and cite it at the `#a + 1 ≤ #b ⟹ #a < #b` step.

### TA4

#### Missing type declarations on bound variables
**Class**: REVISE
**Issue**: The claim statement `(A a, w : Pos(w) ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)` binds `a, w` with no type. Every symbol in the range (`Pos(w)`, `#a`, `aᵢ`, `⊕`, `⊖`) is defined only for elements of `T`, so without `a, w ∈ T` the predicate is ungrounded. Peer claims in this region use the explicit form (TA0 writes `(A a, w ∈ T : ...)`, TA-Pos writes `(A t ∈ T :: ...)`). The Formal Contract does list `a ∈ T, w ∈ T`, so the contract and the narrative statement disagree — checklist item 6 requires that disagreement be flagged as REVISE.
**Required**: Rewrite the bound-variable range to `(A a, w ∈ T : Pos(w) ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)` to match the Formal Contract preconditions and the typing the proof actually uses (T0-carrier membership when it invokes `aᵢ ∈ ℕ` at `k = #a`, TumblerAdd's `a, w ∈ T` precondition, etc.).

### T10a.2

#### Dependency mismatch with parent ASN; redundant pre-step inflates dependencies
**Class**: REVISE
**Issue**: T10a's roll-up for T10a.2 lists only `T10a, T10a.1, Prefix, T3` ("By T10a.1, all siblings have equal length; Prefix supplies the positional-agreement clause on the shorter tumbler's positions, and T3 collapses equal-length positional agreement to identity"). T10a.2's own contract additionally lists `TA5 (HierarchicalIncrement), (a)` and `T1 (LexicographicOrder), (a) irreflexivity, (c) transitivity`. These are present only because the proof opens with a "First, `tᵢ ≠ tⱼ`" detour that re-derives tumbler-distinctness from `i < j`. If the precondition "distinct siblings from the same allocator" already means `tᵢ ≠ tⱼ` as tumblers (the reading in T10a's *Domain* paragraph: "two distinct elements are *distinct siblings* of A", and matching T10a's roll-up `same_allocator(a, b) ∧ a ≠ b → ...`), the entire "First" paragraph is superfluous and TA5/T1 are not used by the actual contradiction step. If, instead, the parenthetical "(i ≠ j)" in the contract is the operative reading, then the proof requires enumeration injectivity (which is T10a.7) — but T10a.7 is not cited and inlining its argument here invites a depends-cycle risk for any future reuse.
**Required**: Pick one reading of the precondition and align the proof + contract. Either (a) state precondition as `tᵢ ≠ tⱼ` (distinct siblings as tumblers), delete the "First" paragraph, and drop TA5 and T1 from the depends list — matching T10a's roll-up; or (b) state precondition as `i ≠ j` and replace the inlined chain-and-irreflexivity derivation with a single citation of T10a.7, updating depends accordingly. Either way, the claim's *Depends* must agree with T10a's listed depends for T10a.2.

### T10a-N

#### Missing NAT-closure dependency
**Class**: REVISE
**Issue**: Step 2 concludes `k ≥ 1` from `k > 0` via "NAT-discrete (at `m = 0`, no `n` satisfies `0 ≤ n < 1` except `n = 0`)". The no-interval form of NAT-discrete at `m = 0` is `0 ≤ n < 0 + 1 ⟹ n = 0`. Reading `0 + 1` as the literal `1` requires NAT-closure's left-identity clause `0 + n = n` (instantiated at `n = 1`), and the symbol `1` itself comes from NAT-closure's `1 ∈ ℕ`. TA5's proof does exactly this rewrite and explicitly declares NAT-closure ("NAT-closure's left-identity clause `0 + n = n` … rewrites `0 + 1` to `1`"). T10a-N uses the same rewrite but omits NAT-closure from Depends.
**Required**: Add NAT-closure to the Depends list with justification: supplies `1 ∈ ℕ` and the left-identity `0 + 1 = 1` used to rewrite NAT-discrete's conclusion to `1 ≤ k`.

### T2

#### Missing NAT-addcompat dependency
**Class**: REVISE
**Issue**: Case 2 sub-cases (`m < n` and `n < m`) assert that "componentwise agreement at every `1 ≤ i ≤ m` is exactly agreement at every `1 ≤ i < k`" with `k = m + 1` (resp. `n + 1`). The "exactly" is an equivalence of index domains `{i : 1 ≤ i ≤ m} = {i : 1 ≤ i < m + 1}`. The forward direction `i ≤ m ⟹ i < m + 1` requires the strict successor inequality `m < m + 1`, which is supplied by **NAT-addcompat (NatAdditionOrderAndSuccessor)**. NAT-discrete's forward direction `m < n ⟹ m + 1 ≤ n` and its no-interval Consequence cover only the reverse direction `i < m + 1 ⟹ i ≤ m`; neither can produce `m < m + 1` without circularity. T1 itself declares NAT-addcompat for the same fact, but T2 does not, so the proof step linking the scan's agreement domain to T1 case (ii)'s witness requirement is ungrounded under the currently declared dependencies.
**Required**: Add NAT-addcompat (NatAdditionOrderAndSuccessor) to the *Depends:* list, with a note that it supplies `m < m + 1` (and symmetrically `n < n + 1`), used in Case 2 sub-cases `m < n` and `n < m` to identify the scan's agreement domain `{1 ≤ i ≤ m}` (resp. `{1 ≤ i ≤ n}`) with the `{1 ≤ i < k}` domain required by T1 case (ii) at `k = m + 1` (resp. `k = n + 1`). Cite NAT-addcompat inline at the two sub-case transitions where this domain identity is invoked.

VERDICT: REVISE

### T6

#### T3 mislabeled as "CanonicalRepresentation"
**Class**: REVISE
**Issue**: T6 refers to T3 as "CanonicalRepresentation" both in the claim's opening prose ("For any T3-canonical, T4-valid tumblers") and in the Depends list entry "T3 (CanonicalRepresentation)". The T3 supplied in the dependencies section is actually **T3 (SequenceEqualityIsComponentwise)** — an extensional equality axiom. There is no "CanonicalRepresentation" content in the provided T3.
**Required**: Rename to "T3 (SequenceEqualityIsComponentwise)" in every occurrence (both the Precondition prose and the Depends entry), and drop the "T3-canonical" phrasing. If the intent was to appeal to some other claim about canonicity, that claim must be cited by its actual label instead.

#### Role attributed to T3 does not match T3's axiom
**Class**: REVISE
**Issue**: The Depends entry says "T3 ... fixes component sequences so the four projections at `a` and `b` are uniquely determined." This is not what T3 does. Uniqueness of the four projections on a T4-valid tumbler is established by T4b (UniqueParse) directly, using T4 + T4a, not by T3. T3's actual axiom is `a = b ≡ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)` — extensional equality. T3's real role in T6 is Ingredient 3: the equivalence "sequences are equal iff lengths match and every position agrees" is the content Ingredient 3 appeals to when it invokes componentwise comparison for cases (a)–(c), and that role is never named in the Depends slot.
**Required**: Rewrite the T3 Depends entry to describe the actual role used in Ingredient 3 — namely, supplying the componentwise-equality characterisation of sequence equality used in cases (a), (b), (c).

#### "a, b satisfy T3" in Preconditions is incoherent
**Class**: REVISE
**Issue**: Preconditions read "`a, b ∈ T` satisfy T3 (CanonicalRepresentation) and T4 (HierarchicalParsing)." But T3 is a universal axiom about `=` on `T` — it holds for the whole carrier — not a per-tumbler property a specific `a, b` can "satisfy" or fail. Only T4-validity is a genuine per-tumbler precondition; T3 is vacuous in this slot (and the name is also wrong, as flagged above).
**Required**: State the preconditions as "`a, b ∈ T` are T4-valid" (i.e., `a, b ∈ dom(N)` in the sense of T4b). Move the T3 appeal to the Depends slot where it belongs, described as supplying extensional equality for the componentwise comparison in Ingredient 3.

### T7

#### Sub-case 2b pairwise matching assumes sorted order without justification
**Class**: REVISE
**Issue**: The proof writes the separator-position sets as `{α+1, α+β+2, α+β+γ+3}` and pairs the equations `α+1 = α'+1`, `α+β+2 = α'+β'+2`, `α+β+γ+3 = α'+β'+γ'+3` by "ascending pairwise matching." This requires showing `α+1 < α+β+2 < α+β+γ+3` (and likewise for primed), i.e. that `α+1` is the smallest, `α+β+2` the middle, `α+β+γ+3` the largest in each set. Given only `β ≥ 1` (from T4a) and the declared ℕ-axioms (NAT-order's strict total order; NAT-closure's closure and identity; NAT-cancel's cancellation; NAT-addassoc's associativity; NAT-discrete's `m<n ⟹ m+1≤n`), the inequality `α+1 < α+β+2` cannot be derived without monotonicity of `+` on ℕ — a fact equivalent to `c > 0 ⟹ a < a+c`, which is not among the declared clauses of any cited dependency. The proof's Depends entry for NAT-order asserts it "supplies ... the ascending pairwise matching of the separator-position sets via their canonical sorted enumerations," but NAT-order's axioms only posit strict total order; the bridge from "strict total order on ℕ" to "the particular enumeration `α+1, α+β+2, α+β+γ+3` is the sorted one" is the step that is not discharged.

Given T7's otherwise pedantic grounding of every numeral and typing step, this gap stands out: the matching step is load-bearing for the contradiction that drives sub-case 2b.
**Required**: Either (a) add an explicit short lemma (local or as a new NAT-* axiom/claim) that `n ∈ ℕ ∧ 0 < n ⟹ m < m+n`, cite it in Depends, and apply it at `n = β+1` and `n = γ+1` to establish the two strict inequalities, or (b) restructure sub-case 2b to avoid sorted-order pairing — e.g., argue that for the largest element `α+β+γ+3 ∈ S_a ∩ S_b`, case analysis on which of the three elements of `S_b` it equals, using NAT-cancel to rule out smaller matches, yields `α+β+γ+3 = α'+β'+γ'+3` without appealing to a pre-sorted enumeration.

### T8

#### Frame field misused as coverage statement
**Class**: REVISE
**Issue**: The `*Frame:*` entry reads "Holds for every operation in Σ, since NoDeallocation constrains the entire transition vocabulary." Per the checklist, Frame names what is preserved / not changed (e.g., "subspace identifier unchanged"). This text is instead a universal-quantification / coverage assertion — it restates that the invariant applies to all of Σ, not a preservation condition. The rubric's own example for a state invariant uses only `*Invariant:*` with no `*Frame:*`.
**Required**: Remove the `*Frame:*` entry, or replace it with a genuine frame condition (e.g., "membership in `allocated` is preserved: `a ∈ allocated(s) ⟹ a ∈ allocated(s')`"). Do not use Frame to encode coverage over Σ — that is already implicit in "for every transition s → s'" in the invariant.

#### Transitive postcondition not exported in contract
**Class**: REVISE
**Issue**: The narrative's claim is transitive — "If tumbler `a ∈ T` has been allocated at any point … then for all subsequent states, `a` remains in the set of allocated addresses" — and the proof explicitly performs induction to get `allocated(s₀) ⊆ allocated(sₙ)`. The formal contract, however, exports only the single-step invariant `allocated(s) ⊆ allocated(s')`. Downstream claims that cite T8 for "permanence" (a property over histories, not single steps) will have to re-derive the induction rather than cite a contracted postcondition. The contract narrows what the claim actually establishes.
**Required**: Add a transitive postcondition to the contract, e.g., `*Postcondition:* for every admissible transition sequence s₀ → s₁ → ⋯ → sₙ, `allocated(sᵢ) ⊆ allocated(sⱼ)` whenever `i ≤ j`; equivalently, once `a ∈ allocated(sᵢ)`, `a ∈ allocated(sⱼ)` for all `j ≥ i`." Keep the one-step invariant as the proof-carrying fact, but export the transitive form that matches the narrative.

VERDICT: REVISE

### TA-PosDom

#### Agreement-range mismatch in Case `#z < k`
**Class**: REVISE
**Issue**: In Case `#z < k`, the proof establishes agreement on the range `1 ≤ i ≤ #z`: "For `1 ≤ i ≤ #z`, `i < k`, so `tᵢ = 0` (by (ii)) and `zᵢ = 0` (from `Zero(z)`), giving `tᵢ = zᵢ`." But T1(ii)'s schema, instantiated with witness `k_T1 = #z + 1`, demands agreement on `(A i : 1 ≤ i < #z + 1 : zᵢ = tᵢ)`. The proof silently identifies these two ranges. The equivalence `i ≤ #z ⟺ i < #z + 1` on ℕ is true but requires NAT-discrete (and/or NAT-order's trichotomy) to bridge — exactly the kind of step the claim explicitly discharges elsewhere (the `1 ≤ #z + 1` derivation just below walks through four NAT clauses for a similarly "obvious" bound). Leaving this step implicit is structurally inconsistent with the rest of the proof and leaves the T1(ii) obligation incompletely discharged.
**Required**: Either (a) reformulate Case 2's agreement argument to range over `1 ≤ i < #z + 1` directly — e.g., note that any such `i` satisfies `i ≤ #z` (by NAT-order trichotomy at `(i, #z)`; if `#z < i`, NAT-discrete gives `#z + 1 ≤ i`, contradicting `i < #z + 1`), and then apply (ii) and Zero(z) — or (b) insert an explicit lemma step converting the `1 ≤ i ≤ #z` agreement to the `1 ≤ i < #z + 1` form required by T1(ii)'s schema, citing the NAT foundations already in Depends.

VERDICT: REVISE

### TA7a

#### TA6 declared as dependency but not consumed in proof
**Class**: REVISE
**Issue**: The Depends entry for TA6 states it "supplies the sentinel interpretation of `[0, ..., 0]` underlying **Z** and is cited by sub-claim TA7a.3". TA7a's own proof does not cite TA6 — neither its invalid-address postcondition (a) nor its strict-ordering postcondition (b) appears in any step of Conjunct 1 or Conjunct 2. "Underlying Z" is already handled by TA-Pos, which defines Z and is already in the depends list. The stated justification explicitly punts to a sub-claim.
**Required**: Remove TA6 from TA7a's Depends list; let TA7a.3 declare its own dependence on TA6. Alternatively, if TA6 is genuinely load-bearing here, rewrite the Depends entry to point to the specific TA6 postcondition consumed by a concrete proof step.

#### T4 declared as dependency but not consumed in proof
**Class**: REVISE
**Issue**: The Depends entry for T4 reads "anchors the element-field shape underlying **S**: each subspace corresponds to a well-parsed hierarchy position whose ordinal lives in **S**." This is motivation, not proof consumption. The set `S = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}` is defined purely in terms of T0's carrier and length operator; no field-separator, zero-count, or hierarchical-parsing postcondition of T4 is invoked in either conjunct's proof. The subspace identifier `N` is explicitly said not to "enter the arithmetic."
**Required**: Either remove T4 from Depends, or make the T4-consuming inference explicit in the proof (e.g., if `o ∈ S` is meant to entail some T4 field-structure fact, state and use that fact).

### TS3

#### Ungrounded literal `2` in the ordering chain
**Class**: REVISE
**Issue**: The Right-side paragraph derives `n₁ + n₂ ≥ 1` via the chain `n₁ + n₂ ≥ 1 + n₂ ≥ 2 ≥ 1`. The symbol `2` is not grounded by any declared (or reachable) dependency. NAT-closure posits `1 ∈ ℕ` only; neither `2` nor a `2 = 1 + 1` definition is introduced in NAT-closure, NAT-order, NAT-addcompat, or anywhere else cited. A downstream reader cannot discharge `1 + n₂ ≥ 2` or `2 ≥ 1` without first knowing what `2` denotes.
**Required**: Replace `2` with `1 + 1` throughout the chain: `n₁ + n₂ ≥ 1 + n₂ ≥ 1 + 1 ≥ 1`. Then the first step is NAT-addcompat right order-compatibility on `1 ≤ n₁`, the second is NAT-addcompat left order-compatibility on `1 ≤ n₂`, and the third unfolds NAT-addcompat's strict successor inequality `1 < 1 + 1` through NAT-order's defining clause `m ≤ n ⟺ m < n ∨ m = n`. No new dependency is required.

VERDICT: REVISE

### TS5

#### T1 missing from Depends
**Class**: REVISE
**Issue**: The proof's final substitution chain `shift(v, n₂) = shift(u, d) > u = shift(v, n₁)` concludes `shift(v, n₂) > shift(v, n₁)`, but the claim's postcondition is `shift(v, n₁) < shift(v, n₂)`. Converting between `>` and `<` on tumblers requires the definitional relation `a > b ⟺ b < a` on T, which is grounded by T1 (lexicographic ordering on tumblers) — not in the Depends list. The worked example also explicitly cites "T1's lexicographic ordering" to compare `[2, 3, 11] < [2, 3, 14]`, further confirming the dependency is used but undeclared.
**Required**: Add T1 (CanonicalOrdering / lexicographic ordering on T, whichever name applies) to Depends with a rationale citing both the `>`/`<` companion conversion at the proof's conclusion and the worked-example comparison. Alternatively, if another claim defines `>` on T as the converse of `<`, cite that claim.

VERDICT: REVISE

## OBSERVE

### ActionPoint

#### Implicit symmetry of equality when excluding `0 = w_{actionPoint(w)}`
**Class**: OBSERVE
**Issue**: NAT-zero yields `0 < w_{actionPoint(w)} ∨ 0 = w_{actionPoint(w)}`, and the derivation excludes the equality branch by citing `w_{actionPoint(w)} ≠ 0`. The move from `w_{actionPoint(w)} ≠ 0` to `¬(0 = w_{actionPoint(w)})` uses symmetry of equality silently. This is a standard logical property and does not affect soundness, but a reader tracking every symmetry step will notice the elision.

VERDICT: REVISE

### T0(a)

#### Informal "agrees with" in formal contract
**Class**: OBSERVE
**Issue**: The postcondition in the formal contract uses the phrase "agrees with t at all positions except i." None of the listed dependencies (T0, NAT-closure, NAT-addcompat) defines an "agrees-with" relation on T. The proof body unfolds it to "t'ⱼ = tⱼ for j ≠ i," so the meaning is recoverable, but the formal contract itself leans on undefined English phrasing rather than a component-wise equation.

#### Symbol `>` used without grounding
**Class**: OBSERVE
**Issue**: The proof's step (iii) concludes `t'.dᵢ = M + 1`, and `M + 1 > M`, and the postcondition states `t'.dᵢ > M`. NAT-addcompat establishes the primitive strict inequality as `n < n + 1`; the symbol `>` is not explicitly declared as `b > a ≡ a < b` in any cited dependency. Standard convention, but a Dijkstra-style reader notes the unannounced symbol swap.

#### Notational drift between `aᵢ` and `t'.dᵢ`
**Class**: OBSERVE
**Issue**: T0 posits component projection as `aᵢ` (subscript). The claim and postcondition write `t'.dᵢ`, mixing the local display name `dᵢ` (valid for the specific `t = d₁.d₂. ... .dₙ`) with the projection operator. For the witness `t'`, the clean projection is `t'ᵢ`; writing `t'.dᵢ` treats `dᵢ` as a slot name, which is not a convention T0 introduces.

VERDICT: OBSERVE

### T4

#### Per-`k` schema does not state minimum segment lengths
**Class**: OBSERVE
**Issue**: The Axiom's per-`k` schemas write `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . ...` but never assert `a ≥ 1, β ≥ 1, γ ≥ 1, δ ≥ 1`. These bounds follow from the field-segment constraint (`t₁ ≠ 0`, `t_{#t} ≠ 0`, no adjacent zeros) together with `zeros(t) = k`, but the schema leaves them implicit. A reader could read `N₁. ... .Nₐ` as permitting `a = 0` (an empty leading segment), which would silently violate `t₁ ≠ 0` at `k ≥ 1`. The constraint forces nonemptiness, so soundness is not at risk; the schema is just understated.

VERDICT: REVISE

### NAT-sub

#### Loose "unique natural number" phrasing overstates what the axioms establish
**Class**: OBSERVE
**Issue**: The opening sentence states that `m − n` is "the unique natural number characterised by `(m − n) + n = m`." The narrative immediately below explains this uniqueness is "established by positing `−` as a function rather than by derivation from right-cancellation of `+`, which no NAT foundation declares." But function-positing only delivers single-valuedness of the output `m − n`; it does not establish the stronger fact that `m − n` is the *only* `k ∈ ℕ` satisfying `k + n = m`. That stronger reading would require right-cancellation, which — as the narrative itself notes — is not declared. The formal contract lists neither uniqueness-of-solution nor right-cancellation, so the contract is sound; the opening sentence's natural-language "the unique natural number characterised by" could be read as asserting the stronger (undischarged) claim. A downstream reader citing the opening sentence risks importing a guarantee the contract does not back.

VERDICT: OBSERVE

### T4a

#### Superfluous use of T4's Exhaustion Consequence
**Class**: OBSERVE
**Issue**: The proof states "`k = zeros(t) ∈ {0, 1, 2, 3}`", invoking T4's Exhaustion Consequence. But the body only branches on `k = 0` vs `k ≥ 1` and derives `k + 1` segments parametrically — it uses only the bound `zeros(t) ≤ 3` (indeed, it uses only `zeros(t) ∈ ℕ` in most places). The explicit enumeration into `{0, 1, 2, 3}` is decorative here.

#### Unstated well-definedness for `s₁ − 1`, `s_{i+1} − 1`
**Class**: OBSERVE
**Issue**: The segment expressions `t[1 .. s₁ − 1]` and `t[s_i + 1 .. s_{i+1} − 1]` implicitly require `s₁ − 1 ∈ ℕ` and `s_{i+1} − 1 ∈ ℕ`. The narrative grounds only `#t − 1 ∈ ℕ` via NAT-sub conditional closure. The argument is recoverable (each `s_j ≥ 1` as an index, so NAT-sub applies), but the claim elevates the `#t − 1` grounding to a named step while leaving the structurally identical `s_j − 1` groundings implicit.

VERDICT: REVISE

### TA5-SigValid

#### Redundant strict-positivity detour
**Class**: OBSERVE
**Issue**: The proof derives `0 < t_{#t}` from T4's `t_{#t} ≠ 0` via NAT-zero's disjunction, then uses `t_{#t} > 0` to trigger TA5-SIG. But TA5-SIG's "maximum-position" branch is triggered by the existential `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`, which is witnessed directly at `i = #t` by T4's `t_{#t} ≠ 0` together with `1 ≤ #t ≤ #t`. The strict-positivity step does no work — it reaches `t_{#t} ≠ 0` back again via disjointness. The NAT-zero dependency is accordingly gratuitous and could be dropped along with the detour.

#### TA5-SIG trigger misstated in Depends
**Class**: OBSERVE
**Issue**: The Depends entry for TA5-SIG says it "unfolds `sig(t)` as the maximum-position formula when `t_{#t} > 0`". TA5-SIG's actual trigger (per its Definition) is the existential `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)` — i.e., any nonzero component anywhere, not specifically the last one. The proof's hypothesis at `i = #t` is one witness, but the Depends line inlines that instantiation into what TA5-SIG itself exports and thus slightly misdescribes the cited contract.

VERDICT: OBSERVE

### T1

#### Case 3 branch selection is elliptical
**Class**: OBSERVE
**Issue**: In Case 3 of Trichotomy, after establishing `m ≠ n` and invoking NAT-order's trichotomy to obtain `m < n ∨ n < m`, the proof immediately writes "If `m < n`, then `k = m + 1 ≤ n`" without spelling out that this branch corresponds exclusively to clause (β). The link is recoverable — clause (γ) would have given `n < m`, contradicting `m < n` — but the reasoning step is implicit. Invoking trichotomy here is also redundant, since (β) directly yields `m < n` and (γ) directly yields `n < m`; a case split on which clause the first divergence position satisfies would have been more direct than going through trichotomy on `(m, n)`.

VERDICT: OBSERVE

### TA5a

#### Formal Contract field naming
**Class**: OBSERVE
**Issue**: The contract uses non-standard field names "Guarantee" and "Failure" in place of "Postconditions". Peer claims (TA5, TA5-SigValid) state analogous iff/conditional preservation results under "Postconditions". The content is correct; only the field label diverges from the convention followed by adjacent claims in the same proof chain.

#### NAT-discrete declared but not load-bearing
**Class**: OBSERVE
**Issue**: The preamble cites "NAT-discrete instantiated at m = 0" to underwrite "non-zero ⇒ strictly positive," and the Depends entry repeats this role. But no subsequent proof step actually needs the sharpened form `1 ≤ n` — every argument uses either `n ≥ 0` (from NAT-zero) or `n ≠ 0` (from T4(iv)/construction). The NAT-zero disjunction `0 < n ∨ 0 = n`, with the equality branch excluded, already yields `0 < n` without invoking NAT-discrete. Declaring NAT-discrete is not harmful, but its stated role is redundant.

#### T4a detour in case k ≥ 3 is avoidable
**Class**: OBSERVE
**Issue**: The k ≥ 3 argument routes through a counterfactual "suppose T4 holds on t', so zeros(t') ≤ 3, so t' ∈ T4a's domain, apply T4a's Reverse-contrapositive to identify the empty interior field segment [#t+2, #t+1], conclude T4(ii) fails at i = #t+1." The same conclusion follows directly and more simply: t'_{#t+1} = 0 and t'_{#t+2} = 0 are both immediate from TA5(d) once k-1 ≥ 2 is established (for which the NAT-sub derivation already in the proof suffices), and T4(ii) at i = #t+1 (in range because #t+1 < #t+k = #t') fails on inspection. The T4a framing is not wrong, but it adds conceptual machinery (field-segment Reverse-contrapositive, segment-as-index-range) that the argument does not actually need, and pulls T4a into the dependency list for a purely ornamental use.

#### Implicit transfer of T4(ii) on original positions
**Class**: OBSERVE
**Issue**: In cases k = 0, 1, 2, the proof checks T4(ii) only at the boundary/modified positions (left-flank #t, right-flank #t+1 or #t+2) and remarks "No new adjacencies arise" or similar. The transfer of T4(ii) for t' at indices 1 ≤ i < #t — which follows from TA5(b) agreement on original positions plus T4(ii) on t — is left implicit rather than stated. A one-sentence acknowledgement ("for 1 ≤ i < #t, t'ᵢ = tᵢ and t'ᵢ₊₁ = tᵢ₊₁ by TA5(b), so T4(ii) on t discharges the original-range adjacency clause for t'") would close the micro-gap. Not a correctness failure — the inference is mechanical — but the current phrasing under-specifies the argument.

VERDICT: OBSERVE

### T10a.7

#### Postcondition "Equivalently" misstates a strict implication as an equivalence
**Class**: OBSERVE
**Issue**: The Postcondition reads: "The map `n ↦ tₙ` is injective: `(A m, n ≥ 0 : m ≠ n : tₘ ≠ tₙ)`. Equivalently, `(A m, n ≥ 0 : m < n : tₘ < tₙ)`." These two formulas are not logically equivalent. The strict-monotonicity form implies injectivity (via trichotomy plus T1(a) irreflexivity), but injectivity alone does not constrain the direction of the inequality between `tₘ` and `tₙ`, so it cannot recover strict monotonicity. The proof does establish the stronger strict-monotonicity form (lemma L plus the closing rewrite delivers `tₘ < tₙ` whenever `m < n`), so the postcondition is correct as a *conjunction* of the two — "the map is injective, and in fact strictly monotone" — but not as an equivalence. A downstream consumer citing "T10a.7's equivalent monotone form" from an injectivity-only statement would be citing an unjustified inference.

VERDICT: OBSERVE

### T10a.3

#### Implicit associativity/commutativity of addition
**Class**: OBSERVE
**Issue**: The local-monotonicity step applies NAT-sub right-telescoping `(m + n) − n = m` at `m = k'_{d_A+1} + … + k'_{d_B}`, `n = γ + k'₁ + … + k'_{d_A}` and concludes `#output(B) − #output(A) = k'_{d_A+1} + … + k'_{d_B}`. This equality requires the regrouping `γ + k'₁ + … + k'_{d_B} = (γ + k'₁ + … + k'_{d_A}) + (k'_{d_A+1} + … + k'_{d_B})`, i.e., associativity of `+` on ℕ, which no declared dependency exposes explicitly. Similar running-sum manipulations appear in the induction. This appears to be a systemic implicit assumption across the ASN rather than a T10a.3-specific gap, so logged as OBSERVE.

#### "`1 ≤ k'`" used without derivation
**Class**: OBSERVE
**Issue**: The paragraph establishing `#c₀ = γ + k' > γ` asserts "Since `1 ≤ k'`" without citing how this follows from `k' ∈ {1, 2}`. T10a's Consequence 3 spelled out "NAT-zero with NAT-discrete at `m = 0` sharpens `k' > 0` to `1 ≤ k'`" — the same derivation is elided here. Not a correctness gap (the inequality is trivially true), but the citation pattern is inconsistent with the otherwise-explicit NAT-* bookkeeping in this claim.

VERDICT: REVISE

### T9

#### "Same argument applies within each child allocator" is trivial commentary, not part of the proof
**Class**: OBSERVE
**Issue**: The closing line "The same argument applies within each child allocator's domain starting from its base `c₀ = inc(t, k')`" adds nothing: the proof body never specialised to the root, so it already covers every `A ∈ 𝒯` once `t₀` is taken to be `A`'s base. As written it suggests an additional case obligation that does not exist.
**Required**: (omit — observation only)

VERDICT: REVISE

### AllocatedSet

#### Inclusion (i) and initial-segment structure (ii) over-qualified with "reachable s"
**Class**: OBSERVE
**Issue**: Postconditions (i) and (ii) require "for every reachable s and every activated A". But the facts follow from the definition of `domₛ(A)` alone: since `domₛ(A) = {t₀, …, t_{nₛ(A)}}` with tᵢ generated by the same `inc(·, 0)` chain as T10a's `dom(A)`, the inclusion and initial-segment structure hold on every state `s ∈ 𝒮` where A is activated, reachability irrelevant. The qualifier is needed only for (iii)'s claim about the aggregate `⋃ {domₛ(A) : s reachable}`. Pointwise inclusion/structure do not depend on reachability.

#### Dependencies T0(a) and T0(b) declared but not invoked in the claim's reasoning
**Class**: OBSERVE
**Issue**: The Depends entries cite T0(a) ("underwriting the inexhaustibility of the sibling inc(·,0) chain") and T0(b) ("allocator nesting via deep increments is not capped"). Neither property is explicitly invoked in the narrative, proof sketches, or postcondition derivations. The claim relies on T10a for the enumeration `dom(A) = {tₙ : n ≥ 0}` and on TA5 (via T10a) for increment behavior; unboundedness of component values and of length is background context, not a lemma used here.

VERDICT: REVISE

### Divergence

#### Exhaustiveness step from ¬(case i) to "all shared components agree" leaves NAT-wellorder implicit
**Class**: OBSERVE
**Issue**: Exhaustiveness argues "if neither case applies, all shared components agree and `#a = #b`, so by T3, `a = b`." The step from ¬(case i) to "all shared components agree" silently uses NAT-wellorder: any shared mismatch would, via least-element, supply a witness satisfying case (i)'s conjunction (prior-agreement discharged by minimality). The dependency is declared, but the inference is not spelled out at the point of use.

VERDICT: REVISE

### TumblerSub

#### Undefined-zpd branch missing from Postconditions
**Class**: OBSERVE
**Issue**: The Postconditions bullet states `a ⊖ w ∈ T`, `#(a ⊖ w) = L`, and the conditional Pos/actionPoint pair "when zpd(a, w) is defined". It is silent on the defining guarantee of the other branch, `Zero(a ⊖ w)` when zpd is undefined — which the narrative makes explicit and which downstream claims are likely to cite. The fact is recoverable from the Definition, but collecting it as a dedicated postcondition would make the contract exhaustive over the cases.

VERDICT: REVISE

### D1

#### T1 witness identified with divergence(a, b) implicitly
**Class**: OBSERVE
**Issue**: The proof asserts "We are in case (i): aᵢ = bᵢ for i < k, and aₖ < bₖ (by T1)." T1 case (i) provides `aₖ' < bₖ'` at some witness index k' for `a < b`, not automatically at `k = divergence(a, b)`. The identification `k' = k` rests on both being the least divergence index (requires Divergence's uniqueness together with the elimination of T1 case (ii) against Divergence case (i)'s `aₖ ≠ bₖ` at `k ≤ #a`). The proof elides this uniqueness step.

#### Equality-disjunct sentence is unclear
**Class**: OBSERVE
**Issue**: "The case-hypothesis #a ≠ #b excludes the equality disjunct." It is not clear which disjunction is being restricted — Divergence case (ii) already carries `#a ≠ #b` as its premise, and sub-cases (ii-a)/(ii-b) exhaust that case via NAT-order trichotomy. The sentence reads as orphan commentary and can be removed or reformulated.

#### Pos(w) derivation elides range check
**Class**: OBSERVE
**Issue**: The proof asserts "Pos(w): wₖ ≥ 1 by NAT-sub strict positivity (precondition bₖ > aₖ)." Pos(w) requires exhibiting an `i ∈ [1, #w]` with `wᵢ ≠ 0`; `wₖ ≥ 1` alone does not discharge this — the bounds `1 ≤ k ≤ #w = #b` are available (from Divergence output and `k ≤ #a ≤ #b`) but not stated. TumblerSub's conditional postcondition Pos(a ⊖ w) could be cited directly, matching the already-cited `actionPoint(w) = zpd(b, a)` as a sibling conditional postcondition.

VERDICT: OBSERVE

### T10

#### Case split on `m ≤ n` vs `m > n` relies on trichotomy as Consequence, not axiom
**Class**: OBSERVE
**Issue**: The case split `m ≤ n` vs `m > n` uses exactly-one trichotomy on ℕ, which NAT-order exports as a *Consequence*, not directly as an axiom clause. The dependency citation "trichotomy and transitivity of `≤` on ℕ" is informal and conflates `<` trichotomy (the axiom/consequence) with `≤` partition. This is sound — `m > n ≡ ¬(m ≤ n)` follows from NAT-order's definitions plus exactly-one trichotomy — but the citation could be sharper.

#### Nonemptiness of the set used for `min` is implicit
**Class**: OBSERVE
**Issue**: `k = min{j : 1 ≤ j ≤ ℓ ∧ p₁ⱼ ≠ p₂ⱼ}` invokes NAT-wellorder, which requires a nonempty subset of ℕ. The nonemptiness is established by the case analysis (Case 1 yields `j ≤ m = ℓ`; Case 2 yields `j ≤ n = ℓ`), but the proof never says "hence the set is nonempty, so NAT-wellorder applies." A one-line acknowledgment would remove the gap between the cases and the `min` invocation.

VERDICT: REVISE

### NoDeallocation

#### NoDeallocation is entailed by AllocatedSet's admissibility axiom
**Class**: OBSERVE
**Issue**: The claim is labeled "an axiom" ("This is a design constraint accepted as an axiom"), but AllocatedSet's admissibility axiom already enumerates Σ's transition shapes (T1)/(T2)/(T3) exhaustively, and each shape entails `allocated(s) ⊆ allocated(s')`: (T1) extends `domₛ(A)` by `t_{nₛ(A)+1}` while leaving other domains and Act fixed; (T2) extends Act by a new A with `domₛ'(A) = {t₀}` while leaving prior domains fixed; (T3) is fully framed by AllocatedSet. So the inclusion is a theorem under AllocatedSet, not an independent axiom. The claim is sound either way (the conclusion holds), but the "axiom" framing hides the derivation and a downstream reader cannot tell whether NoDeallocation adds primitive content or merely names a consequence. A short note tying the axiom to the three-shape admissibility — or restating it as a derived contract — would resolve the ambiguity without changing the exported `allocated(s) ⊆ allocated(op(s))` guarantee.

#### Nelson quote motivates more than NoDeallocation guarantees
**Class**: OBSERVE
**Issue**: The Nelson quote on "permanent tumbler address" motivates address *permanence* — once t is allocated to A it remains so, and its meaning does not shift. NoDeallocation alone gives only that t is never removed from the allocated set; address-to-allocator stability and uniqueness require additional facts (T10a's at-most-once spawning, same_allocator). The motivational paragraph reads as if NoDeallocation discharges the permanence guarantee, when it discharges only the "ever-growing" half.

VERDICT: OBSERVE

### OrdinalShift

#### Minor phrasing: T0 length axiom restated as ≥
**Class**: OBSERVE
**Issue**: The derivation cites "T0's length axiom `#a ≥ 1`", but T0's actual axiom clause is `(A a ∈ T :: 1 ≤ #a)`. The equivalence `#a ≥ 1 ⟺ 1 ≤ #a` holds via NAT-order's `≥` definition (which is declared in depends), so the substance is grounded, but the cited phrasing differs from what T0's formal contract literally asserts.

#### Implicit reflexivity of ≤
**Class**: OBSERVE
**Issue**: Step (iv) of the TA0 discharge argues "actionPoint(δ(n, m)) = m = #v, so actionPoint(δ(n, m)) ≤ #v". The step silently uses reflexivity of ≤ (derivable from NAT-order's defining clause by selecting the `m = n` disjunct). NAT-order is in depends, so the inference is grounded, but the unfolding is left to the reader.

#### Component postcondition index range implicit
**Class**: OBSERVE
**Issue**: The postcondition `shift(v, n)ᵢ = vᵢ for i < #v` omits an explicit lower bound on i. Since T0 types the index domain as `{1, …, #shift(v,n)} = {1, …, #v}`, the range `1 ≤ i < #v` is implicit and vacuous when `#v = 1`. No soundness gap, but a stricter reading would spell out `1 ≤ i < #v`.

VERDICT: OBSERVE

### T5

#### Redundant `#p ≥ 1` in preconditions
**Class**: OBSERVE
**Issue**: The preconditions say "`p` is a tumbler prefix with `#p ≥ 1`." Since `p ∈ T` and T0 defines T as nonempty finite sequences, `#p ≥ 1` is automatic. The narrative's "Let `p` be a tumbler prefix with `#p ≥ 1`" carries the same redundancy.

VERDICT: REVISE

### TA4

#### Case 2 concludes equality without citing T3
**Class**: OBSERVE
**Issue**: In Case 2 the proof writes "this is `a`" after deriving that TumblerSub returns the zero tumbler of length `k` and that `a = [0, …, 0]` of length `k` by precondition + case. The conclusion is sequence equality of two componentwise-identical, equal-length tumblers, which is exactly T3's job — T3 is cited for the analogous step in Case 1 (`s = [0, ..., 0, aₖ] of length k, which by T3 ... equals a`) but left implicit in Case 2. Not a soundness gap (T3 is already declared), just asymmetric citation.

VERDICT: REVISE

### ReverseInverse

#### NAT-cancel citation imprecise
**Class**: OBSERVE
**Issue**: In the "Promote to `yₖ + wₖ > wₖ`" chain, the proof cites "NAT-cancel's summand absorption" to rule out the equality disjunct `yₖ + wₖ = wₖ`. NAT-cancel's axiom clause reads `m + n = m ⟹ n = 0`, which would match `yₖ + wₖ = yₖ`, not `yₖ + wₖ = wₖ`. The equation at hand requires the *mirror* form `n + m = m ⟹ n = 0`, which NAT-cancel's body explicitly calls a theorem (not a clause) derivable with NAT-closure. Precedent in TA4 and TumblerAdd says "symmetric summand absorption" or gives the mirror form explicitly; this proof drops the qualifier.

#### Strict-positivity undercount
**Class**: OBSERVE
**Issue**: In Y3b, "`yₖ = aₖ − wₖ > 0` (by NAT-sub's conditional closure and strict-positivity clauses)" — NAT-sub's strict-positivity clause yields `aₖ − wₖ ≥ 1`, not `> 0`. The bridge `≥ 1 ⟹ > 0` rests on `1 > 0` (derivable via NAT-addcompat's strict successor inequality at `n = 0` plus NAT-closure's additive identity), which is not from NAT-sub. Minor informality; TumblerSub is more careful, stating `≥ 1` verbatim.

#### Implicit `≠ 0 ⟹ > 0` step
**Class**: OBSERVE
**Issue**: Closing the `yₖ > 0` subproof, "Hence `yₖ > 0`" is inferred after both branches under the `yₖ = 0` hypothetical produce contradictions. The inference from `yₖ ≠ 0` (together with `yₖ ∈ ℕ`) to `yₖ > 0` uses NAT-zero's disjunction `0 < n ∨ 0 = n` to exclude the equality disjunct. NAT-zero is already declared, but the step is left silent; other proofs in this ASN spell it out.

#### Equality-branch handling structurally awkward
**Class**: OBSERVE
**Issue**: When the Step-1 split gives the equality branch (`aₖ = wₖ`), `a = w` follows directly by T3 and `(a ⊖ w) ⊕ w = (zero) ⊕ w = w = a` discharges the goal without any contradiction argument. The current proof folds this branch into the `yₖ > 0` subproof within the contradiction-by-assumption `y ⊕ w ≠ a`, which is formally valid but hides the easy case behind the harder one. A cleaner structure would dispatch the equality branch once in Step 1.

VERDICT: OBSERVE

### T10a.2

#### Unjustified WLOG `i < j`
**Class**: OBSERVE
**Issue**: The proof opens "Let `tᵢ` and `tⱼ` be distinct siblings from the same allocator with `i < j`." Reducing the symmetric statement `i ≠ j` to the case `i < j` uses NAT-order trichotomy on indices, which is unstated and uncited. The closing "The symmetric argument excludes `tⱼ ≼ tᵢ`" relies on the same symmetry but is invoked only at the end. A one-line WLOG justification (or NAT-order citation) would make the reduction explicit; without it the index ordering appears chosen arbitrarily.

VERDICT: REVISE

### T10a-N

#### Redundant NAT-zero invocation in Step 2
**Class**: OBSERVE
**Issue**: Step 2 cites "NAT-zero (`0 ≤ k`)" alongside the stronger hypothesis `k > 0`. The axiom form of NAT-discrete (`m < n ⟹ m + 1 ≤ n`) applies directly to `0 < k` and yields `0 + 1 ≤ k` in a single step, making the detour through the no-interval consequence form plus NAT-zero unnecessary. The reasoning is sound either way, but the cited form is more indirect than needed.

#### Step 5 citation is underspecified
**Class**: OBSERVE
**Issue**: Step 5 writes "From (3), (4) by NAT-order (`m ≤ n ⟺ m < n ∨ m = n`), conclude `#t₁ < #t₁ + k = #t₂`." Chaining `#t₁ < #t₁ + 1` with `#t₁ + 1 ≤ #t₁ + k` uses the ≤-unfolding disjunction plus NAT-order's transitivity (on the `<` branch) and substitution of equality (on the `=` branch). Citing only the ≤-definition clause understates what is invoked; transitivity is part of what makes the chain go through.

VERDICT: REVISE

### T4b

#### NAT-discrete citation redundant for strict positivity
**Class**: OBSERVE
**Issue**: T4b argues "every component strictly positive by NAT-zero and NAT-discrete at `m = 0`" for placing projection images in the `ℕ⁺`-component subset. T4 defines `ℕ⁺ = {n ∈ ℕ : 0 < n}`, and NAT-zero alone — instantiated at a non-separator `tᵢ`, excluding the `0 = tᵢ` branch via `tᵢ ≠ 0` — already yields `0 < tᵢ`, which is precisely `ℕ⁺` membership. NAT-discrete at `m = 0` merely converts `0 < tᵢ` to `1 ≤ tᵢ` (an equivalent form of the same predicate). T4's own derivation of `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` at non-separator positions cites only NAT-zero. The citation is sound but the NAT-discrete appeal here carries no load that NAT-zero has not already discharged; the Depends rationale for NAT-discrete ("promotes non-zero components to strictly positive") misattributes work done by NAT-zero.

#### Uniqueness argument compresses enumeration-uniqueness step
**Class**: OBSERVE
**Issue**: The uniqueness paragraph reads "Two distinct decompositions would require two distinct separator sets; there is exactly one." This is correct when read at the level of the separator *set* `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}` (uniquely determined by `t` via T0's component projection), but the projections `N, U, D, E` are defined through the strictly increasing *enumeration* `s₁ < … < s_k` supplied by NAT-card. NAT-card's axiom posits existence of an enumeration and selects a single `k`, but explicitly declines to derive uniqueness of the enumeration's elements (it lacks the induction/well-foundedness to do so). The claim implicitly assumes that any two strictly increasing enumerations of the same separator set coincide element-wise — which is true but not supplied by NAT-card in isolation. The argument succeeds at the level the claim operates but could be tightened by noting that the per-`k` case-analysis values `(t₁, …, t_{s₁-1})` etc. are functions of the *set* (`min`, `next`, …) rather than of a chosen enumeration, or by explicitly stating that the enumeration of a separator set is unique as a standing convention.

#### "Local unpacking" of `#t ≥ 1` already a direct T0 clause
**Class**: OBSERVE
**Issue**: T4b writes "by the definition of length `#t ≥ 1` — this is a local unpacking performed here, not a postcondition cited from T0." T0's Formal Contract's Axiom clause states `T is the set of finite sequences a over ℕ satisfying 1 ≤ #a`, so `#t ≥ 1` is directly posited by T0's Axiom rather than being something T4b re-derives. The qualification is sound but misleading about provenance; the simpler reading — "`#t ≥ 1` by T0" — would match T0's actual contract. The phrasing appears identically in T4a and appears to be a shared stylistic convention rather than a substantive derivation.

VERDICT: OBSERVE

### T4c

#### Exhaustion duplicates T4's Consequence
**Class**: OBSERVE
**Issue**: T4 already exports `zeros(t) ∈ {0, 1, 2, 3}` as a Consequence of its formal contract, with the same iterated trichotomy+NAT-discrete argument T4c reproduces verbatim. T4c's Exhaustion section is a self-contained re-derivation rather than a citation. The Depends entry for T4 says "supplies the T4-valid subdomain constraints, used in exhaustion" — invoking only T4's Axiom, not its exported Consequence — so the exhaustion work is done twice in the ASN. Sound as written; just a framing choice that inflates the proof.

VERDICT: OBSERVE

### T6

#### Ingredient 3 termination bound loosely stated
**Class**: OBSERVE
**Issue**: Ingredient 3 says the componentwise-equality procedure "terminates in at most `m + 1` steps", where `m` is the length of the left sequence. When `m ≠ n` the procedure terminates after the single length comparison, so the bound is actually `min(m, n) + 1`. The stated `m + 1` is a valid upper bound, just slack — and it also tacitly privileges the left length over the right. Not a soundness issue, but the asymmetry reads oddly.

VERDICT: REVISE

### T7

#### T1 reference after the Formal Contract lacks a declared dependency
**Class**: OBSERVE
**Issue**: The trailing paragraph "The ordering T1 places all text addresses (subspace 1) before all link addresses (subspace 2)..." cites T1 but T1 is not in Depends. This paragraph appears to be commentary motivating downstream use rather than part of the claim's proof, so it does not affect T7's soundness. If the paragraph is intended as an exported observation it should either cite T1 formally or be removed; if commentary, it reads unambiguously as such.

VERDICT: REVISE

### TA-assoc

#### T1 dependency justification is strained
**Class**: OBSERVE
**Issue**: The depends entry for T1 reads: "TumblerAdd's contract, consumed by this proof, is interpretable only with T1 in scope." The parts of TumblerAdd's contract actually consumed by this proof — the piecewise definition `rᵢ = aᵢ / aₖ+wₖ / wᵢ`, membership `a⊕w ∈ T`, and the length identity `#(a⊕w) = #w` — do not reference T1's order; they are typed in T0 and ℕ. T1 underwrites only the strict-advancement and dominance postconditions of TumblerAdd (`a⊕w > a`, `a⊕w ≥ w`), neither of which this proof invokes. The listing is defensible as "TumblerAdd's full contract rests on T1 transitively," but the narrative rationale overstates what this proof itself needs.

#### Lift from `≥ 1` to `> 0` citation is incomplete
**Class**: OBSERVE
**Issue**: At three sub-cases the proof lifts `b_{k_b} ≥ 1` (or `c_{k_c} ≥ 1`) to strict `> 0` with the citation "NAT-zero plus NAT-order's `m ≤ n ⟺ m < n ∨ m = n`." Those two alone do not close the step. From `1 ≤ b_{k_b}` and NAT-zero's `0 < b_{k_b} ∨ 0 = b_{k_b}`, the branch `0 = b_{k_b}` reduces to `1 = 0` after using `¬(1 < 0)` on `1 ≤ 0`; NAT-zero + NAT-order alone do not contradict `1 = 0` — distinguishing `0` from `1` requires NAT-addcompat's strict successor `0 < 0+1` together with NAT-closure's left identity `0+1 = 1`. NAT-addcompat and NAT-closure are both in the Depends list, so the proof is sound in aggregate, but the inline citation undershoots the toolkit used. A tidier form would cite ActionPoint's set-membership fact `w_{actionPoint(w)} ≠ 0` (from the defining set `S = {i : … ∧ wᵢ ≠ 0}`) directly, after which NAT-zero's disjunction plus exclusion of `0 = b_{k_b}` by `≠ 0` closes without needing `0 < 1`.

VERDICT: OBSERVE

### TA7a

#### Tail-positivity precondition includes redundant lower bound
**Class**: OBSERVE
**Issue**: The ⊕-precondition states `(A i : k ≤ i ≤ #w : wᵢ > 0)`. The claim itself says the proof uses this precondition "restricted to its upper sub-range" (i.e., `k < i ≤ #w`), since at `i = k` the postcondition `wₖ ≥ 1` is already delivered by ActionPoint's minimum-value clause under `Pos(w)`. The `i = k` instance is therefore strictly redundant. The narrative advertises the preconditions as "tight enough"; the looser lower bound is cosmetic rather than load-bearing.

#### `o ≥ w` precondition in Conjunct 2 is derivable from `o₁ > w₁`
**Class**: OBSERVE
**Issue**: The ⊖-precondition lists both `o ≥ w` and `o₁ > w₁`. Given `o, w ∈ T` (so `#o, #w ≥ 1` by T0) and `o₁ > w₁`, T1 case (i) at divergence position 1 yields `w < o`, hence `o ≥ w`. The `o ≥ w` precondition is therefore redundant against the conjunction of the other preconditions. Not a soundness issue, but asymmetric with the "preconditions tight" framing.

VERDICT: REVISE

### TS1

#### Implicit discharge of OrdinalDisplacement's preconditions
**Class**: OBSERVE
**Issue**: The proof cites "δ(n, m) ∈ T — OrdinalDisplacement postcondition" (and likewise for Pos and actionPoint) without explicitly discharging OrdinalDisplacement's preconditions (n ∈ ℕ, m ∈ ℕ, n ≥ 1, m ≥ 1). In particular, `m ∈ ℕ` and `m ≥ 1` at `m = #v₁` rely on T0's length typing and T0's length axiom `(A a ∈ T :: 1 ≤ #a)`. These are established transitively via the invocation of OrdinalShift, so the proof is sound, but the step is left silent. A one-line note ("where m ∈ ℕ by T0's length typing and m ≥ 1 by T0's length axiom applied at v₁") would align this invocation with the discharge-style used elsewhere in the proof.

VERDICT: OBSERVE

28 verified, 53 observed, 37 found.
