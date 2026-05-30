# Channel Assignment — ASN-0084 review-52

**Date:** 2026-05-30 11:16

## Issue 1: Necessity sketch for R-PRE(iv) computes w_β via an identity that its own hypothesis invalidates
Reason: Derivable from the ASN's own definitions plus D-SEQ (ASN-0036). The reviewer's own observation — under D-SEQ V_S(d) is contiguous {[1,1],…,[1,N]}, so cardinality widths are always well-defined and source references stay in V_S(d) — settles whether R-PRE(iv) is redundant for well-definedness; the fix is to confront that internally and either exhibit a genuine failure or recharacterize what R-PRE(iv) adds beyond D-SEQ + a c_{n−1} bound. No design intent or implementation evidence needed.

## Issue 2: CS3 well-typedness sketch repeats the same width conflation
Reason: Internal. CS3's necessity must be argued from the stated cardinality definition and the ambiguity of "the subspace S" in R-PRE(iv) when cuts span subspaces (plus the R-FRAME-P/S(a) inertness conflict) — all present in the ASN. No external channel required.

## Issue 3: Δ / R-DISP machinery is introduced and then declared non-operational
Reason: Internal structural decision. The ASN itself states Phase 3 runs on π and R-COMM alone and that Δ is consumed only as an equality predicate; whether to connect R-DISP to a postcondition or demote it to a remark is fully determined by the ASN's own proof dependencies.

## Issue 4: Canonical-decomposition apparatus is not load-bearing for any postcondition
Reason: Internal. R-SP's "Q is non-trivial" paragraph and S8 (ASN-0036, which already exports maximal-run uniqueness) determine that no postcondition consumes merge-process confluence; the decision to remove (a)–(d)/helper lemma and cite S8 in the worked examples is derivable from the ASN and its foundation alone.

## Issue 5: Meta-prose — dependency-audit use-site inventory in the body
Reason: Purely editorial. Removing the use-site inventory and relocating the ASN-0053 removal to the `depends:` set requires no external information.

## Issue 6: Meta-prose — "Q is non-trivial" and necessity-sketch framing in R-SP
Reason: Editorial restructuring internal to the ASN — reduce R-SP to its sufficiency proof and relocate any correct necessity result. No design intent or implementation evidence bears on the cut.
