# Review of ASN-0086

The technical core is sound: the domain discipline (`→*`-reachable ⊆ substrate-conforming ⊆ state-local-conforming) is tracked consistently, R0/R0a's branch splits are complete, the WP analyses are genuinely non-trivial with both directions established, and the worked sketch verifies the key postconditions against concrete tumblers. The findings below concern definitional well-posedness and the accreted forward-reference prose the anti-bloat classifier flags.

## REVISE

### Issue 1: Clause (c) of substrate-conforming presupposes the contiguity L-ContiguousPrefix proves
**ASN-0086, Definition — substrate-conforming state, clause (c)**: "if a step adds a fresh key at home `d` whose homed-set occupied chain indices `0..J` before the step, that key occupies exactly chain index `J+1` of `A_L(d)` — no gap, no index skipped."

**Problem**: The phrase "homed-set occupied chain indices `0..J`" is only meaningful if every homed key lies on `A_L(d)`'s sibling chain *and* forms a contiguous initial prefix. But a general homed key need not lie on the chain at all — the NestedLinkWitness `a'' = inc(a, 1)` is homed at `d` yet is a child-spawn off `A_L(d)`'s sibling enumeration, so it has no chain index. Thus clause (c)'s hypothesis is ill-posed except on states that already satisfy the contiguity that L-ContiguousPrefix is later charged with proving. L-ContiguousPrefix's inductive step *does* resolve this (the IH keeps each pre-state contiguous, making "indices `0..J`" well-defined at each step), but the definition as written is not self-contained — its well-posedness silently leans on the invariant downstream.

**Required**: Either restate clause (c) without presupposing chain-membership/contiguity (e.g., "the fresh key equals `inc(ℓ_prev, 0)` where `ℓ_prev` is the prior T1-maximum of the homed-set, or `[d.0.s_L.1]` if the homed-set is empty"), or state explicitly that (c) is read jointly with L-ContiguousPrefix's contiguity along the inductively-constructed trajectory and is not a free-standing per-state predicate.

### Issue 2: Triple deferral to NestedLinkWitness across three sections
**ASN-0086**: the same `a'' = inc(a, 1)` separating witness is invoked in three different paragraphs:
- *Definition — state-local-conforming state*: "The separation is witnessed by states that preserve every state-local invariant yet violate R0a's antichain (Remark — NestedLinkWitness, below)."
- *Definition — substrate-conforming state*: "The nested emission `a'' = inc(a, 1)` of Remark — NestedLinkWitness satisfies (b) yet lands off the frontier, so it violates (c)."
- *Remark — NestedLinkWitness*: "A higher layer may emit `a'' = inc(a, 1)` ... The resulting state is state-local-conforming yet violates R0a's antichain — a separating witness."

**Problem**: Two forward references and one definition, all restating the same `inc(a, 1)` construction in different words. This is the "multiple paragraphs in different sections defer to the same downstream location" pattern compounding across cycles. A reader meets the witness three times before extracting one fact.

**Required**: State the witness once (the Remark), and have the two definitions cite it by name without re-describing the `inc(a, 1)` mechanics.

### Issue 3: Document-ordering / scope-justification meta-prose
**ASN-0086, Assumption — EmptyInitialLinkStore**: "(A restart from a persisted store inherits whatever was last flushed; we root the state space at the fresh system, from which every persisted configuration is `→*`-reachable.)"

**ASN-0086, R7a proof**: "The proof has two structural phases: a monotonicity argument establishing the Δ-enumeration of fresh link addresses, and a K.σ/K.λ replay reconstructing them as `→`-steps."

**Problem**: The first parenthetical justifies *why the root state was chosen* rather than advancing the assumption's content — document-scope rationale. The second is a proof-roadmap sentence occupying a structural slot; the two phases are self-evident from the proof body that follows.

**Required**: Drop both. The assumption's content is `dom(Σ_init.{C,M,L}) = ∅`; the R7a proof reads identically without the phase-preview sentence.

## OUT_OF_SCOPE

### Topic 1: Pre-emptive retraction of not-yet-allocated addresses
Nullify executes even when `a ∉ A_rel^Σ` (P1 does not gate), depositing an `L_R` tuple whose coverage `{t : a ≼ t}` could later capture an address allocated at `a`. Whether such "retract-before-exists" tuples should be admissible, and their interaction with future emission, is a behavioral question for a future ASN, not an error here.

META: not applicable — the ASN defines state (`L_K`, `A_K`, `nullified`), operations (Emit/Observe/Nullify), and invariants (R0–R7) at an abstract, implementation-independent level; it has not drifted into implementation mechanics.

VERDICT: REVISE
