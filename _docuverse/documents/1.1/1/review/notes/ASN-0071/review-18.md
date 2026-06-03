# Review of ASN-0071

## REVISE

### Issue 1: Depth-mismatch over-collection is admitted but never analyzed

**ASN-0071, "The query"**: "The vspec drops all three: it admits spans whose positions may not all be currently arranged, whose source subspace may be empty in `d_s`, and **whose depth may differ from `d_s`'s common depth**."

**ASN-0071, "Resolution"**: "The relaxation makes the query total over well-typed inputs; resolution silently filters anything that does not match a current arrangement entry."

**Problem**: The ASN performs a careful over-collection analysis for the *action-point* dimension — pinning `actionPoint(ℓ) = #u` (tighter than T12's `≤ #u`) precisely because an interior action point "would let the displacement act on an interior prefix component, so `⟦σ⟧` would range across prefix structure and resolution would collect content positions the user never named." It then explicitly drops the `#u = m` requirement and notes that `⟦σ⟧` "is not depth-restricted." But it never analyzes the *symmetric* over-collection that the depth relaxation introduces.

Concretely: `S8-depth` fixes a single common depth `m` on `d_s`'s content subspace. Suppose `m = 3` with content positions `{[s_C, 1, k] : 1 ≤ k ≤ n}`, and a user submits a depth-2 vspec `u = [s_C, 1]`, `ℓ = δ(1, 2)`, reach `[s_C, 2]`. Then `⟦σ⟧ = {t : [s_C,1] ≤ t < [s_C,2]}` contains **every** `[s_C, 1, k]` (by T1 case (ii) at the prefix, then case (i) at position 2 since `1 < 2`). So `⟦σ⟧ ∩ dom(M(d_s))` is the *entire* depth-3 subtree under `[s_C, 1]` — `n` positions resolved from a span the user anchored at a single depth-2 coordinate. This is exactly the "collect content the user never named" failure that the `actionPoint = #u` precondition exists to foreclose, recurring across the depth axis. The claim that filtering "drops anything that does not match a current arrangement entry" is no defense here: these positions *do* match arrangement entries — they are simply at the wrong granularity. The subspace-confinement proof confines only position 1; it places no bound on the depths collected.

**Required**: Either (a) reinstate a depth constraint tying `#u` to `d_s`'s common depth `m` (the analog of C0a's PrefixConfinement that the vrelaxation removed), or (b) prove that cross-depth resolution is the intended, benign "prefix names subtree" semantics and state it as such, mirroring the rigor already given to the action-point case. The asymmetry — interior-prefix over-collection forbidden, cross-depth over-collection silently permitted — must be resolved, not left implicit.

### Issue 2: Subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` asserted "for every Q and Σ" without the well-definedness gate

**ASN-0071, Claims table (F-iaddrs)**: "subset claim `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` for every `Q` and `Σ`."

**Problem**: `iaddrs_one(d_s, σ)(Σ)` consults `Σ.M(d_s)`, and `dom(Σ.M) = Σ.E_doc` (M1). When `d_s ∉ Σ.E_doc`, `Σ.M(d_s)` is undefined and the expression `⟦σ⟧ ∩ dom(Σ.M(d_s))` is ill-formed — exactly the situation the `wp-defined: (A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)` precondition was introduced to exclude for `find`. The subset claim cannot hold "for every `Q` and `Σ`"; it holds only under `wp-defined`. The body even argues this gap is not benign in general ("P1 makes the gap benign only under that ordering, which the type signature does not enforce").

**Required**: Gate the F-iaddrs subset claim (and the prose "the subset claim ... holds for every `Q` and every `Σ`") on the same `wp-defined` precondition stated for `find`.

### Issue 3: Worked scenario does not delineate composite boundaries, so J0/J1★ validity of the constructed state is asserted, not shown

**ASN-0071, "A worked scenario"**: "Each precondition is discharged by the prior state; we narrate the result" (steps 1–13).

**Problem**: ValidCompositeAmended evaluates the coupling constraints J0, J1★, J1'★ *only between the initial and final state of each composite*. The thirteen steps interleave K.δ, K.α, K.μ⁺, K.ρ without grouping them into composites. This matters: step 3 (K.α emits `a₁`) freshly allocates `a₁`, and J0 requires every newly allocated I-address to appear in some arrangement *in the post-state of the composite*. If steps 3 and 4 (the K.μ⁺ placement) lie in different composites, the composite ending at step 3 violates J0. The verification of F-FIN and the home/transcluding recovery rest on `Σ` being reachable, so the state's validity must be established, not narrated.

**Required**: Group the numbered steps into explicit valid composites and confirm J0, J1★, and J1'★ hold at each composite boundary (the allocate–place–record triples are the natural grouping; state it).

## OUT_OF_SCOPE

### Topic 1: Historical-containment query over the provenance relation `R`

**Why out of scope**: The ASN correctly identifies that an `R`-based "ever-contained" query has different semantics than current-state `find`, and routes it to a separate mechanism (Open Questions). This is a future ASN, not a defect here.

### Topic 2: Visibility/access-control filtering and replica-divergent completeness

**Why out of scope**: The ASN deliberately specifies the unfiltered, single-state operation and names filtering and replication as separable policy/consistency layers. Correctly deferred.

VERDICT: REVISE
