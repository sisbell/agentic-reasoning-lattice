# Review of ASN-0087

## REVISE

### Issue 1: m_L(d) = 2 asserted as universal, not derived
**ASN-0087, Preconditions** (and Effect, Inputs, S8-depth row of M-Inv-State): "`#v_ℓ = m_L(d) = 2` ... otherwise `#v_ℓ = m_L(d)`, the existing link-subspace depth (S8-depth, ASN-0047), **which equals 2 since every prior first link was placed at depth 2 by the same convention**."

**Problem**: The non-empty-case claim that `m_L(d) = 2` is contingent, not established. The ASN itself states the substrate K.μ⁺_L admits *any* `m ≥ 2` and that `Σ` does not determine `m`. For `m_L(d) = 2` to hold universally, every link V-position in every document must have been placed at depth 2 — which requires (a) MAKELINK is the *sole* operation that places link V-positions, and (b) MAKELINK always applies M-DepthConv, plus (c) an inductive argument over document history. None of (a)–(c) is shown. "X equals 2 because of a convention" is an asserted conclusion, not a proof. (The argument is *available* — J4/ForkComposite copies only the content subspace `V_{s_C}`, so links enter only via MAKELINK — but it is never made.) The operation remains *correct* either way, since the non-empty case computes `#v_ℓ = m_L(d)` regardless of value; what is unjustified is the `= 2` annotation.

**Required**: Either derive the universality explicitly (state the standing premise that MAKELINK is the only link-placement path, cite J4's content-only copy, and give the inductive step from M-DepthConv), or drop the `= 2` and state the non-empty case as `#v_ℓ = m_L(d)` without the universal claim.

### Issue 2: v_ℓ freshness justified only within-subspace at point of claim
**ASN-0087, Freshness of the Allocation**: "The V-position `v_ℓ` is fresh in `dom(M(d))` by K.μ⁺_L's positioning rule combined with D-SEQ★ (ASN-0047): the link subspace V-positions form a contiguous sequence ... and `v_ℓ` extends it by one."

**Problem**: This justification establishes only `v_ℓ ∉ V_{s_L}(d)`. The asserted conclusion `v_ℓ ∉ dom(M(d))` additionally requires `v_ℓ ∉ V_{s_C}(d)` — the cross-subspace exclusion via SC-NEQ at position 1. That exclusion is supplied later (correctly) in the S2 verification, but at the point this freshness claim is stated it covers only half of `dom(M(d)) = V_{s_C}(d) ∪ V_{s_L}(d)`.

**Required**: Complete the argument here (add the position-1 `s_L ≠ s_C` exclusion against content positions), or forward-reference the S2 verification rather than citing D-SEQ★ alone.

## OUT_OF_SCOPE

### Topic 1: dom(M) / E_doc reconciliation (ASN-0093 vs ASN-0047)
**Why out of scope**: MAKELINK composes ASN-0093's K.λ (state phrased in `dom(M)`, registration via K.σ) with ASN-0047's K.μ⁺_L (state phrased in `E_doc`, registration via K.δ document case). The two foundations carry different document-registration disciplines, so discharging K.μ⁺_L's `d ∈ E_doc` precondition via `d ∈ dom(M)` rests on a coupling the combined substrate must supply. The ASN transparently defers this to a framework-level reconciliation affecting every operation, not just MAKELINK. This is correctly identified as a future framework ASN — but note it is genuinely load-bearing for the operation's validity, so the soundness of MAKELINK is conditional on it.

### Topic 2: Well-formedness of forward-reaching endsets; protocol-layer atomicity
**Why out of scope**: The Open Questions (constraints on endsets covering not-yet-allocated addresses beyond `e₃ ≠ ∅`; the layer at which composite-level atomicity is enforced) are new territory. The ASN correctly defines what the substrate guarantees (intermediate-state visibility, derived discoverability) and locates atomicity at the protocol layer without overreaching.

VERDICT: REVISE
