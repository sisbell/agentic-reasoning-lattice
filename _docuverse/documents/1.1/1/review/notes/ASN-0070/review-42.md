# Review of ASN-0070

I read the note in full, checked every introduced claim's proof against its stated dependencies, walked the edge cases (empty endset, empty document, vacuous subspace, fully-contracted arrangement, cross-subspace straddle, multiplicity), and applied the forward-reference accretion lens. My findings below.

## REVISE

None rises to a required revision. Details:

**Proof completeness.** The heavy proof — F-canonical — is genuinely worked, not hand-waved. Step 1's case split (`1 ≤ k < m_S(d)` excluded by infinitude of `⟦σ⟧_V`; `k = m_S(d)` shown by *both* inclusions) is exhaustive via the ActionPoint bound, and the consecutivity Characterisation's reverse direction is carried by an explicit induction with all four `(q,q')` sub-cases discharged (T1 + NAT-order irreflexivity + discreteness), not "by symmetry." Step 2a separately discharges *existence* (the per-run construction with N1/N2 verified) before uniqueness — both halves of the theorem are present.

**Edge cases.** Empty resolution (F-empty) is proven denotationally *and* representationally, with the non-empty-component contrapositive (T12(b) start-membership) closing the canonical-form claim. The vacuous-subspace convention closes uniqueness when `m_S(d)` is undefined. Multiplicity (F-multi) separates the implication from the structural admissibility (reachability via K.μ⁺'s lack of a content-subspace injectivity constraint, contrasted with CL-UNIQ). F-sound/F-complete correctly decompose the postcondition's set-equality into its two inclusions.

**Symmetric cases** (F-subspace `s_L` branch; F-multi `v₂`) name both directions' premises rather than asserting "similarly" — adequate.

**Anti-bloat.** I looked specifically for defensive justifications, exhaustiveness padding, use-site inventories, and duplicated paragraphs. The candidates I found (F-det re-narrating S3★-aux exhaustiveness already stated in F0's partition clause; the F-det Depends parenthetical "F0 ... which itself rests on S2"; the "k > m_S(d) cannot arise" tag) are each a single clause that remains load-bearing within its local proof step. None forces a reader to skip past meta-prose to follow a claim. The five worked configurations each exercise a *distinct* property (sound/complete, multi, empty, state/persist, cross-subspace straddle) — not redundant. The Discussion's Nelson readings are system-guarantee statements/analogies, which the standards explicitly exempt.

**Foundation discipline (Standard 7).** Every numbered reference in the body is to ASN-0034/0036/0043/0047/0053/0058 — all foundations. No non-foundation cross-reference, no reinvented foundation notation.

## OUT_OF_SCOPE

### Topic 1: Multi-home resolution relationships, concurrency semantics, transclusion-lineage correspondence
**Why out of scope**: These are the note's own Open Questions, correctly left as future ASNs rather than claimed here. They are not defects in this note.

VERDICT: CONVERGED
