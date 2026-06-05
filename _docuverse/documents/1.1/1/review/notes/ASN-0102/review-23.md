# Review of ASN-0102

I checked the arrangement-displacement proofs (X7, X16), the wp/S3★ computation, the run-fragmentation argument (X8), the coupling discharge (X14), and the four worked examples. The mathematics is solid: the tiling argument in X16 is exhaustive across all three position classes and the boundary cases (p=1, p=n_S+1, empty subspace), the X8 within-reference argument correctly avoids the maturity-alone fallacy with a two-step V-adjacency-then-non-I-adjacency proof, and the J1★/J1'★ split via `New`/`Old` with the P4★ pre-state appeal is logically clean and non-circular. The self-transclusion and empty-subspace examples exercise the `Old ≠ ∅` and `New = A` branches properly.

The findings below are accretion, which this note's `review-mode.anti-bloat` classifier flags as the active concern. I found no correctness defects.

## REVISE

### Issue 1: Definition-section rationale explains why decisions matter rather than stating the contract
**ASN-0102, Definition of COPY**: "(We reserve the symbol `Σ` throughout this note for a system *state* ... so that the vocabulary to which COPY is added cannot be mistaken for the state on which COPY acts.)" and "Declaring COPY elementary — one indivisible event ... — is what underwrites both the atomicity guarantee (X15) and the pre-state resolution that makes self-transclusion well-defined (X10)."
**Problem**: The first is a defensive notation justification; the second is rationale-plus-forward-reference (to X15, X10) explaining why the elementary declaration is useful rather than stating what the definition is. Both match the flagged pattern "new prose around a definition explains why it is needed rather than what it says." A reader must skip past them to reach the five-component contract.
**Required**: State "COPY is an elementary transition added to 𝒦" and the frame; drop the parenthetical and the underwriting sentence. X10/X15 already carry their own derivations from SequentialTransitionAxiom.

### Issue 2: Provenance-effect rationale prose
**ASN-0102, Definition (Provenance)**: "Folding the K.ρ-style recording into COPY's own effect is what lets a single elementary transition meet the coupling obligation that the foundation otherwise discharges at a composite boundary."
**Problem**: This justifies the design choice rather than advancing the definition; the obligation it forward-references is discharged in X14. Rationale of this kind is noise in a definitional slot.
**Required**: Delete. The `Σ'.R = Σ.R ∪ {...}` clause plus X14's J1★ discharge already carry the content.

### Issue 3: Repeated deferral to X8
**ASN-0102, "The source designation and its resolution"**: "The precise relation between this constructed `k` and the canonical (maximally-merged) count is settled in X8; we do not assert equality here. We will return to both."
**Problem**: A forward-pointer-with-deferral that adds no reasoning at its site; "we will return to both" is pure scaffolding. Matches the flagged "multiple paragraphs defer to the same downstream location" pattern.
**Required**: State the constructed `k = Σ kᵢ` fact plainly and let X8 own the canonical-count relation without the announcement.

### Issue 4: X14 invariant inventory padded with relocated per-invariant callouts
**ASN-0102, X14**: "**ActivatedEmission** in particular carries forward because ..." and "**P6 (ExistentialCoherence)** is discharged separately, because it quantifies over neither the link store nor the entity set but over the *content* store ..."
**Problem**: Wholesale invariant discharge is legitimate, but these "in particular"/"discharged separately" callouts read like prior individual findings relocated into the paragraph rather than integrated — the flagged "paragraph looks like a prior finding's content relocated rather than removed" pattern. They re-explain frame facts (`Σ'.E = Σ.E`, `dom(Σ'.C) = dom(Σ.C)`) already stated in the same paragraph.
**Required**: Collapse the per-invariant callouts into the grouped frame-discharge sentences; the link/entity Class (a) conjuncts and P6 follow from the already-stated `Σ'.L = Σ.L`, `Σ'.E = Σ.E`, X1, X6 without individual restatement.

## OUT_OF_SCOPE

### Topic 1: The four Open Questions (re-displacement of copied content, transitive containment when a reference-holder becomes a source, time-varying views, identity under unreachable allocator)
**Why out of scope**: These concern later operations (subsequent displacement, version derivation, replication) explicitly excluded by the Scope block. They are correctly parked as open questions, not flagged as gaps in this note.

VERDICT: REVISE
