# Review of ASN-0086

## REVISE

### Issue 1: wp Case 2 regime (i) "automatic" simplification is unsound over the stated domain

**ASN-0086, Weakest-Precondition Analysis, Case 2 (regime (i) and the closing simplification)**: "Under the unit-depth retraction discipline (regime (i) holds for the pre-state), `NoCraftedSpanReachesD` is automatic — every `L_R^Σ` tuple has to-span coverage `{t : b ≼ t}` for some `b ∈ A_rel^Σ`, and R0a's antichain on `dom(Σ'.L)` puts `a_emit(Σ, d) ∉ {t : b ≼ t} ∩ A_rel^{Σ'}` for every such `b` — and the wp simplifies to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible ∧ (K ≁ R ∨ ...)`."

**Problem**: This simplification invokes **R0a**, which holds only at *substrate-conforming* states. But Emit_K's domain — and therefore this wp's domain — is the *state-local-conforming* sub-space (Definition — Emit_K), which the ASN itself constructs to *admit* antichain-violating states (the `a'' = inc(a, 1)` witness). Over that domain regime (i) does **not** make `NoCraftedSpanReachesD` automatic. Concrete counterexample using the ASN's own non-conformance witness: let `a, a'' ∈ dom(Σ.L)` be homed at `d` with `a ≼ a''` (`a'' = inc(a, 1) = a·[1]`), and let `L_R^Σ` contain the unit-depth retraction `(_, _, {(a, δ(1, #a))})` (unit-depth discipline satisfied). If `ℓ_prev = a''`, then `a_emit = inc(a'', 0) = a·[2]`, and `a ≼ a_emit`, so `a_emit ∈ coverage({(a, δ(1, #a))})` — `NoCraftedSpanReachesD(Σ, d)` is false even though regime (i)'s hypothesis holds. The simplified three-conjunct wp would then wrongly conclude `(a, F, G) ∈ A_K^{Σ'}`.

**Required**: Either restrict the regime-(i) simplification (and its "automatic" claim) explicitly to substrate-conforming pre-states, or carry `NoCraftedSpanReachesD` as an irreducible conjunct over the full state-local-conforming domain. The relational-layer specialization at the end is fine because that layer is substrate-conforming; the "direct K.λ caller … most permissive scope" version is the one that breaks.

### Issue 2: R0a-Cor1 induction base assumes `dom(Σ_init.L) = ∅` without justification

**ASN-0086, R0a-Cor1 proof**: "*Base:* `dom(Σ_init.L) = ∅`, so every `H_d^{Σ_init} = ∅` and contiguity holds with `J_d^{Σ_init} = -1`."

**Problem**: The emptiness of the initial link store is asserted with no citation. None of the foundation ASNs supplied here establish `dom(Σ_init.L) = ∅` (ASN-0040's seed `B₀` is explicitly permitted to be non-empty, so the analogy cuts the other way). The entire contiguous-prefix induction — and hence R0a Case 2, R0a-Cor2, and R7a discharge (4) — rests on this base.

**Required**: State the initial-state link-store emptiness as an explicit assumption of this ASN, or cite the foundation that provides it. Alternatively, generalize the base to "`H_d^{Σ_init}` is a contiguous chain prefix for every `d`" and justify that for whatever seed the substrate admits.

### Issue 3: Anti-bloat — changelog prose, repeated defensive clauses, and redundant restatement

The note carries the `review-mode.anti-bloat` classifier; the following are findings at source:

- **Changelog prose in a structural slot.** Properties Introduced table, R0a-Cor1 row: "Single-key contiguity induction on conformance clause (b) … **supersedes the former ConformingHomedContiguity sub-lemma, which is now folded in here**." A table of properties should state the property, not narrate which prior sub-lemma it replaced.
- **Repeated defensive clause.** The R0 proof repeats "*at every state in the operations' domain — not only at the `→*`-reachable ones*" (and the near-identical "*not only at the `→*`-reachable ones*") at the end of the first-emission discharge, the subsequent-emission discharge, and again in the summary sentence. One statement of the scope claim suffices; the others are noise the reader must skip past.
- **Lemma statement duplicated in the table.** Properties Introduced, R7a row, re-states the contingency clause verbatim: "(the address-reconstruction half `Σ_m.L = Σ'.L` holds under clause (b); absent it, only `dom(Σ_m.L) = dom(Σ'.L)` …)" — already fully stated in the R7a lemma. The table row should point to the lemma, not re-prosecute its contingency.
- **Orphan meta-sentence.** Foundation paragraph: "Citations of S3 refer to S3 (ReferentialIntegrity, ASN-0036)." This advances no reasoning and belongs (if anywhere) inline at first use.

**Required**: Delete the "supersedes the former…" changelog fragment, collapse the three "→*-reachable" repetitions to one, drop the duplicated contingency clause from the R7a table row, and remove the orphan S3-citation sentence.

### Issue 4: R6b formal statement uses prose predicates inside the quantifier

**ASN-0086, R6b**: "`(A Σ → Σ', a, b : a ∈ nullified(Σ) witnessed by a tuple at b : a ∈ nullified(Σ') even if b ∈ nullified(Σ'))`"

**Problem**: "witnessed by a tuple at b" and "even if `b ∈ nullified(Σ')`" are English glosses embedded in a formal quantifier, not predicates. The intended content — that the witnessing existential ranges over `L_R^Σ` and is insensitive to `b`'s own membership in `nullified` — is precise in the proof but not in the stated contract.

**Required**: Replace the prose with the formal predicate, e.g. `(A Σ → Σ', a, b, F', G' : (b, F', G') ∈ L_R^Σ ∧ a ∈ coverage(G') : a ∈ nullified(Σ'))`, and state the `b`-insensitivity as a separate clause about the quantification domain rather than inside the binder.

## OUT_OF_SCOPE

### Topic 1: Cardinality/structural bound on `nullified(Σ)` relative to `dom(Σ.L)`
**Why out of scope**: Whether unbounded retraction is permitted or a structural ratio must hold is a new invariant question (already listed in Open Questions), not a defect in the present derivations.

### Topic 2: Atomicity of Emit vs. concurrent Observe / consistency model for `A_K` transitions
**Why out of scope**: A concurrency-semantics question; this ASN reasons about a sequential, atomic transition relation (SequentialAtomicTransitions, ASN-0093) and need not settle the concurrent model.

### Topic 3: Multi-arity typed relations `L_K^{(n)}`
**Why out of scope**: The note deliberately restricts to standard-triple links; higher-arity relational structure is explicitly deferred and belongs in a future ASN.

VERDICT: REVISE
