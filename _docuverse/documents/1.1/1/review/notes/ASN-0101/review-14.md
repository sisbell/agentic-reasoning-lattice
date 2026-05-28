# Review of ASN-0101

I've worked through the DELETE operation specification, the gap-closing shift mechanism, the boundary cases, both worked examples, and each of the eleven claims. The substantive content is sound — the operation specification is complete, the shift function is well-defined and bijective, the frame conditions are precise, and the invariant preservation arguments cover the foundation invariants. The worked examples correctly verify the predicted post-states. However, several proofs have prose-clarity issues that should be tightened.

## REVISE

### Issue 1: D1 order-preservation proof has a setup sentence that isn't directly used

**ASN-0101, D1 justification**: "By TS1 (ShiftOrderPreservation, ASN-0034), u₁ < u₂ would imply shift(u₁, n) < shift(u₂, n), i.e., v₁ < v₂. The contrapositive at the order-preserving inverse: from v₁ < v₂ and equal lengths, T1 trichotomy on u₁, u₂ yields one of u₁ < u₂, u₁ = u₂, or u₂ < u₁."

**Problem**: The "u₁ < u₂ would imply..." sentence sets up the *forward* direction of TS1 (which is our conclusion, not a hypothesis). The actual proof eliminates the case u₂ < u₁ using TS1 in that direction, not via the forward implication stated. The "contrapositive at the order-preserving inverse" framing is confusing because no contrapositive is actually used.

**Required**: Restructure so TS1's role is clear: trichotomy gives u₁ < u₂, u₁ = u₂, or u₂ < u₁; eliminate u₁ = u₂ by TS2 (would give v₁ = v₂, contradicting v₁ < v₂); eliminate u₂ < u₁ by TS1 (would give v₂ < v₁, contradicting v₁ < v₂); conclude u₁ < u₂. Drop the redundant forward-direction setup.

### Issue 2: D11 wp negation uses an unstated determinism assumption

**ASN-0101, D11**: "Equivalently, the negation: `wp(DEL[d, σ], ¬Q_disc(ℓ, d)) ≡ (A i : 1 ≤ i ≤ |L(ℓ)| : project(L(ℓ).eᵢ, d, Σ) ⊆ X)`"

**Problem**: The equivalence `wp(op, ¬Q) ≡ ¬wp(op, Q)` holds for deterministic operations but not in general. The ASN does establish DEL is functional (under D0's specification, M'(d) is uniquely determined by the pre-state and σ), but never explicitly invokes this to license the negation equivalence in D11.

**Required**: Either prove DEL is deterministic (a one-line argument: M'(d) is constructed from M(d), σ_d, and the pre-state value of M(d) at each source position — each component uniquely determined), or derive the negation wp directly from the post-condition without going through wp(op, ¬Q) = ¬wp(op, Q). A statement that DEL is deterministic and that this licenses the negation equivalence would suffice.

### Issue 3: D8 Group (iii) P4★ derivation is too compressed

**ASN-0101, D8 Group (iii) justification**: "P4★ by the conjunction R' = R and Contains_C(Σ') ⊆ Contains_C(Σ) (DELETE can only shrink the content-subspace range, so historical containment is preserved)"

**Problem**: The inclusion `Contains_C(Σ') ⊆ Contains_C(Σ)` is asserted in passing. For a reader to verify it requires tracing: every post-state content-subspace witness (v, a) with v ∈ V_{s_C}(M'(d)) and M'(d)(v) = a corresponds to a pre-state witness — either the same v ∈ Λ (giving same a) or u ∈ Ρ with σ_d(u) = v (giving M(d)(u) = a, so (a, d) ∈ Contains_C(Σ) via u). Witnesses with v ∈ X disappear. This is a multi-step argument compressed into a parenthetical.

**Required**: Expand the parenthetical to a sentence or two showing the source correspondence (post-state witnesses lift to pre-state witnesses via Λ-identity or σ_d-inverse) explicitly, so the inclusion `Contains_C(Σ') ⊆ Contains_C(Σ)` is derived rather than asserted.

### Issue 4: D8 S2 disjointness routing is more verbose than the argument requires

**ASN-0101, D8 Group (i) justification**: The disjointness `Λ ∩ Q = ∅` is established via two named routes (*Q non-empty route — integer-range disjointness* and *Q empty route — trivially disjoint*) with explicit arithmetic conditions distinguishing them.

**Problem**: The standard argument is uniform: Λ has last component ≤ p−1; Q (when non-empty) has last component ≥ p; so the integer ranges are disjoint when Q is non-empty, and trivially when empty. The two-route presentation, with explicit identification of the boundary `n = n_S − p + 1`, adds bookkeeping without sharpening the conclusion. The "Q empty route" parenthetical "(the maximum permitted by D0's containment bound)" is also distracting — the case is handled by a single line in the unified argument.

**Required**: Consolidate to a single sentence: "Λ ∩ Q = ∅ because Λ-positions have last component in {1, ..., p−1} and Q-positions (when non-empty) have last component in {p, ..., n_S−n}, which is disjoint from {1, ..., p−1}; when Q is empty, the intersection is trivially empty."

### Issue 5: The "boundary case `v = r` maps to `σ_d(r) = s`" claim implicitly assumes Ρ ≠ ∅

**ASN-0101, "What shifts" section**: "The boundary case v = r = [S, 1, ..., 1, p + n] maps to σ_d(r) = [S, 1, ..., 1, p] = s, so the first shifted position lands exactly where the deletion began — closing the gap precisely."

**Problem**: The statement implicitly assumes r ∈ Ρ (so σ_d(r) is defined). When p + n = n_S + 1 (deletion at the end), r ∉ V_S(d) and Ρ = ∅, so σ_d(r) is not defined. The reader has to figure this out independently — the prose suggests the boundary holds always.

**Required**: Add a qualifier: "When Ρ ≠ ∅ (equivalently, p + n ≤ n_S), the smallest element of Ρ is r itself, and σ_d(r) = s — the first shifted position lands exactly where the deletion began."

### Issue 6: D9 second bullet quantifier compactness

**ASN-0101, D9 second bullet**: "If d'' = d, restricted to subspace S' ≠ S: project(L'(ℓ).eᵢ, d, Σ') ∩ V_{S'}(d) = project(L(ℓ).eᵢ, d, Σ) ∩ V_{S'}(d)."

**Problem**: The bullet says "subspace S' ≠ S" but reads as if quantified over a particular S'. In the two-subspace framework (s_C, s_L) there is exactly one such S', but the prose doesn't make this explicit, leaving a reader to wonder whether "every S' ≠ S" or "the unique S' ≠ S" is intended.

**Required**: Either name the variable scope ("the unique S' ∈ {s_C, s_L} with S' ≠ S") or universally quantify ("for every S' ∈ {s_C, s_L} with S' ≠ S"). The current phrasing is ambiguous in a way that becomes load-bearing if the substrate is later generalised to more than two subspaces.

## OUT_OF_SCOPE

### Topic 1: Composite validity diagnostics under multi-step composites containing DEL

**Why out of scope**: D10 correctly identifies that DEL inside a multi-step composite can break composite-level J0 (the K.α → K.μ⁺ → DEL example). A diagnostic apparatus — decidable predicates for when a composite containing DEL satisfies J0/J1★/J1'★ at its endpoints — belongs in a separate ASN addressing composite validity more generally, not as additional content for DEL itself.

### Topic 2: Reversibility and view-equivalence of post-DELETE states

**Why out of scope**: The open question "Under what condition on the post-DELETE arrangement does a subsequent operation observe a state indistinguishable from a state reached without the DELETE — that is, when is DELETE fully reversible relative to a given observer's view?" is a future ASN's concern. It requires both INSERT (out of scope here) and a formal notion of observer view (not yet specified).

### Topic 3: Re-merging adjacent runs after gap closure

**Why out of scope**: The ASN correctly notes that after a deletion, two previously non-adjacent runs that become V-adjacent are not automatically merged by the abstract specification (and Gregory's implementation confirms this). Whether subsequent operations should re-canonicalise the arrangement representation belongs in a bundle-algebra or arrangement-canonicalisation ASN, not DEL.

VERDICT: REVISE
