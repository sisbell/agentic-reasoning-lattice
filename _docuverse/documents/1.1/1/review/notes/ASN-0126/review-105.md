# Review of ASN-0126

## REVISE

### Issue 1: T4-validity of the chain elements is hypothesized, never discharged
**ASN-0126, Range sterilization**: "The chain ascends strictly: a sibling advance modifies only the sig position — for a T4-valid input, the terminal position (TA5(c), TA5-SigValid, as in CPP, ASN-0043) — incrementing that component while preserving length and every earlier position…"

**Problem**: The ascent argument carries the hypothesis "for a T4-valid input" but the note never establishes that every `chain_d(j)` is T4-valid. For filled slots (`j ≤ J_d^Σ`) L0b covers it, since those addresses are in `dom(Σ.L)`. But the sterilization analysis quantifies over **unfilled** slots `j > J_d^Σ` — exactly the slots B sterilizes — and those are not in `dom(Σ.L)`, so L0b is unavailable and the hypothesis is undischarged at precisely the load-bearing indices. The gap propagates: strict ascent feeds B's consecutiveness (the squeeze argument), and the up-set realizability ("a to-span at the subspace root `g = d.0.s_L` has coverage … containing every `chain_d(j)`") needs each `chain_d(j)` to retain the prefix `d.0.s_L`, which is CPP's sibling-advance case — also conditioned on sig-is-terminal, i.e., on T4-validity of each input. Without the discharge, Corollary RangeSterilization's clauses (i) and (ii) rest on an unproven premise for every future slot.

**Required**: Two or three sentences before the ascent paragraph: `chain_d(0) = d.0.s_L.1` is T4-valid because it is the terminus of a T10a-conforming chain seeded at the T4-valid document node `d` (DocVal via S7d, as L11a's chain argument uses — equivalently, it is `a_emit`'s first-emission output, an L1c-conforming address), and T10a.4 propagates T4-validity across each sibling advance `inc(·, 0)`; induction on `j` then covers every chain element, filled or not. This is the same chain-extension pattern FSE (ASN-0043) already uses.

### Issue 2: The Observe_R claim quantifies over retractions the wrapper does not produce
**ASN-0126, Retraction as an attributed Binary**: "so `Observe_R`, matching a from-pattern `F̂` against `coverage(F)`, now matches every retraction homed at `d_retr` against any under-`d_retr` pattern."

**Problem**: The universal "every retraction homed at `d_retr`" holds only for retractions carrying the canonical from-fill `r`. The gate enforces `|F| = 1`, not `F = {r}`: any single-span source clears Binary registration. The note's own worked illustration falsifies the sentence as written — Step 1 emits a gated retraction homed at `d` via generic `Emit_R` with `F = [c₁]`, and the under-`d_retr` pattern `F̂ = {d_retr}` fails `F̂ ⊆ coverage([c₁])` (since `#c₁ > #d_retr`, `d_retr ∉ {t : c₁ ≼ t}`), so that retraction is not matched.

**Required**: Qualify the quantifier — "every *wrapper-routed* retraction homed at `d_retr`" (or: every retraction carrying the canonical from-fill) — or state the from-fill convention as normative for `Nullify_Binary` and scope the Observe_R consequence to retractions routed through it.

## OUT_OF_SCOPE

### Topic 1: Registry evolution / runtime registration
**Why out of scope**: Construction-time-only registration is a deliberate commitment — P1 depends on it, and the empty-registry corner in the worked illustration shows the framework is honest about the consequence (a permanently link-inert substrate). An app that must add a type after `Σ_init` (schema migration) needs a registration step kind with its own frame and a weakened P1/P2 — successor-note territory, related to but distinct from Open Question 4.

### Topic 2: Sterilization under a Multi-registered retraction class
**Why out of scope**: Corollary RangeSterilization explicitly fixes R registered Binary, which is what pins `G' = {(g, ℓ)}` single-span and makes B consecutive. The framework permits an app to register its retraction class Multi, making B a finite union of consecutive blocks; clause (i) generalizes per-span but (ii)'s single-block count does not. The corollary's hypothesis is explicit and matches the note's prescribed retraction route, so the variant is future analysis, not an error in the proof given.

### Topic 3: Adoption over a non-empty legacy link store
**Why out of scope**: P6's base case rides on `Σ_init.L = ∅`, inherited from ASN-0086. Gating an existing store mid-history — where `dom(Σ.L)` may already hold higher-arity, unregistered, or shape-non-conforming values — is a deployment/migration question that the framework's `Σ_init` construction deliberately excludes; it needs its own treatment of how P6 weakens over a legacy slice.

VERDICT: REVISE
