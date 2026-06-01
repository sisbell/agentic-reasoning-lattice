# Channel Assignment — ASN-0047 review-246

**Date:** 2026-06-01 12:56

## Issue 1: Deferral chain (and a misdirected pointer) for the K.μ~ "full-clearance form" canonical statement
Reason: Purely structural/editorial fix — relocate the existing canonical statement ahead of its first use and correct the forwarding pointers. All content already exists in the ASN; no design intent or implementation evidence is at stake.

## Issue 2: The primary allocation operations discharge their freshness obligation entirely by forward reference
Reason: Purely an ordering/presentation fix — either reorder the SubAllocFresh/SubAllocatorBundle machinery or inline the three-part freshness discharge, all of which is already stated within the ASN. No external design or code input is needed.
