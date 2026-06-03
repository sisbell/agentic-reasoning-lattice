# Review of ASN-0069

## REVISE

### Issue 1: V9a's second half re-states V9b and adds reconciliation meta-prose
**ASN-0069, §"Provenance Recording", V9a**: "Direct allocation is excluded from this enumeration: V9b establishes `origin(a) ≠ d_new` for every fork-recorded pair, so `d_new` provably did not allocate `a` itself. The indistinguishability of V9a thus ranges only over the acquisition paths that remain possible — fork and transclusion — not over a path V9b has ruled out."

**Problem**: V9a's claim is complete at "neither stored in R nor reconstructable." The two trailing sentences (a) restate V9b's content (`origin(a) ≠ d_new`) and (b) add a meta-qualification about how V9a's scope narrows in light of V9b. This is the "imagines a case the claim already excludes" pattern: V9a raises "direct allocation" as an acquisition path only to have V9b rule it out, and then editorializes about the relationship between the two named properties. V9a and V9b are adjacent named properties; the reader does not need V9a to pre-reconcile itself against the property stated immediately below it.

**Required**: Trim V9a to its core claim (provenance records containment, not acquisition path; the per-address chain of custody is neither stored nor reconstructable). Let V9b state `origin(a) ≠ d_new` on its own without V9a relitigating it.

## OUT_OF_SCOPE

### Topic 1: V6a's link-discoverability apparatus (coverage / project / discoverable_from)
**ASN-0069, §"Subspace Selectivity", V6a and the three preceding local definitions**

V6 (link subspace not inherited) is fork mechanics and is in scope. But V6a goes further and erects a general link-query framework — `coverage(e)`, `project(a, i, d, Σ)`, `discoverable_from(a, d, Σ)` — none of which is a fork-specific notion. These are link-semantic primitives (how a link's endset coverage projects onto a document's V-positions, and when a link is "findable" from a document). The scope note lists **link semantics** as out of scope. The fork-relevant consequence ("the link store is unchanged across the fork, and the source's projections are preserved while the fork inherits the source's content-subspace projections") can be stated from V5 + V3 + V4 without standing up a discoverability calculus that a dedicated link-semantics ASN will need to own.

**Why out of scope**: Discoverability/projection is the query layer over links, not a property of the CREATENEWVERSION transition. Defining it here pre-commits notation (coverage/project/discoverable_from) that belongs in the link ASN and risks colliding with it.

VERDICT: REVISE
