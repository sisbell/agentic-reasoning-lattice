# Review of ASN-0115

## REVISE

### Issue 1: R6's `act = ∅` sub-case is justified by a false premise, and "terminal overrun" mischaracterizes it

**ASN-0115, "Partial delivery: the gap is legal, not an error"**: the proof's parenthetical for the empty-active case reads

> "(If instead `act = ∅`, then `⟦σ⟧` meets no bound position, and — exactly as in the `V_S(d) = ∅` branch — every named position is an unbound overrun with no interior active range for a hole to fall in.)"

**Problem**: This sub-case is reached *after* the proof has already split off `V_S(d) = ∅` and is now in the `V_S(d) ≠ ∅` branch ("Otherwise `V_S(d) ≠ ∅` … which is the case the remainder of this argument analyses"). So when `act = ∅` arises here, the active range `V_S(d) = {[S,1,…,1,k] : 1 ≤ k ≤ n_S}` is **non-empty**. The justification "no interior active range for a hole to fall in" is therefore false — there *is* an active range; the span's slice simply fails to reach it. Two ways `act = ∅` can occur with `V_S(d) ≠ ∅`: (a) the start's prefix differs from `[S,1,…,1]` (so the depth-`m_S` slice lies under a different prefix entirely), or (b) the prefix is canonical but `s_{m_S} > n_S`. The headline claim — "always a *terminal overrun* of the subspace's contiguous active range — the named positions past the bound frontier" — holds in (b) but not in (a): in (a) the unbound positions are not "past the frontier `n_S`," they sit under an unrelated prefix and are not an overrun of the active range in the stated sense.

The conclusion ("no interior hole within the active range") survives in both — the span names nothing inside the range, so it punches no hole — but the *reason given* and the *positive characterization* are both wrong for sub-case (a).

**Required**: In the `act = ∅` sub-case, distinguish `V_S(d) = ∅` (no active range exists) from `V_S(d) ≠ ∅` (active range present but not reached), and discharge the latter by **slice-disjointness** (the depth-`m_S` slice does not intersect `V_S(d)`), not by claiming no active range exists. Either restrict the "terminal overrun past the bound frontier" wording to the canonical-prefix case, or demote the positive characterization to the load-bearing negative one (no interior hole within the active range).

### Issue 2: undefined symbol `n` in the slice characterization

**ASN-0115, "Partial delivery…"**: "Hence the depth-`m_S` slice of `⟦σ⟧` is exactly `{[S, 1, …, 1, k] : s_{m_S} ≤ k < s_{m_S} + n}`, the only free coordinate being `k`."

**Problem**: `n` is never bound in this scope. It is the width's deepest component `ℓ_{m_S}` — the slice contains exactly that many positions (cf. the §Exactness worked instance, where `ℓ = δ(5,2)` yields a 5-element slice). A reader can infer it, but a slice bound stated with an undefined symbol is exactly the kind of gap this review exists to catch.

**Required**: Introduce `n = ℓ_{m_S}` at first use, or write `s_{m_S} + ℓ_{m_S}` directly.

### Issue 3: R6 claim statement and R6 proof restate the same scoping caveat (anti-bloat)

**ASN-0115, "Partial delivery…"**: the claim blockquote says

> "Named positions of `⟦σⱼ⟧` deeper than `m_S` are unbound too, but for a simpler reason: by S8-depth … so any named position of depth `> m_S` is absent … and is harmlessly filtered out of `act`; the no-interior-hole guarantee is a claim about the bindable slice, not about every named tumbler in the interval."

and the proof body says, in different words,

> "Named positions of `⟦σ⟧` deeper than `m_S` are necessarily unbound, and the reason is immediate: S8-depth fixes the depth … so a named position of depth `> m_S` is simply absent … The no-interior-hole property is therefore a statement about the bindable slice, not about every tumbler of the interval."

**Problem**: Near-verbatim duplication of both the "deeper-than-`m_S` is unbound for a simpler reason" point and the "bindable slice, not every tumbler" caveat. A precise reader meets the same argument twice and must check they are not subtly different (they are not).

**Required**: State the bindable-slice scoping once. Put the property in the claim; derive it (with the depth-`> m_S` remark) once in the proof.

### Issue 4: defensive and meta-prose that does not advance the reasoning (anti-bloat)

Three sites:

- **"What a spec-set is…", Confinement proof**: "The argument consumes only ordinal-level width and `#s ≥ 2`, and holds for **every** `t ∈ ⟦σ⟧`, bound or not — no content-reference hypothesis is required." The "holds for every `t`" clause merely restates the lemma's own quantifier; "no content-reference hypothesis is required" defends against an imagined objection (the ASN-0058 C0a content-reference version). Neither advances the proof.
- **"The substrate we build on", standing precondition**: "Each claim cites the specific invariant it relies on at its use site." is editorial commentary on the document's citation practice, attached to no claim. "R7 (Repeatability) additionally relates two such reachable states comparable under `→*`; the base definitions inherit the single-state form of this precondition." is a forward reference enumerating a downstream consumer of the precondition.
- **"What a spec-set is…", `item` well-definedness**: "The per-case S3★ citations discharge store membership *within* each case; S3★-aux discharges that the case split *covers* `act`." restates the two preceding sentences as a which-citation-does-what inventory.

**Problem**: In each case the reader must step past prose that re-describes a citation, defends against an unraised concern, or points forward, rather than carrying the argument.

**Required**: Trim to the load-bearing statements — the Confinement lemma's own quantifier; the reachability precondition itself; the per-case/coverage citations without the inventory gloss.

## OUT_OF_SCOPE

The Open Questions correctly defer channel faithfulness, outright-failure policy, dangling-reference delivery, inline provenance, and single-span subspace straddling — each is genuinely new territory, not a gap in this ASN. The ASN otherwise respects its scope boundary: R10 delivers a link *reference* and explicitly stops short of endset structure (ASN-0111/0114 territory), and no extent-reporting (ASN-0112/0113) or link-search content is smuggled in. No out-of-scope claims to flag.

VERDICT: REVISE
