# Channel Assignment — ASN-0040 review-52

**Date:** 2026-05-28 21:48

## Issue 1: B1 is stated over all (p, d), forcing proof of namespaces baptism can never produce
Reason: Pure formal restructuring derivable from the ASN's own content — every consumer (hwm, B2, Bop freshness, B8, B9) already invokes B1 only for B6-valid pairs, and Bop's precondition guarantees baptism targets are B6-valid, so scoping the invariant and deleting sub-cases B/C requires no external intent or implementation evidence.

## Issue 2: Non-circularity disclaimer is meta-prose justifying proof ordering
Reason: Internal consequence of the Issue 1 fix — removing the B10 invocation in sub-case B eliminates the need for the disclaimer; nothing about design intent or implementation is at stake.

## Issue 3: B6 Formal Contract Postcondition (b) restates the entire necessity proof
Reason: Editorial deduplication derivable from the ASN alone — the necessity proof body already carries the full case analysis, so the contract slot can collapse to the bare claim without consulting any channel.

## Issue 4: Atomicity section opens with axiom rationale, not axiom content
Reason: Editorial restructuring derivable from the ASN alone — B4's statement and the race illustration are both already present in the document; deciding how to present them needs no design-intent or implementation input.
