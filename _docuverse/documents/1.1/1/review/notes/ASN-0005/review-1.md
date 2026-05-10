# Review of ASN-0005

## REVISE

### Issue 1: No concrete worked example
**ASN-0005, Formal summary / throughout**: The ASN never instantiates its postconditions against a specific scenario.
**Problem**: Not a single concrete deletion is traced through the specification. For instance: "DELETE(d, 3, 2) applied to a document whose POOM maps positions 1–5 to I-addresses a₁–a₅ — verify DEL0, DEL1, DEL6 against the resulting state." Without this, every postcondition is verified only by staring at quantifiers.
**Required**: At least one concrete example (preferably in the text subspace) that checks DEL0, DEL1, DEL6, and DEL9 against named values. Boundary example (DELETE at position 0 or DELETE of entire content) strongly recommended as a second.

### Issue 2: DEL6 partial-overlap analysis covers one of three cases
**ASN-0005, "I-dimension invariance in surviving entries"**: "If the original entry mapped V-range [v₁, v₂) to I-range [i₁, i₂) and the deletion removes the first k positions, the surviving entry maps the remaining V-range to I-range [i₁ + k, i₂)."
**Problem**: Three distinct partial-overlap geometries exist when [p, p⊕w) intersects a POOM entry spanning [v₁, v₂):

  (a) Tail removal — deletion starts interior to the entry and extends past its end (v₁ < p, p⊕w ≥ v₂). Surviving: [v₁, p) → [i₁, i₁+(p−v₁)). I-displacement unchanged; width shrinks. Not discussed.

  (b) Head removal — deletion starts before the entry and ends interior (p ≤ v₁, p⊕w < v₂). This is the one case the ASN analyzes.

  (c) Middle split — deletion is strictly interior (v₁ < p and p⊕w < v₂). One entry splits into two surviving fragments: [v₁, p) → [i₁, i₁+(p−v₁)) and [p⊕w, v₂) → [i₁+(p⊕w−v₁), i₂). After V-compaction the second fragment shifts left by w. This case produces a net increase in POOM entry count, which DEL6 does not acknowledge.

**Required**: Analyze all three cases. State explicitly that middle-split produces two entries from one, with the I-displacement offset computed independently for each fragment.

### Issue 3: Precondition does not require subspace confinement
**ASN-0005, Formal summary**: "Position p is valid in document d's virtual stream, and the span [p, p ⊕ w) lies within the existing content."
**Problem**: The precondition does not require that [p, p⊕w) lies entirely within a single subspace (text or link). Yet DEL1 and DEL1a specify different compaction behaviors depending on which subspace the deletion targets. If the range could straddle the text/link boundary, the specification is contradictory — it would need to simultaneously compact (DEL1) and not compact (DEL1a) the surviving positions.
**Required**: Add an explicit precondition conjunct: the range [p, p⊕w) is contained within exactly one subspace of document d. The behavior selector (DEL1 vs DEL1a) is determined by which subspace contains the range.

### Issue 4: Operation journal used in specification claims but absent from declared state
**ASN-0005, DEL14(b.iii) and DEL15**: "The operation journal records the action" / "a journal record naming the deleted I-addresses."
**Problem**: The system state Σ is declared with four components: ispace, poom(d), spanindex, links. The operation journal is not among them. Yet DEL14(b.iii) names the journal as a reversal source, and DEL15 appeals to it for pre-deletion state preservation. This is an undeclared state component bearing specification weight. Either the journal is part of Σ (in which case declare it and state its invariants) or it is not (in which case do not appeal to it in specification claims about reversal).
**Required**: Either add the journal to Σ with its monotonicity properties, or remove DEL14(b.iii) and the journal claim in DEL15, leaving only the two journal-independent reversal sources (POOM and link endset).

### Issue 5: No weakest precondition analysis
**ASN-0005, throughout**: No wp computation appears anywhere in the ASN.
**Problem**: DELETE has non-trivial postconditions — particularly DEL1 (V-compaction with shifting), DEL6 (I-invariance under compaction), and the derived span-index forward inclusion. Computing wp(DELETE, "forward inclusion holds") would expose exactly what must be true before the deletion for the index to remain a valid superset afterward. This is the kind of non-trivial wp the review standards require.
**Required**: Compute wp for at least one postcondition where the answer is not "trivially the precondition." The span-index forward inclusion is a good candidate: wp(DELETE(d,p,w), ∀d',a: (∃q: poom'(d').q=a) ⟹ (a,d') ∈ spanindex') requires showing that DELETE's POOM shrinkage weakens the antecedent while P2 maintains the consequent — this is straightforward but must be shown, not assumed.

### Issue 6: DEL8 formalization uses undefined notation
**ASN-0005, "Ghost links and partial resolution"**: `resolve(L, endset, d) = {v_span : (E a ∈ endset(L) : poom(d).v_span = a)}`
**Problem**: `poom(d)` maps individual positions to addresses. The notation `poom(d).v_span = a` is undefined — a span is a range, not a position. The intended semantics is: collect all positions p where poom(d).p ∈ endset(L), then group maximal contiguous runs into spans. The formalization as written does not express this.
**Required**: Define resolution in terms of positions: `resolve_addrs(L, endset, d) = {p ∈ dom.poom(d) : poom(d).p ∈ endset(L)}`, then define span grouping as a separate step that collects maximal contiguous subsequences of resolve_addrs into spans. This makes the filtering and the grouping independently verifiable.

### Issue 7: Span-index forward inclusion asserted but not proven preserved by DELETE
**ASN-0005, "The span index divergence"**: "The forward inclusion holds — every live reference is indexed: (A d, a : (E p : poom(d).p = a) ⟹ (a, d) ∈ spanindex)"
**Problem**: This inclusion is stated as a fact. The ASN does not prove that DELETE preserves it. The argument is: DELETE removes entries from poom(d) (weakening the antecedent for d) and does not remove entries from spanindex (maintaining the consequent by P2); for d' ≠ d, poom(d') is unchanged by DEL2. The argument is short, but the ASN should state it rather than assert the conclusion.
**Required**: A two-case proof (d' = d and d' ≠ d) showing that DELETE preserves the forward inclusion. Three lines suffice.

## OUT_OF_SCOPE

### Topic 1: Ghost link discovery mechanism
**Why defer**: DEL7 defines the ghost state (no POOM maps to the endset addresses) and DEL13 claims ghost links can source identity-preserving COPY. But how does the system *find* a ghost link if no document's V-space reaches it? This requires specifying the link index's query capabilities independently of POOM traversal — a link-focused concern that belongs in an ASN on the link enfilade or link resolution.

### Topic 2: Full economic model under deletion
**Why defer**: DEL18 acknowledges "without developing a full economic model." The observation that I-space persistence preserves royalty obligations is sound as far as it goes, but the interaction between deletion, storage cost allocation, and ghost content economics is new territory.

### Topic 3: POOM entry fragmentation bounds
**Why defer**: The ASN's open questions correctly identify that cycles of INSERT, DELETE, and COPY can increase POOM entry count without increasing content size (especially given Issue 2's middle-split case). Bounding fragmentation is an enfilade-level concern that requires the tree rebalancing properties.
