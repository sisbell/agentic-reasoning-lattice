# Channel Assignment — ASN-0075 review-1

**Date:** 2026-05-25 06:43

```
## Issue 1: D-EXH proof skips required chain through L14 and S3★
Reason: The fix is a proof-chain elaboration using axioms already listed in the Foundation Recap (subspace_I precondition, L14, S3★, P4★). No design intent or implementation detail is needed.
```

```
## Issue 2: D-ORD claims false uniqueness of vpos_B
Reason: The fix is a deterministic choice — `vpos_B(a) = min{v : M(d_B)(v) = a}`, well-defined by T1 totality and S8-fin. All resources are present in the ASN's foundation.
```

```
## Issue 3: D-ACT cites M11-M12 for wrong decomposition
Reason: A direct proof of unique I-contiguous same-origin decomposition follows from T1 (linear order on I-addresses) and the origin function, both already cited. Removing or replacing the M11-M12 citation needs no external input.
```

```
## Issue 4: No concrete worked example
Reason: The worked example is mechanical given the ASN's definitions and the ASN-0047 transitions already cited; the scenario can be constructed abstractly and traced through the predicates without external consultation.
```

```
## Issue 5: wp analysis trivial
Reason: The non-trivial wp computations the reviewer suggests are derivable from the predicates and output-set definitions introduced in this very ASN, combined with P4★ and historical fidelity already in the foundation recap.
```

```
## Issue 6: D-DISCR uses informal transition language
Reason: The fix names specific transitions from ASN-0047 (already cited) and clarifies that the two histories are independent reachable states, with the same `a` allocated in a shared prefix before divergence. GlobalUniqueness is satisfied by sharing the allocator-firing prefix — all derivable from ASN-0047.
```

```
## Issue 7: Open question on DELETED monotonicity is already established
Reason: P2 (R ⊆ R') and the K.μ⁺ transition semantics from ASN-0047 already settle the original question. Removing it or substituting a technical refinement (e.g., interaction with K.μ~) is internal cleanup.
```
