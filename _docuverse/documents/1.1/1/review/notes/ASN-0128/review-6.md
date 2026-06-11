# Review of ASN-0128

This is a post-revision pass (the prior cycle's R-VAL and I0/I1a findings have been addressed). I checked every proof obligation in the note line by line; the load-bearing derivations all close. Summary of what was verified before the verdict:

- **I0's minimal-element identity** — both inclusions of "≼-minimal elements of coverage(e) = ≼-minimal elements of addrs(e)" are shown, and the recovery of coverage from the minimal listings correctly uses finiteness of `addrs(e)` (every element of a finite set sits above a minimal one; prefix-chains are finite). The bound on what a dedup hit can suppress is therefore genuinely established, not asserted.
- **I1a's induction** — the case analysis is complete: K.σ/K.α frame `Σ.L`; non-K deposits leave `L_K` fixed and `nullified` grows monotonically, so classes only shrink; a K-deposit is forced by the surface-emitted hypothesis to be an Emit_K miss, giving its class at most one active member at the post-state; the K ~ R sub-case (a wrapper deposit nullifying a member of another class, including retraction-of-retraction) is handled, and class membership is immutable by L12. The hypothesis's downward inheritance along the derivation (intermediate states of a surface-emitted history are themselves surface-emitted, since `L_K` grows monotonically and deposit mode is historical) is used implicitly but is a one-line fact; it does not weaken the proof.
- **DR's C3-vacuity derivation** — the heart of the note, and it is sound. Both P-tgt branches put the target `a` into the link domain no later than the retraction's own post-state; L12a (carried per step by ASN-0126's B2 and across extended-record derivations by RP-b) keeps it there; freshness of `f = a_emit(Θ, d)` gives `f ≠ a`; and the strict-prefix enumeration is exhaustive — every strict prefix of `chain_d(m)` is a prefix of `d` (zeros ≤ 2, violating L1), `d.0` (`#E = 0`), or `d.0.s_L` (`#E = 1`), each violating L1 or L1b, which `a` satisfies as a link address at Θ. So `¬(a ≼ f)`, and C3's existential is empty over a surface-disciplined `L_R`.
- **DR's wp equivalence** — the attainability convention is declared exactly where it is load-bearing: the note itself exhibits the case (P0 failure against a resident target) where the postcondition holds at the unchanged state, so the bare-guarantee reading would falsify necessity. Necessity is then discharged per precondition, including the genuinely-false case under ¬P-tgt; sufficiency is completed per branch, with the hit branch re-establishing residence, nullification, single-tuple scope (R0a antichain), and persistence at `Σ' = Σ` from the incumbent tuple rather than from a step. The self-emit-cannot-hit argument (subtree root uniqueness via mutual ≼, the root resident since its own emit, the self-emit candidate fresh) is correct.
- **I6's wp** — POST is correctly coverage-typed; necessity holds in every excluded case (rejection forfeits the returned address POST exhibits; an admitted miss failing C2/C3 deposits born-nullified at the returned address); the disciplined-domain reduction correctly cites both DR (C3 vacuity) and S3 (Emit_K exposed only at K ≁ R, discharging C2's first disjunct).
- **RP apparatus** — ρ preserves everything the gate and the cited ASN-0126 results read; the RP-a/RP-b division is maintained with care (FrontierUnification by RP-a; RangeSterilization and R6a/R6c only by RP-b's derivation projection; RP-c justified precisely because the relation acquired no new precondition).
- **BH2 termination**, **BH4's age non-negativity** (an active tuple at index j forces `f_d ≥ j+1`), **retract_stale's once-at-entry P0** (persistence by domain monotonicity, the front-truncation counterexample for per-constituent evaluation is correct), and the **D2/D3 bridge identities** (including the `targets_under` equality via PrefixSpanCoverage) all check out.
- Boundary cases are present: gate-failing hit candidates (gate-first order made observable), invalid-`d` hit admission, born-nullified resurrection at sterilized slots, single-element chains, branches and cycles at the walk's first step, the empty stale set, self-loop edges, and the Σ_init base everywhere.
- The depth standards are met: a concrete worked example exists (the abstract registry, exercising every unexhausted shape/behavior cell including the born-nullified case), the wp analyses are non-trivial in both Case-1 and Case-2 forms, and consequences are derived rather than gestured at.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: BH1 dominance over behavior-unlocked surfaces (`sources_to` on a filtered address, default-view `chain()` through a retired mid-chain element)
**Why out of scope**: The note *does* specify the shipped behavior — BH1's rewrite scope is exactly `members` and `targets_of`, "nothing else is rewritten," so the walk and reverse lookup are active-view, full stop. Whether the default view *should* extend to those surfaces is a design choice for a successor; the note correctly pins the current semantics and logs the question (its Open Question 1) rather than leaving behavior undefined.

### Topic 2: Multi-app registry composition and collision resolution
**Why out of scope**: C0's key uniqueness plus R-C1 state the constraint and R-VAL enforces it by failed construction; the *protocol* by which several apps' declarations merge into one `Σ_init.registry` is new machinery (the note's Open Question 8), not an error in the construction-time story given here.

### Topic 3: Audit-view chain walking and reachability closure over the denoted graph
**Why out of scope**: Both are deliberate withholdings with grounded rationale (single-pass query discipline; adjudication belongs to the reader). `reach` and historical `chain()` are decidable extensions a successor can ship when a forcing case appears; their absence creates no unsoundness in what is shipped.

### Topic 4: A real concurrency semantics
**Why out of scope**: I4 resolves races by appeal to a serializing authority ahead of the relation, which is the honest boundary of a sequential interleaved step model inherited from ASN-0086. A genuine concurrent semantics (commutativity, conflict, merge) would be a new framework, not a repair to I4 — which correctly derives the outcomes for both serialization orders, born-nullified cases included.

### Topic 5: BH1 × BH1 composition (multiple read-filter types)
**Why out of scope**: The Views section's union phrasing ("when *some* Unary type registered with BH1…") together with the per-K rewrite rule determines the multi-filter case, including a filter type's own members being filtered by another filter type. A worked statement of the composed rewrite belongs with the predicate-composition successor the note already defers to.

VERDICT: CONVERGED
