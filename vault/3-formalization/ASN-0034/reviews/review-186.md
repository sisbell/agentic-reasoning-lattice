# Cone Review — ASN-0034/TA5a (cycle 1)

*2026-04-17 18:38*

### TA5-SigValid cites only T0 for "non-zero ⇒ strictly positive" in ℕ
**Foundation**: T0 (CarrierSetDefinition) — supplies ℕ as carrier but does not license the strict-positivity inference. The NAT-* axioms are stated as separate foundation objects precisely to carry those inferences.
**ASN**: TA5-SigValid proof:
> "T4's field-segment constraint requires `t_{#t} ≠ 0`, so the last component is non-zero; and since `t_{#t} ∈ ℕ` by T0, `t_{#t} ≠ 0` entails `t_{#t} > 0`."

TA5-SigValid's *Depends* lists only T4, T0, TA5-SIG — no NAT-* axioms.
**Issue**: The step "`t_{#t} ∈ ℕ` and `t_{#t} ≠ 0` ⟹ `t_{#t} > 0`" is exactly the inference that T4a, T4, and T4c discharge by explicitly citing NAT-zero (`0 ≤ n` on ℕ) jointly with NAT-discrete (instantiated at `m = 0` to rule out `0 ≤ n < 1`). TA5-SigValid performs that same inference but cites only T0, which on its own supplies the carrier but not the discreteness property that rules out `0 < n < 1`. The ASN's own convention — set in T0's contract and followed in T4a's Depends prose — is that ℕ-facts used in a proof appear as explicit NAT-* citations. TA5-SigValid breaks that convention, leaving the "`> 0`" step unsourced under the ASN's stated standard. (The downstream chain through TA5a, which routes this positivity via TA5-SigValid for the case `k = 1`, inherits the gap.)
**What needs resolving**: TA5-SigValid's Depends list must either (a) add NAT-zero and NAT-discrete to match the per-step citation convention used for this same inference elsewhere in the ASN, or (b) reformulate the proof so that only "`t_{#t} ≠ 0`" is used (since membership of `#t` in `{i : tᵢ ≠ 0}` needs non-zeroness, not strict positivity), eliminating the `> 0` step and its missing citations.
