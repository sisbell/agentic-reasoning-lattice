# Revision Categorization — ASN-0029 review-4

**Date:** 2026-03-11 10:51

## Issue 1: AccountAddr undefined
Category: INTERNAL
Reason: The ASN already defines `account(d)` as "the unique `a` with `zeros(a) = 1` and `a ≼ d`". The fix is extracting the explicit set definition `AccountAddr = {a ∈ T : zeros(a) = 1}` from this existing characterization.

## Issue 2: D0 existential scoping
Category: INTERNAL
Reason: Purely a formula-structuring issue. The fix is widening the existential's scope to bind `d` across both post and frame — a notational repair requiring no external information.

## Issue 3: D0 and D12 do not establish D1
Category: INTERNAL
Reason: The ASN already identifies D1 as "a specialization of T9 (ForwardAllocation)" and references T10 (PartitionIndependence). The fix is adding a postcondition clause invoking T9/T10a, which the ASN already cites as the justification.

## Issue 4: D13 Case 1 — descendant vs. immediate child
Category: INTERNAL
Reason: The ASN already describes the behavior as "allocated as a structural child of the source" and the worked example verifies `parent(d_v) = d_s`. The fix is strengthening the formal statement to match the prose and example already present.

## Issue 5: D14 — parent existence in Σ.D not derived
Category: INTERNAL
Reason: The review itself supplies the complete derivation chain (D12 precondition → D13 strengthened → D2 permanence). All premises are already in the ASN; the fix is stating and assembling the derivation.

## Issue 6: D17 — no frame condition
Category: INTERNAL
Reason: The ASN already treats D17 as a pure query (no state modification is described or implied). The fix is adding the explicit frame `Σ' = Σ`, which is the only consistent reading of the existing specification.
