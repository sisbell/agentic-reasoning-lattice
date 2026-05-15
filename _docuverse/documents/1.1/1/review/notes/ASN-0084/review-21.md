# Review of ASN-0084

## REVISE

### Issue 1: Imprecise citation of OrdinalShift's domain
**ASN-0084, Identification paragraph**: "OrdinalShift on a singleton tumbler, `shift([k], j) = [k + j]` for j ∈ ℕ (ASN-0034)"
**Problem**: ASN-0034's OrdinalShift requires `n ≥ 1` as a precondition. The case `j = 0` is not covered by OrdinalShift — it is supplied by this ASN's own identity convention ("By convention, `c₀ + 0 = c₀`"). The phrasing "for j ∈ ℕ (ASN-0034)" conflates the foundation contract with the ASN's extension.
**Required**: Split the statement: "for j ≥ 1, OrdinalShift (ASN-0034) gives `shift([k], j) = [k + j]`; the case j = 0 is covered by the identity convention below." The same care is needed wherever TS3 is invoked at boundary offsets (e.g., Split/Merge verification, R-COMM derivations, canonical-decomposition step b), since TS3 itself requires both shift amounts ≥ 1.

### Issue 2: Subspace confinement omits the OrdShiftHom (b) citation
**ASN-0084, "Consequences of R-PRE"**: "The rearrangement constructions in this ASN (PivotPostcondition, SwapPostcondition) only assign new I-addresses to V-positions in V_S(d) and leave all other positions fixed (R-FRAME-P, R-FRAME-S), so no position outside subspace S is ever produced. This is a derived consequence of CS3, CS4, and S8a (positivity of ordinals, ASN-0036), not a separate verification obligation."
**Problem**: The cited dependencies (CS3, CS4, S8a) do not, by themselves, establish that all positions named in R-P1, R-P2, R-S1, R-S2, R-S3 remain in subspace S. The load-bearing fact is OrdShiftHom (b) from ASN-0036 — `subspace(shift(v, n)) = subspace(v)` — which guarantees that `c₀ + j`, `c₁ + j`, `c₂ + j` all retain subspace S because the cuts have subspace S (CS3). S8a is about ordinal positivity, not subspace preservation.
**Required**: Cite OrdShiftHom (b) as the source of subspace preservation under ordinal shift; CS3 only fixes the subspace of the cuts themselves.

### Issue 3: R-PRE omits w_μ ≥ 1 for the 4-cut case
**ASN-0084, R-PRE clause (v)**: "Both transposed regions are non-empty: w_α ≥ 1 and w_β ≥ 1."
**Problem**: For n = 4, the proof of R-SWP requires `w_μ ≥ 1` to establish pairwise disjointness of the three clause ranges. The fact `w_μ ≥ 1` is derivable (CS2 forces c₁ < c₂; R-PRE(iv) makes the interval [c₁, c₂) ∩ V_S(d) non-empty), but R-PRE does not list it. R-SWP's proof inlines the derivation ("CS2 forces c₁ < c₂, so w_μ ≥ 1"), but this should be either an R-PRE clause for n = 4 or a "Consequences of R-PRE" bullet alongside the subspace-confinement consequence.
**Required**: Either add a "(vi) For n = 4, w_μ ≥ 1" clause to R-PRE, or hoist the derivation `w_μ ≥ 1` into the Consequences of R-PRE so that R-SWP, R-DISP, and R-BLK can cite it uniformly rather than re-deriving it inline.

### Issue 4: Compressed bounds in canonical decomposition step (b)
**ASN-0084, CanonicalRunDecomposition step (b), v₁ = v₂ sub-proof**: "The position [S, ord(v₁) − 1] lies in V(b₂): ord(v₂) ≤ ord(v₁) − 1 < ord(v₂) + n₂."
**Problem**: The right inequality `ord(v₁) − 1 < ord(v₂) + n₂` is asserted without derivation. The argument requires: from `w = v₁ + k₁ = v₂ + k₂` we get `k₂ = p + k₁ ≥ p`; from `w ∈ V(b₂)` we have `k₂ < n₂`; hence `p ≤ k₂ < n₂`, so `p − 1 < n₂`, so `ord(v₁) − 1 = ord(v₂) + p − 1 < ord(v₂) + n₂`. Also missing: `ord(v₁) ≥ 2` (needed to make `ord(v₁) − 1 ≥ 1` so the position lies in V_S(d) by D-SEQ), which follows from `ord(v₁) > ord(v₂) ≥ 1`.
**Required**: Show the chain `p ≤ k₂ < n₂` explicitly, and note `ord(v₁) − 1 ≥ 1` (so NAT-sub is on its defined domain and the position is in V_S(d)). The same step then transfers cleanly to the symmetric `n₁ = n₂` case.

### Issue 5: Signed-magnitude carrier arithmetic undefined
**ASN-0084, PermutationDisplacement definition**: "Sums `+m + (−n)` and the total-displacement zero identity are interpreted under this carrier — see the closing paragraph of this section."
**Problem**: The closing paragraph counts "forward totals" and "backward totals" using sums and products (`w_α · w_β`, etc.) on the signed-magnitude carrier `{+, −, 0} × ℕ`, but neither addition nor multiplication is defined on this carrier. The carrier admits two natural choices (e.g., `(+, m) + (−, n) = (+, m − n)` when m ≥ n, etc.) but the ASN selects neither. The "total-displacement zero identity" claim — "the signed totals cancel — a necessary consequence of π being a bijection on a contiguous range" — is informal commentary, not a derived consequence.
**Required**: Either (a) define `+` and `·` on the signed-magnitude carrier and discharge the cancellation as a formal lemma, or (b) explicitly demote the closing-paragraph discussion to informal commentary and remove the "necessary consequence" language. The main lemmas (R-DISP, R-PPERM, R-SPERM) do not depend on it, so demotion is the lighter fix.

### Issue 6: R-BLK Phase 1 "later cut in right-hand piece" claim not derived
**ASN-0084, R-BLK Phase 1**: "When a later cut falls in a run already split by an earlier (strictly smaller) cut, it necessarily falls in the right-hand piece — CS2's strict ordering guarantees this."
**Problem**: The claim is correct but not proved. The derivation: at step i, cut c_i interior to run b_k = (v_k, a_k, n_k) at offset c yields a right piece starting at v_k + c with ord = ord(v_k) + c = ord(c_i). At step j > i, cut c_j satisfies ord(c_j) > ord(c_i) by CS2. If c_j is in the original V(b_k), then ord(c_j) ≥ ord(v_k) + c (since c_j > c_i and ord(c_i) = ord(v_k) + c), placing c_j in the right piece's extent.
**Required**: Spell out the inequality chain `ord(c_j) > ord(c_i) = ord(v_k) + c`, so the reader does not have to reconstruct why CS2's strict ordering on cuts entails confinement to the right piece across iterations.

### Issue 7: R-RI labeled LEMMA but presented inline
**ASN-0084, property table** lists "R-RI | LEMMA | Rearrangement preserves S3..." while the body presents R-RI as a single inline sentence in the "Consequences of R-PRE / invariant preservation" prose, not as a separately stated lemma.
**Problem**: The derivation chain `ran(M'(d)) = ran(M(d)) ⊆ dom(C) = dom(C')` is correct but the citation pattern is asymmetric with the other lemmas (R-PIV, R-SWP, R-PPERM, etc.), each of which has a labeled header line. R-RI is consumed downstream and deserves the same explicit lemma structure.
**Required**: Lift R-RI to a labeled lemma header (preconditions, depends, postconditions) parallel to the other lemmas in this ASN, even if the body remains a one-paragraph proof.

### Issue 8: Identification paragraph's NAT-sub claim incomplete at j = 0
**ASN-0084, Identification paragraph**: "NAT-sub `m − n` (partial, m ≥ n) corresponds to the unique j with shift([n], j) = [m] when [n] ≤ [m]."
**Problem**: When `[n] = [m]` (i.e., m = n), NAT-sub gives `m − n = 0`, and "shift([n], 0)" is not OrdinalShift but the identity convention. The "unique j" includes j = 0, which is outside ASN-0034's OrdinalShift contract. The biconditional only holds under the ASN's extended convention.
**Required**: Clarify that the correspondence is between NAT-sub on its defined domain and the shift-or-identity composition (OrdinalShift for j ≥ 1, identity for j = 0).

## OUT_OF_SCOPE

### Topic 1: Higher-depth V-positions (#v > 2)
**Why out of scope**: The ASN explicitly restricts to depth 2 ("a strict scope boundary; we make no claim about deeper depths"). At depth > 2, ordinals are tumblers of length ≥ 2, and cut-point arithmetic would no longer reduce to NAT-add on singletons. A future ASN can lift the construction.

### Topic 2: Inverse rearrangements and composition
**Why out of scope**: The ASN's open questions enumerate these. The inverse of a pivot is another pivot with cuts (c₀, c₀ + w_β, c₂); the inverse of a swap is another swap. Compositional algebra (whether the composition of two rearrangements is itself a single rearrangement) is a substantive question deserving its own treatment.

### Topic 3: Effect of rearrangement on links and versions
**Why out of scope**: The Shared Vocabulary names links as typed bidirectional associations attached to content identity, and versions as immutable DAG nodes. This ASN preserves ran(M(d)) and dom(C), so link endsets and content identity are unaffected, but the full interaction with link/version state belongs to ASNs that introduce those constructs.

### Topic 4: Cross-subspace rearrangements
**Why out of scope**: CS3 confines cuts to a single subspace S. A rearrangement that exchanges regions across subspaces (e.g., between text and links) is a different operation requiring different preconditions and a different bijection structure.

### Topic 5: Tombstone handling in the link subspace
**Why out of scope**: ASN-0036 permits gaps in V_2(d) (the link subspace). R-PRE(iv) requires the affected range to be gap-free, so rearrangements over sparse link-subspace regions need separate treatment.

### Topic 6: Bound on canonical-partition run-count change
**Why out of scope**: Listed in the ASN's open questions. The worked examples show that run count can both increase (3-cut example: 2 → 4) and decrease via post-rearrangement merging (4-cut example: 5 → 4). Establishing a tight bound is its own claim.

VERDICT: REVISE
