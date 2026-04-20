# Cross-cutting Review — ASN-0034 (cycle 1)

*2026-04-08 10:16*

I've read this ASN end-to-end, tracing definitions, precondition chains, and case analyses across all 60+ properties. Here are the cross-property issues that per-property checks cannot see.

### TumblerSub tail-copy rule silent on zero-padding beyond #a
**Foundation**: (internal consistency — TumblerSub definition)
**ASN**: TumblerSub definition: "rᵢ = aᵢ if i > k (copy from end position)" and "The result has length max(#a, #w)"
**Issue**: The definition states that zero-padding applies "before scanning for divergence" but does not extend this convention to the tail-copy rule. When `#w > #a`, the result has positions `i` with `#a < i ≤ max(#a, #w)` where `aᵢ` does not exist in the original tumbler. The TA2 proof correctly interpolates "(zero-padded)" — writing "rᵢ = aᵢ (zero-padded). If i > #a, then aᵢ = 0 ∈ ℕ (zero-padded)" — but the definition text never authorizes this reading. The TA3 and TA7a proofs similarly rely on zero-padded tail values without the definition granting them. A formalizer reading the definition literally would find the result undefined at positions beyond `#a`.
**What needs resolving**: The TumblerSub definition must state that all component references — divergence scan AND tail copy — use zero-padded values, or equivalently define `aᵢ = 0` for `i > #a` throughout the subtraction procedure.

### Formal Divergence and TumblerSub's zero-padded divergence are distinct but conflated
**Foundation**: Divergence definition vs TumblerSub definition
**ASN**: TA3 Verification: "d_a = divergence(a, w) is well-defined. The divergence d_b = divergence(b, w) is also well-defined" — then used as TumblerSub's computation points
**Issue**: The formal **Divergence** definition gives `divergence(a, b) = min(#a, #b) + 1` when one tumbler is a proper prefix of the other (case ii). TumblerSub finds the first position where the *zero-padded* sequences disagree, which can be strictly deeper — e.g., `a = [1, 2, 0, 5]`, `w = [1, 2]`: formal Divergence gives 3 (prefix exhaustion), but zero-padded divergence gives 4 (first nonzero extension). The TA3 Verification writes `d_a = divergence(a, w)` using the formal definition's name but needs TumblerSub's zero-padded value for its structural reasoning ("for i < d, both results are zero" and "at position d: compute a_d − w_d"). When the two values differ, TumblerSub zeros position d_formal (it's before d_zeropadded) rather than applying the subtraction formula — the numerical result coincides (both give 0, since a_d = w_d at the formal divergence point), but the derivation is structurally wrong. D0 correctly connects the two concepts by restricting to Divergence case (i) where they agree, but TA3 does not establish this restriction in its broader case analysis.
**What needs resolving**: Either (a) define the zero-padded divergence as a named concept distinct from the formal Divergence, and have TumblerSub and TA3 reference it explicitly, or (b) establish within the TA3 proof that under Case B conditions (component divergence at j between a and b), the formal Divergence and zero-padded divergence of (a, w) coincide — which they do, since the existence of j ≤ min(#a, #b) forces d ≤ j ≤ min(#a, #b), placing the divergence in case (i).

### PartitionMonotonicity misattributes the sub-partition sibling stream
**Foundation**: T10a (AllocatorDiscipline)
**ASN**: PartitionMonotonicity proof: "The first child prefix t₀ is produced by inc(s, k) with k > 0 … The parent's output stream then resumes with inc(·, 0) (T10a): t₁ = inc(t₀, 0), t₂ = inc(t₁, 0), and so on"
**Issue**: Under T10a, after spawning a child via `inc(s, k')`, the parent's own sibling stream resumes from `s` with `inc(s, 0)` — producing the next parent-level sibling. The sequence `t₁ = inc(t₀, 0), t₂ = inc(t₁, 0), …` is the **child-level allocator's** sibling stream starting from the child prefix `t₀`, not the parent's resumed stream. The proof attributes this sequence to "the parent's output stream" when it is produced by a different allocator at a deeper hierarchical level. The mathematical conclusions (uniform length, non-nesting, cross-partition ordering via PrefixOrderingExtension) hold regardless of which allocator produces the sequence — the properties follow from TA5 and T10a applied to any allocator — but the narrative creates a false model of the allocation hierarchy that could mislead implementers about which entity owns the sub-partition prefix stream.
**What needs resolving**: Clarify that t₀, t₁, t₂, … are produced by the child-level allocator's sibling stream (starting from the child prefix established by the parent's single `inc(·, k')` operation), and that the parent's own sibling stream continues independently at the parent level.

## Result

Not converged after 1 cycles.

*Elapsed: 1278s*
