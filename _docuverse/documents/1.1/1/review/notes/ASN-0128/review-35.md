# Review of ASN-0128

This pass checked every proof obligation in the note rather than sampling. The deep checks and their outcomes:

- **I0/I0a.** The single-span coverage-identity argument is complete: equal half-open intervals force equal starts (T1-least) and equal endpoints (the lesser endpoint would separate the intervals), and TA-LC's preconditions are discharged from T12 well-formedness. I0a's both-direction proof of minimal-elements identity is sound, including the `r'' ≼ t ≺ r ⟹ r'' ≺ r` length step. The case closure for rejecting the finer criterion covers all three slots, and the conclusion is correctly scoped to argument-blindness rather than invisibility.
- **I1a.** The induction covers all step kinds, including the two subtle ones: non-K deposits that shrink `A_K` by nullification, and the K ~ R wrapper-routed instantiation where the deposit may shrink *another* class. The born-nullified deposit case (zero rather than one new active member) is handled.
- **I6.** The wp's necessity argument is correct per route — the attainability convention genuinely is load-bearing (gate-first rejection with a standing I0-equal incumbent), and the admitted-miss-failing-C3 case genuinely falsifies POST at the returned address because the fresh address holds only the born-nullified deposit. Sufficiency per branch checks out; C2 absorption into `pre` is right since `K ≁ R` is a uniform precondition. The idem-⊥ corollary correctly notes POST never consults duplicates at other addresses.
- **DR.** The proof is sound: both P-tgt branches place the target in the link domain by the depositing step's post-state, L12a carries residence forward, distinctness comes from freshness vs. residence at Θ, and the antichain step correctly routes through the post-state Θ' (reachable regardless of C3, via RP-c) to instantiate R0a. The necessity analysis honestly handles the case where rejection leaves the postcondition *true* (P0 failure against a resident target), which is exactly where the convention earns its keep. The off-discipline counterexamples — range-G sterilization and the unit-depth ghost-target bypass that silently no-ops a later self-emit — are precise witnesses that the SD qualifier on sufficiency cannot be dropped.
- **Wrapper hit branch.** Residence (self-emit cannot hit under SD: the match's root was P-tgt-valid at its own emit, hence resident, while the self-emit candidate is fresh), nullification (R6b's three hypotheses assembled at the unchanged state), single-tuple scope (R0a), and persistence are each re-established from the pre-existing tuple, not hand-waved from the absent step.
- **BH4.** Age totality and single-valuedness via L-ContiguousPrefix and strict T1-ascent; `age ≥ 0` from `j ≤ J_d`; the batch net postcondition's per-constituent case split (admitted miss under enforced P-tgt; hit already-nullified via R6b with residence by L12a) plus R6a persistence to `Σ_fin` is a complete argument, and the same-document/different-document/nullified-prior-retraction trichotomy for re-retraction is correctly *not* collapsed into blanket dedup.
- **BH2.** Termination bound is genuine (targets lie in the finite vertex set, pairwise distinct); the self-loop and 2-cycle cases fall under "unique successor already occurs in the sequence" since `x₀` is in the distinctness scope; the non-denoting-G tuple yields no edge, consistently giving `succs = ∅` while `target_of` returns ⊥ — different questions, no contradiction.
- **Bridge discipline.** Every RP cite I checked is correctly scoped: single-state claims through RP-a (FrontierUnification at I2, R0a, L-ContiguousPrefix, P6), successor- or step-quantified claims through RP-b (RangeSterilization — which I2 explicitly routes through RP-b, not RP-a — R6a/R6c, L12/L12a, `dom(Σ.M)` monotonicity), step existence through RP-c (I6's miss, DR's antichain step).
- **Examples and boundaries.** The abstract registry example exercises hit-with-differing-decomposition, born-nullified, branch verdicts, and view-selector behavior against the spec text, and each checks out. Empty-F emits are gate-rejected at every shape (`|F| = 1`); Multi admits `G = ∅` harmlessly; D3's `targets_under` equality at F-denoting states verifies by unfolding both sides.
- **Anti-bloat scan.** I looked specifically for the forward-reference accretion patterns. The DR statement/proof split carries one forward pointer and is structurally forced (the proof consumes SD and S3's policy). The remaining candidates — the RP preamble sentence, the operation-set paragraph — each advance a load-bearing claim (state-space change necessitating new transfer clauses; no fourth primitive, `retract_stale` steps extend SD derivations). Nothing rose to relocated-finding residue or duplicated prose.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: BH1 dominance over behavior-unlocked surfaces
**Why out of scope**: The note pins the active-view semantics completely and its Open Question 1 correctly identifies that the BH1 × BH2 case is the canonical lifecycle scenario (`retired` and `supersedes` both ship). Either dominance choice changes no committed claim here; it is a successor's decision, not a gap in this note's contracts.

### Topic 2: Multi-app registry composition and collision resolution
**Why out of scope**: C0/R-C1 state the constraint (key uniqueness, failing construction on collision) and R-VAL makes it decidable; the merge *protocol* among several apps sharing one substrate is new machinery, properly deferred (Open Question 8).

### Topic 3: Audit-view chain walking
**Why out of scope**: BH2's active-view commitment is internally complete (a nullified mid-chain tuple is honestly a sink); whether historical-chain recovery is a substrate obligation or an app-side reconstruction over `Observe_K(…, hist)` is genuinely new surface, not an error here (Open Question 6).

VERDICT: CONVERGED
