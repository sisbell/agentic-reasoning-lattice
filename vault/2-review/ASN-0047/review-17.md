# Review of ASN-0047

## REVISE

### Issue 1: Properties table mislabels K.μ~ as elementary transition
**ASN-0047, Properties Introduced table, J3 row**: "K.μ~ as elementary transition requires no coupling"
**Problem**: The body text correctly identifies K.μ~ as a "distinguished composite, not a primitive transition" (Elementary transitions section) and J3's own prose says "The distinguished composite K.μ~ is likewise self-sufficient." The properties table contradicts this by calling it an elementary transition.
**Required**: Change the J3 row to "K.μ~ as distinguished composite requires no coupling: C' = C ∧ E' = E ∧ R' = R".

### Issue 2: Valid composite definition includes derived conditions
**ASN-0047, Coupling and isolation, Definition (Valid composite transition)**: "A composite transition Σ → Σ' is *valid* iff it is a finite sequence of elementary transitions... satisfying three conditions: (1)... (2)... (3a)... (3b)..."
**Problem**: Condition (3b) is stated as part of the definition, then immediately acknowledged as derivable: "Conditions (3b) follow from (1), (2), and (3a)." A definition should state necessary and sufficient conditions; including a derivable consequence inflates what a reader must verify to show validity and obscures which conditions are primitive. Someone checking whether a composite is valid would waste effort verifying (3b) when (1)+(2)+(3a) already suffice.
**Required**: Remove (3b) from the definition. State it as a separate theorem: "Every valid composite transition produces a final state satisfying P6, P7, P8, S2, S3, S8a, S8-depth, S8-fin, and Contains(Σ') ⊆ R'." The derivation references (P4, P6, P7, P8 proofs and the elementary-transition S-invariant analysis) already exist in the ASN — they just need to serve a theorem rather than justify a redundant definition clause.

### Issue 3: K.μ~ conflates multiset preservation with set equality
**ASN-0047, Elementary transitions, K.μ~**: "The multiset of referenced I-addresses is preserved — formally, ran(M'(d)) = ran(M(d)), immediate from the bijection."
**Problem**: `ran` is a set, not a multiset. The bijection `M'(d)(π(v)) = M(d)(v)` preserves the full multiset of I-addresses (each V-position retains its value), which is strictly stronger than set equality of ranges. The sentence presents set equality as the formalization of multiset preservation, collapsing the distinction. In a specification that downstream ASNs will build on, the difference matters — multiplicity is relevant to span decomposition (S8) and to reasoning about how many V-positions reference a given I-address.
**Required**: State the two claims separately. The bijection definition already captures multiset preservation; note that ran equality is a corollary. For example: "The bijection preserves the mapping pointwise — each V-position retains its I-address — so the multiset of referenced I-addresses is identical. As a corollary, ran(M'(d)) = ran(M(d))."

### Issue 4: P4 proof uses equality where only inclusion holds
**ASN-0047, Coupling and isolation, P4 proof, K.μ⁺ case**: "K.μ⁺ yields Contains(Σ') = Contains(Σ) ∪ Δ."
**Problem**: This equality holds only when no K.μ⁻ acts on any document in the same composite. If K.μ⁻ removes an I-address from some document's range, the corresponding pair leaves Contains(Σ') but remains in Contains(Σ) ∪ Δ, making the left side strictly smaller. The correct statement is Contains(Σ') ⊆ Contains(Σ) ∪ Δ, which suffices for the conclusion: Contains(Σ) ⊆ R ⊆ R' (by IH and P2), Δ ⊆ R' (by J1), so Contains(Σ') ⊆ R'. The proof reaches the right conclusion, but the intermediate claim is imprecise.
**Required**: Replace `=` with `⊆` in that sentence: "Contains(Σ') ⊆ Contains(Σ) ∪ Δ." The subsequent two-subcase analysis and conclusion are unchanged.

## OUT_OF_SCOPE

### Topic 1: Distinguishing links from documents within E_doc
**Why out of scope**: The ASN explicitly defers this: "The structural distinction between documents and links — endset semantics, subspace layout — belongs to a separate analysis." At the transition level both participate identically; endset-specific invariants (e.g., link discoverability under K.μ⁻) require their own ASN.

### Topic 2: Concurrent composite transitions
**Why out of scope**: The ASN models composites as sequential finite sequences from a single initial state. Two agents independently composing transitions from the same state — and the conflict/merge semantics this entails — is a concurrency concern explicitly excluded from scope.

VERDICT: REVISE
