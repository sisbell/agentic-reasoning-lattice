# Review of ASN-0069

The proof apparatus here is genuinely thorough: V1's two inductions, the B8 precondition discharge in §"Identity by Sub-Allocation", the ValidComposite★ verification with its per-sub-case K.δ freshness arguments, and the V11 chain induction all hold up under scrutiny. The boundary cases that usually get hand-waved — empty source (V7), single-position content subspace, subsequent-fork operand divergence (`d_op = d_prev ≠ d_src`), deletion-then-fork — are each handled explicitly. I found no rigor gap.

The remaining findings are accreted meta-prose around forward references and document structure, which this note's `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Worked-example empty-source paragraph restates the quantifier-domain principle and adds a back-pointer
**ASN-0069, §"Worked Example", "Empty source (V7)" paragraph**: "the dependent properties (V9, V12(c), V12(d)) degrade to vacuity while the structural ones (V1, V2, V3, V12(a)) hold substantively, for the quantifier-domain reasons established in §'The Empty-Source Case' — which need not be re-run here."

**Problem**: §"The Empty-Source Case" already states the organising principle in full ("The single organising principle is quantifier domain: the structural properties — V1... — hold substantively... while every property whose universal quantifier ranges over `V_{s_C}(d_op)`... holds vacuously"). The worked-example paragraph re-states the same substantive/vacuous classification and then defers back to the section that established it ("need not be re-run here"). An example should exhibit the concrete outcome, not re-derive the meta-classification and point at its own source. This is the "two paragraphs say the same thing in different words" + deferral pattern compounded.

**Required**: In the worked example, keep only the concrete outcome (`d_new° = inc(d_src°, 1)`, `M'(d_new°) = ∅`, `R' = R`, and the independent-continuation observation). Drop the property-by-property substantive/vacuous restatement and the "for the quantifier-domain reasons established in §... — which need not be re-run here" clause.

### Issue 2: Dependency Audit defends the dependency list rather than advancing reasoning
**ASN-0069, §"Dependency Audit"**: "ASN-0040 ... is consumed in §'Identity by Sub-Allocation', which grounds version identity in NextAddress, B6 (ValidDepth), B8 (Uniqueness), and B9 (UnboundedExtent) — the consumption argument and the B8 precondition discharge are given there and not repeated here. ASN-0040 is correctly retained."

**Problem**: The clause "the consumption argument and the B8 precondition discharge are given there and not repeated here" is meta-prose about document layout, and "ASN-0040 is correctly retained" is a self-justification of the dependency list. Neither advances the specification; both exist to defend that the dep audit was performed. This is the defensive-justification / document-ordering-rationale pattern.

**Required**: Reduce to a statement of fact: each declared dependency is consumed, naming where (e.g., "ASN-0040 supplies NextAddress, B6, B8, B9, consumed in §'Identity by Sub-Allocation'"). Drop "not repeated here" and "correctly retained."

### Issue 3: Notation block enumerates its own downstream consumers
**ASN-0069, §"Independence Among Forks", "Notation for multiple forks" remark**: "The conventions are used uniformly in V10, V11, and the worked example."

**Problem**: This is a downstream-consumer inventory — it lists where the convention is later used rather than advancing the convention's meaning. (Distinct from the previously-declined finding about *moving* this block; this is about deleting one inventory sentence within it, not relocating the block.) The disambiguating content — superscript-before vs superscript-after, and the length distinction `#d_src + 1` vs `#d_src + 2` — fully defines the convention without the use-site list.

**Required**: Delete the "used uniformly in V10, V11, and the worked example" sentence; retain the superscript-position rule and the length distinction.

## OUT_OF_SCOPE

### Topic 1: Concurrent-modification guarantees during a fork
The first and second Open Questions (concurrent source modification, descendant discoverability with time bounds) reach beyond the sequential atomic-transition model this ASN inhabits. Correctly parked as open questions, not errors here.

### Topic 2: Snapshot vs living forks; renumbering inherited V-positions for compactness
V4's literal-inheritance commitment (`m'_{s_C} = m_{s_C}(d_op)`) fixes one discipline; the alternative (depth-renumbering, living forks) is acknowledged in the Open Questions and belongs to a future ASN.

VERDICT: REVISE
