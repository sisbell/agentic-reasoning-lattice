# Channel Assignment — ASN-0099 review-76

**Date:** 2026-06-04 14:38

## Issue 1: A1/A1a and the "Arrangement Independence" intro triple-state the same fact
Reason: Pure restatement-removal — A1a is retained, A1's uniqueness summary and the intro sentence are deleted, and F9's citation is re-pointed to A1a. All of this is internal bookkeeping over the ASN's own lemma structure; no design intent or implementation evidence needed.

## Issue 2: Defensive and motivational prose in the two-phase factoring
Reason: Deleting API-ergonomics and motivational prose that restates facts already carried by the undefined-on-`d ∉ dom(Σ.M)` clause, K.μ-family frames, and L12. The stability distinction is already used at F9/F11 internally; the fix is a trim, fully derivable from the ASN.

## Issue 3: F4 repeats per-witness L3 caveats already covered by the global realizability claim
Reason: The L3 endset-shape admissibility is already stated once in the Realizability paragraph; stripping the per-witness repetitions is mechanical deduplication using the ASN's own L3 references. No external channel needed.

## Issue 4: Worked-example narration justifies example construction
Reason: Deleting meta-prose about why the example is arranged as it is; Query 6 already exhibits the K.λ growth case directly. Purely a narration trim internal to the ASN.

## Issue 5: "Local Atomicity" section restates foundation + F2
Reason: Compressing a section that restates SequentialTransitionAxiom (ASN-0093) and re-derives F2 completeness. Both are already established in the ASN; the fix is internal compression with no need for design intent or code evidence.
