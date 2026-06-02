# Review of ASN-0070

## REVISE

### Issue 1: Link-subspace depth asserted constant, citing a nonexistent foundation axiom

**ASN-0070, The Setting**: "For `S = s_L`: `m_{s_L}(d) = 2` always, fixed by LinkVPositionDepthAxiom (ASN-0047)."

**Problem**: No claim named `LinkVPositionDepthAxiom` exists in ASN-0047. The actual ASN-0047 claim `m_L(d)` (LinkSubspaceDepth) states the opposite: `m_S(d)` is "well-defined only while `V_S(d) ≠ ∅`," and after clearance "the next insertion re-pins `m_S(d)` from scratch at any value `≥ 2`." K.μ⁺_L's `ValidFirstLinkPosition(d, v_ℓ, m)` likewise fixes the first link V-position "for any chosen `m ≥ 2`." So the link-subspace depth is variable (`≥ 2`), not constant 2, and may be undefined when `V_{s_L}(d) = ∅`.

This propagates: the V-restricted denotation's vacuous-case clause states the undefined-depth situation "occurs only for `S = s_C` when `V_{s_C}(d) = ∅`." That is false under the corrected reading — the link subspace can also be empty with `m_{s_L}(d)` undefined, and that case is not handled.

**Required**: Replace the constant-2 claim with "`m_{s_L}(d) ≥ 2`, fixed when `V_{s_L}(d) ≠ ∅` (S8-depth / `m_L(d)`, ASN-0047), undefined otherwise," and extend the vacuous-case clause of `⟦·⟧_V` to cover an empty link subspace symmetrically with the content subspace.

### Issue 2: Citation of a nonexistent ASN-0058 claim

**ASN-0070, Computation via Decomposition**: "By M-sub (SubspaceConfinement, ASN-0058), every V-position of `β` shares the V-subspace of `v`..."

**Problem**: ASN-0058 defines no claim `M-sub` / `SubspaceConfinement`. The property cited (every position in a block's V-extent shares the start's subspace) is supplied by `M-int` (TumblerIntervalCharacterization), whose "subspace agreement" postcondition gives exactly `subspace(y) = subspace(x)` for `x ≤ y < x + n`.

**Required**: Cite `M-int` (ASN-0058), or derive the block subspace-confinement inline; remove the fabricated `M-sub` reference.

### Issue 3: V-restricted denotation definition inconsistent between body and summary

**ASN-0070, V-Restricted Denotation vs. Claims Introduced table (F1)**: The body defines `⟦Σ_V^S⟧_V := { t ∈ ⟦Σ_V^S⟧ : subspace(t) = S ∧ #t = m_S(d) ∧ (A i : 1 ≤ i ≤ m_S(d) : t_i ≥ 1) }` and spends a full paragraph arguing the positivity clause is load-bearing for canonical-form uniqueness and the postcondition equality. The table entry for F1 drops it: "`⟦Σ_V^S⟧_V := {t ∈ ⟦Σ_V^S⟧ : subspace(t) = S ∧ #t = m_S(d)}`."

**Problem**: The summary omits the very clause the body declares necessary; a reader/implementer working from the table would get a different (over-broad) denotation that admits zero-component tumblers the body explicitly excludes.

**Required**: Restore the positivity clause in the F1 table entry to match the body definition.

### Issue 4: Worked-example I-coverage stated as a finite set when it is a lexicographic interval

**ASN-0070, A Worked Example**: "The coverage is `coverage(L(ℓ).e₁) = {a₁, a₁ + 1, a₁ + 2}`."

**Problem**: By the coverage definition (`⋃⟦σ⟧` over all of `T`) and T12, `coverage({(a₁, δ(3, m_a))}) = {t ∈ T : a₁ ≤ t < a₁ ⊕ δ(3, m_a)}` is a lexicographic interval that also contains deeper-depth tumblers (e.g. `a₁.x`, `(a₁+1).y`), not just the three depth-`m_a` addresses. This is precisely the raw-vs-restricted distinction the ASN insists on for V-space; the same precision is dropped on the I-side. The final result is unaffected (the intersected I-extents are depth-`m_a`), but the stated equality is false as written.

**Required**: State the coverage as the half-open interval, or qualify the set as the depth-`m_a` members of the coverage that the block I-extents meet.

## OUT_OF_SCOPE

### Topic 1: Partial-reach reporting of unresolved I-addresses
**Why out of scope**: The first Open Question (whether the result must preserve which coverage addresses failed to resolve) is genuinely new result-form territory, correctly deferred rather than treated as a gap in this query operation.

### Topic 2: Concurrency semantics under concurrent arrangement modification
**Why out of scope**: `follow` is specified as a state-pure query at a fixed `Σ`; concurrent-transition semantics belong to a transition/concurrency ASN, not this one.

VERDICT: REVISE
