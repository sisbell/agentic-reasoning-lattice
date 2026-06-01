# Review of ASN-0086

## REVISE

### Issue 1: R7a's "absent clause (b)" branch contradicts its own hypothesis, is unproven, and is false

**ASN-0086, R7a (statement)**: "For any state-affecting transition `Σ ↝ Σ'` issued by a substrate-conforming layer ... such that — *under conforming-layer clause (b) (frontier-contiguous deposition)* — `Σ_m.L = Σ'.L` ...; absent clause (b), only the weaker `dom(Σ_m.L) = dom(Σ'.L)` (the same fresh addresses, up to deposition order) is guaranteed."

**Problem**: The leading hypothesis "issued by a substrate-conforming layer" already entails clause (b): the *Definition — substrate-conforming layer* states such a layer "preserves clauses (a) ... and (b) ... at every step." So every in-scope transition satisfies clause (b), and the "absent clause (b)" branch describes a case the hypothesis excludes — reviser drift (a paragraph imagining a case the precondition rules out).

Worse, the weaker conclusion is never proven (the entire proof, discharge (4)(i), reads "By clause (b) ... R0a-Cor1 holds at Σ'") and is in fact false. Absent clause (b), `Σ'` may contain a nested link address such as `a'' = inc(a, 1) = a·[1]` (the very non-conformance witness used in the *state-local-conforming* definition and in WP Case 2). That address is not a sibling-frontier element of any `A_L(d)` chain (it arises from a `k=1` child-spawn, not `inc(·, 0)`). The R7a replay deposits link keys only through K.λ's first/subsequent (`inc(·, 0)`) emission rule, so it can never produce `a''`. Hence `dom(Σ_m.L) ≠ dom(Σ'.L)`, contradicting the hedge.

**Required**: Delete the "absent clause (b)" hedge (and the "contingent on conforming-layer clause (b)" qualifier in the Properties-Introduced row), since the hypothesis already supplies clause (b). If a genuinely weaker hypothesis is intended, restate it and prove the weaker conclusion rather than asserting it.

### Issue 2: The "single-depth" content of R6b is not in its formal contract

**ASN-0086, R6b**: `(A Σ → Σ', a, b, F', G' : a ∈ A_rel^Σ ∧ (b, F', G') ∈ L_R^Σ ∧ a ∈ coverage(G') : a ∈ nullified(Σ'))`

**Problem**: The named property is *SingleDepthRetraction* — that deciding `a ∈ nullified` quantifies over the audit slice `L_R^Σ` and never consults whether the witness `b` is itself nullified. But the antecedent `a ∈ A_rel^Σ ∧ (b,F',G') ∈ L_R^Σ ∧ a ∈ coverage(G')` is exactly the unfolding of `a ∈ nullified(Σ)`, so the formula reduces to "a nullification witness persists across `→`" — which is R6a restated. The distinctive non-fixpoint content lives entirely in the *Definition of nullified* (existential over `L_R`, not `A_R`) and in the surrounding prose, not in the contract. The formal claim does not establish what its name asserts.

**Required**: Either state the single-depth property as a formula that distinguishes it from R6a — e.g. explicitly that `a ∈ nullified(Σ)` holds *even when* the witness `b ∈ nullified(Σ)` — or fold the persistence half into R6a and present single-depth purely as a labeled definitional remark, not as a separate lemma whose formula duplicates R6a.

### Issue 3: Repeated restatement of the "at most one fresh key per home per step" discipline

**ASN-0086, multiple sections**: the same fact — "this note's operations deposit at most one fresh link key per home per step ... a composite `↝`-step may touch several homes but contributes at most one fresh key to any single home" — appears verbatim-in-substance in (a) *Definition — substrate-conforming state*, (b) the R0a-Cor1 induction step, and (c) the R7a statement note / proof discharge (4).

**Problem**: Two-plus paragraphs in the same document saying the same thing in different words (a flagged anti-bloat pattern). The precise reader must reconcile three statements of one invariant to confirm they agree.

**Required**: State the at-most-one-key-per-home property once (in the substrate-conforming-state Definition, where it belongs) and cite it from R0a-Cor1 and R7a rather than re-deriving the enumeration each time.

### Issue 4: state-local-conforming definition justifies its shape by downstream consumers

**ASN-0086, Definition — state-local-conforming state**: "**The bare operations `Emit_K`/`Nullify` and the precondition computations below range over the state-local-conforming sub-space** ... The sub-space still admits the antichain-violating states (e.g. the `a'' = inc(a, 1)` target case), so the non-conformance counterexamples the wp analyses rely on are retained."

**Problem**: A definition's introduction enumerating its downstream consumers ("the wp analyses rely on") and justifying its boundary by what later proofs need, rather than advancing the definition's own meaning — a flagged accretion pattern. The witness construction belongs at the WP Case-1/Case-2 sites that actually use it.

**Required**: State the four-way containment and the separating witness without the "retained for the wp analyses" use-site justification; let the WP analyses cite this definition rather than the definition pre-advertising them.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations and Observe ordering/atomicity
**Why out of scope**: The note explicitly restricts to standard-triple links (`|Σ.L(a)| = 3`) and defers higher-arity projections, Observe result ordering, and Emit/Observe concurrency to the Open Questions. These are new structure on top of the present substrate, not defects in it.

### Topic 2: `L_K`–arrangement (`Σ.M`) interaction under M2
**Why out of scope**: Predicates depending on whether from/to content is currently *visible* in a document require arrangement structure, which M2 (EmptyArrangement) suppresses in the adopted foundation. This is correctly a future ASN once arrangements carry content.

VERDICT: REVISE
