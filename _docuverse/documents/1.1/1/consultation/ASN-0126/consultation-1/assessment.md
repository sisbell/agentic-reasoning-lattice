# Channel Assignment — ASN-0126 review-1

**Date:** 2026-06-08 20:36

## Issue 1: "Cardinality" of F and G is never defined on endsets
Reason: Reconciling `|F|`/`|G|` with ASN-0043's endset/coverage formalism is mechanical, but choosing whether "single source" means one *address* (singleton coverage) or one *span* (which may cover a subtree) is a design-intent decision that fixes the whole vocabulary. Nelson resolves the intended meaning.
Nelson question: Is a typed relation's source meant to denote a single address, or may a single source span legitimately cover a range/subtree of addresses?

## Issue 2: Multi's "finite set of addresses" can be an infinite coverage
Reason: Once Issue 1 fixes the cardinality measure (coverage vs. span count), Multi's finiteness condition follows mechanically from ASN-0043's endset and PrefixSpanCoverage definitions. No external channel needed.

## Issue 3: t_F / t_G domain checks contradict P5 (Sh-confStateIndependence)
Reason: This is an internal contradiction between the state-indexed domains `A_doc/A_rel/A` (ASN-0086) and P5's state-independence claim; resolving it (drop the check or retract P5) is derivable from the ASN's own definitions.

## Issue 4: Domain restriction to A_doc/A_rel/A contradicts L4 and L9
Reason: Deciding whether to narrow L4/L9 turns on whether typed relations are intended to permit ghost (not-yet-stored) references, and on whether the implementation actually allows links to dangling addresses. Both intent and evidence are needed to justify keeping or restricting ghost permission.
Nelson question: Are typed relations intended to be allowed to reference addresses where no content yet exists (ghost references), or must every endset address resolve to stored content?
Gregory question: Does udanax-green permit a link's endset to reference addresses that have no stored content, and does it enforce any residence check at link creation?

## Issue 5: P4 asserts a constraint on → with no enforcement mechanism
Reason: ASN-0086's `→ ≡ K.σ ∪ K.α ∪ K.λ` and K.λ's L3 precondition are already in scope; gating K.λ by Sh-conf or labeling P4 definitional is derivable from the cited transition relation.

## Issue 6: P1 (RegistryInvariance) is asserted, not derived; Σ is silently extended
Reason: Extending the state tuple with `registry` and deriving P1 from per-step frame conditions follows directly from ASN-0043/0086's definitions of Σ and the transition relation; no external channel needed.

## Issue 7: The three shapes do not partition tuples
Reason: The nesting of conformance conditions (Unary ⊂ Binary ⊂ Multi) and the registrations-vs-tuples distinction are internal logical observations about the note's own predicates.

## Issue 8: No concrete worked example
Reason: Adding concrete tumbler instances exercising Unary/Binary/Multi and checking P4/P5 uses only the ASN's own definitions plus the tumbler notation from ASN-0043; derivable internally.
