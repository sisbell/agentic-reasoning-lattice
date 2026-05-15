# Review of ASN-0082

## REVISE

### Issue 1: Post-I3 contiguity-violation discussion conflates text and link subspaces
**ASN-0082, Post-Insertion Shift, "Arrangement invariants not preserved" paragraph**: "The shift preserves typing invariants (S8-depth, S8a, S3) but does *not* preserve the contiguity invariants of ASN-0036. The gap created by the shift — n vacated positions between the left region and the shifted region — violates D-CTG (VContiguity): the post-state V_S(d) is not contiguous..."
**Problem**: I3 is parameterized by any S ≥ 1 (the shift sub-operation works on text or link subspaces). But D-CTG, D-MIN, D-SEQ in ASN-0036 are explicitly text-subspace-only — the foundation's frame note exempts V_2(d) ("link subspace V_2(d) is exempt — sparse with tombstones is permitted"). For S ≠ 1 insertion, "violates D-CTG" is incorrect: the foundation imposes no D-CTG on link subspace, so no violation occurs. The discussion implicitly treats all I3 applications as text-subspace.
**Required**: Distinguish the cases. State that for S = 1, the gap violates D-CTG/D-MIN/D-SEQ and the INSERT ASN must re-establish them; for S ≠ 1, no foundation contiguity invariant applies and the shift is a complete sub-operation requiring only content placement to compose with INSERT.

### Issue 2: wp analysis of I3-S2 leaves vacate/positive overlap unworked
**ASN-0082, "Weakest-precondition analysis (I3-S2 backwards through the assignment regions)" paragraph following case (6)**: "the (vacate) statement removes positions from dom(M'(d)) and so cannot collide with another assignment within dom(M'(d)); collisions between (vacate) and a positive assignment are addressed below as the (shift) ∩ (vacate) overlap, where (shift) wins by construction"
**Problem**: The "shift wins by construction" claim is the load-bearing argument that I3-V's exclusion clause prevents double-assignment when an original position v ≥ p is also a shifted destination (e.g., the worked example's [1,5]). The wp analysis enumerates six explicit cases for positive assignments but treats this overlap with a parenthetical hand-wave. Without unpacking, a reader cannot verify that the four-assignment-region simultaneous statement is wp-consistent.
**Required**: Add an explicit (shift) ∩ (vacate) case to the wp analysis showing that I3-V's exclusion `v ∉ {shift(u, n) : ...}` discharges the obligation by removing the position from I3-V's range exactly when I3 places it in dom(M'(d)). Naming the discharger explicitly is what the other six cases do; this one deserves the same treatment.

### Issue 3: D-SEP(b) proof relies on containment without citing it
**ASN-0082, D-SEP proof of (b), Case 2**: "D-SEQ on the pre-state V_1(d) (text subspace, ASN-0036), V_1(d) = {[1, k] : 1 ≤ k ≤ N}. ... The containment precondition `p₂ + w₂ − 1 ≤ N` ensures that all c values from p₂ through p₂ + c − 1 lie within [1, N], so X = {[1, k] : p₂ ≤ k < p₂ + c}."
**Problem**: The argument constructs the last element of X as [1, p₂ + c − 1] and applies D-CTG with this as u. For D-CTG to apply, [1, p₂ + c − 1] must be in V_1(d), which requires p₂ + c − 1 ≤ N — exactly the containment precondition. The dependency is woven through the X-form derivation but not called out at the D-CTG application site, where its load-bearing role is most visible.
**Required**: At the D-CTG application step, explicitly note that [1, p₂ + c − 1] ∈ V_1(d) by containment, so the precondition is doing essential work. Without this, a reader skimming D-SEP(b) cannot see why containment matters — the precondition reads as a generic "stay within bounds" constraint rather than as the specific witness D-SEP(b) needs.

### Issue 4: Contraction lacks a sub-operation/full-operation framing
**ASN-0082, Post-Contraction Shift section**: The contraction formal contract is presented without a framing comparable to I3's "**Scope.** This ASN characterizes the *shift sub-operation* of INSERT — ... not the full INSERT operation."
**Problem**: A reader who has just absorbed I3's careful disclaimer about being a sub-operation will reasonably ask: is contraction also a sub-operation, or is it the full DELETE? D-I (`Σ'.C = Σ.C`) and the absence of any content-placement clause suggest contraction is the complete arrangement transformation for DELETE (since Xanadu's content immutability means DELETE never removes content). But this is left implicit. The asymmetry with INSERT is structural — INSERT adds content, DELETE doesn't — and that's worth stating, otherwise readers infer a phantom "post-contraction operation" still to come.
**Required**: Add a Scope paragraph at the start of the Post-Contraction Shift section paralleling the one for I3, stating that contraction is the complete V-arrangement transformation for DELETE (no content placement is required because S0 makes content immutable; D-I records this as exact equality).

## OUT_OF_SCOPE

### Topic 1: Composition of insertion shift with subsequent operations
**Why out of scope**: The round-trip property (INSERT then CONTRACT recovers the pre-state, modulo content-placement) requires reasoning about operation composition, which is operation-level rather than displacement-arithmetic. Belongs in INSERT/DELETE composition ASNs.

### Topic 2: Span growth at insertion points (straddling spans)
**Why out of scope**: I3-S characterizes spans within the shifted region. Spans straddling p (start in left region, reach in shifted region) effectively grow by n. This is a different kind of property — operation semantics rather than displacement arithmetic — and would belong in a span-aware INSERT ASN.

### Topic 3: Link subspace contraction with tombstones
**Why out of scope**: The ASN's subspace scoping axiom restricts contraction to S = 1 with explicit rationale that link subspaces require tombstoning rather than gap-closure. Deferred per the ASN's own statement.

### Topic 4: Deeper-depth contraction (#p > 2)
**Why out of scope**: The depth scoping axiom restricts contraction to #p = 2, with explicit rationale tied to TA4's zero-prefix precondition. The Open Questions section flags this as a generalization target.

VERDICT: REVISE
