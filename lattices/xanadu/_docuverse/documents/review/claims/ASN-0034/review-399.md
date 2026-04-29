# Regional Review — ASN-0034/T4a (cycle 1)

*2026-04-23 00:25*

### Undefined relations `≥` and `>`
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder), NAT-sub (NatPartialSubtraction)
**ASN**: NAT-order defines only `<` as primitive and `≤` via `m ≤ n ⟺ m < n ∨ m = n`. But NAT-sub's axioms use `≥` and `>` (e.g., "`(A m, n ∈ ℕ : m ≥ n : m − n ∈ ℕ)`", "`(A m, n ∈ ℕ : m > n : m − n ≥ 1)`"); T4a's proof uses "`#t ≥ 1`", "`s₁ ≥ 2`", "`s_k ≤ #t − 1`" (the last requiring `#t ≥ 1` to ground the subtraction).
**Issue**: The relations `≥` and `>` appear in formal axiom bodies and proof steps without being introduced. In a document that explicitly defines `≤` in its Definition slot ("The axiom slot introduces `<` before constraining it... the non-strict companion `≤` is defined"), the symmetric counterparts cannot be left to reader convention. The NAT-order contract's Definition slot currently lists only `≤`; NAT-sub uses `≥`/`>` as if given.
**What needs resolving**: Either NAT-order's Definition slot should introduce `≥` and `>` as reverses of `≤` and `<`, or every downstream use must be rephrased in terms of the defined `<`/`≤`. The fix should not expand NAT-order's axiom slot (these are notational definitions, not axioms).

### Meta-prose embedded in axiom bodies
**Class**: OBSERVE
**Foundation**: NAT-closure, NAT-zero, NAT-discrete, NAT-order
**ASN**: NAT-closure's prose: "Successor closure `n + 1 ∈ ℕ` is not axiomatized separately: it is the instance of the codomain commitment at `(m, n) := (n, 1)`... The mirrored clause `n + 0 = n` is not axiomatized here; commutativity of `+` is not enumerated, so the right-identity form is not derivable from this axiom alone." NAT-zero's "The minimum predicate `(A n ∈ ℕ :: ¬(n < 0))` is therefore exported as a *Consequence:* of the formal contract, lifted from..." T4's Exhaustion: "This uses trichotomy alone — substitution of equals under `<` is not among NAT-order's stated properties, so we avoid relying on it."
**Issue**: These are defensive justifications explaining why a particular structural choice is safe, why something is NOT axiomatized, or why a dependency is declared — meta-commentary about the document's construction rather than content that advances the axiom or proof. A reader following the claim must skip past this to recover the formal content. Not a correctness issue since the axioms themselves stand, but it is reviser-drift noise that accumulated across prior cycles.

### Field-segment decomposition under weakened precondition
**Class**: OBSERVE
**Foundation**: T4, T4a
**ASN**: T4a's preconditions allow `t ∈ T` with `zeros(t) ≤ 3` but without full T4-validity. Field segments are defined in T4's body as "maximal contiguous sub-sequences of non-zero positions — k+1 of them when zeros(t) = k."
**Issue**: The segment decomposition is used in T4a outside T4's validity hypothesis. This works (e.g., for `t = (0)` the decomposition yields two empty segments, consistent with the biconditional), but the decomposition is introduced in T4's prose within a context that presumes "every tumbler `t ∈ T` used as an address satisfies..." The reader must re-derive that the definition continues to make sense when the positional constraints fail. A one-line note in T4 or T4a clarifying that the segment decomposition is defined purely from the zero-position enumeration (independent of field-segment non-emptiness) would remove the need for this re-derivation.

VERDICT: REVISE
