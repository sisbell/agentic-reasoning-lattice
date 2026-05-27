# Review of ASN-0099

## REVISE

(none)

## OUT_OF_SCOPE

The ASN's "What We Have Not Specified" section adequately catalogues forward-looking topics (computation procedure, replication, caching, access control, FOLLOWLINK inverse, queries outside dom(C) ∪ dom(L), combined filtered+scoped operation). Nothing additional to flag.

## Notes on Examination

I worked through the major derivations and witness constructions. Findings:

**F4 realizability witnesses (Strengthenings 1–3, Weakenings 1–2):** Each witness checks out under the substrate axioms. Strengthening 1's `α.0 ∉ I = {α}` argument is sound (α.0 ∈ T per T0; α ≼ α.0; lengths differ so α.0 ≠ α). Strengthening 2's slot-3 placement to avoid the L3 mandate is correctly motivated. The "Populating all three slots is essential" note for Strengthening 1 is necessary (without it, the empty-slot vacuous-subset would mask distinction).

**F9 derivation chain:** F8 → ComprehensionInvariantUnderΣL → F9 holds. The split between A1a (published-frame, K.μ~ and K.μ⁺_L) and A1b (closed-world, K.μ⁺/K.μ⁻/K.ρ) is correctly scoped against the substrate's published frames. A1b's convention-grounded status is transparently surfaced (appendix + claim table tag), and is genuinely load-bearing — LP3/L12 alone yields only monotonicity, not the equality F9-cor asserts. The author's choice to commit methodologically rather than revise the substrate is justified in the appendix on scope and separability grounds.

**F9-λ:** The disjoint-union form is correctly derived from K.λ's freshness precondition + L12 + PerLinkInvarianceUnderValuePreservation. The note that ComprehensionInvariantUnderΣL is *not* applicable (since dom(L) grows) and the per-link primitive is load-bearing is sharp.

**F10a Case (ii):** The four-step zero-count balance argument from M0 + T4 + Prefix + T0/NAT-discrete correctly derives `d₂[#d₁+1] ≥ 1` and lifts to anchor non-nesting. The T1 case (i) application at position #d₁+1 is sound.

**Worked example (Queries 1–6):** All six queries check against the substrate preconditions and post-state predictions. Query 5's five-step V ∖ {K.λ} chain correctly exercises A1a + A1b across K.δ, K.α, K.μ⁺, K.ρ, K.μ⁻ and demonstrates the I-side vs V-side divergence (the load-bearing distinction between F11's I-side persistence and ASN-0098's V-side discoverable_from). Query 6's K.λ extension correctly exercises F11 + F9-λ + F19 together — including the subspace separation argument for ℓ_new's non-match against {α₂} and its match against {α_c}.

**Meta-lemma factoring:** ComprehensionInvariantUnderΣL and PerLinkInvarianceUnderValuePreservation are correctly factored. F11 and F19-filt correctly use the per-link primitive (since K.λ may grow dom(L) along the reachable sequence), while F8, F9, F15, F17 use the comprehension-level form (which requires full Σ.L = Σ'.L).

**ChainIndexEqualsAllocationOrder sub-lemma:** Correctly identifies T1 rank within a home document with chain index and K.λ event count, via ChainMembershipForOrigin (contiguous prefix) + ChainEnumerationInjectivity (strict T1 ordering) + K.λ's subsequent-emission precondition.

**Edge cases covered:** Empty I, empty Σ.L, empty constraint set, empty constraint target J = ∅, empty document arrangement, single-element queries, cross-document transclusion, cross-subspace queries (Query 4's link-image), V-positions outside dom(Σ.M(d)) (silent projection), out-of-arity filter constraints (i > |Σ.L(a)| guard).

**Cross-ASN references:** All citations target foundation ASNs (ASN-0034, 0036, 0043, 0047, 0058, 0093, 0098). No non-foundation references.

VERDICT: CONVERGED
