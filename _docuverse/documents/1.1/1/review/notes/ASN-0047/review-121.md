# Review of ASN-0047

## REVISE

### Issue 1: Sub-allocator A_v(d) case-split incomplete for K.δ k=0 minted documents

**ASN-0047, "Allocator hierarchy under documents" section, *Sub-allocator names* paragraph**:

> "(a) If `d` is an *original* document — minted by a prior K.δ case (ii) k = 2 step with operand `parent(d) ∈ E_account` — then `A_v(d)` is a child of `A_doc(parent(d))` ... (b) If `d` is a *version* — `d = inc(d', 1)` minted by a prior K.δ case (ii) k = 1 step on some predecessor `d' ∈ E_doc` — then `A_v(d)` is a child of `A_v(d')`"

**Problem**: The case-split partitions on which K.δ event *minted* d, but does not cover documents minted by K.δ k = 0. The K.δ k = 0 case is fully permitted with `t ∈ E_doc` (per the K.δ k = 0 definition and the worked Multi-version invariant chain). The chain explicitly shows `v_{i+1} = inc(v_i, 0)` via K.δ k = 0 for `i ≥ 1`, meaning v₂, v₃, ... are minted by k = 0. Likewise, the second, third, ... documents created under the same account via K.δ k = 0 with operand a sibling document are not covered.

This matters because the K.δ k = 1 discharge invokes the case-split: "T10a.6 (DomainDisjointness, ASN-0034) identifies the unique parent allocator of `A_v(t)` in T10a's tree from t's own provenance — `A_doc(parent(t))` when t is an original document, `A_v(t')` when t is a version minted from a predecessor `t'`." If a K.δ k = 1 event fires with operand `t = v_i` for i ≥ 2 (a k = 0 minted version), neither "original document" nor "version minted by k = 1" applies literally.

**Required**: Reformulate the case-split based on t's *owning allocator* rather than its *minting event*:
- (a') If `t ∈ dom(A_doc(parent(t)))` — t inhabits the account's document sub-allocator — then `A_v(t)` is a child of `A_doc(parent(t))`. This covers t minted by K.δ k = 2 (first document) and t minted by K.δ k = 0 from another document on the same account chain.
- (b') If `t ∈ dom(A_v(d'))` for some d' — t inhabits a version sub-allocator — then `A_v(t)` is a child of `A_v(d')`. This covers t minted by K.δ k = 1 (first version) and t minted by K.δ k = 0 from another version on the same A_v(d') chain.

By T10a.6, these two cases are mutually exclusive and exhaustive over E_doc.

### Issue 2: Properties Introduced table omits `L' = L` from J2 and J3 frame conjuncts

**ASN-0047, "Properties Introduced" table, J2 and J3 rows**:

> "J2 | K.μ⁻ as elementary transition requires no coupling: C' = C ∧ E' = E ∧ R' = R
> J3 | K.μ~ as named composite requires no coupling: C' = C ∧ E' = E ∧ R' = R"

**Problem**: The prose definitions of J2 and J3 in the body explicitly include `L' = L` as part of the extended-state frame:

> "(The `L' = L` conjunct is the link-store extension contributed by the *Extended system state* paragraph above; the original J2 predated the link store and is superseded by this extended form in the extended state.)"

The table entries silently drop this conjunct. Since L is a state component in the extended state and P3's monotonicity clause `dom(L) ⊆ dom(L')` must be visibly discharged by every transition, the table should reflect the extended frame.

**Required**: Update the J2 and J3 table entries to read `C' = C ∧ L' = L ∧ E' = E ∧ R' = R`, matching the prose.

### Issue 3: K.δ case (ii) k = 1 multi-version chain — Sub-allocator names interaction with the case-split issue

**ASN-0047, "K.δ case (ii) discharge and parent-allocator activation" section, *k = 1 (version under existing document allocator)*: paragraph**:

> "Subsequent versions of t arise from K.δ k = 0 events whose operand is a prior version of t (`inc(prev_version, 0)`); those are T1 sibling-increments on `A_v(t)`'s frontier and are dispatched by the k = 0 case above, not by k = 1."

**Problem**: The discharge claims subsequent versions are "T1 sibling-increments on `A_v(t)`'s frontier" and are "dispatched by the k = 0 case above." But the k = 0 case above only requires `t ∈ E ∧ ¬IsNode(t) ∧ inc(t, 0) ∉ E` — it does *not* identify which allocator's frontier t is on. The K.δ k = 0 operation is allocator-agnostic; the same K.δ k = 0 with operand a version of d would produce inc(version, 0) on A_v(d)'s chain, while K.δ k = 0 with operand a sibling document under an account would produce inc(doc, 0) on A_doc(account)'s chain. The discharge would benefit from explicitly noting that the *same* K.δ k = 0 operation dispatches differently depending on which allocator the operand inhabits, with FrontierEquivalence (which already mentions the "(t, 0)-branch" of t's "sub-allocator") providing the per-allocator frontier semantics.

**Required**: Strengthen the prose to clarify that K.δ k = 0's operational uniformity (one operation, allocator-agnostic precondition) is reconciled with allocator-tree provenance by FrontierEquivalence's three-premise chain, which makes `inc(t, 0) ∉ E` equivalent to "t is the frontier of *its* sub-allocator's (t, 0)-branch" — the specific sub-allocator being determined by T10a.6 from t's provenance. This is consistent with the fix proposed in Issue 1.

### Issue 4: K.μ~ admissibility clause (i) — redundancy not noted

**ASN-0047, "Decomposition of K.μ~" section, second paragraph**:

> "π is admissible iff (i) every `π(v)` satisfies S8a, (ii) the induced post-state `M'(d)` would satisfy S8-depth, D-CTG★, D-MIN★, and S3★, and (iii) `π ≠ id`."

**Problem**: Clause (i) "every π(v) satisfies S8a" is automatically discharged once K.μ~-FIX is established and S8a holds at Σ (the inductive hypothesis). K.μ~-FIX gives `dom(M'(d)) = dom(M(d))`, so π's range is dom(M(d)). Every v ∈ dom(M(d)) satisfies S8a by the inductive hypothesis (S8a is a per-state invariant in ExtendedReachableStateInvariants). Therefore π(v) ∈ dom(M(d)) satisfies S8a unconditionally.

The dependency chain at the head of *Decomposition of K.μ~* derives subspace preservation and K.μ~-FIX as consequences, but the admissibility clauses are stated as if these consequences were not yet available. The ASN should note the redundancy explicitly, or remove clause (i) as implied by the other constraints.

**Required**: Either (a) remove clause (i) as superseded by S8a (per-state invariant) + K.μ~-FIX (derived postcondition), or (b) add a footnote indicating clause (i) is redundant given the chain but retained for definitional clarity.

### Issue 5: Worked example "interior content replacement" — admissibility verification ordering

**ASN-0047, "Worked example: interior content replacement" section, **Step 1: K.μ⁻** paragraph**:

> "*Admissibility (per-subspace).*
> - *Content subspace.* `V_{s_C}(d) = {[1,1], [1,2], [1,3], [1,4]}` shrinks to `V_{s_C}(d_int) = {[1,1]}` — partial suffix removal with `n'_{s_C} = 1`"

**Problem**: The K.μ⁻ amendment in *Amendments to existing transitions* says there is "no separate per-subspace shape precondition: D-CTG★ + D-MIN★ + D-SEQ★ at the post-state — together with K.μ⁻'s contractive effect — force the suffix-removal shape on each subspace independently". So per-subspace suffix removal is a *consequence* of the K.μ⁻ post-state invariants, not a precondition to verify at K.μ⁻ firing time.

But the worked example shows admissibility being *verified* via "partial suffix removal with n'_{s_C} = 1" — framing it as a precondition check. This conflates the consequence-vs-precondition distinction. A reader trying to verify whether K.μ⁻ can fire here might think they must check the suffix shape ex ante, when in fact the K.μ⁻'s D-CTG★/D-MIN★ postconditions guarantee it ex post.

**Required**: Reframe the admissibility verification to discharge K.μ⁻'s actual preconditions explicitly — namely (a) `dom(M(d)) ≠ ∅`, (b) the contractive effect `dom(M'(d)) ⊂ dom(M(d))`, and (c) the per-state invariants D-CTG★, D-MIN★ at the *post-state* M_int. The "partial suffix removal" language can be retained as a description of the chosen contraction shape, but it should be clear this is being designed-in (the operation's degree of freedom) rather than verified-against-a-precondition.

## OUT_OF_SCOPE

None of the issues I identified rise to OUT_OF_SCOPE. The ASN's Open Questions section already enumerates appropriate deferrals (concurrency, link withdrawal mechanism, registry protocol details, etc.).

VERDICT: REVISE
