# Review of ASN-0128

The mathematics holds up under detailed checking. I verified the load-bearing chains step by step: I0's closure argument (including the single-span-determined-by-coverage sub-lemma — least element, endpoint separation via TA-strict, displacement recovery), I0a's two-directional minimality proof, I1a's induction including the K ~ R wrapper case, the I6 wp's sufficiency and necessity per branch under the attainability convention, and DR's full derivation — the antichain argument for C3-emptiness, the hit branch's residence/nullification/scope/persistence bullets, and the two off-discipline defeat modes (range-G vs. ghost-target unit-depth bypass), which are correctly distinguished and correctly scoped outside DR's quantifier. The RP transfer apparatus is applied with care (RP-a vs. RP-b vs. RP-c citations are consistently the right one, including the I2 caveat's explicit RP-b routing for RangeSterilization). Boundary cases — empty F rejected by the gate, empty Multi G, no-edge `chain`, self-loop, empty stale batch, self-emit Nullify — are all covered. What remains is one precision defect and two anti-bloat findings of exactly the pattern this cycle's classifier flags.

## REVISE

### Issue 1: The D2/D3 regime bridge's hypothesis has no carrier
**ASN-0128, Default predicates, D2 (IsK)**: "so over address-denoting tuples `is_K(addr) ⟺ (E x : x ∈ members(K, active) : x ≼ addr)`"
**Problem**: "Over address-denoting tuples" attaches to nothing in the formula — both sides aggregate over the *entire* active K-slice, so a per-tuple restriction cannot be what the phrase does. The ⟸ direction is unconditional, but ⟹ fails at any reachable state holding an active K-tuple whose single F-span is non-unit-depth: take `F = {(t, δ(1, m))}` with `m < #t`, deposited via raw `K.λ_sh` — gate-conformant (`|F| = 1`, T12-well-formed since `m ≤ #t`), `addrs(F) = ∅`, yet `is_K` holds throughout its coverage. At such a state the displayed biconditional is false as written. D3 repeats the defect: "so written, over address-denoting tuples it *equals* the coverage-keyed alternative" — the coverage-keyed union additionally collects `addrs(G)` from tuples whose F is non-denoting but whose coverage contains `addr`, which `targets_under` misses. AD's "Verdict for nonconforming tuples" already acknowledges precisely this divergence between the two regimes, so the bridge as literally stated contradicts the note's own off-surface story.
**Required**: State the hypothesis as a condition on the state, in both D2 and D3 — e.g. "at states whose active K-slice is address-denoting (every state reached by a K-surface-emitted derivation, by AD's by-construction guarantee)" — or formally restrict both sides of each equivalence to the denoting sub-slice.

### Issue 2: The no-reachability rationale is argued twice with the same evidence
**ASN-0128, BH2 (determinate-walk), Effect** — "Gregory's link machinery permits cyclic link topologies outright — … discovery being set intersection, never traversal — and Nelson's supersession is linear by *convention* only: … adjudicating among competing claims belongs to readers, not the back end. … no closure or reachability predicate ships … by design, not omission" — **and What this note doesn't cover, "Reachability over the denoted graph"** — "both authorities place multi-hop traversal outside the system — Gregory's machinery answers every link query in a single pass (set intersection over endsets; …), and Nelson leaves following a supersession chain, and adjudicating among its competing claims, to the reader."
**Problem**: The same conclusion (no closure ships) is justified twice, two sections apart, deploying the same two authority citations nearly verbatim. BH2's Effect needs the cycle-constructibility evidence to justify the general-digraph carrier and the branch/cycle verdicts; it does not also need the full no-traversal case, which the doesn't-cover bullet makes again in full. This is the duplication pattern that compounds across cycles.
**Required**: The rationale lives once. Keep the evidence in the doesn't-cover bullet (its natural slot, where the `reach` decision is actually made); BH2's Effect retains the one-sentence scope commitment ("one-step, no closure — by design") and points there, or vice versa.

### Issue 3: Two bullets defer to the same successor
**ASN-0128, What this note doesn't cover**: "**Predicate composition.** … A separate successor (ASN-0126 Open Question 5)." and "**Behavior-behavior interaction edge cases.** … the predicate set's closure under composition is deferred to the predicate-composition successor."
**Problem**: Two bullets in the same list defer to the same downstream location; the second adds only the same-type behavior-pair example before landing at the identical deferral. This is the multiple-deferrals-to-one-location pattern flagged at source.
**Required**: Merge — fold the same-type pair example into the predicate-composition bullet as one sentence.

## OUT_OF_SCOPE

### Topic 1: Transactional semantics for `retract_stale`
**Why out of scope**: The note correctly specifies the batch as an interleavable step sequence with the stale set evaluated once at entry, and proves each constituent admitted. Whether a snapshot-consistent or atomic batch variant is a substrate obligation is new machinery — a concurrency-control commitment the four-component state currently has no vocabulary for — not an error in the sequential contract given here.

### Topic 2: Default-view semantics on behavior-unlocked surfaces
**Why out of scope**: The BH1 × BH2/BH3 dominance question (filtered mid-chain elements, `sources_to` on a filtered address) is pinned to active-view semantics and explicitly deferred (Open question 1). The shipped `retired`/`supersedes` pair makes this the canonical lifecycle scenario and a successor will be forced to settle it, but settling it requires re-opening BH1's rewrite scope, which this note commits coherently as-is.

### Topic 3: Registry composition and evolution
**Why out of scope**: Multi-app declaration merging, coverage-class collision resolution, and any post-`Σ_init` registration path (Open questions 7–8) are construction-protocol territory. R-VAL's fail-construction contract is complete for the single-declaration-set case it claims; the protocol that *produces* a declaration set is a different artifact.

VERDICT: REVISE
