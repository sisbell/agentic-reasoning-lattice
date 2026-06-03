# Review of ASN-0070

I read the full note, checked the F-canonical existence/uniqueness proof (Steps 1–5), the contiguity characterisation, the six worked configurations, the wp analysis, and the fourteen derived lemmas. The mathematics is sound: the case split on `actionPoint(ℓ)` is exhaustive and both inclusions are proved in each case; the consecutive-tumbler characterisation is proved both directions; the worked examples each exercise a distinct property (empty, vacuous-subspace, multiplicity, cross-subspace straddle, interior offset, multi-document) with no fabricated coverage; cross-ASN references are all to foundation ASNs (0034/0036/0043/0047/0053/0058). Edge cases — empty endset, coverage missing the arrangement, vacuous subspace, both-empty document, interior-offset clip, multiplicity — are all handled.

The note is under `review-mode.anti-bloat`. The findings below are accreted-prose consolidations, not correctness defects.

## REVISE

### Issue 1: The "`follow` modifies nothing" assurance is restated in four places

**ASN-0070, Claims table + Derived Properties preamble + F-state Frame + F-persist Frame**: F1 already carries the frame clause `Σ' = Σ`. The same fact is then re-asserted as a standalone claim row — "F-frame | `follow` reads `Σ` and modifies no state component — the frame clause `Σ' = Σ` of F1" — restated again in the preamble ("`follow` is a query; per-lemma Frame slots are omitted unless an across-transition observation is involved"), and again inside F-state ("`follow` itself modifies nothing") and F-persist ("No state modification by `follow` itself").
**Problem**: F-frame's claims-table row adds nothing beyond F1's frame clause; no lemma depends on it. The "modifies nothing" half of the F-state and F-persist Frame slots duplicates a fact the preamble policy already governs — the only informative content in those slots is the across-transition observation (the variation lives in `M(d)`/`Σ.L`, not in anything `follow` writes).
**Required**: Drop the F-frame row (fold into F1's frame). Trim the F-state and F-persist Frame slots to the across-transition observation alone, deleting the redundant "`follow` itself modifies nothing" half that F1 and the preamble already establish.

### Issue 2: F-empty re-derives a fact F-canonical's construction already yields

**ASN-0070, F-empty derivation**: "We argue that no non-empty canonical-form span-set has empty V-restricted denotation: by F-canonical, every component span `σ = (s, δ(c, m_S(d)))` ... has start `s` ... By T12(b) ... `s ∈ ⟦σ⟧` ... so `⟦σ⟧_V` is non-empty ... By contrapositive, empty V-restricted denotation forces the empty span-set."
**Problem**: F-canonical's existence construction (Step 3) over `X = R(d,e)|_S = ∅` produces zero maximal runs, hence `Σ_V^S = ⟨⟩`, and its uniqueness clause makes that the only canonical representative. The standalone contrapositive (start-in-denotation ⇒ non-empty) re-runs reasoning the canonical-form theorem already settles for the empty case.
**Required**: Replace the inline contrapositive with a direct citation of F-canonical at `R(d,e)|_S = ∅` (empty `X` ⇒ unique canonical form `⟨⟩`).

## OUT_OF_SCOPE

None. The second Open Question (BEBE replication / cross-server traversal consistency) is correctly posed as future work rather than claimed here, so it needs no flag.

VERDICT: REVISE
