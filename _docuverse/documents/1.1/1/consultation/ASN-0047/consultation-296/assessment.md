# Channel Assignment — ASN-0047 review-296

**Date:** 2026-06-01 22:29

## Issue 1: GlobalUniqueness invoked system-wide, but the system is a multi-rooted node forest
Reason: The fix is a structural reduction derivable from the ASN itself — ASN-0034's GlobalUniqueness (single-rooted, base case "sole root allocator") applies to each per-node subtree because a baptised node N is the sole root of its own inc-allocator subtree, and cross-node distinctness already rests on T10/CrossNodeAccountBase. No design intent or implementation evidence is needed; the ASN already establishes the forest structure (NodeBaptism, NodeLineage) and the cross-node machinery, so scoping the GU citations per-subtree is an internal reformulation.

## Issue 2: Chained deferrals to "the uniform shape-package discharge above"
Reason: Purely an editorial restructuring of the ASN's own forward references — collapse the two-hop deferral chain into one. No external information is required.

## Issue 3: K.δ case (ii) spawn-admissibility duplicated across two sections
Reason: Purely an editorial deduplication of content already present in the ASN — state the spawn-admissibility requirements once in the K.δ box and the parent-allocator identification once in the dedicated section. No external information is required.
