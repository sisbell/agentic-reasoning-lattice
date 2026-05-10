# Review of ASN-0043

## REVISE

### Issue 1: L11a — link allocator conformance to T10a not established

**ASN-0043, Link Distinctness and Permanence**: "Link addresses are produced by forward allocation (T9, ASN-0034) within the link subspace. By GlobalUniqueness (UniqueAddressAllocation, ASN-0034), no two allocation events anywhere in the system produce the same address."

**Also, Home and Ownership section**: "Link addresses are produced by allocation events conforming to T10a (via L1a)."

**Problem**: GlobalUniqueness has a precondition: "a system conforming to T10a (allocator discipline)." The ASN applies GlobalUniqueness to link allocation without establishing that link allocators conform to T10a. L1a constrains WHERE link addresses end up (under the creating document's prefix) but not HOW they are produced — specifically, that siblings use `inc(·, 0)` and child-spawning uses `inc(·, k')` with `k' ∈ {1, 2}`. The parenthetical "(via L1a)" is misleading: L1a is a postcondition on address structure, not a statement about allocation process. You could place addresses under a document prefix by random selection rather than sequential allocation — L1a alone does not entail T10a conformance. The derivation chain L1a → T10a → T9 → GlobalUniqueness → L11a has a gap at the first arrow.

**Required**: State explicitly that link allocation operates within a T10a-conforming system, either as a precondition on L11a or as a standalone axiom paralleling T10a's role for content allocation. Then the chain is: T10a (system-wide axiom) + L1a (allocation prefix) → GlobalUniqueness applies → L11a follows. This also closes the same gap in L11b's verification, which cites "L11a uniqueness for `a'` by GlobalUniqueness."

### Issue 2: L11b — fresh-address existence asserted without derivation

**ASN-0043, Link Distinctness and Permanence**: "by L-fin, `dom(Σ.L)` is finite, so the same document's link subspace contains unoccupied addresses; allocate `a'` by forward allocation within it"

**Problem**: This claim requires two steps, neither shown: (1) the set of valid link addresses within a document's link subspace is infinite, and (2) an infinite set with finitely many occupied elements contains unoccupied elements. Step (1) needs L1b (element field depth ≥ 2, giving at least one ordinal component after the subspace identifier) and T0(a) (UnboundedComponentValues — that ordinal component ranges over all naturals), yielding infinitely many valid link addresses per document. Step (2) is the pigeonhole principle applied to L-fin. The L9 proof handles an analogous claim more carefully: "by L-fin, `dom(Σ.L)` is finite; by T0(a), node-field components are unbounded, so document prefixes exist beyond those occupied by any existing address." L11b skips the corresponding argument.

**Required**: Derive fresh-address existence explicitly, citing T0(a) + L1b for the infinite supply and L-fin for finite occupancy. Alternatively, extract the argument into a shared lemma (e.g., "FreshLinkAddress") that both L9 and L11b can cite.

### Issue 3: L4 — self-contradictory property classification

**ASN-0043, Properties Introduced table**: `L4 | LEMMA | EndsetGenerality — endset spans satisfy T12 (definitional from L3); the substantive content is the absence of additional constraints: no single-document, content-only, or existence restriction`

**Problem**: The Statement column says the formal content is "definitional from L3," yet the Type column says LEMMA. These are contradictory — a definitional consequence is not a lemma. L4's formal content (spans in endsets satisfy T12) follows immediately from the type definition `Endset = 𝒫_fin(Span)` where `Span` requires T12. Its substantive content (the absence of further constraints) is a design observation — the same category as L7 (DirectionalFlexibility), which is correctly labeled META for stating what the invariants do NOT constrain.

**Required**: Reclassify L4 as META (parallel to L7) or DEF, and align the statement text with the chosen classification.

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage belongs in span algebra, not link ontology
**Why out of scope**: PrefixSpanCoverage is a general property of spans and tumbler prefix ordering. Its proof uses only T1, T12, OrdinalShift, and the Span definition — no link-specific concept appears. Placing it here means any future ASN needing this result must depend on ASN-0043 even when links are irrelevant. A span algebra or tumbler algebra ASN would be the natural home. The proof is correct and the lemma is used here (L9, L10, L13); the concern is organizational, not correctness.

### Topic 2: Link participation in document arrangements
**Why out of scope**: The model derives that links cannot appear in arrangements (S3 requires `M(d)(v) ∈ dom(Σ.C)`; L0 gives `dom(Σ.L) ∩ dom(Σ.C) = ∅`). Gregory's implementation has links occupying V-positions in a document's permutation matrix. The ASN correctly identifies this gap and defers resolution. Extending S3 to accommodate link V-positions would modify ASN-0036's arrangement semantics — new territory requiring its own ASN, not an error here.

VERDICT: REVISE
