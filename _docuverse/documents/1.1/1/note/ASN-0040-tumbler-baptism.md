# ASN-0040: Tumbler Baptism

*2026-03-15*

We seek to understand what it means for a position to enter the tumbler hierarchy. The algebra (ASN-0034) gives us an infinite space of well-formed addresses — ordered by T1, structured into fields by T4, permanently allocated by T8, strictly increasing by T9. But the algebra cannot distinguish between a position that *has been assigned* and one that merely *could be*. Something marks the transition from arithmetic possibility to system fact.

Nelson calls this transition *baptism*:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers."

Three observations are compressed into that sentence. Baptism is *hierarchical* — it descends level by level through the field structure. Baptism is *sequential* — Nelson elsewhere describes creation as "successive new digits to the right," emphasizing that positions arrive in order, not arbitrarily. And baptism is *permanent* — "Any address, once assigned, remains valid forever." We defer the authorization aspect (who may baptize) to a future ASN on tumbler authorization. Here we characterize the structural mechanism: how the set of baptized positions grows, and what it preserves as it grows.

Gregory's implementation reveals the operational anatomy. Baptism is a two-phase process: first, the system queries the existing address space for the highest allocated position under a given parent prefix and increments to produce a candidate; second, it writes that candidate into the persistent store. The write — not the query — is the moment of baptism. A candidate computed but never written does not exist; if the query were repeated without an intervening write, it would return the same candidate. The address becomes real at the instant of commitment.

We formalize baptism as the growth law of the address space.


## State space and transitions

We work within the foundation's transition framework (ASN-0034, AllocatedSet and NoDeallocation): the *state space* `𝒮`, a closed *transition vocabulary* `Σ` of partial operations, and reachability `→*` as the reflexive-transitive closure of the induced transition relation. A *state* is `s`; this ASN extends each state with the registry component `s.B`. Obligations of the form `(A s, s' : s → s' : …)` constrain every admissible transition; `(A s : s reachable from s_init : I(s))` is a state invariant.

This ASN introduces one state component — the baptismal registry s.B (defined below); the partition of Σ that governs its growth is fixed at B0a. The initial state s_init has s_init.B = B₀, the seed set established at genesis; "reachable" without qualification means reachable from s_init.


## The baptismal registry

We introduce the central state component:

**s.B (BaptismalRegistry).** s.B ⊆ T — the set of baptized tumblers.

A tumbler t is *baptized* iff t ∈ s.B. Initially s.B contains a finite seed set B₀ ⊆ T of root addresses established at system genesis, subject to the conformance requirement stated at B₀ conf. below. Thereafter it grows monotonically.

**B0a (Baptismal Closure).** Σ partitions into two classes whose treatment of the s.B component is fixed:

  - *Baptismal operations.* For each (p, d) satisfying B6 (Valid Depth, below), `baptize(p, d) ∈ Σ` is the operation specified by Bop below; its action on the registry is `op(s).B = s.B ∪ {next(s.B, p, d)}`.
  - *s.B-frame operations.* Every other `op ∈ Σ` preserves the registry: `(A op ∈ Σ \ {baptize(p, d) : B6(p, d)}, s ∈ dom(op) : op(s).B = s.B)`.

Irrevocability follows immediately:

**B0 (Irrevocability — corollary of B0a).** `(A s, s' : s → s' : s.B ⊆ s'.B)`. In the baptismal branch `op(s).B = s.B ∪ {next(s.B, p, d)}` and in the s.B-frame branch `op(s).B = s.B`, so `s.B ⊆ op(s).B` in both, hence `s.B ⊆ s'.B` for every transition. Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid."

B0 is a single-step law. We extend it to finite transition sequences:

**B0★ (Multi-step Irrevocability — corollary of B0).** `(A s, s' : s →* s' : s.B ⊆ s'.B)`, where s →* s' denotes the reflexive-transitive closure of the transition relation — that is, s' is reachable from s by a finite (possibly empty) sequence of transitions.

*Proof.* B0 makes `s ↦ s.B` monotone under single transitions, and monotonicity transfers to the reflexive-transitive closure by chaining ⊆ along the witnessing sequence. ∎

**B0b (Transition Dichotomy — restatement of B0a at the transition level).** Every transition `s → s'` is either *s.B-frame* (`s'.B = s.B`) or *baptismal* (`s'.B = s.B ∪ {next(s.B, p, d)}` for some B6-valid (p, d)) — the two cases of B0a's partition, read on a single edge.

The binary character of this state is fundamental. Nelson's model has no third status between baptized and unbaptized: "the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." A position is either conceptually assigned (in B) or not. Whether anything is *stored* at that position is a separate question, which we address below as the ghost validity property.


## The sibling stream

Consider a parent address p ∈ T and a baptismal depth d ≥ 1. From TA5, `inc(p, d)` produces a tumbler strictly greater than p that extends p by d components: d − 1 zero separators followed by 1. This is the *first child* of p at depth d. Repeated sibling increments yield a counting sequence:

  c₁ = inc(p, d)

  cₙ₊₁ = inc(cₙ, 0)    for n ≥ 1

**S(p,d) (SiblingStream).** We call the sequence c₁, c₂, c₃, ... the *sibling stream* of p at depth d, written S(p, d). By TA5(c), each sibling increment preserves the tumbler's length and advances only the last significant component by 1. Every element of S(p, d) has the form [p₁, ..., p_{#p}, 0, ..., 0, n] — the parent's components, then d − 1 zeros, then the ordinal n. We establish this canonical form and the uniform length #cₙ = #p + d by induction (the strict ordering is proved separately at S0 below):

*Proof.* We must show that every element cₙ of S(p, d) has the form [p₁, ..., p_{#p}, 0, ..., 0, n] — the parent's first #p components, then d − 1 zeros, then ordinal n — with uniform length #cₙ = #p + d. The argument proceeds by induction on n.

*Base case (n = 1).* c₁ = inc(p, d) with d ≥ 1. By TA5(d) (ASN-0034), c₁ has length #p + d: the first #p components are preserved from p (TA5(b)), the next d − 1 positions #p + 1 through #p + d − 1 are zero-valued field separators, and the final position #p + d has value 1. This is exactly [p₁, ..., p_{#p}, 0, ..., 0, 1] with d − 1 zeros and ordinal 1.

*Inductive step.* Assume cₙ = [p₁, ..., p_{#p}, 0, ..., 0, n] with d − 1 zeros and #cₙ = #p + d for some n ≥ 1. Since n ≥ 1, position #p + d holds value n > 0, so sig(cₙ) = #p + d — the ordinal position is the last significant component. Consider cₙ₊₁ = inc(cₙ, 0). By TA5(c), cₙ₊₁ has the same length as cₙ (#cₙ₊₁ = #p + d) and differs from cₙ only at position sig(cₙ) = #p + d, where cₙ₊₁ at that position equals n + 1. All other positions are unchanged: the first #p components remain p₁, ..., p_{#p} (since every position i ≤ #p satisfies i < sig(cₙ) = #p + d), and the d − 1 zeros at positions #p + 1 through #p + d − 1 remain zero (since each such position j satisfies j < #p + d = sig(cₙ)). Therefore cₙ₊₁ = [p₁, ..., p_{#p}, 0, ..., 0, n + 1], the claimed form with ordinal n + 1. ∎

*Formal Contract:*
- *Definition:* S(p, d) = c₁, c₂, c₃, ... where c₁ = inc(p, d) and cₙ₊₁ = inc(cₙ, 0) for n ≥ 1.
- *Preconditions:* p ∈ T, d ≥ 1.
- *Postconditions:* `(A n ≥ 1 : cₙ = [p₁, ..., p_{#p}, 0, ..., 0, n])` with d − 1 zeros, `#cₙ = #p + d`, `sig(cₙ) = #p + d`, and `cₙᵢ = pᵢ` for `1 ≤ i ≤ #p`. (The sig identity holds because the ordinal n ≥ 1 occupies the final position #p + d, which is therefore the rightmost nonzero component.)
- *Axiom:* TA5(b) (prefix preservation), TA5(c) (sibling structure), TA5(d) (child structure).

**S0 (StreamOrdering).** `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)`.

*Proof.* We derive the strict ordering directly from the per-step increase of inc(·, 0). For each n ≥ 1, cₙ₊₁ = inc(cₙ, 0), and TA5(a) gives inc(cₙ, 0) > cₙ, so cₙ < cₙ₊₁. To extend this to arbitrary indices i < j, fix i and induct on j. *Base case (j = i + 1):* cᵢ < cᵢ₊₁ is the per-step increase just established. *Inductive step:* assume cᵢ < cⱼ; the per-step increase gives cⱼ < cⱼ₊₁, and T1's transitivity (c) gives cᵢ < cⱼ₊₁. By induction, cᵢ < cⱼ for every j > i. The base c₁ = inc(p, d) ∈ T (TA5(d)) and each cₙ ∈ T (TA5(c)) supply the well-formed operands these comparisons require; no T4-validity of the base is needed. ∎

*Formal Contract:*
- *Preconditions:* p ∈ T, d ≥ 1. S(p, d) = c₁, c₂, ... defined by c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0).
- *Postconditions:* `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)` — the sibling stream is strictly increasing.
- *Axiom:* TA5(a) — per-step strict increase of inc(·, 0); T1 transitivity (c) and irreflexivity (a).

**S1 (StreamPrefix).** `(A n : n ≥ 1 : p ≼ cₙ)` — every stream element extends p as a prefix.

*Proof.* `p ≼ cₙ` is immediate from S(p,d)'s postconditions `#cₙ = #p + d ≥ #p` (since d ≥ 1) and `cₙᵢ = pᵢ` for `1 ≤ i ≤ #p`, by the Prefix definition (ASN-0034). ∎

*Formal Contract:*
- *Relation:* `≼` is the foundation Prefix relation (Prefix, ASN-0034).
- *Preconditions:* p ∈ T, d ≥ 1. S(p, d) = c₁, c₂, ... defined by c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0).
- *Postconditions:* `(A n : n ≥ 1 : p ≼ cₙ)` — every stream element extends p as a prefix.

As a consequence, since every cₙ extends p, the entire stream lies within the set {t ∈ T : p ≼ t}, which forms a contiguous interval under T1 by T5 (ContiguousSubtrees).

Nelson describes exactly this process: "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." The word "successive" is precise — positions arrive in order, c₁ before c₂ before c₃. "Items 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." The stream is traversed monotonically, not sampled.

One structural identity of the stream construction relates a depth-1 stream under a trailing-zero parent to a depth-2 stream under its truncation: a parent ending in a trailing zero generates the same stream at depth 1 as its truncation does at depth 2.

**S2 (Trailing-Zero Stream Identity).** Let p ∈ T with #p ≥ 2 and p_{#p} = 0, and let p′ be p with its final component removed (#p′ = #p − 1 ≥ 1, p′ᵢ = pᵢ for 1 ≤ i ≤ #p − 1). The length bound #p ≥ 2 guarantees p′ ∈ T (T0 requires #p′ ≥ 1); it excludes only the singleton p = [0], which violates T4 in any case. Then S(p, 1) = S(p′, 2).

*Proof.* The first element of S(p, 1) is c₁ = inc(p, 1); by TA5(d) with d − 1 = 0 intermediate zeros, c₁ has length #p + 1 with positions 1 through #p preserved from p and position #p + 1 set to 1, so c₁ = [p₁, ..., p_{#p−1}, 0, 1] (using p_{#p} = 0). The first element of S(p′, 2) is c′₁ = inc(p′, 2); by TA5(d) with one intermediate zero, c′₁ has length #p′ + 2 = #p + 1 with positions 1 through #p′ = #p − 1 preserved from p′, position #p′ + 1 = #p set to 0 (the separator), and position #p′ + 2 = #p + 1 set to 1, so c′₁ = [p₁, ..., p_{#p−1}, 0, 1]. Component-by-component, c₁ = c′₁. Both streams share the deterministic recurrence cₙ₊₁ = inc(cₙ, 0), so they coincide: S(p, 1) = S(p′, 2). ∎

*Formal Contract:*
- *Preconditions:* p ∈ T, #p ≥ 2, p_{#p} = 0; p′ = [p₁, ..., p_{#p−1}] (so p′ ∈ T).
- *Postconditions:* S(p, 1) = S(p′, 2).
- *Axiom:* TA5(d) (child structure), deterministic stream recurrence.


## Depth and field structure

Baptism interacts with the field hierarchy through the depth parameter. Recall from ASN-0034 that zeros(t) — the count of zero-valued components — determines the hierarchical level: 0 for node, 1 for user, 2 for document, 3 for element. When baptism crosses from one level to the next, it must introduce a new zero separator.

**B5 (Field Advancement).** `zeros(inc(p, d)) = zeros(p) + (d − 1)`.

For d = 1: zeros is preserved — the child is at the same hierarchical level. For d = 2: zeros advances by 1 — the child descends one level.

*Proof.* We must show that for a tumbler p and depth d ≥ 1, the zero count of inc(p, d) equals zeros(p) + (d − 1). Let t' = inc(p, d). Since d ≥ 1, TA5(d) applies: t' has length #p + d, with the first #p components preserved from p (TA5(b)), d − 1 zero-valued components at positions #p + 1 through #p + d − 1, and a final component of value 1 at position #p + d.

We partition the components of t' into three ranges and count zeros in each. Positions 1 through #p are identical to the corresponding components of p by TA5(b), contributing exactly zeros(p) zero-valued components. Positions #p + 1 through #p + d − 1 are the field separators introduced by the increment — there are d − 1 of them, each zero-valued, contributing d − 1 zeros. (When d = 1 this range is empty, contributing none; when d = 2 it contains exactly one zero.) Position #p + d holds value 1, contributing no zeros.

Since these three ranges exhaust all #p + d positions of t', the total zero count is zeros(t') = zeros(p) + (d − 1) + 0 = zeros(p) + (d − 1). ∎

*Formal Contract:*
- *Preconditions:* p ∈ T with d ≥ 1. (In the baptismal context, d ∈ {1, 2} by B6(ii).)
- *Postconditions:* `zeros(inc(p, d)) = zeros(p) + (d − 1)`.

B5 establishes the zeros count for the *first* child c₁ of a stream. The sibling stream preserves it:

**B5a (Sibling Zeros Preservation).** `(A t : t_{sig(t)} > 0 : zeros(inc(t, 0)) = zeros(t))`

*Proof.* We must show that for any tumbler t with t_{sig(t)} > 0, the zero count of inc(t, 0) equals zeros(t). Let t' = inc(t, 0). By TA5(c), t' has the same length as t (#t' = #t) and differs from t only at position sig(t), where t'_{sig(t)} = t_{sig(t)} + 1. At every other position, t'_i = t_i.

We count zeros in t' by comparing each component with the corresponding component of t. At every position i ≠ sig(t), t'_i = t_i, so position i is zero-valued in t' exactly when it is zero-valued in t — these positions contribute identically to both zeros(t') and zeros(t). At position sig(t), the precondition gives t_{sig(t)} > 0, so this position contributes no zero to zeros(t). After the increment, t'_{sig(t)} = t_{sig(t)} + 1 ≥ 2 > 0, so this position contributes no zero to zeros(t') either. Since every position contributes identically to both zero counts, zeros(t') = zeros(t). ∎

*Formal Contract:*
- *Preconditions:* t ∈ T with t_{sig(t)} > 0.
- *Postconditions:* `zeros(inc(t, 0)) = zeros(t)`.

To apply B5a across the sibling stream S(p, d), we discharge its precondition: every cₙ satisfies cₙ_{sig(cₙ)} > 0. By S(p, d), sig(cₙ) = #p + d and (cₙ)_{#p+d} = n ≥ 1 > 0, so every stream element satisfies the precondition. Combined with B5, every element of S(p, d) inherits the zeros count established at c₁:

  `(A n ≥ 1 : zeros(cₙ) = zeros(p) + (d − 1))`

The B6 validity table below depends on this uniformity — all elements in a stream share the same hierarchical level.

This deserves attention. The `.0.` that appears in addresses like `1.1.0.1.0.1` is not a syntactic convention imposed by a parser — it is a *consequence* of baptism at depth 2. When inc(p, 2) extends p by two components, the first is zero (the field separator, from TA5(d)'s d − 1 = 1 intermediate zero) and the second is 1 (the first child's ordinal). The field structure of tumblers is *produced* by baptism arithmetic.

**B6 (Valid Depth).** Baptism at depth d from parent p is valid when:

  (i) p satisfies T4,

  (ii) d ∈ {1, 2}, and

  (iii) zeros(p) + (d − 1) ≤ 3.

Conditions (ii) and (iii) are necessary and sufficient for T4 preservation of the sibling stream, given (i). Condition (i) is necessary for T4 except at the d = 1 trailing-zero case, where it is retained for injectivity rather than T4 (necessity sub-case (b) below). Condition (ii) follows from the ASN-0034 lemma "TA5 preserves T4": for d ≥ 3, the appended sequence contains adjacent zeros, violating T4's non-empty-field constraint. Condition (iii) ensures no address exceeds the four-level hierarchy. Together:

| Parent level | d = 1 (same level) | d = 2 (level crossing) |
|---|---|---|
| Node (zeros = 0) | node child | user child |
| User (zeros = 1) | user child | document child |
| Document (zeros = 2) | sub-document / version | element child |
| Element (zeros = 3) | sub-element | **invalid** |

At most three level crossings can occur in a valid address chain: node → user, user → document, document → element. This is the four-field structure of T4, now visible as a consequence of baptism depth arithmetic rather than an independent syntactic constraint.

*Proof.* We prove sufficiency (all three conditions imply T4 preservation) and then necessity (violating any single condition either produces a T4 violation in the stream or collapses namespace disjointness).

**(⟸) Sufficiency.** Assume (i) p satisfies T4, (ii) d ∈ {1, 2}, and (iii) zeros(p) + (d − 1) ≤ 3. We show every element of S(p, d) satisfies T4.

For the first child c₁ = inc(p, d): TA5a (IncrementPreservesT4, ASN-0034) states that for any t satisfying T4, inc(t, k) satisfies T4 iff `k = 0`, or `k = 1 ∧ zeros(t) ≤ 3`, or `k = 2 ∧ zeros(t) ≤ 2`. With t = p and k = d, conditions (i) and (ii) make p T4-valid and put d ∈ {1, 2}. For d = 1, the first child is c₁ = inc(p, 1), i.e. k = 1, which TA5a conditions on zeros(p) ≤ 3; this is discharged by T4-validity of p (T4 permits at most three zeros), the same bound that condition (iii) reduces to at d = 1. For d = 2, TA5a's `k = 2 ∧ zeros(t) ≤ 2` branch requires zeros(p) ≤ 2, which is exactly condition (iii) specialized to d = 2. The TA5a case applicable at the chosen d is therefore satisfied, so c₁ satisfies T4.

For subsequent siblings cₙ₊₁ = inc(cₙ, 0): TA5a's `k = 0` case states that inc(t, 0) satisfies T4 for any T4-valid t with no further constraint — sibling increment modifies only position sig(t), advancing a positive value by one (TA5(c)), so no zeros are added and no new adjacencies are introduced. Since c₁ satisfies T4, and each sibling increment preserves T4, by induction every cₙ satisfies T4.

**(⟹) Necessity.** We show that violating condition (i), (ii), or (iii) produces a T4 violation in the stream, with one exception: the d = 1 trailing-zero case is the S2 exception.

*Condition (ii) is necessary for T4.* Let d ≥ 3. By TA5(d), inc(p, d) appends d − 1 ≥ 2 zeros followed by 1. Positions #p + 1 and #p + 2 are both zero — adjacent zeros that parse as two consecutive field separators enclosing an empty field, violating T4's non-empty-field constraint. No choice of p avoids this: the adjacent zeros lie in the appended suffix, independent of p's content.

*Condition (iii) is independently necessary at d = 2.* Let zeros(p) + (d − 1) > 3 with p satisfying T4. By B5, zeros(c₁) = zeros(p) + (d − 1) > 3. But T4 requires zeros(t) ≤ 3 for any valid address — at most three field separators for the four-level hierarchy. The first child already exceeds the zero budget, so c₁ violates T4. This bites independently only at d = 2, where condition (iii) reads zeros(p) ≤ 2 — a strictly stronger constraint than T4 alone permits for p (which allows zeros(p) ≤ 3). At d = 1, condition (iii) reduces to zeros(p) ≤ 3, which is already implied by condition (i) (T4-validity of p); there it adds nothing and is subsumed by (i) rather than independent.

*Condition (i) is necessary for the system.* Let p violate T4 with d ∈ {1, 2}. A T4 violation is the failure of at least one of T4's four clauses: the zero-count bound zeros(t) ≤ 3, the no-adjacent-zeros constraint, the leading-component constraint t₁ ≠ 0, and the trailing-component constraint t_{#t} ≠ 0. We partition exhaustively over these clauses. If p violates the count bound (zeros(p) > 3), or has a defect among the positions preserved into c₁ by TA5(b) — the leading position when p₁ = 0 (which coincides with the trailing position #p only in the singleton case p = [0]), or an interior adjacent-zero defect at positions 1 through #p − 1 — then p falls in sub-case (a) below. Otherwise p's only defect is a clean trailing zero with p₁ > 0 and zeros(p) ≤ 3, and p falls in sub-case (b). These exhaust the four clauses: count failures and any leading or interior failure route to (a), and a trailing-only failure routes to (b).

*(a) Count violation or defect in p's preserved prefix: zeros(p) > 3, or some T4 defect at positions 1 through #p − 1 of p, or p₁ = 0 (the leading-zero case, including the singleton p = [0] in which leading and trailing positions coincide).* By TA5(b), inc(p, d) preserves positions 1 through #p. For a positional defect (leading or interior), each defective position of p survives unchanged into c₁ at the same index. Each subsequent cₙ₊₁ = inc(cₙ, 0) modifies only position sig(cₙ) = #p + d > #p (since d ≥ 1), leaving positions 1 through #p untouched. By induction, every stream element carries the defect. For example, with p = [0, 1, 2] (leading zero, #p = 3): c₁ = inc([0, 1, 2], 1) = [0, 1, 2, 1], and (cₙ)₁ = 0 for all n ≥ 1, violating T4's t₁ ≠ 0 requirement. For the singleton p = [0] (in which p₁ = p_{#p} = 0): with d = 1, c₁ = inc([0], 1) = [0, 1] and each cₙ = [0, n] violates t₁ ≠ 0; with d = 2, c₁ = inc([0], 2) = [0, 0, 1] preserves (cₙ)₁ = 0 from p for every n. For a count violation (zeros(p) > 3, with no single position individually defective — e.g. p = [1, 0, 1, 0, 1, 0, 1, 0, 1], four non-adjacent interior zeros), the propagation is by zero count rather than by a fixed position: TA5(b) preserves all of p's positions into c₁, so c₁ carries every zero of p plus the d − 1 ≥ 0 separators TA5(d) inserts, giving zeros(c₁) = zeros(p) + (d − 1) ≥ zeros(p) > 3 (B5). Sibling increments add no zeros — by B5a, zeros(cₙ) = zeros(c₁) for every n ≥ 1, since sibling increment advances only the positive ordinal at sig(cₙ) — so every stream element has zeros(cₙ) > 3, violating T4's zeros(t) ≤ 3 clause throughout the stream.

*(b) Pure trailing zero as the sole T4 defect: p_{#p} = 0, p₁ > 0, zeros(p) ≤ 3, no adjacent zeros in p (which forces #p ≥ 2, since p₁ > 0 = p_{#p} requires the leading and trailing positions to be distinct).* The load-bearing case for T4-necessity is d = 2. At d = 1 the stream is *not* T4-defective — by S2, a pure-trailing-zero parent p at d = 1 generates the same fully T4-valid stream as the B6-valid namespace obtained by dropping p's trailing zero and incrementing the depth (e.g. ([1, 0], 1) and ([1], 2) share the stream [1, 0, n]). Condition (i) excludes such parents here not to avoid a T4 violation but to keep the namespace map injective: were ([1, 0], 1) admitted, two distinct namespaces would share their entire stream. This is the sole point where (i) is retained beyond what T4 alone forces.

When d = 2, every stream element violates T4 — by a propagation argument structurally distinct from sub-case (a). The defect does not preexist in p's interior; it arises within c₁ itself from the union of p's trailing zero and the separator TA5(d) inserts. By TA5(b), c₁ preserves positions 1 through #p of p, so (c₁)_{#p} = p_{#p} = 0. By TA5(d) with d = 2, c₁ has length #p + 2 and the intermediate position #p + 1 holds the field separator with value 0. Therefore (c₁)_{#p} = 0 and (c₁)_{#p+1} = 0 — adjacent zeros at positions #p and #p + 1 of c₁, violating T4's non-empty-field constraint (T4(ii) at i = #p). To propagate this to every cₙ, we show position #p + 1 is never modified by sibling increments. By S(p, 2), sig(cₙ) = #p + 2 for all n ≥ 1, and position #p + 1 satisfies #p + 1 < #p + 2 = sig(cₙ), so it is invariant across the stream (TA5(c) modifies only sig(cₙ)). Hence (cₙ)_{#p} = 0 and (cₙ)_{#p+1} = 0 for every n ≥ 1, and every stream element carries the same adjacent-zero violation as c₁.

Condition (i) is therefore necessary for T4 preservation: a count violation (zeros(p) > 3) and T4 defects in p's preserved prefix — interior, leading, or the singleton p = [0] — propagate to every stream element via TA5(b) and B5/B5a (sub-case (a)), and a pure trailing zero at d = 2 creates adjacent zeros within c₁ that propagate to the whole stream (sub-case (b)). The four T4 clauses are thereby exhausted. ∎

*Formal Contract:*
- *Preconditions:* p ∈ T, d ∈ ℕ with d ≥ 1.
- *Postconditions:* (a) Sufficiency: `(p satisfies T4 ∧ d ∈ {1, 2} ∧ zeros(p) + (d − 1) ≤ 3) ⟹ (A n ≥ 1 : cₙ ∈ S(p, d) satisfies T4)`. (b) Necessity: violating a binding condition forces a T4 violation; the sole exception is the d = 1 trailing-zero case, where (i) is retained for injectivity (S2) rather than for T4.


## Namespace disjointness

Each parent-depth pair defines a namespace. Distinct namespaces must produce non-overlapping address ranges, or global uniqueness collapses.

**B7 (Namespace Disjointness).** For distinct valid pairs (p, d) ≠ (p', d'):

  S(p, d) ∩ S(p', d') = ∅

provided both `(p, d)` and `(p', d')` satisfy B6.

*Proof.* We prove disjointness directly from the canonical stream form (S(p,d), S1) and the field-segment constraint (T4). By S(p, d), every element of S(p, d) has length #p + d, extends p as a prefix (S1), and carries d − 1 zero separators at positions #p + 1 … #p + d − 1; symmetrically for S(p', d'). Suppose for contradiction some address a ∈ S(p, d) ∩ S(p', d').

*Length split.* If #p + d ≠ #p' + d', then a would have two distinct lengths — impossible by T3 (CanonicalRepresentation), since a tumbler has a single length. So #p + d = #p' + d' = L, and a has length L under both forms.

*Equal-length parents.* If #p = #p', then p ≼ a from S(p, d) (S1) and p' ≼ a from S(p', d') make both p and p' the length-#p prefix of a; by T3 they agree componentwise, so p = p'. With #p + d = #p' + d' this forces d = d', hence (p, d) = (p', d'), contradicting distinctness.

*Unequal-length parents.* Otherwise #p ≠ #p'; from #p + d = #p' + d' with d, d' ∈ {1, 2} the lengths can differ by at most 1, so WLOG #p < #p' with #p' = #p + 1, d = 2, d' = 1. Read position #p + 1 of a two ways. From the S(p, 2) form, position #p + 1 is the lone zero separator: a_{#p+1} = 0. From the S(p', 1) form (d' = 1, no separator), positions 1 … #p' = 1 … #p + 1 are preserved from p', so a_{#p+1} = p'_{#p+1} = p'_{#p'} — the last component of p'. Since (p', d') satisfies B6, p' satisfies T4, whose field-segment constraint forbids a zero final component (TA5-SigValid: p'_{#p'} ≠ 0). Thus a_{#p+1} > 0, contradicting a_{#p+1} = 0.

Every case yields a contradiction, so S(p, d) ∩ S(p', d') = ∅. ∎

*Formal Contract:*
- *Preconditions:* (p, d) and (p', d') both satisfy B6, with (p, d) ≠ (p', d').
- *Postconditions:* `S(p, d) ∩ S(p', d') = ∅`.
- *Depends:* S(p,d) (canonical stream form and length #p + d), S1 (every element extends p), T3 (CanonicalRepresentation — a tumbler has a single length, and componentwise prefix agreement forces parent equality), T4 / TA5-SigValid (valid addresses have a nonzero last component, via B6(i)), TA5(d) (child increment, fixing the separator positions).


## Seed conformance and registry finiteness

The invariant proofs that follow induct over transition sequences from the initial state. They require a conforming seed and a finiteness guarantee that each transition preserves.

**B₀ conf. (SeedConformance).** B₀ is finite, `(A p, d : children(B₀, p, d) is a contiguous prefix of S(p, d))`, and `(A t ∈ B₀ : t satisfies T4)`.

Non-emptiness is not among them; this ASN neither requires nor establishes it.

B₀ conformance fixes the seed as a finite set; B0a constrains every transition to add at most one element. The composition yields a registry-wide finiteness invariant:

**B_fin (Registry Finiteness).** `(A s : s reachable from s_init : s.B is finite)`.

*Proof.* By induction on the number of state transitions from the initial state.

*Base case.* In the initial state, s.B = B₀. By B₀ conf. (SeedConformance), B₀ is finite. The invariant holds at genesis.

*Inductive step.* Assume s.B is finite for state s with registry B. By B0b (Transition Dichotomy), a transition s → s' either leaves B' = B (finite by the inductive hypothesis) or sets B' = B ∪ {a} for a single new element a — a finite set plus a singleton, hence finite. By induction, s.B is finite in every reachable state. ∎

*Formal Contract:*
- *Invariant:* `(A s : s reachable from s_init : s.B is finite)`.
- *Base:* B₀ conf. — B₀ is finite.
- *Preservation:* B0b — every transition either leaves s.B unchanged or replaces it by its union with a single element (a finite set unioned with a singleton is finite).


## Children and the next address

We define the *children* of parent p at depth d in state B:

  children(B, p, d) = B ∩ S(p, d)

— the baptized addresses that belong to the sibling stream. The next address in a namespace is determined by the current registry state:

**next(B,p,d) (NextAddress).**

  next(B, p, d) = if children(B, p, d) = ∅ then inc(p, d) else inc(max(children(B, p, d)), 0)

— find the greatest baptized sibling and produce its immediate successor; if none exists, produce the first child.

*Justification of well-definedness.* When children(B, p, d) = ∅ the result is inc(p, d); otherwise children(B, p, d) is a non-empty finite subset of T (finite by B_fin), which T1 totally orders, so its max exists. Both branches land in T by TA5 (TA5(d) for inc(p, d), TA5(c) for inc(max(...), 0)), so next is total on its domain. ∎

*Formal Contract:*
- *Definition:* next(B, p, d) = if children(B, p, d) = ∅ then inc(p, d) else inc(max(children(B, p, d)), 0), where children(B, p, d) = B ∩ S(p, d).
- *Preconditions:* B ⊆ T finite (discharged by B_fin when B = s.B for a reachable s); p ∈ T; d ≥ 1; S(p, d) defined.
- *Postconditions:* next(B, p, d) ∈ T — the result is a valid tumbler.
- *Axiom:* TA5(c) (sibling increment well-definedness), TA5(d) (child increment well-definedness), T1 (total order guarantees max exists).


## The contiguous prefix property

We claim that children(B, p, d) is always a *prefix* of the sibling stream: the first m elements for some m ≥ 0, with no gaps.

**B1 (Contiguous Prefix).** `(A p, d : B6(p, d) : (A n : n ≥ 1 ∧ cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B)))`.

Equivalently: for every B6-valid namespace (p, d), children(B, p, d) = {c₁, ..., cₘ} for some m ≥ 0.

*Proof.* We must show that in every state reachable from a conforming seed B₀, for every B6-valid namespace (p, d), children(s.B, p, d) is a contiguous prefix of S(p, d). The argument proceeds by induction on the number of state transitions from the initial state.

*Base case.* In the initial state, s.B = B₀. By B₀ conf. (SeedConformance), children(B₀, p, d) is a contiguous prefix of S(p, d) for every (p, d). B1 holds at genesis.

*Inductive step.* Assume B1 holds for state s with registry B. By B0b (Transition Dichotomy), a transition s → s' is either s.B-frame — then B' = B and B1 holds at B' immediately by the inductive hypothesis — or baptismal, the case we now treat.

*Baptismal transition.* By B0b, a baptismal transition sets B' = B ∪ {a} where a = next(B, p₀, d₀) for some (p₀, d₀) satisfying B6; the union shape is fixed by B0b, not by the operation spec stated later. We must show that children(B', p, d) is a contiguous prefix of S(p, d) for every B6-valid (p, d). Two cases exhaust the possibilities.

*Target namespace: (p, d) = (p₀, d₀).* By the inductive hypothesis, children(B, p₀, d₀) = {c₁, ..., cₘ} for some m ≥ 0. Two sub-cases arise from the definition of next (NextAddress).

When m = 0: children(B, p₀, d₀) = ∅, so a = next(B, p₀, d₀) = inc(p₀, d₀) = c₁, the first element of S(p₀, d₀) by the definition of the sibling stream. Therefore children(B', p₀, d₀) = {c₁}, a contiguous prefix of length 1.

When m ≥ 1: the maximum of children(B, p₀, d₀) is cₘ, since the prefix {c₁, ..., cₘ} is strictly ordered by S0 (StreamOrdering). The definition of next gives a = inc(cₘ, 0), which is exactly c_{m+1} by the sibling-stream recurrence. By B0 (Irrevocability), B ⊆ B', so {c₁, ..., cₘ} ⊆ B'. Together with the new element c_{m+1} ∈ B', we obtain children(B', p₀, d₀) = {c₁, ..., cₘ, c_{m+1}}, a contiguous prefix of length m + 1.

*All other B6-valid namespaces: (p, d) ≠ (p₀, d₀) with (p, d) satisfying B6.* Both (p₀, d₀) and (p, d) meet B7's preconditions, so B7 gives S(p₀, d₀) ∩ S(p, d) = ∅, hence a ∉ S(p, d). Therefore children(B', p, d) = children(B, p, d), a contiguous prefix by the inductive hypothesis.

In both the target namespace and every other B6-valid namespace, children(B', p, d) is a contiguous prefix of S(p, d).

Since B1 is preserved in the target namespace and in every other B6-valid namespace, B1 holds for B' under baptismal transitions; the s.B-frame case was dispatched above via B0b. By induction on the transition sequence, B1 holds in every reachable state. ∎

*Formal Contract:*
- *Invariant:* `(A p, d : B6(p, d) : (A n : n ≥ 1 ∧ cₙ ∈ s.B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ s.B)))` — equivalently, for every B6-valid (p, d), children(s.B, p, d) = {c₁, ..., cₘ} for some m ≥ 0.
- *Base:* B₀ conf. — seed set satisfies contiguous prefix for all (p, d), a fortiori for every B6-valid (p, d).
- *Preservation:* Each baptismal transition preserves B1 in the target namespace (by B0b, B0, S0, TA5(c), and the next definition) and in every other B6-valid namespace (by B7).

From B₀ conformance (T4 for seeds) and B6(i) (T4 for parents), we derive by induction on the baptism sequence that T4 validity is a registry-wide invariant:

**B10 (T4ValidityInvariant).** `(A t ∈ s.B : t satisfies T4)`

*Proof.* We must show that in every state reachable from a conforming seed B₀, every element of s.B satisfies T4 (FieldSeparatorConstraint, ASN-0034). The argument proceeds by induction on the number of state transitions from the initial state.

*Base case.* In the initial state, s.B = B₀. By B₀ conf. (SeedConformance), every t ∈ B₀ satisfies T4. The invariant holds at genesis.

*Inductive step.* Assume B10 holds for state s with registry B — every t ∈ B satisfies T4. By B0b (Transition Dichotomy), a transition s → s' is either s.B-frame — then B' = B and B10 holds at B' immediately by the inductive hypothesis — or baptismal, the case we now treat.

*Baptismal transition.* By B0b, the transition sets B' = B ∪ {a} where a = next(B, p, d) for some (p, d) satisfying B6. We must show every t ∈ B' satisfies T4. For elements t ∈ B, the inductive hypothesis gives t satisfies T4 directly. It remains to show the new element a satisfies T4.

By the definition of next (NextAddress), a = next(B, p, d) is a stream element of S(p, d): the first child a = inc(p, d) = c₁ when children(B, p, d) = ∅, and the sibling a = inc(cⱼ, 0) = c_{j+1} ∈ S(p, d) otherwise, where cⱼ = max(children(B, p, d)) (the maximum exists because B is finite by B_fin and T1 totally orders the non-empty finite set children(B, p, d) ⊆ B). Since (p, d) satisfies B6, B6's sufficiency result (§B6) gives that every element of S(p, d) satisfies T4; in particular a does.

So a satisfies T4. With every element of B satisfying T4 by the inductive hypothesis, every element of B' = B ∪ {a} satisfies T4; the s.B-frame case was dispatched above via B0b. By induction on the transition sequence, B10 holds in every reachable state. ∎

*Formal Contract:*
- *Invariant:* `(A t ∈ s.B : t satisfies T4)` — every baptized address satisfies FieldSeparatorConstraint. *Corollary:* `s.B ⊆ T`, since T4-validity entails t ∈ T.
- *Base:* B₀ conf. — every seed element satisfies T4.
- *Preservation:* Each baptismal transition adds a = next(s.B, p, d) ∈ S(p, d); since (p, d) satisfies B6, B6's sufficiency result gives every element of S(p, d) — hence a — satisfies T4. B0a ensures no non-baptismal mechanism introduces elements that might violate T4.

The gap between T9 (ForwardAllocation) and B1 is the *no-skip property*: baptism always selects the immediate successor in the stream, never an arbitrary later value. T9 says addresses increase; B1 says they increase *contiguously*. The difference is the guarantee that every ordinal from 1 through m is represented, which T9 alone does not assert.


## The high water mark

B1 yields a simplification: the entire allocation state of a namespace reduces to a single natural number.

**hwm(B,p,d) (HighWaterMark).** hwm(B, p, d) = #children(B, p, d) — the *high water mark*.

*Justification.* Let m = #children(B, p, d). By B1 (Contiguous Prefix), children(B, p, d) = {c₁, ..., cₘ} — the first m elements of the sibling stream S(p, d) with no gaps. The count therefore determines the prefix: children(B, p, d) is a single-valued function of m, with max(children) = cₘ when m ≥ 1. ∎

*Formal Contract:*
- *Definition:* hwm(B, p, d) = #children(B, p, d) where children(B, p, d) = {cₙ ∈ S(p, d) : cₙ ∈ B}.
- *Preconditions:* B6(p, d); B satisfies B1 for (p, d); p ∈ T, d ≥ 1; S(p, d) defined.
- *Invariant:* for B6-valid (p, d), hwm(B, p, d) = m implies children(B, p, d) = {c₁, ..., cₘ} and max(children) = cₘ (when m ≥ 1).
- *Axiom:* B1 (contiguous prefix), S0 (stream ordering).

Because children(B, p, d) = {c₁, ..., cₘ} is a contiguous prefix (B1), the maximum is always cₘ and the next element is always c_{m+1}. The operational definition of next — "find max, increment" — reduces to counting:

**B2 (High Water Mark Sufficiency).** `next(B, p, d) = c_{hwm(B,p,d) + 1}`.

Concretely: if hwm = 0, then next = inc(p, d) — the first child; if hwm = m > 0, then next = inc(cₘ, 0) — the next sibling. No counter distinct from the data, no free list, no reservation table. The cardinality of the existing children is a sufficient statistic for the next allocation.

*Proof.* We must show that for any registry B satisfying B1 and any valid parent-depth pair (p, d), the operationally defined next address equals the (hwm + 1)-th element of the sibling stream S(p, d). Let m = hwm(B, p, d) = #children(B, p, d). By B1 (Contiguous Prefix), children(B, p, d) = {c₁, ..., cₘ} for this m — the first m elements of S(p, d) with no gaps. The argument splits into two cases exhausting the possible values of m.

*Case 1: m = 0.* The children set is empty: children(B, p, d) = ∅. By the definition of next (NextAddress), next(B, p, d) = inc(p, d). By the definition of the sibling stream, c₁ = inc(p, d). Since hwm + 1 = 0 + 1 = 1, the claim c_{hwm+1} = c₁ = inc(p, d) = next(B, p, d) holds.

*Case 2: m ≥ 1.* The children set is non-empty: children(B, p, d) = {c₁, ..., cₘ}. We must identify max(children(B, p, d)). By S0 (StreamOrdering), the sibling stream is strictly increasing: c₁ < c₂ < ... < cₘ under the lexicographic order T1. The maximum of a finite strictly ordered set is its last element, so max(children(B, p, d)) = cₘ. By the definition of next, next(B, p, d) = inc(cₘ, 0). By the recursive clause of the sibling stream definition, c_{m+1} = inc(cₘ, 0). Since hwm + 1 = m + 1, the claim c_{hwm+1} = c_{m+1} = inc(cₘ, 0) = next(B, p, d) holds.

In both cases, next(B, p, d) = c_{hwm(B,p,d) + 1}. ∎

*Formal Contract:*
- *Preconditions:* B satisfies B1 for all B6-valid (p, d); (p, d) satisfies B6; S(p, d) = c₁, c₂, ... defined by c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0).
- *Postconditions:* `next(B, p, d) = c_{hwm(B,p,d) + 1}`.


## Atomicity

Baptism reads the high water mark, computes the next address, and commits the result as one indivisible step.

**B4 (Atomic Baptism).** Each baptismal operation is a single atomic transition. For every (p, d) satisfying B6:

  `(A s ∈ dom(baptize(p, d)) : baptize(p, d)(s) = s' with s'.B = s.B ∪ {next(s.B, p, d)})`

The value `baptize(p, d)(s).B = s.B ∪ {next(s.B, p, d)}` is read against the precondition state s and committed on one edge of the transition relation `→`: there is no intermediate observable state s_mid with `s → s_mid → s'`.

B0a guarantees that no other operation modifies s.B between any two transitions, so within a single Σ-transition the read of `s.B ∩ S(p, d)` is exact.


## The baptism operation

With the next address defined, the seed and finiteness invariants (B₀ conf., B_fin), the registry-wide invariants (B1, B10), and atomicity (B4) all in hand, we specify the baptism operation itself.

**Bop (Baptism).** The operation baptize(p, d) is defined by:

  PRE: B6(p, d) — depth validity; no parent-baptized prerequisite is imposed
  POST: s'.B = s.B ∪ {next(s.B, p, d)}; only s.B is modified
  STRUCTURAL (on Σ): B4 (Atomic Baptism) — read-against-precondition-state semantics

*Proof of well-definedness and correctness.* We must show that under the stated preconditions, baptize(p, d) is well-defined and produces a fresh address.

**Well-definedness.** The postcondition invokes next(s.B, p, d), which NextAddress establishes lies in T for any finite B ⊆ T, p ∈ T, d ≥ 1; B_fin (§B_fin) discharges the finiteness premise for B = s.B at any reachable s, so next(s.B, p, d) ∈ T here.

**Freshness.** Let a = next(s.B, p, d). We show a ∉ s.B without appeal to contiguity. By definition children(s.B, p, d) = s.B ∩ S(p, d) ⊆ S(p, d). Two branches of the next definition arise.

*children(s.B, p, d) = ∅.* Then a = inc(p, d) = c₁ ∈ S(p, d). Were a ∈ s.B, then a ∈ s.B ∩ S(p, d) = children(s.B, p, d) = ∅ — impossible. So a ∉ s.B.

*children(s.B, p, d) ≠ ∅.* Then a = inc(max(children(s.B, p, d)), 0); the maximum exists because children(s.B, p, d) is a non-empty finite subset of T (finite by B_fin, totally ordered by T1). Write q = max(children(s.B, p, d)). Since q ∈ children(s.B, p, d) ⊆ S(p, d), q = cₘ for some m, and a = inc(cₘ, 0) = c_{m+1} ∈ S(p, d). By S0 / TA5(a), inc(·, 0) strictly advances its argument, so a > q ≥ x for every x ∈ children(s.B, p, d); hence a ∉ children(s.B, p, d). Since a ∈ S(p, d), from a ∉ children(s.B, p, d) = s.B ∩ S(p, d) we get a ∉ s.B.

In both branches a ∉ s.B. The argument uses only the next definition, B_fin, S0/TA5(a), and the definition of children — contiguity (B1) and the high water mark (B2, hwm) play no role. ∎

*Formal Contract:*
- *Preconditions:* p ∈ T, d ∈ ℕ with d ≥ 1; B6(p, d) holds. (B1, B10, B_fin are reachable-state invariants, not caller obligations.)
- *Structural assumptions on Σ:* B4 (Atomic Baptism) — each `baptize(p, d) ∈ Σ` is a single atomic edge of the transition graph; this is an invariant of the operation vocabulary, not a caller-checked precondition.
- *Postconditions:* s'.B = s.B ∪ {next(s.B, p, d)} with next(s.B, p, d) ∉ s.B; s'.B satisfies B0, B1, B10, and B_fin.
- *Frame:* Only s.B is modified.


## Ghost elements: baptism without content

A baptized position need not contain anything. Nelson names these *ghost elements*:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements."

A ghost element is "virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." The position is in s.B — it has been baptized, it is permanent, it anchors a namespace for children — but nothing is stored at that address.

We record the relationship between baptism and content as a *forward requirement* on whichever future ASN introduces content storage.

**B3 (Ghost Validity — forward requirement on content storage).** Let a future ASN introduce a predicate `Occupied : T × 𝒮 → {⊤, ⊥}` denoting "the address t carries content in state s". Every future ASN introducing Occupied must arrange its operations so that

  `(A s : s reachable from s_init : (A t ∈ T : Occupied(t, s) ⟹ t ∈ s.B))`

— content is permitted only at baptized addresses. Under this requirement, the permitted configurations of a tumbler t ∈ T in a reachable state s are:

  - t ∈ s.B ∧ Occupied(t, s): a populated position
  - t ∈ s.B ∧ ¬Occupied(t, s): a ghost element (permitted)
  - t ∉ s.B ∧ ¬Occupied(t, s): an unbaptized, unoccupied position (not a baptized position / not a system entity)


## A baptism traced

We trace a concrete sequence to ground the formal development. Begin with B₀ = {[1]} — a single root node. We verify B₀ conformance. First, [1] satisfies T4: a single positive component, no zeros. Second, [1] does not belong to any sibling stream — membership in S(p, d) requires element length #p + d, and no valid parent p with d ∈ {1, 2} satisfies #p + d = 1 (since #p ≥ 1). Therefore children(B₀, p, d) = ∅ for all (p, d), which is trivially a contiguous prefix of length 0. The seed is conforming.

**Step 1: first user.** Namespace ([1], 2) — node [1], depth 2 (level crossing to user).

  next(B₀, [1], 2) = inc([1], 2) = [1, 0, 1]

TA5(d) appends d − 1 = 1 zero separator and child value 1. B5: zeros([1, 0, 1]) = 1 = 0 + (2 − 1). B6: d = 2 and zeros([1]) + 1 = 1 ≤ 3. B1: children = {[1, 0, 1]}, a prefix of length 1.

State: B₁ = {[1], [1, 0, 1]}.

**Step 2: second user.** Same namespace ([1], 2).

  next(B₁, [1], 2) = inc([1, 0, 1], 0) = [1, 0, 2]

TA5(c): sibling increment preserves length, advances position sig([1, 0, 1]) = 3, so the ordinal goes from 1 to 2. B5a: zeros([1, 0, 2]) = 1 = zeros([1, 0, 1]) — sibling preserves zeros. B1: children = {[1, 0, 1], [1, 0, 2]}, a prefix of length 2.

State: B₂ = {[1], [1, 0, 1], [1, 0, 2]}.

**Step 3: document under first user.** Namespace ([1, 0, 1], 2) — user [1, 0, 1], depth 2 (level crossing to document).

  next(B₂, [1, 0, 1], 2) = inc([1, 0, 1], 2) = [1, 0, 1, 0, 1]

B5: zeros([1, 0, 1, 0, 1]) = 2 = 1 + (2 − 1). B6: d = 2 and zeros([1, 0, 1]) + 1 = 2 ≤ 3. B1: children = {[1, 0, 1, 0, 1]}, a prefix of length 1. B7: S([1], 2) elements have length 3; S([1, 0, 1], 2) elements have length 5 — the *Length split* case of B7 gives disjointness.

State: B₃ = {[1], [1, 0, 1], [1, 0, 2], [1, 0, 1, 0, 1]}.

**Step 4: sub-document under first document.** Namespace ([1, 0, 1, 0, 1], 1) — document [1, 0, 1, 0, 1], depth 1 (intra-level descent to sub-document, exercising d = 1).

  next(B₃, [1, 0, 1, 0, 1], 1) = inc([1, 0, 1, 0, 1], 1) = [1, 0, 1, 0, 1, 1]

TA5(d) with k = d − 1 = 0 intermediate zeros: no zero separator is inserted; the value 1 is appended at position #p + d = 6. B5: zeros([1, 0, 1, 0, 1, 1]) = 2 = zeros([1, 0, 1, 0, 1]) + (1 − 1) — d = 1 contributes no new zeros, so the parent's zero count is preserved. B6: p = [1, 0, 1, 0, 1] satisfies T4 (last component 1 is positive), d = 1 ∈ {1, 2}, and B6(iii) at d = 1 reduces to zeros(p) ≤ 3, which holds since zeros([1, 0, 1, 0, 1]) = 2 ≤ 3. B1: children(B₄, [1, 0, 1, 0, 1], 1) = {[1, 0, 1, 0, 1, 1]}, a contiguous prefix of length 1, witnessing prefix extension under a fresh namespace at d = 1.

State: B₄ = {[1], [1, 0, 1], [1, 0, 2], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 1]}.

Nelson's "Items 2.1, 2.2, 2.3, 2.4" is exactly this mechanism — successive baptisms under parent 2 at depth 1, yielding the sibling stream 2.1, 2.2, 2.3, 2.4 by repeated application of inc(·, 0). The sequence is determined, contiguous, and the ordinals carry no semantics beyond order.

**B7 illustrated — non-nesting prefixes.** The steps above produce streams of different lengths, the easiest disjointness witness. We now exhibit two namespaces whose elements share a length yet remain disjoint because their parents are non-nesting. From state B₂ above, the parents [1, 0, 1] and [1, 0, 2] are both length 3, distinct, and neither is a prefix of the other (they disagree at position 3). Consider S([1, 0, 1], 1) and S([1, 0, 2], 1). Both streams have element length 4: #[1, 0, 1] + 1 = #[1, 0, 2] + 1 = 4, with p = [1, 0, 1], d = 1, p' = [1, 0, 2], d' = 1.

At position 3 of each stream: c₁ = inc([1, 0, 1], 1) = [1, 0, 1, 1] and c'₁ = inc([1, 0, 2], 1) = [1, 0, 2, 1]. By S1, every cₙ ∈ S([1, 0, 1], 1) preserves [1, 0, 1] as prefix and hence has value 1 at position 3, and every c'ₘ ∈ S([1, 0, 2], 1) has value 2 at position 3. Sibling increments inc(·, 0) modify only position sig(·) — namely position 4 in both streams (TA5(c)) — so position 3 is invariant across both streams: always 1 in S([1, 0, 1], 1), always 2 in S([1, 0, 2], 1). By T1's lexicographic comparison resolving at the first position of disagreement, every element of S([1, 0, 1], 1) is distinct from every element of S([1, 0, 2], 1). The streams are disjoint.

**B7 illustrated — nesting prefixes.** A harder witness: two namespaces whose elements share a length and whose parents nest. Suppose node [1, 1] has been baptized via inc([1], 1) = [1, 1] (TA5(d) with k = 1: #t' = 2, zero intermediate zeros, position 2 set to 1). Consider S([1], 2) and S([1, 1], 1). Both streams have element length 3: #[1] + 2 = #[1, 1] + 1 = 3. The prefixes nest — [1] ≼ [1, 1] — with p = [1], d = 2, p' = [1, 1], d' = 1.

At position 2 of each stream: inc([1], 2) = [1, 0, 1] — the value at position 2 is 0, the zero separator produced by TA5(d) with d − 1 = 1 intermediate zero. inc([1, 1], 1) = [1, 1, 1] — the value at position 2 is p'₂ = 1 > 0 (by T4, valid addresses do not end in zero, so the last component of [1, 1] is positive). Sibling increments inc(·, 0) modify only the last component (TA5(c)), so position 2 is invariant across both streams: always 0 in S([1], 2), always 1 in S([1, 1], 1). The streams disagree at a fixed position and are therefore disjoint.

**B9 unbounded extent exhibited.** The trace so far stops at B₄ with hwm(B₄, [1], 2) = 2 — two children of [1] at depth 2 (the addresses [1, 0, 1] and [1, 0, 2] baptized in Steps 1 and 2; Step 4's d = 1 baptism contributed to a different namespace and left hwm at ([1], 2) unchanged). B9 (Unbounded Extent, stated below) asserts that for any target M ∈ ℕ, a finite sequence of further baptisms in this namespace reaches hwm ≥ M. We exhibit the construction concretely for M = 5: three additional baptisms suffice (since hwm currently equals 2). Each step is a single Bop transition on namespace ([1], 2); we record next(B, [1], 2), the postcondition state, the resulting children set, and the contiguous-prefix verification.

  **Step 5: third user.** Same namespace ([1], 2).

  next(B₄, [1], 2) = inc(max{[1, 0, 1], [1, 0, 2]}, 0) = inc([1, 0, 2], 0) = [1, 0, 3]

  TA5(c): sibling increment preserves length, advances position sig([1, 0, 2]) = 3, so the ordinal goes from 2 to 3. By B2, this is c_{hwm+1} = c₃. B6 holds as in Step 2 ((p, d) = ([1], 2) is unchanged). B5a: zeros([1, 0, 3]) = 1 = zeros([1, 0, 2]) — sibling preserves zeros. B1: children = {[1, 0, 1], [1, 0, 2], [1, 0, 3]} = {c₁, c₂, c₃}, contiguous prefix of length 3.

  State: B₅ = {[1], [1, 0, 1], [1, 0, 2], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 1], [1, 0, 3]}. hwm(B₅, [1], 2) = 3.

  The remaining two baptisms in ([1], 2) follow the same pattern, reaching the final state B₇ = B₅ ∪ {[1, 0, 4], [1, 0, 5]} with hwm(B₇, [1], 2) = 5 = M.

The target hwm = 5 is reached in exactly three baptisms from B₄, witnessing B9 for the pair ((p, d), M) = (([1], 2), 5); for any target M' > 5, an additional M' − 5 baptisms in ([1], 2) extend B₇ to a registry with hwm = M' along the same pattern. Crucially, contiguity is maintained at every step — children(B₅, [1], 2) = {c₁, c₂, c₃}, children(B₆, [1], 2) = {c₁, ..., c₄}, and children(B₇, [1], 2) = {c₁, ..., c₅} — so the trace simultaneously witnesses B9 (unboundedness) and B1 (contiguity) under iteration.


## Co-reachable uniqueness

**B8 (Co-reachable Uniqueness).** Distinct *co-reachable* baptismal acts produce distinct addresses, where two acts are co-reachable iff both lie on a single transition path s_init →* s for some reachable state s:

  `(A a, b : produced by distinct co-reachable baptismal acts : a ≠ b)`.

The proof splits two ways: distinct baptisms within the same namespace, and baptisms in different namespaces. B8 establishes uniqueness only along a single transition path.

*Proof.* We must show that for any two distinct *co-reachable* baptismal acts β₁ and β₂ — both lying, by the co-reachability hypothesis, on a single transition path s_init →* s — the addresses they produce are distinct. Let a be the address produced by β₁ in namespace (p, d), and b the address produced by β₂ in namespace (p', d'). We proceed by case analysis on whether the two baptisms target the same or different namespaces.

*Case 1: same namespace — (p, d) = (p', d').* The co-reachability hypothesis gives a single transition path s_init →* s carrying both β₁ and β₂. Along that one path the edges are linearly ordered, so β₁ and β₂ are comparable; without loss of generality β₁ precedes β₂, the argument with roles exchanged being identical. By B4 (Atomic Baptism), each baptism is a single Σ-edge of this path. Let s₁ be the state on which β₁ acts and s₂ the state on which β₂ acts. By the Bop postcondition, the successor state s₁' = β₁(s₁) has s₁'.B = s₁.B ∪ {a}, so a ∈ s₁'.B. Since β₁ precedes β₂, s₂ is reachable from s₁' through a (possibly empty) sequence of transitions — that is, s₁' →* s₂. B0★ (Multi-step Irrevocability), the labelled corollary of B0 covering finite transition sequences, gives s₁'.B ⊆ s₂.B, hence a ∈ s₂.B.

Let m₁ = hwm(s₁.B, p, d) and m₂ = hwm(s₂.B, p, d). By B2 (High Water Mark Sufficiency), a = c_{m₁+1} and b = c_{m₂+1}, where cₙ denotes the n-th element of S(p, d). Since a = c_{m₁+1} ∈ s₂.B and B1 (Contiguous Prefix) holds for s₂, the children of (p, d) in s₂ include {c₁, ..., c_{m₁+1}}, so hwm(s₂.B, p, d) ≥ m₁ + 1. That is, m₂ ≥ m₁ + 1, hence m₂ + 1 ≥ m₁ + 2 > m₁ + 1. The indices m₁ + 1 and m₂ + 1 are distinct with m₁ + 1 < m₂ + 1. By S0 (StreamOrdering), c_{m₁+1} < c_{m₂+1} under the lexicographic order T1. By T1 irreflexivity, c_{m₁+1} ≠ c_{m₂+1}. Therefore a ≠ b.

*Case 2: different namespaces — (p, d) ≠ (p', d').* By construction, a ∈ S(p, d) — baptism in namespace (p, d) produces the next element of its sibling stream — and b ∈ S(p', d') by the same reasoning. By B7 (Namespace Disjointness), S(p, d) ∩ S(p', d') = ∅, so a ≠ b.

In both cases a ≠ b. No two distinct baptisms, whether in the same namespace, across sibling namespaces, or at different hierarchical levels, can produce the same address. ∎

*Formal Contract:*
- *Preconditions:* β₁, β₂ are distinct *co-reachable* baptismal acts — both lie on one transition path s_init →* s for some reachable s — in a system conforming to B0★ (which subsumes B0), B0a, B1, B4, and B7; β₁ produces a in namespace (p, d) and β₂ produces b in namespace (p', d'), where both (p, d) and (p', d') satisfy B6.
- *Postconditions:* `a ≠ b`. (The claim is scoped to co-reachable acts: two baptisms on incomparable branches of the reachability relation may compute the same address, but are never jointly observed in any reachable state.)


## Unbounded growth

Nelson insists that the address space imposes no capacity limits:

> "A tumbler consists of a series of integers. Each integer has no upper limit."

**B9 (Unbounded Extent).** `(A p, d : B6(p, d) : (A M ∈ ℕ : (E s' : s →* s' via baptisms : hwm(s'.B, p, d) ≥ M)))`.

No architectural limit constrains how many children a position may have.

*Proof.* We must show that for any pair (p, d) satisfying B6 and any bound M ∈ ℕ, there exists a state s' with s →* s' (via baptisms) such that hwm(s'.B, p, d) ≥ M. The argument is constructive: we exhibit the required sequence of baptismal transitions.

Let m = hwm(s.B, p, d) — the current count of children in namespace (p, d). If m ≥ M, set s' = s (the empty transition sequence witnesses s →* s via reflexivity) and the claim holds trivially. Otherwise m < M, and we construct a sequence of M − m baptismal transitions, each `baptize(p, d) ∈ Σ` targeting namespace (p, d). We show by induction on k that k successive baptismal transitions s → s₁ → ... → sₖ produce a state sₖ with hwm(sₖ.B, p, d) = m + k.

*Base case (k = 0).* s₀ = s with hwm(s.B, p, d) = m = m + 0. The claim holds by the reflexive case of →*.

*Inductive step.* Assume sₖ is a state reachable from s by k baptismal transitions in namespace (p, d), with hwm(sₖ.B, p, d) = m + k < M. We perform the transition `sₖ → sₖ₊₁` induced by `baptize(p, d) ∈ Σ` — that is, sₖ₊₁ = baptize(p, d)(sₖ). The preconditions of Bop are satisfied: B6(p, d) holds by hypothesis; by B4 (Atomic Baptism), each baptism is a single transition edge, so the constructed sequence is a chain of M − m successive edges.

By Bop, the postcondition gives sₖ₊₁.B = sₖ.B ∪ {next(sₖ.B, p, d)}. By B2 (High Water Mark Sufficiency), next(sₖ.B, p, d) = c_{m+k+1}, the (m + k + 1)-th element of the sibling stream S(p, d). This element is well-defined, and its existence is what the construction actually consumes. Each cₙ is produced by an increment that is total on T: c₁ = inc(p, d) ∈ T by TA5(d), and each cₙ₊₁ = inc(cₙ, 0) ∈ T by TA5(c). The final component of cₙ equals the ordinal n; passing from cₙ to cₙ₊₁ advances that component to n + 1, which is itself a natural number because ℕ is closed under successor (NAT-closure). Nothing in TA5(c) or in successor closure bounds the ordinal, so the construction may be iterated through every natural number, and the stream never exhausts its namespace.

The new element c_{m+k+1} is fresh — by the freshness argument of Bop, it does not appear in sₖ.B. The contiguous prefix property is preserved — by B1 preservation under Bop, children(sₖ₊₁.B, p, d) = {c₁, ..., c_{m+k+1}}. Therefore hwm(sₖ₊₁.B, p, d) = m + k + 1.

After M − m steps, hwm(s_{M−m}.B, p, d) = m + (M − m) = M. Setting s' = s_{M−m}, we have s →* s' via the M − m baptismal transitions, and hwm(s'.B, p, d) = M ≥ M. ∎

*Formal Contract:*
- *Preconditions:* (p, d) satisfying B6(p, d); M ∈ ℕ; current state s reachable from s_init.
- *Postconditions:* There exists s' with s →* s' via a finite sequence of baptismal transitions such that hwm(s'.B, p, d) ≥ M.
- *Axiom:* TA5(c), TA5(d) — inc(·, 0) and inc(·, d) are total on T, supplying each cₙ; NAT-closure — ℕ is closed under successor, so the child ordinal n + 1 ∈ ℕ at every step, hence grows without bound.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| s.B | B ⊆ T — the set of baptized tumblers (baptismal registry) | introduced |
| S(p,d) | Sibling stream: c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0) | from TA5(b), TA5(c), TA5(d) |
| hwm(B,p,d) | High water mark: #children(B, p, d) — sufficient allocation statistic | from B1, S0 |
| next(B,p,d) | Next address: if children = ∅ then inc(p, d) else inc(max(children), 0) | from TA5(c), TA5(d), T1 |
| Bop | baptize(p, d): PRE B6; STRUCT B4 (invariant of Σ, not per-call); POST s'.B = s.B ∪ {next(s.B, p, d)}; FRAME modifies only s.B | from B0a, B4, B6, B_fin, next def., S0, TA5(a) |
| S0 | `(A i, j : 1 ≤ i < j : cᵢ < cⱼ)` — stream strictly ordered | from TA5(a), T1 |
| S1 | `(A n : n ≥ 1 : p ≼ cₙ)` — all stream elements extend parent | from TA5(b), TA5(c), TA5(d) |
| S2 | `#p ≥ 2 ∧ p_{#p} = 0 ⟹ S(p, 1) = S(p′, 2)` (p′ = p without trailing zero) — trailing-zero stream identity | from TA5(d) |
| B0 | `s.B ⊆ s'.B` for all transitions — irrevocability (extends T8) | from B0a |
| B0★ | `s.B ⊆ s'.B` for all s →* s' (reflexive-transitive closure of transitions) — multi-step irrevocability | labelled corollary of B0 |
| B0a | Σ partitions into baptismal operations (the `baptize(p, d)` for B6-valid (p, d), each acting on s.B as in Bop) and s.B-frame operations (every other op satisfies `op(s).B = s.B`) — registry grows only through baptism | design requirement |
| B0b | Every transition is s.B-frame (`s'.B = s.B`) or baptismal (`s'.B = s.B ∪ {next(s.B, p, d)}`, one new element) | restatement of B0a (transition-level) |
| B₀ conf. | B₀ is finite, `children(B₀, p, d)` is a contiguous prefix for all (p, d), and `(A t ∈ B₀ : t satisfies T4)` — seed conformance | design requirement |
| B_fin | `(A s reachable : s.B is finite)` — registry finiteness | from B₀ conf., B0a |
| B1 | `B6(p, d) ⟹ (cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B))` — contiguous prefix over B6-valid namespaces (requires conforming B₀) | from B₀ conf., B0, B0b, B6, B7, next def., S0, TA5(c) |
| B2 | `next(B, p, d) = c_{hwm+1}` — high water mark sufficiency (from B1) | from B1, S0, NextAddress |
| B3 | Forward requirement on a future predicate `Occupied : T × 𝒮 → {⊤, ⊥}`: `(A s reachable, t ∈ T : Occupied(t, s) ⟹ t ∈ s.B)` — content permitted only at baptized addresses; ghost elements (`t ∈ s.B ∧ ¬Occupied(t, s)`) explicitly allowed | forward requirement on future ASN |
| B4 | Each `baptize(p, d) ∈ Σ` is a single atomic transition: `baptize(p, d)(s).B = s.B ∪ {next(s.B, p, d)}` is computed and committed in one step, with no intermediate observable state | design requirement |
| B5 | `zeros(inc(p, d)) = zeros(p) + (d − 1)` — field advancement | from TA5(b), TA5(d) |
| B5a | `zeros(inc(t, 0)) = zeros(t)` — sibling increment preserves zeros | from TA5(c) |
| B6 | `p satisfies T4`, `d ∈ {1, 2}`, and `zeros(p) + (d − 1) ≤ 3` — valid depth | from T4, TA5, B5 |
| B7 | `(p, d) ≠ (p', d') ⟹ S(p, d) ∩ S(p', d') = ∅` — namespace disjointness | from S(p,d), S1, T3, T4/TA5-SigValid, TA5(d), B6 |
| B8 | Distinct co-reachable baptisms produce distinct addresses — co-reachable (single-path) uniqueness | from B0★, B1, B2, B4, B7, S0, T1 |
| B9 | `(A p, d : B6(p, d) : (A M ∈ ℕ : (E s' : s →* s' via baptisms : hwm(s'.B, p, d) ≥ M)))` — unbounded extent | from B1, B2, B4, B6, Bop, TA5(c), TA5(d), NAT-closure |
| B10 | `(A t ∈ s.B : t satisfies T4)` — registry-wide T4 validity | from B₀ conf., B0a, B6, TA5(c), TA5a |


## Open Questions

- Must a parent position be baptized before children can be baptized beneath it? Nelson's ownership model implies yes; Gregory's implementation does not check at structural levels. Resolution depends on the ownership model (Tumbler Ownership).
- Under what activation discipline does `allocated(s) ⊆ s.B` hold — what must align each allocator-extension transition with a baptismal operation, and cover the genesis allocator domain with the seed?
- What concrete seed sets B₀ are valid — which root configurations satisfy B₀ conformance while providing a viable system genesis?
- Must the specification distinguish between a ghost element that could hold content and a structural position that cannot — or is this distinction derivable from the field structure alone?
- Under what conditions may bulk allocation — baptizing a contiguous range of k positions in a single operation — satisfy B4's atomicity and B1's contiguity requirements?
- What must a distributed system guarantee about cross-replica baptism ordering to maintain global address uniqueness without centralized coordination?
- What invariants must element-level subspace partitioning (T7) satisfy so that the contiguous prefix property holds independently within each subspace?
