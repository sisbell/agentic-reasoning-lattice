# Review of ASN-0099

## REVISE

### Issue 1: Retired-labels paragraph is pure numbering meta-prose
**ASN-0099, "Claims Introduced"**: "The labels F7, F16, F17, and F18 are deliberately retired — claims removed across revisions — so the F-sequence is a set of stable identifiers, not a contiguous range; no claim in this ASN references a retired label."
**Problem**: This advances no reasoning about state, operations, or invariants. It justifies the label-numbering scheme — exactly the document-bookkeeping accretion the anti-bloat pass targets. The table already omits F7/F16/F17/F18; their absence needs no narration. A future reader gains nothing and must skip past it.
**Required**: Delete the paragraph. If a gap in the F-sequence ever confuses, the omission from the table is self-explanatory.

### Issue 2: Use-site back-pointers in the match-predicate prose
**ASN-0099, "The Match Predicate"**: "F1's `matches` (introduced at the Phase 2 definition site above) is the coverage-form generalization of ASN-0098's `discoverable_from` (defined there in project form)."
**Problem**: The parentheticals "(introduced at the Phase 2 definition site above)" and "(defined there in project form)" are location pointers, not content. The relation to `discoverable_from` is the substantive part; the cross-pointers are navigation scaffolding that rots as the document is edited.
**Required**: State the relation directly: "matches is the coverage-form of ASN-0098's `discoverable_from`." Drop the slot-location annotations.

### Issue 3: "Primary obligation" framing is protocol rationale
**ASN-0099, "Completeness"**: "F2★ ∧ F3★ at the V form is the **primary obligation on `result_V`**: any implementation exposing the V-side surface must satisfy it. When the implementation also exposes the I-side surface satisfying F2 ∧ F3, the factoring equation `result_V(R, d, Σ) = result(image(R, d, Σ), Σ)` follows by F2 ∧ F3 + F2★ ∧ F3★ (V form) + F12..."
**Problem**: The "primary obligation / surface exposure" framing is rationale about which conformance surface matters most, not a system guarantee. The load-bearing content is the factoring equation and its derivation.
**Required**: Keep the factoring equation and its premise chain; drop the "primary obligation … any implementation exposing the V-side surface must satisfy it" editorializing.

### Issue 4: F10 finiteness cites the implementation result where the definition suffices
**ASN-0099, F10**: "Finiteness: F3 gives `result(I, Σ) ⊆ dom(Σ.L)`; L-fin gives `|dom(Σ.L)| < ∞`."
**Problem**: F10 is a claim about the abstract set `findlinks(I, Σ)` (its elements `aⱼ` satisfy `matches`), not about an implementation's `result`. By the definition of `findlinks`, `findlinks(I, Σ) ⊆ dom(Σ.L)` holds directly — routing through F3 (a soundness claim about `result`) is an unnecessary detour that couples the ordering claim to the conformance contract.
**Required**: State `findlinks(I, Σ) ⊆ dom(Σ.L)` by definition, then apply L-fin.

## OUT_OF_SCOPE

### Topic 1: Audit witness / index-agreement obligation
**Why out of scope**: The first Open Question (recoverable witness that the index agrees with the link store) is implementation-conformance machinery for a future ASN, not a guarantee this one must specify.

### Topic 2: Latency bound between K.λ and query visibility
**Why out of scope**: The second Open Question (time bound on link appearance) concerns timing/consistency semantics deliberately deferred under "What We Have Not Specified."

VERDICT: REVISE
