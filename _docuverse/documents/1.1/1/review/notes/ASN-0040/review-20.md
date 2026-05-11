# Review of ASN-0040

## REVISE

### Issue 1: The Σ.B = allocated(Σ) identification is asserted but not supported

**ASN-0040, "Relationship to ASN-0034's allocated set"**: "We therefore identify `Σ.B = allocated(Σ)` as an extensional equation, and treat the names as interchangeable across the two ASNs."

**Problem**: The identification requires that every address baptized in ASN-0040 corresponds to an admissible allocator step under ASN-0034's T10a. T10a's (T2) child spawn requires `parent(A) ∈ Act(s) ∧ spawnPt(A) ∈ domₛ(parent(A))`. ASN-0040's B6 imposes T4-validity, depth ∈ {1, 2}, and the zero-count bound — but explicitly defers the parent prerequisite ("Whether p must itself be baptized... is deliberately deferred to the Open Questions"). If parent prerequisite does not hold, baptisms can occur under unbaptized p, producing addresses in Σ.B that have no corresponding activated allocator under T10a — Σ.B and allocated(Σ) diverge.

The mismatch is concrete: B₀ conf. permits seeds like `{[1, 0, 1]}` (a user without its node parent). Under the identification this implies `allocated(Σ_init) = {[1, 0, 1]}` without [1] ever being allocated — impossible under T10a's spawning rules.

**Required**: Either (a) strengthen B6/B₀ conf./Bop to require `p ∈ Σ.B` and ancestor closure of B₀, making the identification provable; or (b) weaken the prose to a one-sided inclusion plus a conditional ("equality holds iff the parent prerequisite is enforced"). The current presentation makes a substantive set-equality claim contingent on an explicitly open question.

### Issue 2: B0 stated as a corollary of T8 under the same unsupported identification

**ASN-0040, "Relationship to ASN-0034's allocated set"**: "B0 (Irrevocability) below is a corollary of T8 (AllocationPermanence) under the identification: T8 asserts `allocated(Σ) ⊆ allocated(Σ')` for every transition, and `Σ.B = allocated(Σ)` substitutes directly to yield `Σ.B ⊆ Σ'.B`."

**Problem**: This derivation chains through Issue 1's identification, so its status is no firmer. The properties table reports B0 as "design requirement" — that is the correct standing — but the prose presents the corollary as an established fact.

**Required**: Drop the corollary framing, or qualify it with the same parent-prerequisite condition that Issue 1 raises. State that ASN-0040 takes B0 as a stand-alone obligation independent of any identification.

### Issue 3: B9's quantifier and Bop's domain do not match

**ASN-0040, B9**: "`(A p ∈ Σ.B, d satisfying B6, M ∈ ℕ : ...)`"
**ASN-0040, Bop preconditions**: "p ∈ T, d ∈ ℕ with d ≥ 1; B6(p, d) holds; B4 holds for namespace (p, d); Σ.B satisfies B1 and B10."

**Problem**: B9 restricts unbounded growth to namespaces with already-baptized parents, while Bop admits baptism under any B6-valid p irrespective of `p ∈ Σ.B`. The mismatch is a silent narrowing: the ASN does not assert or refute that unbounded growth holds under unbaptized parents, even though Bop says baptisms there are legal. This is another surface of the unresolved parent prerequisite (Issues 1, 2).

**Required**: Either widen B9 to all B6-valid `(p, d)` with an explanatory note, or restrict Bop's preconditions to require `p ∈ Σ.B` and remove the open question. The internal quantifier inconsistency must be eliminated.

### Issue 4: B7's Case 2 is proved abstractly but never traced concretely

**ASN-0040, "A baptism traced" + "B7 Case 3 verified"**: The example exercises B7 Case 1 (different stream lengths, via lengths 3 vs 5 in Step 3) and Case 3 (nesting prefixes, via [1] vs [1,1] at equal stream length). Case 2 — non-nesting prefixes at equal stream length, the only case that depends on T10 (PartitionIndependence) rather than length or position-#p+1 structure — has no concrete witness.

**Problem**: Of the three exhaustive cases on which B7's proof rests, only two are illustrated. Case 2 is conceptually distinct: it appeals to a foundation result not used by the other two. A reader has no specific scenario against which to verify the claim.

**Required**: Add a small trace such as namespaces `([1], 2)` and `([2], 2)` (non-nesting prefixes [1], [2], same depth, so element length 3 in both streams): exhibit S([1], 2) = [1,0,1], [1,0,2], ... and S([2], 2) = [2,0,1], [2,0,2], ..., verify divergence at position 1 by T1 case (i).

### Issue 5: Proofs invoke B4 with event-based vocabulary that the framework section retires

**ASN-0040, Bop freshness clause**: "B4 ensures the observation is stable: no concurrent same-namespace baptism modifies children(Σ.B, p, d) between the read and the commitment."
**ASN-0040, B1 proof, target namespace**: "...as a single Op-transition acting on B; its observation of children(B, p₀, d₀) is the exact state at the moment of commitment, with no interleaved modification by another transition."

**Problem**: The framework section explicitly states the transition vocabulary subsumes the older "commit(β₁) ≺ read(β₂)" event phrasing: "We adopt the transition phrasing throughout the formal arguments below." But the proofs of Bop, B1, B8, and B9 continue to use "read", "commitment", "concurrent baptism", and "interleaved modification" — vocabulary that presupposes intra-transition substructure the framework does not provide. The reasoning is correct under the transition reading, but the prose imports terms from a framing the ASN says it has discarded.

**Required**: Restate the substantive content in transition terms — for example: "B4 establishes `baptize(p, d)` as a single edge in the transition graph, so `next(Σ.B, p, d)` is evaluated against the precondition state Σ of the same transition that produces Σ'." Remove "read/commit", "concurrent", and "interleaved" phrasings from formal arguments.

### Issue 6: TA5a citation reformulated without acknowledgment

**ASN-0040, B6 sufficiency proof**: "the 'TA5 preserves T4' lemma (ASN-0034) states that inc(t, k) preserves T4 when t satisfies T4, k ≤ 2, and `zeros(t) + (k − 1) ≤ 3`."

**Problem**: ASN-0034's TA5a (IncrementPreservesT4) actually states: "inc(t, k) satisfies T4 iff k ∈ {0, 1}, or k = 2 ∧ `zeros(t) ≤ 2`." The reformulation `k ≤ 2 ∧ zeros(t) + (k − 1) ≤ 3` is a correct uniform sufficient condition under T4-validity of t, but presenting it as TA5a's statement misdescribes the foundation. A reader checking against TA5a will find a different formula.

**Required**: Either quote TA5a's actual case-based condition and then derive the uniform form ("equivalently, under T4-validity, the condition `zeros(t) + (k − 1) ≤ 3` with `k ≤ 2` discharges TA5a's preconditions in all cases"), or annotate the reformulation as the author's restatement.

## OUT_OF_SCOPE

(none — the Scope section's deferrals match what the proofs actually rely on)

VERDICT: REVISE
