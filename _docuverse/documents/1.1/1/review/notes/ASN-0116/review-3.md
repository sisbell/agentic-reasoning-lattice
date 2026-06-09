# Review of ASN-0116

## REVISE

### Issue 1: P4's "superset" claim is false under the shift relabeling

**ASN-0116, §"Invariants the operation must preserve" (P4) and §"What shifts"**: "Hence the post-insert set is a superset of the prior set, equal to it iff the new-block part is empty." / "What insertion can do is *enlarge* a link's resolved-witness set — never shrink it."

**Problem**: `project(e, d, Σ')` and `project(e, d, Σ)` are sets of *V-positions*, and the suffix witnesses are **relabeled** by `v ↦ shift(v, n)`. They are not in a superset relation. Counterexample: `V_S(d) = {q₁, q₂}`, `M(d)(q₂) = a₂`, `coverage(e) = {a₂}`, so `project(e,d,Σ) = {q₂}`. Insert `n=1` at `p = q₁`: then `q₂ → q₃` carries `a₂`, so `project(e,d,Σ') = {q₃}`. But `{q₃} ⊉ {q₂}`. The witnesses moved; the set did not grow by inclusion.

**Required**: State the correct relation. The prior witnesses are in *bijection* with (left ∪ `shift`(suffix) ∪ cross-subspace), so the witness *count* is non-decreasing (`|project(e,d,Σ')| = |project(e,d,Σ)| + |new-block witnesses|`), and the resolved *content* grows monotonically (`coverage(e) ∩ ran(M(d)) ⊆ coverage(e) ∩ ran(M'(d))`). Remove the V-position-set "superset" wording.

### Issue 2: P6 computes a *sufficient* precondition, not the *weakest*

**ASN-0116, §"A weakest precondition"**: "Therefore `D(d, Σ') = D(d, Σ) ∪ {a : (E i) coverage(eᵢ) ∩ A_new ≠ ∅}`. The two sets coincide iff that added set is empty." and the boxed `wp(...) ≡ INSERT-pre ∧ (A a, i : coverage(Σ.L(a).eᵢ) ∩ A_new = ∅)`.

**Problem**: `D(d,Σ') = D(d,Σ)` holds iff `Added ⊆ D(d,Σ)`, not iff `Added = ∅`. A link whose endset has one span into `A_new` (ghost) **and** another span into `ran(M(d))` is in `Added` *and* already in `D(d,Σ)` — permitted by L4/L9 — so inserting does not change `D(d)`. The boxed condition rejects such pre-states even though discoverability is preserved. The ASN labels this the *weakest* precondition; it has computed a strictly stronger sufficient one.

**Required**: Either give the true weakest precondition (`INSERT-pre ∧ {a : (∃i) coverage(Σ.L(a).eᵢ) ∩ A_new ≠ ∅} ⊆ D(d, Σ)`) or relabel the boxed condition as a *sufficient* precondition and keep the tight-endset corollary as a discharge of that sufficient form.

### Issue 3: I3-S3 cited under a content frame INSERT overrides

**ASN-0116, §"The document remains one coherent sequence"**: "well-formedness is exactly ASN-0082's family: … **I3-S3** for referential integrity."

**Problem**: ASN-0082's I3-S3 (referential integrity) is derived under **I3-C** (PostInsertionContentFrame: `dom(C') = dom(C)`, content unchanged). INSERT explicitly violates I3-C via I-ALLOC (`dom(C') = dom(C) ∪ A_new`). The conclusion still holds — left/shifted images lie in `dom(C) ⊆ dom(C')` — but it follows from S3 plus content *monotonicity*, not from a lemma proved under content-fixed frame. The ASN correctly omits I3-C from its citations but then leans on I3-S3, which depends on it.

**Required**: Derive referential integrity for the left/shifted regions directly (image in `dom(C) ⊆ dom(C')` by S3 + append-only P2), rather than citing I3-S3 whose proof frame INSERT does not satisfy.

### Issue 4: Worked example does not exercise the link claims (P4, P5, P6)

**ASN-0116, §"A worked insertion"**: verifies P0, P1, P2, I-DOM, I-NEW and two boundaries.

**Problem**: The subtlest *introduced* claims — P4's witness decomposition, P5 isolation, and the P6 wp side condition — are never checked against a concrete scenario. A concrete link example (a suffix witness relabeled under the shift, plus a ghost reference resurrected by `A_new`) would have surfaced Issues 1 and 2 directly. Per the depth standard, the key novel postconditions must be verified against a specific scenario.

**Required**: Add a worked instance with at least one link whose coverage includes (i) a suffix I-address that shifts and (ii) a ghost address minted into `A_new`, and check P4 and the P6 branch `coverage(e) ∩ A_new ≠ ∅` against it.

### Issue 5: "resurrection (LP18)" mislabels the general new-witness case

**ASN-0116, §"What shifts" (new-block witnesses)**: "a resurrection in the sense of **LP18 (ASN-0098)**, an orphaned reference becoming discoverable."

**Problem**: LP18 is specifically about a link *orphaned* at `Σ` (discoverable from no document) becoming discoverable. The new-block witness mechanism (`shift(a,k) ∈ coverage(e)`) applies whether or not the link was orphaned — a link already discoverable elsewhere also gains a new-block witness. Attributing the general case to LP18 overreaches.

**Required**: Distinguish the general "new-block witness gain" (any link with `coverage(e) ∩ A_new ≠ ∅`) from the LP18 special case (orphaned link). Cite LP18 only for the orphaned sub-case.

## OUT_OF_SCOPE

### Topic 1: Provenance recording (R) and ASN-0047 valid-composite coupling

**Why out of scope**: INSERT is composed from ASN-0093's K.α and ASN-0082's I3, neither of which carries a provenance component. ASN-0047's valid-composite framework would require J1★ (provenance recording for new content-subspace range entries), but the ASN works in the ASN-0093/0082 substrate and explicitly defers the provenance relation to its Open Questions. This is a separate integration concern, not a defect in the present model — though if INSERT is later required to be an ASN-0047 valid composite, J1★/K.ρ coupling must be added.

### Topic 2: Concurrent insertions and serialization

**Why out of scope**: The Open Questions correctly raise concurrent freshness without a serializing authority; this belongs to a future ASN, not the single-authority INSERT specified here.

VERDICT: REVISE
