# Regional Review — ASN-0034/T4 (cycle 2)

*2026-04-23 00:00*

### Hierarchical-structure prose forward-references and duplicates T4
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: Section "Hierarchical structure": "The maximal written form — the case with all four fields present, `zeros(t) = 3` — is: `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ` where `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` at every position."
**Issue**: The paragraph uses `zeros(t)` before T4's body defines it as `|{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|`, and presents the `k = 3` schema with the same inequalities `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ`. T4's Axiom then restates the identical `k = 3` case. The prose preview adds narrative (quotations from Nelson, the renaming note) but the technical schema it exhibits is already in T4.

### Subscript `k` overloaded in T4 Axiom schema
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: T4 Formal Contract Axiom: "for each `k ∈ ℕ` with `0 ≤ k ≤ 3` at which `zeros(t) = k`, the form is — … `k = 2`: `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ`; `k = 3`: `… . 0 . E₁. ... .Eδ`. In every case, `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` at every position present."
**Issue**: Outer `k` ranges over the zero-count `{0,1,2,3}`; inner `k` in `Dₖ` is the document-field position index ranging over `{1, …, γ}`. Same letter, two quantifier scopes in the same Axiom sentence. The clash is readable but the precise reader has to disambiguate by context.

### Canonical-form schema sits under Axiom but is derivable
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: T4 Formal Contract Axiom: "Valid address tumblers satisfy: `zeros(t) ≤ 3`; `(A i : 1 ≤ i < #t : ¬(tᵢ = 0 ∧ tᵢ₊₁ = 0))`; `t₁ ≠ 0`; `t_{#t} ≠ 0`. … The canonical written form of a T4-valid address tumbler is given by the following schema…"
**Issue**: The four primary conditions (zero-count bound, non-adjacency, first/last non-zero) are the stipulated axiom. The per-`k` schema — including implicit `α, β, γ, δ ≥ 1` for each field segment — is derivable from those conditions (no adjacent zeros and no boundary zeros force each between-zero segment non-empty). Placing it inside Axiom conflates what is stipulated with what follows. The schema reads more naturally as a Consequence.

### Exhaustion proof's disclaimer about substitution of equals is inconsistent with NAT-zero's body
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: T4 body Exhaustion: "The mechanism for excluding the branch `zeros(t) < m` given a lower bound `m ≤ zeros(t)` is uniform: … This uses trichotomy alone — substitution of equals under `<` is not among NAT-order's stated properties, so we avoid relying on it." Contrast NAT-zero body: "In the second case, `0 = n` rewrites `n < 0` to `0 < 0`, again contradicting irreflexivity."
**Issue**: NAT-zero's body freely substitutes equals under `<`; T4's Exhaustion refuses to, on the grounds that NAT-order does not enumerate such a property. Substitution of equals is a rule of first-order logic with equality, not a property any relation must declare. The two derivations in the same ASN therefore apply different rules of reasoning to the same logical primitive. Either NAT-zero's body should be rewritten to match T4's discipline, or T4's Exhaustion can lose the disclaimer and compress the `m = zeros(t)` subcases to direct rewriting.

### NAT-card uniqueness justified by one-line appeal to trichotomy
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: NAT-card body: "The length `k` is uniquely determined by `S` because two strictly increasing enumerations of the same set must agree element-by-element under NAT-order's trichotomy; hence `|·|` is a well-defined total function…"
**Issue**: The claim that two strictly increasing enumerations of the same finite set must agree element-by-element is a theorem requiring induction on length (unequal-length case derives a contradiction; equal-length case pairs off via trichotomy at each position). The body collapses both steps into "under NAT-order's trichotomy." Since NAT-card is asserting `|S|` axiomatically as a unique value, the body's informal justification is not load-bearing — but its brevity is the kind of "by similar reasoning" gloss flagged for precise specs.

VERDICT: OBSERVE

## Result

Regional review converged after 2 cycles.

*Elapsed: 1719s*
