# Review of ASN-0131

## REVISE

### Issue 1: Insert/delete stability imports ASN-0082 primitives without establishing the link-store frame the conclusion depends on

**ASN-0131, "Stability: the answer as the document is edited" (insert/delete paragraph) and RE-EDIT**: "to range over them the analysis widens its vocabulary beyond ASN-0047's atomic transitions to ASN-0082's displacement primitives, taken in their own right, not as K.μ composites. … its effect on the image is read off the displacement directly … and RE tracks the swing by membership, each surfaced endset's spans held fixed (RE-IDENT)."

**Problem**: ASN-0082's `I3`/`D-SHIFT` are defined over the `(C, M)` state model — that ASN has no link store at all (its cited invariants are S/D/T-series; its frames are `I3-C`/`D-I` over content, never over `Σ.L`). The conclusion that RE "tracks [only] the swing by membership" with "spans held fixed" requires the displacement to leave `Σ.L` — hence `addressable(Σ)` and `Avail(Σ)` — fixed (otherwise the answer could move by population change, not image swing) and to preserve L12/coverage (otherwise spans are not fixed). The note states the link-store frame `L' = L` explicitly for *every* ASN-0047 atomic mover (it cites it for K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L, K.α, K.δ, K.ρ) but supplies no such frame for the imported insert/delete — and explicitly disclaims treating them as K.μ composites, which is the very thing that would have carried the frame over. So the `Σ.L`-frame (and `Σ.E`/`Σ.R`-frame) on which RE-EDIT's insert/delete clause rests is asserted nowhere. The standard you hold elsewhere — frame conditions stated, not assumed — is not met here.

**Required**: When lifting I3/D-SHIFT to the full `(C, L, E, M, R)` state, state (or assume explicitly) that these displacement primitives frame `Σ.L`, `Σ.E`, `Σ.R`, so that `addressable`/`Avail` are fixed and only the image swings; or restrict RE-EDIT's insert/delete coverage to a form whose link-store frame is already established.

### Issue 2: Citation-practice promise in the standing-assumption bridge

**ASN-0131, "The unit of the answer: anchoring without names"**: "We invoke each such lemma where it is used."

**Problem**: This sentence advances no reasoning — it is a promise about citation practice appended to the cross-ASN bridge. It is exactly the meta-prose a precise reader must skip past. (The substantive bridge claim — `Σ.L` evolves only through K.λ, so ASN-0086's `Σ.L`-only lemmas hold at populated-arrangement states — should stay; the parenthetical noting ASN-0086's empty-arrangement layer is informative and should stay too.)

**Required**: Delete the sentence.

### Issue 3: Content-identity invariance stated twice, in two sections, in different words

**ASN-0131, "Stability …" opening**: "One invariant underlies this whole section, and we state it once: each surfaced endset's coverage is permanent (RE-IDENT) …"

**Problem**: "we state it once" is inaccurate. The same invariant was already stated in full in the transclusion section: "the content-level answer … is invariant. The endset's coverage is permanent: links are immutable (L12) … no transition alters an endset's coverage (LP3) … arrangement-independent even though its selection … is arrangement-mediated." RE-IDENT is a general coverage-permanence property, not a consequence of transclusion; deriving it as a "delicate consequence" of transclusion and then restating it to govern stability duplicates the content across sections. The same pattern recurs for RE-WHOLE, whose "convention-not-forced-by-RE-CLIP; touching-spans-only would satisfy RE-CLIP while violating RE-WHOLE; provisional pending OQ1" qualification is stated in full in the Extent section and again in full in the claims-table entry.

**Required**: State RE-IDENT once at its natural (general) site and cite it from both the transclusion and stability sections; carry each claim's provisionality/convention status once (derivation site), not re-stated in full in the claims table.

## OUT_OF_SCOPE

(none — the note's deferrals are already routed to Open Questions: intersection-distributivity, V-order rendering, link-subspace regions, non-co-resident stores, type-slot/content match, multiplicity preservation. The mentions of FINDLINKSFROMTOTHREE / FINDNUMOFLINKSFROMTOTHREE are contrasts, not claims, so nothing to flag there.)

VERDICT: REVISE
