# Review of ASN-0047

## REVISE

### Issue 1: Non-circularity disclaimer for K.μ~ admissibility restated four times
**ASN-0047, *Decomposition of K.μ~***: The same point — that `S3★(Σ')` under K.μ~ is guaranteed by the admissibility filter, not derived by Steps (A)/(B), and is therefore not circular — is stated at least four times:
- In the admissibility paragraph: "*guaranteed by the admissibility filter itself* … not derived from the decomposition … neither can serve as a circular re-establishment of `S3★(Σ')`."
- Step (A) opening: "This step derives a structural property … by consuming the filter hypotheses; it does not establish them," plus the parenthetical "(Because this consumes `S3★(Σ')`, it cannot be read back as a proof …)."
- Step (B) opening: "`S3★(Σ')` is the filter's hypothesis … not by this step."
- B.3: "this is a consistency check, not an independent establishment of S3★(Σ') — that is the filter hypothesis …".

**Problem**: This is defensive meta-prose (the `review-mode.anti-bloat` pattern: prose explaining why the structure is sound rather than advancing it). One precise statement of "K.μ~ is a guarded transition; any admitted π satisfies the post-state package by clause (i); non-vacuity is the transposition witness" suffices. The four restatements force the reader to re-confirm the same disclaimer at each step.

**Required**: State the guard-discharges-the-invariant point once (at the admissibility definition or in the S3★ matrix cell), and let Steps (A)/(B) carry only their object-level content (subspace preservation; mechanical realisability) without re-litigating circularity.

### Issue 2: P4 unsatisfiability argued twice in separate sections
**ASN-0047, *Definition (Current containment)*** and ***Scoped coupling constraints*** (intro): The first says P4 "would require `Contains(Σ) ⊆ R`, but … `(ℓ, d) ∉ R` — P4 is unsatisfiable for the unscoped relation once any link-subspace mapping exists." The second repeats: "an unscoped coupling and P7 are mutually unsatisfiable — … `ℓ ∈ dom(L)` with `dom(L) ∩ dom(C) = ∅` (L14)."

**Problem**: Two paragraphs in different sections establish the same unsatisfiability via the same L14/P7 disjointness chain, motivating the same content-subspace scoping. This is duplicated motivation, not two distinct arguments.

**Required**: Argue the unsatisfiability once (it most naturally belongs at the P4★ definition, which is where the scoping is introduced) and cross-reference, rather than re-deriving in the coupling-constraints preamble.

### Issue 3: Subspace-position correspondence attributed to S3★ alone
**ASN-0047, *Notation* (Subspace-position correspondence)**: "For `v ∈ dom(M(d))` with `M(d)(v) = a`, `subspace(v) = subspace_I(a)` (S3★)."

**Problem**: S3★ alone yields only *membership* (`subspace(v) = s_C ⟹ a ∈ dom(C)`), not equality of subspace *identifiers*. The stated equality `subspace(v) = subspace_I(a)` requires S3★ **plus** L0 (which pins `subspace_I(a) = s_C` for `a ∈ dom(C)` and `= s_L` for `a ∈ dom(L)`). As written, the one-line derivation cites only one of the two premises it needs.

**Required**: Cite the correspondence as following from S3★ + L0 (S3★ routes the value to the correct store by subspace; L0 fixes that store's I-address identifier), or note the two-step chain explicitly.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The fork composite (J4) deliberately starts the forked document's link subspace empty and notes "A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." Correctly deferred; the relevant Open Question is already recorded.

### Topic 2: Tombstoning / interior link withdrawal
The D-CTG★/D-MIN★ strengthening forecloses interior link withdrawal via K.μ⁻, and the ASN flags that reconciling Nelson's tombstoning design needs a separate withdrawal mechanism. This is correctly an Open Question, not a defect in this ASN.

VERDICT: REVISE
