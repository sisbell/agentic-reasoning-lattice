# Cone Review — ASN-0036/D-CTG-depth (cycle 1)

*2026-04-14 20:03*

I've read the foundation statements and the ASN as a whole. Here are the cross-cutting findings.

---

### V_S(d) and subspace() are load-bearing but formally undefined
**Foundation**: Σ.M(d) defines `dom(M(d))` and `ran(M(d))` but not `V_S(d)`
**ASN**: D-CTG invariant: `u ∈ V_S(d) ∧ q ∈ V_S(d)`; D-CTG-depth postcondition: `v₁ ∈ V_S(d) ∧ v₂ ∈ V_S(d)`; S8-depth body text: `V_S(d)` used throughout
**Issue**: The notation `V_S(d)` appears in the formal contracts of three properties (D-CTG invariant, D-CTG-depth preconditions and postcondition, S8-depth discussion) but has no definition block anywhere in the ASN. Similarly, `subspace(v)` appears in D-CTG's formal invariant (`subspace(v) = S`) and is consistently used as `v₁` in prose, but is never given a formal definition. The implicit meaning — `V_S(d) = {v ∈ dom(M(d)) : v₁ = S}` and `subspace(v) = v₁` — is recoverable from context, but formal contracts quantify over `V_S(d)` as if it were a defined term. Without a definition block, two properties could silently diverge on what `V_S(d)` includes (e.g., whether it carries a depth constraint from S8-depth or is purely subspace-filtered).
**What needs resolving**: A definition property (or a definition block within Σ.M(d)) that formally specifies `subspace(v) = v₁` and `V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}`, so that the formal invariants in D-CTG and D-CTG-depth reference a defined term rather than an implicit one.

---

### D-CTG-depth proof constructs intermediates outside T0(a)'s guarantee
**Foundation**: T0(a) (UnboundedComponentValues): "there exists `t' ∈ T` that agrees with `t` at all positions except at position `i`, where `t'.dᵢ > M`" — modifies a single component and guarantees `t' ∈ T`
**ASN**: D-CTG-depth proof: "For any natural number n > (v₁)ⱼ₊₁, define w of length m by: wᵢ = (v₁)ᵢ for 1 ≤ i ≤ j, wⱼ₊₁ = n, wᵢ = 1 for j + 2 ≤ i ≤ m … By T0(a) (UnboundedComponentValues, ASN-0034), unboundedly many values of n > (v₁)ⱼ₊₁ exist."
**Issue**: The proof has two gaps in its use of T0(a). First, w is constructed by modifying positions j+1 through m simultaneously (setting wⱼ₊₁ = n and wᵢ = 1 for i > j+1), but T0(a) modifies a single position and guarantees the result is in T. The constructed w is not the tumbler that T0(a) produces, and its membership in T is never established — yet D-CTG's universal quantifier ranges over T, so w ∈ T is required for D-CTG to force w ∈ V_S(d). Second, T0(a) is cited for "unboundedly many values of n exist," which is a property of ℕ, not something T0(a) is needed for. What T0(a) actually provides — and what the proof needs — is membership in T. A simpler construction avoids both gaps: apply T0(a) directly to v₁ at position j+1 with bound M, obtaining t' ∈ T that differs from v₁ only at position j+1. This t' satisfies subspace(t') = S (position 1 preserved since j+1 ≥ 3), #t' = m, v₁ < t' < v₂ (ordering decided at position j+1 for the lower bound and at position j for the upper bound), and t' ∈ T (by T0(a)'s postcondition).
**What needs resolving**: The proof must either establish that T contains all finite sequences of ℕ₀ (making the current construction valid by definition) or use T0(a)'s single-component modification directly, which provides T-membership as part of its postcondition and makes the multi-component construction unnecessary.

---

### Starting-ordinal constraint is asserted but has no formal status
**Foundation**: T4 (HierarchicalParsing): "every non-separator component is strictly positive" — gives ordinals ≥ 1 but not = 1
**ASN**: D-CTG-depth text: "Nelson's statement specifies not just contiguity but also the starting ordinal: 'addresses 1 through 100,' not '42 through 141.' All ordinal numbering in the tumbler system starts at 1 … V-positions follow the same convention."
**Issue**: The text asserts that V-position ordinals start at 1, citing Nelson's design and T4's exclusion of zero. But no formal contract in the ASN captures this. D-CTG guarantees no gaps; S8-fin guarantees finiteness; T4's positive-component constraint gives a lower bound of 1 on non-separator components. Together these establish that V_S(d) occupies a contiguous block {prefix.a, prefix.(a+1), …, prefix.N} with a ≥ 1 — but nothing forces a = 1. The starting ordinal of 1 is a convention that the formal contracts cannot derive. If operation ASNs rely on this convention (e.g., INSERT placing the first character at ordinal 1), they have no formal property to cite.
**What needs resolving**: Either formalize the base-ordinal constraint as an invariant (e.g., "for non-empty V_S(d), the minimum value of the last component is 1") or acknowledge that the starting ordinal is an operation-level obligation and remove the assertion from D-CTG-depth's text, deferring it to the operation specifications where it can be discharged.
