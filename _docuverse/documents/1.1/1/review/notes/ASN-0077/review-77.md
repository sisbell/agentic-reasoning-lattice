# Review of ASN-0077

## REVISE

### Issue 1: WF_V conjunct (iii) is a derived conjunct whose justification is stated three times

**ASN-0077, Definition (WF_V)**: conjunct (iii) reads

> "(iii) `V_{u₁}(d) ≠ ∅` ... (a **derived convenience conjunct**, not an independent well-formedness condition: it follows from (v) and (vi), since by TA-strict `u ∈ ⟦σ⟧` with `#u = m` by (v), and the range condition (vi) then forces `u ∈ dom(M(d))`, whence `u ∈ V_{u₁}(d)` — see the 'Empty-restriction within a non-empty document' edge case; it is named here only so that non-emptiness can be cited directly where convenient);"

**Problem**: This is reviser-drift around a forward reference, flagged under the `review-mode.anti-bloat` classifier. The redundancy of (iii) is asserted in three separate places that must be reconciled by the reader:

1. Inside conjunct (iii)'s parenthetical (the derivation above);
2. The trailing sentence after the definition: *"The independent content is carried by (i), (ii), (iv), (v), and (vi); conjunct (iii) is a derived consequence of (v)+(vi) retained only as a directly citable handle on non-emptiness."*;
3. The full re-derivation in the "Empty-restriction within a non-empty document" edge case: *"By TA-strict, `u = start(σ) ∈ ⟦σ⟧`. By precondition (v), `#u = m`... precondition (vi)... gives `u ∈ dom(M(d))`. Hence `u ∈ ⟦σ⟧ ∩ dom(M(d))`..."*

A predicate definition used as a precondition should not contain a conjunct logically derivable from its other conjuncts. The hybrid "derived convenience conjunct" carrying its own self-justifying prose ("named here only so that non-emptiness can be cited directly where convenient") is exactly the meta-prose the reader must skip past to read the precondition. The parenthetical's own forward pointer ("see the ... edge case") plus the edge-case re-derivation is the "two paragraphs say the same thing in different words" pattern.

**Required**: Pick one home for the non-emptiness fact. Either (a) drop (iii) from WF_V and have O11 sub-case (a), O11' sub-case (b), O11.1, and SDP's callers cite the edge-case lemma (`u ∈ ⟦σ⟧ ∩ dom(M(d))` from (v)+(vi)) where they currently write "by precondition (iii)"; or (b) keep (iii) as a plain conjunct with no justifying prose and delete both the trailing "independent content is carried by..." sentence and the duplicate edge-case derivation. Remove the self-referential rationale either way.

## OUT_OF_SCOPE

### Topic 1: Unified content+link origin operation over an I-stream range
**Why out of scope**: The first Open Question (a single operation reporting both content and link origins where the subspaces meet) is genuinely new territory — the I-span lift's content-only behavior is settled and correct in the cross-subspace edge case. A unified operation belongs in a future ASN.

### Topic 2: Transitive provenance / intermediate transclusion chain
**Why out of scope**: Surfacing the chain `d₁ → d₂ → … → dₙ` rather than the direct origin is correctly excluded ("Not transitive provenance") and raised as future work.

### Topic 3: Historical containment from Σ.R
**Why out of scope**: A complementary operation reporting documents that ever contained content (distinct from current arrangement origins) is correctly deferred to a future ASN.

VERDICT: REVISE
