# Review of ASN-0124

I checked the proofs case by case. The mathematics is sound: FD-IMGC's two-direction derivation correctly leans on S3★/S3★-aux/SD; the dynamics characterization (FD-FRAME/FD-STEP/FD-CWP) is exhaustive over the K-vocabulary and each clause is verified; FD-FRESH's composite is genuinely shown valid step-by-step with the couplings discharged initial-to-final, and the `I ⊆ dom(Σ.C)` restriction is load-bearing and used exactly where the freshness argument needs it (`A_new ∩ I = ∅`); FD-VDYN's four-way split is complete and the swing identity through FD-IMGC is correct; FD-WITNESS's two directions correctly route through P4a (⊆) and P4★+P2 (⊇) at composite boundaries; the worked illustration verifies the reorder-drop, the chain-severance, and the ghost set against concrete addresses, and I reproduced each. Boundary cases (empty `I`, empty arrangement, full clearance, append vs. mid-insert, empty intersection in FD-COOC) are handled. No proof-by-"similarly", no checkmark proofs, no undeclared cross-ASN references. The historical-companion claims derive locally from the cited ASN-0047 apparatus and are not re-raised here.

One finding remains, in the dimension this review cycle is explicitly tasked with.

## REVISE

### Issue 1: Forward-reference / roadmap meta-prose the precise reader must skip

The note is flagged `review-mode.anti-bloat`. The derivations advance the argument; the following prose does not, and clusters around the patterns the mode names (essay roadmap, downstream-consumer inventory, defensive justification, repeated deferral to the same downstream location).

**ASN-0124, The Problem**: "From address-keying flow identity-not-resemblance, flat chain reach, and stability under positional edits. From the present tense flow soundness against ghosts, non-monotonicity of the live answer, and the existence of a distinct, monotone *historical* companion query... From comprehension over the whole stratum flow completeness, asker-independence, and the impossibility of locality restrictions."
**Problem**: The first two sentences of that paragraph state the actual thesis (containment is present-tense, address-keyed) and earn their place. These three "From X flow A, B, C" sentences are a table-of-contents-in-prose previewing roughly ten downstream claims (FD-IDENT, FD-CHAIN, FD-FRESH, FD-SOUND, FD-GHOST, FD-NONMONO, FD-HIST, FD-COMPLETE, FD-ASKER, FD-LOCAL). They advance no reasoning; the reader skips to the thesis sentence and to the claims themselves.
**Required**: Drop the three roadmap sentences; retain the thesis (the design-decision sentence and its unpacking).

**ASN-0124, FD-RES, clause (c) discussion**: "Clause (c) is a genuine commitment, not an oversight; its information-theoretic consequences are FD-LOSSY below, and its compensation — that per-region structure is recoverable by issuing the regions separately — is FD-COOC."
**Problem**: This carries both a defensive justification ("a genuine commitment, not an oversight") and a downstream-consumer inventory for a definition (FD-RES) that enumerates FD-LOSSY and FD-COOC rather than advancing the definition's meaning — both flagged patterns. The flattening commitment is already plain from the definition (`resolve` returns a bare I-set); the consequences are stated where they belong, at FD-LOSSY and FD-COOC.
**Required**: State the flattening as the definition's postcondition without the defensiveness or the forward inventory; let FD-LOSSY/FD-COOC carry their own content.

**ASN-0124, FD-PART / FD-SOUND / FD-NONMONO** (deferral clustering): FD-PART defers — "The conjunctive 'contains all of it' question is not lost; it is a derived query, by composition — FD-COOC." FD-SOUND defers — "(What a query keyed on past containment looks like... is the subject of the historical-companion section.)" FD-NONMONO defers — "Contrast the historical companion below, which is monotone (FD-RMONO)" and "...why the composition of the two phases deserves its own lemma."
**Problem**: Multiple sections defer to the same two downstream locations (FD-COOC; the historical section), and FD-NONMONO additionally justifies the *existence* of the following lemma ("deserves its own lemma"). Individually brief, collectively the accretion the mode targets.
**Required**: Keep at most the single most informative pointer to each downstream location; remove the lemma-existence justification (FD-VDYN's presence needs no defense in prose).

## OUT_OF_SCOPE

The note's own Open Questions already defer the genuinely future material (interior-of-composite coherence, *when*-contained ordering, attribution-bearing refinement, past-arrangement reach, distributed-availability weakening, asker authority, provenance compaction, multiplicity exposure). These are correctly scoped out; I have no additional topic to add.

VERDICT: REVISE
