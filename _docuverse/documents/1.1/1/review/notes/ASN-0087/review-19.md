# Review of ASN-0087

This is a careful, deeply-worked operation specification. The L1c chain construction, the freshness three-layer argument, and the invariant sweep are genuinely rigorous, and the boundary cases (empty link subspace, reflexive endsets, address/V-position desync via permanent `dom(L)`) are handled correctly. The worked example checks out arithmetically. The defects below are in the *justifications* attached to certain preserved invariants, not in the conclusions — but in a spec whose value is the proof, a misattributed reason is a real defect.

## REVISE

### Issue 1: S7d is misclassified as content-quantified
**ASN-0087, "Per-State Invariants at Σ' → state components unchanged"**: "S7a, S7b, S7d (origin and structural attribution for content addresses): vacuous since `Σ'.C = Σ.C`; the predicates quantify over `dom(C)`, which is unchanged."
**Problem**: S7d (DocumentAllocationDiscipline) does **not** quantify over `dom(C)`. By its foundation definition (ASN-0036), S7d is a statement about *document tumblers*: every `d` satisfies `zeros(d) = 2`, arises from a distinct allocation event, and distinct documents have distinct tumblers. Its preservation has nothing to do with the content frame `Σ'.C = Σ.C`; it follows from `dom(Σ'.M) = dom(Σ.M)` (MAKELINK registers no new document). The stated justification is wrong even though the conclusion (S7d preserved) is correct. A reader checking the proof is told to verify the wrong frame clause.
**Required**: Separate S7d from S7a/S7b. Justify S7d via the unchanged document set (`dom(M)` not extended by K.λ or K.μ⁺_L), not via `Σ'.C = Σ.C`.

### Issue 2: M-Inv-State table miscategorizes M0 and S7d, contradicting the body
**ASN-0087, M-Inv-State claim**: "vacuous-by-frame invariants (M0, S4, S7a, S7b, S7d, C1b, C1c, C-fin, P6, P7, P8, NodeLineage, ActivatedEmission) — the C-quantified ones vacuous via `Σ'.C = Σ.C`, the E-quantified ones via `Σ'.E = Σ.E`."
**Problem**: M0 and S7d are neither C-quantified nor E-quantified — both range over the document set / document tumblers (`dom(M)`). The stated dichotomy supplies no preservation basis for them. This also contradicts the body, which correctly justifies M0 via "`dom(Σ'.M) = dom(Σ.M)`." The summary table and the body disagree on why M0 holds.
**Required**: Add an M-frame category ("preserved because `dom(M)` is unchanged") covering M0 and S7d, and reconcile the table with the body.

### Issue 3: "Vacuous" misused for invariants preserved by inheritance over nonempty domains
**ASN-0087, several places** (e.g. S4, S7a, S7b, C1b, C1c, P6, P7): "vacuous since `Σ'.C = Σ.C`."
**Problem**: "Vacuous" means the quantification universe is empty. But `dom(C)` is generally nonempty at `Σ`, so these invariants are not vacuously true at `Σ'` — they are *preserved by frame-inheritance* (no new instances, existing instances unchanged). The reasoning is sound but the term is imprecise, and the imprecision is what produced the Issue 1/2 categorization slips.
**Required**: Replace "vacuous" with "preserved by inheritance (no new `dom(C)` entries)" for invariants over nonempty unchanged domains; reserve "vacuous" for genuinely empty quantifications (e.g. "MAKELINK introduces no new content *allocation events*").

### Issue 4: `m_L(d)` referenced where it is undefined in the K.μ⁺_L precondition
**ASN-0087, Preconditions**: "`#v_ℓ = m_L(d)` [when `V_{s_L}(d) = ∅`, MAKELINK fixes `m_L(d) = 2` via M-DepthConv ...]"
**Problem**: By its foundation definition, `m_L(d)` is "well-defined only while `V_{s_L}(d) ≠ ∅`." The precondition line literally writes `#v_ℓ = m_L(d)` in a case where `m_L(d)` is undefined; the bracket patches the meaning but the precondition as stated is ill-formed. Since M-DepthConv is load-bearing precisely because the depth is *not* recoverable from `Σ` here, the precondition should not pretend `m_L(d)` exists.
**Required**: State the empty-subspace branch as `#v_ℓ = 2` (chosen by M-DepthConv) rather than `#v_ℓ = m_L(d)`, keeping `m_L(d)` only for the non-empty branch.

## OUT_OF_SCOPE

### Topic 1: `dom(M)` / `E_doc` substrate reconciliation
**Why out of scope**: The ASN discharges K.μ⁺_L's `d ∈ E_doc` precondition by `d ∈ dom(M)` "under the standing assumption that the combined substrate maintains the coupling," and explicitly defers the reconciliation to a future framework-level ASN. This is a genuine assumed-but-unproven dependency, but it affects every operation over the combined ASN-0047/ASN-0093 substrate, not MAKELINK specifically. Correctly deferred.

VERDICT: REVISE
