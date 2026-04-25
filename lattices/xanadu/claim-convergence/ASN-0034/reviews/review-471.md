# Regional Review — ASN-0034/NAT-card (cycle 6)

*2026-04-24 02:26*

### NAT-card axiom mixes ellipsis notation and set-builder comprehension for overlapping constructions
**Class**: REVISE
**Foundation**: —
**ASN**: NAT-card Axiom first clause: the outer quantifier ranges over `S ⊆ {1, 2, …, n}` using ellipsis, while the same clause spells the enumerating function's domain in comprehension form `f : {j ∈ ℕ : 1 ≤ j ≤ k} → ℕ` and writes the image as `{f.j : 1 ≤ j ≤ k}`.
**Issue**: Within a single axiom clause two notations coexist for "initial segment of ℕ bounded by a positive integer": the informal `{1, 2, …, n}` and the grounded `{j ∈ ℕ : 1 ≤ j ≤ k}`. The comprehension form is what makes the `k = 0` case well-defined (empty domain); the ellipsis form is left to a Depends-slot gloss ("`{1, 2, …, n} = {j ∈ ℕ : 1 ≤ j ≤ n}`") for its unfolding. A reader consulting only the Axiom slot sees the ellipsis version and must either import the convention from Depends or from folklore. Two notations for the same construction in one clause also invite the failure mode where a future edit tightens one site and not the other.
**What needs resolving**: Use comprehension form uniformly in the Axiom bullet, writing `S ⊆ {j ∈ ℕ : 1 ≤ j ≤ n}` in place of `S ⊆ {1, 2, …, n}`. Then the ellipsis-to-comprehension unfolding can be dropped from Depends. Alternatively, pick the ellipsis form and define it once formally — but the comprehension form is what the rest of the axiom is already using.

### NAT-card `k = 0` parenthetical is stated twice — in the body sentence and inside the Axiom clause
**Class**: REVISE
**Foundation**: —
**ASN**: NAT-card body: "(at `k = 0` the domain `{j ∈ ℕ : 1 ≤ j ≤ 0}` is empty, `f` is the empty function, vacuously strictly increasing with image `∅`, forcing `S = ∅` and `|∅| = 0` without recourse to a convention on empty lists)". NAT-card Axiom: "(at `k = 0` the domain is empty, `f` is the empty function, vacuously strictly increasing with image `∅`, so the predicate forces `S = ∅` and `|∅| = 0` without any convention on empty lists)".
**Issue**: The same ~30-word parenthetical appears in two slots, with trivial wording differences. The content is a verification that the existentially-quantified predicate resolves at `k = 0` — a property a precise reader confirms by inspection, not a clause of the postulate. Keeping it in both the body and the Axiom slot is the "paragraph looks like a prior finding's content relocated rather than removed" pattern from the instructions: the prior finding asked to move to a function-based formulation to eliminate empty-list conventions; the function-based formulation landed, but the accompanying rationale wasn't reduced — it was placed in two sites instead of one.
**What needs resolving**: Keep one instance. Body prose is the natural site for a gloss; the Axiom slot should carry the quantified clause plus minimal tags. The function-based clause already forces `S = ∅` when `k = 0` by its own syntax (the image `{f.j : 1 ≤ j ≤ 0}` is empty), and a reader of the Axiom alone can confirm this without the parenthetical.

### T0 body's reflexivity-of-`≤` derivation computes around NAT-order inside a T0 sentence
**Class**: REVISE
**Foundation**: —
**ASN**: T0 body: "Reflexivity of `≤` follows from the equality branch of NAT-order's definition `m ≤ n ⟺ m < n ∨ m = n` at `m := n := 1`, so `1 ≤ 1` holds; together with `1 ≤ #a` this places `1` in the index set `{j ∈ ℕ : 1 ≤ j ≤ #a}`, so the index domain `{1, …, #a}` is never empty and bounded quantifiers of the form `(Q i : 1 ≤ i ≤ #a : …)` range over a nonempty set rather than collapsing to vacuity."
**Issue**: The derivation is two immediate steps in NAT-order: unfold `≤` via its definition, then take the equality branch. T0's job is to posit `T` with its length and index structure, including the nonemptiness clause `1 ≤ #a`. That the index set `{j ∈ ℕ : 1 ≤ j ≤ #a}` contains `1` is an immediate consequence of the axiom; spelling out the `≤`-unfolding and the equality-branch selection in T0's body is the third reviser-drift pattern the instructions flag — "new prose around an axiom explains why the axiom is needed rather than what it says." T0 is not where the properties of `≤` are established. If `≤` is in scope, the reader can read `1 ≤ #a` directly.
**What needs resolving**: Remove the reflexivity derivation. If the nonemptiness reading benefits from one sentence, say "so `{j ∈ ℕ : 1 ≤ j ≤ #a}` is nonempty" and stop; leave the unfolding of `≤` to the reader, or to NAT-order where `≤` is defined.

VERDICT: REVISE
