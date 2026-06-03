# Review of ASN-0087

## REVISE

### Issue 1: K.μ~ reordering cannot rebind a link's V-position
**ASN-0087, Permanence**: "Subsequent operations may remove it (per the contraction operation's rules) or rebind its image (per the reordering operation's rules — K.μ~ … what changes is which value M(d)(v_ℓ) maps to, and where ℓ re-appears as the image of some other V-position)."
**Problem**: K.μ~ admissibility clause (v) (ASN-0047) is *link-subspace fixing*: `(A v ∈ dom_L(M(d)) :: π(v) = v)`. Since `v_ℓ` is a link V-position, `π(v_ℓ) = v_ℓ` and the bijection equation gives `M'(d)(v_ℓ) = M(d)(v_ℓ) = ℓ`. The link binding `v_ℓ ↦ ℓ` is therefore *invariant* under K.μ~. The claim that reordering rebinds `M(d)(v_ℓ)` or moves `ℓ` to another V-position is false; only K.μ⁻ can remove it.
**Required**: Correct the statement to reflect that K.μ~ fixes the entire link subspace; the only mutation of `v_ℓ ↦ ℓ` available is removal by K.μ⁻.

### Issue 2: V-position depth fixed at 2 via a non-existent axiom
**ASN-0087, Preconditions / Effect**: "`#v_ℓ = m_L = 2` [by LinkVPositionDepthAxiom (ASN-0047)]"
**Problem**: No "LinkVPositionDepthAxiom" exists in ASN-0047. Worse, ASN-0047's K.μ⁺_L explicitly permits the *first* link V-position to have any chosen depth: `ValidFirstLinkPosition(d, v_ℓ, m)` "for any chosen `m ≥ 2`". The depth `m_L` is a free parameter at first allocation (pinned only thereafter by S8-depth), not a fixed 2. Hardcoding 2 and the "at depth 2" qualifiers throughout (Preconditions, Effect, positioning rule, S8-depth/D-MIN★/D-CTG★ discharges) over-constrains the operation.
**Required**: Use `m_L(d) ≥ 2` (with the first link's `m` chosen per ValidFirstLinkPosition); remove the invented axiom citation. The worked example may pick `m = 2`, but the general Effect must not fix it.

### Issue 3: Phantom invariant citations S7c and S9
**ASN-0087, Per-State Invariants / Atomicity / Transition Invariants**: "S7a, S7b, S7c, S7d (origin and structural attribution …)" and "S9 (TwoStreamSeparation, ASN-0036)".
**Problem**: ASN-0036 defines S7, S7a, S7b, S7d — there is no **S7c**. ASN-0036 (and ASN-0093) define no **S9 / TwoStreamSeparation**. Both are cited as discharged/relied-upon foundation claims that do not exist.
**Required**: Remove S7c; replace S9 with an actual foundation claim (e.g., the relevant content/link separation is L14 + S0/P0) or delete the appeal.

### Issue 4: Per-state invariant verification omits C1b, C1c, ActivatedEmission
**ASN-0087, M-Inv-State / Per-State Invariants at Σ'**: vacuous list is "(M0, S4, S7a, S7b, S7c, S7d, C-fin, P6, P7, P8, NodeLineage)".
**Problem**: ASN-0047's ExtendedReachableStateInvariants requires C1b ∧ C1c ∧ ActivatedEmission at every reachable state. These are absent from the verification while the non-existent S7c is included. They are vacuous under MAKELINK (C and E unchanged), but the ASN claims an exhaustive per-state discharge.
**Required**: Add C1b, C1c (vacuous via `Σ'.C = Σ.C`) and ActivatedEmission (vacuous via `Σ'.E = Σ.E`) to the discharged set.

### Issue 5: Cited labels LP2★ and ChainUniformLength are not defined in the foundations
**ASN-0087, Permanence of the Recording / L1c uniqueness table**: "By LP2★ (ASN-0098) …"; "contradicting ChainUniformLength's `#ℓ = #t_1^L(d) = #d + 3`".
**Problem**: ASN-0098 defines LP2 and LP3★ (and the closure schema) but no named **LP2★**. ASN-0093 has no **ChainUniformLength** lemma. The multi-step value preservation is already supplied by LP13 (and LP3★ for coverage); the uniform-length fact must be derived from a named foundation result.
**Required**: Replace LP2★ with LP13 (or "schema (★) applied to LP2"); replace ChainUniformLength with an actual ASN-0093 result, or derive the length fact explicitly.

## OUT_OF_SCOPE

### Topic 1: Reconciliation of `dom(M)` (ASN-0093) and `E_doc` (ASN-0047)
**Why out of scope**: The ASN discharges K.μ⁺_L's `d ∈ E_doc` precondition via `d ∈ dom(M)` under an explicitly assumed coupling, and names a future substrate-reconciliation ASN as the proper site. This is a genuine framework-wide concern affecting every operation, not a defect local to MAKELINK — provided the assumed coupling is clearly flagged as an open dependency (which it is).

### Topic 2: Endset well-formedness for spans referencing unallocated I-addresses
**Why out of scope**: The forward-reaching endset case (L4 generality, resurrection via LP18) is acknowledged in the Open Questions; defining additional well-formedness constraints is new territory for a future ASN.

VERDICT: REVISE
