# Revision Categorization — ASN-0063 review-1

**Date:** 2026-03-21 18:04

## Issue 1: CL1/CL2 claim coverage equals image, but the equality is false
Category: INTERNAL
Reason: The mismatch between finite image sets and infinite span denotations is derivable from the tumbler ordering definitions already present in ASN-0034 and ASN-0053. The fix (containment instead of equality, or element-level restriction) uses only existing definitions.

## Issue 2: Step 2 of CREATELINK is not a defined elementary transition
Category: INTERNAL
Reason: The pattern for defining elementary transitions is established by K.μ⁺ in ASN-0047, and the link subspace invariants (D-CTG, D-MIN, S8-depth) are already stated in ASN-0036/0058. The new transition is a straightforward adaptation with subspace-specific referential integrity.

## Issue 3: S3 violated by link-subspace arrangement mappings
Category: INTERNAL
Reason: The ASN already commits to placing links in M(d) and acknowledges a "link-subspace analogue" of S3. Generalizing S3 to subspace-conditional referential integrity follows directly from the existing subspace separation (L0, L14) and the ASN's own design choice.

## Issue 4: J1 and P7 are mutually unsatisfiable for link-subspace mappings
Category: INTERNAL
Reason: The ASN deliberately omits K.ρ from the composite, implicitly scoping provenance to content. The fix (scope J1 and P7 to content-subspace mappings) follows from the existing subspace partition and the ASN's own treatment of the composite. The coupling constraints in ASN-0047 were written before link-subspace mappings existed and simply need the same subspace guards.

## Issue 5: "Already normalized" claim is incorrect
Category: INTERNAL
Reason: The counterexample (non-consecutive blocks producing overlapping I-spans through transclusion) is constructible from existing definitions of mapping blocks (ASN-0058) and content sharing (S5, ASN-0036). The fix is removing the false claim and noting S8 normalization is required.

## Issue 6: Normalization invokes S8 without checking level-compatibility
Category: INTERNAL
Reason: T10 (PartitionIndependence, ASN-0034) guarantees that spans of different depths occupy disjoint address subspaces, so different-depth CL0 I-spans cannot overlap or be adjacent. Normalization can proceed independently per depth level. This follows from existing tumbler algebra properties.

## Issue 7: CL11 incorrectly claims D-CTG and D-MIN are text-subspace-scoped
Category: INTERNAL
Reason: D-CTG's quantification over all subspaces is explicit in ASN-0036. Verifying D-CTG, D-MIN, and S8-depth for the link subspace follows once Issue 2's fix specifies v_ℓ's value. The invariant statements and verification machinery are all present.

## Issue 8: No concrete worked example
Category: INTERNAL
Reason: All the machinery for constructing a worked example — tumbler address format, mapping blocks, V→I projections, endset construction, postcondition verification — exists in ASN-0034, 0036, 0053, 0058, and this ASN. The example is constructible from existing definitions without external evidence.
