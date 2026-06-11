# Review of ASN-0119

I checked the imported ASN-0084 machinery against its claim statements (postcondition equations, R-PPERM/R-SPERM tables, R-COMM displacement constants), re-derived both worked examples numerically (pivot, swap, the two-move composite, all four footprint configurations, the composed bijection table), and audited the invariant discharge against ASN-0047's full conjunct list (per-state, composite-boundary, couplings, P3, M1, NoDeallocation). The arithmetic checks out everywhere I tested it: the pivot and swap tables match R-P1/R-P2 and R-S1–S3, the composed `π₂ ∘ π₁` equals the atomic `π`, the middle-region displacement `w_β − w_α` is correct, RA8b's three-way inequality is properly grounded in the stipulated distinct-allocation pre-state, and the RA2a/S3★/J1★ chain is sound — including the correct observation that full-range invariance (RA1) alone does not settle J1★. The conjunct accounting is complete: I could not find a member of ExtendedReachableStateInvariants, the boundary properties, or the couplings left undischarged, and the value-dependent trio (S8★, CL-OWN, CL-UNIQ) each receives a positive argument rather than riding the key-set inheritance. The K.μ~ coincidence discharge is honest about the value-degenerate non-coincidence and covers clauses (i)–(v).

One residue item remains under the anti-bloat mode.

## REVISE

### Issue 1: notation convention declared, never used, and contradicted by the rest of the note
**ASN-0119, "The two streams"**: "Because `E` and `R` are inert under the operation, we suppress them from the state-tuple notation and write `Σ = (C, M, L)` for the active components."
**Problem**: The suppressed tuple `Σ = (C, M, L)` never appears again anywhere in the note. More to the point, the suppression is not actually exercised: `E` and `R` are named explicitly and repeatedly throughout — RA4 itself is stated as `Σ'.E = Σ.E ∧ Σ'.R = Σ.R`, the P3 discharge writes `E = E', R = R'` at equality, the closure rule keys conjuncts on "`E` and `R` by RA4," and the claims table carries the full equations. A convention announced in one sentence and abandoned everywhere downstream is exactly the residue the anti-bloat pass targets, and it carries a mild hazard: a reader could take it to mean `E` and `R` have been dropped from the formal state, when the invariant-discharge section depends on their being first-class frozen components.
**Required**: Delete the sentence. The preceding sentence in the same paragraph already does the real work (extending ASN-0084's frame with RA6 and RA4 for the components it does not name); nothing downstream consumes the `(C, M, L)` shorthand. While editing that passage, the trailing "— by the same discipline" can be tightened or dropped: its referent is unstated and the clause adds nothing to the frame-extension statement it ends.

## OUT_OF_SCOPE

None. The future-work surface I encountered while reviewing — run-structure guarantees for footprints spanning three or more regions, concurrent rearrangement serialization, cross-document boundary-hood under transclusion, recoverability of the prior arrangement, and the displacement-arithmetic refinement guard — is already fenced by the ASN's own Open Questions section, and none of it is an error in this note.

VERDICT: REVISE
