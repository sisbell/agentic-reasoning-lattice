# Review of ASN-0101

## REVISE

### Issue 1: D8 and D10 duplicate the P4★/P4a/P7a neutrality arguments
**ASN-0101, D8** ("The composite-boundary properties P4★, P4a, P7a are not per-state invariants"): the three neutrality bullets establish "DEL cannot break" each property — P4★ via `R'=R` + `Contains_C` shrinkage, P7a via `dom(C')=dom(C)` + `R'=R`, P4a via `R'=R`.
**ASN-0101, D10** ("*Neutrality (D8).*"): "P4★ because `R' = R` ... and DEL only content-subspace-monotone-shrinks `Contains_C`; P7a because `dom(C') = dom(C)` (D2) and `R' = R`; P4a because `R' = R` records no new provenance pair".

**Problem**: The same three neutrality facts are stated twice in two different sections. D10's "Neutrality (D8)" already labels itself as citing D8, then restates D8's content verbatim in substance. This is the "two paragraphs in different sections say the same thing" pattern — a reader following D10's boundary derivation must re-read material already carried in D8.

**Required**: Pick one home for the neutrality facts. Since the *positive* boundary establishment (using J0, J1★, P2) lives only in D10, fold the neutrality statement into D10 and have D8 establish per-state invariants only, deferring composite-boundary handling to D10 by reference. Alternatively, keep the neutrality in D8 and have D10's "Neutrality (D8)" be a one-line citation ("by D8's neutrality bullets") rather than a restatement.

### Issue 2: D8's scope blends per-state preservation with composite-boundary claims
**ASN-0101, D8**: "the post-state satisfies every foundation *per-state* invariant ... **and DEL cannot break any *composite-boundary* property**."

**Problem**: D8 is titled "Arrangement well-formedness preservation" and its three-group structure is a single-transition preservation argument. The composite-boundary properties are not single-transition invariants (D8 itself says so), and their actual establishment requires composite-level premises handled in D10. Carrying a "cannot break" sub-claim about them inside D8 mixes two distinct obligations and is the source of the Issue 1 duplication.

**Required**: Scope D8 to per-state invariants. Move the composite-boundary discussion (including the "not per-state invariants" framing) entirely into D10, where the boundary derivation lives.

### Issue 3: D9 second-bullet parenthetical justifies a notation choice rather than advancing the claim
**ASN-0101, D9, second bullet**: "(The two sides reference the same V-position set: by D6, `V_{S'}(M'(d)) = V_{S'}(d)` for `S' ≠ S`, so the choice of pre-state or post-state subscript yields the same set, and we use the pre-state form `V_{S'}(d)` on both sides for notational consistency.)"

**Problem**: This is meta-prose explaining a subscript-naming convention. The substantive content — that the projection on `S' ≠ S` is unchanged — is already the bullet's claim and is re-justified in the Justification paragraph. The parenthetical adds notation bookkeeping the reader must parse without reasoning gain.

**Required**: Drop the parenthetical; if the equality `V_{S'}(M'(d)) = V_{S'}(d)` needs stating, it is already supplied by D6 and cited in the Justification.

## OUT_OF_SCOPE

None. The ASN stays within DELETE mechanics and correctly defers versioning/recoverability, causal ordering, and orphan-enumeration to its Open Questions rather than legislating them.

VERDICT: REVISE
