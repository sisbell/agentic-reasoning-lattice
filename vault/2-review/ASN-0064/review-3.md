# Review of ASN-0064

## REVISE

### Issue 1: F1 proof claims V(βⱼ) is convex in T1, which is false
**ASN-0064, "From Positions to Identity"**: "V(βⱼ) = {vⱼ + k : 0 ≤ k < nⱼ} is convex, since it consists of consecutive ordinal increments from vⱼ (D-SEQ, ASN-0036 establishes that V-positions within a subspace form a contiguous ordinal range)"
**Problem**: V(βⱼ) is not convex in the unrestricted T1 order. Extension tumblers lie strictly between consecutive ordinal increments. Concrete counterexample: V(βⱼ) = {[1,5], [1,6]}. By T1(ii), [1,5] < [1,5,1] (proper prefix), and by T1(i), [1,5,1] < [1,6] (component 2: 5 < 6). So [1,5,1] lies strictly between two elements of V(βⱼ) but is not in V(βⱼ). Convexity fails. The D-SEQ citation is also misapplied — D-SEQ establishes that V_S(d) forms a contiguous ordinal range, not that individual block extents V(βⱼ) are convex.
**Required**: The intersection argument works in the depth-m sub-order: (a) no depth-m tumbler lies between consecutive ordinal increments (no integer between k and k+1), so V(βⱼ) is convex within depth-m; (b) the restriction of ⟦σ_V⟧ to depth-m tumblers is convex (restriction of a convex set to a subset of the same total order); (c) their intersection is convex within depth-m. State this restricted-order argument explicitly, or argue directly: if vⱼ + c ∈ ⟦σ_V⟧ and vⱼ + c' ∈ ⟦σ_V⟧ with c < c', then for each c ≤ k ≤ c', vⱼ + c ≤ vⱼ + k ≤ vⱼ + c' in T1 (ordinal increments preserve order), so vⱼ + k ∈ ⟦σ_V⟧ by S0. This uses only the T1-convexity of ⟦σ_V⟧ and avoids the false convexity claim about V(βⱼ).

### Issue 2: F1 proof does not verify T12 well-formedness of constructed I-spans
**ASN-0064, "From Positions to Identity"**: "a contiguous set of V-positions maps to a contiguous set of I-addresses: a single I-span"
**Problem**: The proof claims the resolved set is representable as "at most m spans" but never verifies that each constructed I-span satisfies T12 (SpanWellDefinedness). The verification is straightforward — an I-run of width w from base aⱼ + c yields span (aⱼ + c, δ(w, depth)) where δ(w, depth) has action point = depth ≤ #(aⱼ + c) — but it must be shown, not assumed.
**Required**: Add one sentence verifying T12: the ordinal displacement δ(w, d) where d = #(aⱼ + c) satisfies w ≥ 1 (since the block intersection is non-empty) and action point d ≤ d, meeting the TA0 precondition.

### Issue 3: F2 mislabeled as INV
**ASN-0064, "The Overlap Predicate"**: "F2 — OverlapSufficiency (INV)."
**Problem**: F2 is a consequence of the overlap definition, not a state invariant. State invariants are predicates preserved across transitions. "Partial overlap suffices" is a property of the overlap predicate's type signature — it holds in every state because it's definitional, not because transitions maintain it. The same labeling issue affects F0 (a lemma about the current state, not a transition invariant) and F8 (a property of the tumbler ordering, not a state predicate).
**Required**: Relabel F2 as LEMMA. Consider relabeling F0 and F8 similarly.

### Issue 4: F6 conflates specification property with implementation commitment
**ASN-0064, "Endset Symmetry"**: "F6 — EndsetSymmetry (INV). All three endsets — from, to, type — are searchable with the same completeness and performance guarantees."
**Problem**: F6 bundles two claims under a single INV label. The first — that the overlap predicate is defined uniformly across endset slots — is a specification-level consequence of the definitions (LEMMA). The second — Nelson's "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS" — is an implementation/architecture commitment about indexing, not a state predicate. A state invariant cannot assert "performance": performance is a property of algorithms over states, not of states themselves.
**Required**: Separate into F6a (LEMMA: overlap predicate uniform across slots, follows from type signature) and F6b (DESIGN: per-endset indexing must support sub-linear search, citing the Nelson guarantee). Neither is INV.

### Issue 5: F11 frame asserts L' = L but L is not in the formal system state
**ASN-0064, "Query Purity"**: "L' = L" within the frame assertion
**Problem**: ASN-0047 defines the system state as Σ = (C, E, M, R). The link store Σ.L is defined in ASN-0043 but does not appear in the formal state. The ASN acknowledges this gap for LinkEntityCoherence ("No foundation currently defines this transition; we assume the property here") but does not note the same gap in F11's frame assertion. The frame lists five components including L, as if L were a recognized state component alongside C, E, M, R.
**Required**: Either (a) note explicitly that L is pending formal integration into the system state (parallel to the LinkEntityCoherence caveat), or (b) restate F11 as: FINDLINKS is not a state transition — it is a pure function from (Σ, Q) to a set. The frame assertion pattern (designed for transitions) is unnecessary; the observation that no transition occurs is sufficient.

## OUT_OF_SCOPE

### Topic 1: Formal integration of link store into system state
**Why out of scope**: ASN-0047's state Σ = (C, E, M, R) needs extension to (C, E, M, R, L) with corresponding monotonicity and permanence properties for L. This requires a link-creation elementary transition (analogous to K.α for content) with preconditions establishing LinkEntityCoherence. This is foundational work that belongs in its own ASN.

### Topic 2: Link-subspace arrangement semantics
**Why out of scope**: ASN-0036 defines arrangement properties (S8a, S8-depth, S3) for the text subspace (v₁ ≥ 1). Whether M(d) includes link-subspace mappings — and if so, under what invariants — is undefined by the foundations. The resolve function's correctness for text-subspace queries is unaffected, but a complete account of link-subspace V-positions requires new foundational work.

### Topic 3: Span denotation and level mismatch in overlap testing
**Why out of scope**: Span denotations include extension tumblers beyond the depth of the start address (e.g., ⟦([1,5], δ(1,2))⟧ includes [1,5,1] at depth 3). When endset spans and resolved spans operate at the same depth, the overlap test is correct. Cross-depth scenarios — where an endset span at depth m overlaps a resolved span at depth m+1 only on extensions — are theoretically possible but depend on allocation discipline not yet formalized. This belongs in a future ASN on span-level representation guarantees.

VERDICT: REVISE
