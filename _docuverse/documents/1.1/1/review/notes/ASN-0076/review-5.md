# Review of ASN-0076

## REVISE

### Issue 1: Composite definition contradicts adjacency-permission prose

**ASN-0076, §The Composite**: The composite is defined with sequential semicolon notation —
```
EDITLINK(...) ≡
    K.λ(d_new, ℓ_new, (e'_1, ..., e'_N));
    K.λ(d_new, ℓ_sup, (E_from, E_to, E_type))
```
— but the prose two paragraphs later asserts: "the two steps need not be adjacent in the transition sequence; arbitrary other transitions may intervene between them."

**Problem**: ValidComposite★ (ASN-0047) defines a composite as "a finite sequence of atomic transitions Σ = Σ₀ → Σ₁ → ... → Σₙ = Σ'" — by construction a contiguous sub-sequence. The E0 proof depends on this contiguity: the supersession step's discharge of `ℓ_sup ∉ dom(L)` and the identification `ℓ_sup = inc(ℓ_new, 0)` both fire "from Σ_1" (the state immediately after step 1). If arbitrary K.λ steps on `d_new` may intervene, then (a) Σ_1 is no longer the operative pre-state for step 2; (b) `ℓ_new` may no longer be the maximum of `{ℓ' ∈ dom(L) : origin(ℓ') = d_new}`; (c) `ℓ_sup ≠ inc(ℓ_new, 0)` in general. The structural claims E1, E4, E7 etc. would survive (they depend only on the constructed endsets), but the formal status of EDITLINK as a ValidComposite★ collapses.

**Required**: Either tighten EDITLINK to a strict ValidComposite★ (two adjacent K.λ steps, no intervening atomic transitions) and delete the "need not be adjacent" prose, or relax EDITLINK to a named pattern over non-adjacent K.λ steps and rework the proof of E0 to not depend on Σ_1 as the literal pre-state of step 2.

### Issue 2: Length-preservation induction left implicit in successor sub-case (b)

**ASN-0076, §E0, successor step, sub-case (b)**: "The depth bound `#E(ℓ_new) ≥ 2` ... is inherited in (b) from TA5(c) — `inc(·, 0)` preserves length — applied to a prior emission that itself satisfied `#E ≥ 2`."

**Problem**: This appeals to an unstated induction. "A prior emission that itself satisfied `#E ≥ 2`" is exactly what is being established — a prior emission may itself have been a subsequent emission, requiring the same justification. The base case (first emission with `#E = 2` by SubAllocatorAxiom.FirstEmission) and the step case (TA5(c) preserves length) need to be named.

**Required**: One additional sentence: "By induction on the position of `ℓ_new` in `A_L(d_new)`'s enumeration: the first emission has `#E = 2` (SubAllocatorAxiom.FirstEmission); each subsequent emission preserves `#E` by TA5(c). Hence every emission of `A_L(d_new)` satisfies `#E ≥ 2`."

## OUT_OF_SCOPE

### Topic 1: Supersession chain semantics, conflict resolution, "current successor" computation
The Open Questions section enumerates these explicitly as deferred — appropriate.

### Topic 2: Type-endset registry conventions (the semantics of `τ_sup`)
The ASN carefully distinguishes structural witness from semantic identification and defers the convention to a future ASN — appropriate.

### Topic 3: Counter-claim / retraction semantics, discovery by span search, content-edit interaction
All explicitly deferred — appropriate.

VERDICT: REVISE
