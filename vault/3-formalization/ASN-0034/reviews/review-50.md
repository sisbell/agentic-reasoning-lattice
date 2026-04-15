# Cone Review — ASN-0034/D0 (cycle 2)

*2026-04-15 14:23*

I'll read the formal statements and project model for full context.

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

After reading the entire ASN as a system — tracing every identifier, every precondition chain from caller to callee, and every case analysis against the domain as defined — I find one new cross-cutting issue.

### D0's postcondition equates actionPoint(b ⊖ a) with divergence(a, b), but TumblerSub computes via zpd(b, a), and the identity zpd = divergence is asserted without proof or formal definition of either concept

**Foundation**: TumblerSub definition (zpd-based construction), T1 (LexicographicOrder)
**ASN**: D0 (DisplacementWellDefined) — postcondition *"actionPoint(b ⊖ a) = divergence(a, b)"*; proof step *"the first divergence between minuend b and subtrahend a is at position k. TumblerSub yields: wᵢ = 0 for i < k, wₖ = bₖ − aₖ, wᵢ = bᵢ for i > k"*
**Issue**: TumblerSub's construction is parameterized by `zpd(b, a)` — the first position where the *zero-padded* sequences disagree. D0's precondition and postconditions are parameterized by `divergence(a, b)` — the first position where `a` and `b` disagree under T1's case structure, which treats length exhaustion (Divergence case (ii): one tumbler runs out of components) as a distinct kind of divergence from component inequality at a shared position. These are different concepts: `divergence` can yield `k = min(#a, #b) + 1` in the prefix case, while `zpd` would yield a different position (the first non-zero component of the longer tumbler beyond the shared range) or be undefined.

D0's proof eliminates Divergence case (ii), leaving case (i) with `k ≤ min(#a, #b)`. It then asserts — in one sentence — *"the first divergence between minuend b and subtrahend a is at position k"* and proceeds to read off TumblerSub's output. This sentence is the bridge: it silently identifies `zpd(b, a) = k = divergence(a, b)`. The identity holds because `k ≤ min(#a, #b)` guarantees both tumblers have actual (non-padded) components at all positions up to `k`, so zero-padding is irrelevant and the two notions of first-disagreement coincide. But this justification is never stated.

The gap is cross-cutting in two ways. First, neither `divergence` nor `zpd` is formally defined in the ASN — both are invoked as named properties (`Divergence` with case (i)/(ii), `ZPD`) that the ASN uses but does not establish, despite declaring no dependencies. Second, the identity between them is not a tautology but a theorem that depends on D0's specific case elimination; the proof chain from D0's postcondition `actionPoint(b ⊖ a) = divergence(a, b)` passes through `actionPoint(b ⊖ a) = zpd(b, a)` (from TumblerSub's construction) and then `zpd(b, a) = divergence(a, b)` (unproven), and any downstream consumer of D0's postcondition inherits this unstated link.

**What needs resolving**: The ASN must either (a) formally define both `divergence` and `zpd`, prove their equivalence under Divergence case (i) — specifically that `k ≤ min(#a, #b)` with component disagreement at `k` implies `zpd = divergence = k` — and cite this equivalence explicitly in D0's proof; or (b) unify the parameterization so that TumblerSub and D0 share a single formally-defined divergence concept, eliminating the implicit bridge.
