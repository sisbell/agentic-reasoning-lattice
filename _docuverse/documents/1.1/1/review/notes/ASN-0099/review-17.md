# Review of ASN-0099

## REVISE

### Issue 1: F4 misattributes witness realizability to L9
**ASN-0099, F4 (MatchFormulaUniqueness)**: "L9 (TypeGhostPermission, ASN-0043) supplies, for every arity `N ≥ 3`, a conforming extension `Σ'` containing a link whose endsets are specified freely (its existential over arity covers the arity-3 standard-triple shape used by every witness here)..."
**Problem**: L9's statement constrains the *type endset* (slot 3) to reference an address *outside* `dom(Σ.C) ∪ dom(Σ.L)`. It does not supply extensions "whose endsets are specified freely" — the other endsets in L9's witness are existentially produced by the L9 construction, not selected by the F4 author. The F4 witnesses construct specific slot-1 and slot-2 coverages (canonical prefix subtrees over arbitrary `α ∈ T`), which L9 does not control.
**Required**: Cite K.λ (LinkAllocation, ASN-0093) directly. K.λ's precondition `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅` together with L4 (EndsetGenerality, ASN-0043) — which permits any address in `T` as a span start — is the actual realizability mechanism. L11b is also irrelevant to single-witness realizability and should be dropped from the citation chain unless multi-witness coexistence is needed.

### Issue 2: F4 title and scope mismatch — addresses minimality, not full uniqueness
**ASN-0099, F4 (MatchFormulaUniqueness)**: "The match predicate of F1 is uniquely fixed by the reader's promise. No strengthened condition ... is a refinement of F1. Any such alternative defines a different match predicate and therefore (via F2 ∧ F3) a different — and, with respect to F1, incomplete — conforming result set."
**Problem**: F4 argues only against *strengthenings* (predicates that exclude pairs F1 admits, yielding incomplete results). It does not address *weakenings* (predicates that admit pairs F1 excludes, yielding unsound results). The title "Uniqueness" suggests both directions; the body delivers only one. The implicit reading — that F3 rules out weakenings while F4 rules out strengthenings, so together they pin F1 — is not stated.
**Required**: Either retitle to "MatchFormulaMinimality" and explicitly note that the weakening direction is discharged by F3 (soundness), or extend F4's argument to cover both directions symmetrically. The reader should not have to infer the division of labor.

### Issue 3: Edge case `J = ∅` in filtered queries not discussed
**ASN-0099, Endset Filtering section**: The empty-boundary discussion covers `I = ∅`, `dom(Σ.L) = ∅`, and `C = ∅`, but omits the case where a filter constraint `(i, J)` has `J = ∅`.
**Problem**: When `J = ∅` for some `(i, J) ∈ C`, the conjunct `coverage(eᵢ) ∩ ∅ = ∅ ≠ ∅` is false at every link, so the universal fails uniformly and `findlinks_filtered(C, Σ) = ∅`. This is a meaningful boundary distinct from the "empty endset at non-type slot" case already discussed (which is `Σ.L(a).eᵢ = ∅`, a property of the link, not the query). The text is silent on the query-side empty.
**Required**: Add a clause to the boundary discussion noting that any constraint with `J = ∅` is unsatisfiable and renders the filtered query result empty regardless of the rest of `C`.

### Issue 4: F12 type signature ambiguity at the `findlinks_V` precondition
**ASN-0099, definition of `findlinks_V` under F12**: "F12 *defines* `findlinks_V` rather than asserting a substantive identity ... The single precondition is inherited from `image`'s `defined when` clause — `findlinks_V` is well-formed precisely when `image(R, d, Σ)` is."
**Problem**: The text says the precondition is *inherited from `image`*, which has `defined when d ∈ dom(Σ.M)`. But `findlinks_V`'s declared signature at F12 also says "defined when `d ∈ dom(Σ.M)`". The relationship between the precondition restatement and the F12 definitional clause is not crisp — is the precondition a separate well-formedness constraint, or is it just `image`'s clause re-exhibited? When V-positions in `R` lie outside `dom(Σ.M(d))`, the silent projection (also discussed) handles them; but the document-level precondition `d ∈ dom(Σ.M)` is a hard requirement.
**Required**: Clarify whether `findlinks_V(R, d, Σ)` for `d ∉ dom(Σ.M)` is (a) undefined, (b) silently empty, or (c) signalled as an error. The current text leans (a) but does not say so explicitly, and the worked example does not exercise the `d ∉ dom(Σ.M)` case.

### Issue 5: Cross-document anchor ordering relies on CrossDocDisjointness for ancestor-descendant case
**ASN-0099, F10 derivation (T1 case (ii) for versions)**: "For two distinct documents `d₁ ≠ d₂`, CrossDocDisjointness (ASN-0093) supplies that `b_L(d₁)` and `b_L(d₂)` are non-nesting under `≼`."
**Problem**: ASN-0093's CrossDocDisjointness lemma is stated for any two distinct documents, but the F10 derivation invokes it specifically for the version-extension case `d₁ ≺ d₂` (T1 case (ii)). The derivation then independently re-derives the non-nesting from zero-count balance (correctly). It is unclear whether F10 relies on the foundation lemma (which would close the case) or re-establishes it locally (in which case the citation is redundant). The two routes coexist without clear precedence.
**Required**: Either drop the local re-derivation and cite CrossDocDisjointness as the sole source, or treat the local derivation as the load-bearing argument (and demote the citation to a parenthetical agreement). The current text reads as if both are needed.

### Issue 6: A1 introduces a load-bearing assumption about prose of another ASN
**ASN-0099, A1 (EffectClauseExhaustivity)**: A1 is admitted to be "transient" pending ASN-0047 revision, but the F9 derivation for K.μ⁺, K.μ⁻, and the F9-cor derivation for K.ρ all rest on A1.
**Problem**: A1 reads ASN-0047's frame-clause silence as binding preservation of unmentioned state components — but ASN-0047 publishes frame clauses that do not name `L'` for K.μ⁺, K.μ⁻, or K.ρ. A1 imports a reading that is *not* explicit in ASN-0047's text. The ASN handles this carefully (scope-bounded, transience flagged, resolution proposed), but the dependency is substantive: every claim that survives an edit relies on a single transient axiom about another ASN's exposition. If ASN-0047 were ever amended in a way that intentionally left `L` unchanged (without adding the `L' = L` conjunct), A1 would still extract the preservation — possibly incorrectly.
**Required**: Either (a) flag in Open Questions that A1 must be retired by ASN-0047 revision before ASN-0099 itself converges (making the convergence of ASN-0099 contingent on ASN-0047 revision), or (b) restate F9's K.μ⁺/K.μ⁻ derivations using L12 alone — without A1 — by exhibiting that K.μ⁺ and K.μ⁻ do not add to `dom(L)` through a direct argument over their effect clauses (which assert nothing about L), so the L12 inclusion `Σ.L ⊆ Σ'.L` combined with `dom(Σ'.L) ⊆ dom(Σ.L)` (derived from "K.λ is the unique link-adding operation in V") closes the equality without an exhaustivity premise. The latter path is cleaner and more direct.

## OUT_OF_SCOPE

### Topic 1: Distributed completeness across partitioned link stores
**Why out of scope**: Acknowledged in Open Questions. Multi-instance partition tolerance is future territory.

### Topic 2: Inverse direction (FOLLOWLINK / RETRIEVEENDSETS)
**Why out of scope**: The ASN explicitly defers this to its own specification.

### Topic 3: Access control formalization
**Why out of scope**: Noted as orthogonal scope filter; deferred.

### Topic 4: Implementation procedure for computing the result
**Why out of scope**: The spec is index-agnostic by design; conformance is exhausted by F2 ∧ F3.

### Topic 5: Timing semantics on K.λ visibility windows
**Why out of scope**: Open Question 6; current spec relies on SequentialTransitionAxiom for atomicity.

### Topic 6: Behaviour when `I` includes addresses outside `dom(Σ.C) ∪ dom(Σ.L)`
**Why out of scope**: The ASN flags this in "What We Have Not Specified" as unsettled.

VERDICT: REVISE
