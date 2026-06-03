# Review of ASN-0068

I checked the core proofs (CV-IN-N, CV-MAX existence/uniqueness, CV-SPAN-VIEW, CV-ATOM, CV-SYM) against the foundation contracts and the five worked examples. The mathematics is sound: the maximal-decomposition existence/uniqueness argument is complete (left/right walk termination correctly grounded in S8a + D-SEQ★ for the left bound and S8-fin for the right; the M-aux region-splitting and the δ=0 / δ>0 uniqueness cases are each discharged), the lockstep-offset reduction via OrdinalShift's last-component formula + T3 is correct, and Examples 1–5 verify against the stated results. The two findings below are anti-bloat (forward-reference accretion), per the note's classifier.

## REVISE

### Issue 1: Orphan sentence previews the Pairwise Scope section
**ASN-0068, paragraph immediately after CV-PROV-FORGOTTEN**: "The pair `(d_a, d_b)` may stand in any relationship — siblings forked from a common ancestor, ancestor and descendant, or wholly independent documents that happen to transclude common material."
**Problem**: This free-floating sentence is attached to no claim and develops the operands' *version-graph relationship*, which is the exact subject of the later **Pairwise Scope** section ("If `d_a` and `d_b` are two versions of the same document... Whether intermediate versions exist... is irrelevant"). It pre-states downstream content rather than advancing CV-PROV-FORGOTTEN, whose body already establishes the distinct point that `origin(a)` may be `d_a`, `d_b`, or neither. This is the forward-reference accretion pattern — two locations carrying the same "the operation is agnostic to the operands' relationship" message.
**Required**: Delete the sentence; the agnosticism-to-version-relationship point is fully developed in Pairwise Scope, and the allocation-origin point is fully developed in CV-PROV-FORGOTTEN's own body.

### Issue 2: Overlapping open questions on result-size bounding
**ASN-0068, Open Questions (4th and 8th)**: "Under what conditions can shared content between two documents be bounded in size — relative to either input's restriction — without exhaustive enumeration?" and "Under what conditions can the result be presented as a set of span-pairs whose total V-width is bounded by the smaller of the two input restrictions?"
**Problem**: Both ask the same underlying question — bounding the result's size relative to the input restrictions. The second is a span-pair-presentation specialization of the first (and ties to CV-SPAN-VIEW). Carrying both as separate open questions is redundant accretion.
**Required**: Fold into a single open question, or differentiate them explicitly if a genuinely distinct question is intended.

## OUT_OF_SCOPE

### Topic 1: Concurrent / replicated-state behavior
**Why out of scope**: The open questions on concurrent mid-comparison modification and on identical results across replicated docuverse copies (replication/BEBE territory) are correctly posed as future work, not developed here. No action needed — flagging only to confirm they are appropriately deferred, not missing coverage.

VERDICT: REVISE
