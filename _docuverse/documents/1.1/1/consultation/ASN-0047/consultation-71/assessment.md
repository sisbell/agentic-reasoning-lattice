# Channel Assignment — ASN-0047 review-71

**Date:** 2026-05-17 03:54

```
## Issue 1: Path 2 coverage list is incomplete relative to the mutual-exclusivity claim
Reason: The mismatch is between the partition claim (path 2 = ¬InEntityAllocatorDomain) and the enumeration (only k=1 ghost-base + downstream k=0). Fix is structural reorganization of the coverage statement using the ASN's own premises.
```

```
## Issue 2: T10a's T2 spawning rule premises are not rigorously discharged for A_v(t)
Reason: The question is what dom_s(parent(A_v(t))) contains when parent and spawnPt both equal t. This is foundation-level formalization of T10a's allocator-domain structure (ASN-0034); resolution requires making the dom_s characterization explicit in this ASN. Gregory could confirm whether udanax-green's allocator tracking gives evidence that a parent document is in its own version sub-allocator's tracked domain.
Gregory question: When udanax-green's docreatenewversion spawns a version chain under document t, does the granfilade machinery treat t itself as a member of the spawning allocator's tracked domain, or is t only the "parent" pointer with its membership tracked elsewhere?
```

```
## Issue 3: InEntityAllocatorDomain's formal definition is imprecise
Reason: "Entity-level allocator" needs explicit enumeration (account's document sub-allocator, version sub-allocator A_v, excluding content/link sub-allocators A_C/A_L) — derivable from the ASN's own allocator taxonomy. Act(·) state argument is also a local notation fix.
```

```
## Issue 4: K.μ⁻'s strict-contraction precondition admits a trivial counter to clause B
Reason: The seam between per-subspace clause (A) and whole-arrangement clause (B) needs a worked sub-case showing all-zero-suffix admissibility per (A) being rejected by (B). Internal expository fix.
```

```
## Issue 5: J4 fork composite underspecifies V-position structure of d_new
Reason: This is a design question — what must forking preserve? V-position correspondence speaks to whether forks are "version-like" (preserving display order) or merely "content-like" (preserving I-address set). Nelson's writing on forking semantics would clarify intent; Gregory's docopy implementation shows the realised behavior.
Nelson question: When a document is forked, does the new document inherit the source's V-position structure (so V-positions correspond exactly to the source's at fork time), or only the I-address set with V-positions chosen freely by the fork operation?
Gregory question: In udanax-green's document-copy operation (docopy/docreatenewdocument when copying content from a source), are the destination V-positions structurally identical to the source's V-positions, or are they freshly allocated under the new document's VSA frontier?
```

```
## Issue 6: K.μ~ table classification mismatches its definition
Reason: Typographic mismatch between the elementary/composite categorization established elsewhere in the ASN and the table's column heading. Internal fix.
```

```
## Issue 7: K.μ~-FIX cites D-SEQ before D-SEQ★ is fully derived
Reason: Staging issue with the inductive structure of the proof. The fix is to make explicit that K.μ~-FIX consumes the inductive hypothesis on the pre-state and the K.μ~ contract's postconditions on the post-state, without claiming D-SEQ★ at the post-state ahead of the induction's closure. Internal restatement.
```
