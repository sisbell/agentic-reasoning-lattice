# Review of ASN-0036

## REVISE

### Issue 1: D-SEQ "Assembly" step skips a step

**ASN-0036, D-SEQ proof, Assembly paragraph**: "The k-values form a finite contiguous range of positive integers (Step 3, Step 4) beginning at 1 (Step 2). Therefore there exists n ≥ 1 such that the k-values are exactly {1, 2, …, n}."

**Problem**: The conclusion leaps from three premises ("finite," "contiguous," "contains 1") to a specific form {1, ..., n} without showing the bridging argument.

**Required**: One additional sentence — let n = max(k-values), well-defined by Step 4's finiteness; by Step 3's contiguity applied from 1 to n, {1, ..., n} ⊆ k-values; by definition of max, k-values ⊆ {1, ..., n}; hence equality. The argument is straightforward but absent.

### Issue 2: S8 uniqueness-within-subspace proof conflates generic t and specific w

**ASN-0036, S8 proof, Uniqueness within a subspace**: "Suppose for contradiction that t ≠ v satisfies #t = m and v ≤ t < shift(v, 1). [...] For the case of interest t = w, shared subspace w₁ = v₁ = S gives t₁ = v₁, forcing j ≥ 2; at m = 2 this further forces j = m = 2, leaving only the j = m case below. The two-case argument that follows treats j generically for any 2 ≤ j ≤ m."

**Problem**: The case analysis works for any t with t₁ = v₁ and #t = m, but the proof mixes the generic argument with its specialization to t = w. A reader has to disentangle which constraints come from the generic hypothesis and which from the specialization.

**Required**: State and prove the within-subspace incompatibility lemma cleanly: "for any t ≠ v with t₁ = v₁ = S and #t = m, t ∉ [v, shift(v, 1))." Then apply with t = w. The j ≥ 2 derivation belongs in the lemma's setup, not in the middle of the case analysis.

### Issue 3: ValidInsertionPosition empty-case parameterization is implicit

**ASN-0036, ValidInsertionPosition definition, empty subspace case**: "V_1(d) = ∅. Then v = [1, 1, ..., 1] of depth m ≥ 2... The specific value of m beyond the bound m ≥ 2 is not fixed by the strand model... Once any position is placed, S8-depth fixes the depth at the chosen m."

**Problem**: In the empty case the set of valid positions is {[1, 1, ..., 1] : m ≥ 2} — a family parameterized by m, not a single position. The formal contract says "exactly one valid position exists per choice of depth m ≥ 2," but the predicate ValidInsertionPosition(d, v) doesn't carry m. In the non-empty case it's a function of state; in the empty case it depends on an external choice.

**Required**: Either parameterize the predicate — `ValidInsertionPosition(d, v, m)` in the empty case — or state explicitly that in the empty case ValidInsertionPosition is a relation on (v, m), with the choice of m an operational input. The current framing makes the parameter dependence implicit and risks confusion when downstream ASNs cite the predicate.

### Issue 4: OrdAddHom precondition contains redundancy

**ASN-0036, OrdAddHom formal contract**: "Preconditions: v ∈ T, #v = m ≥ 2; w ∈ T, Pos(w) (TA-Pos, ASN-0034), #w = m, w₁ = 0, actionPoint(w) ≤ m."

**Problem**: Given #w = m and ActionPoint's general bound `1 ≤ actionPoint(w) ≤ #w` (ASN-0034), the conjunct actionPoint(w) ≤ m is automatic. Stating both invites the reader to verify whether the constraint is load-bearing or derivative.

**Required**: Drop actionPoint(w) ≤ m (or replace with a comment noting it follows from #w = m and ActionPoint's contract). A minor tightening, but the precondition list is the contract — redundant clauses obscure which conditions are genuinely required.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG, D-MIN, subspace alignment

**Why out of scope**: The ASN explicitly defers preservation of these properties to operation-layer ASNs (Scope section, Remark following S8a, prose after the D-SEQ example). Operations like INSERT and DELETE establishing contiguity restoration and subspace agreement is a verification obligation each operation's ASN carries, not a gap in the strand model.

### Topic 2: Canonical (minimum-cardinality) span decomposition

**Why out of scope**: S8 asserts existence of *some* finite decomposition, not minimum cardinality. The "Non-canonicality" remark addresses this directly, and #runs(d) optimization belongs to operations and implementation layers (Open Question; Scope excludes enfilade implementation internals).

### Topic 3: OrdSubHom and ord-arithmetic round-trip property

**Why out of scope**: The ASN proves OrdAddHom for ⊕ and explicitly raises subtraction and round-trip questions in Open Questions. TA7a's conditional S-closure for subtraction makes this future work, properly deferred rather than skipped here.

### Topic 4: Specific depth m in empty subspace

**Why out of scope**: The ASN fixes only the lower bound m ≥ 2 and explicitly defers the choice to first-placing operations (Open Question; ValidInsertionPosition definition prose). Nelson's text leaves deeper subdivision open (LM 4/31).

VERDICT: REVISE
