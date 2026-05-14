# Review of ASN-0058

## REVISE

### Issue 1: M7 miscites M-aux for component preservation

**ASN-0058, M7 prose (overlap-exclusion argument)**: "Let m = depth(v₁); by S8-depth (ASN-0036) applied to subspace(v₁), every V-position in that subspace has depth m, and M-aux gives (v₁ + n₁)_j = (v₁)_j for all j < m."

**Problem**: M-aux (OrdinalIncrementAssociativity) states only associativity — (v + c) + j = v + (c + j). It does not establish componentwise behavior of ordinal shift. The cited equation (v₁ + n₁)_j = (v₁)_j for j < m is component preservation under shift, which is a property of OrdinalShift (ASN-0034, postcondition iii: shift(v, n)_i = v_i for i < #v), equivalent to TumblerAdd's prefix-copy clause at action point #v.

**Required**: Replace "M-aux gives" with "OrdinalShift (ASN-0034) postcondition (iii) gives" or "TumblerAdd's prefix-copy clause gives".

### Issue 2: M12 miscites TA0 for component preservation

**ASN-0058, M12 proof (failure-of-condition-3 case, sub-argument j ≥ 1)**: "The unit shift δ(1, m) has action point m: applied to a depth-m tumbler x, it produces [x₁, ..., x_{m−1}, x_m + 1] (TA0 preserves components below the action point, ASN-0034)."

**Problem**: TA0 (WellDefinedAddition) is a named corollary exporting only TumblerAdd's well-definedness postconditions — membership in T and length identity #(a ⊕ w) = #w. TA0 does not state component preservation. The cited claim is TumblerAdd's piecewise definition (r_i = a_i for i < k). The same proof correctly cites "TumblerAdd preserves components below the action point" earlier in M12, making this citation internally inconsistent; M16 also cites TumblerAdd correctly for the identical property.

**Required**: Replace "TA0 preserves components below the action point" with "TumblerAdd's piecewise definition gives r_i = a_i for i < k" (matching M16's usage).

### Issue 3: depth(v) used without definition

**ASN-0058, M7 prose and M12 proof**: "Let m = depth(v₁)"; "depth(v') = depth(v) = m, so #v' = m".

**Problem**: depth(v) appears as a function returning tumbler length, but neither ASN-0058 nor any foundation ASN (ASN-0034, ASN-0036, ASN-0053) defines it as such. ASN-0036's S8-depth uses "depth" in prose to mean tumbler length but does not introduce depth(·) as a notation; the foundation notation is #v. The "so #v' = m" formulation in M12 reads as if depth and # are distinct.

**Required**: Replace depth(v) with #v throughout, or define depth(v) := #v explicitly when first introduced in ASN-0058.

## OUT_OF_SCOPE

(None.)

VERDICT: REVISE
