# Channel Assignment — ASN-0047 review-182

**Date:** 2026-05-31 23:06

## Issue 1: TrackedEmission is a load-bearing per-state invariant but is omitted from the maintained invariant set
Reason: Internal fix — the choice is whether to fold TrackedEmission into the master induction conjunction/matrix or cite its standalone preservation sketch at the FrontierEquivalence consumption site. Both options are editorial reorganizations of material already present in the ASN; no design intent or implementation evidence is needed.

## Issue 2: K.σ-subsumption stated twice in different sections
Reason: Internal fix — pure deduplication, keeping the statement at the K.δ definition and reducing the Typing-note bullet to a pointer. No external channel needed.

## Issue 3: Defensive meta-prose explaining why a lemma does not apply / why a guard is not a conclusion
Reason: Internal fix — replace negative meta-prose with the positive substantive claims (T3 distinctness; caller-checked guard) already established in the ASN. No external channel needed.

## Issue 4: Three composite-boundary properties each defer to the same downstream "Class (b)" location
Reason: Internal fix — consolidate each of P4★/P4a/P7a to a single statement site with one forward pointer; all content already exists in the ASN. No external channel needed.
