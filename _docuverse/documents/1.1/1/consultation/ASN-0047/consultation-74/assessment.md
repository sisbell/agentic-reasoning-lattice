# Channel Assignment — ASN-0047 review-74

**Date:** 2026-05-17 05:00

## Issue 1: K.μ⁺_L's m_L parameter freedom at the first-link case
Reason: Resolving (a) vs (b) requires checking whether Nelson's design pins link-subspace depth and whether Gregory's implementation treats `2.1` as a fixed convention or a parameter — paralleling the SubspaceConventionAxiom evidence pattern.
Nelson question: Does Literary Machines pin the link-subspace depth (so that the first link is always `[N.0.U.0.D.0.2.1]` with depth 2), or is the depth a design parameter left to the implementer?
Gregory question: Is `findnextlinkvsa`'s hardcoded `2.1` first link VSA structurally fixed by the data format (like the LINKATOM=2 constants in `xanadu.h:144–146`), or is it a configurable convention?

## Issue 2: Link-subspace analog of S8 correspondence runs not explicit
Reason: Whether link-subspace correspondence runs are a needed downstream structure requires both design intent (does Nelson use link-batch operations or link-subspace span queries?) and implementation evidence (does udanax-green expose correspondence-run structure for the link subspace?).
Nelson question: Does the design require batch or range operations over the link subspace (e.g., "all links of document d in arrangement order") that would need correspondence-run structure analogous to the content subspace, or are link-subspace operations always per-individual-link?
Gregory question: Does udanax-green expose any link-subspace operation (followlink, endsetqueries, or similar) that traverses a contiguous run of link V-positions as a structural unit, analogous to content-subspace span operations?

## Issue 3: K.δ case (ii) precondition presentation complexity
Reason: Purely presentational — adding a summary table consolidating routing information already present in the ASN. Derivable from the ASN's own content.

## Issue 4: K.μ~ contract's subspace-preservation redundancy
Reason: Structural presentation decision about a derivable property within the ASN's own logical framework. Derivable from the ASN's own content.

## Issue 5: NodeLineage label inconsistency
Reason: Formal classification (axiom vs. derived invariant) is determined by the ASN's own logical structure — whether the K.δ case (i) precondition is the operative discharge or NodeLineage stands as an independent premise. Derivable from the ASN's own content.
