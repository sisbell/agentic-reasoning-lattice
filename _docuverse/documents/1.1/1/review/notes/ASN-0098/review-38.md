# Review of ASN-0098

This note carries the `review-mode.anti-bloat` classifier. The mathematics is meticulous and the operation/boundary coverage is genuinely thorough (empty arrangement, empty retention, empty endset, orphan/resurrection all handled). My findings are concentrated where prior cycles have accreted meta-prose, forward-reference scaffolding, and duplicated justification around the tightness/canonical machinery.

## REVISE

### Issue 1: Boundary-insertion exclusion explained three times before LP19 states it
**ASN-0098, LP6 / LP9 / "Boundary and Width Behaviour"**: LP6 says "under tight construction the new I-address lies outside `coverage(e)` (LP19a below formalises this freshness claim)... Without tightness, the new I-address could fall within a half-open coverage interval reaching past existing content". LP9 repeats nearly verbatim: "the newly allocated I-address lies outside coverage, and the projection does not grow... Without tightness, the new I-address could fall within a half-open coverage interval reaching past existing content, in which case the projection grows by that V-position." The tight section then states it a third time as LP19/LP19a.
**Problem**: The same claim, with the same "without tightness" hedge and the same forward pointer to LP19, is delivered three times before the lemma that actually proves it. Two of the three are forward-reference advertisements, not reasoning steps.
**Required**: State the tightness consequence once, at LP19/LP19a where it is proved. In LP6 and LP9, cite LP19 in a clause without re-explaining the without-tightness counterfactual.

### Issue 2: "Working reference frame" paragraph is a use-site inventory
**ASN-0098, State Components, "Working reference frame"**: "The layered frame supplies the full operation vocabulary... together with the extended-state invariants S3★ (GeneralizedReferentialIntegrity), S3★-aux (SubspaceExhaustiveness), CL-OWN, CL-UNIQ, and the per-subspace amendments D-CTG★, D-MIN★, D-SEQ★. The projection function defined in the next section consults only `coverage(e)` and `Σ.M(d)`; whenever an operation's frame holds `Σ.M(d)` constant, projection invariance follows by LP4."
**Problem**: CL-OWN and CL-UNIQ are listed but never used in any proof in this ASN — a pure inventory. The final sentence pre-announces LP4's content before LP4 is stated. The whole paragraph advances no reasoning; it catalogues foundations and forward-references a lemma.
**Required**: Drop the unused-invariant inventory; cite each foundation invariant at the one site that consumes it. Remove the LP4 pre-announcement.

### Issue 3: Document-structure meta-paragraph
**ASN-0098, end of "Operation Effects on Projection"**: "We make no separate claim about the *cumulative* behaviour of mixed-kind chains: the multi-step results of this ASN — LP18 (resurrection) and LP19 (tight boundary exclusion across `Σ_e →* Σ_n`) — are stated and proved as self-contained results that consume state-invariant facts and per-step lemmas as their proofs require."
**Problem**: This describes the ASN's own claim-structure and what it declines to claim, rather than advancing any guarantee. It is defensive scaffolding about how the document is organized.
**Required**: Delete. The per-step lemmas and the self-contained multi-step results stand on their own; LP18/LP19 declare their own hypotheses.

### Issue 4: Repeated "load-bearing" justification of the canonical restriction
**ASN-0098, "Boundary and Width Behaviour"**: The canonical restriction is argued to be load-bearing at least three times — "The canonical restriction is therefore load-bearing both for LP-Fin and for the well-definedness of the tightness predicate"; "The canonical assumption `ℓ = δ(n, #s)` is therefore load-bearing for LP-Fin's finitude conclusion"; and again "the canonical restriction is structurally necessary for predicate decidability."
**Problem**: Three separate paragraphs assert the same necessity claim in different words. One demonstration (the within-chain infinite-intersection construction) settles it; the surrounding "load-bearing" restatements are commentary.
**Required**: Keep the one constructive demonstration that non-canonical spans force `|F ∩ [s, s⊕ℓ)| = ℵ₀`; remove the repeated "load-bearing"/"structurally necessary" glosses.

### Issue 5: Non-canonical non-tightness proven across three overlapping blocks
**ASN-0098, "Boundary and Width Behaviour"**: The same content appears in (a) the "*Non-canonical spans yield infinite intersections*" block, (b) the "within-chain construction extends to this case" block for `#ℓ = #s` non-ordinal, and (c) the "*Non-canonical spans are unconditionally non-tight*" grounds (i)/(ii)/(iii) block. All three exhibit the chain `A_X(d_0)` supplying infinitely many in-interval F-candidates and conclude non-tightness.
**Problem**: Three passes over one result. Grounds (i)/(ii) in block (c) restate the constructions of blocks (a)/(b); the prose "finitude itself fails on those sub-ranges" duplicates what (a)/(b) just established.
**Required**: Prove the within-chain infinite-intersection construction once (parametric in `actionPoint(ℓ)`, covering both `#ℓ < #s` and `#ℓ = #s` non-ordinal), then have the tightness predicate cite it. Replace grounds (i)/(ii) with a one-line cite and keep only ground (iii)'s distinct point (definitional rejection of `#ℓ > #s`).

### Issue 6: LP20 trailing paragraph restates the per-subspace citations it just used
**ASN-0098, LP20**: After the per-subspace inclusions are derived inline with S3★-aux and S3★ cited at the step, a following paragraph re-explains: "The corollary's per-subspace argument draws two facts from ASN-0047. S3★-aux (SubspaceExhaustiveness) discharges exhaustiveness... S3★ (GeneralizedReferentialIntegrity) supplies the per-subspace targets..."
**Problem**: This paragraph re-narrates citations already discharged in the proof immediately above — two passages saying the same thing.
**Required**: Delete the trailing recap; the inline citations already name S3★-aux and S3★ at their use sites.

### Issue 7: "Remark on K.δ" closes with an exhaustiveness flourish
**ASN-0098, LP8, "Remark on K.δ"**: The remark legitimately covers the IsNode/IsAccount/IsDocument cases, but ends "Each K.δ kind therefore reduces to either LP4 or LP8, and no separate displacement claim is required."
**Problem**: The case coverage is wanted; the closing "no separate displacement claim is required" is a defensive exhaustiveness assertion that adds nothing to the reduction already shown.
**Required**: Keep the case reduction; drop the trailing "no separate displacement claim is required" sentence.

## OUT_OF_SCOPE

### The link-canonical companion case (LP12b scope note)
The ASN already marks the symmetric link-canonical wp class as out of scope with a correct structural reason (LP-Fin Corollary at `X = s_L` gives an interval that intersects `dom(L)`, so the content-canonical argument inverts). This is properly scoped — no change needed, noted here only to confirm it is not a missing-coverage defect.

VERDICT: REVISE
