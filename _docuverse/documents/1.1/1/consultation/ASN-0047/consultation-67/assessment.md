# Channel Assignment — ASN-0047 review-67

**Date:** 2026-05-17 01:29

## Issue 1: TA5/T10a conflation in ghost-base versioning Step 3 counterfactual
Reason: The fix is purely internal — K.δ's own ghost-operand discussion already specifies that TA5 supplies determinism and the K.δ precondition supplies freshness, so the counterfactual just needs to be rewritten to match that account. No external context is required.

## Issue 2: SubAllocatorAxiom's operational-vs-structural tension is acknowledged but underspecified
Reason: Resolving this requires understanding whether sub-allocators are conceptually one allocator-with-two-frontiers or two distinct allocators (Nelson, design intent), and how the implementation actually structures the allocator-tracking machinery (Gregory). Both inform whether SubAllocatorAxiom should extend T10a with virtual spawning events or stand outside T10a's Act(s) framework.
Nelson question: At document creation, are a document's content and link sub-allocators conceptually one allocator with two reserved frontiers, or two distinct allocators sharing a document-level root?
Gregory question: When a document is created in udanax-green, does the implementation track the content and link sub-allocators as a single structure with two frontier states, or as two separately-managed allocator records?

## Issue 3: Inconsistency in T10a applicability to ghost operands
Reason: The fix is internal — the ASN already has the conceptual machinery to distinguish "T10a's tumbler universe" (which contains ghosts) from "T10a allocator domains in E" (which do not). It just needs the terminology made explicit and the worked example reconciled with the K.δ definition.

## Issue 4: Convention s_C = 1, s_L = 2 is treated as conventional but is structurally load-bearing
Reason: The choice between baking in the convention versus generalizing depends on whether the design commits to these specific values (Nelson) and whether the implementation treats them as fixed constants or as configurable instantiations (Gregory). Both inform the authorial decision.
Nelson question: Are the subspace assignments s_C = 1 (content/text) and s_L = 2 (link) a fixed structural commitment of the Xanadu design at LM 4/30–4/31, or a chosen instantiation where any pair of distinct positive subspace identifiers would satisfy the design intent?
Gregory question: Are TEXTATOM=1 and LINKATOM=2 in xanadu.h hardcoded in a way that other parts of the protocol depend on these specific values (e.g., sort order, dispatch tables), or are they configurable constants whose specific numerical values are incidental?

## Issue 5: K.μ⁻ effect clause requires non-empty `dom(M(d))` only via precondition narrative
Reason: Internal definitional cleanup — the strict-subset clause's unsatisfiability on empty arrangements is a derivable consequence, and the precondition list just needs restructuring to reflect that. No external context required.

## Issue 6: K.μ~ degenerate cases not consistently handled in elementary-sequence reading
Reason: Internal axiomatic refinement of ValidComposite★ — the zero-step composite case can be made explicit from the ASN's own content. No external context required.

## Issue 7: P4★ "load-bearing" classification at intermediate state in worked example is confusing
Reason: Internal terminology clarification — the "load-bearing" qualifier was misapplied to an incidentally-satisfied intermediate-state check. Fix is editorial.

## Issue 8: ASN-0036's S0 subsumption by P0 — but S0 is per-transition
Reason: Internal logical equivalence exposition — the subsumption argument can be made visible with a short derivation in this ASN's text alone.

## Issue 9: SubspaceAxiom listing omitted
Reason: Internal table organization — the split between s_C/s_L (foundation restatement) and SC-NEQ (this ASN's axiom) can be clarified by editorial reorganization. No external context required.

## Issue 10: K.λ first-link case discharges `ℓ ∉ dom(L) ∪ dom(C)` via SubAllocatorAxiom but the structural producibility chain is left implicit
Reason: Internal cross-referencing — the L1c reconciliation already exhibits the inc-chain witness, just needs to be cross-linked from K.λ's precondition. No external context required.

## Issue 11: NodeUniqueAllocation justification cites "ownership-derived uniqueness" without formal premise
Reason: Internal presentational restructuring — the axiom statement and protocol justification can be separated using content already present in the ASN. No new consultation evidence needed.

## Issue 12: Worked example "node baptism" presents counterfactuals without clear pass/fail criterion
Reason: Internal formal exposition — the rejection model (precondition failure → transition not in the set) can be stated using the ASN's own transition framework. No external context required.

## Issue 13: D-SEQ★ derivation appeals to "infinite-cardinality contradiction" that requires careful S8-fin invocation
Reason: Internal proof exposition cleanup — the contradiction is sound and just needs tighter staging of the three sub-claims (distinctness, membership, finiteness violation). No external context required.

## Issue 14: Frame extension table doesn't cover K.μ⁺_L
Reason: Internal table completion — the frames for K.μ⁺_L and K.λ are stated at their definition sites and just need to be lifted into the central catalogue. No external context required.

## Issue 15: K.μ⁻ admissibility's per-subspace independence requires at least one subspace to contract
Reason: Internal precondition restructuring — the strictness requirement is already implied by the effect clause and just needs to be lifted to a numbered precondition. No external context required.
