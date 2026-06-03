# Review of ASN-0069

## REVISE

### Issue 1: V10(b) invokes V5a without discharging its `d* ∈ Σ.E_doc` hypothesis
**ASN-0069, §"Independence Among Forks", V10(b)**: "Both preservation directions — modifications M-targeted at `d_new¹` preserve `M(d_new²)`, and vice versa — are V5a instantiated at `d* = d_new²` and at `d* = d_new¹` respectively, valid because a step targeting one sibling does not target the other (`d_new¹ ≠ d_new²` by V10(a))."

**Problem**: V5a's stated hypothesis is two-part: *(i)* `d* ∈ Σ.E_doc` in the initial state of the considered sequence, and *(ii)* no step is M-targeted at `d*`. The cited validity ("a step targeting one sibling does not target the other") discharges only *(ii)*. For the direction "modifications M-targeted at `d_new¹` preserve `M(d_new²)`," V5a is instantiated at `d* = d_new²`, but `d_new²` is created at `Σ²` — so the membership `d_new² ∈ Σ.E_doc` holds only for sequences whose initial state is at or after `Σ²`. The discharge omits this; as written the instantiation does not pin the state range over which the independence is asserted.

**Required**: In V10(b), restrict the preservation claims to sequences beginning at a state where both siblings are in `E_doc` (i.e., at or after `Σ²`), and discharge V5a's `d* ∈ E_doc` hypothesis at that initial state via P1 (as V5/V5a do elsewhere), not only the targeting-distinctness hypothesis.

### Issue 2: Worked example re-explains the `d_new²` / `d²_new` notation already fixed in the notation block
**ASN-0069, §"Worked Example", subsequent-fork paragraph**: "The sibling-notation `d_new²` distinguishes this second sibling fork of `d_src` — of length `#d_src + 1`, parent `d_src` in the version sub-allocator — from any chain notation; in particular, `d_new² ≠ d²_new` of the prior paragraph (which has length `#d_src + 2` and parent `d_new` in its sub-allocator)."

**Problem** (anti-bloat — two paragraphs saying the same thing): The §"Independence Among Forks" notation block already states the full distinction: "`d_new²` is the second sibling fork of `d_src`; `d²_new` is the second link in a fork chain... `d_new²` has length `#d_src + 1`... while `d²_new` has length `#d_src + 2`." The worked example restates the sibling-vs-chain distinction, both length values, and the inequality — content the reader was already given. The worked example's job is to *use* the convention on a concrete instance (`d_new² = inc(d_new, 0) = p.2`), not to re-derive the convention.

**Required**: Drop the re-explanation; let the worked example apply the established notation (the concrete `p.1` / `p.2` exhibition two sentences later already does the useful work). This is duplication, distinct from the notation-block *placement* (which is correct and not in question).

### Issue 3: Essay flourish in §"Composability" restates V8c
**ASN-0069, §"Composability: Fork of a Fork", closing paragraphs**: "There is no accumulation of state, no recursion, no per-chain bookkeeping... Siblings, ancestors, descendants, cousins — the relationship is irrelevant to the comparison machinery, because the I-addresses carry the relationship structurally."

**Problem** (anti-bloat — essay content restating a named property): The "relationship is irrelevant" sentence restates V8c (*correspondence is symmetric and document-type-untyped*) in rhetorical form. The enumeration "Siblings, ancestors, descendants, cousins" advances no reasoning beyond V8c's symmetry/untypedness, which the section has already established by citation.

**Required**: Compress to a single sentence pointing to V8c (intercomparison along the fork tree reduces to I-address equality, relationship-independent per V8c), and drop the rhetorical enumeration.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork / source-modification semantics beyond sequential atomicity
The Open Questions raise concurrency (Q1) and multi-step interleaved deletion (Q9). These are correctly deferred — they require a concurrency model the sequential-transition substrate does not yet supply, and belong in a future ASN.

### Topic 2: Snapshot vs. living fork distinction
Q3's snapshot/living-fork invariants are new territory (the present ASN commits to snapshot-at-fork-time via V10a) and rightly left to a future ASN.

VERDICT: REVISE
