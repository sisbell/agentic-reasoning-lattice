# Channel Assignment — ASN-0111 review-44

**Date:** 2026-06-10 23:59

## Issue 1: The caching discipline's residual-class prohibition and exactness claim are falsified by a permanence family the note misses
Reason: The choice between weakening (a) and completing (b) hinges on whether the `#U(a) = 1` restriction is a stable feature of the system or an artifact of the current kinematics — if hierarchical sub-accounts are intended or implemented, the user-field permanence family and option (b)'s closure claim are unsafe. Nelson settles design intent for the user field; Gregory settles what address shapes the implementation actually emits, paralleling the note's existing "Gregory's allocator concurs" evidence for the depth family.
Nelson question: Is the user/account field of a tumbler address intended to be hierarchical — that is, does the design contemplate sub-accounts whose user field has more than one component — or is the user field meant to stay flat?
Gregory question: Does udanax-green's account-creation path ever emit, or its retrieval path ever accept, addresses whose user field has more than one component, and more broadly do its allocators ever produce addresses outside the shape node-lineage-under-1, single-component user field, `#E = 2`?

## Issue 2: Inaccurate citation of J4's composite shape in the worked read
Reason: The fix is internal — the review establishes that the sentence's own J0/J1★/J1'★ discharge carries the validity argument, so the J4 appeal can be dropped or reworded to claim only the shared coupling pattern without consulting either channel.

## Issue 3: The address-insufficiency observation and its consequence are stated twice
Reason: The fix is internal — it is a deduplication edit, keeping the proved statement at the screen paragraph and trimming the motivational restatement, with no new fact required from either channel.

## Issue 4: Defensive notation-provenance clause in the signature paragraph
Reason: The fix is internal — the review supplies the exact replacement wording, and the change removes provenance commentary without altering any technical content.
