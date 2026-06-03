# Review of ASN-0075

## REVISE

### Issue 1: Observationality is asserted three times across separate sections

**ASN-0075, "The SHOWDELETIONS Operation" / wp(Q0) paragraph / "Observational Frame"**: The fact that SHOWDELETIONS only reads state is established in three places: the post-definition paragraph ("it allocates nothing, rewrites nothing, and invokes no transition relation. Observationality is therefore immediate from the definition (the full frame is recorded as D-OBS)"), the wp(Q0) paragraph ("Since SHOWDELETIONS only reads state (established above)..."), and the D-OBS claim itself ("The operation reads M(d_A), M(d_B), and R... No transition relation is invoked").

**Problem**: This is the duplicate-statement pattern compounded with a forward reference. The post-definition paragraph asserts observationality informally and points forward to D-OBS, which then re-states the same content formally. The wp(Q0) paragraph re-derives it a third time. Two paragraphs in the document say the same thing in different words, and the early assertion creates a forward dependency on the claim that canonically establishes it.

**Required**: State the observational frame once (in D-OBS), and let the wp pass-through and Q0 derivation cite that single claim rather than re-asserting or pre-asserting it.

### Issue 2: D-DISJ claim statement contains meta-prose contrasting itself with the wp formula

**ASN-0075, "D-DISJ"**: "This is a sufficient condition for vacuity not given by the `wp(SHOWDELETIONS, Q0)` formula above, which characterises emptiness through the current arrangements `M`; D-DISJ characterises it through `R` alone."

**Problem**: This sentence does not advance the lemma; it editorializes about how D-DISJ relates to a different result stated earlier (characterizing-through-M vs. characterizing-through-R). It is a defensive/comparative gloss inserted into a claim statement. The reader following the proof must skip past it.

**Required**: Remove the comparative sentence. The lemma statement and proof stand on their own; the relationship to the wp(Q0) formula is not needed to use or verify D-DISJ.

### Issue 3: Forward-reference parentheticals to downstream claims

**ASN-0075, "Foundation Recap" close and "The Three States of Content" open**: "We restrict attention to the content subspace throughout (the operation is confined to `s_C`; see D-SUBSP)." and "(the full frame is recorded as D-OBS)".

**Problem**: These parentheticals point forward to claims defined many sections later, the forward-reference accretion this review mode targets. The substantive justification already lives in D-SUBSP and D-OBS; the early pointers add navigation overhead without advancing the local argument.

**Required**: Drop the parenthetical forward pointers. The restriction to `s_C` is already enforced by the `dom(C)` restriction (stated immediately), and observationality is established at D-OBS.

### Issue 4: Bundle-pattern citation-convention prose is justificatory rather than load-bearing

**ASN-0075, D-DISCR, "Throughout both histories..." paragraph**: "We cite 'the bundle pattern' at each composite below rather than re-deriving this discharge at every step."

**Problem**: The bundle-pattern definition itself is useful compression, but the closing meta-sentence explains the citation convention rather than the argument. It is the "why I am abbreviating" gloss that accretes around proofs across cycles.

**Required**: Keep the bundle-pattern definition; delete the sentence announcing that it will be cited. Citing it at each use site is self-explanatory.

## OUT_OF_SCOPE

### Topic 1: Restoration, multi-document families, concurrency, span-presentation of deletion sets
**Why out of scope**: These appear only in the Open Questions section, correctly framed as future work rather than claims of this ASN. No action needed — flagging only to confirm they were checked and are appropriately deferred.

VERDICT: REVISE
