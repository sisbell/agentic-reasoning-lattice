# Revision Categorization — ASN-0029 review-9

**Date:** 2026-03-11 16:56

## Issue 1: T10 incorrectly cited for between-allocator uniqueness
Category: INTERNAL
Reason: The fix requires splitting the uniqueness argument using T10 (for non-nesting child allocators) and T3/structural length (for root vs child). Both arguments are derivable from tumbler properties already defined in ASN-0001.

## Issue 2: Worked examples skip allocation values without explanation
Category: INTERNAL
Reason: TA5(c) defines `inc(t, 0)` as incrementing by exactly 1. The examples simply need corrected values (3→4, 2→3) to match the stated mechanism — a self-consistency fix.

## Issue 3: P3 preservation for new document in D12 not verified
Category: INTERNAL
Reason: The derivation is one step from existing postconditions — D12(c), D12(e), and P3 on the pre-state. All premises are already stated in the ASN.

## Issue 4: Summary overstates address-purity of ancestry
Category: INTERNAL
Reason: The distinction between ≺ (address-intrinsic) and parent (Σ.D-dependent), and the stability argument (D2 + inc(d_s,1) leaves no room for interposition), are all derivable from existing definitions in ASN-0001 and this ASN. No design intent or implementation evidence needed.
