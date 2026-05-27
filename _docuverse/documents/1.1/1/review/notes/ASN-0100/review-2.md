# Review of ASN-0100

## REVISE

### Issue 1: I3 lemma citations don't fit INSERT's post-state

**ASN-0100, "Verifying the Invariants" subsections** cites `I3-S2`, `I3-S3`, `I3-VD`, `I3-VP`, `I3-fin`, `I3-S7` as "transitively discharging" or "discharging" S2, S3★, S8-depth, S8a, finiteness, and S7 for INSERT's post-state.

**Problem**: I3 in ASN-0082 models a *shift-only* post-state. I3-CS (PostInsertionDomainClosureSubspace) explicitly states "(A v : v ∈ dom(M'(d)) ∧ subspace(v) = S : (v < p ∧ v ∈ dom(M(d))) ∨ (E u : ... : v = shift(u, n)))" — every post-state subspace-S position is *either* Left *or* a shift-image. This excludes the Insertion region entirely. I3-V (PostInsertionVacating) confirms this by mandating that pre-state right-region positions not in the shift-image set are vacated. INSERT's post-state has four regions (Left + Insertion + Shifted-right + cross-subspace); I3-S2's verification only ranges over three (shifted, left, cross-subspace) per its own stated reasoning.

**Required**: Either remove these citations entirely (the ASN's explicit verifications already handle the full case) or qualify each citation as "discharging the Left + Shifted-right + cross-subspace portion; the Insertion portion is verified separately." A reader following the citations to ASN-0082 will find that I3-S2 etc. literally do not cover the Insertion positions that distinguish INSERT from a bare shift.

### Issue 2: Uniqueness of substrate decomposition is overstated

**ASN-0100, "Atomicity and Canonical Order"**: "The substrate decomposition above is the unique well-typed sequence, modulo the ordering of independent K.α and K.ρ firings."

**Problem**: Multiple valid decompositions reach the same Σ'. Consider K.μ⁻ retaining `n'_{s_C} = 0` (shrinking the content subspace fully) instead of `n'_{s_C} = p_m − 1`. The intermediate has `V_{s_C}(d_intermediate) = ∅`, satisfying D-CTG★, D-MIN★, D-SEQ★ vacuously. The subsequent K.μ⁺ re-adds the full sequential run `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}` starting from the minimum. K.μ⁺'s precondition requires only "M'(d) satisfies D-CTG★ and D-MIN★" — the new positions need not be at the high end, only the resulting M'(d) must be sequential from min. The post-state is identical.

The ASN's argument against this case — "K.μ⁺ would have to re-add positions in the middle of the Left region... but K.μ⁺'s constraints D-CTG★, D-MIN★ force any new V-position in V_{s_C}(d) to extend the existing sequential run at its high end" — assumes K.μ⁺ extends only at the high end, but the precondition imposes no such restriction.

**Required**: Either drop the uniqueness claim entirely (the specification rests on the post-state Σ', which is unique) or restate it as "the post-state Σ' is uniquely determined; the substrate decomposition that realises it is not". The case analysis in "Atomicity and Canonical Order" should also acknowledge that K.μ⁻ retention parameters are free to range over {0, 1, …, p_m − 1} and K.μ⁺ may be split across multiple firings, provided each intermediate satisfies the per-state invariants.

### Issue 3: SequentialTransitionAxiom doesn't entail composite-level atomicity

**ASN-0100, "Atomicity and Canonical Order"**: "By the SequentialTransitionAxiom of ASN-0093, no other composite can interleave between Σ and Σ'."

**Problem**: SequentialTransitionAxiom (ASN-0093) states that *each transition* is "atomic, uninterruptible" and that "transitions are totally ordered". Each *elementary* transition is atomic. The axiom does not prohibit elementary transitions from *other* composites interleaving between the elementaries of INSERT's composite. ValidComposite★ (ASN-0047) likewise defines composites as finite sequences of atomic transitions; the composite-level atomicity is not enforced by the formalism.

The ASN's earlier framing — "implementations realise the composite via transactional sequencing, locking, copy-on-write, or log-and-commit" — acknowledges that composite atomicity is an implementation concern. The subsequent invocation of SequentialTransitionAxiom contradicts this acknowledgment.

**Required**: Either restate as "no elementary transition of another composite can split an elementary transition of INSERT (by SequentialTransitionAxiom)" — the actual content of the axiom — or move the composite-level atomicity claim to the implementation-concerns open question and remove the SequentialTransitionAxiom citation. The current phrasing overstates what the foundation guarantees.

### Issue 4: K.α and K.ρ commutativity claim is incorrect for K.α among themselves

**ASN-0100, "Atomicity and Canonical Order"**: "modulo the ordering of independent K.α and K.ρ firings (which commute among themselves but not with K.μ⁺ and K.μ⁻)."

**Problem**: K.α firings do *not* commute among themselves. By K.α's allocation discipline in ASN-0093, the k-th K.α firing produces the k-th element of the chain `A_C(d)`. The first firing must produce `[d.0.s_C.1]` (if no prior content with origin d) or `inc(a_prev, 0)`; the second firing must produce `inc(a_0, 0)`; and so on. The chain order is strict — there is no freedom to fire K.α(a_1) before K.α(a_0) because "a_0" is *defined* as the first emission and "a_1" as the second. ChainEnumerationInjectivity (ASN-0093) establishes that the enumeration is strictly increasing, fixing the order.

K.ρ firings *do* commute among themselves and can be interleaved with later K.α firings (K.ρ(a_k, d) only requires a_k ∈ dom(C), so it can fire any time after K.α produces a_k).

**Required**: Restate as "K.α firings have a strict order determined by the chain enumeration of A_C(d); K.ρ firings commute among themselves and may be reordered with respect to K.α firings of strictly higher index, subject only to the per-firing precondition that the recorded a_k must be in dom(C) at the time of K.ρ."

### Issue 5: K.μ⁻ omission rule is conflated across two distinct cases

**ASN-0100, "Substrate Decomposition"** lists the two K.μ⁻ omission cases: "(i) when the pre-state V_{s_C}(d) = ∅ (nothing to retain or shrink); (ii) when p_m = N + 1 (append case)".

**Problem**: Case (i) is sometimes load-bearing because K.μ⁻'s precondition `dom(M(d)) ≠ ∅` fails (when both V_{s_C} and V_{s_L} are empty), and sometimes load-bearing because K.μ⁻'s strict-shrinkage clause `(E S : n'_S < n_S)` cannot be satisfied without shrinking V_{s_L}(d) (when V_{s_C} is empty but V_{s_L} is not). These are distinct preconditions failing for distinct reasons. The ASN treats them as one undifferentiated case.

For an empty V_{s_C}(d) with non-empty V_{s_L}(d), case (i) might mislead a reader into thinking K.μ⁻ is omitted because dom(M(d)) is empty — but dom(M(d)) is not empty in this sub-case. K.μ⁻ is omitted because the only way to satisfy strict shrinkage is to shrink V_{s_L}(d), which would break frame INS.frame.subspace.

**Required**: Split (i) into two sub-cases: (i.a) V_{s_C}(d) = ∅ ∧ V_{s_L}(d) = ∅ — K.μ⁻'s `dom(M(d)) ≠ ∅` precondition fails; (i.b) V_{s_C}(d) = ∅ ∧ V_{s_L}(d) ≠ ∅ — K.μ⁻'s strict-shrinkage clause cannot be satisfied without shrinking V_{s_L}(d), violating the frame.

### Issue 6: Empty-case post-state invariant verifications are stated but not walked through

**ASN-0100, "Sequential text-subspace structure" and "Empty-document first insertion" example**: For the empty pre-state case with V_{s_C}(d) = ∅, the ASN states "post-state V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ n}, satisfying all three predicates with m_C := m" but doesn't walk through the verification.

**Problem**: For the empty case, the verification differs structurally from the non-empty case (no Left, no Shifted-right, no K.μ⁻). The reader has to construct the verification. Specifically:
- D-MIN★ at empty case requires `[s_C, 1, …, 1] of depth m`. The Insertion positions `shift(p, k) = [s_C, 1, …, 1, 1 + k]` (since p_m = 1 for the unique valid first position) have last components {1, …, n}. The minimum is `[s_C, 1, …, 1, 1] = [s_C, 1, …, 1]` (interpreting `1 = p_m + 0`). The verification works but requires care.
- S8-depth's enforcement at `m_C := m` is mentioned but the mechanism — that the first occurrence of `V_{s_C}(d') ≠ ∅` fixes the depth permanently for all subsequent text-subspace operations — could be made explicit.

**Required**: A concrete walk-through of D-MIN★, D-CTG★, D-SEQ★, S8-depth, S8a for the empty case post-state, mirroring the level of detail given for the interior case.

### Issue 7: Cross-document independence verification is brief

**ASN-0100, "Cross-document independence (Q3)"**: Verifies cross-document independence via the frame `(A d' : d' ≠ d : M'(d') = M(d'))` and content preservation, then states "Coupled with L' = L and content-store preservation, this means that any document d' that transcludes content from d continues to map the same V-positions to the same I-addresses, and those I-addresses continue to resolve to the same values."

**Problem**: The verification doesn't address what happens to d''s *projection* of any link, or to discoverability from d'. The projection-shift correspondence section discusses projection changes for the *modified* document d only via the per-document π map. For d' ≠ d, the section says "for d' ≠ d: π is the identity and N_{ℓ,i} = ∅, so project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)" — but this is buried in the projection-shift section, not surfaced in the cross-document independence verification where a reader would look for it. The two sections need to be connected.

**Required**: Cross-reference the projection-shift correspondence to the cross-document independence verification, or state explicitly in the cross-document section that "projection from any d' ≠ d is unchanged by LP4 (ArrangementSpecificity, ASN-0098) applied to the unchanged M'(d') = M(d')." A reader auditing cross-document independence should not have to discover this in a different section.

### Issue 8: Weakest precondition analysis is computed but not labeled

**ASN-0100** does projection-preservation reasoning but does not explicitly compute wp for a non-trivial postcondition.

**Problem**: The review standard asks for wp analysis on non-trivial cases. The ASN's projection-shift correspondence implicitly computes wp for "discoverable_from(ℓ, d, Σ')" given various pre-state conditions, but it never frames the reasoning as wp. For example: `wp(INSERT(d, p, ⟨v⟩), discoverable_from(ℓ, d, ·))` should expand to "discoverable_from(ℓ, d, Σ) OR (E k : a_k ∈ coverage(Σ.L(ℓ).e_i))", which collapses to `discoverable_from(ℓ, d, Σ)` for tight endsets by LP19a — a non-trivial conclusion worth labeling.

**Required**: Add a brief wp section computing wp for at least one non-trivial postcondition — discoverability of a particular link, or P4★ maintenance for a particular I-address — and showing how the pre-state condition follows from the substrate's discipline.

### Issue 9: INS.M-shift discharge by I3 is correctly cited but I3's relationship to INSERT is not delineated

**ASN-0100, claims table for INS.M-shift**: "discharged by I3 (ASN-0082)"

**Problem**: This citation is correct (I3 of ASN-0082 literally states `(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p : shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`, matching INS.M-shift). But the ASN does not explain *why* the I3 lemma — derived in ASN-0082 for a shift-only operation — applies to INSERT's M'(d), which also has Insertion positions. The shift-image positions in I3's M'(d) and in INSERT's M'(d) happen to coincide on Right-region inputs, but a reader cannot derive this from the citation alone.

**Required**: One sentence clarifying that I3's `M'(d)` and INSERT's `M'(d)` agree on the shift-image positions (which are exactly the Shifted-right region) because both operations apply the same shift rule on the Right region, and INSERT additionally introduces Insertion positions disjoint from shift-images. Without this bridge, the citation reads as a hand-wave.

## OUT_OF_SCOPE

### Topic 1: Concurrent INSERTs from independent agents
**Why out of scope**: The open question "concurrent INSERTs targeting the same V-position from independent agents" raises a serialization concern that belongs to a future ASN on concurrency control / serialization order. The present ASN correctly specifies single-INSERT semantics.

### Topic 2: Partial-failure recovery
**Why out of scope**: The open question "what must an implementation provide to recover canonical order after a partial failure during the substrate composite" is about implementation-level transactional guarantees, not substrate semantics. This belongs to a future ASN on durability or to implementation documentation.

### Topic 3: Link subspace insertion via K.μ⁺_L
**Why out of scope**: The ASN explicitly bounds scope to the content subspace. Insertion into the link subspace via K.μ⁺_L has structurally different semantics (single first-arrangement constraint, no shift) and is a separate operation worth its own ASN.

### Topic 4: K.α and K.ρ ordering equivalence classes
**Why out of scope**: A complete enumeration of equivalent substrate decompositions and an algebraic theory of substrate-decomposition equivalence is a separate question that does not impact INSERT's post-state specification. Belongs to a future ASN on composite-decomposition equivalence.

VERDICT: REVISE
