# Review of ASN-0077

## REVISE

### Issue 1: O11.1 mislabels conjunct (v) as state-independent

**ASN-0077, Corollary O11.1 (derivation)**: "Conjuncts (ii) (level-uniformity), (iv) (T12...), and (v) (length identity `#ℓ = #u`) are structural properties of `(u, ℓ)` alone and state-independent."

**Problem**: Conjunct (v) of WF_V is not "the length identity `#ℓ = #u`." As defined, it is "`#ℓ = #u = m`, where `m` is the common V-position depth in subspace `u₁` of `d` (S8-depth)." The second equality couples `#u` to the arrangement's common depth, which is a property of `M(d)` — state-dependent, not structural. O11.1 silently drops the `= m` clause when it files (v) among the state-independent conjuncts, then performs the actual depth-coincidence work ("the common depth `m` in subspace `u₁` at Σ' coincides with the common depth at Σ") under the conjunct (vi) bullet. So the obligation that genuinely preserves (v) is established, but it is attributed to (vi), while (vi)'s own obligation (range ⊆ `dom(M'(d))`, which follows trivially from `dom(M(d)) ⊆ dom(M'(d))`) is left entangled with it. A reader checking conjunct (v) at its own bullet finds it dismissed as structural and under-justified.

**Required**: State that conjunct (v) has a state-dependent component (the equality with the document's common depth) and discharge it explicitly — the four-case depth-coincidence argument currently sitting under (vi) is the proof of (v)'s preservation. Separate it from (vi)'s monotonicity step, which is the only thing (vi) actually requires once `m = #u` is fixed.

### Issue 2: Redundant restatement in the `origins_V` two-form preamble

**ASN-0077, "Lifting origin to a V-span"**: "We work with two equivalent expressions... The reader-facing form... is: *(F1)*... The block-collapsed form... *(F3)*... (F1) is the definition; (F3) is the equivalent block-collapsed form derived below via O2."

**Problem**: The closing sentence "(F1) is the definition; (F3) is the equivalent block-collapsed form derived below via O2" restates what the two preceding sentences already say (that the forms are equivalent, that (F3) reads through the C1a decomposition) and adds a forward pointer to the equivalence proof that follows immediately. This is the forward-reference-accretion pattern: a definition's setup carrying a redundant "derived below" pointer where the derivation is the next paragraph.

**Required**: Drop the closing restatement; the subsequent "Equivalence chain (F1) ≡ (F3)" heading already signals the derivation.

## OUT_OF_SCOPE

### Topic 1: Unified content+link origin operation over an I-stream range
**Why out of scope**: The ASN's first Open Question raises a combined operation reporting origins of both subspaces; this is new territory (the I-span lift deliberately confines to `dom(C)`), correctly deferred rather than treated as a defect here.

### Topic 2: Surfacing the intermediate transclusion chain / historical containment from Σ.R
**Why out of scope**: O4 and the "What SHOWORIGIN does not promise" section correctly scope these to separate future operations; the coupling invariants with `Σ.R` belong to a provenance-operation ASN, not here.

VERDICT: REVISE
