# Review of ASN-0128

This is a verification pass over the full note: the registration-record extension and its transfer machinery (RP, RP-a/b/c), the idem contract chain (I0–I6), the behavior catalog, the default predicates, and the standard registrations with the DR proof. I checked every proof obligation I could discharge against the foundation claims. Findings below.

**What was checked and held:**

- **I0's case analysis** is complete. The single-span identity argument (equal coverage → equal start as T1-least element → equal endpoint by total-order separation → equal displacement by TA-LC, with T12 well-formedness discharging TA-LC's preconditions) is correct, and the case split over slots (F by P6's `|F| = 1` via RP-a; Unary/Binary G vacuously or by the same identity; Multi G read only in result position) covers every slot. The gate-first ordering in I1 correctly prevents the one leak (a two-span presented F coverage-equal to a stored single span) from reaching the dedup check.
- **I0a's** mutual-inclusion proof for minimal-elements identity is complete in both directions, and the separating pair correctly witnesses strictness of the rejected refinement.
- **I1a's induction** is sound: the miss-only deposit discipline gives at-most-one per class at the deposit's own class; non-K and K~R deposits only shrink other classes (nullification is monotone); immutability via L12/B2/RP-b rules out post-hoc class change; the born-nullified and self-emit corner cases are both absorbed by "at most one."
- **I6's wp** is correct under the attainability convention, including the subtle necessity split (rejection falsifies by convention since POST is parameterized by a returned address that doesn't exist; an admitted C3-failing miss falsifies POST genuinely via SliceUniqueness at the fresh address). C2's absorption into `pre` through the `K ≁ R` clause is right, and the idem-⊥ corollary follows by `hit ≡ ⊥` substitution.
- **DR's proof** is the strongest piece: monotonicity places every disciplined retraction target in the link domain at every later state, distinctness comes from freshness of `a_emit`, and the antichain instantiation of R0a at the post-state (which exists because C3 gates landing, not stepping) closes `¬(a ≼ f)`. The hit branch's Residence bullet correctly rules out a self-emit hit under SD, and the off-discipline unit-depth bypass counterexample (silent no-op with `{t : a ≼ t} ∩ A_rel^{Σ'} = ∅`) genuinely witnesses that the SD qualifier on sufficiency cannot be dropped — including the observation that no extension of an unallocated chain slot can be a link address, since all deposits land at depth-2 chain frontiers.
- **BH2's termination bound** (distinct extensions drawn from the finite vertex set), the self-loop and branch verdicts, and the S2 slot convention's consistency with the walk direction all check out, including the example's `tip(a_v1) = tip(a_v2) = ⊥` at the branch.
- **BH4's net postcondition** for `retract_stale` is correctly derived per constituent: P0 by one-time check plus domain monotonicity, P-tgt's first disjunct by L12a per step, the hit case discharged through R6b's three hypotheses at the unchanged state, and persistence to `Σ_fin` by R6a via B3/RP-b. The same-document-active-tuple case split (hit) versus cross-document or nullified-retractor (redundant but harmless miss) is the right partition.
- **The sterilization containment argument in S3** is correct: the ghost-target call at `d.0.s_L` is rejected by P-tgt (not a link address by L1b, not the frontier), and `nullified` reading only `L_R` plus C0 key uniqueness makes containment complete against app-registered types.
- **Transfer hygiene** is consistently maintained — single-state facts routed through RP-a, successor-quantified ones through RP-b (the RangeSterilization citation in I2 is explicitly and correctly routed through derivation projection rather than RP-a), and step existence through RP-c.
- **Anti-bloat scan:** the long justification passages (AM's asymmetry defense, I0's rejection of the finer criterion, S2's direction inversion, S3's policy defense) each resolve a genuine design fork and carry load-bearing case analysis or counterexamples; the DR statement/proof split carries exactly one forward pointer and no restatement. I found no relocated findings, no consumer inventories, no ordering apologetics, and no duplicated paragraphs.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: The serializing authority behind I4
**Why out of scope**: I4 correctly scopes concurrency outside `→_sh` and assumes "a serializing authority orders the two calls before either becomes a step." The authority's own contract — whether ordering is per-home or global, what fairness it owes, how it composes with batch tooling like `retract_stale` interleaving with another writer's batch — is agent-layer protocol territory, not a gap in this note's sequential semantics.

### Topic 2: Audit-slice retention
**Why out of scope**: `L_K` grows monotonically forever; nullified tuples, born-nullified deposits, and dedup-suppressed history accumulate without bound. Whether the substrate owes a compaction/archival story — or, equally, a positive guarantee that it never compacts, preserving the audit trail as a permanent commitment — is a storage-layer note. This note's append-only inheritance (L12/L12a) is correct as far as it reaches.

### Topic 3: Rejection diagnostics
**Why out of scope**: the surface's partiality is uniformly "no step, no address" across four distinct rejection causes (gate failure, `K ~ R`, invalid `d` on a miss, P-tgt failure at the wrapper). Whether a caller can distinguish which precondition failed — an error taxonomy over the rejection branch — is API-surface design above the spec; the spec-level rejection semantics here are complete without it.

VERDICT: CONVERGED
