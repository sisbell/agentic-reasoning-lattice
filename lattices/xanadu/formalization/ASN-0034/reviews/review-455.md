# Regional Review — ASN-0034/T10 (cycle 1)

*2026-04-23 17:36*

### Meta-register commentary across NAT axioms
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: NAT-order, NAT-closure, NAT-wellorder, NAT-zero prose
**Issue**: Recurring paragraphs explain *how* the axiom is structured rather than *what* it claims. Examples: "The axiom slot introduces `<` before constraining it: the first clause … posits `<` … and the four strict-total-order clauses that follow then constrain that relation. NAT-closure follows the same register …"; "The axiom slot introduces `+` before constraining it … the same register NAT-order uses to posit `<` …"; "NAT-order is therefore declared in the Depends slot so that the axiom body can be read without silently importing the definition." This is register/justification commentary about authoring choices, not mathematical content, and it compounds across four adjacent foundations.

### NAT-closure defensive prose about the missing right identity
**Class**: OBSERVE
**ASN**: NAT-closure — "The mirrored clause `n + 0 = n` is not axiomatized here; commutativity of `+` is not enumerated, so the right-identity form is not derivable from this axiom alone."
**Issue**: The axiom says what is posited; stating what is *not* posited, and why it is *not* derivable, is defensive annotation addressed to an imagined critic rather than content a downstream consumer needs.

### T3 prose statement uses an undeclared `n`
**Class**: OBSERVE
**ASN**: T3 — `(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`
**Issue**: `n` in the ellipsis is not bound; if `#a ≠ #b` the expression is ill-formed at face value. The *Postcondition* `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)` is the clean form and makes the prose redundant.

### T3 Gregory-implementation narrative in the claim body
**Class**: OBSERVE
**ASN**: T3 — paragraphs on `tumblerjustify`, `iszerotumbler`, the `[0,0,5,...]` / `[0,7,...]` scenario, and "T3 matters because address identity is load-bearing …"
**Issue**: Concrete examples are legitimate content, but their placement inside a foundation claim whose proof is a two-line unfolding of sequence extensionality is disproportionate and shifts the reader from the claim to consequences of its *violation*. Placement finding per the review criteria, not existence.

### T10 depends cites NAT-wellorder for two different uses
**Class**: OBSERVE
**ASN**: T10 — "NAT-wellorder — well-definedness of `min` on nonempty subsets of ℕ."
**Issue**: The proof uses `min` in two different modes: `ℓ = min(m, n)` (needs only NAT-order trichotomy) and `k = min{j : 1 ≤ j ≤ ℓ ∧ p₁ⱼ ≠ p₂ⱼ}` (the actual well-ordering use). The single gloss blurs this; a reader verifying the citation must re-derive which invocation is load-bearing.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 319s*
