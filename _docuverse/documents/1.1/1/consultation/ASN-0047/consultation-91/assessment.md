# Channel Assignment — ASN-0047 review-91

**Date:** 2026-05-17 21:33

## Issue 1: D-CTG★/D-MIN★ strengthening abandons link-subspace exemption without justification
Reason: The strengthening conflicts with Nelson's explicit tombstoning design (LM 4/9), so we need Nelson's view on whether uniform contiguity is admissible or whether the exemption is design-critical. We also need Gregory to confirm how link withdrawal actually behaves in the implementation — whether it preserves arrangement slots (tombstoning) or truncates the index.
Nelson question: Is the link-subspace contiguity exemption (LM 4/9 tombstoning) a load-bearing design requirement, or could a system that withdraws interior links by truncating the suffix still satisfy the design intent?
Gregory question: When `dounlinkdoc` or the equivalent link-withdrawal path executes in udanax-green, does the link's V-position in the document arrangement persist as a tombstone, or is the arrangement contracted? What does the spanfilade look like after withdrawal at an interior link position?

## Issue 2: S7d implicit weakening for ghost-base versioning
Reason: The ghost-base case relaxes a foundation invariant; we need Nelson on whether versioning from an uninstantiated base was intended as a design feature, and Gregory on whether `docreatenewversion` actually accepts ghost operands or enforces base membership.
Nelson question: Was version creation intended to require the version base to exist as an allocated document, or is versioning from a "ghost" tumbler (structurally valid but never instantiated) part of the design — e.g., for prismatic-document ancestry indication where the addressed ancestor need not exist?
Gregory question: In `docreatenewversion` (do1.c), does the implementation perform a lookup or membership check on the version-base tumbler `t` before calling `makehint(DOCUMENT, DOCUMENT, depth=1)`, or does it operate purely on the tumbler structure without verifying that `t` was previously allocated as a document entity?

## Issue 3: Anti-bloat in K.δ Path notation and sequentiality footnote
Reason: Pure editorial cleanup — the Path-naming and sequentiality footnote are reviser drift that can be collapsed from material already in the ASN. The case structure of the freshness obligation and the concurrency concern can be re-expressed without consulting external channels.

## Issue 4: Anti-bloat in L3 empty-F/G semantics
Reason: The design decision is already made and supported by citations present in the prose being reduced; the fix is to condense the defense without changing the substance.

## Issue 5: S8 extended-state preservation hand-waved via "projection"
Reason: This is a proof-rigor issue derivable from material already in the ASN — either construct the projection adaptation from ASN-0036's S8 statement, or state an extended-state S8★ per-subspace. No external evidence is required.

## Issue 6: K.μ~ link-subspace fixity proof requires reader assembly
Reason: Pure expository fix — spell out the bijection + subspace-preservation + K.μ⁺ amendment chain that the ASN already implicitly relies on. All ingredients are present in the ASN.

## Issue 7: NodeUniqueAllocation as bare freshness axiom
Reason: The protocol behind node allocation is jointly specified by Nelson's hierarchical baptism design and Gregory's granfilade implementation; we need both to determine whether NodeUniqueAllocation can be replaced with a minimal protocol description or must be deferred to a node-allocation ASN.
Nelson question: What is the design-level discipline for node baptism — is there a single authority that issues node addresses, and what uniqueness guarantee does that authority provide? Should this guarantee be specified at the docuverse model level or treated as out-of-scope?
Gregory question: In the udanax-green node-allocation path (single global granfilade with query-and-increment dispatch), what mechanism enforces freshness of node addresses? Is there a registry of allocated nodes, or is uniqueness enforced by the dispatch protocol itself?

## Issue 8: K.δ Path 2 sequentiality assumption smuggled via footnote
Reason: The sequential-semantics assumption is a model-level decision that needs design-intent grounding (Nelson) and implementation context (Gregory) to determine whether it should be stated as a model axiom or extended to handle concurrency.
Nelson question: Did the docuverse design assume sequentially-executed, atomically-committed operations at the protocol layer, or was concurrent operation contemplated — and if so, what serialization or transactional discipline did the design assume?
Gregory question: Does the udanax-green back-end serialize entity-allocation events (K.δ-equivalent operations) at a single point — e.g., a global lock around the granfilade query-and-increment — or do multiple protocol commands process concurrently with a finer-grained discipline?

## Issue 9: D-CTG-depth / D-SEQ★ chain — the inner-positions-fixed step requires a small case-split note
Reason: Pure mathematical clarification — add one sentence handling the m = 2 vacuous case and noting the m = 3 terminal-coincidence in the u_M construction. No external input needed.
