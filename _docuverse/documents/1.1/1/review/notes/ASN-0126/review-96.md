# Review of ASN-0126

The note is, on the mathematics, in good shape. I checked the load-bearing proofs against the standards that matter here and they hold:

- **P5 (GateRealizability)** correctly lifts `Emit_K`'s `K.λ` step at `π(Σ)` back to a `K.λ_sh` step at Σ: all five preconditions (L3, `d ∈ dom(Σ.M)`, (0), (i), (ii)) are discharged, and `K ∈ T_admissible` is recovered via the non-emptiness transfer in **RegisteredAdmissible** — a genuinely necessary step, since the emitted type slot is `K`, not the stored representative `K_j`. Sound.
- The **Retraction-as-Binary** three-move derivation is correct, including the load-bearing "frame the two post-states together": the wrapper-emit and the empty-from `Nullify` call `a_emit` on the *same* `(π(Σ), d_retr)`, `a_emit` is blind to F, so the two post-states share their link domain and R-Scope's conclusion transfers.
- **P6**'s induction discharges all three conjuncts for already-present tuples via L12 (value), P1 (registration), P4 (conformance), each correctly bridged through ProjectionBridge + B1.
- Boundary cases are unusually well covered: `F = ∅` rejected, `G = ∅` (Unary/Multi) handled, empty registry → link-inert, `Σ_init.L = ∅` base, ghost targets (P4 example), self-targeting (Binary self-emit in the wp). The "born nullified" worked example concretely verifies the gate-vs-landing separation. These are exactly the checks the standard demands, and they are present.

I found no correctness gap. The findings below are the prose-level patterns the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: "Tension with type identity" is an editorial overstatement, and imprecise
**ASN-0126, Shape-conformance**: "This decomposition-sensitivity is the gate's distinctive point, and it sits in tension with type identity — types are keyed by *coverage class* (The registry), which is coverage-invariant, yet conformance counts spans."

**Problem**: Two distinct defects in one sentence. (a) "is the gate's distinctive point" is significance-editorializing that adds nothing to the definition. (b) "sits in tension with type identity" is misleading. Type identity tests coverage of slot 3; shape conformance counts spans of slots 1–2. They act on *different slots for different purposes*, and slot 3 simply *selects* which span-count constraint applies to slots 1–2. There is a dependency, not a conflict — an emitter freely chooses K (for the type/shape it wants) and then supplies F, G with conforming span counts; the two checks can never be mutually unsatisfiable. "Tension" invites the reader to look for an unresolved conflict that does not exist. The substantive content (span count and coverage diverge, in both directions) is already established concretely by the two preceding sentences.

**Required**: Cut the coda, or replace it with the accurate framing — the framework deliberately combines a decomposition-blind type identity (coverage, slot 3) with a decomposition-sensitive shape gate (span count, slots 1–2), and the two are independent. Do not call it a tension.

### Issue 2: Transfer-machinery scoping is forward-pointed and partly duplicated
**ASN-0126, The projection bridge (B2)**: "A transition invariant of ASN-0086 (quantified over `→`-steps, e.g. L12) transfers only across a genuine `→_sh`-step `Σ →_sh Σ'`, whose projection `π(Σ) → π(Σ')` is the single ASN-0086 step it constrains; P6 makes that transfer inline."

**Problem**: The clause "P6 makes that transfer inline" annotates B2's *statement* with how a downstream lemma will use it — forward-reference accretion. B2's meaning is complete without it (P6 indeed performs the L12 transfer directly via ProjectionBridge + B1, not via B2, so the pointer is accurate but belongs at P6, not embedded in B2). The B2 caveat is then re-explained downstream — Gate realizability opens with "does not come from B2, which yields no `→_sh`-successors (The projection bridge)" — restating the rationale B2 already gave. This is the "multiple sections defer to / re-derive the same scoping" pattern.

**Required**: State B2's scope once and neutrally (no successors; transition invariants transfer only across a genuine `→_sh`-step). Drop the "P6 makes that transfer inline" pointer. Let P6 and Gate realizability *cite* B2's scope when they invoke it, rather than re-deriving the "no successors" reason.

## OUT_OF_SCOPE

### Topic 1: Expressibility of a discontiguous from-source under `|F| = 1`
**Why out of scope**: The Single-source rule forbids any F that is not a single span, so a from-source whose addresses do not form one well-formed span is inexpressible (Multi relaxes only G, never F). This is a real limitation, but the note already routes it to Open Question 6 ("Extension beyond F=1"). Correctly deferred — not a defect in this note.

META: (none — the ASN defines new state, an operation refinement, and state invariants abstractly enough that an alternative substrate would have to satisfy them; it has not drifted into implementation mechanics.)

VERDICT: REVISE
