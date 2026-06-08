# Review of ASN-0102

I reviewed the COPY operation against the rigor standards: precondition completeness, case coverage, every invariant conjunct, boundary cases, and the anti-bloat patterns the note is flagged for.

## Findings

**Precondition completeness (PC1–PC4).** Complete. The empty-copy boundary is excluded explicitly (`W ≥ 1` via C2), the empty-subspace case is handled by a depth choice (ValidFirstInsertionPosition), and the insertion-position range `1 ≤ p ≤ n_S+1` is pinned.

**Edge-case coverage.** Every boundary the checklist demands is present and worked concretely: position 0 / first insertion (empty subspace, `p=1`), append (`p=n_S+1`, trailing boundary absent), self-transclusion overlapping the displaced region, cross-origin fragmentation, and a coalescing copy where both inter-reference and leading boundaries fire. The five worked examples verify the relevant postconditions against specific arrangements, including the non-trivial `W > (n_S−p+1)` case where the no-overwrite conclusion is correctly grounded in range disjointness rather than full pre-population.

**Tiling proof (X16).** Checked the partition `[1,p) ∪ [p,p+W) ∪ [p+W, n_S+W] = [1, n_S+W]` against all boundary `p`: interior, `p=n_S+1` (displaced interval empties to `[6,5]`), and `p=1, n_S=0`. No gap, no overlap in any case. S8a is independently discharged for copied, displaced, *and* unmoved classes; cross-subspace disjointness is argued via component-1 distinctness and T3 rather than hand-waved.

**Invariant discharge (X14).** Every conjunct of ExtendedReachableStateInvariants and ExtendedTransitionInvariants (P3) is addressed individually, not by "similarly." The coupling discharge is the hardest part and is handled carefully: J0 vacuous by X1; the J1'★ argument explicitly splits the copied set at the opening boundary `B` (where P4★ legitimately holds) rather than at the mid-composite state `Σ` (where P4★ may fail), and flags why the Σ-local split would be unsound. P4★ is established by induction on composite boundaries, and P7 grounding plus `T_elem × E_doc` well-typing are both shown at the `Σ.R` extension.

**wp analysis.** `wp(COPY, S3★)` is non-trivial: the three-class partition reduces S3★ to a single membership obligation on the copied region, discharged at the pre-state by C1. Not a trivial "true."

**Abstract framing.** The ASN commits only to the arrangement `Σ'.M(d)`, treating block count as representational (X8) and citing Gregory only as evidence. It does not drift into implementation mechanics — no META.

**Anti-bloat scan.** I checked for relocated findings, imagined-excluded-cases, axiom-justification prose, repeated downstream deferrals, and duplicate paragraphs. The candidates I found (X10(a) recasting the frame clause; the one-line INSERT comparison; the X4/X6 prose on instance-vs-value identity and structural attribution) are all either protected by the explicit carve-out — "statements of what an operation does or does not do" — or serve a real structural purpose (X10(a) completes the source-handling dichotomy that X10(b) contrasts against). X10(b) properly *cites* X15 rather than re-deriving atomicity. No material accretion remains.

## OUT_OF_SCOPE

The four Open Questions (re-displacement of copied content, transitive containment under chained references, time-varying views, identity under unreachable allocator) are correctly deferred — each opens new state-evolution territory beyond a single COPY step. The ASN defines no INSERT/DELETE/REARRANGE/link/version claims, so there is nothing to flag.

VERDICT: CONVERGED
