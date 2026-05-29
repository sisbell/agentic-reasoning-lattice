# Review of ASN-0040

The arithmetic core is solid: the sibling-stream induction (S(p,d)), B5/B5a zero-counting, B6 sufficiency/necessity, and B7's case split all hold up, and the recent removal of the T10a dependency leaves S0 and B7 resting cleanly on TA5/T1/T3. The B1→B2→hwm→B8/B9 chain is acyclic and the co-reachable (rather than global) framing of B8 is the correct, honest restriction. Most findings concern accreted meta-prose, which this note's anti-bloat classifier asks me to surface, plus one scope item.

## REVISE

### Issue 1: B0a defers its own content to a downstream location with editorial framing
**ASN-0040, B0a (Baptismal Closure)**: "the operation specified at Bop, the canonical site of the registry-mutation rule. Its sole effect on the registry is the single-element adjunction Bop fixes."
**Problem**: This is the "definition introduction defers downstream" pattern. B0a's job is to partition Σ; instead of stating the baptismal class's registry effect, it points forward to Bop and editorializes ("canonical site of the registry-mutation rule"). A reader following B0a must jump to Bop to learn what the adjunction is, then return. The phrase "canonical site" advances no reasoning.
**Required**: State the baptismal class's effect directly (`op(s).B = s.B ∪ {next(s.B, p, d)}`) or simply name the single-element adjunction without the "canonical site" framing and the forward defer.

### Issue 2: B3's Occupied predicate is unused machinery introduced with scope-justification prose
**ASN-0040, B3 (Ghost Validity)**: "a placeholder for any future content-storage layer… Content storage is out of scope here, so `Occupied` is left uninterpreted and no operation of this ASN reads or sets it."
**Problem**: This is "new prose explains why the construct is needed rather than what it asserts." The ASN introduces a predicate that, by its own admission, no operation reads or sets — unverified obligation attached to operations that do not exist in this note. The ghost-element *observation* (a baptized position may carry no content) is a genuine baptism concept, but the `Occupied` machinery and its self-justifying scope paragraph are bloat around it.
**Required**: Either state the ghost-element notion abstractly without introducing an uninterpreted predicate, or move the `Occupied ⟹ baptized` constraint to the content-storage ASN. Drop the "placeholder/out of scope/left uninterpreted" explanation either way.

### Issue 3: B7 cites TA5-SigValid for a fact T4 states directly
**ASN-0040, B7 (unequal-length-parents case)**: "whose field-segment constraint forbids a zero final component (TA5-SigValid: p'_{#p'} ≠ 0)."
**Problem**: The needed fact is `p'_{#p'} ≠ 0`, which T4's field-segment axiom states outright (`t_{#t} ≠ 0`). TA5-SigValid gives `sig(t) = #t`, from which the non-zero-last-component follows only after also excluding the all-zero tumbler — an indirect route to a fact already on the table.
**Required**: Cite T4 directly for `p'_{#p'} ≠ 0`.

## OUT_OF_SCOPE

### Topic 1: The B3 invariant binding future content-storage operations
**Why out of scope**: `(A s, t : Occupied(t,s) ⟹ t ∈ s.B)` is a constraint on content-storage operations, and content storage is explicitly deferred. The invariant belongs in the content-storage ASN where `Occupied` is actually interpreted and where an operation can be shown to preserve it. (See Issue 2 — flagged there because the predicate machinery sits inside this note's claim list.)

### Topic 2: `allocated(s) ⊆ s.B` alignment, parent-prerequisite chain, distributed cross-replica ordering
**Why out of scope**: These are correctly parked in Open Questions and depend on the allocator-activation discipline, the ownership model, and the replication protocol respectively — new territory, not defects here.

VERDICT: REVISE
