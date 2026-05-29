# Review of ASN-0040

The formal development is strong: every claim carries a worked proof, the inductive invariant arguments (B0★, B1, B10, B_fin) are complete, the freshness proof in Bop correctly avoids circularity with contiguity, B8's restriction to co-reachable acts is exactly right (cross-branch same-namespace baptisms *should* coincide), and the concrete trace exercises d=1, d=2, empty/non-empty children, and both B7 disjointness cases. I found no correctness hole in any proof. My findings concern self-containment and one prose item.

## REVISE

### Issue 1: S(p,d), S0, and uniform length silently re-derive foundation results
**ASN-0040, The sibling stream / S0 / S(p,d) postconditions**: "S(p, d) = c₁, c₂, c₃, ..." with "`#cₙ = #p + d`" and S0: "`(A i, j : 1 ≤ i < j : cᵢ < cⱼ)`".

**Problem**: S(p,d) is, structurally, the foundation's allocator domain `dom(A)` (T10a) with base `inc(p,d)`: `c₁ = inc(p,d)` is the child base, `cₙ₊₁ = inc(cₙ,0)` is the sibling chain. Consequently S0 re-proves T10a.7 (EnumerationInjectivity / strictly increasing under T1) and the uniform-length postcondition re-proves T10a.1 (UniformSiblingLength), both with the same TA5(a)/T1 and TA5(c) arguments the foundation already discharges. A precise reader hits this duplication and cannot tell whether it is deliberate or an oversight. The likely reason it is deliberate — that baptism is not yet identified with the T10a allocation discipline (this is exactly the open question "Under what activation discipline does `allocated(s) ⊆ s.B` hold") — is never stated where the duplication occurs.

**Required**: Either cite T10a.1/T10a.7 (and `dom(A)`) for these results, or add one sentence at S(p,d) stating that baptismal streams are derived independently from the primitives TA5/T1 because their identification with T10a allocator domains is deferred. Without that, the re-derivation reads as reinvention of foundation machinery.

### Issue 2: B7 partially duplicates T10a.6 without noting the overlap
**ASN-0040, B7 (Namespace Disjointness)**: "For distinct valid pairs (p, d) ≠ (p', d'): S(p, d) ∩ S(p', d') = ∅".

**Problem**: For distinct B6 namespaces (which map to distinct allocator bases), this is the T10a.6 (DomainDisjointness) conclusion `dom(X) ∩ dom(Y) = ∅`. B7 does carry genuinely new content — the length-split / equal-parent / unequal-parent case analysis and the B6(i) aliasing necessity argument — so it is not pure duplication, but the disjointness conclusion itself overlaps T10a.6 and the relationship is unacknowledged.

**Required**: Note that B7's conclusion specializes T10a.6 to baptismal namespaces, with the case analysis and the B6(i)/aliasing argument as the ASN-local content. This keeps the foundation overlap explicit rather than implicit.

### Issue 3: Restating aside after S1 does not advance the argument
**ASN-0040, after S1**: "The word 'successive' is precise — positions arrive in order, c₁ before c₂ before c₃. The stream is traversed monotonically, not sampled."

**Problem**: This restates S0 (strict ordering) in prose immediately after S0 has been proved. Under the note's `review-mode.anti-bloat` classifier, this is essay content in a structural slot that a reader skips to follow the formal chain; "traversed monotonically, not sampled" adds nothing S0 has not established.

**Required**: Drop the restatement; the Nelson "successive" quote alone suffices as grounding.

## OUT_OF_SCOPE

### Topic 1: Cross-branch / cross-replica baptism uniqueness
**Why out of scope**: B8 is correctly limited to co-reachable acts; global uniqueness across divergent state-DAG branches (where the same namespace+hwm yields the same address by design) and distributed coordination are already deferred in the Open Questions and belong to a replication/ownership ASN, not here.

### Topic 2: The Occupied predicate and content placement (B3)
**Why out of scope**: B3 names a future `Occupied` predicate and constrains future content-storage operations. Content storage is listed out of scope; B3 is correctly framed as a forward requirement rather than a content-storage definition, so it stands — but the predicate's actual definition and operation effects are future-ASN territory.

VERDICT: REVISE
