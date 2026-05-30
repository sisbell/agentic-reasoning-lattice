# Review of ASN-0082

I checked the arrangement-layer proofs (I3 and its preservation lemmas, the contraction operation D-SHIFT/D-DOM and all post-lemmas), the ordinal-extraction machinery (ord/vpos/w_ord, OrdAddHom, OrdinalExceedsDisplacement), the span-algebra corollaries (I3-S, D-S), every boundary case, and the anti-bloat patterns flagged for this note.

## REVISE

(none)

The technical content holds up under scrutiny:

- **Insertion shift (I3).** Well-definedness rests on injectivity (TS2) and strict-advance-past-p (TS4 gives shift(v,n) > v ≥ p), and the left/shifted/cross-subspace regions are genuinely disjoint by subspace and document partition. The gap-region argument (v=p lands on the exclusive upper bound; v>p lands strictly past it via TS1) correctly excludes exactly the n vacated positions. The deliberate non-preservation of D-CTG/D-MIN/D-SEQ in the text subspace is correctly scoped — this is the shift sub-operation, not the full INSERT.
- **Contraction.** The contiguity invariant — the one most often hand-waved — is fully computed, not asserted: L ∪ Q₃ = {[1,k] : 1 ≤ k ≤ N−c} is derived in closed form with all four boundary configurations (L=∅, R=∅, both, neither), then D-CTG's quantifier is verified directly against it. Gap closure (D-SEP: ord(r) ⊖ w_ord = ord(p)) and boundary adjacency (D-DP: max-L-ordinal = p₂−1, min-Q₃-ordinal = p₂, consecutive) establish no-gap/no-overlap rigorously.
- **OrdinalExceedsDisplacement** correctly discharges TA4's depth-1 preconditions (k = actionPoint(w_ord) = 1 = #ord(p), zero-prefix quantifier vacuous) and the strict half via TA3-strict + TA6.
- **Boundary coverage** is complete: insert-at-start, insert-past-end, empty document; contraction with L=∅, R=∅, full deletion; cross-subspace examples for both directions including a shifted image landing in a former tombstone slot (S2/S3 verified there).
- **Off-subspace/off-document dispatch convention** is a sound factoring (discharged uniformly by D-CS/D-CD), not bloat.

On the anti-bloat checks specifically: the "Scope" paragraphs state what the operation does and does not do (explicitly protected), the OrdShiftHom justification paragraph genuinely discharges the m ≥ 2 precondition rather than restating it, and the worked examples are concrete verification (protected). I did not find meta-prose that obstructs following a claim.

## OUT_OF_SCOPE

### Topic 1: Contraction at ordinal depth greater than one
**Why out of scope**: I3 (insertion) is proved for general depth m ≥ 2, but the contraction operation is restricted to #p = 2. The asymmetry is real but is the correct boundary for this ASN — at depth > 1, TA4's zero-prefix precondition collides with S8a's componentwise positivity at intermediate components. This is already named in Open Questions 2 and 3 and belongs in a future ASN supplying a weaker inverse law.

### Topic 2: External reference update after a shift
**Why out of scope**: What the system must provide so that an externally-recorded V-position can be re-resolved after a shift repositions it (Open Question 1) is a protocol concern for a later operation ASN, not an arrangement-layer property of this one.

META: not applicable — the ASN defines operation postconditions, frame conditions, and abstract state invariants that any implementation must satisfy, squarely within specification territory.

VERDICT: CONVERGED
