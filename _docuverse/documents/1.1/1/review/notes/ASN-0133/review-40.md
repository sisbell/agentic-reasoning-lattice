# Review of ASN-0133

This is a logically careful note — I verified the Q0 view-rebuild completeness, the Q3 dedup/audit-slice argument, Q-EXT, the Q5/Q5a separation, the H-SFAIR regime-form derivation, and the Q6 case taxonomy, and they hold up. The findings below are a correctness error in the worked verification, an unproven assertion, and (per the anti-bloat classifier) accreted meta-prose.

## REVISE

### Issue 1: Single-target removal cannot make the producer's half "unreached"

**ASN-0133, Worked composition, "A reached terminal state" (final parenthetical)**: "Had the environment instead unflagged t between Σ₀ and ρ_P's scheduled fire, t would leave [D_{ρ_P}] — H-FAIR's removal escape — and ρ_P's half could go unreached: the non-grow-only producer's one environment hypothesis, made concrete."

**Problem**: This contradicts the note's own case taxonomy (Q6). The example has a *single* target `t`, so `[D_{ρ_P}] = {t' ∈ M_tgt : is_attn(t')} = {t}`. Unflagging `t` retracts `attn(t)`, giving `is_attn(t) = ⊥`, so `t ∉ [D_{ρ_P}]` and `[D_{ρ_P}] = ∅`. The producer conjunct `(∀ x ∈ [D_{ρ_P}] :: ¬T_P(x))` is then **vacuously true** — the half is *reached*, not unreached. Removal makes `T_P`'s conjunct true; it cannot make it false-at-every-state.

Per Q6, "unreached" (no state ever quiescent) is **case (3)**, which "needs *unboundedly many* distinct arguments" cycled out of phase, or at minimum a fixed set `{x₁,…,x_j}` with `j ≥ 2` "arranged so that at *every* state at least one xᵢ stands trigger-true — ... leaving *no* all-empty gap." A single argument oscillating in and out of its domain is **case (2)** — "quiescent in the gaps, non-quiescent during each presentation: quiescence *is reached* ... but not *held*." With one target, every unflagged instant is an all-empty gap (`[D_{ρ_P}] = ∅`, quiescent), so the worst the environment can do is deny *holding*, never *reaching*. The parenthetical conflates "`t` never gets its comment" (work undone) with "ρ_P's quiescence half unreached" (the half is satisfied precisely because an unflagged `t` no longer needs attention).

**Required**: Either (a) relabel the consequence as case (2) — "ρ_P's half could fail to be *held*, reached in every unflagged gap but re-armed by re-flagging" — or (b) to actually exhibit "unreached" (case 3), extend the example to ≥2 targets cycled out of phase, matching the general statement two paragraphs up ("flagged target**s** the environment can cycle out of phase ... possibly unreached"). The general (plural-target) statement is correct; only this single-target parenthetical errs.

### Issue 2: The stratification "repair" is asserted, not derived, and introduces undefined machinery

**ASN-0133, Worked composition (ρ_R' variant)**: "Stratification states the repair for that variant: ρ_P at stratum 0, ρ_R' at stratum 1, legal iff resolver emissions never enlarge the producer's domain — never make a fresh target need attention. The general condition 'no emission re-arms a strictly lower stratum' is the right demand for a non-SF lower stratum..."

**Problem**: "Stratum"/"stratification" appears nowhere in the formal sections (RG–Q9); it is introduced here ad hoc, and the legality condition is stated declaratively ("states the repair," "is the right demand") with no proof that a stratified registry terminates. A worked example should *illustrate* the note's established results, not assert new unformalized mechanisms as settled. The ρ_R' coupling itself is a fine concretization of Q4's warning — it is the *repair* that overreaches.

Worse, the derivation is *available and omitted*: if "resolver emissions never enlarge `[D_{ρ_P}]`," then `[D_{ρ_P}]` grows only by environment input, which is exactly Q5a's bounded-external-input hypothesis — so "stratification ⟹ domain-growth-is-external ⟹ Q5a ⟹ H-RF" follows from results already in the note. The note asserts the conclusion instead of routing through Q5a.

**Required**: Either derive the claim explicitly (it is a corollary of Q5a once the legality condition reduces producer-domain growth to external input), or cut the "stratum" framing and state plainly that cross-rule coupling defeating bounded growth is future work (it overlaps Open Question 4). As written it presents an unproven termination discipline as established.

### Issue 3: The S-monotonicity rationale is stated twice, SC forward-justifying Q9's content

**ASN-0133, SC**: "Q9's anti-monotone nesting rests on exactly this, and the three canonical bodies below satisfy it by construction ... while barring the pathological bodies — an S under negation — that would invert the nesting."
**ASN-0133, Q9**: "Without S-monotonicity the nesting inverts: a body with S under negation — β_ρ^S(x) ≡ ¬S(addr(x)) — grows the filtered domain as S shrinks ... inverting the implication — exactly the body SC's S-monotonicity excludes."

**Problem**: Both passages carry the same content — "an `S` under negation inverts the nesting; S-monotonicity excludes it." SC pre-explains *why* the constraint exists (deferring to Q9) and Q9 restates the same exclusion (deferring back to SC). This is the duplication / forward-justification pattern the anti-bloat pass targets: the rationale and the `¬S` counterexample belong in one place.

**Required**: At SC, state only *what* the constraint is ("`β_ρ^S` must be monotone in `S` — `S` occurring only positively"). Let Q9 own the rationale (anti-monotone nesting and the `¬S(addr(x))` counterexample). Drop SC's "Q9's anti-monotone nesting rests on exactly this ... that would invert the nesting."

### Issue 4: The H-W critique buries a one-line fact under editorial framing

**ASN-0133, "The H-RF/H-W separation"**: "But H-W's deeper defect is not its starvation-fragility — it is that H-W *is* the termination conclusion in disguise. ... *That* — not merely its generic failure under starvation — is why H-W is no usable route: a hypothesis logically equivalent to 'every path reaches and holds quiescence' cannot serve as a hypothesis of a termination theorem..."

**Problem**: The load-bearing fact — `|W(σ)| < ∞` forces a maximum trigger-true index `k*`, past which every state is quiescent, so H-W ⟹ reaches-and-holds quiescence, hence circular — is sound and worth keeping. But it is two sentences wrapped in a paragraph of evaluative framing ("deeper defect," "no usable route," "*That* — not merely its generic failure," "presupposing the eventual-and-held quiescence it would be invoked to prove"). The note defines W/H-W and proves Q5 essentially to disown them; the disowning argument is then over-narrated. A precise reader works through a hypothesis the note exists to reject.

**Required**: State the circularity once, tersely (H-W ⟹ every σ reaches-and-holds quiescence with no fairness, so it is strictly stronger than Q6's conclusion and cannot be a hypothesis of it). Retain the H-RF < bounded-growth < conclusion ordering and "H-W ⟹ H-RF (Q5's injection)," which is the genuinely informative placement. Cut the editorial restatements.

### Issue 5: `is_in_chain` does not reach `chain`'s default-view value

**ASN-0133, Q0**: "a Boolean trigger reaches its default-view value only through one of the two sequence-eliminating primitives — V-PRIM's order-forgetting projection `elems(chain(x))` ... or the verdict atom `is_in_chain`, which UV never rewrites and so reads identically at every view, needing no rebuild."

**Problem**: `is_in_chain` is "evaluated against the *unrewritten* [active] walk" (UV, ASN-0129) — it is view-stable and therefore does **not** reflect the default-view filtering of `chain` at all. So it is not a route to *chain's* default-view value; it is a *separate* view-stable quantity that sidesteps the issue. Under the charitable reading "its" = the trigger's value (a trigger using `is_in_chain` is view-stable, so its default value equals its value), the sentence is defensible — but the surface reading ("reaches [chain's] default-view value ... through `is_in_chain`") is false, and the conflation of two distinct quantities makes a subtle step harder to follow. The Q0 conclusion is unaffected.

**Required**: Separate the two: a Boolean trigger consuming a chain does so via `elems(chain(x))` — whose *default* value needs the set-valued filter rebuild — or via `is_in_chain`, which is view-stable and needs no rebuild *because it never reads the filtered chain*. Don't list `is_in_chain` as a way to obtain chain's default-view value.

## OUT_OF_SCOPE

### Topic 1: A stratified-registry termination theorem (constructive cross-rule discipline)
**Why out of scope**: Q4 establishes that locality alone cannot exclude mutual re-arm, and Q6 closes single-registry termination via bounded growth + SF + extinction + fairness. A *checkable structural discipline* that guarantees the bounded-growth hypothesis across coupled rules (the "stratification" gestured at in Issue 2) is new territory — it is the constructive counterpart of Q4's warning and overlaps Open Question 4's cross-scope cascade concern. It belongs in a future ASN, not as an asserted aside in this one's worked example.

META: (none — the note stays at the substrate/coordination boundary, keeping rule bodies and schedulers explicitly out of the model, and Q0/Q1 are genuine substrate-level guarantees.)

VERDICT: REVISE
