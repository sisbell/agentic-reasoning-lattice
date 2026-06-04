# Review of ASN-0087

I checked the decomposition, the precondition reductions, the worked example arithmetic, the wp derivations (both cases), and the full invariant-preservation ledger against ASN-0047's `ExtendedReachableStateInvariants`/`ExtendedTransitionInvariants` and the composite-boundary couplings. The mathematics is sound and complete: every per-state invariant in the theorem is discharged or frame-inherited, S2's exclusion is split correctly into within/cross-subspace cases, the D-CTG★ proof is genuinely depth-general (not assuming `m = 2`), the S8★ link-subspace length-1 decomposition correctly tracks why uniqueness (c) is dropped there, and the Σ_mid atomicity analysis holds. My findings are confined to the anti-bloat lens this note carries.

## REVISE

### Issue 1: "Structurally distinct reasons" overstates a two-vs-one distinction
**ASN-0087, Composite-Boundary Properties**: "The three coupling constraints are vacuously satisfied — but for *structurally distinct* reasons, which we discharge separately"
**Problem**: J0 and J1'★ are discharged by the *same* reason — an empty quantification universe inherited from the frame (`dom(Σ'.C) ∖ dom(Σ.C) = ∅` because `Σ'.C = Σ.C`; `R' ∖ R = ∅` because `Σ'.R = Σ.R`). Only J1★ is structurally different (a nonempty universe with no qualifying content-subspace witness). The "structurally distinct reasons, which we discharge separately" framing inflates two-distinct into three, and the reader must process a three-bullet defensive breakdown to discover that two collapse. This is exactly the meta-prose accretion the classifier targets.
**Required**: Compress to the actual structure — e.g., "J0 and J1'★ hold by empty quantification universe (frame fixes `C` and `R`); J1★ holds because the sole new V-position `v_ℓ` has subspace `s_L ≠ s_C`, so no content-subspace witness arises." Drop the "structurally distinct reasons" sentence.

### Issue 2: Freshness/derivation of `ℓ`, `v_ℓ` restated across three adjacent claims-ledger rows
**ASN-0087, Claims Introduced (M-Pre, M-Alloc, M-Effect)**: M-Pre ("System-supplied parameters: `ℓ` from `A_L(d)`'s next emission; `v_ℓ` from K.μ⁺_L's positioning rule"), M-Alloc ("allocates a fresh `ℓ ∈ T \ (dom(Σ.L) ∪ dom(Σ.C))` and a fresh `v_ℓ`…"), and M-Effect each re-state that `ℓ` and `v_ℓ` are system-derived and fresh.
**Problem**: The same fact (`ℓ`, `v_ℓ` derived and fresh, with `subspace(v_ℓ) = s_L` and depth per M-DepthConv) is carried by three consecutive rows. Two paragraphs/rows saying the same thing in different words is a flagged pattern.
**Required**: Fold the freshness/derivation statement into M-Alloc alone; let M-Pre carry only the caller obligation and M-Effect carry only the state delta.

## OUT_OF_SCOPE

### Topic 1: Protocol-layer atomicity of the composite and well-formedness of forward-reaching endsets
**Why out of scope**: The Open Questions correctly defer composite-level atomicity (the visibility bound on `Σ_mid`) and the well-formedness constraints on endsets covering not-yet-allocated addresses to the protocol layer / a future ASN. These are genuinely new territory, not defects here. I confirm the note introduces no INSERT/DELETE/COPY/REARRANGE/version/BEBE mechanics — scope discipline is clean.

VERDICT: REVISE
