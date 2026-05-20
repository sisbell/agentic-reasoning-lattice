# Review of ASN-0086

## REVISE

### Issue 1: Numerical inconsistency in strict-strengthening argument
**ASN-0086, "Definition — substrate-conforming layer" → strict-strengthening paragraph**: "the tumbler `a* = [d.0.s_L.1.1]` (length `#d + 3 + 2`, with `home(a*) = d`, `E(a*)₁ = s_L`, `zeros(a*) = 3`) is reachable by an L1c-admissible chain `d → d.0.1 → d.0.2 → d.0.2.1 → d.0.2.1.1`"
**Problem**: `[d.0.s_L.1.1]` has length `#d + 4` (appending 4 positions: 0, s_L, 1, 1), not `#d + 3 + 2 = #d + 5`. The chain shown adds 4 positions (k₁=2 adds 2; k₂=0 adds 0; k₃=1 adds 1; k₄=1 adds 1, total 4), consistent with `#d + 4`. The "#d + 3 + 2" expression is either a computational typo or the chain notation is wrong by one step.
**Required**: Correct to `#d + 4`, or extend the chain by one step if `#d + 5` was intended.

### Issue 2: R0a Case 1 reverse direction is a substitution-claim, not a derivation
**ASN-0086, R0a Case 1 (cross-home)**: "(Reverse direction: `¬(a' ≼ a)`, by explicit substitution.) The forward derivation depends on `a` and `a'` only through the predicates [...] all of which are symmetric in their argument positions. We instantiate the forward derivation under the variable substitution `(a, a', d, d') := (a', a, d', d)` [...]"
**Problem**: The five enumerated bullets verify that the *predicates* are symmetric under substitution, but the actual reverse derivation (concluding `home(a) = home(a') = d' ≠ d` under `a' ≼ a`) is not carried out. For a Dijkstra-style proof, the reader should not have to mentally execute the symmetric substitution; either the argument is shown or a substitution lemma is invoked by name.
**Required**: Either carry out the reverse derivation in 2–3 lines parallel to the forward, or invoke a named symmetry lemma. The current "by explicit substitution" walks the boundary of proof-by-similarity.

### Issue 3: R0's substrate-invariant discharge omits ASN-0093 M/C invariants
**ASN-0086, R0 proof, L-invariant preservation block**: "ASN-0036's S-invariants (S0, S1, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ) transfer by input-substitution: each is a predicate over `(Σ.C, Σ.M)`, and K.λ's Frame fixes both components."
**Problem**: R0 verifies ASN-0036 S-invariants in one line but does not enumerate ASN-0093 M0, M1, C0, C1, C1b, C1c, C-fin, which are also predicates over `(Σ.C, Σ.M)` and require the same Frame discharge. R7a's *Per-step substrate-invariant discharge* block enumerates all of these per step type and per mechanism; R0's brevity creates an asymmetry — if the per-step accounting is needed in R7a, the equivalent should appear in R0.
**Required**: Add ASN-0093 M-/C-invariants to R0's discharge list, with the same one-line "transfer via K.λ Frame on (Σ.C, Σ.M)" argument. Alternatively, factor out a "K.λ Frame preserves all (Σ.C, Σ.M)-predicates" lemma and cite it at both sites.

### Issue 4: DEF-Consequence label used in Properties Introduced table but undefined in type-label key
**ASN-0086, "Properties Introduced" → Type labels paragraph and table row for R6b**: The type-label key paragraph defines "DEF, LEMMA, OP, COMMITMENT" (four labels). The table's R6b row uses "DEF-Consequence", a fifth label not in the key.
**Problem**: The label is used without being named in the type taxonomy. R6b's prose explains why the label is unusual (substantive consequence of definitional choice), but the table key should match the labels used.
**Required**: Either add "DEF-Consequence" to the type-label key paragraph with one sentence of definition, or relabel R6b as DEF (with the substantive content remaining in the body).

### Issue 5: Worked Sketch does not exhibit a K.σ-prefix scenario
**ASN-0086, "Worked Sketch"**: All four steps (Step 0 first-emission; Steps 1–3 subsequent-emission) operate at a single pre-existing home `d ∈ dom(Σ_{-1}.M)`. The sketch acknowledges cross-home retraction in passing ("a different caller homed at `d' ∈ dom(Σ_0.M)` with `d' ≠ d` would supply `Nullify(Σ_0, d', a₁)` instead") but does not demonstrate it.
**Problem**: R7a's substantive content — that composite operations decompose into K.σ-prefix + K.λ — is exhibited in the proof's Worked Examples 1 and 2 but not in the main Worked Sketch. A reader of the Sketch alone never sees a K.σ-prefix fire and never sees the chain-anchor `[d.0.s_L.1]` in a context where it is the *initial* link at a freshly-allocated home. R0a-Cor1 (contiguous prefix across `A_L(d)`) and R0a-Cor2 (`#E = 2`) are exercised only on a single home's chain.
**Required**: Add a "Step 0a" or auxiliary worked example exercising K.σ at a fresh `d_new`, followed by the K.λ first-emission at `[d_new.0.s_L.1]`, to demonstrate that R0a-Cor1's `J_d^Σ` transitions from `-1` to `0` at the moment of first emission.

### Issue 6: L5/L6/L8 categorization in substrate-conforming catalog (a)
**ASN-0086, "Definition — substrate-conforming layer" → catalog (a)**: Lists "L5 (EndsetSetSemantics), L6 (SlotDistinction), [...] L8 (TypeByAddress)" alongside genuine state invariants like L0, L1, L12.
**Problem**: Per the ASN-0043 catalog supplied to this review, L5 is a predicate definition (set-semantics characterization), L6 is a predicate/definitional commitment on positional accessors, and L8 is a function definition (`same_type` plus equivalence-relation claims). These are not state invariants requiring preservation across transitions in the same sense as L0/L1/L11a/L12; their "preservation" is trivial (a definition holds wherever its terms are well-defined). The catalog conflates definitional commitments with operational invariants.
**Required**: Either separate catalog (a) into "state invariants requiring per-step preservation" and "definitional commitments that hold wherever the link store is well-formed", or add a one-sentence note explaining why L5/L6/L8 are bundled with the operational invariants.

## OUT_OF_SCOPE

### Topic 1: Higher-arity link relations (`|Σ.L(a)| > 3`)
**Why out of scope**: The note restricts to standard-triple links explicitly and lists the multi-arity question in Open Questions. Extending `A_K^{(n)}` and Nullify to higher-arity links is genuinely new territory.

### Topic 2: Cardinality bound on `nullified(Σ)` relative to `dom(Σ.L)`
**Why out of scope**: Listed in Open Questions. Unbounded retraction is admitted by R6a + R3; whether ratios should be constrained is a substrate-design decision for a future ASN.

### Topic 3: Substrate-level unit-depth retraction enforcement
**Why out of scope**: Listed in Open Questions. WP Case 2 makes explicit that crafted-span retractions are not precluded by K.λ; whether a designated K-operation should enforce unit-depth retraction is a substrate-level design question.

### Topic 4: Concurrent semantics for Emit and Observe
**Why out of scope**: Listed in Open Questions. The ASN inherits ASN-0093's `SequentialAtomicTransitions` axiom (sequential, totally ordered, atomic transitions); concurrent variants are future work.

### Topic 5: L1b tightening to `#E = 2`
**Why out of scope**: R0a-Cor2 establishes `#E = 2` unconditionally within the substrate; the question of whether L1b itself should be tightened is correctly identified in Open Questions.

### Topic 6: Cross-layer admissible-type collision
**Why out of scope**: Listed in Open Questions. Multi-layer type coordination is genuinely new architecture beyond this ASN's scope.

VERDICT: REVISE
