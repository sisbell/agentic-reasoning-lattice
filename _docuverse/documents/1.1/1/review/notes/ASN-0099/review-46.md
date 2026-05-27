# Review of ASN-0099

I worked through F1's match predicate, F4's realizability witnesses, the A1a/A1b split, the F9 family + F9-λ, F11's I-side persistence, F19's monotonicity, the F10 ordering derivation, the worked example's six queries, and the sub-lemmas (ComprehensionInvariantUnderΣL, PerLinkInvarianceUnderValuePreservation, ChainIndexEqualsAllocationOrder).

The ASN is unusually thorough. The two-phase factoring (image + match) is clean. The conformance contract family (F2 ∧ F3 and variants for filtered, scoped, V-side) is properly stated with each half independently citable. F4's design justification correctly disclaims mathematical uniqueness while supplying five operational-distinguishability witnesses; each witness construction respects L3's e₃ ≠ ∅ mandate and is realizable via the discharge through K.λ from any state with `dom(Σ.M) ≠ ∅`. The spans-monotonicity analysis correctly identifies that containment breaks monotonicity while reverse-containment and ≥k cardinality preserve it, with the witness-structure argument doing the additional distinguishing work.

A1's split into A1a (published-frame preservation of L) and A1b (closed-world convention at K.μ⁺, K.μ⁻, K.ρ) is transparent; the appendix properly surfaces A1b as methodological with grounding from Nelson's design intent and Gregory's implementation as convergent (not constitutive). Downstream claims inheriting A1b are correctly tagged.

F9-cor + F9-λ exhaust V's single-step impact on findlinks(I, ·); F9★ closes the K.λ-free multi-step case; F19 closes the general reachable case. F11's distinction from ASN-0098's V-side discoverable_from is explicitly worked, and Query 5 exhibits the divergence under K.μ⁻. F10's ordering correctly composes ChainIndexEqualsAllocationOrder (within-document) with F10a (cross-document via PrefixOrderingExtension); F10a Case (ii) walks the zero-count balance argument explicitly through four foundation steps.

The worked example covers basic match, transclusion transparency (F6), filtered conjunction (F7), cross-subspace mapping into dom(L) (F12 + S3★), multi-step preservation across V ∖ {K.λ} (F9★), and persistence + growth across K.λ (F11 + F9-λ). Each query verifies specific postconditions against concrete tumbler addresses with documented coverage disjointness.

Edge cases (empty I, empty dom(L), empty endsets at non-type slots, empty constraint set, empty arrangement domain) are explicitly handled. Realizability discharge for F4 universally covers any F1-admitted (endset configuration, I) pair via two K.δ steps to reach `dom(M) ≠ ∅`, then K.λ with freely chosen endsets.

All cross-ASN references are to foundation ASNs (0034, 0036, 0043, 0047, 0053, 0058, 0093, 0098). No reinvented notation. No drift into implementation territory.

VERDICT: CONVERGED
