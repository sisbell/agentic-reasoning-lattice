# Review of ASN-0082

## REVISE

### Issue 1: D-MIN-post case `L ≠ ∅` glosses the closure step
**ASN-0082, D-MIN-post proof**: "D-L preserves it, so min(L ∪ Q₃) = [1, 1]."
**Problem**: Establishing `min(L) = [1, 1]` does not directly yield `min(L ∪ Q₃) = [1, 1]` — the missing step is that `min(L) ≤ min(Q₃)` (when `Q₃ ≠ ∅`), which requires noting that since `L ≠ ∅` forces `p > [1, 1]`, hence `p₂ ≥ 2`, so by D-DP(b) `min(Q₃) = vpos(1, ord(p)) = [1, p₂] > [1, 1]`. The chain is sound but the proof's compact phrasing skips this disjunction analysis. The parallel case `L = ∅ ∧ R ≠ ∅` is written cleanly; the mixed case should match.
**Required**: Make the closure step explicit, e.g., "Since `L ≠ ∅`, some `v ∈ V_1(d)` has `v < p`, so `p > [1, 1]` and `p₂ ≥ 2`; by D-DP(b), `min Q₃ = [1, p₂] > [1, 1] = min(L)`; hence `min(L ∪ Q₃) = min(L) = [1, 1]`."

### Issue 2: "NAT-order's transitivity" cited where T1's transitivity is required
**ASN-0082, D-MIN-post**: "min(V_1(d)) ≤ v < p by min's lower-bound property and NAT-order's transitivity"
**Problem**: The chained comparison is between tumblers (`min(V_1(d))`, `v`, `p`), which is governed by T1 (LexicographicOrder, postcondition (c)), not NAT-order. NAT-order ranges over ℕ. The mixed `≤/<` transitivity is derivable from T1's strict transitivity plus T1's `≤`-defining clause. While the conclusion is correct, the citation chain is incorrect for formal verifiability.
**Required**: Replace "NAT-order's transitivity" with "T1's transitivity" (or "the mixed `≤/<` chain from T1's strict transitivity composed with T1's `≤`-defining clause").

### Issue 3: "Strict-implies-weak" property invoked without explicit derivation
**ASN-0082, D-BJ proof**: "NAT-order's strict-implies-weak (`a > b ⟹ a ≥ b`)"
**Problem**: This property is not named as a clause in NAT-order's contract. It is derivable — `a > b` unfolds via the `>`-defining clause to `b < a`, the `≤`-defining clause's disjunction takes the strict branch to `b ≤ a`, and the `≥`-defining clause gives `a ≥ b` — but the chain should be explicit. The same pattern appears in the D-SHIFT well-definedness derivation.
**Required**: Replace each "NAT-order's strict-implies-weak" invocation with an explicit one-line chain, or introduce a named local derivation early in the ASN and cite it consistently.

### Issue 4: Introduction's framing as "extends ASN-0053" misrepresents the content
**ASN-0082, opening paragraph**: "This ASN extends ASN-0053 (Span Algebra) with two complementary shift properties..."
**Problem**: The ASN's primary content is I3, D-SHIFT, and their 15+ preservation lemmas, all concerning arrangement transformations on `M(d)` — the domain of ASN-0036, not ASN-0053. The span-algebra connections (I3-S, D-S) are two short corollaries near the end. A reader expecting span-algebra extensions will be surprised to find an arrangement-transformation specification.
**Required**: Rephrase the opening to indicate the ASN primarily extends ASN-0036 (with arrangement transformations underlying INSERT and DELETE) and derives span-algebra corollaries connecting to ASN-0053.

## OUT_OF_SCOPE

### Topic 1: Contraction at depth > 2
**Why out of scope**: The Open Questions section identifies this as future work. The TA4 zero-prefix obstruction is rigorously analyzed in the "Necessity from TA4" discussion, justifying the `#p = 2` restriction as mathematically forced by the chosen proof primitives. A separate ASN deriving the partial-inverse identity without TA4 would be required.

### Topic 2: Full INSERT operation (content placement at gap positions)
**Why out of scope**: The Scope subsection explicitly defers this. The shift sub-operation specified here is composable; a future INSERT ASN will extend `dom(C)` and re-establish D-CTG/D-MIN/D-SEQ.

### Topic 3: Link-subspace mutation discipline (tombstoning)
**Why out of scope**: Contraction is scoped to `S = 1` by axiom. Link-subspace mutation requires a tombstoning operation (since `V_2(d)` is sparse-with-tombstones by D-CTG's frame note), which is a distinct operation deferred to a future ASN.

VERDICT: REVISE
