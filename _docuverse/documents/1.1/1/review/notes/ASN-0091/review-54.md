# Review of ASN-0091

This is a mathematically careful note — I checked the run-decomposition witnesses (fragmentation 1→2, coalescence 3→2, equality 2→2), the four worked examples, and the projection/coverage arithmetic, and the substance holds up. The ChainDisjointAdjacency inline lemma is sound and its sig=# precondition is correctly fixed. No correctness defect surfaced. The findings below are accreted meta-prose, which this note's `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: The collapse/non-trivial case split is stated three times in different words
**ASN-0091, "REARRANGE as Vstream-Only Operation" and "REARRANGE_K Realises the Abstract Class"**: The same distinction — that the cut-induced π may be non-identity yet leave `M'(d) = M(d)` — is restated across four passages:
- "This makes π non-identity *as a permutation of V-positions*, but that is strictly weaker than ASN-0047's K.μ~ admissibility clause (ii)... The two come apart whenever the affected-range value sequence is *invariant under the cut-induced block permutation*."
- "We therefore split the realisation by whether the cut-driven π produces a net change..."
- "its realiser is ASN-0047's K.μ~ in the non-trivial case and the identity composite in the collapse case."
- "REARRANGE_K carries no non-triviality precondition: it remains defined wherever R-PRE holds, collapsing to the identity precisely on affected ranges fixed by the cut-induced permutation."

**Problem**: The concrete S5 witness ("a 3-cut pivot with `w_α = w_β = 2`...") is load-bearing and should stay. The surrounding prose re-explains the `π ≠ id` vs `M'(d) ≠ M(d)` gap repeatedly. This is "two paragraphs in the same document say the same thing in different words," compounded to four.
**Required**: State the distinction once (with the S5 witness), record the case split in one sentence, and cite it where the realiser is selected rather than re-deriving it.

### Issue 2: Duplicate frame-inherited invariant inventory
**ASN-0091, "State-Component-Only Invariants" and the Worked Example RA-adm bullet**: The full list of frame-inherited invariants is enumerated twice. First: "...S0, S1, S4, S7, S7a, S7b, S7d ... P0, P1, P2, P3, P6, P7, P7a, P8, NodeLineage, ActivatedEmission, L0, L1, L1a, L1b, L1c, L3, L12, L14, L-fin, C0, C1, C1b, C1c, C2, and C-fin." Then in the Worked Example: "...P0, P1, P2, P3, P6, P7, P7a, P8, NodeLineage, ActivatedEmission, L0–L14, L12, L-fin, C0–C2, C-fin."
**Problem**: A use-site inventory restated verbatim across sections. The Worked Example re-enumeration adds nothing beyond the general claim already made.
**Required**: Keep the enumeration once (in "State-Component-Only Invariants"); have the Worked Example cite it rather than re-list it.

### Issue 3: Prose-and-table redundancy in clause correspondence
**ASN-0091, "Clause Correspondences and Per-Invariant Discharges"**: The RA-reg discharge is stated in prose — "ASN-0047's K.μ~ precondition `d ∈ E_doc` discharges RA-reg directly: ASN-0047's M1 ... records the identification `dom(M) = E_doc`..." — and then again as a table row: "RA-reg | K.μ~'s precondition `d ∈ E_doc`, via the unification `E_doc = dom(M)`."
**Problem**: The two clause-correspondence tables duplicate the prose immediately surrounding them; the RA-reg row is the clearest instance. Mapping tables that restate adjacent prose are inventory accretion.
**Required**: Choose one form — table or prose — for the clause correspondences, not both.

### Issue 4: Essay-flavored parenthetical restating RE-origin
**ASN-0091, "Origin and Provenance Invariance"**: "(More precisely: origin is a function on tumblers, not state, so it has no temporal dimension at all. RE-origin records the fact that REARRANGE consumes no degree of freedom that origin depends on.)"
**Problem**: RE-origin's content ("origin consults only the address `a`... invariant across every state transition") is already established in the preceding sentence. The parenthetical re-expresses it in informal terms ("no temporal dimension," "consumes no degree of freedom") without advancing the claim.
**Required**: Delete the parenthetical; the structural statement above it is sufficient.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: REARRANGE_K's cut sequence is fixed to the content subspace (CS3, ASN-0084). The note correctly routes link-subspace rearrangement to Open Question #2 rather than specifying it here.

### Topic 2: Upper bound on run-cardinality increase / cut-sequence completeness
**Why out of scope**: The note proves run cardinality is non-monotone (RE-frag/coal/eq) but leaves the magnitude bound and the realizability of arbitrary well-formedness-preserving bijections to Open Questions #4 and #5. These are new territory, not defects.

VERDICT: REVISE
