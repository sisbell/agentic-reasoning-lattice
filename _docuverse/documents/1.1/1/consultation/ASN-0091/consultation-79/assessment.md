# Channel Assignment — ASN-0091 review-79

**Date:** 2026-06-04 03:45

## Issue 1: RA-adm discharge silently assumes Σ is reachable
Reason: The fix is internal — RA-adm and the realisation theorem can be scoped to reachable states (the foundation already operates from Σ₀ via ExtendedReachableStateInvariants), or a direct transfer argument can be assembled from machinery already present (clause (i)'s discharge already shows S8a/S8-depth/D-CTG★/D-MIN★ transfer verbatim via RA-dom).

## Issue 2: RE-trans (iii) skips the step establishing a ∈ dom(C)
Reason: The fix is internal — the ASN already cites CL-OWN (link-subspace images satisfy origin(M(d)(v)) = d_view) and the transclusion premise origin(a) ≠ d_view, which together exclude the link case and force a ∈ dom(C) before C2 applies.

## Issue 3: Composite-boundary properties not addressed at the abstract level
Reason: P4★ and P4a are derivable internally (one line each from RE-ran/RE-R, as already shown in Worked Example 1), but P7a is never stated in the ASN, so its definition and what frame-fixity must preserve cannot be derived from the ASN alone — this is a formal foundation property cataloged in the knowledge base synthesis.
Gregory question: What does the composite-boundary invariant P7a require of a post-state Σ', and is it discharged solely by frame-fixity of Σ.C and Σ.R?

## Issue 4: ChainDisjointAdjacency lemma is buried inline yet load-bearing across sections
Reason: The fix is internal — it is a purely organizational change promoting an already-proven inline lemma to a named claims slot; no design intent or implementation evidence is required.
