# Review of ASN-0063

## REVISE

### Issue 1: P4 (ProvenanceBounds) violated — omitted from CL11

**ASN-0063, CL11 (InvariantPreservation)**: P4 is not addressed anywhere in the invariant preservation proof.

**Problem**: K.μ⁺_L adds the mapping `v_ℓ ↦ ℓ` to `M(d)`, placing `ℓ` into `ran(M'(d))`. By the definition of `Contains`, `(ℓ, d) ∈ Contains(Σ')`. P4 requires `Contains(Σ') ⊆ R'`. But `R' = R` (unchanged), and P7 requires every entry `(a, d) ∈ R` to satisfy `a ∈ dom(C)`. Since `ℓ ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅` (L14), `(ℓ, d) ∉ R'`. Therefore `Contains(Σ') ⊄ R'` — P4 is violated.

The ASN correctly identifies the analogous conflict for J1/P7 and introduces J1★ to resolve it, but does not notice that P4 has the same structural problem: `Contains(Σ)` is unscoped and includes all addresses in `ran(M(d))`, not just content-subspace addresses.

**Required**: Define a content-scoped containment relation, e.g. `Contains_C(Σ) = {(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}`, and introduce P4★: `Contains_C(Σ) ⊆ R`. Then verify P4★ is preserved by CREATELINK (it is: no content-subspace mappings change, `R' = R`).

---

### Issue 2: S3 supersession not stated

**ASN-0063, S3★ definition and CL11**: "S3★ extends the referential integrity guarantee to the link subspace."

**Problem**: S3 from ASN-0036 states `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))` — every V-position maps to `dom(C)`. K.μ⁺_L adds a mapping `v_ℓ ↦ ℓ` where `ℓ ∈ dom(L)`, `ℓ ∉ dom(C)`. This violates S3 as stated. CL11 verifies S3★ but does not mention S3, leaving the reader to wonder whether S3 still holds (it does not).

The same issue applies to the coupling constraints: J1★ and J1'★ replace J1 and J1', but the valid composite definition (ASN-0047) references J0, J1, J1'. The ASN should state that the coupling constraints for the extended state are J0, J1★, J1'★.

**Required**: Explicitly state: (a) S3★ supersedes S3 for the extended state `Σ = (C, L, E, M, R)`. (b) S3 remains valid when restricted to pre-extension states (no link-subspace mappings). (c) Existing transitions (K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.ρ) trivially preserve S3★ because none creates link-subspace mappings. (d) The coupling constraints for valid composites in the extended state are J0, J1★, J1'★.

---

### Issue 3: CL0 proof uses undefined shift(a_β, 0)

**ASN-0063, CL0 proof**: "Define the I-span `ρ = (shift(a_β, c), δ(c' − c, #a_β))`."

**Problem**: The OrdinalShift definition (ASN-0034) requires `n ≥ 1`: "For a tumbler `v` of length `m` and natural number `n ≥ 1`." When the V-span starts at or before the block's V-start, `c = 0`, and `shift(a_β, 0)` is undefined. This is the common case — the worked example has `c = 0` for both blocks.

The M-aux convention (`v + 0 = v`) from ASN-0058 handles the `c = 0` case, but CL0 uses `shift` notation instead of the `+` notation that carries this convention.

**Required**: Either (a) use `a_β + c` notation throughout (which handles `c = 0` by M-aux convention), or (b) handle the `c = 0` case separately: when `c = 0`, the I-span start is `a_β` itself; when `c ≥ 1`, it is `shift(a_β, c)`.

---

### Issue 4: CL0 statement conflates image with span denotation

**ASN-0063, CL0**: "the image of their overlap through β is a single well-formed I-span."

**Problem**: The image `{a_β + k : c ≤ k < c'}` is a finite set of element-level I-addresses. The I-span `ρ`'s denotation `⟦ρ⟧` is an infinite set containing all tumblers in the half-open interval (including proper extensions at greater depths). These are not equal — `{a_β + k : c ≤ k < c'} ⊂ ⟦ρ⟧`. The ASN correctly notes this three paragraphs later ("The containment is strict in general"), but the CL0 statement itself asserts identity rather than containment.

**Required**: Restate CL0: "the image of their overlap through β is contained in the denotation of a single well-formed I-span" or "is representable by a single well-formed I-span." This makes CL2 (ResolutionContainment) follow cleanly without the reader needing to reconcile the CL0 statement with the subsequent caveat.

---

### Issue 5: K.μ⁺_L freshness of v_ℓ unstated

**ASN-0063, K.μ⁺_L**: Effect `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`.

**Problem**: For this to be a proper extension preserving S2 (ArrangementFunctionality), `v_ℓ ∉ dom(M(d))` is required. This IS derivable from the preconditions: when `V_{s_L}(d) = ∅`, the position is the minimum (not yet used); when non-empty, `v_ℓ = shift(max(V_{s_L}(d)), 1) > max(V_{s_L}(d))` by TS4, placing it beyond all existing link-subspace positions; and `subspace(v_ℓ) = s_L ≠ s_C` ensures no collision with text-subspace positions (T7). But neither the derivation nor the conclusion appears in the ASN.

**Required**: Either add `v_ℓ ∉ dom(M(d))` as an explicit precondition, or derive it from the existing preconditions with an explicit argument.

---

### Issue 6: Direct I-span endset path not formalized

**ASN-0063, Endset Resolution section**: "the system supports raw I-span endsets that bypass resolution entirely. In that case the endsets are taken as-is."

**ASN-0063, CREATELINK composite**: "Let F = resolve(S_F), G = resolve(S_G), Θ = resolve(S_Θ)."

**Problem**: The CREATELINK composite's formal definition assumes V-space resolution for all endset specifications. The alternative input path — direct I-spans that bypass resolution — is described in prose but absent from the composite definition. The `resolve` function is defined only for `(d, Ψ)` pairs; it has no clause for direct I-span input.

**Required**: Either (a) extend `resolve` to handle direct I-span specifications (trivially: the identity function), or (b) define two CREATELINK variants with explicit dispatch. The composite must formally handle both input forms so that CL3 and CL11 cover both paths.

---

## OUT_OF_SCOPE

### Topic 1: Link-subspace V-depth m_L

K.μ⁺_L references "the link-subspace V-depth for d" (m_L) without specifying how it is determined for a document's first link. S8-depth requires depth uniformity within a subspace, so the first link position establishes m_L. Any m_L ≥ 2 is valid, but the choice is a design parameter this ASN leaves open.

**Why out of scope**: The abstract specification correctly requires S8-depth compliance without needing to fix m_L. A future ASN on document structure or subspace conventions can pin this.

### Topic 2: P3 (ArrangementMutabilityOnly) extension for L

P3 says "No other component (C, E, R) admits contraction or reordering." With L added to the state, P3 should include L. Since L is monotonically growing (L12a) and immutable (L12), it satisfies the constraint, but P3 needs restating for the five-component state.

**Why out of scope**: P3's extension is mechanical and does not affect CREATELINK's correctness. It belongs in a foundation revision that integrates L into the transition framework.

VERDICT: REVISE
