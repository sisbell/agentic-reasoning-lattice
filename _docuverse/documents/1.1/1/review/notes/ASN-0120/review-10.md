# Review of ASN-0120

The algebra here is solid — the V→I confinement step (T5 + ordinal displacement), the ML2 surplus-descendant argument (`#E = 2` exact bound), and the ML9 weakest-precondition derivation including the `d' = d` boundary case are all carried through with real steps, a worked example, and a non-trivial wp. I found no correctness gap in the proofs. The findings below are the forward-reference accretion and reviser-drift the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: ML6 defends against a case its own precondition excludes
**ASN-0120, "Three endsets" section (ML6)**: "Matching by address does not, for MAKELINK, license a ghost type. The type argument is `ρ`-resolved exactly as from and to (ML3), so `ρ(R₃, Σ) ⊆ dom(Σ.C)` ... MAKELINK therefore does *not* exercise L9's general ghost-type permission, which would require minting a type reference to unstored content — something `ρ` cannot produce."
**Problem**: This is reviser drift — the paragraph imagines a ghost-type scenario that ML6's own precondition (`ρ(R₃,Σ) ≠ ∅`, and `ρ ⊆ dom(Σ.C)` already established for every endset in ML1) structurally forbids. The claim that MAKELINK "does not exercise L9" is a negative defense against a path `ρ` cannot take. The substantive content — type matched by address (L8), classifier vs bare connection — survives in two sentences; the L9 non-exercise argument is meta-prose.
**Required**: State what the third endset is (an address-matched classifier, L8) and drop the L9 ghost-type rebuttal, or compress it to a single clause noting the type resolves to content like any other endset.

### Issue 2: Defended omission in the wp `enabled` predicate
**ASN-0120, ML9 derivation**: "Source-document allocation is *not* a separate conjunct of `enabled`, and its absence is deliberate, not an omission. ... So definedness of `ρ(R₁, Σ)` ... is presupposed by well-formed input rather than guarded by `enabled` ..."
**Problem**: This is the reviser-drift pattern of justifying why something is *not* present. The paragraph argues at length that a conjunct the author chose to leave out is intentionally left out. The reader does not need the negative-space defense; they need the definition of `enabled`, which is given one line earlier.
**Required**: Remove the "absence is deliberate, not an omission" defense. If well-formed spec-sets guarantee allocated sources, state that once as a property of the argument type, not as a justification for the shape of `enabled`.

### Issue 3: Use-site inventory and non-use justifications around the resolution proof
**ASN-0120, resolution section**: (a) "This exact bound is load-bearing twice over: it is what makes the creation-state equality ... (ML1, ML2) hold ... and it is what keeps that equality intact under later `K.α` allocation (ML8) ..."; (b) "(In the ASN-0047 substrate S3★ supersedes ASN-0036's S3, which alone would not discharge the containment ... Note we cannot lean on ASN-0058's C0/C0a here — those force action point `= m` only for a *well-formed* content reference ... so the confinement is re-derived directly ...)"
**Problem**: (a) enumerates the downstream consumers of the `#E = 2` bound ("load-bearing twice over ... ML1, ML2 ... ML8") rather than advancing the bound's meaning — a use-site inventory. (b) is a defensive justification explaining why two foundation results (S3, C0/C0a) are *not* the ones invoked; it is reasoning about the proof's provenance, not the proof. Both force the reader past meta-prose to reach the actual confinement argument.
**Required**: Keep the `#E = 2` derivation and the S3★-based containment step; drop the "load-bearing twice over" inventory and the parenthetical accounting for which foundation lemmas were declined.

### Issue 4: Editorializing inside the implementation notes
**ASN-0120, ML6 parenthetical**: "... the latter even debug-prints the missing-type pointer, an acknowledged accommodation rather than a rejection ... The abstract operation forbids what the implementation tolerates; the precondition is the correct contract."
**Problem**: The CREATELINK behavior (empty type sporgl passes the guards) is legitimate concrete evidence and should stay. The closing editorial sentences — "an acknowledged accommodation rather than a rejection" and "the precondition is the correct contract" — are essay content asserting that the spec is right and the code is wrong, which the precondition statement already conveys. Editorializing, not evidence.
**Required**: Retain the factual description of CREATELINK's behavior; remove the evaluative closing sentences.

## OUT_OF_SCOPE

The four Open Questions (endset run ordering, empty non-type endsets, link-subspace endset targets, no-document discoverability and resurrection) correctly defer genuinely new territory rather than gaps in this ASN. No additional out-of-scope items.

VERDICT: REVISE
