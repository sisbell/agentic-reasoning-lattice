# Channel Assignment — ASN-0134 review-40

**Date:** 2026-06-14 11:42

## Issue 1: A1 classifies all of BH4 as a zero-step read, but `retract_stale` is a batch
Reason: Purely internal contradiction — A5 already states outright that `retract_stale` is "a sequence of wrapper steps, not an atomic operation," directly refuting A1's zero-step gloss, and BH4's decomposition into `age`/`stale`/`retract_stale` is already cited from ASN-0128. Narrowing the citation to the read operations follows from the note's own A5 plus the already-present ASN-0128 reference; no design intent or implementation evidence is in question.

## Issue 2: The stack's per-state invariant roster is enumerated twice (§2 and A6)
Reason: Editorial deduplication of two lists both already present in the note — A6's package is a superset of the §2 preview. Consolidating the roster to A6 and reducing §2 to its argumentative content (no boundary-reserved property class) is derivable from the note alone; no facts about design intent or the implementation are needed.

## Issue 3: Forward-reference accretion around clause 8 / §9
Reason: Anti-bloat restructuring internal to the note — collapsing repeated pointers to clause 8/§9 into one and dropping document-structure forward references. No semantic content changes, so neither channel is implicated.

## Issue 4: "MinimalIsolationContract" contains an admittedly non-load-bearing clause
Reason: The note already establishes via W6 (citing ASN-0126 P1 / ASN-0128 R1) that runtime registry writes are nonexistent, and the §9 prose already certifies clause 6 as redundant. Resolving the minimality tension — drop clause 6 into W6's directive or reframe it as a retained derived directive and qualify the minimality claim — is a presentation choice fully grounded in content already in the note.
