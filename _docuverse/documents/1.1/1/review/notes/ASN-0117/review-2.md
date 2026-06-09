# Review of ASN-0117

## REVISE

### Issue 1: DEL-REMOVE / P1 makes a false domain claim and the worked example contradicts itself

**ASN-0117, "DELETE … Effect" (DEL-REMOVE) and P1**: "(A k : J ≤ k < J + c : q_k ∉ dom(M'(d)))" — "the deleted block's V-positions leave the arrangement."

**Problem**: This is false for mid-span deletion. By DEL-DOM, the text-subspace domain is `L ∪ Q₃ = {q_1,…,q_{N−c}}`. The V-position *labels* that actually leave the domain are the top `c` labels `{q_{N−c+1},…,q_N}`, **not** the deleted-span labels `{q_J,…,q_{J+c−1}}`. The deleted-span labels are reoccupied by shifted survivors. Your own worked example exhibits the contradiction: with `N=5`, `p=q_3`, `c=2`, you write "Removal … q_3, q_4 ∉ dom(M'(d)) … ✓ P1" and then immediately "q_5 → q_3 carrying a_5 … M'(d)(q_3) = a_5". So `q_3 ∈ dom(M'(d))` with value `a_5`, directly falsifying `q_3 ∉ dom(M'(d))`. (DEL-REMOVE accidentally holds only for suffix-deletes and full-deletes, where no relabelling lands on the cut.) Note ASN-0082 never claims deleted positions leave the domain — D-DOM only characterizes the resulting domain set. DEL-REMOVE is an incorrect addition on top of the foundation.

**Required**: Restate P1/DEL-REMOVE in terms of what is actually removed: the specific V→I *correspondences* `q_k ↦ M(d)(q_k)` for `J ≤ k < J+c` cease to be members of `M'(d)`, the top `c` position labels `{q_{N−c+1},…,q_N}` leave `dom(M'(d))`, and the deleted I-addresses `A_del` persist in `C`. Correct the worked example's "✓ P1" line accordingly.

### Issue 2: LP10 (ContractionMonotonicity) is misapplied to DELETE

**ASN-0117, P4 / discoverability**: "DELETE shrinks d's range — ran(M'(d)) ⊆ ran(M(d)) — by removing the deleted mappings (foundation LP10 (ContractionMonotonicity), ASN-0098)."

**Problem**: LP10 is keyed to a K.μ⁻ transition, whose hypothesis is domain restriction *with value agreement on the retained domain*. DELETE relabels keys (shift), so values on retained labels change: `M'(d)(q_J) = M(d)(q_{J+c}) ≠ M(d)(q_J)`. Hence LP10's hypothesis is not met. Worse, LP10's *conclusion* (position-set projection `project(e,d,Σ') ⊆ project(e,d,Σ)`) is actually **false** for DELETE: a label whose old value was outside `coverage(e)` can acquire (via shift) a value inside it, so a position can *enter* the projection. The range-level fact `ran(M'(d)) ⊆ ran(M(d))` is true but does not follow from LP10.

**Required**: Drop the LP10 citation. Derive `ran(M'(d)) = M(d)(L) ∪ M(d)(R) ⊆ ran(M(d))` directly from DEL-LEFT/DEL-SHIFT (as the wp section already does correctly), and base discoverability shrinkage on LP12 (range-based) plus that direct derivation.

### Issue 3: ASN-0082 contraction lemmas are cited at S = s_C without establishing s_C = 1

**ASN-0117, "What shifts" and DELETE precondition**: "S = subspace(p) = s_C … #p = 2 … This is exactly the foundation contraction's precondition (ASN-0082)."

**Problem**: ASN-0082's Contraction and its postcondition family (D-SHIFT, D-L, D-DOM, D-SEP, D-CTG, D-MIN, …) are stated with the literal precondition `S = 1` and `V_1(d)`. ASN-0117 invokes them at `S = s_C` and writes `q_k = [s_C, k]`. The citations are only licensed if `s_C = 1`, which is the foundation convention (SubspaceConventionAxiom, ASN-0047/ASN-0093) but is never invoked here.

**Required**: State `s_C = 1` via the foundation SubspaceConventionAxiom (or otherwise justify that ASN-0082's S=1 contraction applies at `s_C`) before citing D-SHIFT/D-L/D-DOM/D-SEP at `S = s_C`.

## OUT_OF_SCOPE

### Topic 1: Correspondence of DELETE to the transition vocabulary
DELETE (mid-span removal + left-shift) is not obviously expressible as any single transition of ASN-0047 (K.μ⁻ is suffix-retention only; K.μ~ preserves the domain). At the displacement layer ASN-0082 blesses the contraction, so this is acceptable here, but the bridge from DELETE to a concrete system transition is future work, not a defect of this ASN.

VERDICT: REVISE
