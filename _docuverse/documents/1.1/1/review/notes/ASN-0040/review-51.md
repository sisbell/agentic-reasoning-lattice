# Review of ASN-0040

## REVISE

### Issue 1: B7 proof carries methodology meta-prose about a prior approach
**ASN-0040, B7 proof and Depends**: "We prove disjointness directly from the canonical stream form (S(p,d), S1) and the field-segment constraint (T4), *without presupposing that p, p′, and their spawns are realized within one T10a-conforming allocator tree*." and Depends: "*The proof is independent of T10a.6's allocator-tree framing.*"
**Problem**: This is reviser drift — prose that explains what the proof *no longer* relies on relative to an earlier version, rather than advancing the argument. A reader following the disjointness proof must skip past a justification of the proof's lineage. The proof stands on its own; the "without presupposing…" clause and the closing independence sentence add nothing the cases don't already establish.
**Required**: Delete both clauses. State the proof from canonical form and let it carry itself.

### Issue 2: B6's "dual role" prose duplicates the necessity proof
**ASN-0040, B6 statement**: "Condition (i) serves a dual role: when the parent has adjacent zeros, the violation propagates to the stream; when the parent ends in zero, the stream may satisfy T4 but coincides with a valid stream from a different parent, collapsing namespace disjointness (B7)."
**Problem**: This is the entire content of necessity sub-cases (a) and (b), pre-stated in the prose block before the proof, then proved again in full below. Two passages in the same property say the same thing in different words. The reader reads the dual-role argument twice.
**Required**: Keep the dual-role characterization in exactly one place — either as a one-line preview or inside the necessity proof, not both.

### Issue 3: Bop's "Well-definedness" re-derives what next()'s justification already established
**ASN-0040, Bop "Proof of well-definedness"**: "If empty, the result is inc(p, d) … If non-empty, the result is inc(max(children(s.B, p, d)), 0). By B1 … max therefore exists and equals cₘ … TA5's first … postcondition then gives `inc(cₘ, 0) ∈ T`. In both branches, next produces an element of T."
**Problem**: next()'s own "Justification of well-definedness" already proved `next(B,p,d) ∈ T` by the identical two-branch case split (empty → inc(p,d) ∈ T; non-empty → max exists by T1 total order, inc ∈ T). Bop re-proves it. The only genuinely new content in Bop's proof is freshness (a ∉ s.B); the well-definedness half is redundant.
**Required**: Have Bop cite next()'s well-definedness result and keep only the freshness argument.

### Issue 4: hwm "Justification" and B2 both derive max = cₘ
**ASN-0040, hwm Justification** ("by S0 … max(children(B, p, d)) = cₘ") and **B2 proof, Case 2** ("By S0 … the maximum of a finite strictly ordered set is its last element, so max(children(B, p, d)) = cₘ").
**Problem**: The same derivation (B1 contiguity + S0 ordering ⟹ max = cₘ) appears in both, even though the hwm justification explicitly defers next-address derivation to B2 ("The next-address derivation from m is carried by B2 below"). If the next derivation is B2's job, the max identity belongs there once.
**Required**: Derive max = cₘ in one location and reference it from the other.

### Issue 5: allocated-set non-claim duplicates an open question
**ASN-0040, "Relationship to ASN-0034's allocated set"**: "This ASN neither assumes nor establishes `allocated(s) ⊆ s.B`."
**Problem**: This defensive non-claim states a deferral that Open Question 2 ("Under what activation discipline does `allocated(s) ⊆ s.B` hold…") already records. Two sections defer the same downstream topic.
**Required**: Drop the body non-claim; the open question carries it.

### Issue 6: B1's use of B10 across simultaneous inductions is under-stated
**ASN-0040, B1 proof, sub-case B**: "Moreover, B10 for the current state ensures every element of B satisfies T4, so children(B, p, d) = ∅."
**Problem**: B1 cites B10 *at the same precondition state* of its own transition induction, and B10 is stated later in the document with its own induction. The reasoning is sound only because B10's induction is independent of B1 (B10 cites B6/B_fin, not B1) — but the ASN never states that the two inductions are jointly well-founded, leaving the reader to verify acyclicity unaided. The forward reference to a later property *inside* an induction warrants an explicit note that B10 is established independently for all reachable states.
**Required**: Add one sentence establishing that B10 (and B_fin) are proved by inductions that do not depend on B1, so B1 may invoke them at any reachable state without circularity.

## OUT_OF_SCOPE

### Topic 1: B3 forward requirement on `Occupied`
**Why out of scope**: B3 is correctly framed as a forward requirement parametric in a future content predicate, and content storage is explicitly deferred. It defines no content operation here, so it stays — but the four-way classification table is borderline essay content in a structural slot. If a future cycle trims it, the populated/ghost/unbaptized/forbidden partition is the load-bearing part; the surrounding prose is not.

META: (none — the ASN defines state (s.B), an operation (baptize), and invariants (B0–B10) abstractly, with no drift into implementation mechanics.)

VERDICT: REVISE
