# Review of ASN-0076

I read the note and checked each claim's derivation, the worked example, and the wp analysis against the foundation contracts.

## REVISE

(none)

## Assessment of the proofs

I traced the load-bearing arguments and found them complete:

- **E0** discharges all four K.λ preconditions at *both* steps explicitly, splitting the successor step into first-emission and subsequent-emission sub-cases. The `#E ≥ 2` depth bound is proved by induction with an explicit base (SubAllocatorBundle) and step (TA5(c) length preservation + TA5(b) modification-confinement + TA5-SigValid terminal-position placement), not hand-waved. Adjacency, ValidComposite★ (J0/J1★/J1'★ vacuous via the C- and M-preserving frame of K.λ), and invariant inheritance are each addressed.
- **E1/E8/E9** correctly route permanence through L12 (single-step) and LP13 (multi-step); the value-preservation conjunct is established by structural identity, not assertion.
- **E2** uses a clean member/non-member argument keyed to the pre-state vs. intermediate state.
- **E5** is a genuine induction with a vacuous base case (k=0), a fixed target document (`home(ℓ_old)`), and 2k-event pairwise distinctness via L11a + SequentialTransitionAxiom.
- **E11** is a non-trivial wp: the pullback through E10's frame plus LP12, with the middle (`ℓ_new`) disjunct shown vacuous via the F-structure / `#E = 2` collapse argument (LP-Sub, T3). This satisfies the depth requirement.

Boundary cases I checked independently — `d_new = home(ℓ_old)` (collision avoided by L11a subsequent-emission), `#τ_sup = 1` (T12 saturates), empty arrangement (orphaning via LP17/LP18), `τ_sup` arbitrary in T — are all consistent with the claims as stated.

The worked example verifies every claim E0–E11 against concrete tumblers. No cross-ASN references outside the foundation set (0034/0036/0043/0047/0098); no reinvented notation.

## Anti-bloat scan

No findings. The repeated depth-bound reasoning is referenced ("by the same argument structure as sub-case (b)") rather than duplicated. E6's application-layer note and E11's collapse paragraph are substantive (statements of model limits and an actual derivation), not meta-prose. The intro's motivation is appropriate and was already tightened.

## OUT_OF_SCOPE

Supersession-chain invariants, cycle detection, "current successor" computation, retraction semantics, and multi-link supersession are correctly deferred to Open Questions rather than asserted here.

VERDICT: CONVERGED
