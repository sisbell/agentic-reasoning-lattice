# Review of ASN-0098

## REVISE

### Issue 1: Defensive prose imagining the case the canonical precondition already excludes

**ASN-0098, Boundary and Width Behaviour (achievability)**: 

> "The action-point identification `k_ℓ = #s` is therefore a *consequence of the construction's specification* (the canonical construction picks ordinal-displacement spans), not a property of arbitrary endset spans — for which no foundation invariant pins the action point to `#s`, and additional preconditions not in force here would be needed."

and, a few lines later:

> "We record both facts here, but they should not be conflated: tightness pins down what is true at `Σ_e`; the half-open exclusion of indices `> m` is what makes future K.α emissions on this chain harmless to the projection."

**Problem**: The achievability analysis is explicitly restricted to canonical spans (`ℓ = δ(n, #s)`). The first passage then spends a sentence on what *would* fail for "arbitrary endset spans" — a case the canonical hypothesis already removes. The second passage is non-conflation narration carrying a forward pointer to LP19 ("the structural fact LP19 will exploit downstream"). Neither advances the achievability argument; both are scaffolding the precise reader must skip past.

**Required**: Delete the arbitrary-span counterfactual (the canonical hypothesis already settles `actionPoint(ℓ) = #s` via OrdinalDisplacement — state that and stop). Drop the "should not be conflated" paragraph; LP19 can cite the half-open exclusion at its own use-site without a pre-announcement here.

### Issue 2: "Scope restriction" essay embedded inside LP12b

**ASN-0098, LP12b**: 

> "*Scope restriction — link-canonical companion case is OUT_OF_SCOPE.* LP12b addresses only the **content-canonical** class of links ... The symmetric **link-canonical** class ... is out of scope: LP-Fin Corollary at `X = s_L` gives an F-interval whose candidates all carry `s_L`, which by L0 is *not* disjoint from `dom(L)`, so the content-canonical disjointness closure inverts and does not extend. Characterising the wp's value there is left to future work."

**Problem**: This is a labeled "Scope" sub-paragraph sitting inside a lemma proof, explaining what the lemma does *not* cover and sketching why the symmetric argument inverts. The lemma's own statement already names its hypothesis (content-canonical spans). The companion-class question belongs in Open Questions, not as a mid-proof excursion. This is the exact accretion pattern the anti-bloat classifier targets — a scope/rationale block grown around a claim.

**Required**: Remove the sub-paragraph from LP12b's proof. If the link-canonical gap is worth recording, add one line to Open Questions ("the wp on a link-canonical retention pattern with `n'_{s_C}=0` is uncharacterised because LP-Fin Corollary at `X=s_L` does not yield `dom(L)`-disjointness").

### Issue 3: Split boundary-case discussion with document-ordering justification

**ASN-0098, LP12a (second boundary case)**: 

> "The argument requires structural machinery (the set `F` of substrate-emittable addresses and its interval characterisation via LP-Fin Corollary) developed in the 'Boundary and Width Behaviour' section below; we defer the derivation to LP12b — ContentCanonicalLinkSubspaceWPFalse."

**Problem**: The second boundary case is stated in LP12a, then immediately deferred to LP12b, with prose justifying *why* it is placed elsewhere ("requires structural machinery ... developed below"). The case is thereby split across two sections with an explicit ordering apology in between. A reader following LP12a's wp must hold an unfinished sub-claim until a later section. Either the case is part of LP12a (state and prove it where the machinery lives) or it is LP12b's (state it only there).

**Required**: Drop the deferral paragraph from LP12a. Let LP12a present its proven content (the general wp and the `R = ∅` case). State the content-subspace-empty/link-retained boundary result once, in LP12b, where `F` and LP-Fin Corollary are in hand.

### Issue 4: Redundant K.δ routing remark

**ASN-0098, LP8 (Remark on K.δ)**: The "Remark on K.δ" re-walks the K.δ case split (IsNode/IsAccount → LP4, IsDocument → LP8) immediately after LP8's hypothesis already states it "explicitly admits both K.σ and K.δ-IsDocument as document-registration operations."

**Problem**: This is a use-routing inventory restating, in different words, the case decomposition LP8's own hypothesis fixes. The only non-redundant content is the Node/Account → LP4 routing, which is a single clause.

**Required**: Compress to one sentence: "K.δ-IsNode and K.δ-IsAccount have frame `M' = M`, so LP4 covers them; K.δ-IsDocument is the document-registration case of LP8." Delete the rest.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery, V-order reflection, cross-document operation comparison

**Why out of scope**: The Open Questions already park these (reverse-discovery primitive, V-order of projected positions, identical-projection conditions across documents). They are genuinely new state/operation territory and correctly left to future ASNs; no action needed.

### Topic 2: Link-canonical wp companion case

**Why out of scope**: Characterising the wp for the link-canonical retention pattern is legitimately future work — the content-canonical disjointness closure does not transfer. The objection in Issue 2 is to its *placement inside a lemma proof*, not to its deferral.

VERDICT: REVISE
