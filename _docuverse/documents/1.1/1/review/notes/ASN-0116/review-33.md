# Review of ASN-0116

I checked the composite decomposition (K.α×n → K.μ⁻ → K.μ⁺ → K.ρ×n), the I3-family citations, the block-disjointness attribution feeding I-NEW/I-DOM, the coupling-constraint discharge (J0/J1★/J1'★), the wp derivation (IP6), and the worked example. The technical content is sound and unusually thorough: the gapped-vs-filled distinction is handled correctly, the I3-V/I3-CS attribution of the vacated block is actually shown (not hand-waved), the range identity RAN correctly drives the provenance and discoverability arguments, and the worked example verifies IP4/IP6 against concrete addresses including the ghost-reference and resurrection sub-cases. The edge cases the checklist demands — front insertion (J=1), append (J=N+1), empty subspace — are each exercised. The OrdShiftHom `k=0` boundary is explicitly excluded rather than silently mis-cited.

The findings below are prose-level, surfaced under the note's `review-mode.anti-bloat` lens.

## REVISE

### Issue 1: Claim-bookkeeping meta-prose in the "Position permanence" discharge
**ASN-0116, "Invariants the operation must preserve" (Position permanence)**: "The I-address-permanence half is already carried by IP0 (every new binding is at a fresh address) and IP2 (no existing address removed or rebound); we therefore reserve the boxed claim for the V-position-impermanence half, which the prose above argues but no prior claim captures."
**Problem**: This sentence is editorial bookkeeping about *which claim covers what and why IP3 is scoped to half the invariant* — it explains the document's own claim inventory rather than advancing any reasoning about INSERT. It is exactly the "defensive justification in a structural slot" the anti-bloat lens targets; a reader following the position-permanence argument must skip it.
**Required**: Drop the bookkeeping sentence. IP3's scope is self-evident from its statement; the I-address half is already discharged by IP0/IP2 without an in-line note announcing the division of labor.

### Issue 2: Position-impermanence stated three times
**ASN-0116, "What shifts…" narrative, IP3, and "Position permanence" subsection**: the point "a V-position binds no permanent content; identity attaches to the I-address, not the slot" appears as narrative ("The shift is a relabelling of slots, not a transport of bindings"), as the boxed IP3 (PositionImpermanence), and again as prose in the invariant-discharge subsection ("the same slot `q_J` denotes different content before and after the insert").
**Problem**: Three full restatements of one idea in different words. The narrative motivates, IP3 formalizes — those two are a legitimate prose→claim pair — but the "Position permanence" subsection's prose re-argues the already-boxed IP3 rather than simply discharging the named invariant by citing it.
**Required**: Collapse the invariant-discharge subsection to a citation of IP3 (impermanence) + IP0/IP2 (permanence), without re-narrating the two-senses-of-position distinction already made in the "What shifts" section.

## OUT_OF_SCOPE

### Topic 1: Transclusion / concurrent-insertion / fragmentation guarantees
The four Open Questions (shared-position insertion, concurrent freshness without a serializing authority, transclusion-origin provenance, post-fragmentation contiguity) correctly defer genuinely new territory. These belong to ASN-0118 (COPY) and future concurrency/version work, not to this ASN. Their placement as Open Questions is appropriate — no action.

VERDICT: REVISE
