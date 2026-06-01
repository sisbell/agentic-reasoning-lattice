# Channel Assignment — ASN-0086 review-158

**Date:** 2026-06-01 05:20

## Issue 1: Properties table cells carry proof-structure commentary, not statements
Reason: Purely editorial — trimming proof-method commentary from table cells while keeping the property statement and type. The statements and proof-dependency notes already exist in the ASN's proof bodies, so the fix is fully internal.

## Issue 2: `→ ≡ K.σ ∪ K.α ∪ K.λ` is stated three times in immediate succession
Reason: Purely editorial deduplication — collapsing three redundant restatements of the same closure fact into the equation plus one naming sentence. No design intent or implementation evidence is needed; the content to retain is already present.
