I read the foundation layer (ASN-0034) and then ASN-0036 as a system, tracing each precondition chain across claim boundaries, checking each term keeps one meaning, and walking the case analyses in the load-bearing proofs.

The architectural spine holds. The two-component split (immutable `C` via S0/S1, mutable `M` via S2/S3), the address-identity layer (S4/S5 over GlobalUniqueness), the attribution layer (S7 over T4/T4b/T10a.4), the run partition (S8 over the shift algebra TS2/TS3/TS4), and the text-subspace contiguity tower (D-CTG → D-CTG-depth → D-SEQ → ValidInsertionPosition) all chain soundly. I verified the trickiest interfaces specifically:

- **S8's lockstep machinery** uses shift's frame property (`#shift(v,1)=#v`, from TA0) to ground the injectivity step (`#u=#u'` for TS2) and the succ-confinement step — *not* S8-depth's domain-restricted quantifier. This matches the formal contract and the prior declined finding's resolution; the body is no longer circular. The I-address side of the displacement identity correctly uses only TS3 + the local `shift(t,0):=t` convention (never OrdShiftHom, which `a` cannot satisfy), and `shift(a,k)` is well-defined for any `a ∈ T` via OrdinalShift/TA0. The chain decomposition (in/out-degree ≤ 1, acyclic by TS4+T1) into disjoint paths is correct, and the partition covers the empty case.
- **S7's well-definedness** correctly insists on T4-*validity* (not bare `zeros=3`) before invoking T4b's projections, routing through T10a.4 instantiated at `A_element`. The uniqueness step correctly separates S7d's *event*-distinctness from address-distinctness and supplies the latter via GlobalUniqueness.
- **D-CTG-depth** constructs intermediates `w` that genuinely satisfy D-CTG's guard (subspace, depth-match, zero-free, betweenness via T1(i)), and the infinitude argument against S8-fin is sound.
- **S5's independence argument** legitimately models S0–S3 alone over an empty transition relation; distinctness of documents/V-positions via T3 is correct.

Two framing-level observations follow.

### S7a body carries a use-site inventory for S7's proof
**Class**: OBSERVE
**Foundation**: S7a (DocumentScopedAllocation); T10a.4 (T4PreservationUnderDiscipline); consumed by S7 (StructuralAttribution)
**ASN**: S7a, closing sentence: *"These two memberships are the premises that, in S7's well-definedness step, license T10a.4's preservation invariant — quantified over allocators A ∈ 𝒯 and domain elements t ∈ dom(A) — to be instantiated at A := A_element, t := a."*
**Issue**: S7a's proper content is to *assert* the two memberships (`A_element ∈ 𝒯`, `a ∈ dom(A_element)`). This closing sentence instead narrates how S7's well-definedness step *consumes* them — a forward use-site explanation. The same justification ("two memberships of distinct types … license T10a.4's instantiation") already appears in S7's proof body, S7's Preconditions, and S7's Depends entry for T10a.4. The supplier claim restating the consumer's reasoning is use-site inventory; it is the kind of cross-cycle reviser residue that accretes around a hard instantiation point.
**What needs resolving**: In S7a, state the two memberships (and that they are the element-level counterpart of S7d's assertion) and stop; let S7's proof/contract carry the T10a.4-instantiation justification, where the precondition is actually discharged.

### D-CTG-depth justifies verifying S8a via membership rather than via D-CTG's guard
**Class**: OBSERVE
**Foundation**: D-CTG (VContiguity) — antecedent guard `subspace(v)=1 ∧ #v=#u ∧ zeros(v)=0 ∧ u<v<q`; S8a
**ASN**: D-CTG-depth proof: *"We also verify that w satisfies S8a — necessary because D-CTG ranges over V_1(d) ⊆ dom(M(d)), and every position in dom(M(d)) satisfies S8a."*
**Issue**: The cited reason runs backward. D-CTG's *antecedent guard* requires `zeros(w)=0` (plus `subspace(w)=1`, `#w=#u`), and that is why `zeros(w)=0` must be verified to fire D-CTG. That every position in `dom(M(d))` satisfies S8a is a *consequence* of the conclusion `w ∈ V_1(d)`, not a precondition for applying D-CTG. Verifying full S8a is harmless (its `#w≥2` conjunct follows redundantly from `#w=#u` and u's S8a), but the stated necessity attributes the obligation to the membership consequence instead of the guard. The verification is correct; only the justification is miscalibrated.
**What needs resolving**: Reframe the step to verify D-CTG's guard conditions directly — in particular `zeros(w)=0` because it is an antecedent conjunct of D-CTG — and note `#w≥2` follows from `#w=#u`; drop the "ranges over V_1(d) ⊆ dom(M(d))" rationale, which describes the post-hoc consequence.

VERDICT: OBSERVE