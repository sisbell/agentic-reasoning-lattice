# Review of ASN-0063

## REVISE

### Issue 1: Subspace identifier constraint unestablished; S8a verification built on false premise
**ASN-0063, CL11 — InvariantPreservation, content invariants**: "S8a (VPositionWellFormedness): guarded by v₁ ≥ 1, applies to text-subspace positions, which are unchanged. ✓"
**Problem**: The ASN never establishes the value of s_L. From T4 (ASN-0034), every element-field component must be strictly positive: `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`. L1 requires link addresses to be element-level. Together: `fields(ℓ).E₁ = s_L > 0`. Since K.λ and K.μ⁺_L use the same identifier s_L for both I-addresses and V-positions, link-subspace V-positions have `v₁ = s_L ≥ 1`. S8a's quantifier `(A v ∈ dom(M(d)) : v₁ ≥ 1 : ...)` therefore covers link-subspace V-positions, contradicting the claim that S8a "applies to text-subspace positions" only. The conclusion (S8a preserved) happens to hold — K.μ⁺_L places `v_ℓ = [s_L, 1, ..., 1]` or a shift thereof, all components positive, so `zeros(v_ℓ) = 0 ∧ v_ℓ > 0` — but the argument as written is wrong.
**Required**: (a) Derive `s_L > 0` from T4 + L1. (b) Acknowledge S8a's quantifier includes link-subspace V-positions when `s_L ≥ 1`. (c) Verify link-subspace positions satisfy `zeros(v) = 0 ∧ v > 0` explicitly.

### Issue 2: Framework extension permits orphan links without acknowledgment
**ASN-0063, Extending the Transition Framework**: "The coupling constraints for valid composites in the extended state Σ = (C, L, E, M, R) are J0, J1★, J1'★."
**Problem**: K.λ alone is a valid composite under this constraint set. J0 is vacuous (no content allocated), J1★ is vacuous (no content-subspace extension), J1'★ is vacuous (no provenance change). The result: a link enters `dom(L)` without being placed in any document's arrangement. CREATELINK always pairs K.λ with K.μ⁺_L, but the framework permits K.λ in isolation, producing an orphan link — discoverable via `disc` but not an out-link of any document. This may be intentional (link withdrawal via K.μ⁻ on the link subspace would also produce orphan links), but the ASN neither discusses the possibility nor adds a J0 analog to prevent it. The claimed-complete list of coupling constraints leaves this unaddressed.
**Required**: Either (a) add a coupling constraint `J0★` requiring every new link address in `dom(L') \ dom(L)` to be placed in its home document's arrangement, or (b) explicitly acknowledge that orphan links are valid system states and note the design rationale.

### Issue 3: Link-subspace V-position depth m_L undetermined
**ASN-0063, K.μ⁺_L**: "v_ℓ is the minimum position [s_L, 1, ..., 1] of depth m_L (D-MIN), where m_L is the link-subspace V-depth for d"
**Problem**: When `V_{s_L}(d) = ∅` (first link in document d), the depth m_L is unconstrained — S8-depth is vacuously satisfied for an empty subspace. The first K.μ⁺_L establishes m_L, but nothing constrains the choice. At `m_L = 1`, the only V-position is `[s_L]`; `shift([s_L], 1) = [s_L + 1]` has `subspace = s_L + 1 ≠ s_L`, so K.μ⁺_L's precondition `subspace(v_ℓ) = s_L` fails for the second link. This limits the link subspace to one entry per document. The worked example uses `m_L = 2`, which supports arbitrarily many links, but nothing prevents an implementation from choosing `m_L = 1`.
**Required**: State `m_L ≥ 2` as a precondition of K.μ⁺_L (or as part of the link-subspace design), with the reason: ordinal shift at depth 1 alters the subspace identifier, violating subspace closure.

### Issue 4: CL0 proof cites wrong property and elides an intermediate step
**ASN-0063, CL0 — BlockProjection**: "The V-extent V(β) is contiguous by M1 (ASN-0058), and ⟦σ_v⟧ is convex by S0 (ASN-0053). Their non-empty intersection is convex, hence of the form {v_β + k : c ≤ k < c'}."
**Problem**: Two issues. (a) M1 (OrderPreservation, ASN-0058) states `v + j < v + k ∧ a + j < a + k` — this is an ordering property, not contiguity. V(β) is contiguous because it is defined as `{v + k : 0 ≤ k < n}`, a sequence of ordinal increments at a fixed depth (D-SEQ, ASN-0036). (b) The step from "non-empty convex intersection" to "of the form {v_β + k : c ≤ k < c'}" requires that V(β) consists of tumblers at a shared depth with consecutive last components (so a convex subset is a contiguous index sub-range). This follows from S8-depth and D-SEQ but is not cited.
**Required**: Cite the definition of V-extent and D-SEQ (or S8-depth) instead of M1. State explicitly that V(β) elements are consecutive at a fixed depth, so convex subsets correspond to contiguous index ranges.

### Issue 5: VSpanImage definition missing well-formedness precondition
**ASN-0063, Definition — VSpanImage**: "image(d, σ_v) = {M(d)(v) : v ∈ ⟦σ_v⟧ ∩ dom(M(d))}"
**Problem**: `⟦σ_v⟧` requires `reach(σ_v) = start(σ_v) ⊕ width(σ_v)` to be defined (TA0), which requires T12: `width > 0` and action point `k ≤ #start`. Neither VSpanImage nor the CREATELINK precondition requires the input V-spans to be well-formed. The well-definedness argument ("⟦σ_v⟧ is determined by the span's start and width") implicitly assumes T12 without stating it.
**Required**: Add T12 (well-formedness) as a precondition of VSpanImage and propagate it to the CREATELINK composite precondition for V-space endset specifications.

### Issue 6: Unformalized principle cited as established property
**ASN-0063, CL4 — ContentNonInterference, five-principle discussion**: "Owner-only modification. Only the document owner can modify their content (Nelson, LM 2/29)."
**Problem**: No foundation invariant (ASN-0034, 0036, 0043, 0047) establishes owner-only modification. The transition framework's preconditions (K.α, K.μ⁺, etc.) constrain structural validity (entity existence, referential integrity) but do not gate operations on ownership. The property may hold by design intent, but it is not a formal guarantee of the specified system. Citing it as one of five independent principles backing CL4's robustness overstates the formal basis.
**Required**: Either cite the formal property that establishes owner-only modification or reframe it as a design intent ("the system is designed so that...") rather than a proven guarantee.

### Issue 7: Inconsistent notation s_C^V
**ASN-0063, CL6 — ArrangementConfinement discussion**: "The text-subspace mappings — {(v, M(d)(v)) : v ∈ dom(M(d)) ∧ subspace(v) = s_C^V} — are invariant."
**Problem**: `s_C^V` appears once in the entire ASN. Everywhere else — S3★, K.μ⁺_L, CL11, the worked example — the text-subspace identifier is written `s_C` without superscript. If the superscript distinguishes V-position subspace identifiers from I-address subspace identifiers, that distinction is never defined and contradicts the ASN's uniform use of `s_L` for both contexts. If it's a typo, it should be corrected.
**Required**: Replace `s_C^V` with `s_C` for consistency, or define the V/I distinction and use it uniformly.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal and D-CTG preservation under K.μ⁻ in the link subspace
**Why out of scope**: K.μ⁻ applied to a link-subspace V-position would remove a link from its home document's arrangement without removing it from L (L12). Whether D-CTG can be maintained (K.μ⁻ from the interior of a contiguous range breaks contiguity) and what invariants withdrawn links must satisfy are open design questions, not errors in CREATELINK. The ASN properly lists this in its open questions.

### Topic 2: Concurrent CREATELINK serialization
**Why out of scope**: Whether concurrent CREATELINKs targeting the same home document require serialized link-address allocation is a concurrency design question. The ASN's abstract specification operates on single-state transitions; concurrent access is a separate concern.

VERDICT: REVISE
