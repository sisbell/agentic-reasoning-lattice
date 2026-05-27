# Channel Assignment — ASN-0099 review-5

**Date:** 2026-05-26 17:20

## Issue 1: F9's multi-step extension conflates pure K.μ sequences with mixed sequences
Reason: Pure derivation cleanup — splits the multi-step claim using F9, F11, and LP13 already cited in the ASN. No external knowledge needed; the distinction is structural.

## Issue 2: Determinism and survivability for filtered and scoped forms are never stated
Reason: Mechanical extension of F8/F9 to `findlinks_filtered` and `findlinks_scoped` by the same comprehension-predicate reasoning. Internal to the ASN's existing formal apparatus.

## Issue 3: F11's derivation double-counts LP13 + L6 and LP3★
Reason: Internal derivation hygiene — pick one citation path from ASN-0098/0043 already referenced. No external knowledge needed; the choice is editorial within the proof structure.

## Issue 4: Worked example does not exercise F10 (ordering) or F14 (scope)
Reason: Extending the worked instance with a second link from a different home document and a scoped/filtered query is determined entirely by the ASN's own definitions (F10's T1-sort, F14's intersection). No external grounding needed.

## Issue 5: Empty-endset boundary case not discussed
Reason: The reviewer takes L3 (ASN-0043) as established that non-type endsets may be empty; the fix is to surface the mechanical consequence for the slot existential in `matches` and for filtered queries. Derivable from the predicate's form once L3's permission is accepted.

## Issue 6: Effect-clause exhaustivity is load-bearing but rests on an unwritten convention
Reason: All three options the reviewer offers (amend ASN-0047, flag the dependency in F9, leave a tracking note) are editorial actions internal to this spec family. The convention's content — that K.μ⁺/K.μ⁻ don't touch L — is already argued via the operation enumeration in the ASN.
