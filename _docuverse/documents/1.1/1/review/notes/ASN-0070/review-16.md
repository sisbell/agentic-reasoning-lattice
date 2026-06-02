# Review of ASN-0070

## REVISE

### Issue 1: Disjointness of the joint V-restricted denotation cites the wrong premise
**ASN-0070, "V-Restricted Denotation"**: "For the full family `Σ_V = (Σ_V^{s_C}, Σ_V^{s_L})`, define the joint V-restricted denotation: `⟦Σ_V⟧_V := ⟦Σ_V^{s_C}⟧_V ⊎ ⟦Σ_V^{s_L}⟧_V`. The two subspace components are disjoint by S3★-aux applied to V-positions."

**Problem**: S3★-aux (SubspaceExhaustiveness) states only that every V-position in `dom(M(d))` has `subspace ∈ {s_C, s_L}` — an exhaustiveness fact that contributes nothing to disjointness. The disjoint-union assertion `⊎` requires that no `t` lies in both sets. By the V-restriction filter, every `t ∈ ⟦Σ_V^{s_C}⟧_V` has `subspace(t) = s_C` and every `t ∈ ⟦Σ_V^{s_L}⟧_V` has `subspace(t) = s_L`; disjointness then follows from `s_C ≠ s_L` (SubspaceConventionAxiom / SC-NEQ, ASN-0047), not from exhaustiveness. This is also internally inconsistent: F0's own partition correctly attributes disjointness to "subspace is single-valued per the first-component projection" and reserves S3★-aux for exhaustiveness. The joint-denotation definition contradicts F0's own (correct) attribution.

**Required**: Replace the citation with `s_C ≠ s_L` (SubspaceConventionAxiom) together with the filter's subspace condition; note that disjointness here is a property of the filtered denotation sets and does not even depend on `dom(M(d))` membership (so S3★-aux's domain restriction is doubly inapposite).

### Issue 2: Load-bearing "maximal run" definition is imprecise and its partition property is asserted, not derived
**ASN-0070, F-canonical Step 2 (Definition) and Step 2a**: "A *maximal run* in a set `X` of such tumblers is a maximal subset of `X` whose elements form a chain of pairwise consecutive tumblers." and Step 2a: "Partition `X` into its maximal runs of consecutive tumblers ... (every element of `X` lies in exactly one maximal run)."

**Problem**: (a) "chain of pairwise consecutive tumblers" is wrong as written — in a chain `t₀ < t₁ < t₂` the pair `(t₀, t₂)` is *not* consecutive, so the elements are not pairwise consecutive. The intended notion is a chain whose *successive* elements are consecutive (equivalently, a connected component of the consecutivity successor-relation restricted to `X`). Step 2a then silently relies on the corrected reading ("each `t_{i+1}` agrees with `t_i` ... and increments the last component by 1"). (b) The claim "every element of `X` lies in exactly one maximal run" — the partition property that the entire existence argument (and hence F-det and F-empty, which depend on F-canonical) rests on — is stated parenthetically without derivation. Since consecutivity (per the Characterisation) is a single-valued successor/predecessor relation on depth-`m_S(d)` subspace-`S` tumblers, the components are disjoint chains and the partition follows, but for a definition this load-bearing the standard is that the one-line claim be discharged.

**Required**: Restate the definition as "a maximal subset of `X` that forms a chain under the consecutivity relation (each element consecutive to its successor)," and add the one- or two-line argument that consecutivity's single-valued successor/predecessor structure makes the maximal runs a partition of `X`.

## OUT_OF_SCOPE

(none — the Open Questions correctly defer partial-reach reporting, concurrency semantics, and cross-document/lineage relationships to future ASNs.)

VERDICT: REVISE
