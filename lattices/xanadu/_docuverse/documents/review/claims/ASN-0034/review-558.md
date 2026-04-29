# Cone Review — ASN-0034/TA-PosDom (cycle 1)

*2026-04-25 19:06*

Reading the ASN as a system. The proof of T1 (strict total order on tumblers) is the most intricate piece — let me walk its cases carefully, then check the foundational NAT-* layer for soundness and the TA-PosDom proof for precondition chains.

After careful review: the lexicographic order proof's three-way trichotomy split is exhaustive, the transitivity proof handles all four (case, case) sub-combinations, NAT-discrete's contrapositive use in TA-PosDom is correctly bounded, and the dependency graph is acyclic with each cited axiom actually used. I find no soundness issues — only a few stylistic notes.

### Redundant trichotomy step in T1 trichotomy Case 3
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder), part (b) Case 3
**ASN**: "Both clauses force `m ≠ n`: (β) gives `m + 1 ≤ n`, hence `m < n` via NAT-addcompat's `m < m + 1`; (γ) gives `n < m` symmetrically. So `a ≠ b` by T3. NAT-order's trichotomy at `(m, n)` resolves `m ≠ n` into `m < n ∨ n < m`. If `m < n`, then `k = m + 1 ≤ n`..."
**Issue**: The case (β) directly establishes `m < n` and `k = m + 1 ≤ n`; case (γ) directly establishes `n < m` and `k = n + 1 ≤ m`. The proof then invokes trichotomy at `(m, n)` to re-derive a disjunction it already has from the (β)/(γ) split, and case-splits on `m < n` vs `n < m` — branches that align exactly with (β) vs (γ). The argument would read more directly by case-splitting on (β) vs (γ) once.

### NAT-carrier body is largely meta-prose
**Class**: OBSERVE
**Foundation**: NAT-carrier (NatCarrierSet)
**ASN**: "The declaration is irreducible at this level: `ℕ` is taken as a primitive — not constructed from a more elementary substrate, not extracted from the meta-language by ambient definability... Every Cartesian product `ℕ × ℕ`... presupposes this primitive commitment."
**Issue**: The axiom asserts one fact ("ℕ is a set"); the body devotes two paragraphs to inventorying use sites (NAT-order's `<`, NAT-closure's `+`, T0's index domain) and explaining what the axiom is *not*. A precise reader has to skip past this to reach content, and the use-site inventory is the kind of cross-reference that decays as the spec evolves.

### NAT-closure body explains the signature rather than asserting it
**Class**: OBSERVE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity)
**ASN**: "The signature `+ : ℕ × ℕ → ℕ` carries two load-bearing commitments. Its domain `ℕ × ℕ` makes `+` total on the naturals — every pair of naturals has a sum — and its codomain `ℕ` closes the operation under addition... Totality rules out partial addition and closure rules out sums that escape ℕ."
**Issue**: This paragraph translates standard signature notation into prose about what it "rules out" — defensive justification that the signature notation already encodes. The signature itself is the assertion; the gloss adds nothing a reader of the formal contract needs.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 482s*
