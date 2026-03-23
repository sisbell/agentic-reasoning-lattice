# Rebase Review of ASN-0036

## REVISE

### Issue 1: S4 derivation incomplete for nesting-prefix allocators
**ASN-0036, Content identity section**: "T10 (PartitionIndependence, ASN-0034) covers cross-allocator distinctness: non-nesting prefixes yield disjoint subtree populations, so allocations from different allocators cannot collide. Together they guarantee that no two distinct allocations — whether from the same allocator or different allocators, whether simultaneous or separated by years — produce the same address."

**Problem**: T10 requires non-nesting prefixes as a precondition (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Parent-child allocators have nesting prefixes: by T10a, the parent creates a child via `inc(t, k')` with `k' > 0`, and by TA5(d), `t ≼ inc(t, k')`. T10 does not apply to this pair. The text claims T9 + T10 cover "whether from the same allocator or different allocators," but the case of different allocators with nesting prefixes is unaddressed.

The conclusion is correct — parent outputs have depth `m` while child outputs have depth `m + k'`, so they are distinct by T3 (CanonicalRepresentation). But this reasoning step is absent from both the body and the registry.

The registry entry `from T9, T10 (ASN-0034)` is therefore incomplete. Note that S7's registry correctly includes T4 among its dependencies (which provides an alternative bridge via separator structure at the element level), but S4 operates at the abstract allocator level where T10a + T3 is the appropriate resolution.

**Required**: Add a sentence to the derivation paragraph handling the nesting case, e.g.: "For allocators with nesting prefixes (parent-child), T10a guarantees the child's outputs are deeper than the parent's (by TA5(d), `#inc(t, k') = #t + k'`), so T3 ensures their outputs are distinct." Update the registry to `from T9, T10, T10a, T3 (ASN-0034)`.

VERDICT: REVISE
