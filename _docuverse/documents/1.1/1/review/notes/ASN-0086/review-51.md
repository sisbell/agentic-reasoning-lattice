# Review of ASN-0086

## REVISE

### Issue 1: SharedDepthOneAllocator step (d) carries an unused conditional-independence claim

**ASN-0086, Setup, SharedDepthOneAllocator lemma, step (d)**: "T10a's at-most-once constraint is keyed on spawn pairs `(t, k')`, so its joint constraint binds only when two child-spawns share the same parent-tumbler-and-parameter pair; distinct spawn pairs are independent under T10a, and the two depth-2 allocators evolve without joint constraint."

**Problem**: The naming convention `A_{d.0.s_L.1}` introduced in step (d) is consumed (R0 Step 2 Case A step (iii), R0a Stage 3 same-home case), but the conditional-independence claim about `A_{d.0.s_C.1}` and `A_{d.0.s_L.1}` evolving without joint constraint is not consumed by any subsequent proof in the note. No downstream argument requires this fact.

**Required**: Retain only the naming convention (which step (c) can absorb) and drop the conditional-independence content, or relocate the independence claim to a lemma whose consumer is named.

### Issue 2: R0 Step 4's L11b verification is defensive prose for a non-obligation

**ASN-0086, R0 Step 4**: "*L11b (NonInjectivity):* a permission allowing distinct addresses to store equal triples; the emission introduces no constraint forbidding this and so cannot violate it."

**Problem**: L11b is an existential permission, not a universal invariant requiring preservation. The "cannot be violated" framing imagines a discharge obligation that the L11b statement itself excludes. The same Step 4 already has an "L-permissions (not invariants requiring preservation)" paragraph that explicitly classifies L4(c), L7, L9, L10 as not needing preservation; L11b is structurally the same kind of statement.

**Required**: Move L11b into the L-permissions paragraph, or drop the entry entirely. The current placement among per-invariant discharges treats it as an obligation that does not exist.

### Issue 3: Implementation hypothesis justification explains why-needed rather than what

**ASN-0086, Setup, Implementation hypotheses, Sparse-allocator hypothesis**: "Stronger than T10a alone, which constrains child-spawn pairs to at-most-once but is silent on whether sibling-stream enumeration requires materialized intermediate deposits."

**Problem**: The hypothesis itself was stated in the preceding sentence. The "Stronger than T10a alone" sentence is comparative-justification meta-prose — explaining why this hypothesis is needed beyond T10a rather than what the hypothesis says. R0 Step 2 cites the hypothesis directly; the comparison to T10a adds no operative content for that consumer.

**Required**: Drop the comparative sentence. The hypothesis stands on its own; consumers see it used in R0 Step 2 and Emit_K's emission discipline.

### Issue 4: Nullify's "Why no content address lies under a" paragraph imagines an excluded case

**ASN-0086, Three Operations, Nullify**: "*Why no content address lies under `a`.* The unrestricted coverage `{t : a ≼ t}` ranges over all of `T`, so one must also account for tumbler positions in `A_doc^{Σ'}`."

**Problem**: `nullified(Σ')` is defined to collect only `a' ∈ A_rel^{Σ'}` — content addresses cannot enter `nullified` by the definition itself. The paragraph proceeds to discharge `a ≼ c` for `c ∈ A_doc^{Σ'}` via subspace-distinctness, but `nullified`'s carrier already excludes that case. The exclusion is structural in the Definition, not a follow-on obligation.

**Required**: Either drop the paragraph (the carrier discharges it), or compress to a sentence noting that `nullified`'s `A_rel`-restriction makes the content-side intersection irrelevant to nullification itself; the subspace-distinctness argument can be kept as a one-liner if "unrestricted intersection = {a}" is genuinely useful elsewhere.

VERDICT: REVISE
