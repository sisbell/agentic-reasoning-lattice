# Channel Assignment — ASN-0047 review-63

**Date:** 2026-05-16 23:46

```
## Issue 1: V-ordering not formally defined
Reason: The fix anchors "V-ordering" to T1 of ASN-0034 restricted to depth-m_S positive tuples with first component S. This is a definitional cross-reference derivable from the ASN and the foundation; no design intent or implementation evidence is required.
```

```
## Issue 2: Reachable-state invariants theorem mixes per-state and per-transition properties
Reason: The fix mirrors the existing per-state / per-transition split already executed for the extended-state version (ExtendedReachableStateInvariants + ExtendedTransitionInvariants). The pattern is internal to the ASN; no external channel needed.
```

```
## Issue 3: Missing concrete worked example for interior content replacement
Reason: The decomposition shape, admissibility conditions, and invariant checks are already fully specified in the ASN; the fix is a mechanical trace on a concrete arrangement. No design intent question and no implementation evidence is needed to construct the example.
```
