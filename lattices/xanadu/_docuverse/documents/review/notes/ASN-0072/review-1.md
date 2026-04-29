# Review of ASN-0072

## REVISE

### Issue 1: Pervasive cross-references to ASN-0043 (not a foundation ASN)
**ASN-0072, throughout**: "L : T ⇀ Link is the link store (ASN-0043)", "L14, ASN-0043", "L0, L1 — ASN-0043", "L1a — ASN-0043", "L3 — ASN-0043", "L12 (LinkImmutability, ASN-0043)"
**Problem**: ASN-0043 is not listed as a foundation ASN. The ASN uses six labeled invariants/definitions from it (L0, L1, L1a, L3, L12, L14) plus the `Link` type, none of which are restated. The reader cannot verify K.λ's preconditions, L14 preservation arguments, or S3★'s link-subspace clause without ASN-0043. The `Link` type — the codomain of the link store — is entirely opaque: `(F, G, Θ) ∈ Link` appears in K.λ but the structural constraints on F, G, Θ are unknown.
**Required**: Either elevate ASN-0043 to foundation status (with extracted formal statements), or restate every definition used: the `Link` type, L0 (both clauses), L1, L1a, L3, L12, L14. Inline paraphrases ("L14 says dom(L) ∩ dom(C) = ∅") do not substitute for formal definitions — they cannot be verified against the source.

### Issue 2: s_C and s_L are undefined symbols; s_C ≠ s_L is never established
**ASN-0072, throughout**: `s_C` and `s_L` appear in every section — K.α amendment, K.μ⁺ amendment, S3★, S3★-aux, K.μ⁺_L, CL-OWN, Contains_C, the main theorem proof.
**Problem**: Neither symbol is formally defined. The ASN derives `s_L ≥ 1` (from L1 + T4) and `s_C ≥ 1` (from S8a), but the critical property `s_C ≠ s_L` — required for every disjointness argument (T7, L14 preservation, the S3★ fixity elimination step) — is never stated as an axiom or derived. Without it, the argument "fields(a).E₁ = s_C, and L0 clause 1 at the pre-state gives fields(ℓ).E₁ = s_L, so a ∉ dom(L)" is incomplete: if s_C = s_L, content and link addresses share a subspace and T7 gives no separation.
**Required**: Define s_C and s_L as subspace identifiers (either as specific values per the vocabulary — s_C = 1, s_L = 2 — or as parameters), and state `s_C ≠ s_L` as an axiom or derive it from L0's partition. Also clarify that the subspace identifier serves the same role for V-positions (`subspace(v) = v₁`) and I-addresses (`fields(a).E₁`).

### Issue 3: P4★ and P7a are composite-level invariants, but the proof claims per-elementary preservation
**ASN-0072, ExtendedReachableStateInvariants proof**: "Inductive step: each elementary transition preserves the full invariant set."
**Problem**: This claim is false for P4★ and P7a.

P4★ (`Contains_C(Σ) ⊆ R`): K.μ⁺ alone adds a content-subspace V-position mapping to address `a`, placing `(a, d) ∈ Contains_C(Σ')`. Its frame has `R' = R`, so if `(a, d) ∉ R`, P4★ is violated. Only the composite-level coupling constraint J1★ — ensuring K.ρ is paired with K.μ⁺ — restores P4★.

P7a (`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`): K.α alone adds `a` to `dom(C')`. Its frame has `R' = R`, so `(a, d) ∉ R` for the newly allocated `a`. Only J0 + J1★ at the composite level guarantee placement and provenance.

The proof partially acknowledges this: "K.μ⁺ ... is coupled with K.ρ by J1★." But this is a composite argument embedded in a per-elementary structure. Intermediate states within a composite may violate P4★ and P7a, so induction on elementary transitions cannot establish them.
**Required**: Restructure the proof into two layers: (a) invariants preserved by each elementary transition individually (all except P4★, P7a), and (b) invariants preserved at valid composite boundaries, via coupling constraints J0, J1★, J1'★. State explicitly that P4★ and P7a may not hold at intermediate states within a composite.

### Issue 4: No concrete worked example
**ASN-0072, all sections**
**Problem**: The ASN defines K.λ and K.μ⁺_L abstractly but never verifies the key postconditions against a specific scenario. For instance: document d at address `1.0.1.0.1` with two text spans and no links; K.λ allocates link ℓ = `1.0.1.0.2.1`; K.μ⁺_L places it at V-position `[2, 1]` — then verify S3★, CL-OWN, L14, D-MIN concretely. A second example showing K.μ~ preserving link-subspace fixity (e.g., a three-text-span, one-link arrangement under reordering) would ground the abstract fixity argument.
**Required**: Add at least one worked example covering the K.λ → K.μ⁺_L sequence, verifying the central postconditions (S3★, CL-OWN, L14, D-CTG/D-MIN) on concrete tumbler values.

### Issue 5: L3 missing from ExtendedReachableStateInvariants
**ASN-0072, ExtendedReachableStateInvariants**: The theorem lists 26 invariants.
**Problem**: L3 (link well-formedness) is not listed. K.λ's precondition requires `(F, G, Θ) ∈ Link` per L3, and L12 (immutability) preserves link values forever. Therefore every link in dom(L) satisfies L3 in every reachable state. This is a reachable-state invariant by construction — K.λ establishes it, L12 preserves it, and no other transition modifies L — yet the theorem omits it.
**Required**: Add L3 to the ExtendedReachableStateInvariants invariant list (contingent on L3 being formally stated per Issue 1). The preservation argument is one sentence: "K.λ creates links satisfying L3 (precondition); L12 preserves all existing entries; no other transition modifies L."

## OUT_OF_SCOPE

### Topic 1: Link-subspace injectivity
K.μ⁺_L does not prevent the same link address ℓ from being arranged at multiple V-positions in the same document. S5 (UnrestrictedSharing) permits this for content, and no restriction is imposed for links. Whether the link subspace should enforce injectivity (each link appears at most once) is a link-ordering question for a future ASN.
**Why out of scope**: The ASN correctly inherits S5's permissiveness; restricting it for links is a new constraint, not a gap in this ASN.

### Topic 2: Endset referential integrity
K.λ accepts `(F, G, Θ) ∈ Link` per L3, but whether endset span addresses must reference `dom(C)` is not addressed. This depends on ASN-0043's definition of L3.
**Why out of scope**: Link endset semantics belong in the link ontology (ASN-0043), not the transition integration.

### Topic 3: Link withdrawal mechanism
Explicitly deferred in the open questions: "What invariants must link withdrawal maintain — must withdrawn links remain arranged, or does withdrawal remove them from M(d)?"
**Why out of scope**: The ASN correctly identifies this as future work and documents the constraints any future mechanism must satisfy (D-CTG suffix truncation or inactive-status alternative).

VERDICT: REVISE
