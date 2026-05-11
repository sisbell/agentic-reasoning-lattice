# Channel Assignment — ASN-0036 review-102

**Date:** 2026-05-11 14:47

```
## Issue 1: Broken NAT-* citation chain for "1 < 2" in S8 auxiliary lemma
Reason: The fix is a direct rederivation using NAT-addcompat's strict successor inequality at n=1 (giving 1 < 1+1 = 2) combined with NAT-order's <-transitivity — all tools already cited from ASN-0034. Derivable from the ASN's foundation.
```

```
## Issue 2: Unstated NAT addition commutativity in S8 auxiliary lemma
Reason: The fix restructures the derivation using NAT-addcompat's left order compatibility and NAT-sub's right-inverse (both already in ASN-0034), bypassing the nonexistent commutativity claim. Derivable from cited foundation.
```

```
## Issue 3: Strict-lifting of NAT-addcompat without NAT-cancel citation
Reason: Mechanical update to depends lists — add NAT-cancel with the strict-lifting role spelled out in S8 and expand D-CTG-depth's existing NAT-cancel entry. Derivable from ASN-0034's NAT-cancel axiom.
```

```
## Issue 4: Incorrect length bound gloss in S8 auxiliary lemma
Reason: Correction of an arithmetic gloss using T4's field-segment constraint (every present field non-empty) already cited in the ASN — recount as 3 separators + 4 components ≥ 7, or ≥ 8 with S7c. Derivable from cited foundation.
```

```
## Issue 5: S5 cross-document construction notation inconsistency
Reason: Pure notational cleanup — standardize on (dᵢ, v) with v fixed throughout the cross-document construction. Internal to the ASN.
```

```
## Issue 6: Properties Introduced table missing subspace(v) row
Reason: Mechanical table update — add a subspace(v) row parallel to the existing subspace_I(a) row, with dependencies on T0 and S8a as already established by the function's Formal Contract. Internal to the ASN.
```

```
## Issue 7: S8 auxiliary lemma applicability under singleton existence proof
Reason: The choice between strengthening S8 to prove non-singleton existence versus clarifying the worked-example framing is internal — the architectural mechanism (T10a + TA5(c) producing consecutive allocations) and the auxiliary lemma's k ≥ 1 machinery are already in the ASN. Derivable from cited foundation and existing prose.
```
