# Review of ASN-0043

## REVISE

### Issue 1: L9 case (ii) — carrier root zeros assumption is unjustified

**ASN-0043, L9 (TypeGhostPermission) proof, case (ii)**: "T10a anchors the allocator hierarchy at `r` and admits document-level allocation only via `inc(·, k')` chains, each of which can only increase the zero count or extend the rightmost component; for the document hierarchy to be inhabitable at all under T10a, the carrier root must satisfy zeros(r) ≤ 2."

**Problem**: The case analysis covers zeros(r) ∈ {0, 1, 2} and excludes zeros(r) = 3, but T10a's root requirement is only T4-validity, which permits zeros(r) ∈ {0, 1, 2, 3}. The cited justification presupposes the conclusion: it argues that the hierarchy *must be* inhabitable, but L9's universal quantification ranges over all conforming states — including those where zeros(r) = 3 and the hierarchy is uninhabitable. In such a state, dom(Σ.M) = ∅ permanently (no inc chain from an element-level root reaches zeros = 2), dom(Σ.L) = ∅ by L1a, and L9's existential cannot be satisfied. The proof's case (ii) construction silently assumes the system is not in this regime.

**Required**: Either (a) declare zeros(r) ≤ 2 as an explicit system-level precondition (or derive it from S7d under an assumption that dom(Σ.M) ≠ ∅ at some prior state), (b) add a fourth sub-case handling zeros(r) = 3 (showing L9 is vacuous or fails benignly), or (c) qualify L9's universal quantification: "for any conforming Σ in which document allocation is possible..."

### Issue 2: L8 — same_type equivalence properties not derived

**ASN-0043, L8 (TypeByAddress)**: "same_type(a₁, a₂) ⟺ coverage(Σ.L(a₁).type) = coverage(Σ.L(a₂).type)"

**Problem**: The definition uses set equality on coverages, so reflexivity, symmetry, and transitivity inherit trivially — but the ASN never states these consequences. "Links sharing a type" is a downstream concept (the ASN invokes it in the discussion of L9 and L10), and that concept is well-defined only if same_type is shown to partition dom(Σ.L) into equivalence classes. A postcondition without its derived consequences is a depth gap.

**Required**: Add three one-line consequences: same_type is reflexive (`(A a ∈ dom(Σ.L) :: same_type(a, a))` by reflexivity of set equality), symmetric (`(A a₁, a₂ :: same_type(a₁, a₂) ⟺ same_type(a₂, a₁))` by symmetry of `=`), and transitive (`(A a₁, a₂, a₃ :: same_type(a₁, a₂) ∧ same_type(a₂, a₃) ⟹ same_type(a₁, a₃))` by transitivity of `=`).

### Issue 3: L10 — hierarchy inclusion not derived

**ASN-0043, L10 (TypeHierarchyByContainment)**: "`coverage({(p, δ(1, #p))}) = subtypes(p)`."

**Problem**: L10 establishes that one span query at p matches every t with p ≼ t. The hierarchy is then illustrated informally (MARGIN ⊂ FOOTNOTE via prefix containment) but never derived as a formal consequence. The natural lemma — `p₁ ≼ p₂ ⟹ subtypes(p₂) ⊆ subtypes(p₁)` — is the formal content of "a query at p₁ matches all subtypes of p₂." Without it, L10 supplies only point-wise matching, not a hierarchy.

**Required**: State the lemma and prove in one line: for any t ∈ subtypes(p₂) we have p₂ ≼ t, which combined with p₁ ≼ p₂ and transitivity of ≼ yields p₁ ≼ t, hence t ∈ subtypes(p₁).

### Issue 4: L11a — bundles two distinct claims under one label

**ASN-0043, L11a (LinkUniqueness)**: "The conclusion has two distinct halves, drawn from separate sources: *Uniqueness across allocation events.* By GlobalUniqueness... *Permanence of the address-to-link binding.* ... This is precisely the content of L12 (LinkImmutability, below); it is not derivable from GlobalUniqueness."

**Problem**: L11a is a single lemma whose proof acknowledges two independent sources (one foundation, one a later claim in this ASN). The permanence half is just a forward reference to L12 — "this is precisely the content of L12." The bundling obscures the structure: uniqueness is a property of allocation events (state-local at allocation time), permanence is a state-transition invariant (carried by L12). Treating them as one lemma makes the dependency graph unclear and creates a forward reference to L12.

**Required**: Split L11a into a uniqueness lemma (cleanly derived from GlobalUniqueness via L1c) and either (a) drop the permanence statement (since it duplicates L12) or (b) restate it as a corollary explicitly downstream of L12.

### Issue 5: L7 — DirectionalFlexibility asserted without scan argument

**ASN-0043, L7 (DirectionalFlexibility)**: "The invariants L0–L14 and L-fin impose no constraint on which of the from/to slots carries directional significance; any directional interpretation is determined by the link type, outside the link structure."

**Problem**: This is a negative claim about the *absence* of directional constraints in the invariants. It is labeled META, but META is not a license to skip verification — the reader must take the claim on faith or scan all fifteen invariants individually. A negative claim about an enumerable set is verifiable by inspection; the proof should perform the inspection.

**Required**: A one-paragraph scan confirming that none of L0, L1, L1a–c, L2, L3, L4, L5, L6, L8, L9, L10, L11a, L11b, L12, L12a, L13, L14, L14a, L-fin references "direction," "source," "target," or any concept that ties slot semantics to position. Alternatively, demote L7 to a design-note paragraph rather than a numbered property.

VERDICT: REVISE
