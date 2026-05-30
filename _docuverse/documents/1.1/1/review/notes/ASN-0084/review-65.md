# Review of ASN-0084

## REVISE

### Issue 1: R-CS3 mischaracterizes how the subspace S is determined

**ASN-0084, R-CS3 (SubspaceConfinementNecessity)**: postcondition "Dropping CS3 ... leaves the precondition R-PRE(iv) **ill-posed**"; proof "**CS3 is the sole clause fixing the single subspace S** that R-PRE(iv) quantifies over ... the symbol S is the common subspace of the cuts, supplied by CS3. With the cuts split across subspaces 1 and 2 **there is no single S**."

**Problem**: The State and Vocabulary section fixes S globally — "we use S = 1 throughout and read every appearance of S in this ASN as the text-subspace identifier 1." Under that convention S is *not* supplied by CS3; it is the constant 1, and CS3 merely requires `subspace(cᵢ) = S = 1`. So R-PRE(iv) is never "ill-posed" and there is never "no single S." The lemma's own proof contradicts its framing: its substantive half ("Reading S = 1 ... the range contains every [1, k] with k ≥ 2 ... R-PRE(iv) then demands [1, 6] ∈ V_S(d), which fails") correctly shows **unsatisfiability** under the fixed S = 1, not ill-posedness. The "no single S / ill-posed" prose is incoherent against the global S = 1 declaration.

**Required**: Restate R-CS3's postcondition and proof purely as an *unsatisfiability* result: with S fixed to 1, a cut sequence whose exclusive bound c_{n−1} lies in subspace 2 forces R-PRE(iv) to quantify over infinitely many subspace-1 positions against a finite V_S(d) (S8-fin), so the precondition cannot hold. Delete the "CS3 fixes/supplies S" and "no single S" claims.

### Issue 2: Redundant back-reference and repeated downstream deferrals (anti-bloat)

**ASN-0084, "Sufficient Precondition" opening; "Invariant preservation"; CanonicalRunDecomposition**: "That R-PRE ... suffices to establish the invariant suite on the post-state M'(d) **is exactly the content of the *Invariant preservation* paragraph above** (with post-state S8 established in R-BLK)."

**Problem**: This sentence advances no reasoning — it restates the prior paragraph and re-defers S8 to R-BLK. The S8 → R-BLK deferral already appears in *Invariant preservation* ("post-state S8 is established where it is consumed, in R-BLK below") and recurs here and in the Open Questions; the CanonicalRunDecomposition definition adds another downstream pointer ("operational reduction deferred to a future ASN" / "Whenever the worked examples report a 'canonical partition,' they name this..."). These are the "multiple paragraphs defer to the same location" and "two paragraphs say the same thing" patterns the precise reader must skip past.

**Required**: Drop the restating sentence; open "Sufficient Precondition" directly with "This section records a complementary necessity result..." Keep a single statement that post-state S8 is established in R-BLK (in the Invariant preservation audit) and remove the duplicate deferrals.

## OUT_OF_SCOPE

### Topic 1: Operational recovery of the maximal partition from B'
**Why out of scope**: R-BLK correctly produces a valid (possibly non-maximal) partition and leans on foundation S8 for the maximal one. The confluent merge procedure that reduces B' to the canonical decomposition is genuinely new territory, already listed in Open Questions.

### Topic 2: k-cut rearrangements (k > 4) and composition of rearrangements
**Why out of scope**: This ASN defines only the 3-cut and 4-cut classes; generalization and closure under composition are future work, correctly deferred.

VERDICT: REVISE
