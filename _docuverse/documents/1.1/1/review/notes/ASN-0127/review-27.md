# Review of ASN-0127

I re-derived every named claim against the foundation contracts, recomputed all witnesses, and checked the worked illustration arithmetic. Summary of the verification, then findings.

**Verification notes.**

- **F-IMG / F-IMG-MONO / F-IMG-CONTR**: element-chasing derivations are complete in both directions; the extension/contraction frames cited match ASN-0047's amended K.μ⁺/K.μ⁻ (prior-domain and retained-domain agreement respectively). Degenerate cases (empty `W`, empty intersection, fresh document) are stated.
- **F-IMG-SWING**: the reindexing formula checks out (`v = π(u)` with π onto `dom(Σ'.M(d))` by K.μ~-FIX; substitution verified against the injective witness both via the formula and directly via the bijection equation). The cardinality-pinning argument (`|π⁻¹(W) ∩ dom| = |W ∩ dom|` for a bijection of the domain onto itself) is correct. I recomputed all four witnesses (injective, gain, loss, four-position) from the bijection equation; each post-state arrangement and post-state image matches the text. Witness admissibility is established without circularity: domain fixity is derived from π being a permutation of the pinned position set, not assumed from K.μ~-FIX; clauses (i)–(v) of ASN-0047's admissibility are each discharged (shape invariants persist because they quantify only over the unchanged domain; the two-distinct-values precondition holds in every witness). Finiteness for the nesting argument is correctly grounded in S8-fin.
- **F-UDIST / F-IMONO / F-VDIST**: the distributivity chain (intersection over union, non-emptiness of a union, existential over disjunction) is shown step by step; the remark that disjoint `W₁, W₂` can yield overlapping images under content sharing correctly identifies why the unrestricted form of F-UDIST is load-bearing in F-VDIST.
- **F-FULL**: `image = ran(Σ.M(d))` for `W ⊇ dom(Σ.M(d))`, and the match predicate at `I = ran(Σ.M(d))` is literally LP12's right-hand side; the bridge to `discoverable_from` is exact, including the empty-arrangement boundary (both sides ∅).
- **F-CIL / F-CIL-perlink / F-PRES / F-INERT / F-LAMBDA**: I checked every frame in ASN-0047 — K.α, K.δ, K.ρ, K.μ⁺_L, and the *amended* K.μ⁺ and K.μ⁻ (which add `L' = L` in the extended state) all publish link-store preservation, so F-PRES is accurate; K.μ~ inherits it by composition. F-INERT's path lift is by explicit induction, not assertion. F-LAMBDA correctly evaluates the fresh link's match at `Σ'` (it is undefined at `Σ`), and disjointness of the two parts is grounded in the ASN-0093 freshness lemmas.
- **E-INV / E-MONO / E-CONS**: LP13 supplies exactly F-CIL-perlink's hypothesis. E-CONS's exclusion direction (the case `a ∈ dom(Σ.L)` is impossible) is argued explicitly rather than by symmetry; the converse uses freshness plus monotonicity correctly.
- **D-NONMONO**: the case split is exhaustive (only the K.μ family touches an existing document's arrangement; all other transitions' frames fix `M(d_q)`). Each monotone chain (extension, contraction, containment-type reorder motion) correctly bridges the comprehension's evaluation state through F-INERT before applying F-IMONO. The insufficiency witness (two-span slot, image moves `{a} ↦ {b}`, discovery set fixed) is correct and admissible. Non-monotonicity is refuted by an explicit incomparable swing, not by appeal.
- **D-CWP**: the bridge `image(W, d_q, Σ') = I_R` is justified (D-SEQ★ gives `R ⊆ dom(Σ.M(d_q))`, so the restriction's domain is exactly `R`); the `A = A ∪ B ⟺ B ⊆ A` reduction is correct; both `I_R` and `Δ` are pre-state quantities, so the biconditional is a genuine wp. The `R = ∅` full-clearance boundary is handled, including validity of full clearance under the strict-contraction clause.
- **Worked illustration**: recomputed every slot intersection in all bullets. The prefix-incomparability scaffolding is fully discharged (sibling incomparability via ChainMembershipForOrigin + T10a.2; `a_θ` vs `a_i` via equal lengths from FirstEmission + TA5(c), distinctness via T7 with T4-validity discharged, and the proper-prefix length gap from Prefix). The composite-validity obligations are met rather than waved at: J0 for the K.α bullet, J1★ for the rise bullet (standing provenance record via P4★ + P2, with K.μ⁻'s `R' = R` frame cited), D-SEQ★/S3★ for the extension, and full K.μ~ admissibility for both swings. The `R = ∅` clearance bullet correctly cross-checks D-CWP's boundary condition against the non-empty pre-state discovery set.

I also checked the anti-bloat patterns specifically: I found no relocated finding-residue paragraphs, no excluded-case prose, no multi-section deferral chains, and no duplicated paragraphs. The two closest candidates — the single parenthetical clarifying that K.μ~-FIX is a consequence rather than a premise during witness construction, and the one-clause role note introducing F-CIL-perlink — each carry semantic load (the former fixes the dependency direction a reader would otherwise question, since the main F-IMG-SWING derivation *does* cite K.μ~-FIX; the latter states when F-CIL's hypothesis fails and what survives). Neither rises to a finding.

Convention checks: all references are to foundation ASNs only; no foundation notation is reinvented (`image`, `matches`, `findlinks`, `findlinks_V` are new primitives, and the one overlap point with ASN-0098 — `discoverable_from` — is bridged by a proven equality rather than a parallel definition); `findlinks_V` is used consistently throughout with no stray occurrences of the old name.

## REVISE

None.

## OUT_OF_SCOPE

### Topic 1: Intersection behavior of `findlinks` / `findlinks_V`
**Why out of scope**: The ASN establishes the union laws (F-UDIST, F-VDIST) and needs nothing more for D-CWP. The dual question — that `findlinks(I₁ ∩ I₂, Σ)` is in general a proper subset of `findlinks(I₁, Σ) ∩ findlinks(I₂, Σ)`, with a characterization of when equality holds — is genuine algebra but new territory, adjacent to Q2's conjunctive queries. Nothing in this note claims or needs an intersection law.

### Topic 2: Slot-attributed and multiplicity-valued results
**Why out of scope**: `findlinks` deliberately discards *which* slot witnessed the match and *how many* V-positions in `W` witness each matched link (the latter would connect to ASN-0098's `project` cardinalities). A slot-resolved or count-valued variant would be needed to support Q2's per-slot conjunctive semantics and Q4's composition with projection, both of which the ASN already marks as open.

VERDICT: CONVERGED
