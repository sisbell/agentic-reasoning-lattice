# Review of ASN-0075

## REVISE

### Issue 1: Foundation Recap closes with an inaccurate forward pointer
**ASN-0075, end of "Foundation Recap"**: "We restrict attention to the content subspace throughout; the next section establishes why the restriction to `dom(C)` suffices to confine the operation to `s_C`."
**Problem**: This is forward-reference accretion in a recap slot. Worse, it is inaccurate: the *next* section ("The Three States of Content") does not establish s_C confinement — it only notes that `a ∈ dom(C) ⟹ subspace_I(a) = s_C` to justify dropping a conjunct. The confinement claim is actually D-SUBSP, several sections later. The sentence advances no reasoning and misattributes where the result is proved.
**Required**: Delete the sentence. The Foundation Recap should end at the CL-OWN bullet; D-SUBSP stands on its own.

### Issue 2: "Restriction to the Content Subspace" opens with a redundant backward pointer
**ASN-0075, "Restriction to the Content Subspace"**: "Confining the operation to the content subspace is enforced by the restriction to `dom(C)`, as established in *The Three States of Content*."
**Problem**: This sentence duplicates the content of the immediately following Claim D-SUBSP and its Justification, which independently re-derive `output ⊆ dom(C)`, `subspace_I = s_C` for content, and L14 disjointness. The backward pointer also misattributes the result to "The Three States of Content," which establishes only the per-address subspace fact, not the operation-level confinement. Two paragraphs in different sections asserting the same confinement with cross-pointers is exactly the accretion this note is flagged for.
**Required**: Remove the opening sentence; let Claim D-SUBSP and its Justification carry the result in one place.

### Issue 3: wp analysis depends on D-OBS, which is established only much later
**ASN-0075, "The SHOWDELETIONS Operation"**: "By D-OBS the operation modifies no state component, so wp computations for state-level predicates pass through unchanged from the pre-state."
**Problem**: The wp derivations for Q1 (non-emptiness) and Q0 (vacuity) rest on observationality, but D-OBS is not stated or proved until the "Observational Frame" section near the end. The reader must accept a forward-cited result to follow the wp section's central move. The dependency is non-circular (D-OBS does not depend on the wp analysis), so this is purely an ordering defect.
**Required**: Either move the observationality claim (D-OBS) before the wp analysis, or have the wp section establish "the definition is a pair of set-builder comprehensions over Σ, hence reads-only" inline without forward-citing the later claim.

### Issue 4: D-NEED corollary's "one step" framing contradicts its own length
**ASN-0075, Corollary D-NEED**: "The discrimination obligation follows from D-DISCR in one step." 
**Problem**: The argument then takes several steps — re-introducing the abstract component `C*`, re-exhibiting `R` as a witness, and re-deriving that DELETED/NEVER_INCLUDED differ on R-membership — material already set up in D-DISCR. The genuinely new content (extending discrimination from composite boundaries to *every* reachable state) is buried under restatement. The "in one step" claim is meta-prose that mischaracterises what follows.
**Required**: Drop the "in one step" framing and the C*-witness restatement; keep only the actual increment over D-DISCR — that R discriminates at every reachable state, not merely at composite boundaries.

## OUT_OF_SCOPE

### Topic 1: Multi-document and third-document witness generalisation
The Open Questions correctly defer "deleted from both but current in a third document" and "families of more than two documents" to future work. These are properly framed as questions, not claimed here. No action needed.

### Topic 2: Restoration / recovery operation semantics
D-ACT notes the output is consumable by I-address operations, and the final Open Question asks what a restoration operation must guarantee. Restoration mechanics belong to a future ASN; the current note correctly only asserts consumability, not restoration behavior.

VERDICT: REVISE
