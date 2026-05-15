# Channel Assignment — ASN-0043 review-67

**Date:** 2026-05-14 18:22

```
## Issue 1: PrefixSpanCoverage cited without a host
Reason: The lemma is a span/tumbler-algebra fact whose proof is sketched in-prose as proceeding from ASN-0034 primitives (PrefixRelation, OrdinalShift, NAT-addcompat, T1, Divergence, NAT-discrete). The fix — reinstate proof inline or axiomatize locally — is derivable from ASN-0034 and the ASN's own framing.
```

```
## Issue 2: L1c's "k₁ = 2 only" justification is incorrect
Reason: The reviewer has already diagnosed the formal error and identified the correct argument (position-of-zero from TA5(b)/(c) and `inc(·, 2)`'s positional zero-insertion). Fix is a proof-structure repair internal to ASN-0034 tumbler-algebra primitives.
```

```
## Issue 3: L11a's formal statement is tautological
Reason: Restating L11a to express its intended content (distinct allocation events ⟹ distinct link addresses, as a corollary of L1c + T10a GlobalUniqueness) is purely a formal reformulation within the ASN's own machinery.
```

```
## Issue 4: L0a amends ASN-0036 from within ASN-0043
Reason: Whether to land an ASN-0036 revision vs. scope disjointness to the s_C-resident portion is a structural/pipeline decision about ASN organization. Gregory's two-leaf-type evidence (GRANTEXT/GRANORGL) is already cited in-ASN and supports either resolution; no new channel input is needed.
```

```
## Issue 5: L9 proof — T4-validity of d' not derived
Reason: The missing step is a derivation from T10a's root T4-validity axiom and T10a.4 (T4PreservationUnderDiscipline) along the allocator chain from 𝒯's root — entirely ASN-0034 primitives.
```

```
## Issue 6: L1c chain length and L1b interaction implicit
Reason: Joint-floor noting (`n ≥ 2` from L1b sharpening L1c's local `n ≥ 1`) is a notational tightening derivable from the two invariants as stated in this ASN.
```

```
## Issue 7: Worked example — ASN-0036 invariants only spot-checked
Reason: The missing one-line confirmations (S7a, S7b, S7c, S7d, S8a, S8-depth, D-CTG, D-MIN, D-SEQ) check ASN-0036 invariants against the concrete Σ already constructed. Both the invariants and the Σ are fully specified within the ASNs; no external channel input is required.
```
