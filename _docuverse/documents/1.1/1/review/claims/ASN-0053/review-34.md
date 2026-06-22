I read the foundation set and then ASN-0053 as a system: the reach/displacement bridge (WF, WR), the convexity/classification layer (S0, SC), the merge/split inverse pair (S3/S4/S3b/S4a/S5), normalization (S8/S9/S10), and the difference family (S11/S11a–d). The precondition chains into ASN-0034 hold up under inspection: every WF invocation that takes a *reach* endpoint (S1, S3, S4-ρ, S8 emit, S11-ρ, S11c Case 2) first discharges carrier-membership through TumblerAdd's `a ⊕ w ∈ T` and equal-length through S6, and the `divergence(s,r) ≤ #s` precondition for D1/D2 is correctly established from equal length excluding T1's prefix case. The S9 uniqueness case split is exhaustive (both-exist {<,=,>} with the equal/equal sub-case ruled out by TA-LC, plus the two shorter-sequence cases), and TA-LC's positivity/action-point preconditions are genuinely discharged from well-formedness rather than from mere non-emptiness. S5's TA-assoc→TA-LC chain checks out, including `k_{d'} ≤ #d` via level-uniformity of λ. I found no broken precondition chain, missing case, or unsound step. The findings below are framing/noise and a documentation inaccuracy.

### S6 carries why-the-axiom-is-needed prose and a use-site inventory
**Class**: OBSERVE
**Foundation**: S6 (LevelConstraint), depending on TumblerAdd
**ASN**: S6 body — "Drop a precondition — say Pos(ℓ) — and s ⊕ ℓ need not be defined, so the length identity has nothing to stand on"; and the Depends note — "This is the sole source of the addition result-length: the in-scope foundations supply only the subtraction length (TumblerSub: #(a ⊖ w) = L) and the round-trip identity (D1...), neither of which yields #(s ⊕ ℓ) = #ℓ for a general width ℓ."
**Issue**: Both passages explain *why* TumblerAdd's result-length identity is the one needed and inventory the alternatives that don't apply, rather than stating what S6 establishes. This is the reviser-drift pattern (axiom prose justifying necessity + use-site inventory) the precise reader must read past to reach the claim.
**What needs resolving**: n/a (OBSERVE)

### S2 / S11d postcondition slots hold defensive meta-prose
**Class**: OBSERVE
**Foundation**: S2 (EmptyDistinction), S11d (GeneralDifferenceBound)
**ASN**: S2 Preconditions — "not the type-incoherent comparison of the tumbler s ⊕ ℓ against #s"; S11d Postconditions — "Achievability is not universality, however: the count is exactly 2 precisely when ⟦β⟧ ⊂ ⟦α⟧ *and* neither boundary coincides... Hence ⟦β⟧ ⊂ ⟦α⟧ (SC case iv) does not by itself force the count to 2."
**Issue**: A postcondition slot asserts what is established; here it instead defends against a misreading (S11d) and pre-empts a type confusion (S2). The content is correct but is argumentation, not a postcondition statement.
**What needs resolving**: n/a (OBSERVE)

### D0 declared "cited" but used by no proof in the ASN
**Class**: OBSERVE
**Foundation**: D0 (DisplacementWellDefined)
**ASN**: Properties Introduced table — "D0 | Displacement well-definedness... | cited"
**Issue**: D0 appears only in the summary table marked "cited," but no proof in the ASN (WF, WR, S4, S5, the reach-function section) invokes it — the round-trip work is done by D1, uniqueness by D2, well-definedness of `s ⊕ ℓ` by TA0. The `#a > #b → a ⊕ (b ⊖ a) ≠ b` clause D0 uniquely adds is never reachable here since every constructed span is level-uniform (equal lengths). The dependency declaration overstates what is actually consumed.
**What needs resolving**: n/a (OBSERVE)

### "span" vs "well-formed span" is used without a fixed convention
**Class**: OBSERVE
**Foundation**: T12 (SpanWellDefinedness), TA-strict
**ASN**: Opening — "by TA-strict every span is non-empty" (presupposes well-formedness of *every* span); S2 — "The empty set is not the denotation of any span. Every well-formed span denotes a non-empty set" (distinguishes "any span" from "well-formed span"); many claims qualify "well-formed level-uniform span" while SC and S3a say only "spans."
**Issue**: The term "span" is never formally defined, and the well-formedness qualifier appears inconsistently — sometimes treated as inherent to "span," sometimes as a distinguishing predicate. Soundness is not affected (every claim that needs Pos(ℓ)/actionPoint bounds states "well-formed"), but a downstream consumer cannot tell from the bare word "span" whether T12's preconditions are assumed.
**What needs resolving**: n/a (OBSERVE)

VERDICT: OBSERVE