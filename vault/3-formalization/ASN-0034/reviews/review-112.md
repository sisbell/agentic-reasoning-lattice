# Cone Review — ASN-0034/D1 (cycle 2)

*2026-04-16 22:53*

### D1 does not cite ActionPoint despite directly invoking it
**Foundation**: N/A — internal property cross-reference
**ASN**: D1 proof: *"Third, the action point of w is k: every component before position k is zero, and wₖ > 0, so k is the first positive component. Since k ≤ #a by hypothesis, the precondition of TumblerAdd (TA0) is satisfied — the action point falls within the start position's length."* D1's Depends clause lists Divergence, T1, ZPD, TumblerSub, TA-Pos, TA0, TumblerAdd, T3 — ActionPoint is absent.
**Issue**: The proof directly computes `actionPoint(w) = k` by exhibiting `k` as the least index with a nonzero component. That is precisely the ActionPoint definition, not a consequence routed through TA0 or TumblerAdd (TA0 *consumes* ActionPoint internally but does not re-export the action-point-identification step as one of its postconditions; TumblerAdd binds `k = actionPoint(w)` but D1 is establishing that binding, not reading it off). The per-step citation convention used throughout this ASN — visible in TumblerAdd explicitly citing T0 for each well-ordering step, and in TumblerSub naming ActionPoint for the analogous identification `actionPoint(a ⊖ w) = zpd(a, w)` — makes this omission a live gap rather than a routed dependency.
**What needs resolving**: Either add ActionPoint to D1's Depends with the ground naming the action-point-identification step of the proof, or rewrite the "action point of w is k" sub-argument so it reads off a postcondition of a property already cited, rather than computing the action point from first principles.

---

### ZPD does not cite T0 despite defining itself via `min {k : …}` over ℕ
**Foundation**: N/A — internal dependency chain
**ASN**: ZPD formal contract: *"Definition: Pad to length L = max(#a, #w): aᵢ = 0 for i > #a, wᵢ = 0 for i > #w. If (A i : 1 ≤ i ≤ L : aᵢ = wᵢ), zpd(a, w) is undefined. Otherwise, zpd(a, w) = min {k : 1 ≤ k ≤ L ∧ aₖ ≠ wₖ}."* Depends lists only Divergence.
**Issue**: The definition names a least element of a subset of ℕ, and the padding clause posits `0 ∈ ℕ` as an extension component — both load-bearing uses of T0 (well-ordering of ℕ; ℕ containing 0 as an element available for padding). The document's convention — visible in TumblerAdd's dependency entry pedantically citing T0 for the "least such j" well-ordering — treats these as per-step dependencies that must be named. ZPD's Depends omits T0 entirely, so the minimality inside its own definition, and the fact that padded components are ℕ-valued, are licensed by no cited source. Downstream properties (TumblerSub, D1) that invoke zpd inherit a dependency cone with T0 missing at this node.
**What needs resolving**: Either add T0 to ZPD's Depends with a ground identifying (i) the well-ordering that licenses `min {k : …}` and (ii) the ℕ-membership of the zero-padded components, or reformulate the contract so the minimality and padding constructions are fully transparent consequences of Divergence alone without invoking T0.

---

### Divergence does not cite T0 despite using well-ordering to name "the least such k"
**Foundation**: N/A — internal dependency chain
**ASN**: Divergence symmetry argument: *"In case (i), the condition `aₖ ≠ bₖ` with agreement on all prior components is unchanged by swapping `a` and `b`, so the least such `k` is the same."* Divergence's Depends lists only T3.
**Issue**: Case (i) of the definition quantifies over a `k` at which the sequences first diverge, and the symmetry postcondition asserts that the least such `k` is preserved under argument swap. Both steps rely on well-ordering of ℕ applied to the subset `{i : 1 ≤ i ≤ min(#a, #b) ∧ aᵢ ≠ bᵢ}` — a use of T0 exactly parallel to what TumblerAdd's Depends clause names explicitly ("invokes T0's well-ordering of ℕ applied to the nonempty subset {j : …}"). Divergence omits this citation, breaking the per-step convention and leaving "the least such k" ungrounded.
**What needs resolving**: Either add T0 to Divergence's Depends with a ground identifying the well-ordering step that names the least divergence index (and the ℕ-membership of `min(#a, #b) + 1` in case (ii)), or reformulate the case (i) witness and the symmetry argument so they do not appeal to minimality.
