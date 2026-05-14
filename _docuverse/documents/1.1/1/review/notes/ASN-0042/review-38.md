# Review of ASN-0042

## REVISE

### Issue 1: Inconsistent "second clause" references for O14

**ASN-0042, O14 discussion and O4 proof**:
- O14 paragraph 2: "The second clause asserts bootstrap finiteness: the system starts with finitely many principals."
- O14 paragraph 8: "...the second clause, which runs in the opposite direction — every initially allocated address is *covered* by some initial principal..."
- O4 proof: "This is the second clause of O14 (BootstrapPrincipal), which asserts exactly that the initial principals cover all initially allocated addresses."

**Problem**: Three references to "the second clause" name two distinct clauses. Counting the listed formulas as written, paragraphs 3–8 only cohere if clause 1 is the conjunction `Π₀ ≠ ∅ ∧ coverage`, clause 2 is `|Π₀| < ∞`, ..., clause 7 is `pfx(π) ∈ Σ₀.B`. Under that counting, paragraph 2 is correct (clause 2 = finiteness) but paragraph 8 and the O4 proof reference the wrong clause.

**Required**: Reconcile the references. Either renumber so a single meaning of "second clause" is used throughout, or replace the misnamed references with precise wording (e.g., "the coverage conjunct of the first clause").

### Issue 2: Inaccurate FiniteRegistry citation regarding O10

**ASN-0042, State Axioms section (FiniteRegistry paragraph)**:
"O10's fork analysis cites O18 to ensure ... O10's proof (zeros=0 case) cites FiniteRegistry to justify the existence of a maximum component value among any finite collection of sub-delegate prefixes."

**Problem**: The actual O10 non-coverage analysis cites neither FiniteRegistry nor a maximum-of-finite-set construction. The argument is: pfx(π_i) ∈ Σ.B (via O18) → pfx(π_i) ∈ S(pfx(π), 2) ∩ Σ.B → U^{(i)}_1 ≤ hwm_0 (via ASN-0040 B1/contiguous-prefix). Each U^{(i)}_1 is bounded individually; no max over a finite collection is taken.

**Required**: Either remove the FiniteRegistry forward reference from the O10 description, or rewrite to cite ASN-0040's B1 and B_fin (the contiguous-prefix property and per-state finiteness of Σ.B that make hwm well-defined).

## OUT_OF_SCOPE

None — the open questions are appropriately listed at the end and don't appear as gaps in the present ASN.

VERDICT: REVISE
