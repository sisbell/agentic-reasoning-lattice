# Channel Assignment — ASN-0047 review-46

**Date:** 2026-05-15 19:07

```
## Issue 1: TA5 sub-clause miscitation in K.λ first-link case
Reason: Pure citation correction within ASN-0034's TA5 structure. The correct sub-clause for the appended-position structure is determinable from the foundation definitions already in the ASN.
```

```
## Issue 2: NodeUniqueAllocation not formally introduced as axiom
Reason: The axiom's substantive content (protocol-established node uniqueness) is already established in the ASN through prior consultation citations (Nelson LM 4/19–4/20, Gregory granf2.c:209). Only formal labeling parallel to SC-NEQ is needed.
```

```
## Issue 3: D-SEQ★ derivation hand-waves on inner-1 components
Reason: Pure mathematical derivation from existing definitions (D-CTG★, D-MIN★, S8-depth, S8-fin, S8a). The infinite-cardinality contradiction or per-subspace D-CTG-depth analog can be developed from the ASN's own content.
```

```
## Issue 4: K.δ "descent" terminology conflates k=1 and k=2
Reason: Terminology/structural clarification derivable from TA5's existing zeros-count semantics. The version-vs-descent distinction is already noted in the ASN's version-semantics aside.
```

```
## Issue 5: K.μ⁻ frame in extended state does not explicitly include L
Reason: Frame extension is structural — K.μ⁻ touches only M(d), so L' = L is structurally compelled. The fix is restating the frame in the Amendments section without external evidence.
```

```
## Issue 6: ExtendedReachableStateInvariants theorem missing several invariants
Reason: The missing invariants (L1b, S7a–d, S4, S9, D-SEQ★) are foundation invariants whose preservation is derivable from the operator definitions and existing preservation arguments in the ASN.
```

```
## Issue 7: K.μ⁻ admissibility precondition references D-SEQ★ before its derivation
Reason: Tied to Issue 3 — once D-SEQ★'s derivation is completed, the forward reference becomes self-contained. Alternatively, restating without the named-theorem reference is purely editorial.
```

```
## Issue 8: Treatment of K.μ⁻ removing a per-subspace prefix vs suffix
Reason: Pure derivation from D-MIN★'s post-state requirement. The argument that prefix removal violates D-MIN★ is mechanical from the existing definitions.
```

```
## Issue 9: K.μ~ degenerate case clarification on link-subspace-only arrangements
Reason: Proof-chain clarification derivable from the link-subspace fixity argument and S3★-aux already in the ASN. The chain dom_C = ∅ → dom = dom_L → π = id by fixity is purely structural.
```

```
## Issue 10: K.λ first-link case requires a multi-step inc chain that is not fully derived
Reason: Formalizing the allocator hierarchy under documents — whether content and link allocators are sibling sub-allocators of a parent element-field allocator, or distinct unified mechanisms — requires both design intent (Nelson) and implementation evidence (Gregory) to choose the right model.
Nelson question: Did the design conceive of a document's content and link sub-allocators as siblings under a single element-field allocator (parent), or as independent address-producing mechanisms each operating directly on the document's tumbler prefix?
Gregory question: In udanax-green, how does the document-level allocation machinery structure content-address and link-address production — does the implementation maintain a parent element-field allocator with distinct content and link sub-allocators, or are content and link addresses produced by independent allocators each rooted at the document's prefix?
```
