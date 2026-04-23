# Regional Review — ASN-0034/TA4 (cycle 1)

*2026-04-23 05:24*

Looking at this as a system rather than a collection of claims, I'll trace the dependency web and see what's cited but not grounded.

### Undefined axiom NAT-wellorder
**Class**: REVISE
**Foundation**: N/A (foundation ASN)
**ASN**: Multiple claims cite `NAT-wellorder (NatWellOrdering)` in their *Depends* lists — TumblerAdd ("NAT-wellorder applied to `{j : 1 ≤ j < k ∧ aⱼ > 0}`"), ActionPoint ("By NAT-wellorder, there exists m ∈ S"), ZPD, T1, TumblerSub. But no `NAT-wellorder` axiom block appears in the ASN. The only NAT-* axioms axiomatized are NAT-closure, NAT-addcompat, NAT-cancel, NAT-zero, NAT-order, NAT-sub.
**Issue**: This is a foundation ASN with empty declared depends, so every cited name must be axiomatized internally. NAT-wellorder is load-bearing (used to pick "first divergence position," "least i with wᵢ > 0," least element of S for `zpd`), but the axiom stating the least-element principle is absent. Every proof that invokes it is resting on an unwritten axiom.
**What needs resolving**: Either add a NAT-wellorder axiom block (statement of the least-element principle on nonempty subsets of ℕ), or derive the instances used from axioms that are present (and remove the NAT-wellorder citations).

### Undefined axiom NAT-discrete
**Class**: REVISE
**Foundation**: N/A (foundation ASN)
**ASN**: T1 dependencies cite `NAT-discrete (NatDiscreteness) — forward direction m < n ⟹ m + 1 ≤ n`, used in Case 1 contrapositively and in the `k₂ < k₁` case-(ii) branch. ActionPoint cites NAT-discrete in its *Depends* ("forward direction m < n ⟹ m + 1 ≤ n") and its proof uses it at `n = w_{actionPoint(w)}`. TumblerSub cites it in its *Depends* block. But no `NAT-discrete` axiom block appears in the ASN.
**Issue**: Cited dependency is not axiomatized. The forward direction `m < n ⟹ m + 1 ≤ n` is not a logical tautology on a strict total order — it is a discreteness property specific to ℕ. Without the axiom, ActionPoint's derivation of `1 ≤ w_{actionPoint(w)}` and T1's Case 1 contrapositive reduction both rest on an unwritten claim.
**What needs resolving**: Add an NAT-discrete axiom block (or fold the forward direction into an existing axiom) so the citation points to a grounded statement.

### Undefined claim Divergence
**Class**: REVISE
**Foundation**: N/A (foundation ASN)
**ASN**: TumblerSub's *Depends* lists `Divergence (Divergence) — case analysis on the pair (w, a)`. Its proof opens "Two Divergence cases arise for the pair (w, a) with w ≠ a: (i) Component divergence at position k with k ≤ #w ∧ k ≤ #a and wₖ ≠ aₖ. (ii) Prefix divergence splits via NAT-order's trichotomy…". ZPD's *Depends* also lists `Divergence (Divergence)` with a "two-case structure" description, and its Relationship-to-Divergence postcondition refers to "Divergence case (i)" and "Divergence case (ii)" and the function `divergence(a, w)`. But no `Divergence` claim with formal contract appears in the ASN.
**Issue**: Divergence is treated as a named claim with exported cases and a function `divergence(a, w)`, yet the ASN defines nothing under that label. The closest match is the *proof-local* definition of "divergence position" inside T1's trichotomy argument — but a proof-local construct in T1 is not a formal dependency that TumblerSub and ZPD can cite and re-case on. The TumblerSub case labels (i)/(ii) do not even align with T1's local labels (α)/(β)/(γ).
**What needs resolving**: Promote Divergence to a first-class claim with its own formal contract (the two-case structure, the function `divergence(a,b)` on `a ≠ b`, and the bounds on `k`), or rewrite the dependent proofs so they do not cite Divergence as an external object.

### "Divergence" label vs. T1's case labels
**Class**: OBSERVE
**ASN**: T1's trichotomy proof uses clauses `(α)`, `(β)`, `(γ)` for divergence positions. TumblerSub's proof uses clauses `(i)`, `(ii)` with `(ii)` further split into `(ii-a)`, `(ii-b)`. ZPD's postcondition uses `(i)`, `(ii)` and refers back to sub-cases `(β)`, `(γ)`.
**Issue**: Even after Divergence is formalized, the three different labelings in use (T1: α/β/γ; TumblerSub: i/ii with ii-a/ii-b; ZPD: i/ii with β/γ) invite cross-reference errors. A single canonical labeling anchored on the Divergence claim would tighten the argument.

### Case 3 "hence m < n" skips a composition step
**Class**: OBSERVE
**ASN**: T1 proof, Case 3: "(β) gives `m + 1 ≤ n`, hence `m < n` via NAT-addcompat's `m < m + 1`".
**Issue**: The composition of `m < m + 1` with `m + 1 ≤ n` into `m < n` uses NAT-order's `≤`-defining clause followed by transitivity (or substitution). The proof elsewhere spells this out (e.g., part (c) Case `k₂ < k₁` expands `k₁ ≤ n` via the `≤`-clause). The elision here is minor.

VERDICT: REVISE
