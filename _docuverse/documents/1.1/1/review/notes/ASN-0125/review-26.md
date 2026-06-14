# Review of ASN-0125

This is a careful, unusually thorough note. The core derivation (mutation is unimplementable → edit = allocation + assertion → the assertion is a typed link-to-link claim) is sound, the operation contracts EL6/EL7 are discharged in detail, and the worked example traces correctly through every state (I verified the addresses H.0.s_L.1…6, the succ_o transitions, and the standoff `current(ℓ₀) = ∅`). EL9(2)'s suffix-drop-and-re-seat construction, EL10/EL13's commutation arguments, EL11(a)'s content-exclusion biconditional, and EL14(e)'s activity-agnostic-membership construction all check out. Two issues remain.

## REVISE

### Issue 1: DC's `[K_sup]` trigger and EL7(vi) ignore claim arity

**ASN-0125, EDITop precondition `DC(ℓ')` and EL7(vi)**:
> "`coverage(ℓ'.e₃) ≠ coverage(R)`, and if `coverage(ℓ'.e₃) = coverage(K_sup)` then `(E x, y ∈ dom(Σ.L) : x ≠ y ∧ ℓ'.e₁ = {(x, δ(1, #x))} ∧ ℓ'.e₂ = {(y, δ(1, #y))})`."

and

> "if ℓ'-slot-3 coverage is `coverage(K_sup)`, `DC(ℓ')` supplies x, y ∈ dom(Σ.L) ⊆ dom(Σ₁.L) … so the new claim at a' conforms to Df-DISC(ii) at Σ₁ (clause ii preserved)"

**Problem**: A "claim" is a member of `S^Σ = L_{K_sup}^Σ`, and the foundation's TypedRelation (ASN-0086) restricts that slice with `|Σ.L(a)| = 3` exactly ("the `|Σ.L(a)| = 3` conjunct restricts every `L_K` to standard-triple links"). But editlink admits any L3-conforming `ℓ'`, i.e. arity `N ≥ 3`. Consider the case `|ℓ'| > 3 ∧ coverage(ℓ'.e₃) = coverage(K_sup)`:

- DC's `[K_sup]` clause *fires* (it tests slot-3 coverage alone, with no `|ℓ'| = 3` conjunct), so it forces `e₁, e₂` into unit-depth form — yet the successor `a'` carrying `ℓ'` is **not** in `S^{Σ₁}` (arity ≠ 3), so it is not a claim at all.
- EL7(vi) then asserts "the new claim at a' conforms to Df-DISC(ii)," presupposing a claim at `a'` that does not exist. The case `|ℓ'| > 3` is not covered: Df-DISC(ii) is preserved on `a'`, but for the opposite reason (`a' ∉ S^{Σ₁}`, so clause (ii) is vacuous on it), not because "the new claim conforms."

The conclusion (`Σ₂` is edit-disciplined) still holds, so this is not a soundness failure — but it is an uncovered case in a load-bearing discipline-preservation proof, and DC as written is silently over-restrictive (it forbids non-claim, arity->3, `K_sup`-typed successors that cannot violate any invariant). The same arity slack sits in the leading `coverage(ℓ'.e₃) ≠ coverage(R)` conjunct, though there it is benign: EL7(iv)'s use ("step 1 emits no [R]-tuple") only needs `coverage ≠ R`, which excludes `L_R` membership regardless of arity.

**Required**: Either (a) tighten DC's `[K_sup]` clause to trigger on "`a'` would be a claim," i.e. `|ℓ'| = 3 ∧ coverage(ℓ'.e₃) = coverage(K_sup) ⟹ schema`, so the constraint applies exactly to would-be-claims; or (b) keep DC conservative but split EL7(vi)'s `K_sup` case explicitly: `|ℓ'| = 3` → `a' ∈ S^{Σ₁}` is a claim and conforms by DC; `|ℓ'| > 3` → `a' ∉ S^{Σ₁}`, so Df-DISC(ii) holds vacuously on `a'`. EL-DM's editlink step inherits this gap (it cites EL7(vi)), so fixing EL7(vi) closes it.

### Issue 2 (anti-bloat): motivational restatement and forward-reference meta-prose

**ASN-0125, EL1 closing paragraph and EL7(ii)**:
> "This is a refusal, not a gap. A system that inferred derivation from resemblance would manufacture relationships its users never asserted — coincidences and independent convergence flagged as descent — and would make the *system* the author of claims that rightfully have authors. Nelson's position is categorical… EL1 is that position as a theorem…"

**Problem**: The theorem EL1 and its proof (determinism ⟹ identical post-state ⟹ no distinguishing predicate) stand on their own. This paragraph re-states the theorem's significance in design-philosophy terms; only the final clause ("not merely undesirable but undefinable") sharpens the formal content, and that sharpening is already the substance of EL1. The note carries the anti-bloat classifier, and this is the clearest instance of essay content occupying a proof slot. A related, smaller instance is the EL7(ii) parenthetical "(That the operation as defined leaves listing uncoupled is a fact of the definition; whether some layer *should* couple edit to listing is the separate open question of edit-to-listing coupling.)" — the first half ("leaves listing uncoupled") is a legitimate statement of what the operation does not do; the trailing pointer to a future design decision is meta-prose riding the forward reference.

**Required**: Trim EL1's closing paragraph to its load-bearing sharpening (emission records no relationship; the distinguishing fact is absent from state, so resemblance-inference is undefinable, not merely undesirable). Drop the future-design-question half of the EL7(ii) parenthetical, retaining the factual "the successor is born unlisted; seating it is a separate K.μ⁺_L act." The motivational-restatement pattern recurs lightly elsewhere (e.g. the regime-contrast flourishes in EL16); a pass for non-advancing interpretation is warranted.

## OUT_OF_SCOPE

None. The ASN scopes its own deferrals cleanly via the Open Questions (retraction authority, supersession-of-retraction, meta-claim stratification, currency non-emptiness, temporal witnesses, span-level endset correspondence, edit-to-listing coupling, prefix-rooted subtype closure), and it does not stray into the harness-excluded operations — its use of `Observe_{K_sup}` (EL11b) is confined to characterizing supersession-claim discovery, not general link discovery.

VERDICT: REVISE
