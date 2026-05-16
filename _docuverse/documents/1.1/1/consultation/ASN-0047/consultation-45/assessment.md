# Channel Assignment — ASN-0047 review-45

**Date:** 2026-05-15 18:14

```
## Issue 1: Node addresses claimed to be single-component
Reason: Whether nodes are single-component or can be multi-component is a design-intent question (what Nelson meant by "node") and an evidence question (what udanax-green enforces). The ASN's own content does not resolve T4c's admission of multi-component zeros=0 tumblers.
Nelson question: In Nelson's tumbler design, is a node identity a single top-level component, or may a node address carry multiple components at the top level?
Gregory question: Does udanax-green allocate node addresses as single-component identifiers, and does any code path enforce or assume single-component node addresses?
```

```
## Issue 2: TA5 cross-reference error in K.δ descent case
Reason: This is a pure citation/formalism fix against ASN-0034's TA5 clauses, derivable from the ASN's own foundation references without external input.
```

```
## Issue 3: "origin(t) = parent(e)" overloads origin notation
Reason: This is an internal notational disambiguation — either introduce a distinct entity-level symbol or extend parent terminology. Fully derivable from the ASN's own definitions.
```

```
## Issue 4: T7 misapplied in K.μ⁺_L verification
Reason: Pure citation correction (T7 → T3/extensionality), derivable from ASN-0034 without external channels.
```

```
## Issue 5: K.α lacks formal inc-conformance precondition
Reason: This is a parallelism fix with K.λ's existing precondition; the formal content already exists in the ASN and ASN-0034. Internal restructuring only.
```

```
## Issue 6: K.δ identity criterion for nodes is incompletely formalized
Reason: The abstract specification needs to state the contract the external node allocator satisfies. Nelson's design intent and Gregory's implementation both bear on what that contract should be.
Nelson question: What guarantees does Nelson's design require of the node-identifier namespace — is global uniqueness assumed as a property of the namespace, or established by some protocol?
Gregory question: In udanax-green, how is node-address uniqueness guaranteed across nodes, and what is the contract the implementation assumes about node identifiers?
```

```
## Issue 7: K.μ~ link-subspace identity is both precondition and derived consequence
Reason: This is a structural/presentation choice about whether to state pointwise-identity as a precondition or derive it. Fully internal to the ASN's formal architecture.
```

```
## Issue 8: ReachableStateInvariants self-reference suggests dual-presentation drift
Reason: Pure restructuring/presentation issue — choose between layered presentation with explicit markers or flat five-component presentation. Internal to the ASN.
```

```
## Issue 9: K.δ k = 1 descent semantics undeveloped
Reason: What a k=1 descent under a document corresponds to semantically (version, sub-document, or out-of-scope) is a design-intent question for Nelson and an implementation question for Gregory.
Nelson question: In Nelson's tumbler design, what entity does a tumbler of form [N, 0, U, 0, D, k] (a document with appended component but no new zero separator) represent — a version, a sub-document, or something else?
Gregory question: Does udanax-green allocate entity addresses of the form [N, 0, U, 0, D, k] (document address extended by one element-field component, zeros still = 2), and if so, what entity kind does this represent?
```

```
## Issue 10: K.μ⁻ admissibility tied to D-SEQ★ but D-SEQ★ is derived later
Reason: Pure ordering/restructuring issue — move D-SEQ★ derivation earlier, mark the forward reference explicitly, or restate the precondition self-containedly. All derivable internally.
```
