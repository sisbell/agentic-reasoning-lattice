# Channel Assignment — ASN-0126 review-8

**Date:** 2026-06-08 21:52

## Issue 1: Registration-check decidability rests on an unstated finiteness condition
Reason: Internal — the fix adds `|Σ_init.registry| < ∞` to C0 (paralleling L-fin) and derives decidability of precondition (i) from finiteness plus ASN-0086's CoverageEqualityDecidable, both already available in the ASN's own content and its declared dependency. No design intent or implementation evidence is at stake.

## Issue 2: The worked illustration never exercises the non-trivial wp case
Reason: Internal — the note already supplies all machinery (Binary R with non-unit G, fresh-address coverage, the three inherited wp conjuncts). Constructing the born-nullified witness is a mechanical instantiation of the note's own definitions; no external authority is needed.

## Issue 3: Opening universal claim overclaims relative to the framework's scope
Reason: Internal — the note's own later scoping clause ("an app needing multi-source relations can interact with the link store directly") supplies the correction; restricting "every typed relation" to "every registered relation the framework gates under `→_sh`" is a self-consistency edit requiring neither design intent nor implementation evidence.
