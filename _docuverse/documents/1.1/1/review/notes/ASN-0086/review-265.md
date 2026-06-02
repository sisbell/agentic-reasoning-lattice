# Review of ASN-0086

I read the note in full and checked each of R0–R6, the two wp cases, the decidability lemma, and the five-step worked sketch against the foundation contracts (ASN-0034/0036/0040/0043/0093, all foundations — cross-references to them are licensed).

## Proof-by-proof findings

**R0a (FlatLinkDomain), Case 1 (cross-home).** Verified: `a ≼ a'` forces `zeros(w)=0`, hence `a'`'s three zeros sit at `a`'s positions (all `≤ #a`), so the `N.0.U.0.D` prefix is shared and `home(a')=home(a)` — contradiction. Sound. Case 2 (same-home) correctly reduces to (UL) + T3. No gap.

**R-Scope (SingleTupleScope).** Both admissible branches check out. P1 branch: R0a at Σ gives `{a' ∈ dom(Σ.L): a ≼ a'} = {a}`; the fresh `b≠a` is prefix-incomparable by R0a at Σ'. Self-emit branch (`a=b` fresh): R0a at Σ has no instance for `a`, so all of `dom(Σ.L)` is prefix-incomparable to `a`, leaving `{a}`. Arity-independence is genuine — the argument consults only the prefix relation. Sound.

**wp Case 1 and Case 2.** Case 1's equivalence "postcondition ⟺ `a ∈ A_rel^{Σ'}` (under P0)" is established in both directions, and `A_rel^{Σ'}=A_rel^Σ ∪ {e}` makes the disjunction `P1 ∨ a=a_emit` exact and co-extensive with P-tgt. Case 2's negation chain — `(a,F,G)∈A_K^{Σ'} ⟺ a∉nullified(Σ')`, then splitting `L_R^{Σ'}` into pre-existing vs. fresh — is correct, and the `a_emit∉coverage(G)` escape branch (the `K~R, G=∅` instance) is correctly identified as non-redundant. Both derivations are complete.

**CoverageEqualityDecidable.** The cell decomposition is rigorous: constancy of each coverage on point/gap cells holds because no endpoint lies strictly interior; the immediate-successor `c_k.0` (T1 case (ii)) correctly decides gap-nonemptiness via the single test `c_k.0 ≠ c_{k+1}`; empty gaps are correctly skipped. No hand-wave.

**R3, R6a, R6b, R6c.** Monotonicity, retraction-stability, single-depth (audit-slice) quantification, and the non-monotonicity of `A_K` all check against R2/L12a and the `nullified` definition. R6b is consistently typed DEF-Consequence in body and table.

**Worked sketch.** I recomputed every address: `a₁=1.0.1.0.1.0.2.1`, `b₁=…2.2`, `a₂=…2.3`, `b₂=…2.4`, `a₃=…2.5`; `shift(a₁,1)=b₁` so `coverage({(a₁,δ(1,8))})=[a₁,b₁)={t:a₁≼t}` correctly excludes `b₁`; `nullified(Σ₃)={a₁,b₁}` with `A_K^{Σ₃}` unchanged (R6b non-fixpoint); Step 4 self-nullification lands `a₃∈nullified(Σ₄)`. All `✓` marks are backed by explicit computation, not proof-by-checkmark.

## Edge cases checked
Empty endsets (`F=G=∅` in Nullify), first vs. subsequent emission branches, self-emit target (P1 false), retraction-of-retractor, and higher-arity links (excluded from every `L_K` by the `|Σ.L(a)|=3` conjunct, nullifiable but operationally inert) are all handled. The disjoint union `L^Σ=⨆ L_K^Σ` is total over arity-3 links and disjoint by SliceUniqueness.

## Anti-bloat pass
No egregious forward-reference accretion: `a_emit`, `L-ContiguousPrefix`, and the discipline definitions are referenced backward from their definition sites. The unit-depth-discipline discharge derives a shape invariant from the step-level commitment (not circular) and feeds the wp Case 2 simplification. The long Step 4 verifies the wp false-branch concretely, which the rigor standard explicitly asks for. No paragraph imagines a precondition-excluded case or relocates a prior finding.

## OUT_OF_SCOPE

### Topic 1: Interaction between `L_K` and non-empty arrangements
**Why out of scope**: This note works over ASN-0093's substrate where `M(d)=∅` (M2), so it never confronts how relational predicates behave when from/to content is visible in a populated `Σ.M(d)`. That is genuinely future territory and is already logged as the first Open Question.

### Topic 2: Concurrency/atomicity of Emit vs. Observe
**Why out of scope**: The sequential-atomic transition model (ASN-0093) makes this moot here; a consistency model for concurrent observation is a later layer, captured in the Open Questions.

VERDICT: CONVERGED
