# Review of ASN-0087

## REVISE

### Issue 1: K.σ vs K.δ-IsDocument reconciliation is asserted, not derived
**ASN-0087, "Inputs" (notation convention paragraph)**: "document registration occurs by K.σ (ASN-0093) or by K.δ in the IsDocument case (ASN-0047), each of which simultaneously enters `d` into both `dom(M)` and `E_doc`"

**Problem**: ASN-0093's K.σ definition specifies effect `dom(M') = dom(M) ∪ {d}` with frame `C' = C; L' = L`. It does not mention `E` at all — ASN-0093 has no entity component. ASN-0047's K.δ-IsDocument adds to both `E` and `dom(M)`. These are structurally different operations. The claim that "K.σ simultaneously enters d into both dom(M) and E_doc" extends K.σ's definition beyond what ASN-0093 establishes.

**Required**: Either (a) state that K.σ is superseded by K.δ-IsDocument in the combined model and use K.δ-IsDocument throughout, (b) extend K.σ's definition in this ASN to also update E (and justify the extension), or (c) note that the combined model imposes the bidirectional invariant `d ∈ dom(M) ⟺ d ∈ E_doc` as an additional constraint not present in either foundation ASN alone. The current phrasing implies the reconciliation is mechanical when it actually requires a design choice.

### Issue 2: L1c chain uniqueness argument uses an underived "structural target"
**ASN-0087, "Per-State Invariants at Σ'" (kⱼ = 0 for j ≥ 4 case)**: "The `k = 1` branch extends length to `#d + 4`; by fact (b), no subsequent address has length `#d + 3`, contradicting the structural target `#ℓ = #d + 3` (forced by L0 and L1 together with the established chain structure)."

**Problem**: L0 says `E(ℓ)₁ = s_L`. L1 says `zeros(ℓ) = 3`. Neither alone nor jointly forces `#ℓ = #d + 3`. A tumbler like `[d, 0, 2, 1, 1]` satisfies both L0 and L1 (zeros at positions 2, 4, #d+1; E starts with 2; #E = 3 ≥ 2 per L1b) with `#(·) = #d + 4`. The bound `#ℓ = #d + 3` follows from K.λ's emission rule (ℓ comes from `A_L(d)`'s chain) combined with ChainUniformLength (ASN-0093), not from L0 + L1.

**Required**: Cite the actual source — either K.λ's emission precondition (which restricts ℓ to A_L(d) outputs) or ChainUniformLength + ChainMembershipForOrigin. The current "L0 and L1 together with the established chain structure" reads as if the constraint is purely structural when it is operational.

### Issue 3: Σ_mid invariant analysis is selective, not comprehensive
**ASN-0087, "Atomicity" section**: "the per-state invariants hold at Σ_mid: *S3★ (referential integrity)*... *L0, L1, L1a, L1b, L3 on the new entry ℓ*... *L1c at Σ_mid*... *L14*... *L-fin*... *Prior entries*..."

**Problem**: The ASN claims `Σ_mid` is "a fully reachable state" satisfying per-state invariants, but the verification covers only L-invariants and S3★. The full per-state invariant set established earlier (S2, S3★-aux, S8a, S8-depth, S8-fin, S8★, CL-OWN, CL-UNIQ, D-MIN★, D-CTG★, D-SEQ★, M0, S4, S7a–d, C-fin, P6, P7, P8, NodeLineage) is not checked at `Σ_mid`. Most are vacuous because `Σ_mid.M = Σ.M` and `Σ_mid.C = Σ.C`, but this is not stated.

**Required**: Either explicitly note that `Σ_mid.M = Σ.M` and `Σ_mid.C = Σ.C` discharges every M-side and C-side per-state invariant by inheritance from Σ, or expand the verification to cover each invariant. The current selective treatment leaves the reader to verify gaps that K.λ's frame structure makes trivial.

### Issue 4: "Standard authoring" is used as a hypothesis without being defined
**ASN-0087, "Weakest Precondition for Discoverability", "Reflexive Endsets", "Side Effects on Prior Links' Discoverability"**: Repeated reference to "standard authoring" with parenthetical glosses ("endsets reference *already-existing* substrate addresses (`coverage(eᵢ) ⊆ dom(Σ.C) ∪ dom(Σ.L)` at `Σ`)").

**Problem**: "Standard authoring" is used to scope key results (wp reductions, exclusion of reflexive case, vacuity of side effects on prior links), yet it has no formal definition. The parenthetical glosses are inconsistent — sometimes the constraint is on `coverage(eᵢ)`, sometimes on the caller's knowledge of ℓ at endset-formation time. These are not the same predicate.

**Required**: Introduce "standard authoring" as a named, formally-stated discipline (e.g., `StandardAuthoring(e, Σ) ≡ (A (s, ℓ) ∈ e :: coverage({(s, ℓ)}) ⊆ dom(Σ.C) ∪ dom(Σ.L))`) and cite it uniformly. The current usage muddles a structural constraint on endsets with an epistemic constraint on the caller.

### Issue 5: Cross-document discovery cascade is not analyzed
**ASN-0087, "Side Effects on Prior Links' Discoverability"**: The biconditional characterising when ℓ' becomes newly discoverable from d covers the case where ℓ' has an endset reaching the fresh ℓ. The corresponding analysis for the new link ℓ and its discoverability from documents *other than d* (`d_target ≠ d`) is in M-WP Case 1.

**Problem**: What is missing is the analysis of *interaction* between these two effects. If ℓ has an endset reaching a₃ in document d', then ℓ is discoverable from d' (M-WP Case 1). Simultaneously, if some prior link ℓ' has an endset reaching ℓ, ℓ' becomes newly discoverable *from d* (M-PriorLinkDisc). These two effects are independent in the ASN's treatment but compose under sequential MAKELINK invocations. No analysis is given of whether such cascades preserve well-formedness across composite sequences.

**Required**: Either state that the cascade is bounded by LP9 + LP13 + L12 (no cascade can violate any preserved invariant because discoverability is a derived predicate, not state) or analyse the cascade structure explicitly. The single-step analysis is correct but leaves the multi-MAKELINK case implicit.

### Issue 6: M-Inv-Bdry's vacuity claim for J0, J1★, J1'★ could be tighter
**ASN-0087, "Composite-Boundary Properties"** and **M-Inv-Bdry**: "J0, J1★, J1'★ are vacuously satisfied (no content-subspace allocation, no content-subspace range growth)."

**Problem**: J0 quantifies over `dom(C') \ dom(C)` which is empty here — vacuous by emptiness of the universe. J1★ and J1'★ quantify over content-subspace V-positions whose image changed. The vacuity of J1★ follows from `subspace(v_ℓ) = s_L ≠ s_C`, not just from "no content-subspace allocation". A future change to MAKELINK that *also* placed something in the content subspace would still leave J1★ to verify. The ASN's collective vacuity claim conflates two independent reasons.

**Required**: Discharge J0 by `dom(Σ'.C) \ dom(Σ.C) = ∅` and J1★/J1'★ by `subspace(v_ℓ) = s_L`, separately. The current grouping obscures which structural feature of MAKELINK is doing the work for each coupling constraint.

VERDICT: REVISE
