# Channel Assignment — ASN-0043 review-51

**Date:** 2026-05-13 10:21

## Issue 1: L8 prose says "addresses" but formal definition uses spans
Reason: The choice between span-set equality and coverage equality is a design decision that needs Nelson's intent and Gregory's implementation evidence. Nelson's quoted text is ambiguous between the two readings; Gregory can tell us what the actual type-matching code does.
Nelson question: When the design says type matching "considers the type's address," does it mean two type endsets match iff they are identical as sets of spans, or iff they cover the same addresses (allowing different span decompositions)?
Gregory question: In the implementation's link-finding/intersection code (`sporglset2linksetinrange`, `intersectlinksets`), does type endset matching compare exact span structures, or is it computed over coverage (set of addresses)?

## Issue 2: L9 witness `d'` is not anchored to a T10a allocation event
Reason: The fix is derivable from ASN-0034 (T10a allocator chain construction) and ASN-0036 (S7d). Either exhibit the explicit allocator chain or parametrize on existing `d ∈ dom(Σ.M)` — both options use only material already in the foundation stack.

## Issue 3: L0 cites a chain that does not establish T4-validity for content addresses
Reason: The fix is internal — use S7b's well-defined T4b projections as the route to T4-validity for content addresses, drawing on ASN-0036 and ASN-0034 (T4b) as already cited.

## Issue 4: L9 allocator chain case split misses the middle case
Reason: Pure proof-case reorganization derivable from L1c and T10a structure. The correct discriminator (per-`d'` rather than global) is internal to the proof's own machinery.

## Issue 5: L9 and L11b verify only a subset of conformance invariants
Reason: Scope clarification about what "conforming" means — a choice between widening preconditions and stating the minimum required set. Derivable from the ASN's relationship to ASN-0036's invariant catalog.

## Issue 6: L11b construction of fresh `a'` is informal
Reason: The construction can be made precise using L-fin, T0(a) (unbounded sibling stream), and GlobalUniqueness (ASN-0034) — all already cited in the proof. No external evidence required.

## Issue 7: `dom(Σ.M)` is used as if defined but ASN-0036 does not introduce it
Reason: Notation gap — add an inline definition `dom(Σ.M) = {d ∈ T : Σ.M(d) is defined}`. Pure internal cleanup.
