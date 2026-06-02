# Review of ASN-0098

## REVISE

### Issue 1: Non-canonical infinitude material proves properties no claim consumes
**ASN-0098, "Boundary and Width Behaviour"**: The `tight` predicate is *defined* to require canonical form (`ℓ = δ(n, #s)`), so a non-canonical span is "rejected at the type level and fixed at false before any quantifier evaluation." Yet the note then spends a full parametric within-chain construction, a "Concrete witness" paragraph with explicit tumblers, and a sub-range taxonomy to prove `|F ∩ [s, s ⊕ ℓ)| = ℵ₀` for the `#ℓ < #s` and non-ordinal `#ℓ = #s` cases — and a further paragraph admitting "The remaining sub-range, (iii) `#ℓ > #s`, is genuinely unsettled by this ASN... The tightness predicate's purposes do not require an answer."
**Problem**: Non-canonical spans are never tight, so their F-intersection cardinality is irrelevant to every claim (LP-Fin, LP-Fin Corollary, LP12b, LP19/LP19a all run on canonical spans only). This is motivation prose — "why the canonical restriction exists" — dressed as a proof. The reader must work through an entire infinitude argument for objects the claims never touch.
**Required**: Compress to one sentence: non-canonical spans are excluded by the canonical-form requirement; the canonical restriction is what makes LP-Fin's quantifier finite/decidable. Drop the parametric construction, the concrete witness, and the (iii) discussion.

### Issue 2: Working-reference-frame paragraph is a use-site inventory
**ASN-0098, "Working reference frame"**: "The extended-state invariants this ASN consumes — S3★ (GeneralizedReferentialIntegrity), S3★-aux (SubspaceExhaustiveness), and the per-subspace amendments D-CTG★, D-MIN★, D-SEQ★ — are cited at the proof steps that use them."
**Problem**: Enumerating consumed invariants and announcing they will be "cited at the proof steps that use them" is meta-prose about the document's own citation practice. It advances no reasoning; the citations at the use-sites already carry the information.
**Required**: Delete the sentence. Keep the one-line frame statement (layered ASN-0047 / ASN-0093) and let the proof steps cite their invariants where used.

### Issue 3: Dual deferral to LP19 for the same point
**ASN-0098, LP6 and LP9**: LP6 — "turns on the endset's construction discipline, settled by LP19/LP19a below: under tight construction it cannot." LP9 — "whether the projection grows depends on the endset's construction discipline; the tight case is settled by LP19 below."
**Problem**: Two paragraphs in different sections defer the same conclusion (tight construction blocks boundary growth) to the same downstream location. This is the "multiple paragraphs defer to the same downstream location" accretion pattern.
**Required**: State the deferral once (at LP6, where the boundary-insertion question first arises) and let LP9 carry only its local growth characterization without re-pointing forward.

### Issue 4: LP12b scope-restriction note over-elaborated
**ASN-0098, LP12b, "Scope restriction"**: The link-canonical OUT_OF_SCOPE note runs a full structural inversion argument (LP-Fin Corollary at `X = s_L`, L0/L4(c) appeals, the "argument inverts" elaboration) to justify a deferral.
**Problem**: A scope note's job is to mark what is not covered and why the present proof does not reach it. The one load-bearing fact is that LP-Fin Corollary at `X = s_L` makes the F-interval *non-disjoint* from `dom(L)`, so the content-canonical closure inverts. The surrounding elaboration restates this at essay length.
**Required**: Reduce to the single inversion fact plus the deferral; drop the repeated framing.

## OUT_OF_SCOPE

The ASN's own deferrals — the link-canonical wp class (LP12b), reverse-discovery, V-order reflection, cross-document operation comparability (Open Questions) — are correctly scoped as future ASNs, not defects here. No additional out-of-scope coverage is missing.

VERDICT: REVISE
