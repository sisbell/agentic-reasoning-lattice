# Review of ASN-0086

I checked the proofs and the worked arithmetic. The substantive correctness is sound: R0's per-branch freshness discharge is exhaustive over `dom(Σ.L) ∪ dom(Σ.C)`; R0a Case 1's zero-counting (`zeros(a') = zeros(a) + zeros(w)`, both 3 ⟹ `zeros(w)=0` ⟹ shared home) is correct; R0a-Cor1's single-key induction is independent of R0a (no circularity); R0a-Cor2's zero-position-stability argument holds via TA5(c)+TA5-SigValid; and the Worked Sketch checks out digit-by-digit (`a₁=1.0.1.0.1.0.2.1`, `b₁=…2.2`, coverage exclusion of `b₁`, `nullified(Σ_3)={a₁,b₁}`, `A_K^{Σ_3}={(a₂,F₁,G₁)}`). Boundary cases (empty store, Nullify of absent/higher-arity address, self-nullification, retraction-of-retractor) are all covered.

The findings below are the anti-bloat patterns this note's classifier asks me to surface.

## REVISE

### Issue 1: The K.λ first/subsequent emission rule is restated in full at five sites
**ASN-0086, R0 proof / Emit_K Effect / Lemma — Emit_K function-ness / Definition — a_emit / R7a discharge (4)**: the two-branch rule "first emission (`{ℓ' : origin(ℓ')=d}=∅`) gives `a=[d.0.s_L.1]`; subsequent gives `a=inc(ℓ_prev,0)` with `ℓ_prev:=max{…}`" appears verbatim (modulo wording) in each of these locations.
**Problem**: This is accreted repetition. The canonical formalization — `a_emit(Σ, d)` — exists, but it is introduced *in the wp section*, after at least four inline restatements have already been given. A precise reader must re-verify that each inline copy agrees with the others.
**Required**: Introduce `a_emit(Σ, d)` once, early (e.g., in the Allocator Structure section), and have R0, Emit_K, the function-ness lemma, and R7a reference it rather than re-spell the branches. The Worked Sketch's concrete computations are fine (they are instantiations, not restatements).

### Issue 2: R0a-Cor2's statement forward-references a Worked-Sketch object that does not yet exist
**ASN-0086, R0a-Cor2**: "(Here `#E(a)` is the length of the element-field projection — e.g., `E(a₁) = [2, 1]`, `#E(a₁) = 2` at the concrete instantiation.)"
**Problem**: `a₁` is defined only later, in the Worked Sketch. A lemma statement should not illustrate itself with an object introduced pages downstream; the reader cannot resolve `a₁` at the point of reading.
**Required**: Either give the illustrative example in terms already in scope (`E(t_1) = [s_L, 1]`, which the proof already uses) or drop the parenthetical.

### Issue 3: Meta-prose justifying why prose/hypotheses are present
**ASN-0086, wp Case 1 Non-weakestness**: "the local weakening is recorded for honesty, not adopted as the layer's contract."
**ASN-0086, after R0's statement**: "The conformance hypothesis is load-bearing: the proof's freshness discharges consume the state-local invariants L0, L1c, and L-fin, none of which survive at an arbitrary `↝*`-reachable non-conforming state…"
**Problem**: These sentences explain *why the surrounding text is included* rather than advancing the argument. The first is bookkeeping about authorial intent; the second explains why a hypothesis is needed (it is matched by the wp Case 1 load-bearingness analysis already, which *shows* it via counterexample). When the same fact is both asserted defensively and demonstrated, the assertion is noise.
**Required**: Drop the "recorded for honesty" sentence (the local-antichain weakening stands on its own). For R0, let the load-bearingness be carried by the demonstration rather than pre-announced; if retained, compress to a clause.

### Issue 4: R6b's formal statement carries an unused antecedent conjunct
**ASN-0086, R6b**: the contract quantifies over `… ∧ b ∈ nullified(Σ) : a ∈ nullified(Σ)`, and the proof states "the fourth hypothesis `b ∈ nullified(Σ)` is never consulted."
**Problem**: As a logical statement, R6b is strictly *weaker* than what the proof establishes (the conclusion follows from the first three hypotheses alone). Advertising a LEMMA whose stated antecedent is broader than its proof requires forces the reader to notice the slack. The demonstrative intent ("nullification of `b` does not block `b`'s effect") is real, but it belongs in a remark, not baked into the quantifier.
**Required**: Either state R6b in its true (three-hypothesis) strength and add a one-line remark that the conclusion is insensitive to `b`'s own nullification status, or recast R6b explicitly as a definitional consequence (the table already labels it "DEF-Consequence" — the heading and contract should match that, not present it as a conditional lemma).

## OUT_OF_SCOPE

### Topic 1: Concurrency / atomicity model for Emit vs Observe
The note's own Open Questions raise whether Emit must be atomic w.r.t. concurrent Observe and the consistency model for observing `A_K` transitions. This is genuinely new territory (a concurrency layer), not a gap in the present single-threaded `→*` development.

### Topic 2: Cardinality bound on `nullified(Σ)` relative to `dom(Σ.L)`
Also flagged in Open Questions. Whether unbounded retraction is permitted is a future structural-ratio question, not an error here.

VERDICT: REVISE
