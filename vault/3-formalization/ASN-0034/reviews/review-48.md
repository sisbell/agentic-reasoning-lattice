# Cone Review — ASN-0034/TumblerSub (cycle 2)

*2026-04-15 13:19*

I'll read the full ASN carefully, tracing every cross-reference and precondition chain.

<tool_call>
<tool_name>Read</tool_name>
<parameter name="file_path">/Users/shane/Documents/github/claude/xanadu-spec/vault/project-model/ASN-0034/formal-statements.md</parameter>
</tool_call>

<tool_call>
<tool_name>Glob</tool_name>
<parameter name="pattern">vault/3-formalization/ASN-0034/**/*.md</parameter>
</tool_call>

<tool_call>
<tool_name>Glob</tool_name>
<parameter name="pattern">vault/project-model/ASN-0034/**/*</parameter>
</tool_call>

After careful analysis of the entire ASN as a system — tracing every definition through every use, every precondition chain from caller to callee, and every case analysis against the actual domain — I find one new cross-cutting issue.

### D0's elimination of Divergence case (ii) asserts an inequality that holds only after an unstated appeal to T1's ordering direction

**Foundation**: Divergence definition (case (ii): `divergence(a, b) = min(#a, #b) + 1` when all shared components agree and `#a ≠ #b`); T1 (LexicographicOrder, case (ii): prefix is less than extension)
**ASN**: D0 (DisplacementWellDefined) — *"The hypothesis k ≤ #a eliminates Divergence case (ii), which would require k = min(#a, #b) + 1 ≥ #a + 1 > #a."*
**Issue**: The inequality `min(#a, #b) + 1 ≥ #a + 1` requires `min(#a, #b) ≥ #a`, i.e., `#b ≥ #a`. The Divergence definition's case (ii) permits both `#a < #b` and `#b < #a` (it requires only `#a ≠ #b`). The proof's inequality chain covers the `#a < #b` sub-case (where `min = #a` and the chain holds with equality) but does not address the `#b < #a` sub-case, where `min(#a, #b) = #b < #a` and `k = #b + 1` could satisfy `k ≤ #a`.

The `#b < #a` sub-case is indeed impossible under D0's hypotheses, but the argument is different from the one the proof gives: Divergence case (ii) with `#b < #a` means all shared components agree and `b` is shorter, so `b` is a proper prefix of `a`; T1 case (ii) then yields `b < a`, contradicting D0's hypothesis `a < b`. This is a T1-ordering-direction argument, not an arithmetic inequality — yet the proof presents a single inequality chain as the sole justification, and that chain's intermediate step `min(#a, #b) + 1 ≥ #a + 1` is false when `#b < #a`.

The gap is cross-cutting: D0's case elimination depends on the interaction between the Divergence definition (which is direction-agnostic — case (ii) applies regardless of which tumbler is shorter) and T1's ordering semantics (which forces the prefix to be the lesser tumbler), but the proof cites neither T1 nor the ordering direction at this step.

**What needs resolving**: The case elimination must either (a) explicitly establish that `a < b` forces `#a < #b` in Divergence case (ii) (via T1 case (ii)), making `min(#a, #b) = #a` and the inequality valid; or (b) split into two sub-cases — `#a < #b` (eliminated by `k = #a + 1 > #a`) and `#b < #a` (eliminated by the T1 contradiction with `a < b`).
