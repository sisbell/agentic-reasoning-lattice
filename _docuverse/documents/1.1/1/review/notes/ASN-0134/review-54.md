# Review of ASN-0134

This is a careful note. The conflict theory (H0–H3), the per-home/global partition (W0–W4, G1), the verdict-soundness chain (V0–V2), and the operation-level order-dependence families (§4, G2) are largely sound, and the note meets the depth bar — a worked allocation scenario (§7), a worked verdict trace (§8), a wp summary (§9), and derived safety (SAFE). The findings below are a rigor gap in the read-isolation argument plus the forward-reference/meta-prose accretion the `anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: A3/A4 derive "single-state view" from "zero-step," but that is clause 4's obligation, not a consequence
**ASN-0134, §2 (A3) and §9 (MIC clause 4 minimality)**:
A3: "An Observe realized at index k is a total function of the single state `Σ_k`... This is just the zero-step half of A1 together with the definition of `Observe_K` in ASN-0086 as a function of Σ."
Clause-4 minimality: "drop 4 and a single logical read's internal accesses — an `age` frontier descent, or `Observe_K`'s own `A_K = L_K ∖ nullified` computation — straddle a commit, compounding two committed states into one verdict though clause 1 keeps every step atomic."

**Problem**: Zero-step-ness establishes only that the read does not *advance* `𝔼` (commits no step). It does **not** establish that the read's *view* is a single state. A faithful `Observe_K` computes `A_K = L_K ∖ nullified`, an internally multi-access read over the link store; absent an atomicity obligation its internal accesses land on different committed states — which is exactly what the clause-4 minimality argument asserts. So the two claims cannot both stand as written: if A3 holds free-standing from A1 + the definition, then the clause-4 counterexample is impossible and clause 4 is not load-bearing; if clause 4 is load-bearing (the minimality says it is), then A3's "function of the single state `Σ_k`" silently assumes it. A4's proof inherits the same gap — "The reader's state `Σ_k` is either at-or-before `Σ_i`... or at-or-after `Σ_{i+1}`" presupposes a single-state view, which for a multi-access `Observe` *is* clause 4 — and A1's "it reads a state and returns" (singular) is the same unstated assumption. The phrase "realized at index k" smuggles in the pinning that clause 4 obligates.

**Required**: Either cite clause 4 (single-state realization of a bounded access) as a premise of A3/A4, or explicitly separate the abstract reading (`Observe_K(Σ)` is a function of one Σ, trivially) from the realized reading (a concurrent implementation's `Observe` yields `Observe_K(Σ_k)` *only under clause 4*), and route A4 / SAFE(a) / V0's realized guarantees through clause 4. As written A3 is labeled a derivation but omits its load-bearing premise, and that premise's independence is then asserted three sections later by the minimality argument.

### Issue 2: The pipelined client model is stated twice, adjacent and near-verbatim
**ASN-0134, §3**: the paragraph before G0 — "An agent may issue operations *concurrently* — *pipelining*: holding several in flight at once, issuing the next before the prior's acknowledgment returns" — and G0's own opening — "*Client model:* an agent may invoke operations *concurrently* — pipelining, several in flight, the next issued before the prior's acknowledgment."

**Problem**: Two slots say the same thing in different words (an anti-bloat target). The lead-in paragraph and the claim restatement are redundant.

**Required**: State the pipelined client model once; have G0 reference it rather than restate it.

### Issue 3: Claims-table cells carry essay content (re-derived proofs and witnesses)
**ASN-0134, Claims Introduced table**: e.g. G0 — "...not sequentially consistent — cross-home commutation alone is SC-benign, but a third party witnesses non-SC (P emits A→B, Q reads B-present then A-absent, forcing an unserializable cycle); linearizable under A7." A5, V2, and A6 cells likewise carry proof prose rather than statements.

**Problem**: Essay content in a structural slot. A claims table should state each claim and its status; re-deriving the non-SC witness (and V2's strict-implication chain, A6's transfer-lemma roster) in a cell duplicates the body.

**Required**: Reduce cells to the claim statement and status; the witnesses and derivations belong only in the body.

### Issue 4: Deferral and positioning meta-prose around already-established claims
**ASN-0134, §5 (W0, W1) and §4 (instance (ii))**:
W1: "preserved by every valid step exactly as W0's monotonicity is; A6 carries that preservation argument, and W1 records the classification it yields." W0: "A6's transition clause already carries them across every step of `𝔼`; W0's part is the classification."
Instance (ii): "Decisively, this instance survives the disciplines that tame the others: ... neither instance (i)'s hypothesis nor the target-residence race's holds."

**Problem**: The model-intrinsic/serialization-borne classification (W0/W1) and the toggle-off scenario (instance (ii)) are genuine content, but they are wrapped in narration: W0/W1 re-explain that A6 already did the proof (deferral narration), and instance (ii) leads with commentary distinguishing it from sibling findings rather than advancing the scenario — the reviser-drift pattern of justifying a case against its neighbors.

**Required**: Keep the classification and the scenario; drop the "A6 carries the argument, W-claim records the classification" narration and the "survives the disciplines that tame the others" positioning.

## OUT_OF_SCOPE

The note's deferrals (scheduler/fairness, rule bodies, BEBE, concrete mechanism, predicate cost) are correctly declared in *What this note does not cover* and surfaced as Open Questions, defining no claims for them. Nothing to add — scoping is clean.

VERDICT: REVISE
