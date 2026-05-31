# Review of ASN-0084

The mathematics here is sound. I traced all five worked examples, the well-definedness lemmas (R-PIV, R-SWP), both permutation lemmas (R-PPERM, R-SPERM), the commutation lemma (R-COMM), and R-CANON's forward/backward-extension arguments — they hold, including the depth-m>2 generalization for non-S subspaces in R-CANON and the boundary configurations. My findings are confined to accreted meta-prose, which this note's `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Defensive "derived vs assumed" justification lodged in the Properties table
**ASN-0084, "Properties Introduced," R-PRE row**: "(Region non-emptiness — w_α, w_β ≥ 1 in both forms, w_μ ≥ 1 when n = 4 — is *derived*, the Width-positivity consequence of (iii)+(iv)+CS2, not an assumed clause.)"
**Problem**: The Statement column of a structural summary table carries a parenthetical defending against a misreading (that width-positivity might be an assumed precondition clause). This is exactly a defensive justification occupying a structural slot — the reader scanning the table for R-PRE's statement must work past prose arguing what R-PRE does *not* assume. The Width-positivity consequence is already derived in full under "Consequences of R-PRE"; the table need only state R-PRE's four clauses.
**Required**: Reduce the R-PRE row's Statement to the precondition clauses (i)–(iv). Drop the derived/assumed parenthetical; it belongs (and already lives) in the Width-positivity consequence.

### Issue 2: The "shift preserves subspace" fact is re-argued inline at four sites
**ASN-0084**: the single foundation fact (OrdShiftHom (a): a within-run/in-region shift preserves the subspace) is independently re-derived at:
- *Consequences of R-PRE, Subspace confinement*: "OrdShiftHom (a) of ASN-0036 gives subspace(c_i + j) = subspace(c_i) = S."
- *R-BLK, Phase 1, Non-S runs*: "By OrdShiftHom (a) of ASN-0036, every V-position v_b + k satisfies subspace(v_b + k) = S' ≠ S".
- *R-CANON, opening facts*: "shift preserves the subspace (OrdShiftHom (a), ASN-0034)."
- *Link-subspace worked example*: "by OrdShiftHom (a) of ASN-0036 every shift within a run preserves the subspace."

**Problem**: This is not the OrdShiftHom-(b) miscitation declined earlier — every citation here is correctly (a). The issue is accretion: the same lemma instance ("a run/region lies entirely within one subspace because shift fixes the subspace") is rebuilt from scratch in each proof rather than established once and cited. R-BLK and R-CANON in particular re-derive identical content for runs in arbitrary subspaces.
**Required**: State once — e.g., as a named consequence near the State section ("every correspondence run lies within a single subspace; any in-region shift preserves it, by OrdShiftHom (a)") — and have R-BLK, R-CANON, and the link example cite it rather than re-argue it.

### Issue 3: EXT-VAC(a) is a consequence with no proof consumer
**ASN-0084, "Consequences of R-PRE," EXT-VAC**: "(a) When ord(c₀) = 1, no V-position satisfies v < c₀ ... so the left-exterior set {v ∈ V_S(d) : v < c₀} is empty."
**Problem**: EXT-VAC(b) (empty right exterior / c_{n−1} ∉ dom(M(d))) is consumed by R-BLK Phase 1. EXT-VAC(a) is consumed by no lemma — only a worked example exercises it. Stating a derived boundary fact in the consequences block when no proof uses it is premature accretion; the example can establish its own left-exterior emptiness inline.
**Required**: Either cite EXT-VAC(a) at a lemma that actually needs it, or demote it from the consequences block into the boundary worked example where it is the only use.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: These are correctly captured as Open Questions. Generalizing the cut count and characterizing whether composed rearrangements remain single rearrangements is new territory for a future ASN, not a gap in this one.

### Topic 2: Weakest-precondition characterization of REARRANGE_K
**Why out of scope**: The note defers the wp of the post-state invariant suite to an Open Question and supplies invariant preservation (R-RI plus the invariant-preservation audit) instead. A full wp analysis is a legitimate future increment, not an error here.

VERDICT: REVISE
