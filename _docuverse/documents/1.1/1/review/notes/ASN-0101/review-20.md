# Review of ASN-0101

## REVISE

### Issue 1: History-sequence formal predicate is not the load-bearing discriminator

**ASN-0101, "The operation" section**: "equivalently, the predicate `(E i : 0 ≤ i ≤ n ∧ Σ_i = Σ_mid)` over the post-composite history sequence holds. DEL as a single elementary transition extends the sequence by exactly one atomic state... the corresponding membership predicate `(E i : 0 ≤ i ≤ n ∧ Σ_i = Σ_mid)` does *not* hold..."

**Problem**: The predicate can hold for the post-DEL sequence when Σ_mid coincides with Σ_pre or Σ_post — for example, when K.μ~ permutes two V-positions that both map to the same I-address (CL-UNIQ does not enforce uniqueness in the content subspace), the resulting M_mid(d) is observably equal to M(d). The author acknowledges this in the parenthetical that follows and falls back on "sequence length" as the load-bearing argument, but the body of the argument relies on the membership predicate.

**Required**: Reframe the formal argument around explicit sequence length (post-composite has length 3 from Σ_pre, post-DEL has length 2) rather than the membership predicate. The "(E i : Σ_i = Σ_mid)" formulation should be removed or recast as a consequence of length differing, not as the discriminator itself.

### Issue 2: D11 omits cross-document cardinality wp

**ASN-0101, D11**: The three wps state (a) discoverability from d, (b) discoverability from d'' ≠ d, and (c) cardinality from d. The cardinality wp for d'' ≠ d is implicit (the projection from any other document is invariant by D9 first bullet, so the cardinality predicate reduces to the pre-state predicate) but not stated.

**Problem**: For completeness and symmetry with the discoverability case, the cross-document cardinality wp should be explicit: `wp(DEL[d, σ], |project(L(ℓ).eᵢ, d'', ·)| = k) ≡ |project(L(ℓ).eᵢ, d'', Σ)| = k` for d'' ≠ d, d'' ∈ dom(M).

**Required**: Add the cross-document cardinality wp as a fourth bullet in D11.

### Issue 3: Relationship between ASN-0098 LP-family and DEL not made explicit

**ASN-0101, throughout**: D7, D9, D11 cite D2, D3, D5, D6 directly. ASN-0098's LP2★, LP3★, LP4–LP14 are stated for "every transition" or "every reachable state sequence" in the ASN-0047 + ASN-0093 vocabulary. DEL is a new transition kind admitted into the vocabulary by D10.

**Problem**: Strictly, ASN-0098's LP-Comp note enumerates an exhaustive case-analysis over the ASN-0047 + ASN-0093 vocabulary that does not include DEL. The reader cannot determine whether LP2★, LP3★, LP13 (etc.) automatically extend to DEL-containing sequences, or whether new lemmas are required. The author's D-claims supply the needed properties directly, but the relationship is not stated.

**Required**: Add a paragraph (in D10 or a separate claim) addressing how the LP-family extends to DEL — for instance, LP2★/LP3★/LP13 extend trivially via D3 (since L' = L), LP4–LP11 are covered for DEL by D5/D6/D9, and LP12/LP12a are supplanted by D11.

### Issue 4: "K.μ⁻ + K.μ~" naming is order-ambiguous

**ASN-0101, "The operation" section**: The composite-substitute strategy is repeatedly called "the K.μ⁻ + K.μ~ composite" or "the K.μ⁻ + K.μ~ composite-substitute strategy", but the prose specifies the order as K.μ~ first, then K.μ⁻.

**Problem**: The "+" notation suggests commutativity, but the composite is order-sensitive. A reader scanning the section may misread the order.

**Required**: Use sequence notation — "K.μ~; K.μ⁻", "K.μ~-then-K.μ⁻", or simply "the two-step K.μ~/K.μ⁻ composite" — consistently.

### Issue 5: D8 Group (iii) P4★ discharge chain is compressed

**ASN-0101, D8 Group (iii) justification**: "P4★ by the conjunction `R' = R` and `Contains_C(Σ') ⊆ Contains_C(Σ)` — the second inclusion is established by lifting each post-state witness to a pre-state witness."

**Problem**: The conclusion Contains_C(Σ') ⊆ R' = R requires three steps: Contains_C(Σ') ⊆ Contains_C(Σ) (lifting), then Contains_C(Σ) ⊆ R (pre-state P4★), then R = R' (D0 frame). The author lists two of three; the middle step is omitted.

**Required**: Make the chain explicit — Contains_C(Σ') ⊆ Contains_C(Σ) ⊆ R = R'.

### Issue 6: Empty arrangement / freshly-registered document case not addressed

**ASN-0101, D0 preconditions**: `s ∈ V_S(d)` is stated but the consequence — that DEL cannot apply to a document with M(d) = ∅ — is not made explicit.

**Problem**: A document freshly created by K.σ (ASN-0093) or by K.δ-IsDocument (ASN-0047) has M(d) = ∅, so V_S(d) = ∅ for both subspaces. DEL is then inapplicable. A reader may wonder how the operation interacts with newly-registered documents.

**Required**: Add a short note (in D0 or in the boundary cases section) stating that DEL requires V_S(d) ≠ ∅ for some subspace S, and hence cannot apply immediately after K.σ or K.δ-IsDocument until at least one V-position has been placed.

## OUT_OF_SCOPE

### Topic 1: Re-canonicalization of bundle decompositions across the gap

**Why out of scope**: The author observes that formerly non-adjacent runs may become V-adjacent (and possibly I-adjacent) after DEL, raising the question of whether implementations should reconcile them via the bundle-algebra merge rules. The ASN correctly discharges S8★ via the singleton decomposition independent of reconciliation, and notes that M11/M12 of ASN-0058 supply abstract existence/uniqueness of the maximally merged form. When/how implementations should reconcile is downstream of DEL's elementary specification.

### Topic 2: Multi-step composite analysis combining DEL with allocation

**Why out of scope**: D10 establishes single-step vacuity of J0/J1★/J1'★ and exhibits a counterexample (K.α + K.μ⁺ + DEL) that breaks composite-level J0. A full theory of valid composites containing DEL — including which composite structures preserve which coupling constraints — is downstream work.

### Topic 3: Recoverability via versioning composites

**Why out of scope**: The "note on recoverability and historical reconstruction" section correctly identifies that DEL supplies the *substrate* for recoverability (via D2 + D5) but not the *mechanism* (which is versioning, e.g., via J4 ForkComposite applied before DEL). Specifying the recoverability composites and their interaction with DEL is downstream work.

VERDICT: REVISE
