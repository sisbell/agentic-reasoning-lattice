# Cone Review — ASN-0034/TA2 (cycle 3)

*2026-04-18 12:08*

### TumblerSub's Depends omits T3 despite using it to derive `a ≠ w` from padded-inequality, and to justify the length-based round-trip failure in the motivation

**Foundation**: T3 (CanonicalRepresentation) — "Tumbler equality is sequence equality: `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`." TA2's Depends cites T3 for exactly this purpose: "the proof concludes `a ≠ w` from the existence of a padded divergence: if `a = w` by T3, the padded sequences would be identical, contradicting the case hypothesis."

**ASN**: TumblerSub. The precondition-consequence proof reads: "Since zpd is defined, `a` and `w` are not zero-padded-equal (ZPD), so in particular `a ≠ w`; combined with `a ≥ w`, this yields `w < a` (T1)." The motivation also reads: "TumblerAdd's result-length identity gives `#(a ⊕ (b ⊖ a)) = #a > #b`, so `a ⊕ (b ⊖ a) ≠ b` by T3 — the round-trip fails on length alone even when the zpd constraint is satisfied." Depends list: T0, T1, Divergence, ZPD, TA-Pos, ActionPoint, NAT-sub, NAT-zero, NAT-order — no T3.

**Issue**: The step "not zero-padded-equal ⟹ `a ≠ w`" is the contrapositive of "`a = w` ⟹ padded sequences identical," which requires T3's characterization of tumbler equality as componentwise sequence equality. Without T3, there is no basis for transporting the tumbler-level equality `a = w` to componentwise identity of the padded sequences. TA2 cites T3 for the identical step; TumblerSub does not. The motivation additionally invokes T3 by name to conclude `≠` from a length difference, which is the reverse direction of T3 (distinct lengths imply distinct tumblers) — also requiring a T3 citation under the ASN's per-step convention.

**What needs resolving**: TumblerSub must either add T3 (CanonicalRepresentation) to its Depends enumeration with per-site accounting (precondition-consequence's not-padded-equal-to-`a ≠ w` step, and the motivation's length-difference-to-`≠` step), or the ASN must adopt a convention under which these steps do not require T3 — and TA2's current T3 citation for the structurally identical step must then be removed in mirror. One meaning per axiom-discharge convention across the document.
