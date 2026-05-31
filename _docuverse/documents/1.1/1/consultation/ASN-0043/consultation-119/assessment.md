# Channel Assignment — ASN-0043 review-119

**Date:** 2026-05-30 18:10

## Issue 1: L11a's embedding of link chains into the single tree 𝒯 is asserted in one sentence, but it is load-bearing for GlobalUniqueness's single-system precondition
Reason: The fix must show the independently-existential L1c chains are genuine events of one allocator tree — in particular that same-document link chains share the single `inc(home, 2)` spawn. Whether they do is an implementation fact about how link allocation is structured per document; Gregory can confirm there is one coherent per-document link allocator. Nelson is not needed — this is structural coordination, not design intent.
Gregory question: Does `docreatelink`/`findisatoinsertmolecule` allocate every link homed in a given document through a single shared allocator (one I-stream/enfilade), so all such links descend from one `inc(home, 2)` child-spawn and diverge only at sibling-ordinal advances?

## Issue 2: L0b carries a downstream-consumer inventory and re-derives a fact L1c already proves
Reason: Purely an internal restructuring — collapse the duplicated T4-validity derivation to a single site with a bare cross-citation and delete the consumer-inventory/placement sentence. Both the redundancy and the fix are fully visible within the ASN's own text.
