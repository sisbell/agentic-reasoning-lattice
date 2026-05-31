# Channel Assignment — ASN-0047 review-150

**Date:** 2026-05-31 15:51

## Issue 1: Step (B) of the K.μ~ dependency chain names its goal as "realising S3★(Σ')" — but S3★(Σ') is an admissibility *input*, making the argument read as circular
Reason: The fix is purely a restructuring of the ASN's own proof exposition — retitling Step (B) and restating that S3★(Σ') holds by the admissibility filter. All propositions involved are already present in the ASN; no external evidence or design intent is required.

## Issue 2: Asymmetric, unjustified permanence of link-subspace depth versus content-subspace depth
Reason: Choosing among the three fixes (justify the asymmetry, weaken to per-interval fixity, or add a content analog) turns on whether link-depth permanence is a genuine design commitment (Nelson) and whether the implementation actually fixes link depth across empty intervals (Gregory); neither is settled by the ASN's own invariants.
Nelson question: Was a document's link-subspace V-position depth intended to be fixed permanently once chosen, or only while the link subspace is non-empty — and if permanent, why does the content subspace carry no analogous cross-state depth commitment?
Gregory question: Does udanax-green fix a per-document link V-position depth at first link insertion and retain that depth across states where the link subspace is emptied and later repopulated, and is content-subspace depth treated the same or differently?

## Issue 3: Axiom prose explains *why the axiom is needed* rather than *what it says*
Reason: The fix is editorial — trim motivation/scope essays from the axiom statements (LinkVPositionDepthAxiom, NodeUniqueAllocation, NodeRegistryBootstrap), leaving the normative claim plus minimal scoping. No external input needed.

## Issue 4: Definition enumerates downstream consumers (use-site inventory)
Reason: The fix is internal — strip the "is the family member cited in X below" clauses from the sub-allocator definitions, retaining only structure (anchor, first emission, emission rule, output level). Derivable from the ASN alone.

## Issue 5: "Temporal scoping of J0" paragraph duplicates the composite-boundary matrix and re-derives by analogy
Reason: The fix is a deduplication entirely within the ASN — state J0's composite-boundary scoping once in the Class (b) matrix and delete or collapse the redundant paragraph. No channels required.

## Issue 6: Repeated forward deferrals for L / K.λ / K.μ⁺_L in *The state model*
Reason: The fix is editorial consolidation of the ASN's own forward-reference scaffolding into a single staging statement. Derivable from the ASN alone.

## Issue 7: K.μ⁺ precondition cites ASN-0036 D-CTG/D-MIN but describes the strengthened per-subspace form
Reason: The fix is a citation correction the ASN can make itself — it already defines D-CTG★/D-MIN★ as the local per-subspace strengthening, so the elementary-site citation can either point to the local starred forms or drop the "each subspace" wording. No external input needed.
