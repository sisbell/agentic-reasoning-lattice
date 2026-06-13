# Channel Assignment — ASN-0123 review-3

**Date:** 2026-06-12 23:04

## Issue 1: The cross-owner identity clause's "three constraints suffice" claim is false — V9's Severance theorem provably needs O5's maximality
Reason: The fix is internal — it is a proof-bookkeeping correction that aligns the contract prose with hypotheses already present in the ASN. V9 already invokes O5's maximality, and V-WF already establishes allocation-by-the-forker (`draws from the forker's account document sub-allocator`); the repair is to promote `allocated_by(π', v)` to an explicit operative hypothesis (or list maximality as a fourth constraint) and drop/correct the "three constraints suffice" sentence. No design intent (the severance semantics are settled) and no implementation evidence (the operation itself is sound per V-WF) are needed.
