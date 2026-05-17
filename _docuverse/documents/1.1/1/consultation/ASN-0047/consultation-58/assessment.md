# Channel Assignment — ASN-0047 review-58

**Date:** 2026-05-16 20:51

## Issue 1: S9 restatement contradicts admitted composites
Reason: The fix is internal — the foundation S9 statement is already established in ASN-0036, and the choice between (a) using foundation S9 verbatim or (b) scoping the strengthened form to elementary transitions is a logical reorganization derivable from the ASN's own content.

## Issue 2: ShiftPreservation cited for the wrong property
Reason: The review itself identifies the correct foundation citations (OrdShiftHom (c) or OrdAddS8a). The fix is a citation replacement against existing foundation lemmas already available in ASN-0036, derivable from the ASN's own notation.

## Issue 3: NodeLineage missing from per-state invariants theorem
Reason: NodeLineage is already defined as an axiom in this ASN with its inductive discharge already specified (Σ₀ by reflexivity, K.δ case (i) by precondition). Adding it to the conjunction and verifying the inductive step is purely internal bookkeeping.

## Issue 4: `fields(a)` notation reinvents foundation E(a)
Reason: The fix is a notational reconciliation against T4b in ASN-0034. The choice between using `E(a)` directly or stating `fields(a) := E(a)` as a local abbreviation is internal — the foundation notation is already established and accessible.

## Issue 5: SubAllocatorAxiom needs explicit reconciliation with L1c
Reason: L1c (LinkAllocatorConformance in ASN-0043) requires a T10a-conforming inc-chain to every link address. Whether the intermediate addresses `[d.0.1]`, `[d.0.2]` should count as "chain steps" without being allocated is a design-intent question for Nelson, and how the implementation actually realises the chain (with or without materializing intermediates) is an evidence question for Gregory.
Nelson question: Does the T10a-conformance requirement for link allocators (L1c) permit "virtual" intermediate addresses in the inc-chain that are never themselves allocated, or must every chain-step address be a live allocation?
Gregory question: In udanax-green's link allocation path (`findnextlinkvsa`/`docreatelink`), are the addresses `[d.0.1]` and `[d.0.2]` ever materialized as granfilade entries or atomtype-prefix bridges, or does the implementation produce `[d.0.s_L.1] = [d.0.2.1]` directly without the structural intermediates appearing in any allocator's domain?

## Issue 6: K.μ~ status oscillates between "distinguished composite" and "transition kind"
Reason: The fix is a presentational consistency choice — either treat K.μ~ uniformly as a named composite (like J4) or as an elementary transition with its own contract. Both options are derivable from the ASN's existing decomposition account and the J4 precedent.
