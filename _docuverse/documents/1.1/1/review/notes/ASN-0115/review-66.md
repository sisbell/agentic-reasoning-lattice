# Review of ASN-0115

I worked through every claim, every proof, the boundary cases (empty spec-set, empty active set, depth-incompatible specs, `act = ∅` inside the depth-compatible branch, non-`{s_C,s_L}` subspaces, deeper-than-`m_S` named positions), all four worked instances, and the wp analysis. The formal content is, with one exception, sound and unusually thorough. The Confinement lemma, the deep-case redundancy argument for the `act` override, the R6 bindable-slice / terminal-overrun analysis, the R8 subspace-sharing and link-vacuity proofs, and the R7 active-set agreement are all correct and handle their cases. The implementation asides survive the anti-bloat carve-out for "statements of what an operation does or does not do." I found one genuine imprecision.

## REVISE

### Issue 1: R7's "exactly when" overstates sufficiency to a biconditional

**ASN-0115, §"Repeatability" (R7), closing sentence**: "the arrangement is the sole mutable input (R4; P3), so repeatability holds **exactly when** the consulted restriction is unchanged — R7's hypothesis"

**Problem**: "exactly when" asserts a biconditional, but only sufficiency is established and true. The formal R7 claim (`Σ.M(dⱼ)|⟦σⱼ⟧ = Σ'.M(dⱼ)|⟦σⱼ⟧` for all `j` ⟹ `deliver(R, Σ) = deliver(R, Σ')`) is the forward direction and is correct. The necessity direction — delivery identical ⟹ restriction unchanged — is false, and the model realizes a counterexample:

- Let `d` have `V_1(d) = {[1,1]}` with `Σ.M(d)([1,1]) = a₁`, `Σ.C(a₁) = "X"`.
- Allocate fresh content `a₂` by K.α with `Σ.C(a₂) = "X"`. S4 (OriginBasedIdentity) explicitly permits `a₁ ≠ a₂` with `Σ.C(a₁) = Σ.C(a₂)`, and K.α imposes no value-distinctness, so this is reachable.
- K.μ⁻ contracts `V_1(d)` to `∅`, then K.μ⁺ re-pins it; D-MIN★ forces the first re-added content position to be `[1,1]`, now mapped to `a₂`. So `Σ'.M(d)([1,1]) = a₂`.

For the unit spec `(d, σ)` naming `[1,1]`: at `Σ` the delivery is `⟨content, "X"⟩`; at `Σ'` it is again `⟨content, "X"⟩` — **identical** — yet the consulted restriction **changed** (`Σ.M(d)|⟦σ⟧([1,1]) = a₁ ≠ a₂ = Σ'.M(d)|⟦σ⟧([1,1])`).

The supporting reasoning has the same gap: "sole mutable input" gives `deliver = f(restriction, stores)` with stores immutable, hence sufficiency; it does **not** give injectivity of `f` in the restriction, which "exactly when" silently requires and which fails by same-valued rebinding.

**Required**: Weaken to sufficiency — e.g., "repeatability is *secured by* keeping the consulted restriction unchanged (R7's hypothesis)" — or qualify the converse explicitly (e.g., "the converse can fail only when a rebinding lands on an equal-valued content address, which a caller cannot rely on"). The formal R7 claim itself needs no change; only the closing prose overstates.

## OUT_OF_SCOPE

None to add. The Open Questions already enumerate the deferred territory (inline provenance, failure semantics, relaxed S3★ dangling references, channel faithfulness, straddling-span delivery), and the ordinal-level restriction cleanly excludes boundary-crossing spans by construction.

VERDICT: REVISE
