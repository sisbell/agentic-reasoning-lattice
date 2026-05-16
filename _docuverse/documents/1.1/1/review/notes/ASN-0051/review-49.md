# Review of ASN-0051

I traced through every SV claim, the wp analysis, and the Worked Example. The ASN is unusually rigorous: proofs are explicit with cited dependencies, boundary cases are addressed, and the Worked Example verifies key postconditions against concrete tumbler values.

## REVISE

(none)

## What I checked

**SV6 (CrossOriginExclusion).** Traced the sandwich argument: the sub-lemma's prefix exclusion (#t ≥ j via T1(ii) on proper prefix), upward divergence (T1(i) with j ≤ #t and j ≤ #(s⊕ℓ) = #ℓ via TA0 + actionPoint codomain), T4-validity verification of t in [s, s⊕ℓ) (t₁ ≠ 0, t_#t ≠ 0, no-adjacent-zeros at boundary (k-1, k) via k > p₃ forcing k-1 ≥ p₃). All cases close.

**SV10 + CrossDocumentDecoupling witnesses.** Verified each elementary step against ASN-0047 preconditions: bootstrap node from InitialState, K.δ on account 1.0.1 and document 1.0.1.0.1, K.α on i₂ (only i₂; i₁ and i₃ remain unallocated tumblers in T to keep J0 honest), K.λ on a = 1.0.1.0.1.0.s_L.1 (zeros=3, E(a)₁=s_L, origin(a)=d, fresh), K.μ⁺ on v₁=[s_C,1] (D-MIN), K.ρ for J1★. Step-by-step preconditions discharge cleanly. CrossDocumentDecoupling extension allocates sibling d₂ = 1.0.1.0.2 under the existing account and j under d₂; SV6 then forces j ∉ ⟦(i₁, ℓ_span)⟧.

**SV11 (PartialSurvivalDecomposition).** Biconditional checked both directions: (⇒) fragment count = m·p forces non-empty term count = m·p and each term as its own fragment (overlap eliminated via S0-convexity within each block's ordinal sequence); (⇐) non-emptiness plus non-adjacency/non-overlap within blocks delivers m·p. The two-span non-injective Worked Example exhibits mechanism (b) (within-block coalescence) and the three-span extension adds mechanism (a) (empty terms from (s₃, ·)). The ASN explicitly acknowledges p ≥ 2 attainment is not exhibited; the biconditional is independent of witness existence.

**SV5 (ReorderingProjectionInvariance).** Composite-level scope is explicit: π is preserved at K.μ~'s endpoints (Σ, Σ'), but the intermediate state Σ_int after the K.μ⁻ stage has reduced π. K.μ~-FIX gives dom(M'(d)) = dom(M(d)) so ψ acts on a fixed arena. The non-degenerate "Reordering that changes locate" subsection added on top of the original within-locate swap correctly exhibits ψ crossing the locate boundary.

**SV7/SV8/SV9 + NewLinkEvaluationDefinedness.** L-frame composes (so K.μ~ is L-frame); discover_s is invariant under all L-frame transitions and grows strictly only under K.λ via L12a. The corollary discharges four definedness obligations (Σ'.L(a_new), slot projection, coverage, M(d) in frame) without state-priming.

**Foundation citations.** Every cross-ASN reference is to ASN-0034, 0036, 0043, 0047, 0053, or 0058. No non-foundation references.

**SV14.** Each part (a)-(e) is a direct corollary of the per-link SV-claim under the document-derived A = ran(M(d)); the strict shrinkage witness extends the Worked Example with a fresh K.λ allocation a' with F' = {(a₃, a₄⊖a₃)}, then K.μ~ + K.μ⁻ removes a₃ from ran(M(d)), exiting a' from discover_through_from(d) while preserving discover_from({a₃}) by SV8.

**wp analysis.** Each elementary transition's wp for `π(e, d) ≠ ∅` is read off correctly. K.μ⁻ is the unique transition with non-trivial wp; the D-SEQ admissibility is named explicitly as a precondition of applicability. The reformulation correctly notes "Nothing new is established beyond the forward claims".

VERDICT: CONVERGED
