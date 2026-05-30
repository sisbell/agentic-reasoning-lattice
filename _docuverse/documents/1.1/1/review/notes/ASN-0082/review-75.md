# Review of ASN-0082

The mathematics here is sound — I checked the displacement arithmetic (OrdAddHom, OrdinalExceedsDisplacement, the ℕ-identity in D-S), the bijection/gap-closure chain (D-BJ → D-SEP → D-DP → D-CTG-post), and the boundary worked examples (L=∅, R=∅, full deletion, cross-subspace). They hold. The findings below are the meta-prose accretion the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Use-site inventory in OrdinalExceedsDisplacement
**ASN-0082, Lemma OrdinalExceedsDisplacement**: "The `#v = 2` hypothesis is discharged at every application site: for `v ∈ R ⊆ V_1(d)` (D-BJ, D-SHIFT, D-SEP) S8-depth fixes the common subspace-1 depth at `#p = 2`; ... The lemma is stated over tumblers of fixed depth 2 so that neither defense need be re-argued in its body."
**Problem**: This is exactly the flagged pattern — a lemma statement enumerating its downstream consumers (D-BJ, D-SHIFT, D-SEP) and explaining why it is structured the way it is ("so that neither defense need be re-argued"). The consumer list and the structural-rationale sentence advance no reasoning; they read as residue from a prior "where is #v=2 discharged?" cycle. The only load-bearing content is the `v = r` sentence (r ∉ dom(M(d)), so the result-length identity, not S8-depth, supplies `#r = 2`).
**Required**: Keep the `v = r` justification. Cut the consumer enumeration "(D-BJ, D-SHIFT, D-SEP)" and the "so that neither defense need be re-argued in its body" rationale. The hypothesis stands as a precondition; consumers discharge it at their own sites.

### Issue 2: D-SEP(a) restates the upstream proof rather than citing it
**ASN-0082, D-SEP, Proof of (a)**: "The identity `ord(r) ⊖ w_ord = ord(p)` is established as a load-bearing intermediate in OrdinalExceedsDisplacement (i) (where it is discharged via TA4 (PartialInverse, ASN-0034) on `(ord(p) ⊕ w_ord) ⊖ w_ord = ord(p)`, using ord(r) = ord(p) ⊕ w_ord from OrdAddHom (a)); we cite it here directly."
**Problem**: The parenthetical re-derives the upstream proof mechanism (TA4, the OrdAddHom step) that already lives in OrdinalExceedsDisplacement (i). This is cross-reference accretion — the reader does not need the upstream derivation reproduced to accept a citation.
**Required**: Reduce to the citation: "By OrdinalExceedsDisplacement (i), ord(r) ⊖ w_ord = ord(p)." Drop the parenthetical.

### Issue 3: Redundant re-derivation inside D-BJ proof of (a)
**ASN-0082, D-BJ, Proof of (a)**: "For every v ∈ R we have v ≥ r, so OrdinalExceedsDisplacement (ii) gives `ord(v) ≥ w_ord` directly (and the strict `ord(v) > w_ord`). At depth #p = 2 this reads `ord(v) = [v₂] ≥ [c] = w_ord` with `c = w₂ ≥ 1`. ∎(derivation of `ord(v) ≥ w_ord`)"
**Problem**: OrdinalExceedsDisplacement (ii) already delivers `ord(v) ≥ w_ord` for every `v ∈ R`. The depth-2 component restatement and the standalone `∎(derivation of ...)` block add nothing the cited lemma does not already provide; it is the citation expanded back into a sub-proof.
**Required**: Collapse to the citation of OrdinalExceedsDisplacement (ii) as the precondition feed for TA3-strict; remove the depth-2 restatement and the embedded ∎ tag.

## OUT_OF_SCOPE

### Topic 1: Depth > 1 generalization of D-SEP / D-DP
**Why out of scope**: The third Open Question (TA4's zero-prefix precondition colliding with S8a positivity at intermediate components) is genuine future territory. The contraction's depth axiom #p = 2 is a deliberate scoping, correctly fenced; deeper ordinals need a weaker inverse law and belong in a successor ASN.

VERDICT: REVISE
