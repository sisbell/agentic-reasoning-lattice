# Review of ASN-0100

This is a strong, near-complete note. The invariant coverage is unusually thorough — every conjunct of ExtendedReachableStateInvariants is addressed, the per-state/composite-boundary distinction is respected, and the hard cases (D-CTG★ closed-interval reduction, S2 region-disjointness, the K.μ⁻/K.μ⁺ projection cancellation) are genuinely worked, not hand-waved. The findings below are about accumulated meta-prose and a notation reinvention, not about correctness gaps in the math.

## REVISE

### Issue 1: Proof-method justification in INS.proj

**ASN-0100, §Coverage and link discoverability (INS.proj, d' ≠ d branch)**: "LP4 (ArrangementSpecificity; ASN-0098) and LP5 (CrossDocumentIndependence; ASN-0098) are single-step lemmas ('for every transition Σ → Σ'), and INSERT is a composite of 2n+1/2n+2 elementary steps, so we must chain them rather than cite them once."

**Problem**: This is commentary about why the proof composes lemmas instead of citing one. The reader does not need to be told that a per-transition lemma must be applied per-transition across a composite; the actual chaining sentence that follows ("LP4 applied at each step... composing across the finite step sequence...") carries the argument by itself.

**Required**: Delete the methodological sentence; keep only the chaining derivation.

### Issue 2: Meta-prose about which intermediates "need" argument

**ASN-0100, §Atomicity and Canonical Order**: "The one genuinely novel intermediate is **post-K.μ⁻**; the other M-modifying step, K.μ⁺, produces the composite's final arrangement M'(d) (below), so only the contracted state needs a self-contained argument." And later: "are therefore not a fresh obligation: they are the very post-state assertions established in §Verifying the Invariants, which verified Σ' directly. No separate per-intermediate derivation exists to give."

**Problem**: These passages justify the document's organization (why no derivation is supplied for the K.μ⁺ intermediate) rather than advancing reasoning. The substantive fact — the post-K.μ⁺ arrangement equals M'(d) because subsequent K.ρ frames M — is enough; the surrounding "only X needs an argument / no derivation exists to give" is the deferral-justification pattern.

**Required**: State the fact (post-K.μ⁺ arrangement = final M'(d), already verified for Σ') in one sentence; drop the prose about which obligations are "fresh."

### Issue 3: Same frame fact justified three times by three authorities

**ASN-0100, §Effect Three, §Formal Contract (Frame Conditions), §Coverage (INS.proj)**: the cross-document and cross-subspace frames are asserted in §Effect Three via "I3-D (ASN-0082)" / "I3-X (ASN-0082)", restated in the Formal Contract via each K-step's per-step frame, and re-derived a third time in INS.proj via LP4-chaining.

**Problem**: Importing the frame from ASN-0082's I3 lemmas (which are themselves postconditions of an insertion operation) while also deriving the identical frame from the substrate composite's K-step frames is redundant, and leaves it ambiguous whether INSERT's frame is *defined* by the substrate decomposition or *inherited* from ASN-0082's prior characterization. One authority should be load-bearing.

**Required**: Pick the substrate-composite K-step frames as the single source (consistent with INS.def making INSERT a composite), and cite ASN-0082 I3 only where it adds something the K-frames do not.

### Issue 4: shift(·,0) identity convention re-declared instead of cited

**ASN-0100, §The Operation's Inputs (Notational convention)**: "We adopt `shift(t, 0) := t`, extending OrdinalShift (ASN-0034), which is defined only for n ≥ 1."

**Problem**: The k=0 ordinal-shift identity is already a foundation convention — ASN-0058's OrdinalShiftBase fixes `t + 0 = t` ("the identity of ordinal shift"), and ASN-0036's S8 already operates "Under the convention `shift(t, 0) := t`." Re-declaring it here as a fresh convention reinvents notation a foundation supplies (standard #7).

**Required**: Cite OrdinalShiftBase (ASN-0058) / the S8 convention (ASN-0036) for the k=0 identity rather than introducing it.

## OUT_OF_SCOPE

### Topic 1: Closure of INSERT under composition, concurrency serialization, derived-metadata updates
**Why out of scope**: These are the note's own Open Questions and correctly deferred — they concern multi-operation algebra, concurrency, and derived state, none of which a single-INSERT per-state specification must answer.

VERDICT: REVISE
