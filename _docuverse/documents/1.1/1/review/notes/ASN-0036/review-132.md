# Review of ASN-0036

## REVISE

### Issue 1: Coalescing/maximal-run caveat stated three times

**ASN-0036, Span decomposition (head) and S8 conjunct (b) paragraph**: Head: "Whether contiguous V-ranges ... can be *coalesced* into longer maximal runs ... is a separate question." Conjunct (b) paragraph: "Whether adjacent singletons coalesce into longer maximal runs is the separate compaction question noted at the head of this section; S8 does not establish it."

**Problem**: The same scope disclaimer appears at the section head, again in the conjunct-(b) paragraph (which explicitly defers back — "noted at the head of this section"), and a third time in Open Questions ("Must the span decomposition ... have a unique maximal form ..."). This is the defer-to-same-location / duplicate-paragraph accretion pattern; the reader must skip the same caveat twice to reach the proof.

**Required**: State the coalescing caveat once. The Open Question is its proper home; remove the two in-body restatements or collapse them to a single clause.

### Issue 2: S7 dependency list stated three times

**ASN-0036, S7**: "S7 follows from S7a (document-scoped allocation ensures ...), S7b (...), S7d (...), T4 ..., and GlobalUniqueness ..."

**Problem**: This narrative dependency inventory duplicates the proof's four labelled sub-arguments (Well-definedness / Identification / Uniqueness / Permanence) and the Formal Contract's *Depends* clause. The same premise list is recited three times in one property. This is the use-site-inventory accretion pattern.

**Required**: Drop the narrative recitation; the proof structure and the *Depends* clause already carry it.

### Issue 3: "not re-derived here" meta-prose in projection contracts

**ASN-0036, subspace_I postcondition (b) and subspace postcondition (b)**: "established at S7b ... this is read off at the first element-field component, not re-derived here." / "S8a's componentwise positivity at `i = 1` gives `v₁ ≥ 1`; not re-derived here."

**Problem**: "not re-derived here" is meta-prose explaining why duplication was avoided rather than advancing the claim. Stating the source (S7b / S8a) is sufficient.

**Required**: Cite the source and stop; delete the "not re-derived here" justifications.

### Issue 4: Operation-layer references embedded in position predicates

**ASN-0036, ValidFirstInsertionPosition / surrounding prose**: "`m` is an operational input chosen by the placing operation"; "Basic INSERT typically commits to `m = 2`"; "After an operation places new content at ... Verifying this is the operation's obligation, not the predicate's."

**Problem**: Operation-specific effects (INSERT frame conditions, allocation conventions) are explicitly out of scope for this ASN. These references couple a state-level predicate to operation mechanics that belong to a later operation ASN, and they read as scaffolding for work not done here.

**Required**: State the predicate purely in state terms (a position `v` of depth `m ≥ 2` equal to `[1,...,1]`). Remove the "placing operation" / "Basic INSERT commits to m=2" framing; defer the choice-of-`m` discussion to the Open Question already present.

### Issue 5: S8's existence claim is discharged only by the degenerate witness

**ASN-0036, S8 Postconditions**: "(b) `Σ.M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` for ... `0 ≤ k < nⱼ`" with the proof exhibiting "the singleton decomposition (every `nⱼ = 1`)."

**Problem**: The proof establishes only that a finite function decomposes into singletons, for which conjunct (b) collapses to the base case. The non-trivial content of (b) (the ordinal-displacement identity at `k ≥ 1`) is never established for any actual arrangement — yet the worked example asserts a length-5 run `(1.1, 1.0.1.0.1.0.1.1, 5)` as "the" decomposition S8 yields, which the theorem does not produce. The contract promises a "span decomposition" apparatus that the proof does not earn beyond the trivial partition.

**Required**: Either (a) restrict the stated postcondition to what is proven (singleton partition with disjoint intervals), letting the run/`nⱼ` apparatus be introduced where coalescing is actually established; or (b) explicitly mark the worked-example 5-run as an illustration of the *definition* of a correspondence run, not of the theorem's output, so the example does not appear to be a consequence of S8.

## OUT_OF_SCOPE

### Topic 1: Whether editing operations preserve D-CTG / D-MIN / S2

The Open Questions raise this; it is correctly deferred. Operation frame conditions belong to a future operation ASN, not here.

### Topic 2: Canonical choice of V-position depth `m`

Which downstream capabilities each depth unlocks is genuine future territory; the lower bound `m ≥ 2` is all the strand model owes.

VERDICT: REVISE
