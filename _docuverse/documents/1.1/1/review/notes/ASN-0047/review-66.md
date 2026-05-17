# Review of ASN-0047

## REVISE

### Issue 1: Cross-document disjointness chain lemma case analysis is incomplete
**ASN-0047, "Allocator hierarchy under documents" / Cross-document disjointness chain (Lemma)**: The proof states three cases — "*Same-account sibling case*: `d₁` and `d₂` share a parent account `a` and are siblings produced by `a`'s document sub-allocator", "*Same-account version pair case*: `d₂ = inc(d₁, 1)`", and "*Different-account case*".

**Problem**: The case analysis is not exhaustive over all distinct document pairs. Two genuinely uncovered configurations:

(a) **Versions of the same base document.** If `d₁ = d_prev.1` and `d₂ = d_prev.2 = inc(d_prev.1, 0)`, these are siblings under *d_prev's version allocator*, not under "`a`'s document sub-allocator". They fall outside the sibling-case wording even though T10a.2 still applies to them as same-allocator siblings.

(b) **Mixed version/sibling.** If `d₁ = inc(d_prev, 1)` (version of d_prev) and `d₂ = inc(d_prev, 0)` (next sibling of d_prev under account a), they are: (i) not siblings of each other under any common allocator (d₁ lives in d_prev's version allocator; d₂ lives in a's document sub-allocator); (ii) not in a direct version-pair relationship (neither is `inc(·, 1)` of the other); (iii) under the same account. T10a.5 doesn't apply because d₁'s allocator is a descendant of d₂'s allocator (they have ancestor-descendant relationship). No case applies.

The conclusion `b_L(d₁) ⋠ b_L(d₂) ∧ b_L(d₂) ⋠ b_L(d₁)` does hold for both configurations — via T10a.2 on the version-allocator siblings in (a), and via a layered argument using T10a.2 on (d_prev, d_other) plus prefix transitivity in (b) — but the lemma's proof doesn't derive these conclusions.

**Required**: Either widen the case structure to cover all same-allocator-sibling configurations (not only "a's document sub-allocator") and add a fourth case for mixed version/sibling scenarios with a layered argument, or replace the three-case structure with a single general result that covers any pair of distinct documents structurally (e.g., by case-splitting on whether d₁ and d₂ are prefix-comparable, then dispatching each branch through T10a.2 / direct anchor-divergence / T10a.5 as appropriate).

VERDICT: REVISE
