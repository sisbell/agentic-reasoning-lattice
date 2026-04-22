# Reverse-Course Oscillation

A reviser's change in cycle N is undone in cycle N+1 — reverted by the next reviewer, reversed by the next reviser, or restructured away as if the earlier change had never been made. The cone does not converge. It flips between two resolutions that both look locally valid, because no shared criterion exists for the reviewer and reviser to defer to.

Unlike [gravitational failures](README.md#gravitational-patterns) (monotonic growth) and [transitional failures](README.md#transitional-patterns) (representation boundary without a contract), the driving force here is undecidability. Two answers are each locally plausible. Nothing in the cycle picks between them, so the cycle picks alternately.

## Forces

**Local plausibility of both resolutions.** A reviewer flags "example missing for the `0.0.0` edge case." The reviser adds it. A later reviewer flags "the `0.0.0` example is redundant with the general definition." The reviser removes it. Both findings are individually reasonable. The disagreement is about completeness-vs-restraint — a judgment the cycle has not made.

**No shared criterion.** The reviewer and reviser each operate on a narrow prompt scoped to their role. Neither holds the rule that would arbitrate. Review cycles are not architected to produce a ruling; they produce findings and fixes within an assumed set of rules. When the rule is absent, each cycle invents one, and the inventions contradict.

**Partial cross-cycle visibility.** The agent running cycle N+1 does not see cycle N's diff. It sees only the current state and its own finding. A change that looks arbitrary-but-locally-defensible in cycle N+1 may be exactly the change cycle N made. Without history visibility, each cycle is blind to its own recent past.

**Add-bias flipping with restraint-bias.** A reviser prompt that rewards completeness and a reviewer prompt that rewards concision together produce cycles that alternate between expansion and contraction on the same content. The prompts are fine in isolation; the feedback loop between them has no damping.

## Signal

- **Symmetric diffs across consecutive cycles.** Cycle N's diff at a file region is the reverse of cycle N+1's diff at the same region. Mechanically detectable by comparing adjacent cycle diffs for the same file region.
- **Repeated revisits with no net change.** A file region is modified in three or more consecutive cycles with near-zero net line change across the span. The work is happening; the state is not advancing.
- **Near-duplicate findings across non-adjacent cycles.** Cycle 2 says "add X"; cycle 5 says "add X" again, because X was added in 2 and removed in 3 and the system is back where it started. Finding-text similarity across cycles with intervening reverts is a signal.
- **Cycle count growing without convergence.** Taken alone this is weak — a cone can be slow without oscillating — but combined with either of the two signals above it sharpens.

## Subtypes

The undecidability has multiple sources, and the resolution differs by source.

**Contract-absent oscillation.** Two resolutions look locally valid because no rule says which is canonical. "T4a cited without statement" could be fixed by inlining the body into the citing file or by leaving the citation and relying on the canonical home — both work locally, neither is ratified. This is the [Uncontracted Representation Change](uncontracted-representation-change.md) case. Disappears when the contract is written.

**Judgment-call oscillation.** The choice is genuinely a matter of editorial judgment — whether an example adds value or adds bloat, whether a qualifier clarifies or clutters. No structural contract can arbitrate. Disappears when a convention is established (in the prompt, in a style note, or in an explicit ruling from upstream).

**Exhaustiveness-vs-restraint oscillation.** One cycle flags "missing cases"; the next flags "overextended scope." The scope of the claim itself is unsettled. Disappears when the scope is explicitly declared — either by the authoring prompt or by a meta-review that settles the question.

## Example: ASN-0034 ActionPoint cone

Three oscillations in eight cycles on the same cone:

- Cycle 2 added a `0.0.0` example; cycle 3 removed it. (Judgment-call.)
- Cycle 1 added T1 to TA-Pos's `depends`; cycle 4 removed it. (Contract-absent — no rule said whether T1 was load-bearing.)
- Cycle 6 rewrote `≥` as `1 ≤`; cycle 7 restructured the claim to use a "nonempty" qualifier, effectively undoing cycle 6. (Contract-absent — symbol resolution unspecified, so each cycle picked a different patch.)

Net effect across the cone: eight cycles, no convergence, ~740 lines of additions mostly reverted by other cycles.

## Resolution

Every resolution takes the same shape: establish the criterion the cycle can defer to. The form varies by subtype.

- **Write the missing contract.** For contract-absent oscillations, the resolution is the same as [Uncontracted Representation Change](uncontracted-representation-change.md) — specify the rule once, have the validator check it, cite it in the prompts so findings and fixes both refer to the shared criterion.
- **Establish the convention.** For judgment-call oscillations, write the preferred resolution into the prompt or a style note. "Prefer the general definition over edge-case examples unless the example surfaces a constraint the definition does not state."
- **Settle the scope.** For exhaustiveness-vs-restraint oscillations, a meta-review or authoring ruling declares what the claim is responsible for. Subsequent reviewers apply the declared scope rather than inventing one.
- **Surface the oscillation itself as a finding.** Once the signal is detected mechanically, a higher-scope review (regional or full) can receive "cycles N and N+1 reversed each other at region R" as input and ask which resolution is correct. This turns the oscillation from an invisible convergence failure into a visible decision request.

## Related

- [Uncontracted Representation Change](uncontracted-representation-change.md) — the contract-absent subtype of oscillation has the same cause and the same resolution. Oscillation is one observable signal of an uncontracted representation change; the other signals (structural findings, multiple cones patching the same gap) are complementary.
- [Review V-Cycle](../design-notes/review-v-cycle.md) — oscillation is a pathology of the review/revise loop. The V-cycle's wider scales (regional, full) can see oscillations that local-scale review cannot, because they see cross-cycle diff history.
- [Self-Healing Areas](../design-notes/self-healing.md#convergence-and-cycle-health) — oscillation detection is a speculative self-healing target; the mechanical signal (symmetric cross-cycle diffs) meets the viability criterion.
