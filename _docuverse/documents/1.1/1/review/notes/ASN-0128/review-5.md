# Review of ASN-0128

## REVISE

### Issue 1: I1a's step case asserts a false frame for K ~ R deposits
**ASN-0128, I1a (ActiveIdemUniqueness)**: "A `K.λ_sh` deposit of a K-tuple is, by the surface-emitted hypothesis, the miss branch of an `Emit_K`: at the pre-state its I0-class had no active member, so at the post-state it has at most one — the deposit itself, when it lands active rather than born nullified. No tuple changes class post hoc … and the deposit leaves every other class untouched. ∎"

**Problem**: "Leaves every other class untouched" is false in a reachable case the lemma itself covers. Instantiate K = [R] with wrapper-routed history (the lemma's parenthetical explicitly admits this instantiation): a wrapper deposit targeting an R-tuple address `a` — retraction-of-retraction, contemplated outright by R6b — nullifies the tuple at `a`, removing it from *its* I0-class's active membership. That class is touched. The invariant survives because nullification only shrinks a class (at-most-one is preserved by shrinking, the same observation the proof already makes for non-K deposits), but the proof as written asserts an untouched frame instead of making that argument. Showing the common case (K ≁ R, where the frame claim is true) does not establish the K ~ R case.

**Required**: Replace "leaves every other class untouched" with the case split: for K ≁ R the deposit touches no other class; for K ~ R it may nullify a member of another class, which shrinks that class's active membership, and shrinking preserves the at-most-one bound.

### Issue 2: DR's wp equivalence is false without the attainability convention, which this note never declares
**ASN-0128, DR (DisciplineRestoration)**: "for single-tuple scope — the postcondition of ASN-0086's wp Case 1 — the weakest precondition at this surface is the operation's own: `wp(Nullify_Binary(Σ, d_retr, a), {t : a ≼ t} ∩ A_rel^{Σ'} = {a}) ≡ P0 ∧ P-reg ∧ P-tgt`" … "Both branches thus deliver single-tuple scope at the call's post-state … which yields the displayed wp."

**Problem**: The branch derivation establishes sufficiency only; necessity is never argued, and it fails under the plain guarantee reading. Counterexample: `d_retr ∉ dom(Σ.M)` and `a ∈ A_rel^Σ`. The call is rejected — "no step, no address," so `Σ' = Σ` — and the postcondition *holds* at the unchanged state: `{t : a ≼ t} ∩ A_rel^Σ ⊇ {a}` by residence and reflexivity, `⊆ {a}` by R0a's antichain (both sides link addresses). So a P0-violating call attains the postcondition, and the displayed equivalence is wrong as a guarantee-wp. It is correct only under the attainability reading `wp(g → S, R) ≡ g ∧ wp(S, R)` — which ASN-0126's WP lemma explicitly declares "in force" for its own wp, and which this note nowhere declares for DR's. (I6 does not have this problem: its POST mentions the returned address, which a rejected call lacks, so rejection genuinely falsifies POST there. DR's postcondition mentions no returned address, so the convention is load-bearing exactly here.)

**Required**: One sentence declaring the attainability reading in force for DR's wp, plus a necessity argument per precondition under that reading (P-tgt failure genuinely falsifies the postcondition; P0 and P-reg failures falsify the wp by the convention alone).

### Issue 3: The extended-record `Σ_init` is used but never constructed
**ASN-0128, RP(i)**: "ρ(Σ_init) is a well-formed ASN-0126 initial state — C0's clauses (finiteness, key uniqueness, representatives in `T_admissible`) are key-side and untouched, and every projected value is a bare shape."

**Problem**: The proof obligation for (i) is larger than its discharge. ASN-0126's initial state is not just a well-formed registry — its framework constructs `Σ_init` by adjoining the registry to ASN-0086's three initial components, with `π(Σ_init) = Σ_init^{0086}`. For `ρ(Σ_init)` to be an ASN-0126 *initial state*, this note's `Σ_init` must have C/M/L equal to ASN-0086's initial components — and the note never says what its `Σ_init`'s C, M, L are. R-VAL constructs only the registry side ("A declaration set failing any test yields no `Σ_init`"). Meanwhile downstream proofs read the missing definition silently: I1a's base case uses `L_K^{Σ_init} = ∅`, and the entire reachability apparatus (R1, RP(iii)) is anchored at this undefined state.

**Required**: A definitional sentence constructing `Σ_init`: the validated extended-record registry adjoined to ASN-0086's three initial components, altering none of them — after which RP(i)'s discharge is actually complete.

### Issue 4: I0's bounded-loss claim asserts a multi-step identity without derivation
**ASN-0128, I0**: "an address-denoting endset's coverage determines and is determined by its ≼-minimal denoted addresses (the minimal listings are recoverable from the coverage as its ≼-minimal elements; every non-minimal listing's subtree is absorbed into a minimal one's), so what a hit can suppress is exactly the absorbed, non-minimal listings of a redundant presentation"

**Problem**: The parenthetical's central identity — the ≼-minimal elements of the coverage are exactly the ≼-minimal denoted addresses — is a two-directional argument, not an observation, and the note proves nothing in either direction. (⊆): a ≼-minimal coverage element `t` lies in `subtree(r)` for some denoted `r`; `r ∈ coverage` and `r ≼ t` force `t = r` by `t`'s minimality, so `t` is denoted, and minimal among denoted since any denoted `r' ≺ t` would lie in the coverage. (⊇): a ≼-minimal denoted `r` is minimal in the coverage, since any `t ∈ coverage` with `t ≺ r` would have a denoted `r'' ≼ t ≺ r`, contradicting `r`'s minimality among denoted addresses. This identity is load-bearing: it is the entire boundedness argument ("what a hit can suppress is exactly…") by which I0 justifies keeping coverage rather than denoted-set equality as the dedup criterion. Elsewhere the note proves steps of exactly this size (DR's strict-prefix enumeration, D3's equality); here it asserts.

**Required**: The two-direction derivation, inline or as a small lemma, so the "exactly the absorbed, non-minimal listings" conclusion rests on shown work.

### Issue 5: S1 overloads the note's own technical term "active"
**ASN-0128, S1 (Retired)**: "Marks an address as no longer active; the default view on every other type excludes it (BH1's rewrite scope)."

**Problem**: "Active" is this note's technical term (Denotation and views: the active view is `A_K^Σ`), and the sentence states the opposite of the technical truth: a `retired`-marked address's tuples remain in every active subset and in the *active view* — nothing is nullified; only the *default view* changes. The note's own example paragraph exists to correct precisely this misreading ("the original `marker` tuple is still in `A_{marker}^Σ` — nothing nullified it"). A registration entry's one-line description should not require that correction.

**Required**: Reword without the reserved term — e.g., "Marks an address as lifecycle-retired: the default view on every other type excludes it; active subsets are untouched."

## OUT_OF_SCOPE

### Topic 1: Caller-facing rejection signaling
The note fixes rejection's state semantics (no step, no address) for gate failures, invalid-`d` misses, and P-tgt/P0 failures, but not how rejection is communicated — result types, error discrimination between a gate failure and a P-tgt failure, whether a hit is distinguishable from a miss at the return surface.
**Why out of scope**: The state-level commitment is the specification's job and is complete; the reporting channel is interface design for a successor, and any implementation satisfying the no-step/no-address contract conforms.

### Topic 2: Formalizing the serializing authority
I4 places concurrent emits "ahead of" the relation, ordered by "a serializing authority," implicitly assuming each call's dedup read and step execute against the same state.
**Why out of scope**: `→_sh` inherits ASN-0086's sequential model by construction; a concurrency model (atomicity of check-then-step, fairness, ordering) is new machinery, not an error in this note's sequential semantics.

VERDICT: REVISE
