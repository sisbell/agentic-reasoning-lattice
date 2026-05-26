# Review of ASN-0098

## REVISE

### Issue 1: Weakest precondition analysis missing for a non-trivial postcondition
**ASN-0098, throughout**: The ASN provides inclusion lemmas (LP9, LP10), exact-difference formulas, and the discoverability biconditional (LP12), but does not synthesize a weakest-precondition computation for any non-trivial postcondition.
**Problem**: A non-trivial wp analysis is mandatory per the review depth standards. A natural candidate the ASN does not address: wp for "discoverable_from(a, d, Σ') is preserved across a K.μ⁻ transition". The building blocks are present (LP10's exact-difference formula and LP12's coverage-range characterization), but the synthesis to an explicit wp statement is left implicit. The reader must infer the wp from the lemmas rather than seeing it derived.
**Required**: Compute wp explicitly for at least one non-trivial preservation postcondition. The discoverability-preservation-under-K.μ⁻ case decomposes cleanly: the wp is the existence of some slot i such that `project(a, i, d, Σ) ∩ R ≠ ∅`, where R is the K.μ⁻ retention set. Derive this from LP10 and LP12 and exhibit at least one boundary case (e.g., the wp's behaviour when retention reduces the content subspace to empty).

### Issue 2: Case numbering ambiguity in the achievability section
**ASN-0098, "Boundary and Width Behaviour" → achievability discussion**: "Descendant documents. The second case is documents d' standing in a proper prefix relation d_0 ≺ d'." "Ancestor documents. The third case is documents d' standing in a proper prefix relation d' ≺ d_0."
**Problem**: The section enumerates four cases (same-document cross-subspace, non-nesting, descendant, ancestor) but labels only the latter two with "the second case" and "the third case". The numbering presumably counts cross-document cases (with non-nesting as the first), but earlier cases lack matching numerical labels, so the references read as inconsistent. A reader looking for "the first case" finds no anchor.
**Required**: Either add explicit cross-document numbering to non-nesting (e.g., "First cross-document case: Non-nesting documents...") or drop the "the second case" / "the third case" phrasings from descendant and ancestor; the section headers alone identify them unambiguously.

### Issue 3: "Structural form #ℓ = #s alone" understates the canonical condition
**ASN-0098, "Boundary and Width Behaviour" → non-canonical remark**: "The canonical assumption #ℓ = #s is therefore load-bearing for LP-Fin's finitude conclusion" and "The distinction between 'could be made tight with discipline' and 'cannot be tight at any state' is decided by the structural form #ℓ = #s alone, not by the contents of the stores."
**Problem**: Canonical is defined as `ℓ = δ(n, #s)`, which is the conjunction of (a) `#ℓ = #s` and (b) ℓ is an ordinal displacement. The wording "structural form #ℓ = #s alone" names only condition (a), omitting (b). Non-canonical spans with `#ℓ = #s` but non-displacement ℓ (e.g., ℓ with multiple nonzero components within T12's action-point bound) are admissible by T12 and are non-tight by the tightness predicate's definitional requirement — not by the F-intersection argument the surrounding paragraphs construct, which addresses only `#ℓ < #s`. The current wording leaves a reader to infer that any `#ℓ = #s` span is canonical, which is false.
**Required**: Tighten the wording. Replace "structural form #ℓ = #s alone" with "structural form ℓ = δ(n, #s) alone" (or "the canonical form alone"). Add a brief note distinguishing two grounds for non-tightness of non-canonical spans: (i) `#ℓ < #s` is non-tight by the infinite-F-intersection argument, demonstrating that the canonical requirement is structurally necessary for predicate decidability; (ii) other non-canonical forms (`#ℓ = #s` with non-displacement ℓ, or `#ℓ > #s`) are non-tight by the tightness predicate's definitional canonical-form requirement.

VERDICT: REVISE
