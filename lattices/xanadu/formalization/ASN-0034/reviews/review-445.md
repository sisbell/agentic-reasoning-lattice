# Regional Review — ASN-0034/TA4 (cycle 2)

*2026-04-23 05:42*

### Undefined axiom NAT-wellorder
**Class**: REVISE
**Foundation**: N/A (foundation ASN; internal dependency)
**ASN**: `TumblerAdd` ("NAT-wellorder applied to `{j : 1 ≤ j < k ∧ aⱼ > 0}`"), `ActionPoint` ("By NAT-wellorder, there exists m ∈ S with (A n ∈ S :: m ≤ n)"), `ZPD` (*Depends* "least-element principle for `min {k : 1 ≤ k ≤ L ∧ âₖ ≠ ŵₖ}`"), `T1` part (b) ("NAT-wellorder applied to the nonempty set of such positions delivers a least element"), and `TumblerSub` (*Depends* "least-element principle for nonempty subsets of ℕ") all cite `NAT-wellorder (NatWellOrdering)`.
**Issue**: No `NAT-wellorder` axiom block appears in the ASN. The axiom blocks present are NAT-closure, NAT-addcompat, NAT-cancel, NAT-zero, NAT-order, NAT-sub. In a foundation ASN with empty declared `depends`, every cited primitive must be axiomatized internally. The least-element principle is load-bearing (it is how the action point, `zpd`, and T1's first-divergence-position are constructed), yet the axiom stating it is absent. Every proof invoking "NAT-wellorder" rests on an unwritten claim.
**What needs resolving**: Add a NAT-wellorder axiom block formalizing the least-element principle for nonempty subsets of ℕ, with its Depends footprint made explicit (at minimum NAT-order for the relation on which "least" is defined).

### Undefined axiom NAT-discrete
**Class**: REVISE
**Foundation**: N/A (foundation ASN; internal dependency)
**ASN**: `T1` *Depends*: "NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n`, used contrapositively in Case 1 … and in part (c) Case `k₂ < k₁` case-(ii) branch". `ActionPoint` *Depends*: "NAT-discrete (NatDiscreteness) — forward direction m < n ⟹ m + 1 ≤ n" (invoked at "NAT-discrete's forward direction m < n ⟹ m + 1 ≤ n at m = 0, n = w_{actionPoint(w)}"). `TumblerSub` also lists NAT-discrete in *Depends*.
**Issue**: No `NAT-discrete` axiom block appears in the ASN. The forward direction `m < n ⟹ m + 1 ≤ n` is not a consequence of strict-total-order clauses alone — it is a discreteness property specific to ℕ. Without the axiom, ActionPoint's derivation of `1 ≤ w_{actionPoint(w)}` and T1's Case 1 contrapositive reduction `¬(m + 1 ≤ n) ⟹ ¬(m < n)` both rest on an unwritten claim.
**What needs resolving**: Add a NAT-discrete axiom block (or fold the forward direction into an existing axiom with its full Depends footprint), so the citation points to a grounded statement.

### Undefined claim Divergence
**Class**: REVISE
**Foundation**: N/A (foundation ASN; internal dependency)
**ASN**: `TumblerSub` *Depends*: "Divergence (Divergence) — case analysis on the pair `(w, a)`." Its proof body opens "Two Divergence cases arise for the pair `(w, a)` with `w ≠ a`: (i) Component divergence at position `k` … (ii) Prefix divergence …". `ZPD` *Depends*: "Divergence (Divergence) — two-case structure (component divergence; prefix divergence) and domain restriction `a ≠ b` …", and its Relationship-to-Divergence postcondition refers to `divergence(a, w)` as a function.
**Issue**: Divergence is cited as a named, first-class claim with exported cases and a function `divergence(a, w)`, but no Divergence claim with formal contract is axiomatized or proved in the ASN. The closest relative is the *proof-local* notion of "divergence position" inside T1's trichotomy argument, but a proof-local construct in T1 is not a formal dependency that TumblerSub and ZPD can cite and re-case on. Moreover, TumblerSub's case labels (i)/(ii) do not align with T1's proof-local labels (α)/(β)/(γ), so the citation cannot even be understood as a label-preserving reuse of T1's internal structure.
**What needs resolving**: Promote Divergence to a first-class claim with its own formal contract — the two cases (component divergence at a shared position; prefix divergence with length-inequality split), the function `divergence(a, b)` on the domain `a ≠ b`, and the bounds on the returned index — or rewrite the consumers so they do not cite Divergence as an external object.

### Cross-claim label drift in divergence reasoning
**Class**: OBSERVE
**ASN**: T1 part (b) uses `(α)`, `(β)`, `(γ)`. `TumblerSub`'s proof uses `(i)`, `(ii)` with `(ii)` split into `(ii-a)`, `(ii-b)`. `ZPD`'s Relationship-to-Divergence postcondition uses `(i)`, `(ii)` but refers to "sub-case (β) or (γ)".
**Issue**: Even once Divergence is formalized, three different labellings for essentially the same case split invite cross-reference errors. A single canonical labelling anchored at the Divergence claim would tighten the argument. No correctness loss, so OBSERVE.

### Elided composition step in T1 Case 3
**Class**: OBSERVE
**ASN**: T1 part (b) Case 3: "(β) gives `m + 1 ≤ n`, hence `m < n` via NAT-addcompat's `m < m + 1`; (γ) gives `n < m` symmetrically."
**Issue**: Deriving `m < n` from `m < m + 1` and `m + 1 ≤ n` requires NAT-order's `≤`-defining clause followed by transitivity (or substitution in the equality branch) — the same composition the proof spells out explicitly elsewhere (part (c) Case `k₂ < k₁`). The elision is locally recoverable but inconsistent with the document's own standard of explicitness.

VERDICT: REVISE
