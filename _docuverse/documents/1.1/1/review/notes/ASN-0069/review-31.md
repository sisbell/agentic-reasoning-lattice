# Review of ASN-0069

## REVISE

### Issue 1: V11 Properties Introduced table entry omits domain conjunct
**ASN-0069, Properties Introduced table (row V11)**: "Transitive identity along unedited fork chains: for every fork chain d_src → d¹_new → ... → d^k_new where each step's source has its content-subspace arrangement (set and pointwise values) unchanged between the prior step's post-state and the current step's pre-state, M^k(d^k_new)(v) = M(d_src)(v) for every v ∈ V_{s_C}(d_src)"
**Problem**: V11's body establishes two conjuncts in its conclusion. The body's initial statement reads "for every v ∈ V_{s_C}(d_src), v ∈ dom(M^k(d^k_new)) and M^k(d^k_new)(v) = M(d_src)(v)", and the inductive step's closing line ("V4 at step k now applies for every v ∈ V_{s_C}(d_src): V4 takes ... and concludes v ∈ dom(M^k(d^k_new)) with M^k(d^k_new)(v) = ...") confirms both conjuncts are load-bearing. The Properties Introduced table entry preserves only the value-equation conjunct, leaving the equation without its existence precondition — a reader consulting the table receives a partial summary in which `M^k(d^k_new)(v)` is referenced without first establishing that it is defined.
**Required**: Restate the table entry to include both conjuncts: "v ∈ dom(M^k(d^k_new)) and M^k(d^k_new)(v) = M(d_src)(v) for every v ∈ V_{s_C}(d_src)".

### Issue 2: V12(a) cites T8 without showing its role
**ASN-0069, V12(a)**: "(a) `d_src ∈ E'_doc ∧ d_new ∈ E'_doc` (T8, P1)"
**Problem**: T8 (AllocationPermanence, ASN-0034) governs address-level allocation: `allocated(s) ⊆ allocated(s')`. V12(a)'s conclusion is about entity-set membership across reachable states (`E ⊆ E'`), which is the direct claim of P1 (EntityPermanence, ASN-0047). The bridge from "address remains allocated" to "tumbler remains in `E_doc`" — i.e., that an allocated address that was once an entity address remains an entity address — is not stated in the foundation or in this ASN. P1 alone delivers the conclusion. As written, the joint citation suggests T8 contributes to the derivation when in fact it does not.
**Required**: Either drop T8 from the citation (leaving "(P1)"), or insert an explicit derivation showing how T8 contributes (e.g., as broader context with P1 as the operative premise).

### Issue 3: V6a(iii) understates the established result
**ASN-0069, V6a(iii)**: "`project(a, i, d_src, Σ) ∩ V_{s_C}(d_src) ⊆ project(a, i, d_new, Σ')` for every slot `i` — the fork inherits the source's content-subspace projection witnesses."
**Problem**: The derivation supplied for V6a(iii) actually establishes equality, not merely one-sided containment. Unfolding `project(a, i, d_new, Σ')` using V4b (`dom(M'(d_new)) = V_{s_C}(d_src)`), V4 (`M'(d_new)(v) = M(d_src)(v)` for v ∈ V_{s_C}(d_src)), and V6a(i) (`coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)`) yields `project(a, i, d_new, Σ') = {v ∈ V_{s_C}(d_src) : M(d_src)(v) ∈ coverage(Σ.L(a).eᵢ)} = project(a, i, d_src, Σ) ∩ V_{s_C}(d_src)`. The reverse direction holds because every position in `dom(M'(d_new))` is in `V_{s_C}(d_src)` (V4b's exact equality, not subset). The ASN's available premises already deliver equality; the one-sided statement leaves the stronger result unstated.
**Required**: Either strengthen V6a(iii) to equality (`project(a, i, d_src, Σ) ∩ V_{s_C}(d_src) = project(a, i, d_new, Σ')`) and update the derivation accordingly, or document explicitly why one-sided containment is the intended scope.

## OUT_OF_SCOPE

None to flag — the Open Questions section frames forward-looking work appropriately as questions rather than claims, and does not introduce issues that should be addressed in this ASN.

VERDICT: REVISE
