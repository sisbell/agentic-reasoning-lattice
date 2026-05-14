# Review of ASN-0043

## REVISE

### Issue 1: L9's formal statement restricted to standard-triple links, while the worked example demonstrates arity 4

**ASN-0043, L9 (TypeGhostPermission)**: "...there exists a conforming state `Σ'` extending `Σ` with a *standard-triple* link whose type endset references an address outside `dom(Σ'.C) ∪ dom(Σ'.L)`"

**Problem**: The formal claim is restricted to arity 3 ("standard-triple"). Step 3 of the worked example exhibits an arity-4 link `a₃ = (F₃, G₃, Θ₃, R₃)` with the same ghost type at `g`, but the L9 statement as written does not cover this case. The witness construction in the proof generalizes trivially (extend `Σ'.L(a) = (∅, ∅, {(g, δ(1, #g))})` with additional empty slots), but this extension is not formalized. A reader checking that the arity-4 link in Step 3 satisfies the ASN's structural guarantees has no L9 to cite — the example is exercising a property L9 doesn't claim.

**Required**: Generalize the L9 statement to "a link" (any arity `N ≥ 3`) rather than "a standard-triple link," and note in the proof that the standard-triple witness extends to higher arities by inserting empty endsets at positions other than slot 3 (L3's non-empty conjunct applies to slot 3 alone; slots 4..N may be empty).

### Issue 2: Worked example exercises L8 only reflexively

**ASN-0043, Worked Example, "L8 (TypeByAddress) at Σ — reflexivity"**: "The single-link state admits a non-vacuous reflexivity check: `same_type(a, a) ⟺ coverage(Σ.L(a).type) = coverage(Σ.L(a).type)`. The right-hand side is a set-equality of identical sets, true by reflexivity."

**Problem**: Every link in the example (a, a', a₂, a₃) is given the same type endset `Θ = {(g, δ(1, 8))}`. L8's substantive content is that types match *by address coverage*, distinguishing same-type from different-type links — but the example concretely exercises only the reflexive case `same_type(a, a)`. The discussion of an alternative endset `Θ'` with identical coverage but distinct span set illustrates coverage's lossiness, but it is hypothetical (no state contains a link with `Θ'`) and does not exercise *discrimination* between different types — the case where `same_type` returns false.

**Required**: Add a concrete second ghost type — e.g., `g' = 1.0.1.0.1.0.3.2` (sibling of `g` in subspace `s_X`) — and a fifth link `a₄` whose type endset targets `g'` rather than `g`. Verify that `coverage({(g, δ(1, 8))}) = {t : g ≼ t}` and `coverage({(g', δ(1, 8))}) = {t : g' ≼ t}` are disjoint (since neither tumbler extends the other, by the prefix structure), and conclude `same_type(a, a₄) = false`. This makes L8's discrimination concrete.

### Issue 3: L1c clause (i) is presented as an axiom but its justification depends on clause (ii)

**ASN-0043, L1c (LinkAllocatorConformance)**: "*(i) T4-validity.* Every link address is T4-valid: `(A a ∈ dom(Σ.L) :: T4-valid(a))`. T4-validity is stated as an explicit conjunct of L1c rather than as an external derivation because clause (ii) below uses the formula `N(a).0.U(a).0.D(a)`, which presupposes T4-validity of `a` to be well-defined under T4b. The conjunct is justified internally by T10a.4: every output of a T10a-conforming allocator is T4-valid, and clause (ii) below witnesses each link address as such an output via its chain."

**Problem**: The structure is reflexively circular as presented. Clause (i) is needed for clause (ii)'s formula `h(a) = N(a).0.U(a).0.D(a)` to be well-formed. Clause (i) is justified by clause (ii)'s chain (via T10a.4). The two clauses are interdependent for both well-formedness and justification. The prose acknowledges this ("justified internally") but does not separate the axiomatic content from the derivable content. A reader cannot tell whether clause (i) is load-bearing or redundant.

**Required**: One of (a) restate clause (ii) using a fresh variable `s` for the chain seed (instead of `h(a)`), then derive `s = h(a)` as a *consequence* after T4-validity is established via T10a.4 on the chain output; or (b) explicitly mark clause (i) as a derived consequence of clause (ii) — not an independent axiomatic conjunct — and state the L1c axiom as the chain alone, with T4-validity as a postcondition. Either resolution clarifies what L1c is committing to versus what it derives.

### Issue 4: L1c's chain-origin clause admits k₁ = 1 which is operationally unreachable

**ASN-0043, L1c chain-origin clause**: "`k₁ ∈ {1, 2}`... *Why `k₁ = 1` is admitted but operationally unreachable.* The disjunction `k₁ ∈ {1, 2}` is inherited from TA5's general step-size admission, but only `k₁ = 2` produces an `a` whose computed `h(a)` equals the seed `t₀`... The clause is retained for symmetry with TA5's step-size admission; the operational discipline always begins with `k₁ = 2`."

**Problem**: The prose argues that any chain with `k₁ = 1` violates `t₀ = h(a)` and is therefore inadmissible as a witness. The clause admits `k₁ = 1` but no `k₁ = 1` chain can satisfy the existential — the disjunct is logically vacuous. "Symmetry with TA5's step-size admission" is a stylistic rationale, not a structural one: TA5 admits `k = 1` because `inc(·, 1)` is a real allocator step; L1c's chain-origin equation precludes `k₁ = 1` regardless. Keeping the unreachable disjunct invites confusion (a reader may construct a `k₁ = 1` chain attempt and have to derive its inadmissibility from scratch).

**Required**: Tighten to `k₁ = 2`, and explain in prose that this is the only `k_i = 2` step in any conforming chain (since TA5a's `zeros ≤ 2` precondition can only fire once before `zeros` reaches 3, the element-level terminal value). The "symmetry" rationale is presentational and not load-bearing.

### Issue 5: Worked example does not re-verify state-local invariants at intermediate states Σ_1, Σ_2

**ASN-0043, Worked Example, Steps 1-3**: At each transition, the example verifies the lemma being exercised (L11b at Σ_1, L13 at Σ_2, L3/L6/L8 at arity 4 at Σ_3) plus L12, L12a, L-fin. State-local invariants L0, L1, L1a, L1b, L1c, L3 (at the prior arity), L5, L6, L11a, L14, L14a are verified at the initial state Σ but not at Σ_1, Σ_2, Σ_3.

**Problem**: The L9 and L11b proofs verify each invariant at the constructed Σ' exhaustively (the proof of L9 spans roughly 50 lines of per-invariant verification). The worked example is the second pillar of concrete verification — it instantiates the construction on a specific state. Reading the example, one cannot confirm that, e.g., L1c holds for `a'` at Σ_1 without re-deriving the sibling-chain argument from the L11b proof. A self-contained example would carry through.

**Required**: At Σ_1, add explicit one-line verifications: L0 (subspace check for a'), L1 (zeros(a') = 3 by T10a.8), L1a (home(a') = d ∈ dom(Σ.M)), L1b (#E(a') = #E(a) ≥ 2 by T10a.1 + chain-prefix preservation), L1c (a's chain + 1 sibling step), L11a (a' ≠ a since T10a.7 makes the sibling chain injective), L14a (no new arrangement entries). Repeat at Σ_2 and Σ_3 with one-line confirmations. The total addition is short; the gain is that the example becomes a true state-by-state conformance demonstration.

VERDICT: REVISE
