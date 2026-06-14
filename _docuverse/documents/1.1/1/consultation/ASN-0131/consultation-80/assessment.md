# Channel Assignment — ASN-0131 review-80

**Date:** 2026-06-14 14:21

## Issue 1: Triple arity-emphasis in RE-ADDR is defensive padding
Reason: Pure prose-redundancy fix — state the addressability fact once and drop the repeated arity restatements (or confine the arity remark to RE-RET's backward direction). Where arity-independence is actually invoked is already settled in the note; no design intent or implementation evidence bears on it.

## Issue 2: Explanatory aside around `addressable` advances no claim
Reason: Pure prose-trim to the kernel sentence "`addressable` depends on `Σ.L` alone," which the note already establishes. The transition-level/state-level contrast is a relocation/deletion decision internal to the document.

## Issue 3: RE-DEF hard-codes whole-endset surfacing, yet the "touching-spans-only reading" it is repeatedly compared against is never defined
Reason: A formal-consistency fix that deliberately does *not* resolve OQ1 (the design-intent question of which reading is faithful) — both required options keep OQ1 open. The touching-spans-only reading is already given a concrete return value in the worked example (`{(a₂, δ(2, #a₂))}`), so writing its formula, or re-marking RE-DEF's return clause provisional, is derivable from the note's own content.

## Issue 4: The `Σ.L`-evolution bridge inclusion is load-bearing but asserted in two sentences
Reason: A proof-gap closure reconciling two already-formalized state models (ASN-0086's `(C,M,L)` vs ASN-0047's `(C,L,E,M,R)`); the reviewer's own resolution path reroutes the needed facts through ASN-0093's model-agnostic link sub-allocator discipline (DisjointSubAllocatorChains, ChainPrefixExtension), all in-corpus. It is a formal step over existing formalizations, not a question of design intent or implementation behavior.
