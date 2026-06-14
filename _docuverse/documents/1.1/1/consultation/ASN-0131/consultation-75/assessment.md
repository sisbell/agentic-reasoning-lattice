# Channel Assignment — ASN-0131 review-75

**Date:** 2026-06-14 12:40

## Issue 1: Defensive higher-arity-retraction digression re-derives a definitional fact for a non-arising case
Reason: Internal — the redundancy is established from content already in the note: ASN-0086's `L_Θ` is defined as the arity-3 type-Θ slice (cited), and "at every arity" follows directly from non-retraction emissions not being type Θ, which the note already states. No design intent or implementation evidence is needed to drop a sentence the note's own argument never invokes.

## Issue 2: Use-site inventory of imported ASN-0086 facts duplicates the in-proof citations
Reason: Internal — all three ASN-0086 facts (unit-depth to-set, R0a/FlatLinkDomain, R-Scope/SingleTupleScope) are already re-stated and re-cited at their points of use within the note; removing the upfront preview is a purely editorial deduplication requiring no external channel.

## Issue 3: "Computable object" over-states what is established; finiteness holds but computability needs a decidable `W`
Reason: The faithful resolution is to constrain `W` to the operation's actual input form rather than arbitrarily picking between the reviewer's two options; whether RETRIEVEENDSETS's region argument is a contiguous span (finitely presented as start + width, hence decidable) is a fact about the FEBE operation's signature — implementation evidence, Gregory.
Gregory question: What form does the region argument of RETRIEVEENDSETS take in udanax-green — a single contiguous span of V-positions (a vspan, presented as a start and width), or an arbitrary set of V-positions?
