# Review of ASN-0086

I reviewed the substrate emission primitive, the R0/R0a discipline structure, every preservation argument in R0 Step 4, the active/audit machinery in R6a–R6c-Corollary, the R7a/R7b decomposition, and the worked sketch's concrete instantiation.

## REVISE

### Issue 1: R6c-Corollary's frame derivation has a small layering inconsistency

**ASN-0086, R6c-Corollary proof prose**: The Scoping note above the R6c statement says "`Σ'.L = Σ.L` follows from L12 (LinkImmutability, ASN-0043) — which forbids modification of existing link entries — together with L12a (LinkStoreMonotonicity, ASN-0043) — which permits only domain-extension at link entries, and since the arrangement-modifying transition class produces no link emission (its sole effect is on `Σ.M(d)`'s arrangement value), no link extension occurs."

**Problem**: The third premise ("arrangement-modifying class produces no link emission") is class-definitional in ASN-0036, so `Σ'.L = Σ.L` follows from the class definition alone — L12 and L12a are redundant for this frame component. The text presents them as load-bearing, but they only justify the *consistency* of the frame with the L-invariants, not the frame itself. Elsewhere in the same paragraph the ASN correctly notes "This frame is part of ASN-0036's definition of the arrangement-modifying transition class and is inherited here without re-derivation," which contradicts the immediately preceding derivation prose.

**Required**: Reconcile the two passages. Either drop the L12/L12a citations from the `Σ'.L = Σ.L` derivation (the class definition suffices), or recast L12/L12a as the invariants the class definition is consistent with rather than premises of the frame.

### Issue 2: Worked Sketch Step 5.2 silently introduces an unspecified arrangement-modifying transition

**ASN-0086, Worked Sketch, Step 5 (concrete) sub-step 5.2**: "perform any arrangement modification on `Σ_4.M(d)` (e.g., an INSERT operation as defined by an editing-operation ASN extending ASN-0036)."

**Problem**: The worked sketch otherwise instantiates every state component with concrete tumbler values and verifies every L-invariant. Sub-step 5.2's appeal to "any arrangement modification" punts the concrete content of the `↦` step — including the value of `Σ_4.M(d)` before and after the modification, and the editing operation invoked — to a forward reference. For a sketch whose stated purpose is to exhibit R6c-Corollary's content concretely, this is a hand-wave at exactly the substrate transition the corollary is supposed to handle. The reader cannot verify that `Σ_4.M(d)` actually admits an arrangement-modifying step in the constructed state (the sketch never populates `Σ.M(d)` with any arrangement entries, so the prior-state arrangement is unspecified).

**Required**: Either populate `Σ.M(d)` with one or two concrete arrangement entries and exhibit a specific arrangement-modifying step (e.g., INSERT at a specific V-position with a specific I-address), or state explicitly that sub-step 5.2 is *only* a structural argument that the frame-preservation reasoning works *whenever* such a step exists, with concrete realization deferred.

### Issue 3: R0 Step 2 Case A's `s_L`-th sibling sweep deserves an explicit T4-validity invocation

**ASN-0086, R0 Step 2 Case A (chain step ii)**: "Sibling sweep `inc(·, 0)` within `A_d`, advancing from `A_d`'s base `d.0.1` (its first emission, enumeration index 1 at element-field depth 1) to `d.0.s_L` (enumeration index `s_L` at the same depth), applied `s_L − 1` times — each step is a `k = 0` sibling advance within `A_d`, unconditionally T4-preserving (TA5a, ASN-0034)..."

**Problem**: TA5a guarantees T4-preservation per step for `k = 0`, but the sweep applies the increment `s_L − 1` times. The induction that intermediate addresses `d.0.1, d.0.2, …, d.0.s_L − 1` are each T4-valid as inputs to the next increment is not explicit. For arbitrary `s_L`, the chain length grows with `s_L`, and each intermediate `d.0.j` for `1 ≤ j < s_L` must satisfy TA5a's input precondition (T4-validity) to license the next step. The argument is sound — TA5a is unconditional for `k = 0` and the seed `d.0.1 = inc(d, 2)` is T4-valid by TA5a (which is unconditional for `k = 1`) plus T10a's `zeros(d) ≤ 2` precondition — but the chain induction is left implicit.

**Required**: Add one sentence noting that the sweep's iterated T4-preservation follows by induction on the iteration index, with TA5a's unconditional preservation for `k = 0` discharging each step.

### Issue 4: The "consequences" sections lack a typology marker

**ASN-0086, throughout**: Each R-claim's *Consequences* paragraph lists derived implications (e.g., R2 consequences (a)–(d): "Distinct emissions are distinguishable," "Counting is well-defined," "Audit references are stable forever," "Idempotency on emit is policy"; R6 consequences (a)–(d): "Operational vs. historical views," etc.).

**Problem**: The consequences mix three distinct kinds of statement: (i) formal corollaries derivable from the R-claim (e.g., R2(a) — distinctness — is a direct consequence of R1+R0); (ii) policy observations about layer responsibilities (e.g., R2(d) — idempotency is a higher-layer concern); (iii) informal architectural commentary (e.g., R6(a) — the operational/historical view distinction). The reader needs to do interpretive work to tell which kind each consequence is. R6(d) flags itself as "anticipating R7 below" and notes "[The reduction has a definitional half; see R7b below]" — that kind of cross-reference would help in other consequence lists too.

**Required**: Mark each consequence as one of {COROLLARY, POLICY, ARCHITECTURE} or equivalent labels, or restructure as a single paragraph that distinguishes them in prose. This is a clarity issue, not a correctness one — but the ASN's overall rigor would benefit from removing the ambiguity.

### Issue 5: The R7 headline's conditionality is hedged in the body but not the abstract

**ASN-0086, opening abstract**: "On top of these we define three operations (Emit_K, Observe, Nullify), and an eighth lemma (R7, NullifyIsEmit) closes the argument that all *relational-layer* state change reduces to a single primitive: `Emit_K`."

**Problem**: The body decomposes R7 into R7a (proven) + R7b (stipulated) and explicitly hedges the reduction's conditionality. The abstract's italicized *relational-layer* qualifier does narrow the scope, but the conditionality on R7b's stipulation is not visible at the abstract level. A reader who skims the abstract and skips to the operations section would miss that R7's reduction is a model commitment, not a derived structural fact.

**Required**: One sentence in the abstract acknowledging that the reduction is the conjunction of one proven sub-claim and one model commitment — paralleling the explicit "of which six (R0–R5) are derivable from ASN-0043 and one (R6, ActiveSubsetWellDefinedness) is well-definedness by construction" hedging already present for R0–R6.

## OUT_OF_SCOPE

### Topic 1: Higher-arity link active subsets (`A_K^{(n)}`)

**Why out of scope**: The ASN defines `A_K` only over standard-triple links and notes (in the Definition of Nullify and Open Questions) that multi-arity active subsets `A_K^{(n)}` are a future extension. The asymmetry between syntactic admissibility of broader-arity Emit_R calls and their operational inertness against `A_K` is correctly flagged and left for future work.

### Topic 2: Concurrent emissions and Observe consistency model

**Why out of scope**: The Open Questions section enumerates concurrency questions explicitly. The ASN treats transitions as atomic and leaves the concurrency model unspecified.

### Topic 3: Lifting the sibling-frontier discipline to a substrate-level guarantee

**Why out of scope**: The ASN's Open Questions section proposes two paths (tightening the substrate emission primitive vs. tightening Emit_K's spec) for future work. The discipline-conditionality of R0a is well-documented and consistent with the present design's layering.

### Topic 4: Promoting the subspace-distinctness axiom (`s_C ≠ s_L`) to ASN-0043

**Why out of scope**: The ASN correctly identifies that ASN-0043's L0/L0a/L14 implicitly require `s_C ≠ s_L` but do not label it. ASN-0086 adopts the hypothesis explicitly. Pushing the axiom back to ASN-0043 is a separate revision to that ASN, not an item for ASN-0086.

VERDICT: REVISE
