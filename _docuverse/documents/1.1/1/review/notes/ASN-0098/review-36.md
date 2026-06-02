# Review of ASN-0098

## REVISE

### Issue 1: Fabricated citation and incorrect depth claim in LP9
**ASN-0098, LP9 (K.μ⁺_L constraints)**: "(b) the new V-position has fixed depth `m_L = 2` (LinkVPositionDepthAxiom of ASN-0047)"
**Problem**: Two errors. (i) ASN-0047 contains no claim named `LinkVPositionDepthAxiom`. (ii) The depth is not fixed at 2. ASN-0047's K.μ⁺_L states that when `V_{s_L}(d) = ∅`, `ValidFirstLinkPosition(d, v_ℓ, m)` holds "for any chosen `m ≥ 2`", and when non-empty, `#v_ℓ = m_L(d)`; ASN-0047's `m_L(d)` definition explicitly says the depth "re-pins from scratch at any value `≥ 2`." A reader building on "link V-positions always have depth 2" would be misled.
**Required**: Remove the fabricated axiom name; state the depth as `m_L(d) ≥ 2` (chosen, not fixed), or drop the parenthetical entirely since LP9's proof consumes only (E1)/(E2) and does not need the depth at all.

### Issue 2: Fabricated citation `ChainUniformLength` (ASN-0093)
**ASN-0098, A Worked Trace**: "all four share the common chain length `#d_alloc + 3` (ChainUniformLength, ASN-0093)"
**Problem**: ASN-0093 has no claim named `ChainUniformLength`. The uniform-length fact must be derived from `FirstEmission` (`#E = 2`) plus `ChainDiscipline` (`inc(·, 0)`) with TA5(c) length preservation.
**Required**: Cite the actual supporting lemmas, or introduce the derivation explicitly.

### Issue 3: Fabricated namespacing `SubAllocatorAxiom.*` in LP12b
**ASN-0098, LP12b**: "by SubAllocatorAxiom.FirstEmission and SubAllocatorAxiom.ChainDiscipline (ASN-0093)" … "by SubAllocatorAxiom's restriction that sub-allocator chains are activated only at document-level tumblers"
**Problem**: ASN-0093 exposes `FirstEmission` and `ChainDiscipline` as standalone lemmas; there is no axiom or container named `SubAllocatorAxiom` in ASN-0093. The phrase "SubAllocatorAxiom's restriction … activation discipline" cites nothing concrete. (The worked trace repeats this with "SubAllocatorAxiom.ChainDiscipline (ASN-0093)".)
**Required**: Cite the real lemma names. For the activation/document-level requirement, cite the actual premises (`ChainMembershipForOrigin` + `L1a` + `M0`).

### Issue 4: Verbatim duplicated conclusion across LP12a and LP12b
**ASN-0098, LP12a (Second boundary case) and LP12b (final sentence)**: "The case exhibits the wp's *per-subspace sensitivity*: the retention set's subspace partition — not merely its total cardinality — determines whether the wp is satisfiable for a given link."
**Problem**: This sentence appears identically in two sections. Two paragraphs saying the same thing in the same words is the duplication pattern flagged for this note.
**Required**: Keep it at the discharge site (LP12b); delete the copy in LP12a's deferred boundary-case paragraph.

### Issue 5: Forward-reference accretion in "Working reference frame"
**ASN-0098, State Components, "Working reference frame"**: "Three claims require the link-subspace machinery and do not survive descent to the ASN-0036 base frame intact: LP9's K.μ⁺_L sub-case … LP12b … LP20's per-subspace corollary refinement …"
**Problem**: This is a downstream-consumer inventory plus a hypothetical frame-descent caveat. The ASN operates in the stated ASN-0047 + ASN-0093 frame; cataloguing which three claims would behave differently in an unused base frame does not advance any argument and forces the reader past meta-prose to reach the working definition.
**Required**: Cut the frame-descent inventory; state the operating frame and the operation/invariant vocabulary in use, nothing more.

### Issue 6: LP-Comp is a use-site inventory, not a claim
**ASN-0098, LP-Comp**: "Every atomic transition … is governed by exactly one of them: K.σ and K.δ-IsDocument by LP8; K.δ-IsNode and K.δ-IsAccount by LP4 … LP-Comp is the assertion that no such lemma is missing."
**Problem**: This is a prose table-of-contents (operation → lemma) plus an exhaustiveness assertion, self-described as "a documentation note, not a load-bearing lemma." It does not advance reasoning, and its prior load-bearing induction is admitted to have been "sketched rather than carried out." Use-site inventories and exhaustiveness claims in a claims slot are the accretion pattern flagged for this note.
**Required**: Remove LP-Comp from the claims sequence/table. If a one-line statement that LP4–LP14 cover all operation kinds is genuinely needed, fold it into prose without the per-operation roster.

### Issue 7: Defensive justification + retained redundant sub-cases in achievability
**ASN-0098, "Relationship to LP-Fin Corollary" and LP19-Achiev-CrossSub-C/L, -NonNest, -Desc, -Anc**: "are direct consequences of LP-Fin Corollary, which already establishes … We retain the per-case verification under individual sub-labels for two reasons. First, motivational clarity … Second, …"
**Problem**: The five LP19-Achiev sub-cases are admitted to be subsumed by the already-proved LP-Fin Corollary; the cross-chain-exclusion content is redundant. The two-reason paragraph is a defensive justification for keeping redundant content rather than reasoning. (The emission-frontier argument is genuinely additional and should stay; the per-family T1-divergence re-proofs are the redundancy.)
**Required**: Delete the redundant cross-chain sub-proofs (cite LP-Fin Corollary for cross-chain exclusion) and the two-reason defense; retain only the emission-frontier argument that carries content beyond the corollary.

### Issue 8: Numbering note is a revision-history essay
**ASN-0098, "Numbering note"**: multi-paragraph narrative — "LP-Comp … is recast in this revision from a load-bearing composite-displacement lemma to a documentation note … LP12b is introduced in this revision to give the deferred discharge … a tracked label … this revision restricts LP-Fin to canonical spans …"
**Problem**: A brief note on which labels are absent is fine; the bulk here explains *why* claims were recast/introduced/restricted across revisions rather than what they currently say. This is revision-rationale essay content that will rot as the ASN evolves.
**Required**: Reduce to the absent-label facts (LP1, LP15 unused; LP14 reclaimed). Move recast/restriction rationale out of the specification.

### Issue 9: Triangular deferral to the same downstream discharge
**ASN-0098, LP12a / LP-Fin Corollary / LP12b**: LP12a's second boundary case "defer[s] the derivation to LP12b … in that section"; LP-Fin Corollary says it "discharges LP12a's second boundary case … the discharge is stated as LP12b immediately below"; LP12b opens "We discharge LP12a's second boundary case (deferred from … above)."
**Problem**: Three paragraphs in three sections all point at the same discharge, restating the deferral relationship each time. This is the "multiple paragraphs defer to the same downstream location" accretion pattern.
**Required**: Keep one forward pointer (from LP12a to LP12b) and let LP12b stand on its own; drop the corollary's redundant "discharge stated below" sentence and LP12b's "deferred from above" preamble.

## OUT_OF_SCOPE

### Topic 1: Weakest precondition for the link-canonical retention class
**Why out of scope**: LP12b correctly scopes itself to content-canonical links and flags the symmetric link-canonical class (`s = [d_s, 0, s_L, k_s]` under `n'_{s_C}=0, n'_{s_L}>0`) as future work, noting LP-Fin Corollary at `X = s_L` places coverage F-candidates inside `dom(L)`, so the wp may be satisfiable. This is correctly deferred, not an error in this ASN.

### Topic 2: Finitude of `|F ∩ [s, s ⊕ ℓ)|` for `#ℓ > #s`
**Why out of scope**: The tightness predicate rejects all non-canonical spans definitionally before evaluating the quantifier, so the `#ℓ > #s` finitude question genuinely does not bear on any claim. Correctly left unsettled.

VERDICT: REVISE
