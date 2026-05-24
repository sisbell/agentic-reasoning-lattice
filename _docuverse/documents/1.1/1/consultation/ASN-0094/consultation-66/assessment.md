# Channel Assignment — ASN-0094 review-66

**Date:** 2026-05-24 11:14

## Issue 1: Cross-ASN reference to non-foundation ASN-0093
Reason: Internal fix — the ASN already has scaffolding clauses (*Per-document link sub-allocator chains*, *Link sub-allocator chain-index function*) that route ASN-0093 facts through ASN-0086's SubstrateConformingLayer interface. Replacing the direct ChainMembershipForOrigin citation with the existing scaffolding name is a textual substitution requiring no external input.

## Issue 2: Cross-ASN references to ASN-0036 in SubstrateConformingLayer definition
Reason: Internal fix — same routing pattern as Issue 1. The SubstrateConformingLayer Definition lives in ASN-0086 (foundation); the local fix is to cite the Definition by name rather than reproducing its enumerated catalog, which is a wording change derivable from the ASN's own scaffolding conventions.

## Issue 3: New axioms in Appendix not in foundation
Reason: Internal mathematical decision — the choice between (a) restructuring NAT-card and NAT-sub to use only listed axioms, (b) acknowledging the foundation extension request more explicitly, or (c) re-deriving the supplements from listed axioms rests on the ASN's own mathematical content. The non-derivability arguments are self-contained derivations that can be verified or revised within the appendix.

## Issue 4: Sh5 per-shape uniformity downgraded mid-document
Reason: Internal consistency fix — the downstream catalog claims (Resolution "inherits" from DirectedPair, "mechanically derived from same templates") need to be re-worded to match the downgraded aspiration status, or the discipline needs to be re-elevated with a procedural recipe. Both options are framework-internal catalog-curation decisions requiring no external evidence.

## Issue 5: Sh5(b) discipline is only procedurally falsifiable
Reason: Internal discipline-level decision — the framework's own commitment about whether Sh5(b) is "META discipline" or "documentation aspiration" rests on the ASN's framing choices. Committing to a tooled verification recipe is a framework-internal extension; downgrading the status is a framework-internal wording change.

## Issue 6: Hand-wave at K.λ frame-condition routing
Reason: Internal citation-precision fix — ASN-0086's `→ — DomExtendingTransition` Definition directly specifies K-op frame conditions, so the cleaner citation route is available within the foundation. Replacing the SubstrateConformingLayer routing with the direct citation is a wording change.

## Issue 7: Sh0/Sh1 Case A's exhaustiveness not fully explicit
Reason: Internal fix — adding the explicit citation to ASN-0086's `L_K^Σ` Definition (its `~`-class indexing clause) at Case A's K.λ-at-non-K-type sub-case is a textual addition derivable from the foundation's own definitions.

## Issue 8: Worked example for Sub-case II.B contradicts its own framing
Reason: Internal example/proof consistency fix — the contradiction between the worked example's concrete component values and Step II.2's structural claim can be resolved by either selecting a different worked example or rephrasing the example's framing. Both options are derivable from the proof's own structure.

## Issue 9: NullifyActiveSubsetCompatibility's "single-tuple scope" reading at suppressed call
Reason: Internal corollary-framing fix — the proof's content at the suppressed branch is fixed (single-tuple-scope is established from pre-call R0a, which holds vacuously of the call's success/failure). The corollary's framing should accurately describe what the proof establishes; this is a wording-level alignment between the corollary's claim and its proof's content.
