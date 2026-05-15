# Review of ASN-0043

## REVISE

### Issue 1: PrefixSpanCoverage misplaced
**ASN-0043, body**: "**Lemma — PrefixSpanCoverage.** For any tumbler `x` with `#x ≥ 1`, `δ(1, #x)` ... `coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}`"
**Problem**: This lemma is a property of tumbler addresses and unit-depth spans — it has no link-specific content. It establishes a coverage identity applicable wherever such spans appear (and is used by L10, L13, and the worked example's coverage discrimination). Its proof traverses T1 cases, Divergence, NAT-discrete promotion, and OrdinalShift — pure span-algebra material. ASN-0043 becomes a venue for span-algebra results, mixing concerns. (See memory note: span-algebra-gap.md.)
**Required**: Relocate PrefixSpanCoverage to a span-algebra or tumbler-algebra ASN and cite it from ASN-0043. ASN-0043 should consume the lemma, not prove it.

### Issue 2: L0 content-side strengthening understated
**ASN-0043, L0**: "The two universals are not symmetric in derivational status. ... The content-side universal *strengthens* ASN-0036. ... Read as a refinement of ASN-0036, L0 is the joint declaration of (a) the link-subspace constant `s_L` ... and (b) the content-subspace constant `s_C` (an addition to ASN-0036's content model)."
**Problem**: The content-side universal `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)` is presented as a parenthetical observation rather than as a structural change to the content store. ASN-0036 admits per-document content subspaces; ASN-0043 silently makes the content subspace a global system constant. A reader looking only at the L0 invariant statement would not realize a content-store axiom has been added — the strengthening is buried in the discussion paragraph.
**Required**: Either (a) name the content-side claim as its own labeled invariant (e.g., L0a) with an explicit "amends ASN-0036" notation, or (b) record it as a candidate amendment to ASN-0036 to be propagated under a coordinated revision. Either way, the implications for ASN-0036 — whether further content-store invariants need updating to consume the global constant — should be addressed, not deferred.

### Issue 3: L9 Case A freshness left implicit
**ASN-0043, L9 proof, Case A**: "*Allocation of `a` (fresh link address under `d'`). By L-fin ... Invoke a T10a-conforming allocator for `d'`'s link subspace, yielding a fresh `a` ... and `a ∉ dom(Σ.L)` (by GlobalUniqueness, ASN-0034, applied to the fresh allocation event against the prior allocations of links in `dom(Σ.L)`)."
**Problem**: The appeal to GlobalUniqueness on a "fresh allocation event" leans on the event/chain distinction L1c's reading paragraph introduces — a distinction the proof has not yet stabilized at this point. The more direct derivation is available: Case A's hypothesis `{b ∈ dom(Σ.L) : home(b) = d'} = ∅` combined with chain-prefix-preservation (`home(a) = d'`) directly forces `a ∉ dom(Σ.L)`, with no recourse to GlobalUniqueness on events. The proof does not state this derivation, leaving the reader to reconstruct it from the case hypothesis.
**Required**: State the freshness argument explicitly using the case hypothesis: under Case A's hypothesis no existing link has home = d'; the constructed `a` has `home(a) = d'` by chain-prefix-preservation along the L1c witness chain; therefore `a ∉ dom(Σ.L)` directly. The GlobalUniqueness appeal can then be dropped from this case, sharpening the proof.

### Issue 4: L1c's "Reading of the chain" paragraph creates a notational debt that is not paid
**ASN-0043, L1c**: "L1c's existentially-witnessed chain is a *structural producibility* witness... It is not an event log over operational allocation history... The per-(t, k') at-most-once constraint of T10a ... constrains the system's *cross-chain* allocator landscape across genuine allocation events, not the structural witnesses by which L1c attests producibility of each `a`."
**Problem**: The paragraph introduces a structural-witness vs. allocation-event distinction that downstream proofs (L11a, L9 Case A) silently rely on. But the ASN never makes "allocation event" precise as a separate concept — the term appears in L11a's preconditions ("distinct allocation events") and in L9's freshness argument without a definition. The reader must infer that "events" inhabit some event-level layer outside the chain framework, but the ASN doesn't formalize that layer. Either events should be elevated to first-class objects in the model (with their own existentials linking them to chains), or the reliance on the distinction should be removed and arguments routed through structural facts alone (as L9 Case B does cleanly).
**Required**: Either define "allocation event" formally (e.g., as a specific (state, t, k') triple firing at a known transition) and tie L1c's chain to a sequence of such events; or rewrite L11a and L9 Case A to use only structural arguments (L-fin, T10a.7, T10a.6 domain disjointness) without invoking events. The current state — informal "events" leaning on a footnote's distinction — leaves the foundation under L11a's uniqueness argument ambiguous.

## OUT_OF_SCOPE

None. The Open Questions list and Scope section cover the deferred territory (operations, query semantics, compound link well-formedness, transclusion-arrangement consistency, version mechanics) appropriately.

VERDICT: REVISE
