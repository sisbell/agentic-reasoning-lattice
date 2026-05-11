# Review of ASN-0040

## REVISE

### Issue 1: B6 necessity case classification leaves p = [0] uncovered

**ASN-0040, B6 necessity proof**: Sub-case (a) is described as "Interior violation: some T4 defect in positions 1 through #p − 1. This covers adjacent zeros anywhere in p and the leading-zero case p₁ = 0." Sub-case (b) requires "p_{#p} = 0 with no adjacent zeros and p₁ > 0."

**Problem**: For p = [0] with #p = 1, position 1 is simultaneously the leading and trailing position; the single zero violates T4(iii) and T4(iv) jointly. Sub-case (a)'s positional range "1 through #p − 1" is empty for #p = 1, yet the text claims sub-case (a) covers "the leading-zero case p₁ = 0" — a contradiction at #p = 1. Sub-case (b) explicitly excludes p₁ = 0. So p = [0] falls in neither sub-case as written, even though the propagation substance applies (TA5(b) preserves position 1; sig(c₁) = 2 in c₁ = [0, 1], so subsequent sibling increments leave position 1 untouched; every (cₙ)₁ = 0, violating T4(iii)). The gap is classificatory but does undermine the claimed exhaustiveness of the necessity argument.

**Required**: Either extend sub-case (a)'s range to "1 through #p" with reconciliation against sub-case (b)'s exclusion of p₁ = 0, relax sub-case (b) to admit p₁ = 0 (with internal sub-splits handling the singleton-zero corner), or add a dedicated sub-case for #p = 1 with p₁ = 0. The classification must exhaustively partition the (i)-violating configurations.

### Issue 2: B0 is logically redundant given B0a, but the implication is unstated

**ASN-0040, "The baptismal registry" section**: B0 (`(A Σ, Σ' : Σ → Σ' : Σ.B ⊆ Σ'.B)`) and B0a (Op partitions into baptismal-class and Σ.B-frame-class) are both presented as independent design requirements.

**Problem**: B0a's partition forces op(Σ).B = Σ.B (frame branch) or op(Σ).B = Σ.B ∪ {next(...)} (baptismal branch); in both branches Σ.B ⊆ op(Σ).B, so B0 holds. B0a strictly implies B0. The text motivates stating B0 separately (proof legibility, independence from T8) but does not acknowledge that the also-required B0a already entails B0. The Properties Introduced table further lists B0 and B0a as parallel "design requirement" entries with no derivability annotation.

**Required**: Either demote B0 to a labelled corollary of B0a (with explicit one-line derivation) while retaining its stand-alone presentation for emphasis, or note in the text that B0a implies B0 and explain why the document lists both as primitive requirements rather than primitive-and-consequence.

### Issue 3: Cross-ASN bridge axioms to allocated(Σ) are stated as prose, not labelled forward requirements

**ASN-0040, "The baptismal registry" section, "Relationship to ASN-0034's allocated set"**: "The bridge has two parts, each an obligation across the two ASNs rather than a theorem of either alone."

**Problem**: B3 (Ghost Validity) formalizes its cross-ASN obligation as a labelled forward requirement with explicit quantification over a yet-to-be-introduced predicate `Occupied`. By contrast, the two bridge parts (every transition extending some domₛ(A) is a baptismal Op-transition adding the same address to Σ.B; allocated(Σ_init) ⊆ B₀) are stated only in prose, with no labels and no formal quantification. The forward inclusion `allocated(Σ) ⊆ Σ.B` is then used to motivate stating B0 directly, but its discharge is left informal. The content is appropriate for cross-ASN scoping; the form is less rigorous than B3.

**Required**: Promote both bridge parts to labelled forward requirements with explicit quantification (e.g., "Bridge1: `(A Σ, Σ', A, a : Σ → Σ' ∧ a ∈ domₛ'(A) ∖ domₛ(A) : (E (p, d) satisfying B6 : Σ → Σ' is induced by baptize(p, d) ∧ a = next(Σ.B, p, d))`"; "Bridge2: `allocated(Σ_init) ⊆ B₀`"), parallel to B3's presentation, so the discharge ledger remains traceable to whichever future ASN ties baptism, allocation, and activation together.

## OUT_OF_SCOPE

(None — all issues identified are within scope of ASN-0040.)

VERDICT: REVISE
