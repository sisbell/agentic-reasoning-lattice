# Review of ASN-0128

I checked every contract clause and proof in this note against the three foundations: the I0 single-span identity argument (T1-least start, endpoint separation, displacement recovery through TumblerAdd), both directions of I0a's minimal-elements proof, the I1a induction (all four step kinds, including the K ~ R wrapper-routed case and born-nullified deposits), the I6 wp assembly (necessity and sufficiency per branch, C2 absorption, the idem-⊥ corollary), DR's main derivation (freshness/distinctness/antichain chain, both P-tgt branches, the hit branch's four re-established guarantees, and the necessity argument under the attainability convention), the transfer machinery (RP-a/b/c routing, including the correct B2-then-RP-a composition for ASN-0086 results and the correct RP-b routing for successor-quantified results like RangeSterilization), BH2's termination bound and stop-condition coverage (sinks, branches, cycles, self-loops, non-vertex arguments), BH4's totality argument via L-ContiguousPrefix, and `retract_stale`'s admission-persistence and already-retracted case split. The boundary cases I probed — empty G under Multi, ghost-target rejection, self-emit retraction (C2-born-nullified, deliberately), Σ_init.L = ∅ grounding DR's base, content addresses failing P-tgt, dedup against range-F incumbents (excluded by the single-span identity), hit with invalid `d` — are each either covered explicitly or excluded by an argument the note actually gives. The anti-bloat patterns I hunted for (relocated findings, duplicate paragraphs, consumer inventories, ordering justifications) did not materialize as findings: the passages that restate contract structure (the exposed-signature outcome list vs. I6; the view-machinery orientation sentences) each carry distinct load — the signature fixes the type and outcome partition, I6 computes the wp over it — and the evidence citations (Nelson's never-merge, Gregory's validate-where-read, the timestamp absence grounding ordinal age) anchor design choices rather than defend them.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Batch-level postcondition for `retract_stale`
**Why out of scope**: BH4 fixes per-constituent admission, persistence of P0/P-tgt across interleaving, and harmlessness of redundant constituents, from which "every address stale at batch entry is nullified at batch completion" follows — but the completion-level contract and its statement as a compound-operation guarantee under arbitrary interference is new machinery (compound/transactional operations), not an error in this note's per-step semantics.

### Topic 2: Surface-level irredundancy enforcement
**Why out of scope**: I1 honestly documents that a hit can suppress a redundant presentation's decomposition and names the mitigation (coverage-irredundant address lists, where I0a makes denoted-set and coverage equality coincide). Promoting that mitigation to a checked precondition — rejecting presentations where one listed address extends another — would be a gate/surface refinement in the spirit of the note's own Open Question 3, not a fix to the committed semantics.

### Topic 3: Surfacing off-surface edges to the walk predicates
**Why out of scope**: AD's omission rule means a raw deposit with a non-unit-depth G makes its source a sink on the denoted graph, so `tip` can report a head while an off-surface assertion points beyond it. The note commits this verdict deliberately (such tuples are reachable only outside the operation surface). Whether BH2 should additionally signal "non-denoting out-edges present" — a fourth verdict alongside sink/branch/cycle — is new territory adjacent to the note's Open Question 6.

### Topic 4: BH1 dominance over behavior-unlocked surfaces
**Why out of scope**: The note's Open Question 1 correctly classifies this — the committed rewrite scope (`members`, `targets_of` only) is pinned and internally consistent; extending or refusing filtering on `sources_to` and the walk is a genuine successor decision, with the shipped `retired` × `supersedes` interaction as its forcing case.

VERDICT: CONVERGED
