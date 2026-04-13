# Cone Review — ASN-0036/S8 (cycle 3)

*2026-04-13 16:49*

I'll examine the full ASN, tracing every dependency chain across properties.

<tool_call>
<tool_name>Grep</tool_name>
<parameters>
<pattern>TumblerAdd|PositionAdvance|inc\(v|TA5\(a\)|TA5\(b\)</pattern>
<path>/Users/shane/Documents/github/claude/xanadu-spec</path>
<include>*.md</include>
</parameters>
</tool_call>

<tool_call>
<tool_name>Grep</tool_name>
<parameters>
<pattern>S7c|S7b|S3.*Referential</pattern>
<path>/Users/shane/Documents/github/claude/xanadu-spec/vault</path>
<include>*.md</include>
</parameters>
</tool_call>

Let me trace the dependency chains systematically across all properties in the provided ASN content.

**Checking the three user-identified findings against the current text:**

The current S8 proof consistently cites OrdinalShift, not TA5 or TumblerAdd. The S8-depth motivational text mentions TA5(c) but explicitly disclaims it: *"this operational fact is motivation for the definition of correspondence runs, not a dependency of the decomposition proof."* All four S8-depth postconditions cite OrdinalShift. Findings 1 and 3 appear to reference text from a prior revision — the equivocation has been corrected.

Finding 2 (#v ≥ 2 not established) remains valid in the current text.

Now, the new issues:

---

### S8 uniqueness argument depends on natural-number discreteness without a declared foundation for the component domain

**Foundation**: T1 (LexicographicOrder) defines `<` on components; OrdinalShift defines `vₘ + n`; T4 establishes that some components are `0` and others are `> 0`. Together these constrain components to an ordered structure with zero, positivity, and addition — consistent with ℤ, ℚ, or ℝ, not only ℕ.
**ASN**: S8 proof, within-subspace uniqueness, Case j = m: `"Since components are natural numbers, vₘ ≤ tₘ < vₘ + 1 forces tₘ = vₘ."` Cross-subspace m = 1: `"if t₁ > S₁ then t₁ ≥ S₁ + 1"` (discreteness again).
**Issue**: The S8 proof's core uniqueness argument — that no depth-m tumbler besides `v` falls in `[v, v+1)` — hinges on natural-number discreteness: if `n ≤ x < n + 1` for `n, x ∈ ℕ`, then `x = n`. This property is invoked twice (within-subspace Case j = m, and cross-subspace m = 1 case analysis) and stated as `"Since components are natural numbers,"` but no foundation statement declares the component domain as ℕ. The foundation statements establish arithmetic and ordering on components but not the discrete-lattice property that eliminates values between consecutive integers. Without this, the uniqueness proof admits a gap: over ℚ or ℝ components, `[v, v+1)` would contain infinitely many points, and the singleton-interval partition argument fails.
**What needs resolving**: Either add a foundation-level declaration that tumbler components are natural numbers (establishing discreteness as a consequence), or cite the specific ASN-0034 definition that fixes the component domain — so the S8 proof's discreteness claims have a traceable foundation link.

---

### S8-depth postcondition 3 depends on S7c without declaring it as a precondition

**Foundation**: OrdinalShift (ShiftDefinition) — prefix rule: `shift(v, n)ᵢ = vᵢ` for `i < #v`.
**ASN**: S8-depth formal contract postcondition 3: `"I-address subspace preservation: (A k : 0 ≤ k < n : E₁(a + k) = E₁(a)) — S7c guarantees element-field depth δ ≥ 2, placing E₁ outside the action point; OrdinalShift's prefix rule copies it unchanged."`
**Issue**: Postcondition 3 holds only because S7c constrains element-field depth to `δ ≥ 2`, which places the subspace identifier `E₁` strictly before the action point `#a`. At `δ = 1`, `E₁` would *be* the action point — `shift(a, k)` would alter the subspace identifier, and postcondition 3 would be false. S7c is cited inline in the postcondition text but S8-depth's formal contract has no Preconditions section — its structure (Axiom + Definition + Postconditions) implies no dependencies. This is inconsistent: the contract structure signals "no preconditions" while postcondition 3 requires S7c. The parallel V-position postcondition (postcondition 1) correctly guards its weaker case with `"(requires #v ≥ 2)"`, but postcondition 3 presents the I-address case as unconditional, with the S7c dependency hidden in the justification text. Any downstream consumer of postcondition 3 must independently discover the S7c requirement.
**What needs resolving**: Either add a Preconditions section to S8-depth's formal contract declaring S7c as a dependency of postcondition 3, or restructure so the correspondence-run postconditions are a separate property with their own explicit preconditions — separating them from the depth-uniformity axiom that genuinely has none.
