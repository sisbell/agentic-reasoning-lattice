# Review of ASN-0101

This ASN is mathematically sound. I checked D0's precondition reduction, D1's gap-closure bijection, D8's three-group invariant sweep (all per-state invariants from ASN-0047's ExtendedReachableStateInvariants are covered), the worked examples, the boundary-case enumeration, and the D11 wp derivations. The reasoning holds; the wp analysis is non-trivial and correctly derived; cross-references are all to foundation ASNs (permitted). No correctness REVISE items.

The findings below are anti-bloat, per this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Use-site inventory in the ℓ_σ notational convention
**ASN-0101, "The operation" (parameters)**: "we write `ℓ_σ` for the span width of `σ` and reserve `ℓ` for link addresses (members of `dom(L)`); the subscript prevents confusion with the link-address variable `ℓ` used in D3, D9, D11, and elsewhere."
**Problem**: The clause "used in D3, D9, D11, and elsewhere" enumerates downstream consumers of the notation rather than advancing the convention's meaning — the flagged definition-introduces-its-consumers pattern. The disambiguation stands on its own without the inventory.
**Required**: Cut "used in D3, D9, D11, and elsewhere"; "reserve `ℓ` for link addresses" already fixes the convention.

### Issue 2: Structural meta-prose in D11's cross-document cardinality bullet
**ASN-0101, D11 (cross-document cardinality bullet)**: "The bullet is the cardinality analogue of the cross-document discoverability bullet above and completes the symmetry between the four projection-postcondition cases (discoverability and cardinality, from `d` and from `d'' ≠ d`)."
**Problem**: This sentence describes the document's structure rather than the claim. The wp equation and its one-line justification carry the content; the symmetry commentary is essay in a claim slot.
**Required**: Delete the sentence. The bullet's equation and pullback justification are self-contained.

### Issue 3: Discursive restatement in the recoverability section
**ASN-0101, "A note on recoverability and historical reconstruction"**: "This division of labour is structural. The DELETE operation is simpler than recoverable-DELETE would have to be; the versioning mechanism is independent of the DELETE operation; both contribute to the system-level guarantee."
**Problem**: The substantive content — D2 + D5 make recovery possible conditional on a versioning mechanism, and DEL alone is information-destroying w.r.t. `M(d)` — is already stated in the two preceding "necessary/not sufficient" paragraphs. This closing paragraph re-narrates the same point without adding a guarantee.
**Required**: Remove the paragraph; the necessary/not-sufficient statements above already establish the substrate-vs-mechanism split.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
