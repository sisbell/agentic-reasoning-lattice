# Review of ASN-0087

I checked the decomposition, the precondition reduction, the effect, the wp analysis (both cases), the side-effect characterization, and all three classes of invariant preservation against the ASN-0047 reachable-state theorem. The mathematics is sound: invariant coverage is complete (every conjunct of `ExtendedReachableStateInvariants`, plus the composite-boundary and transition invariants, is discharged), boundary cases are handled (empty endset slots, empty link subspace, depth-≥3 pre-states), the worked example checks out arithmetically, and the wp has a genuine non-trivial case (the reflexive route). The D-CTG★ discharge over the full depth-`m_L` slice (the prior cycle's gap) is now correct — the interior-component argument via T1 case (i) is complete.

The findings below are anti-bloat (this note carries `review-mode.anti-bloat`): duplication that the precise reader must work around.

## REVISE

### Issue 1: Effect section restates what Inputs + the formula already establish

**ASN-0087, Effect**: "Whenever MAKELINK is the placing operation the caller never supplies `v_ℓ`: in the non-empty case it is computed from `Σ` (the link subspace's current cardinality at the recorded depth `m_L(d)`), and in the empty (first-link) case its serial component is computed from `Σ` (cardinality 0, giving serial 1) while its depth is supplied by M-DepthConv."

**Problem**: The point that the caller does not supply `v_ℓ` is already made in *Inputs* ("The caller does not specify the link's address or its V-position … the V-position `v_ℓ` is derived from the current state together with … M-DepthConv … its serial component fixed by the link subspace's current cardinality, its depth fixed per M-DepthConv"). The computational detail is already given by the `v_ℓ` formula immediately above this paragraph in the Effect section itself. The paragraph advances no new reasoning — it is the Inputs statement re-said over the just-stated formula.

**Required**: Delete the paragraph. The formula plus the Inputs statement carry the content.

### Issue 2: Claims-table entries M-Inv-Bdry / M-Inv-State / M-Inv-Trans re-derive instead of stating the claim

**ASN-0087, Claims Introduced, M-Inv-Bdry**: "… The three coupling constraints are discharged separately: J0 by `dom(Σ'.C) ∖ dom(Σ.C) = ∅` (frame on C); J1★ by `subspace(v_ℓ) = s_L ≠ s_C` (structural, the new V-position fails J1★'s content-subspace filter); J1'★ by `R' ∖ R = ∅` (frame on R)."

**Problem**: This reproduces verbatim the discharge reasoning already given in the *Composite-Boundary Properties* subsection (the J0 / J1★ / J1'★ paragraphs). The same pattern appears in M-Inv-State (re-listing the by-frame grouping) and M-Inv-Trans (re-stating each conjunct's trivial-frame discharge). A claims-table entry should state *what holds* (e.g., "P4★, P4a, P7a and coupling constraints J0/J1★/J1'★ hold at `Σ'`"); the derivation belongs in the body and is already there. The other table entries (M-WP, M-PriorLinkDisc, M-Effect) correctly state results without re-deriving — these three break that convention and duplicate the body.

**Required**: Reduce M-Inv-State / M-Inv-Bdry / M-Inv-Trans to the claim statement, dropping the embedded discharge reasoning that the *Invariant Preservation* section already carries.

## OUT_OF_SCOPE

None beyond the topics the ASN already correctly defers in its Open Questions (forward-reaching endset well-formedness, deferred-consistency model, type-endset to never-allocated addresses) — those are appropriately routed to future ASNs.

VERDICT: REVISE
