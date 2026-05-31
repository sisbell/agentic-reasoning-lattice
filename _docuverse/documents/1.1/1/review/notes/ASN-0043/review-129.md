# Review of ASN-0043

I read the full note, verified the load-bearing proofs (CPP, the L1c chain and its `s = home(a)` derivation, the L11a single-tree discharge, and all six worked-example steps), and checked the invariant conjuncts. The mathematics is sound — the coverage arithmetic in Steps 5–6, the forced-edge argument for the shared-home case, and the CPP induction all hold. My findings are confined to the meta-prose accretion the `anti-bloat` classifier asks me to surface; I found no substantiable correctness gap.

## REVISE

### Issue 1: Disjointness conclusion is stated in L0a but its derivation deferred forward, with document-ordering prose
**ASN-0043, L0a (ContentSubspaceScope)**: "The disjointness this ASN derives is: `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅` ... The derivation of this disjointness rests on two link-allocation invariants developed below — L1 ... and L1c ... — and is given as L0b, after L1c."
**Problem**: This is the flagged "prose justifies document ordering" + "defer to a downstream location" pattern. L0a's job is to define the `s_C`-resident slice and the `s_C`-resident predicate; it instead also states the disjointness *result* and then spends a sentence explaining that the proof lives later (L0b) because of what L1/L1c supply. The same forward dependency on L1c is announced a third time in the "Definition — home" block ("T4-validity from L1c's chain ... below"). A precise reader must hold the unproven conclusion and the ordering rationale across three intervening pages until L0b discharges it. The deferral is structural, not informational.
**Required**: Let L0a define only the slice and the `s_C`-resident predicate. Move the disjointness statement to L0b where it is actually proved, and drop the "rests on … developed below … given as L0b, after L1c" sentence (the dependency is evident from L0b's own citations).

### Issue 2: L11a announces its proof plan twice
**ASN-0043, L11a (LinkUniqueness)**: Para 1 — "We discharge this by exhibiting one global tree 𝒯 of which every link chain is a subtree." Para 2 — "What L1c supplies, however, is only the *existence* of some conforming chain per link; GlobalUniqueness needs the stronger fact that `a₁` and `a₂` are genuine allocation events of the *one* tree 𝒯 ..."
**Problem**: Two paragraphs in the same section state the same roadmap point in different words — that L1c gives per-link existence, and the missing piece is single-tree membership for GlobalUniqueness. This is the flagged "two paragraphs say the same thing in different words" pattern. The object-level argument (distinct-homes case, shared-home forced-edge case) is what carries the proof; the doubled framing is scaffolding the reader skips.
**Required**: Keep one statement of the gap (the L1c-existence-vs-single-system observation immediately before the two-case split) and delete the redundant framing sentence in para 1.

## OUT_OF_SCOPE

None beyond what the note's own Open Questions already capture (global content-subspace constant, transclusion/link-store interaction, compound-link well-formedness). Those are correctly deferred, not errors here.

VERDICT: REVISE
