# Review of ASN-0133

This is a careful, heavily-worked note. I checked the proofs of Q0 (the load-bearing PL-membership argument), Q3's Marker pattern (both idem regimes), Q5/Q5a's injections, Q-EXT's step-agnostic at-most-once, the full Q6 case analysis (regimes (i)/(ii), cases (1)–(3), the H-SFAIR regime form), and the scope anti-monotonicity (Q9). The mathematics holds — I found no correctness gap in the termination results. The findings below are one precision defect plus the meta-prose the note's `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: targets_of's rebuild formula is actually members'
**ASN-0133, Q0**: "The two view-parameterized collections `members`/`targets_of`, and with them the domain base `M_K`, carry their default value the same way: the UV filter `{· : ¬filtered(·)}` ... wrapped around the active rebuild `⋃(A_K, addrs_F)`"

**Problem**: `⋃(A_K, addrs_F)` is the active rebuild of `members` only. `targets_of(x, active) = ⋃{addrs_G(c) : c ∈ A_K ∧ x ∈ addrs_F(c)}` (D3) — it depends on the argument `x`, matches the *source* (`x ∈ addrs_F(c)`), and collects `addrs_G`, not `addrs_F`. The written formula ignores `x` and yields sources, i.e. `members`. So the one concrete formula the note gives for "members/targets_of" is correct for the first atom and wrong for the second. The *claim* (targets_of is rebuildable via PC3's device) survives — `⋃({c ∈ A_K : x ∈ addrs_F(c)}, addrs_G)` is a well-typed term — but the spelling presented does not compute targets_of.

**Required**: Either write targets_of's rebuild explicitly (`{y ∈ ⋃({c ∈ A_K : x ∈ addrs_F(c)}, addrs_G) : ¬filtered(y)}`), or mark `⋃(A_K, addrs_F)` as the members-only instance of the schematic device, not a formula shared by both.

### Issue 2: Worked example — the ρ_R′ digression illustrates an excluded case, then defers
**ASN-0133, Worked composition / Bound (Q5a)**: "To exhibit the divergence Q4 warns locality cannot exclude, the coupling must be made real: take a variant resolver `ρ_R'` that on resolving `c` also flags a fresh target ... The repair for that variant needs no new termination machinery — it is a corollary of Q5a. Impose the legality condition that `ρ_R'`'s emissions never enlarge `[D_{ρ_P}]` ... The general problem ... this note does not settle; it overlaps Open Question 4's cascade/re-opening theory and is left there."

**Problem**: The worked example's job is to verify the actual `(ρ_P, ρ_R)` registry, which the note has just shown is type-isolated. This block instead constructs a *different* registry to re-illustrate Q4 (already stated abstractly), repairs it with a condition the note itself labels "a corollary of Q5a" (no new result), and ends by deferring the general version to ASN-0130-adjacent OQ4. It is a self-contained digression that does not advance the verification and terminates in a downstream pointer — the exact "imagines a case the registry excludes + defers to downstream location" pattern.

**Required**: Cut to one sentence — Q4's warning is vacuous here by type isolation; the general coupling discipline is OQ4 — and remove the ρ_R′ construction and its repair.

### Issue 3: Worked example — type-isolation restated four-plus times
**ASN-0133, Worked composition**: the fact "no rule writes `attn`/`tgt`, so `[D_{ρ_P}]` grows only by the environment" recurs:
- "no rule writes `attn` or `tgt` — `ρ_P` emits `cmt`, `ρ_R` emits `res` — so the producer's domain grows only by environment deposits"
- "with `attn`/`tgt` written by no one, `{t ∈ M_tgt : is_attn(t)}` is static"
- "since no rule writes `attn` or `tgt` (above) and `res` is no retraction, a `ρ_R` deposit moves neither `M_tgt` nor `is_attn` ... type-isolated"
- "`{t ∈ M_tgt : is_attn(t)}` accrues precisely by environment deposits of `attn`/`tgt` — exactly the bounded-flagged-population hypothesis above"

**Problem**: One structural fact, stated four times in adjacent paragraphs. The precise reader must confirm each restatement says nothing new.

**Required**: State it once (the "crux" sentence suffices), and let the type-isolation and closed-special-case observations cite it rather than re-derive it.

### Issue 4: Q6 — post-proof restatement of the hypothesis packages
**ASN-0133, Q6 (after ∎)**: "Since all-SF + extinction-disciplined + bounded domain growth ⟹ H-RF (Q5a), that structural package with H-FAIR makes the registry's work terminate — and delivers reached and held quiescence under weak fairness when domains are grow-only, deferring both to regime (i) or H-SFAIR otherwise." ... "Extinction discipline is not a third independent hypothesis of Q6: it is a hypothesis of Q5a..."

**Problem**: The package result is now stated three times — the "Reaching and holding, by hypothesis package" preview before the proof, the regime (i)/(ii) derivation inside it, and this closing summary. The summary adds nothing the bulleted preview did not, and "Extinction discipline is not a third independent hypothesis" is a defensive clarification of a confusion the proof already forecloses. (The adjacent drop-H-RF / drop-H-FAIR necessity remark *is* load-bearing — keep that.)

**Required**: Delete the package restatement; keep only the necessity contrast.

*Minor recurrences of the same kind, not itemized:* the `is_in_chain` two-sentence restatement in Q0 ("not a second route ... sidestepping the rebuild rather than performing it"), the Q0 closer ("no agent reports, no consensus, no decision history"), and the H-RF/H-W separation paragraph's length all trend the same way.

## OUT_OF_SCOPE

The note's "What this note doesn't cover" and Open Questions already fence the right boundaries (scheduler construction, the turn-fairness model H-SFAIR's satisfiability needs, an environment model, the `pd_extinct`/SF certificate, per-scope vs global work). I have no additional future-ASN items to add — the self-scoping is adequate.

VERDICT: REVISE
