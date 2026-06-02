# Review of ASN-0070

## REVISE

### Issue 1: F-canonical proves uniqueness but not existence

**ASN-0070, "Canonical Form" / Theorem F-canonical**: "Given `R(d, e)`, there exists exactly one per-subspace family satisfying the canonical-form shape of F-canon-form."

**Problem**: The theorem asserts *existence and uniqueness* ("there exists exactly one"), but the proof body discharges only uniqueness. Steps 1–3 all begin from a *hypothesized* normalized span-set `Σ̂` and force its structure; the "unique reconstruction" paragraph compares two given Step-1-restricted span-sets with the same `⟦·⟧_V` and shows they coincide. Nowhere does the proof start from an arbitrary `R(d,e)|_S` — a finite set of depth-`m_S(d)`, positive-component, subspace-`S` tumblers — and *construct* a canonical span-set whose V-restricted denotation equals it. The existence half is therefore asserted, not proven.

This shows up concretely in the citation trail: Step 1 establishes level-uniformity ("the hypothesis of S6") and then jumps directly to **S9** (NormalizationUniqueness) for the uniqueness collapse. **S8** (NormalizationExistence, ASN-0053) — the lemma that actually guarantees a normalized equivalent *exists* — is never invoked, here or in F-det step 5 (which likewise cites only S9). F-det and F-empty both lean on F-canonical for "given the fixed V-restricted denotation, there is a (the) canonical form," so the unproven existence half propagates.

**Required**: Add the existence direction to F-canonical's proof: partition `R(d,e)|_S` into maximal runs of consecutive depth-`m_S(d)` subspace-`S` tumblers (using the consecutivity characterization already proved in Step 2), map each run to the ordinal-displacement span `(min(run), δ(|run|, m_S(d)))`, and show (i) each such span's `⟦·⟧_V` equals its run, (ii) the resulting set satisfies N1/N2 (maximality of runs supplies N2's strict separation), invoking S8 for the normalized-existence guarantee. Cite S8 in F-canonical's dependency list and in F-det.

### Issue 2: F1 postcondition asserts component depth unconditionally

**ASN-0070, F1 (FollowOperation), Postcondition**: "each `Σ_V^S` is a finite V-span-set whose components are spans in subspace `S` of depth `m_S(d)`."

**Problem**: `m_S(d)` is undefined whenever `V_S(d) = ∅` (stated explicitly in The Setting and in the V-restricted denotation section). The postcondition as written predicates "depth `m_S(d)`" of the components unconditionally, which is meaningless in the vacuous-subspace case. The V-restricted denotation section patches this with the `Σ_V^S = ⟨⟩` convention, so the equality `⟦Σ_V^S⟧_V = R(d,e)|_S = ∅` is still satisfiable — but F1's own statement does not carry the caveat, leaving the postcondition ill-typed exactly when a subspace is empty (e.g., a freshly created document with empty arrangement).

**Required**: Qualify F1's depth clause, e.g. "components are spans in subspace `S` of depth `m_S(d)` when `V_S(d) ≠ ∅`; otherwise `Σ_V^S = ⟨⟩`," mirroring the convention already adopted for `⟦·⟧_V`.

## OUT_OF_SCOPE

### Topic 1: Partial-reach reporting and content-retrieval success
**Why out of scope**: The first and seventh Open Questions (whether unreached coverage must be reported, and whether `R(d,e)` V-positions always permit successful content lookup) concern result *semantics* and a future retrieval operation, not the inverse-image query specified here. Correctly deferred.

VERDICT: REVISE
