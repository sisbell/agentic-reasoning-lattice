# Review of ASN-0042

## REVISE

### Issue 1: O3 proof omits freshness condition when asserting the delegation predicate
**ASN-0042, O3 (OwnershipRefinement) proof**: "The remaining clause of O15 supplies an existing principal `π_d ∈ Π_Σ` satisfying conditions (i)–(vi) — that is, `delegated_Σ(π_d, π')` holds."
**Problem**: `delegated(Σ, Σ', π, π')` is defined (Delegation section) as condition (iii) plus the conjunction of (i), (ii), (iv), (v), (vi), **and (vii)** (freshness, `pfx(π') ∉ Σ.B`). Citing "(i)–(vi)" both mis-numbers the substantive conditions and drops (vii). The conclusion happens to be sound (O15 guarantees the full seven-condition predicate held at π''s introducing event), but the stated justification does not establish what it claims. OwnershipDomainPermanence Step 1 and O8 cite the full predicate correctly; O3 is the outlier.
**Required**: Replace "(i)–(vi)" with the full predicate `delegated_Σ(π_d, π')` (all conditions, freshness included), or justify why O15's guarantee of the complete predicate is being invoked rather than a hand-reconstruction of a subset.

### Issue 2: Covering-chain lemma states its independence from T5 three times
**ASN-0042, Ownership Domains**: (a) intro — "a direct consequence of Prefix (PrefixRelation) … and is independent of T5 (ContiguousSubtrees)"; (b) the lemma reasserts the same in prose; (c) proof close — "By T3 … no further appeal to T5 is required."
**Problem**: Defensive document-ordering meta-prose. A reader following the one-line proof must skip past two restatements of what the proof does *not* depend on. This is the anti-bloat "prose justifies document ordering / defensive justification" pattern compounding across cycles.
**Required**: State the dependency (Prefix, T3) once in the proof; delete the two independence-from-T5 disclaimers.

### Issue 3: O1b axiom prose explains why-needed and forward-references O2
**ASN-0042, O1b**: "Without injectivity, two principals sharing a prefix could both claim longest-match, and the effective owner function `ω` (defined in O2 below) would not yield a unique result."
**Problem**: Matches the flagged pattern "new prose around an axiom explains why the axiom is needed rather than what it says," plus a forward reference to a downstream consumer (O2). The axiom statement `pfx(π₁)=pfx(π₂) ⟹ π₁=π₂` is self-evident; the rationale belongs (if anywhere) in O2's dependency list, where O1b is already cited.
**Required**: Delete the why-needed sentence; O2 already names O1b as a premise.

### Issue 4: O14 prose enumerates downstream consumers
**ASN-0042, O14**: "Without these base cases, the inductive arguments for O1a, O1b, T4, and O4 cannot begin."
**Problem**: Use-site inventory — the axiom's introduction lists the proofs that consume it rather than advancing the axiom's content. The consuming proofs each already cite O14's relevant clause as their base case.
**Required**: Remove the enumeration; the base-case role is recorded at each induction site.

### Issue 5: `allocated_by_Σ` axiom carries a "Mechanism: Out of scope" sub-paragraph
**ASN-0042, allocated_by_Σ (AllocatedBy)**: sub-labels "Signature / Semantics / **Mechanism: Out of scope; belongs to the tumbler baptism specification.**"
**Problem**: Matches the flagged pattern of "Scope"-type sub-paragraphs explaining around an axiom what it does *not* cover. The Scope section at the end already declares the baptism mechanism out of scope.
**Required**: Drop the Mechanism sub-clause; keep Signature and Semantics.

### Issue 6: Transfer discussion duplicated across two sections
**ASN-0042, OwnershipDomainPermanence** ("The address is a birth certificate; a transfer would require a separate deed … We record this as an open question") and **Structural Provenance** ("This separation — between *who created* and *who currently holds rights* … Under a hypothetical transfer regime, they would diverge").
**Problem**: Two paragraphs in different sections make the same provenance-vs-authority / hypothetical-transfer argument in different words, and both defer to the same Open Question. Anti-bloat "two paragraphs say the same thing" + "multiple paragraphs defer to the same downstream location."
**Required**: Consolidate the transfer/provenance-divergence discussion into one location (Structural Provenance, where O6 lives) and reduce the other to a single pointer.

### Issue 7: "forevermore" refinement reading stated three times with a forward deferral
**ASN-0042, Permanence and Refinement** intro ("its precise reading is established at OwnershipDomainPermanence below"), **OwnershipDomainPermanence** ("This is Nelson's 'forevermore': not that ω is static … but that no external act can alter it"), **O8 design confirmation** ("O8 instantiates the refinement-only reading … established at OwnershipDomainPermanence").
**Problem**: The interpretive gloss is deferred forward, then restated, then restated again. The forward deferral plus the duplicated gloss are both flagged accretion patterns.
**Required**: State the refinement reading once (at OwnershipDomainPermanence) and have the other two sites cite it without re-explaining.

### Issue 8: DelegatorAllocatesPrefix freshness paragraph is procedural meta-prose
**ASN-0042, DelegatorAllocatesPrefix proof**: "The freshness conjunct removes the need to argue against an earlier sub-position allocation: condition (vii) records the design commitment that principal prefixes are reserved…"
**Problem**: This sentence explains why the proof is easier than an alternative proof, rather than advancing the derivation. The mechanical content (condition (vii) gives `pfx(π') ∉ Σ.B`, O18 gives membership in `Σ'.B`) is already stated in the preceding two sentences.
**Required**: Delete the "removes the need to argue" sentence.

### Issue 9: Worked Example counterfactual branch is bloat
**ASN-0042, Worked Example (Sub-account namespaces)**: "(Symmetrically, had `π_A` instead chosen to baptize `[1, 0, 2, 3]` as a third namespace, O18 would foreclose any later delegation … advance to `c_4 = [1, 0, 2, 4]`…)"
**Problem**: A counterfactual that the running trajectory explicitly does not take ("the worked example pursues the delegation branch from here on"). It does not verify any postcondition against the actual trajectory; the mutual-exclusivity point it illustrates is already made by the preceding sentence about `[1,0,2,1]`/`[1,0,2,2]`.
**Required**: Remove the parenthetical counterfactual.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
The Open Questions raise what invariants a transfer regime must preserve. Correctly deferred — transfer machinery is unspecified in the source design and is genuinely future territory, not a defect here.

### Topic 2: Authentication / session-to-prefix binding
The Trust Boundary section correctly treats `session.account = pfx(π)` as exogenous and lists concrete authentication mechanisms as out of scope, consistent with the Scope declaration.

META: not applicable — the ASN defines ownership state (Π, pfx, ω), a delegation operation, and invariants (exclusivity, coverage, refinement) at the abstract level any conforming implementation must satisfy; the Gregory citations are corroboration, not the substance. It is on-track but carries accreted meta-prose.

VERDICT: REVISE
