# Channel Assignment — ASN-0098 review-48

**Date:** 2026-06-02 15:53

## Issue 1: T4-validity of `F`-members is justified by a lemma that does not cover the unregistered documents `F` explicitly includes
Reason: The fix swaps a chain-lemma citation for a direct structural T4 check on the form `[d, 0, s, k]`; the review itself spells out the four-clause argument, and the T4 clauses live in ASN-0034, a foundation the ASN already cites. No design intent or implementation evidence is required.

## Issue 2: `F`'s informal introduction names its downstream consumer instead of advancing the definition
Reason: Pure prose restructuring — fold the zero-extension exclusion intuition into the formal definition paragraph and drop the use-site preview. Entirely internal to the ASN.

## Issue 3: LP6, LP7, LP14 triplicate one frame-template
Reason: The three paragraphs are the same LP4-based one-step argument at K.α/K.λ/K.ρ; collapsing them into one template plus a labeled instance list is internal editing with no new claim.
