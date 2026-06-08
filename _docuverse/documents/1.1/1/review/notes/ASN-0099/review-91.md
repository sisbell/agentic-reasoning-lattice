# Review of ASN-0099

I checked the mathematics in detail: the definitions (`image`, `findlinks`, `findlinks_V`, `findlinks_filtered`, `findlinks_scoped`), the algebraic properties (F8, F13, F20, F20a), the wp analysis (F21–F23), the K.λ delta characterization (F9-λ), and the six-query worked example. The substantive content is sound, complete, and carries the required depth (non-trivial wp, concrete worked example, boundary cases). The cross-ASN references are all to foundation ASNs (0034, 0036, 0043, 0047, 0058, 0093, 0098), so none violate the self-containment rule. My findings are confined to prose accretion the `anti-bloat` classifier directs me to surface at source.

## REVISE

### Issue 1: Use-site inventory inside ComprehensionInvariantUnderΣL
**ASN-0099, "Determinism and Comprehension Invariance"**: "The chain: ... Predicates built from these — F1's existential, the filtered form's universal, scoped intersection — evaluate identically at the two states."
**Problem**: The meta-lemma's statement is already fully generic ("for every comprehension over `dom(Σ.L)` whose membership predicate consults only `Σ.L` and query-data"). Enumerating the three specific downstream consumers (F1's existential, the filtered universal, scoped intersection) inside the proof chain adds nothing to the lemma's meaning — it is a use-site inventory, exactly the pattern that compounds across cycles. The generic conclusion plus "set extensionality closes the equality" suffices; each consuming claim already cites the meta-lemma at its own point of use.
**Required**: Drop the consumer enumeration from the proof chain. Let the generic statement stand; the individual claims (F8, F15, etc.) already invoke it where needed.

### Issue 2: Reader-intent essay coupled to a design decision
**ASN-0099, "The Match Predicate"**: "the reader's question — what connects here? — does not privilege from over to."
**Problem**: The substantive justification for the uniform slot-existential is L7 (directional significance lives in the link type), already cited in the same sentence. The trailing reader-intent gloss is essay content that does not advance the argument — the design point stands entirely on L7. The same narrative thread reappears in F6's closing ("the document of origin vanished from the computation") and the "Identity, Not Value" coda.
**Required**: State the slot-uniformity decision on its L7 grounding and remove the reader-intent restatement. Keep one motivational framing (the intro) rather than re-seeding it at each property.

## OUT_OF_SCOPE

None. The non-goals listed under "What We Have Not Specified" (FOLLOWLINK/RETRIEVEENDSETS, replication, caching, access control) are correctly deferred and not specified here.

VERDICT: REVISE
