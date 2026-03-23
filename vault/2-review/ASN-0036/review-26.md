# Rebase Review of ASN-0036

## REVISE

### Issue 1: S4 registry missing TA5 dependency
**ASN-0036, Properties Introduced table**: `S4 | ... | from T9, T10, T10a, T3 (ASN-0034)`
**Problem**: The body text explicitly uses TA5(d) in the nesting-prefix argument: "by TA5(d), `#inc(t, k') = #t + k'`". Without TA5(d), the claim that child allocators produce deeper outputs than parents has no foundation — T10a says the parent performs `inc(·, k')` but does not state the depth formula. TA5(d) is the property that establishes `#t' = #t + k`, which is the load-bearing step before T3 gives distinctness.
**Required**: Add TA5 to S4's registry entry: `from T9, T10, T10a, TA5, T3 (ASN-0034)`.

VERDICT: REVISE
