# Review of ASN-0069

## REVISE

### Issue 1: V0 Effects citation for "undefined elsewhere" cites the wrong claim

**ASN-0069, §"The Fork Composite", V0 Effects block**: "M'(d_new)(v) undefined for v ∉ V_{s_C}(d_src) (V6)"

**Problem**: V6 establishes only `V_{s_L}(d_new) = ∅` — it excludes link-subspace V-positions, but not arbitrary V-positions in the content subspace that lie outside `V_{s_C}(d_src)`. The exact characterization of `dom(M'(d_new))` is V4b's "domain equality" claim: `dom(M'(d_new)) = V_{s_C}(d_src)`. Without citing V4b, the Effects formula is incomplete — a hypothetical v with `subspace(v) = s_C` but `v ∉ V_{s_C}(d_src)` would not be excluded by V6 alone.

**Required**: Cite V4b as the primary justification, with V6 as a corollary covering link-subspace V-positions specifically.

### Issue 2: V0 Effects citation for R' cites V9 alone, which gives only inclusion

**ASN-0069, §"The Fork Composite", V0 Effects block**: "R' = R ∪ {(a, d_new) : a ∈ ran(M'(d_new))}          (V9)"

**Problem**: V9 asserts `(A a : a ∈ ran(M'(d_new)) : (a, d_new) ∈ R')` — an inclusion `R' ⊇ R ∪ {(a, d_new) : ...}`, not equality. The set equality requires also that no other pairs are added, which depends on K.δ's frame `R¹ = R`, K.μ⁺'s frame `R² = R¹`, and the bound that the n K.ρ steps add exactly the n distinct pairs `{(a_j, d_new)}`.

**Required**: Either cite V9 together with the K.δ and K.μ⁺ frame conditions, or expand V9 to claim set equality (with proof).

### Issue 3: V8a cites P0/S0 but the operative axiom is K.α's arrangement-preservation frame

**ASN-0069, V8a**: "Subsequent K.α allocations (extending C) do not affect existing I-addresses (by P0/S0), so V8's correspondence between d_src and d_new over the V-positions present at fork time is preserved..."

**Problem**: P0/S0 are content-permanence axioms (`dom(C) ⊆ dom(C')`, value preservation). V8's correspondence is about equality of `M(d_src)(v)` and `M(d_new)(v)` — properties of the arrangement, not of C. What preserves V8 across K.α is K.α's frame condition `(A d :: M'(d) = M(d))` — K.α does not modify any arrangement. The citation chain is wrong: P0/S0 govern content-store growth, not arrangement preservation.

**Required**: Replace the P0/S0 citation with K.α's arrangement-preservation frame, and make explicit that since K.α leaves M unchanged, the equality V8 records at the post-fork state persists across K.α steps.

### Issue 4: Notation convention for multiple forks introduced after first use

**ASN-0069, §"Worked Example", "Notation for multiple forks" remark**

**Problem**: The disambiguation between sibling-fork notation (`d_new¹`, `d_new²` — superscript after `_new`) and chain-fork notation (`d¹_new`, `d²_new` — superscript before `_new`) is given in the worked example section, but V10 already uses `d_new¹`/`d_new²` and V11 already uses `d¹_new`/`d²_new` before this remark appears. A reader proceeding linearly through V10 and V11 has no guide to the superscript-position convention until later.

**Required**: Move the "Notation for multiple forks" remark to before V10 (or to the top of the "Independence Among Forks" section), so the convention is established at the point of first use.

### Issue 5: V4 prose precondition is redundant with vacuity

**ASN-0069, V4**: "After a fork of `d_src` with `V_{s_C}(d_src) ≠ ∅`, the new document's content-subspace arrangement satisfies: `(A v ∈ V_{s_C}(d_src) :: v ∈ dom(M'(d_new)) ∧ M'(d_new)(v) = M(d_src)(v))`"

**Problem**: The formal universal `(A v ∈ V_{s_C}(d_src) :: ...)` is vacuously true when `V_{s_C}(d_src) = ∅`, so V4 holds in both the non-empty and empty cases without needing the prose precondition. The prose qualifier "with `V_{s_C}(d_src) ≠ ∅`" suggests V4 has narrower scope than it does, and creates inconsistency with the table entry (which omits the qualifier).

**Required**: Either remove the prose qualifier "with `V_{s_C}(d_src) ≠ ∅`" so V4 holds unconditionally (vacuously in the empty case), or explicitly state that V4 is intentionally restricted to the non-empty case and explain why the empty-case vacuity is not adopted.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork protocol semantics
The "Open Questions" section lists "concurrently modified" forking as future work. This is correctly out of scope — SequentialTransitionAxiom provides the abstract atomicity guarantee; richer concurrent semantics belong in a future replication/protocol ASN.

### Topic 2: Snapshot vs living fork distinction
Listed in "Open Questions". The current V0 is snapshot-style (V10a's time-sensitivity); a living-fork variant would require different axioms about arrangement co-evolution. Future ASN.

### Topic 3: Fork of a transcludent
Listed in "Open Questions". When `M(d_src)` references I-addresses with `origin ≠ d_src`, the provenance recording semantics need additional analysis. Future ASN.

### Topic 4: Version DAG coherence as a collection
Listed in "Open Questions". V11 handles single chains; coherent presentation of the full version space requires separate machinery. Future ASN.

VERDICT: REVISE
