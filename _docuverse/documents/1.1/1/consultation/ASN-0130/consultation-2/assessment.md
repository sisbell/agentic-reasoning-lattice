# Channel Assignment — ASN-0130 review-2

**Date:** 2026-06-12 08:47

## Issue 1: Discipline is claimed enforced but the shipped surface itself provides the undisciplined route
Reason: The fix is internal — the enforcement mechanism (extending I6's uniform emit preconditions, exactly ASN-0128's `K ≁ R` / S3 pattern) is already established in the corpus and named by the review, and choosing enforcement over unenforced convention follows from the note's own claimed guarantees (PR1, PR2, PR5).

## Issue 2: The view dimension is unresolved — and PR5's certificate is ill-posed without it
Reason: The choice between recording a view in the signed term and keeping definitions view-polymorphic with view-indexed (or view-independent) certificates is a genuine semantic design decision the ASN's content does not settle; Nelson speaks to whether a published definition's meaning was meant to be fixed or reader-relative, and Gregory speaks to whether query scope is caller-supplied in the implementation.
Nelson question: Did Nelson intend a published, citable artifact (here a stored predicate/filter) to carry a meaning fixed at publication for all readers, or was the scope of link visibility — which links and states a query sees — meant to be each reader's per-use choice, as with front-end link filtering?
Gregory question: In udanax-green's link retrieval (e.g., findLinksFromToThree and its specset arguments), is the state being queried — which document versions' spans are searched — supplied by the caller on each query, or fixed by the backend, and can historical (non-current) versions be queried the same way as current ones?

## Issue 3: PR0's wp equivalence holds only on disciplined derivations, but is displayed unscoped
Reason: Internal — this is a proof-scoping repair within the note's own framework, and the review names the exact fix (add PR0's wp to the existing discipline-scoping sentence, with the reduced form scoped to SD as the C3-elimination step already is).

## Issue 4: Well-typedness of the expansion is asserted, never derived
Reason: Internal — the missing substitution lemma is dischargeable from machinery the note already cites (WT-ref's premise sorts plus ASN-0129's PC2 composition/substitution rule), by induction along the reference DAG that PR2 already proves well-founded.

## Issue 5: "Resident references" misdescribes condition (iv) in two places
Reason: Internal — a terminology correction; condition (iv)'s actual content (registration, which entails residence but not conversely) is fully defined within the note, so the bullet and step 5 just need rewording to match it.
