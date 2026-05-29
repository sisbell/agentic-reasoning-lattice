# Review of ASN-0040

## REVISE

### Issue 1: B1 is stated over all (p, d), forcing proof of namespaces baptism can never produce

**ASN-0040, B1 (Contiguous Prefix)**: "`(A p, d, n : n ≥ 1 ∧ cₙ ∈ B ⟹ (A i : 1 ≤ i < n : cᵢ ∈ B))`" — quantified over *all* `(p, d)`, including pairs that fail B6.

**Problem**: Every consumer of B1 — `hwm`, B2, the freshness clause of Bop, B8 Case 1, B9 — invokes it only for B6-valid `(p, d)`. Nothing ever needs contiguity for a non-B6 namespace. Yet because the invariant is unrestricted, the inductive proof must dispatch sub-cases B and C (non-B6 namespaces whose streams are T4-invalid, or whose sole defect is a trailing zero at d=1). These sub-cases are the *sole* reason B1's proof:
- invokes B10 at its own precondition state (forcing the non-circularity disclaimer below),
- depends on S2 (Trailing-Zero Stream Identity),
- reaches into B6's *necessity* sub-cases (a)/(b) by section reference.

Restrict B1's invariant to `(p, d)` satisfying B6. The base case (B₀ conf.) weakens harmlessly; the target namespace is B6-valid because baptism requires B6; "other namespaces" reduce to other B6-valid pairs, handled entirely by B7 (sub-case A). Sub-cases B and C vanish along with their dependencies.

**Required**: Scope B1 (and the `(A p, d)` quantifier in B2's precondition) to B6-valid namespaces; delete sub-cases B and C and the machinery they pull in.

### Issue 2: Non-circularity disclaimer is meta-prose justifying proof ordering

**ASN-0040, B1, sub-case B**: "(B10 and B_fin are each established by transition inductions that cite only B6, B0a, B₀ conf., and TA5 — never B1 — so they hold for every reachable state independently of this induction; B1 may therefore invoke them at its own precondition state without circularity, the two inductions being jointly well-founded.)"

**Problem**: This is a paragraph defending the document's proof ordering ("non-circular by Y argument"), not advancing the claim. It exists only because sub-case B reaches for B10. Fixing Issue 1 removes the B10 invocation and this disclaimer with it.

**Required**: Remove the parenthetical (consequent on the Issue 1 fix).

### Issue 3: B6 Formal Contract Postcondition (b) restates the entire necessity proof

**ASN-0040, B6, Formal Contract**: "(b) Necessity: violating (ii) or (iii) produces T4 violations in S(p, d); violating (i) either propagates defects in p's preserved prefix (interior adjacent zeros, leading zero p₁ = 0, or the singleton case p = [0]...) to every stream element via TA5(b), or — when the sole defect is a pure trailing zero with p₁ > 0 ... — produces adjacent zeros within c₁ for d = 2 ... or creates a stream identical (by S2) to that of the distinct B6-valid namespace (p', 2) for d = 1..."

**Problem**: This single sentence reproduces the full narrative of the necessity proof (sub-cases (a), (b)/d=1, (b)/d=2) in different words. Two passages in the same property saying the same thing; the contract slot should state the property, not re-prove it.

**Required**: Collapse Postcondition (b) to the bare claim ("(i)–(iii) are jointly necessary; proof above") and let the proof body carry the case analysis.

### Issue 4: Atomicity section opens with axiom rationale, not axiom content

**ASN-0040, Atomicity, opening**: "Informally, the baptism process — read the high water mark, compute the next address, commit the result — must not be interleaved with another baptism in the same namespace. If two baptisms both read hwm = m before either commits, both compute c_{m+1} and both attempt to commit the same address — violating B8."

**Problem**: This is prose explaining *why* B4 is needed (a race would break B8) rather than what B4 says. The same justification reappears inside B4's body ("across two same-namespace baptismal transitions... exactly one of β₁;β₂ or β₂;β₁"). The race scenario is fine as a concrete illustration but is currently framed as standing rationale.

**Required**: Drop the motivating paragraph or fold the race illustration into a single concrete-example line; state B4 directly.

## OUT_OF_SCOPE

### Topic 1: The `Occupied` predicate and content/ghost classification (B3)

**Why out of scope**: Content storage is explicitly deferred. B3 handles this correctly — it states a *parametric forward requirement* on a future predicate rather than defining content operations here, so no revision is needed. Noting only that this is the right boundary, not a defect.

VERDICT: REVISE
