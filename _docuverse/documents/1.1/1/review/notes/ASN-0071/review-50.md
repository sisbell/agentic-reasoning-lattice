# Review of ASN-0071

## REVISE

### Issue 1: Triple-restatement of the find predicate in F-ORIGIN section
**ASN-0071, "Home versus transcluding documents"**: "The mechanism is structural — the I-address `a` is the same `a` everywhere it appears, because content has permanent identity (P0); sharing of content corresponds to identity of I-address, and identity of I-address is what `find` tests for."
**Problem**: This sentence states one fact ("`find` matches on I-address identity, and content identity is I-address identity") three consecutive ways. The carrier claim (F-PART) and the definition of `find` already establish that membership is decided by I-address intersection; the restatement adds no new step. This is the "two paragraphs say the same thing in different words" pattern compressed into one sentence.
**Required**: Reduce to a single clause — the load-bearing content is only "`origin(a)` is a function of the tumbler (P6) so the home/transcluder distinction is recoverable without tagging." Drop the structural-mechanism restatement.

### Issue 2: ContentReference/`resolve` equivalence is non-load-bearing for the operation
**ASN-0071, "Resolution"**: the paragraph "When a vspec `(d_s, σ)` is also a well-formed ContentReference, `iaddrs_one(d_s, σ)(Σ)` equals the set-flattening of ASN-0058's `resolve(d_s, σ)` ... vspec resolution and well-formed-ContentReference resolution coincide exactly."
**Problem**: `iaddrs_one` is defined as a plain image `{Σ.M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s))}`. No claim in the table (F-iaddrs … F-FIN) depends on block decomposition or `resolve`; the operation's guarantees never invoke ASN-0058's run algebra. The worked scenario then computes resolution *twice* — once via the three-block `resolve` decomposition and once directly as the image — confirming the bridge is decorative. An entire derivation plus duplicated scenario computation establishing a relationship the specification does not use is accretion.
**Required**: Reduce the bridge to at most a one-line pointer ("when the span is a well-formed ContentReference, this image coincides with ASN-0058's `resolve`"), and drop the parallel `resolve`-based computations in the worked scenarios in favor of the direct image computation that already appears.

### Issue 3: Essay-style exegesis re-narrating already-proven claims
**ASN-0071, "Partial overlap suffices"**: "This is the operative reading of Nelson's promise to *'retrieve any portion ... regardless of where the native copies are located'* (LM 4/63). The clause carries two distinct commitments, each discharged here. *'Any portion'* governs result granularity ... *'Regardless of where the native copies are located'* governs location transparency ..."
**Problem**: The two "commitments" map exactly onto F-PART (just proven in this section) and F-CONTENT (proven earlier in "The operation"). The paragraph re-narrates two settled claims through a quote rather than advancing reasoning. A single motivating clause tying the claim to Nelson's promise would suffice; the two-commitment dissection is essay content occupying a proof slot.
**Required**: Collapse to one sentence naming the Nelson promise as motivation; do not re-derive F-PART/F-CONTENT under quote-exegesis headings.

## OUT_OF_SCOPE

### Topic 1: Relationship to historical containment relation R
The first Open Question (current-state result vs. permanent provenance `R`) is correctly deferred — connecting `find` to `R`'s ever-containing semantics is a future ASN, not a gap here.

### Topic 2: Rejection vs. silent filtering policy
The second Open Question (when to reject unresolvable vspec positions rather than filter via F-FILT) is a policy layer above the abstract query; correctly out of scope.

VERDICT: REVISE
