# Review of ASN-0042

## REVISE

### Issue 1: Unilateral O10★ trajectory length is over-specified without justification
**ASN-0042, O10 Postconditions / Unilateral O10★**: "a chain Σ →⁺ Σ' of 2 (when zeros(pfx(π)) = 1) or 3 (when zeros(pfx(π)) = 0) baptisms, all performed by π alone."

**Problem**: O10's postcondition only requires `a' ∈ dom(π) ∩ Σ'.B ∧ ω_{Σ'}(a') = π`. A *single* baptism producing `a' = pfx(π).0.{hwm_0 + 1}` (user-level when zeros(pfx(π)) = 0, document-level when zeros(pfx(π)) = 1) satisfies the postcondition — the same Form A/B coverage analysis rules out sub-delegate coverage at that address. Form A fails at position #pfx(π) + 1; Form B (=length) fails by `u ∉ S'`; Form B (>length) cannot be a prefix because its length exceeds #a'. The proof commits to descending to element level (3 or 2 baptisms) without articulating why that depth is required.

**Required**: Either (a) state explicitly that the fork creates an element-level (content-bearing) address — Nelson's "inclusion link" target — and tie the trajectory length to that motivation in the postcondition, or (b) simplify Unilateral O10★ to a single-baptism witness with correspondingly weaker length commitment.

### Issue 2: O10's existence and unilateral proofs use inconsistent non-coverage conditions
**ASN-0042, O10 proof body**: The existence argument states "Choose any u ∈ ℕ_{>0} ∖ S," while the unilateral version sets "u = hwm_0 + 1 ... u ∉ S'," where S' ⊊ S.

**Problem**: The structural analysis at b_2 and b_3 shows that Form B (>length) sub-delegates fail at position #pfx(π) + 3 (positive component in their prefix vs. zero in b_2/b_3) regardless of `u`. Only Form B (=length) sub-delegates require the `u ∉ S'` condition. The existence argument's `u ∉ S` is therefore unnecessarily strong, and the discrepancy between the two parts obscures the actual structural reason for non-coverage — the reader is left wondering whether the broader bound is essential.

**Required**: Tighten the existence proof to use `u ∉ S'`, or fold the existence and unilateral arguments together — the unilateral construction with `u = hwm_0 + 1` already subsumes existence (S' ⊆ {1, ..., hwm_0} by O18 + B1, so `u = hwm_0 + 1 ∉ S'` holds in every reachable state).

### Issue 3: Worked example's "Self-ownership at the prefix" wording understates O18
**ASN-0042, Worked Example, "Self-ownership at the prefix"**: "Suppose now that the principal's prefix itself is an allocated address — for instance, [1, 0, 2] ∈ Σ.B, perhaps allocated as π_A's account-root index entry by π_A immediately upon delegation."

**Problem**: O18 (DelegationBaptizes) directly guarantees `pfx(π_A) ∈ Σ_1.B` as a *mandatory* consequence of the delegation transition itself — not "perhaps" through a subsequent action by π_A. The hedged "Suppose... perhaps allocated" wording treats as hypothetical what the ASN's own axiom mandates. The "general fact" stated below ("whenever pfx(π) ∈ Σ.B, ω(pfx(π)) = π") then holds *unconditionally* for every π ∈ Π_Σ in every reachable state by combining O18 (delegate's prefix in Σ.B) with O18's bootstrap clause (every initial principal's prefix in Σ_0.B).

**Required**: Replace the hedged framing with a direct citation to O18, and present "ω(pfx(π)) = π" as a corollary that holds in every reachable state for every principal — not as a hypothetical scenario.

### Issue 4: O17 (AllocatedAddressValidity) duplicates ASN-0040's B10
**ASN-0042, State Axioms, O17**: "Every allocated address is a valid tumbler: (A Σ, a : a ∈ Σ.B ⟹ T4(a))."

**Problem**: ASN-0040's B10 (T4ValidityInvariant) already establishes this as a derived invariant from B₀ conf., B6, and TA5a (IncrementPreservesT4). Stating O17 as an independent axiom in ASN-0042 duplicates B10 without adding constraint power. ASN-0040 is in the foundation; ASN-0042 should import its invariants rather than re-axiomatize them.

**Required**: Recast O17 as a derived fact citing ASN-0040's B10, or remove it and cite B10 directly at the consumption sites (AccountPrefix proof, O6 proof).

### Issue 5: O10's per-baptism authorization verifies O5 but not B6
**ASN-0042, O10 proof body, "Per-baptism authorization"**: The section verifies O5 (subdivision authority) at each baptism step but never explicitly verifies ASN-0040's B6 (ValidDepth precondition for Bop).

**Problem**: B6 requires at each baptism call: (i) p satisfies T4, (ii) d ∈ {1, 2}, (iii) zeros(p) + (d − 1) ≤ 3. The trajectory's baptisms satisfy this — e.g., for the zeros(pfx(π)) = 0 case, the third baptism has zeros(b_2) + 1 = 2 + 1 = 3 ≤ 3 — but the verification is implicit. A reader cannot confirm trajectory well-formedness without recomputing zero counts at each step. Without B6, the Bop calls are not well-defined operations.

**Required**: Add explicit B6 verification (per-step or summary sentence) showing the trajectory's depth choices remain within B6's bound at every baptism — the zeros(b_j) values and zeros(p) + (d − 1) sum at each step.

### Issue 6: O15's condition labels skip (iii)
**ASN-0042, State Axioms, O15**: The inlined conjuncts are labeled (i), (ii), (iv), (v), (vi). Condition (iii) — "π' ∈ Π_{Σ'} ∖ Π_Σ" — is folded into the outer quantifier rather than appearing as an inlined conjunct, with the (iii) label "reserved... to preserve numbering with the Delegation section."

**Problem**: The non-contiguous numbering disrupts readability. The reader must track an unusual convention to follow proofs that cite "condition (ii)" or "condition (vi)" — particularly when these proofs themselves (O7(a), AccountLevelPermanence Step 3, NestingByDelegation) appear hundreds of lines later.

**Required**: Renumber the conditions contiguously as (i)–(v) (and propagate the renumbering through all citations), or make condition (iii) an explicit inlined conjunct so the labels match.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer mechanism
Nelson mentions "someone who has bought the document rights" (LM 2/29). The ASN explicitly defers this to a future ASN in the Open Questions list. No conflict.

### Topic 2: Concrete realization of delegation through Bop
The `delegated_Σ` predicate characterizes when a transition is a delegation, but the operation's signature and how its baptismal component invokes Bop with specific (p, d) parameters is not specified. This belongs to a future ASN bridging the ownership and baptism mechanisms.

### Topic 3: Cross-node identity federation
O9 establishes node-locality. Cross-node federation invariants are acknowledged as an open question.

### Topic 4: Authentication mechanism
O11 axiomatizes authentication as external to the ownership model; concrete mechanisms (certificates, keys, tokens) are explicitly out of scope.

VERDICT: REVISE
