# Review of ASN-0069

## REVISE

### Issue 1: φ described as both "unique" and "any such" — the freedom is misattributed
**ASN-0069, §"Sharing, Not Duplication" and §"The Arrangement Layer"**: The ASN quotes J4 as installing content "via the **unique** order-preserving bijection `φ : V_{s_C}(d_op) → V_{s_C}(d_new)`", then in §"The Arrangement Layer" writes that J4 "leav[es] the *V-position identity* of the pairing to **any such φ**. Literal inheritance fixes `φ` to be the identity on V-positions — **one admissible discipline among several**."

**Problem**: These are inconsistent. For two canonical sequential blocks (`V_{s_C}` is `{[s_C,1,…,1,k] : 1 ≤ k ≤ n}` by D-SEQ★) of equal cardinality, the order-preserving bijection is uniquely the k-th↦k-th map — there are not "several" φ for a fixed target set. The actual design freedom is in the *target set* `V_{s_C}(d_new)`, specifically its depth `m'_{s_C}` (which V4's "Why V-positions are not rebased" paragraph itself discusses). The ASN attributes the freedom to "any such φ" when φ is forced once the target depth is chosen. This also undercuts V4's framing as a "design commitment strengthening J4": what V4 actually fixes is target-depth = source-depth, from which φ = identity follows.

**Required**: State that φ is unique given the target set; the commitment V4 makes is to install `V_{s_C}(d_new)` at the source's depth (`m'_{s_C} = m_{s_C}(d_op)`), so `V_{s_C}(d_new) = V_{s_C}(d_op)` and φ is the identity. Remove "any such φ" / "one admissible discipline among several" or rephrase so the freedom is located in depth selection, not in φ.

### Issue 2: "(At the tumbler-algebra level …)" parentheticals re-ground verified foundation results
**ASN-0069, §"Identity by Sub-Allocation" (Address uniqueness), §"Independence Among Forks", V10(a)**: Three parentheticals: "(At the tumbler-algebra level this is underwritten by T10a.6 (DomainDisjointness, ASN-0034)…)"; "(At the tumbler-algebra level B8's same-namespace distinctness is underwritten by T10a.7 (EnumerationInjectivity)…)"; "(At the tumbler-algebra level the two emissions lie at distinct enumeration indices and T10a.7…)".

**Problem**: B8 (Uniqueness) is itself a verified foundation result (ASN-0040), citeable as-is. Explaining *why B8 holds* by pointing further down to T10a.6/T10a.7 adds no reasoning to this ASN — it narrates the internal dependency chain of the foundations. This is the redundant-grounding pattern: prose around a cited result justifying the result rather than using it. The three occurrences say the same thing in three places.

**Required**: Drop the three parentheticals; cite B8 (and B9) directly. The tumbler-algebra grounding is internal to the foundations and need not be restated here.

## OUT_OF_SCOPE

### Topic 1: V6a's link-discoverability machinery (coverage / project / discoverable_from, V6a(ii) and (iii))
**Why out of scope**: The scope list excludes "link semantics." V6a introduces three local definitions — `coverage(e)`, `project(a, i, d, Σ)`, `discoverable_from(a, d, Σ)` — solely to prove that links remain *discoverable* from the source and the fork. Discoverability is a property of link-query operations applied after the fork, not of the fork state transition itself. The fork ASN's genuine obligations here are V4 (shared I-addresses) and the link-store frame `L' = L` (essentially V6a(i)); the projection/discoverability apparatus and V6a(ii)/(iii) belong in a link-operations ASN. (V6a(i), the persistence of `Σ.L` across the fork composite, is fork-relevant and may stay.)

META: not applicable — the ASN remains at the abstract state/operation level; the V6a content is misplaced topically, not drifted into implementation mechanics.

VERDICT: REVISE
