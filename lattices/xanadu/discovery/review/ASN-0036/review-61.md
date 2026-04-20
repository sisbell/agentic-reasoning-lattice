# Review of ASN-0036

## REVISE

### Issue 1: S8 proof assumes m ≥ 2 via forward reference to ValidInsertionPosition

**ASN-0036, S8 (Finite span decomposition), Uniqueness across subspaces**: "since sig(v) = m ≥ 2, TA5(b) gives (v + 1)ᵢ = vᵢ for all i < sig(v)... (The case m = 1, where the V-position is a bare subspace identifier [S], is operationally excluded: ValidInsertionPosition requires m ≥ 2 for all V-positions...)"

**Problem**: The cross-subspace uniqueness argument requires m ≥ 2 to invoke TA5(b) for preserving component 1 under inc(v, 0). The proof cites ValidInsertionPosition, which is defined later in the ASN — a forward dependency. The Properties table for S8 lists "S8-fin, S2, S8a, S8-depth, T1, T3, T5, T10, TA5" with no mention of ValidInsertionPosition or any m ≥ 2 constraint. This creates an undeclared dependency: S8 relies on ValidInsertionPosition, which is built atop the D-SEQ/D-CTG machinery that follows S8.

The forward reference is also unnecessary. At m = 1, each subspace S contains at most one V-position: the only depth-1 tumbler with v₁ = S is [S] itself (by T3, canonical representation — any other depth-1 tumbler [k] with k = S is the same tumbler). The singleton interval [[S], [S+1]) at depth 1 contains no other depth-1 tumbler: S ≤ k < S + 1 with k ∈ ℕ forces k = S. Cross-subspace uniqueness is therefore trivial at m = 1 — two singleton intervals [[S₁], [S₁+1]) and [[S₂], [S₂+1]) for S₁ ≠ S₂ cannot overlap because their only depth-1 members are [S₁] and [S₂] respectively.

**Required**: Handle m = 1 directly in the proof before the cross-subspace argument: "For m = 1, each subspace has at most one V-position [S], and the singleton interval [[S], [S+1]) contains no other depth-1 tumbler, so both within-subspace and cross-subspace uniqueness are immediate." Then proceed with the existing T5/T10 argument for m ≥ 2. Remove the forward reference to ValidInsertionPosition.

### Issue 2: Correspondence run definition uses ordinal displacement at k = 0, which is undefined

**ASN-0036, S8 (correspondence runs)**: "A correspondence run is a triple (v, a, n) ... such that the arrangement preserves ordinal displacement within the run: (A k : 0 ≤ k < n : Σ.M(d)(v + k) = a + k)"

**Problem**: The notation `v + k` is introduced as shorthand for ordinal displacement (OrdinalShift, ASN-0034). OrdinalShift has precondition n ≥ 1. At k = 0, the expression `v + 0` falls outside OrdinalShift's domain. The ASN handles this informally: "At k = 0 this is the base case M(d)(v) = a — no displacement, no arithmetic." This is clear to the reader but formally incomplete — the universal quantifier ranges over k ≥ 0, yet the `+` notation has no defined meaning at k = 0.

**Required**: Formally close the definition. Either (a) extend the convention: "Define v + 0 = v (identity) and v + k = shift(v, k) for k ≥ 1"; or (b) restructure the run definition to separate the base case: "M(d)(v) = a, and for 1 ≤ k < n: M(d)(shift(v, k)) = shift(a, k)."

### Issue 3: S8a status in Properties table misattributes logical dependency

**ASN-0036, Properties Introduced table**: "S8a | ... | from T4, S7b (ASN-0034)"

**Problem**: S8a is established from an axiom ("V-positions are element-field tumblers") combined with T4's positive-component constraint. The proof text says it plainly: "S8a is a design requirement: V-positions are element-field tumblers, and T4 constrains the structure of every field." S7b (element-level I-addresses: zeros(a) = 3) appears in the S8a proof only as architectural motivation — it explains *why* V-positions mirror element-field structure, not that they logically *must*. If S7b were removed, the axiom that V-positions are element-field tumblers would still stand, and T4 would still yield the three conjuncts. The table entry "from T4, S7b" presents a motivational relationship as a logical dependency.

**Required**: Correct the Properties table entry to: "axiom (V-positions are element-field tumblers); structural properties from T4 (ASN-0034)."


## OUT_OF_SCOPE

### Topic 1: Operation-specific preservation of contiguity invariants
**Why out of scope**: The ASN explicitly identifies "Does each well-formed editing operation preserve D-CTG and D-MIN?" as an open question and notes that preservation "is a verification obligation for each operation's ASN." Each operation must independently prove it maintains contiguity — this is new territory for future ASNs, not an error in this one.

### Topic 2: Canonical (maximal) span decomposition
**Why out of scope**: S8 proves existence of a finite decomposition via singletons. Whether a unique maximal decomposition (fewest runs) exists requires defining when adjacent runs can be merged — a property of the representation that depends on I-address structure across run boundaries. This is a distinct question from what S8 establishes.

### Topic 3: Formal document set in the state model
**Why out of scope**: The state Σ = (C, M) treats M as a family indexed by documents without formalizing the index set. For this ASN's properties — all quantified "for all d" or "for a given d" — the implicit interpretation (M(d) = ∅ for documents that don't exist) suffices. Formalizing the document set requires document creation semantics, which is excluded from scope.

VERDICT: REVISE
