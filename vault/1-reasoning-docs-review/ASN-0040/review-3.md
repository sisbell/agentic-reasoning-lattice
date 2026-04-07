# Review of ASN-0040

## REVISE

### Issue 1: wp formulas omit serialization assumption
**ASN-0040, The high water mark**: "wp(baptize(p, d), B1) = B1 ∧ B0a" and "wp(baptize(p, d), a ∉ B) = B1 ∧ B7"
**Problem**: Both formulas are presented as unqualified equations, but both assume serialized execution within the namespace. The ASN acknowledges this two paragraphs later — "Both derivations reason about a single baptism acting on a known state B — they assume sequential execution within each namespace. B4 discharges this assumption" — and correctly notes that without B4 both results are invalidated. But the formal expressions stand alone as equations. A reader citing them gets the wrong precondition. Furthermore, B0a and B7 are transition constraints and mathematical lemmas respectively, not state predicates — mixing them with the state predicate B1 in a wp formula conflates different kinds of conditions.
**Required**: Either annotate each wp formula with its assumption (e.g., "under B4" or "assuming serialized execution per B4") or restructure as: state precondition is B1; environmental assumptions are B0a and B4; supporting lemma is B7. The distinction between what must hold of the pre-state versus what must hold of the transition should be explicit in the formal notation, not just the prose.

### Issue 2: B0a uses undefined "valid"
**ASN-0040, The baptismal registry**: "t was produced by baptism(p, d) for some valid (p, d)"
**Problem**: "Valid" is not defined at B0a. B6 (Valid Depth) defines depth validity later in the ASN, and the parent-in-B question is deferred to Open Questions — both defensible choices. But B0a is a formal property and "valid" is load-bearing: it determines what can enter B. A reader encounters B0a before B6 and has no anchor for "valid."
**Required**: Either forward-reference B6 explicitly ("for some (p, d) satisfying B6 below") or define a minimal validity predicate at the point of use. If "valid" intentionally means only B6 and not parent-in-B, say so — the deliberate deferral of the parent prerequisite is worth stating at the property, not only in Open Questions.

### Issue 3: B1 induction covers only the inbound direction
**ASN-0040, The contiguous prefix property**: "This argument rests on two additional properties. First, no operation outside this namespace inserts an element into S(p, d) — established below as B7."
**Problem**: The inductive step shows B1 is preserved for the target namespace (p, d): the new element c_{hwm+1} extends the contiguous prefix, and B7 prevents external operations from inserting into S(p, d). But B1 is universally quantified over all (p', d'). The argument must also show that the new element c_{hwm+1} does not disrupt any *other* namespace — i.e., c_{hwm+1} ∉ S(p', d') for (p', d') ≠ (p, d), so children(B', p', d') = children(B, p', d'). This follows immediately from B7's symmetry (disjointness is bidirectional), but the outbound direction is never stated.
**Required**: Add one sentence to the inductive step: since c_{hwm+1} ∈ S(p, d) and S(p, d) ∩ S(p', d') = ∅ by B7, the new element does not enter any other namespace's children set, so B1 is preserved for all (p', d').

### Issue 4: B9 is informally stated
**ASN-0040, Unbounded growth**: "B9 — Unbounded Extent: (A p ∈ Σ.B, d valid, M ∈ ℕ :: the system permits hwm(B, p, d) to reach M)"
**Problem**: "The system permits" is not a formal predicate. Does it mean no invariant bounds hwm? That for any M there exists a reachable state with hwm ≥ M? That no property of this ASN introduces a finite ceiling? The prose ("No architectural limit constrains how many children a position may have") is clear, but the formal statement should match.
**Required**: State B9 as a reachability claim: for any p ∈ Σ.B, valid d, and M ∈ ℕ, there exists a sequence of baptisms from the current state producing a state B' with hwm(B', p, d) ≥ M — or equivalently, no finite upper bound on hwm is derivable from B0–B8.

## OUT_OF_SCOPE

None. The ASN stays within its declared scope. The Open Questions are appropriate future work, and the Scope section correctly identifies deferred topics.

VERDICT: REVISE
