# Channel Assignment — ASN-0134 review-19

**Date:** 2026-06-14 01:53

## Issue 1: A1 establishes a category of single-index reads that no contract clause covers, and attributes their soundness to a clause whose body excludes them
Reason: Internal reconciliation only. Every ingredient the fix needs is already in the ASN — A1's three-way read classification, the single-bounded-access property of `age`/single-home `stale` (already established and even Gregory-confirmed via `findpreviousisagr` within A1), and the soundness mechanism (clause 1/A0 atomicity + one-access ⟹ one committed index). The reviewer concedes the substantive claim is correct; only the clause citations (clause 4, V0, M1(d)) must be made consistent with A1's own taxonomy, which is a matter of the note's internal cross-references, not design intent or new implementation evidence.
