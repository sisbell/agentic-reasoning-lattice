# Review of ASN-0076

## REVISE

### Issue 1: τ_sup underspecified
**ASN-0076, "The Composite"**: "`τ_sup` — a designated tumbler at which the supersession type-endset resolves, a fixed convention of the type registry."
**Problem**: "Type registry" is not a foundation concept. τ_sup's structural form is left entirely undefined — is it in `dom(C)`, `dom(L)`, an element-level tumbler, a document-level tumbler, or something else? PrefixSpanCoverage requires `#τ_sup ≥ 1`, but the ASN doesn't verify even this. L8 (TypeByAddress) demands consistent coverage across supersession links, but the ASN doesn't establish how `τ_sup` achieves stability across allocation events.
**Required**: Either (a) constrain τ_sup to a specific tumbler kind with explicit precondition `τ_sup ∈ T ∧ #τ_sup ≥ 1` and a stability axiom; (b) parameterize EDITLINK by τ_sup as an external input with stated invariants; or (c) explicitly defer type-address semantics to a future ASN and reformulate claims as conditional on the existence of such a tumbler.

### Issue 2: E10 frame statement is wrong on two counts
**ASN-0076, E10**: "`(A d ∈ E_doc \ {d_new} :: Σ'.M(d) = Σ.M(d)) ∧  Σ'.R ⊇ Σ.R    (no R-modifications by K.λ itself)`"
**Problem**: K.λ's frame in ASN-0047 establishes `(A d :: M'(d) = M(d))` — universal, not excluding `d_new`. EDITLINK does not modify `M(d_new)` either (K.μ⁺_L is separate). The exception is spurious. Second conjunct: K.λ has `R' = R` (equality), so `⊇` is strictly weaker than what holds. The parenthetical contradicts the formula.
**Required**: `(A d ∈ E_doc :: Σ'.M(d) = Σ.M(d)) ∧ Σ'.R = Σ.R`. Remove the d_new exception; tighten ⊇ to =.

### Issue 3: No verification against ValidComposite★
**ASN-0076, E0**: "The composite is *not* a primitive of the transition vocabulary `Σ`... It is a named pattern of two existing primitive applications."
**Problem**: ASN-0047 defines ValidComposite★ as the formal admissibility predicate for composites, requiring coupling constraints J0, J1★, J1'★ to hold. The ASN claims EDITLINK is a valid composite without verifying these. J0 requires content allocation to be paired with placement, but EDITLINK allocates links, not content — J0 is vacuously satisfied. J1★/J1'★ concern content-subspace provenance — also vacuously satisfied. But the ASN must say so explicitly to claim valid composite status.
**Required**: Add a verification subsection: "EDITLINK as a valid composite. The composite applies K.λ twice. (i) Elementary preconditions of K.λ are satisfied at each intermediate state, as discharged above. (ii) J0 is vacuously satisfied: `dom(C') = dom(C)`, so the antecedent `a ∈ dom(C') \ dom(C)` is empty. (iii) J1★ and J1'★ are vacuously satisfied: arrangements are unchanged, so range differences are empty. Therefore EDITLINK satisfies ValidComposite★."

### Issue 4: Missing formal preconditions
**ASN-0076, "The Composite"**: "We name an existing link `ℓ_old ∈ dom(Σ.L)`... We name a document `d_new ∈ E_doc`..."
**Problem**: The composite definition prose-states what is needed, but no formal precondition block enumerates them. By contrast, every elementary transition in ASN-0047 has a precise *Precondition:* clause. The reader must infer EDITLINK's preconditions by tracing K.λ's preconditions through the composite — but the composite's preconditions must be evaluated at the *initial* state, not at intermediate states.
**Required**: Add an explicit Precondition clause: `ℓ_old ∈ dom(Σ.L) ∧ d_new ∈ E_doc ∧ N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : e'_i ∈ Endset) ∧ e'_3 ≠ ∅ ∧ τ_sup ∈ T ∧ #τ_sup ≥ 1`.

### Issue 5: E2 cites "L12 monotonicity" instead of L12a
**ASN-0076, E2 proof**: "By L12 monotonicity and the chain of states leading to that intermediate state, `ℓ_old ∈ dom(L)`"
**Problem**: L12 in ASN-0043 is link immutability (`a ∈ dom(Σ.L) ⟹ a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`). The monotonicity consequence is named separately as L12a (LinkStoreMonotonicity). Citing "L12 monotonicity" is imprecise — name the lemma.
**Required**: Replace "By L12 monotonicity" with "By L12a (LinkStoreMonotonicity), `dom(L) ⊆ dom(L_i)` at every intermediate state `L_i`".

### Issue 6: ℓ_sup distinctness from ℓ_old and ℓ_new not stated
**ASN-0076, E2 and E4**: ℓ_sup is introduced as a fresh allocation but its distinctness from the other named tumblers is not formally claimed.
**Problem**: E2 establishes `ℓ_new ≠ ℓ_old`. The supersession link is also fresh, so `ℓ_sup ≠ ℓ_old` and `ℓ_sup ≠ ℓ_new` by L11a. This is needed to prevent degenerate cases (e.g., a self-referential supersession claim where `ℓ_sup = ℓ_new`).
**Required**: Add a corollary or extend E2: "ℓ_sup ≠ ℓ_old ∧ ℓ_sup ≠ ℓ_new, by L11a applied to the two K.λ events of the composite."

### Issue 7: E7 depends on undefined discovery operation
**ASN-0076, E7**: "We claim only the abstract guarantee: if a discovery operation `find_links(a)` returns... then `ℓ_sup` is in `find_links(ℓ_old)` and in `find_links(ℓ_new)`."
**Problem**: E7 is stated as a property of EDITLINK, but it is conditional on an operation not defined here or in any cited foundation. The witness — coverage of the endset spans contains ℓ_old and ℓ_new — is solid, but E7 as written claims a property of "discovery operations" that may or may not exist. The conditional framing partially mitigates this but blurs what is being asserted.
**Required**: Reframe E7 as a *structural property* rather than a behavioral guarantee: "For any operation `f : T → 𝒫(dom(L))` that returns `{ℓ : (E (s, w) ∈ Σ.L(ℓ).e_i : a ∈ coverage({(s, w)}))}`, `ℓ_sup ∈ f(ℓ_old) ∩ f(ℓ_new)`." This separates the structural fact (the coverage relationship) from the existence of a discovery operation.

### Issue 8: No concrete worked example
**ASN-0076, throughout**: The ASN states E0–E10 in the abstract without verifying them against a specific scenario.
**Problem**: Per review standards, at least one concrete example should verify the key postconditions. Pick specific tumbler values for `ℓ_old`, `d_new`, endsets, τ_sup, compute `ℓ_new` and `ℓ_sup` from the deterministic K.λ allocation rule, and check E1, E2, E4, E10 against the resulting state.
**Required**: Add a worked example section. E.g., suppose `home(ℓ_old) = [3.0.5.0.7]`, `Σ.L(ℓ_old) = (F_old, G_old, Θ_old)`, `d_new = [3.0.5.0.7]` (same document as the original). Then `ℓ_new` = first or next emission of `A_L(d_new)`; `ℓ_sup` = subsequent emission of the same sub-allocator. Show concretely that ℓ_old, ℓ_new, ℓ_sup are pairwise distinct, that `Σ.L(ℓ_old)` is unchanged, and that `Σ'.L(ℓ_sup) = (E_from, E_to, E_type)` with the expected endset structure.

### Issue 9: "Failures and resumptions" language inconsistent with foundation
**ASN-0076, E0 discussion**: "the steps need not be atomic; any other transitions may occur between them, including failures and resumptions — the composite is well-defined as long as both K.λ applications eventually fire."
**Problem**: SequentialTransitionAxiom in ASN-0047 establishes that transitions are atomic, total, and sequentially ordered. There is no failure model. "Failures and resumptions" is implementation-level vocabulary that has no formal counterpart at this layer.
**Required**: Replace with: "the steps need not be adjacent in the transition sequence; arbitrary other transitions may intervene between them."

### Issue 10: "Concurrent users" language imprecise
**ASN-0076, E5 discussion**: "Two distinct users, working independently, may each issue an EDITLINK against the same `ℓ_old`..."
**Problem**: SequentialTransitionAxiom rules out true concurrency at this level of abstraction. Two EDITLINKs against the same `ℓ_old` occur in *some* order, just one after the other in the transition sequence. The architectural property is that *neither order produces a conflict*; both supersession claims coexist.
**Required**: Reframe as: "Two independent EDITLINK composites against the same `ℓ_old`, occurring in either order, yield a state containing both supersession claims as distinct facts. No transition ordering produces a conflict."

### Issue 11: "Reader's Perspective" section is informal
**ASN-0076, "A Reader's Perspective"**: Sketches a discovery procedure as numbered steps without formalization.
**Problem**: The section is illustrative but presents no verified claim. It introduces concepts ("tree or DAG of supersession claims", "current candidate", "policy chooses which leaf to follow") that are not formalized and arguably introduce implementation-level vocabulary.
**Required**: Either formalize the procedure as a lemma (with preconditions, postconditions, and proof of termination/correctness), or move it to an appendix labeled as illustration and explicitly disclaim its status as a verified property. Given the open question list already defers chain semantics, the latter is probably more appropriate.

## OUT_OF_SCOPE

### Topic 1: Type registry semantics and τ_sup origin
**Why out of scope**: How τ_sup is established as a stable, system-wide convention requires a type-registry ASN — the addressing scheme for type tumblers, their allocation discipline, and their relationship to L8/L10 are substantial territory beyond an editing operation note. (But: Issue 1 above still requires the ASN to be precise about τ_sup's *structural form as a precondition input* even if its origin is deferred.)

### Topic 2: Discovery operation formalization
**Why out of scope**: The ASN explicitly defers `find_links` to a link-search ASN. This is appropriate. (But: Issue 7 above still requires E7 to be reformulated so it states a structural property rather than depending on a behavioral guarantee from undefined machinery.)

### Topic 3: Supersession chain semantics
**Why out of scope**: Cycles, multi-link supersessions (one-to-many, many-to-one), and chain resolution policies are flagged as open questions and properly belong in future work.

### Topic 4: Reader resolution policy
**Why out of scope**: Which of multiple supersession claims to honor is a social/application question; the ASN correctly defers it.

### Topic 5: Counter-claim and retraction structure
**Why out of scope**: The ASN sketches the idea (a counter-claim is itself a link) but does not formalize. Belongs in a separate ASN.

VERDICT: REVISE
