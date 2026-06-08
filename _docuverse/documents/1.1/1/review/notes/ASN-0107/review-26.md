# Review of ASN-0107

## REVISE

### Issue 1: No-removal of links is re-derived in four places

**ASN-0107, E4 / D3 / R1 / "How the Count Changes: Links Retracted" intro**:
- E4: "the substrate provides no link-removal transition (L12), so no term subtracts."
- D3: "A link is never removed from `dom(Σ.L)` — the substrate provides no removal operation (L12)"
- R1: "No store-level link retraction exists"
- Section intro: "The substrate provides no link-removal transition (L12), and udanax-green confirms the design literally..."

**Problem**: The single fact — L12 forbids link removal — is restated four times in different words across consecutive claims. This is the "two paragraphs say the same thing" accretion the anti-bloat classifier targets; each claim re-derives the consequence locally rather than citing one statement of it.

**Required**: State the no-removal consequence once (the "Links Retracted" section intro, with its udanax-green evidence, is the natural canonical site) and have E4, D3, and R1 cite it rather than re-derive "no term subtracts" / "never removed" / "no retraction exists" independently.

### Issue 2: R3 and R4 presuppose multiple consulted arrangements that the discovery anchoring excludes

**ASN-0107, R3 and R4**:
- R3: "The conjunct fails only when *all* of slot-`i` coverage has left every consulted arrangement"
- R4: "A link drops only if all of its endpoint addresses leave every consulted arrangement"

**Problem**: The discovery anchoring is defined over a *single* querying document `d_q` — `Qᵢ(Σ) = {Σ.M(d_q)(v) : v ∈ Wᵢ ∩ dom(Σ.M(d_q))}`. The plural "every consulted arrangement" presupposes the multi-document anchoring that the note's own Open Questions explicitly defers ("when the three request parts are independently anchored to different documents' arrangements"). The prose reaches past the claim's carrier into territory the ASN has not defined.

**Required**: Phrase the failure condition against the single resolved part `Qᵢ(Σ)` (the conjunct fails when `coverage(Σ.L(a).eᵢ) ∩ Qᵢ(Σ) = ∅`), or scope the multi-arrangement reading explicitly to the open question.

### Issue 3: Method-narration in D2

**ASN-0107, D2**: "We reason about `Qᵢ` directly, as the forward image of a query region."

**Problem**: This sentence narrates *how* the proof proceeds rather than advancing it; the three per-transition clauses that follow already reason about `Qᵢ` directly and stand without the announcement. It is meta-prose in a structural slot.

**Required**: Delete the sentence; the extension/contraction/reordering clauses are self-supporting.

## OUT_OF_SCOPE

### Topic 1: Multi-document independent anchoring of the three request parts
**Why out of scope**: Correctly deferred to the Open Questions. The single-`d_q` discovery anchoring is the right unit for this ASN; the cross-document case is new territory (subject to Issue 2's phrasing fix).

### Topic 2: Relationship between `num` and the cardinality of the retrieval (FINDLINKS) result
**Why out of scope**: Retrieval is ASN-0099 per the stated scope; the count-vs-retrieval staleness question is appropriately left open.

VERDICT: REVISE
