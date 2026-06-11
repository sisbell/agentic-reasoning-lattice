# Review of ASN-0120

## REVISE

### Issue 1: `wf` does not enforce the depth its own gloss asserts
**ASN-0120, "What the endset arguments name, and what resolution recovers"**: "Each `σ_j` thus names an allocated source (`d_j ∈ dom(Σ.M)`), lies in the *content subspace* (`subspace(u_j) = s_C`) at the common content V-position depth `m = #u_j ≥ 2` in `d_j` (ASN-0058), …"
**Problem**: The formal predicate contains only `#u_j ≥ 2`; nothing ties `#u_j` to the common depth that S8-depth fixes on `V_{s_C}(d_j)`. The prose asserts the alignment as if `wf` guaranteed it. The two come apart on real inputs: a depth-2 spec `u_j = [1,1]` against a document whose content subspace has common depth 3 satisfies `wf`, and its interval `⟦σ_j⟧` *does* capture depth-3 active positions ([1,1] ≤ [1,1,1] < [1,2] under T1), so `ρ` resolves them. The confinement argument and the containment `ρ ⊆ dom(Σ.C)` survive this (they use only `m = #u_j ≥ 2` and prefix sharing), but the operation's precondition then admits specs whose boundaries cut the arrangement at a depth the document does not use — a behavior the prose flatly denies and the claims table repeats ("each `σ_j` content-subspace at depth `m`").
**Required**: Either add the conjunct (`V_{s_C}(d_j) ≠ ∅ ∧ #u_j = m_{s_C}(d_j)`, ASN-0058 ContentReference condition (iii) style) to `wf`, or correct the prose to say depth-match is *not* required and state what `ρ` recovers under mismatch. Pick one; the formula and its gloss must agree.

### Issue 2: Elementary precondition discharge gaps (K.μ⁺_L and K.λ)
**ASN-0120, "Residence, and its independence…"**: "`a` is link-subspace and fresh (`a ∉ dom(Σ.L)` before `K.λ`), so since the link-subspace range of `M(d)` lies entirely in `dom(Σ.L)` (S3★/CL-OWN, ASN-0047) we have `a ∉ ran(M(d))`"
**Problem (a)**: The case analysis is incomplete. `a ∈ ran(M(d))` would mean `M(d)(v) = a` for some `v`; by S3★-aux, `subspace(v)` is `s_C` or `s_L`. The quoted argument closes only the `s_L` branch (link-subspace images lie in `dom(Σ.L)`, which `a` is not in). The `s_C` branch — `a` appearing as a content-subspace image, hence `a ∈ dom(Σ.C)` — is never excluded by the cited facts. It is closable (FirstEmissionFreshness/SubsequentEmissionFreshness give freshness against `dom(C) ∪ dom(L)`, or L0 gives `subspace_I(a) = s_L ∉` the content store's subspace), but the closing step must be written.
**Problem (b)**: "The endset is the finite set of these spans" asserts finiteness without discharging it. K.λ's precondition requires `eᵢ ∈ Endset = 𝒫_fin(Span)`, so finiteness of `ρ(R, Σ)` is a proof obligation, not a description. It follows in one line — `p` is finite and each `dom(Σ.M(d_j))` is finite by S8-fin — but the line is missing.
**Required**: (a) State the two-branch exclusion via S3★-aux, closing the content branch explicitly. (b) Cite S8-fin for finiteness of `ρ` where the endset is packaged.

### Issue 3: ML10's frame omits E and R, and J1'★'s vacuity is misgrounded
**ASN-0120, ML10 and "The substrate we build on"**: "Σ'.C = Σ.C; (A d' ≠ d : Σ'.M(d') = Σ.M(d')); existing Σ.L entries unchanged" and "no content-subspace range-new I-address (J1★, J1'★ vacuous)".
**Problem**: The ASN works inside ASN-0047's extended state — it invokes ValidComposite★, J0/J1★/J1'★, K.λ and K.μ⁺_L, whose frames include `E' = E` and `R' = R` — yet ML10 states neither. An implementer reading ML10 cannot tell whether MAKELINK may create entities or record provenance. Moreover the J1'★ vacuity argument is wrong as stated: J1'★ quantifies over `(a, d) ∈ R' \ R`, so "no content-subspace range-new I-address" does not make it vacuous — if `R` grew without a range-new address, J1'★ would be *violated*, not vacuous. Vacuity needs `R' \ R = ∅`, which holds precisely by the `R' = R` frame clauses of K.λ and K.μ⁺_L that the ASN never states.
**Required**: Add `E' = E ∧ R' = R` to ML10 (inherited from the two transitions' frames), and ground J1'★'s vacuity on `R' = R` rather than on the absence of range-new addresses.

### Issue 4: Worked example — the type spec is not concrete, and the contiguity remark contradicts the example's own data
**ASN-0120, "A worked example"**: "A type address `θ₁` is held somewhere stable." and "The two runs of `e₁` stay separate when `a₁, a₂` are non-adjacent in I-space".
**Problem**: First, `ρ(R₃, Σ) = {θ₁}` requires a named source document `d₃ ∈ dom(Σ.M)` with an active content-subspace V-position mapping to `θ₁ ∈ dom(Σ.C)`; "held somewhere stable" exhibits none of this, yet ML6's precondition is one of the two definedness conditions the example exists to check. Second, the example's own addresses `a₁ = A.0.s_C.1` and `a₂ = A.0.s_C.2` are consecutive chain siblings — *adjacent* in I-space — so the "when non-adjacent" remark does not describe the case constructed; whether the two entries merge there actually turns on V-adjacency of the two source positions (M7 requires both), which the example also leaves unspecified.
**Required**: Name the type's source document and active V-position explicitly; either choose genuinely non-adjacent resolved addresses for the two-run illustration or state the V-positions and apply M7's two-sided condition correctly.

### Issue 5: Meta-prose accretion
**ASN-0120, several sections**
**Problem**: Instances of author-to-reviewer prose that do not advance any claim: (i) "We diverge from `resolve` in one deliberate respect *and name it as such*" and "this generalization is required, not incidental" — defensive justification; the divergence itself (partial spans) is the content, the apologia is noise. (ii) "Two structural facts about resolution deserve emphasis, both abstract" — framing that announces instead of stating. (iii) "The ordinal-displacement conjunct is load-bearing: … (derived below)" pre-announces the confinement derivation that appears in full two paragraphs later — the same content twice. (iv) The closing paragraph ("These ten claims are not independent demands … facets of one decision … refracted through…") restates the introduction's thesis ("the whole content of MAKELINK is a single conversion of coordinates") and adds nothing. (v) The Gregory CREATELINK observation in the ML6 paragraph sits as an inline parenthetical, breaking the blockquoted *Implementation note* convention used everywhere else in the document.
**Required**: Delete (i), (ii), (iv); keep the confinement derivation in one place only; move (v) into an implementation-note block.

### Issue 6: "The consultation" — dangling referent grounding ML5's directionality claim
**ASN-0120, "Three endsets…"**: "The consultation forces the first reading and forbids the second."
**Problem**: ML5's directionality half — semantic labeling, not traversal restriction — is justified by appeal to "the consultation," a source with no antecedent in this ASN. A self-contained note cannot rest a claim's grounding on an unnamed external process. The actual support is already present in the same paragraph: the Nelson quotation and the symmetry of the discoverability test (ML9).
**Required**: Drop the "consultation" sentence and ground the reading directly on the quoted Nelson line plus the endset-symmetry of LP12/ML9.

## OUT_OF_SCOPE

### Topic 1: Direct I-address endset arguments (ghost types, foreign endsets)
**Why out of scope**: The ASN correctly restricts itself to V-spec arguments and notes that reaching ghost or link-subspace addresses requires a different argument shape; specifying that shape (and its interaction with L9/L4 generality) is a future ASN, not a defect here.

### Topic 2: Link deletion / owner-side removal
**Why out of scope**: ML7 deliberately scopes permanence to "no one else's edit can break it" and defers owner deletion to a separate operation; that operation's contract is new territory.

VERDICT: REVISE
