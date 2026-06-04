# Review of ASN-0091

## REVISE

### Issue 1: RE-C section is restatement plus motivational essay, redundant with the invariant discharge
**ASN-0091, "What the Content Store Sees: Nothing"**: "No content is allocated, freed, or modified by rearrangement. Every I-address in `dom(Σ.C)` retains its bound value; no new I-address enters `dom(Σ.C)`; the function `Σ.C` is literally unchanged. This is the architectural reason rearrangement cannot disturb content identity: the layer where identity lives is untouched."
**Problem**: The three clauses after the colon ("retains its bound value", "no new I-address enters", "the function is literally unchanged") all restate `Σ'.C = Σ.C` in different words, followed by a motivational sentence that advances no reasoning. The same content-store invariance is *independently* discharged in "State-Component-Only Invariants" via S0/C0. Content-store invariance is thus stated in two sections plus thrice within this paragraph.
**Required**: Collapse to the single claim `Σ'.C = Σ.C` (RE-C) with its RA-frame citation; drop the triple restatement and the "layer where identity lives" essay.

### Issue 2: Fragmentation is demonstrated by two separate full traces
**ASN-0091, "Run Decomposition Is Not Invariant" ("Direct witness (fragmentation)")** uses cut `([1,1],[1,2],[1,4])` on run `([1,1], a, 3)` to show cardinality 1→2. **Worked Example 1** then re-verifies RE-frag with the same cut on `[1,1]↦a₁, [1,2]↦a₂, [1,3]↦b₁`, again 2→3.
**Problem**: Two complete numeric fragmentation traces establish the same phenomenon (RE-frag). The coalescence and equality phenomena each get a single witness; fragmentation alone is doubled.
**Required**: Keep one fragmentation trace. Either drop the standalone "Direct witness (fragmentation)" and let Worked Example 1 carry RE-frag, or have Worked Example 1 cite the existing witness rather than reproduce it.

### Issue 3: Defensive justifications of example existence in the verification slots
**ASN-0091, "Worked Example — 4-cut Swap"**: "This +1 μ-displacement is not realisable under any 3-cut pivot, yet it violates no RE-* invariant".
**ASN-0091, "Worked Example — Interior Cuts"**: "The abstract class — RA-dom, RA-π, RA-frame, RA-adm — would permit a bijection that moved `[1, 1]` and `[1, 5]`; R-EXT is what pins them."
**Problem**: These closing sentences argue *why each example is worth including* rather than verifying a claim against the trace. The traces themselves already exercise R-SPERM and the non-empty exterior; the justification prose is meta-commentary the precise reader skips.
**Required**: Drop the justificatory sentences; the distinct mechanism each trace exercises is self-evident from the computation.

### Issue 4: Shared-I-address theme spread across four touchpoints
**ASN-0091**: The non-uniqueness of π is introduced abstractly ("REARRANGE as Vstream-Only Operation": "It is not in general unique: when `Σ.M(d)` has shared I-addresses … the assignment within each such block is free"), re-stated in the "Net-effect split" paragraph, then carried by *two* full worked examples ("Bijection Non-Uniqueness" and "Net-Effect Collapse"), both built on the same shared-image setup, with the second example back-pointing ("This is the bijection-non-uniqueness phenomenon described abstractly in the opening section").
**Problem**: The two distinct payloads — RE-proj uniformity under non-unique π, and the empty-realiser collapse branch — are each genuine, but the surrounding setup, abstract framing, and cross-references are duplicated. This is more surface area than the two facts require.
**Required**: Consolidate the abstract non-uniqueness statement and the net-effect-split prose so the shared-image licence is stated once; let the two worked examples carry only their distinct payloads without re-narrating the abstract phenomenon.

## OUT_OF_SCOPE

### Topic 1: Link-subspace REARRANGE semantics
The note's own Open Questions ask what semantics rearrangement should carry on the link subspace. CS3 fixes cuts to `s_C`, so this ASN correctly scopes to content-subspace rearrangement; link-subspace reordering is a future ASN, not a gap here.

### Topic 2: Reconstitution of a source span split across a cut
RE-trans establishes per-fragment origin preservation but explicitly declines to establish joint reconstitution of a split source span. This is correctly deferred to a future ASN (and flagged in Open Questions), not an error.

VERDICT: REVISE
