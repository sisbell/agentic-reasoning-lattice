## Audit

### Σ.M(d), V-sub, subspace, S8a, S8-fin, S8-depth, D-CTG

These are all posits or definitions; their formal statements are internally consistent and their Depends lists are correctly assembled. S8a's positivity Consequence is correctly derived (zeros = 0 → empty filter → no component is zero → each component > 0 via NAT-zero). S8-depth's exclusion of OrdShiftHom and OrdinalShift from its Depends list is correctly argued. No issues in this group.

### D-CTG-depth — structure audit

The overall proof strategy is sound: a disagreeing interior pair (u, x) generates ≥ N+1 intermediate tumblers in V₁(d) via D-CTG, contradicting S8-fin's bound N. The individual steps I traced are formally correct:

- T1-witness k = j is uniquely pinned (k < j contradicts established agreement; k > j contradicts j being a disagreement site). ✓
- Clause (ii) ruled out: m < m+1 (NAT-addcompat) makes m+1 ≤ m false (NAT-order trichotomy). ✓
- j < m derived: NAT-addcompat gives j < j+1; chained with j+1 ≤ m through NAT-order transitivity. ✓
- w > u: k = j+1 ≤ m = min(m,m), w_{j+1} = n > u_{j+1}. ✓
- w < x: k = j < m ≤ min(m,m), w_j = u_j < x_j; agreement at i < j via minimality of j (interior) and shared subspace (i=1). ✓
- zeros(w) = 0: components 1..j positive by S8a Consequence; j+1 positive by 0 < u_{j+1} < n (NAT-order transitivity); j+2..m = 1 > 0 by NAT-closure Consequence 0 < 1. NAT-card k=0 case closes the zeros step. ✓
- All D-CTG guards satisfied for w. ✓
- Distinctness of w⁽ᵏ⁾ across different n values: differ at component j+1, so unequal by T3. ✓
- Surjectivity of S8-fin's f gives indices j_k ∈ {1,...,N}. ✓
- Map k ↦ j_k injective: same index would force f(j_k) = w⁽ᵏ⁾ and f(j_k) = w⁽ˡ⁾ by single-valuedness of f, so w⁽ᵏ⁾ = w⁽ˡ⁾ against distinctness. ✓
- NAT-card upper bound: {j_k : 1 ≤ k ≤ N+1} ⊆ {j : 1 ≤ j ≤ N}, so |{j_k}| ≤ N. ✓
- N+1 ≤ N contradicts N < N+1 (NAT-addcompat at n=N) via NAT-order transitivity; N < N contradicts irreflexivity. ✓

One gap identified.

---

### Successive minimum enumeration termination is informally grounded

**Class**: REVISE
**Foundation**: NAT-card (NatFiniteSetCardinality, ASN-0034); NAT-wellorder (NatWellOrdering, ASN-0034)
**ASN**: D-CTG-depth, closing finiteness step — *"The bound function is the count of S's not-yet-drawn members: it starts at the N + 1 pairwise-distinct values j_k delivered by the injective k ↦ j_k, strictly decreases by one at each extraction, and so empties the residual after exactly N + 1 steps, indexing the draws by precisely {r ∈ ℕ : 1 ≤ r ≤ N + 1}."*
**Issue**: The proof needs |S| = N+1, where S = {j_k : 1 ≤ k ≤ N+1}. It tries to establish this by constructing a strictly increasing enumeration g of S of length N+1 (for NAT-card's value clause) via successive minimum extraction. But the claim that the construction runs for exactly N+1 steps — i.e., that the domain of g is exactly {r : 1 ≤ r ≤ N+1} — is the very statement that |S| = N+1. The proof justifies it by appealing to a "bound function" that "starts at N+1 pairwise-distinct values," but that starting value of N+1 is the cardinality of S, which is what g is being constructed to establish via NAT-card. The formal termination of the while-loop requires showing, for each r = 1,...,N+1, that the residual R_r is non-empty (so NAT-wellorder can be invoked), and showing R_{N+2} = ∅ (so g's image equals S). Both require the invariant |R_r| = N+1−(r−1), which is a formal induction on r not carried out. The map k ↦ j_k is injective from {1,...,N+1} to S but is not strictly increasing, so it is not the enumeration NAT-card's value clause needs; sorting it is exactly the successive minimum step, making the argument circular at the cardinality level. The rest of the proof derives each step with explicit foundation citations (individual NAT-addcompat invocations, specific NAT-card clause references) and this is the only step relying on informal counting.
**What needs resolving**: Provide a formal inductive argument establishing the invariant `|R_r| = N+1−(r−1)` for r = 1,...,N+1 — showing the residual is non-empty at each extraction step and empty after N+1 steps — grounded in NAT-card and NAT-wellorder without assuming the cardinality result being derived. Alternatively, break the argument into two separate claims: (a) the image of any injective map from {1,...,N+1} has cardinality N+1 (proved by induction on N+1, using successive minima with the inductive hypothesis as the termination argument), and (b) application to {j_k}. Either route must make the inductive structure explicit.

---

### "Infinite sequence" overstates the T0(a) iteration

**Class**: OBSERVE
**Foundation**: T0(a) (UnboundedComponentValues, ASN-0034)
**ASN**: D-CTG-depth proof body — *"Iterating the bound … we obtain a strictly increasing sequence n₁ < n₂ < n₃ < … of natural numbers … The sequence n₁ < n₂ < … being infinite has at least N + 1 terms."*
**Issue**: The sequence is not pre-established as infinite; each term is produced on demand by one invocation of T0(a). Describing it as "infinite" implies an independently existing unbounded supply that the proof never constructs. The proof only needs N+1 terms, obtained by N+1 applications of T0(a) with increasing bounds M₀ = u_{j+1}, M₁ = n₁, ..., M_N = n_N.
**What needs resolving**: Rephrase as: "Apply T0(a) N+1 times with bounds M₀ = u_{j+1} and M_r = n_r to obtain n₁ < n₂ < ... < n_{N+1} with each n_k > u_{j+1}."

---

### Variable j overloaded across proof sections

**Class**: OBSERVE
**Foundation**: (notation)
**ASN**: D-CTG-depth proof body and Depends section — j names the specific first-disagreement position (2 ≤ j ∧ j+1 ≤ m) throughout the witness construction, while the closing finiteness step quotes S8-fin's index domain `{j ∈ ℕ : 1 ≤ j ≤ N}` and uses j_k for the pulled-back indices, creating three simultaneous uses of j in the critical section.
**What needs resolving**: Rename the bound variable in S8-fin's domain to a fresh letter (e.g., ι or r) wherever it appears in the finiteness step, and rename the pulled-back indices to match (e.g., ι_k). The first-disagreement position j should retain its name throughout.

VERDICT: REVISE