# Review of ASN-0084

## REVISE

### Issue 1: Notational collision between content store C and cut sequence C
**ASN-0084, throughout**: The symbol C denotes both the content store (Σ.C, referenced as "C' = C" in S0 of ASN-0036) and the cut sequence (C = (c₀, ..., c_{n−1}), in REARRANGE_C and R-PRE(C)).
**Problem**: R-FRAME-P(c) and R-FRAME-S(c) both write "C' = C (S0, ASN-0036)" where C means the content store, while adjacent prose ("Given a cut sequence C…") uses C for the cut sequence. Context disambiguates but every occurrence requires the reader to perform that disambiguation.
**Required**: Rename the cut sequence to a distinct symbol (e.g., K = (c₀, ..., c_{n−1}); operation REARRANGE_K, precondition R-PRE(K)).

### Issue 2: Missing worked example for 4-cut Δ_μ negative sub-case
**ASN-0084, Worked Examples**: Three Δ_μ sub-cases exist for the 4-cut μ-branch:
- w_β > w_α: Δ_μ = +(w_β − w_α) — covered (8-position example)
- w_β = w_α: Δ_μ = 0 — covered (7-position example)
- w_β < w_α: Δ_μ = −(w_α − w_β) — **not covered**
**Problem**: The third sub-case exercises the (−) sign branch of Δ on μ — structurally distinct from the two presented sub-cases. R-DISP handles it symbolically but no concrete trace verifies R-S1, R-S2, R-S3 application or per-position Δ values when middle positions shift backward.
**Required**: Add a worked example with w_α > w_β (e.g., w_α = 3, w_β = 1, w_μ = 2), tracing every clause and verifying Δ_μ = −(w_α − w_β) on each middle V-position.

### Issue 3: R-PRE(v) admitted as redundant but retained
**ASN-0084, R-SP "R-PRE(v) is non-independent"**: "R-PRE(v) is logically implied by R-PRE(iii) ∧ R-PRE(iv) via D-SEQ (ASN-0036). ... Dropping R-PRE(v) while preserving R-PRE(iii) and R-PRE(iv) leaves Q unaffected; R-PRE(v) is stated separately for emphasis."
**Problem**: An explicitly redundant precondition is bookkeeping noise, not specification. "For emphasis" mixes documentation into the precondition lattice. A precondition that is logically implied by the others has no semantic role; consumers cannot distinguish "must check (v)" from "can derive (v)."
**Required**: Either (a) drop R-PRE(v) and let the width bounds follow from R-PRE(iii) ∧ R-PRE(iv) ∧ ASN-0036-invariants as a named *consequence*; or (b) restructure so the width-positivity is primary and cut-coverage is derived. The current dual statement is rigor-deficient.

### Issue 4: Necessity sketch for R-PRE(iii) conflates well-typedness with semantic necessity
**ASN-0084, R-SP "A second counterexample (R-PRE(iii) — CS3 violation)"**: "R-PRE(iv) is now ill-defined as stated (it quantifies over positions in *the* subspace S of the cuts, presupposing CS3); under the most natural reading where R-PRE(iv) is vacuous in the absence of CS3 ... (iv) does not refute the configuration. ... no candidate M'(d) is admissible: the postcondition contract cannot be evaluated."
**Problem**: This argument shows Q is *ill-typed* (the operation has no well-defined postcondition without CS3), not that Q has a counterwitness. A necessity argument should exhibit a state satisfying all other R-PRE conjuncts plus ASN-0036-invariants where Q fails under REARRANGE_C. Relying on "the most natural reading" of one precondition to interpret another precondition's violation is not Dijkstra-grade reasoning.
**Required**: Either (a) reformulate R-PRE(iv) to be unambiguously defined regardless of CS3, then exhibit a witness where Q fails on a concrete equation; or (b) explicitly distinguish CS3 as a well-typedness guard (operation applicability) from preconditions that are necessary for invariant preservation, and label the sketch as a well-typedness argument rather than necessity.

### Issue 5: Δ definition uses NAT-sub on possibly multi-component values, well-typedness deferred to "Mutual exclusivity" paragraph
**ASN-0084, PermutationDisplacement definition**: "Δ(v) = (+, ord(π(v)) − ord(v)) if ord(π(v)) > ord(v); Δ(v) = (−, ord(v) − ord(π(v))) if ord(π(v)) < ord(v)."
**Problem**: For non-S positions at depth m > 2, ord(v) is a tumbler of length m − 1, not an ℕ-element. NAT-sub is on ℕ. The expressions "ord(π(v)) − ord(v)" in the (+) and (−) branches are therefore ill-typed at non-S inputs. The ASN argues the branches don't fire on non-S inputs (the "Mutual exclusivity" paragraph), but the *definition* itself contains expressions whose evaluation is undefined on parts of the domain.
**Required**: Restate the definition with explicit domain conditioning — e.g., define Δ only on V_S(d) (where ord is singleton-identified with ℕ⁺) and stipulate Δ(v) = (0, 0) on non-S by convention. Or: use T1 strict order rather than NAT-sub on ord values where the branch precondition is itself a tumbler-order comparison. The current form requires the reader to construct the well-typedness argument from the mutual-exclusivity prose.

## OUT_OF_SCOPE

### Topic 1: Cross-subspace transposition
REARRANGE_C is scope-restricted to text subspace S = 1; cross-subspace rearrangements are a separate operation class.

### Topic 2: Deeper text subspaces (m_1 > 2)
The ASN exploits the singleton-tumbler identification at depth 2. Deeper text hierarchies are out of scope.

### Topic 3: k-cut rearrangements for k > 4
Generalizations to larger cut counts are explicitly listed as an open question.

### Topic 4: Composition of rearrangements
Whether REARRANGE_C₂ ∘ REARRANGE_C₁ is itself a cut-point rearrangement is an open question.

### Topic 5: Maximality of R-BLK output
B' = R-BLK(B) may not be canonical; characterizing post-rearrangement merges is deferred.

### Topic 6: Necessity of preconditions
The ASN provides sufficiency only; a full weakest-precondition analysis is out of scope.

VERDICT: REVISE
