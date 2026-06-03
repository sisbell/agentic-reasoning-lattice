# Review of ASN-0070

## REVISE

### Issue 1: Empty result component mis-attributed to the vacuous-subspace convention

**ASN-0070, A Worked Example, Configuration 1 ("Partial emptiness (not F-empty)")**: "The link-subspace component `Σ_V^{s_L}` is empty ... This is an individual subspace component being empty, admissible by the V-Restricted Denotation convention."

**Problem**: In Configuration 1, `M(d)` maps `[2, 1] → ℓ₀`, so `V_{s_L}(d) = {[2,1]} ≠ ∅` and `m_{s_L}(d) = 2` is *defined*. The empty result component `Σ_V^{s_L} = ⟨⟩` therefore arises from coverage missing the arrangement, **not** from a vacuous subspace. But the cited "V-Restricted Denotation convention" is specifically the *Vacuous-subspace convention*, whose stated trigger is "`m_S(d)` is undefined ... when `V_S(d) = ∅`." That convention does not apply here — `m_{s_L}(d)` is defined. The correct justification is that `⟨⟩` is admissible as the empty (vacuous-union) span-set under the *main* V-restricted denotation, satisfying `⟦⟨⟩⟧_V = ∅ = R(d, e)|_{s_L}`. The note conflates two distinct sources of an empty component: (a) a vacuous subspace, and (b) a populated subspace whose V-positions miss coverage. Only (a) is covered by the named convention; the example exhibits (b) and cites (a).

This is compounded by F1's own prose: "each `Σ_V^S` is a finite V-span-set whose components are spans in subspace `S` of depth `m_S(d)` when `V_S(d) ≠ ∅`, and `Σ_V^S = ⟨⟩` in the vacuous case." Binding `⟨⟩` to "the vacuous case" reads as `⟨⟩ ⟺ vacuous`, which Configuration 1 directly contradicts (`⟨⟩` in a non-vacuous subspace).

**Required**: Distinguish the two sources of an empty component in F1's postcondition prose and in the Configuration 1 verification. State that `Σ_V^S = ⟨⟩` is admissible both when `V_S(d) = ∅` (vacuous convention) and when `V_S(d) ≠ ∅` but `R(d, e)|_S = ∅` (empty union under the main denotation), and fix the Configuration 1 citation to the latter.

### Issue 2: Insertion mechanics narrated in the Setting are unused by the query

**ASN-0070, The Setting**: "pinned by the first link insertion (`ValidFirstLinkPosition` of K.μ⁺_L, for any chosen `m ≥ 2`) and held thereafter ... pinned by the first content insertion (ValidFirstInsertionPosition) ... the next insertion re-pins it from scratch at any value `≥ 2`."

**Problem**: `follow` is a pure query that reads the *current* `M(d)`; how `m_S(d)` was pinned by past insertions and how it re-pins after clearance is never used in any F0/F1/F-canonical argument. The note needs only "when `V_S(d) ≠ ∅`, all V-positions in subspace `S` share a common depth `m_S(d)` (S8-depth)." The pinning-and-re-pinning narrative describes insertion-operation behavior that does not advance the query's reasoning, and the re-pinning fact is then restated in the V-Restricted Denotation's "Vacuous-subspace convention." This is duplicated background, not load-bearing content.

**Required**: Reduce the Setting to the current-state fact actually consumed (common depth `m_S(d)` exists when the subspace is non-empty, undefined otherwise) and drop the insertion/re-pinning narration; retain a single statement of the vacuous case at the one site (V-Restricted Denotation) where the `⟨⟩` convention is defined.

## OUT_OF_SCOPE

### Topic 1: Multi-home resolution relationships, concurrency, transclusion-lineage cross-document relations
**Why out of scope**: The three Open Questions (relationship between resolutions against documents transcluding from different home subsets; concurrency semantics under concurrent modification; `follow(ℓ, d, i)` vs `follow(ℓ, d', i)` under shared transclusion lineage) are genuinely new territory requiring additional state or operation semantics, not gaps in this query's specification. They are correctly deferred.

VERDICT: REVISE
