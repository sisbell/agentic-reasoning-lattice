# Review of ASN-0103

I checked the central derivations — `D_A = E ∩ S(A,2)` (both inclusions), the freshness reduction `d ∈ S(A,2)\D_A = S(A,2)\E`, the length-filter separation of documents from versions, the single-`K.δ` reduction, atomicity, vacuous coupling, and the full `ExtendedReachableStateInvariants` + P3 discharge. The mathematics is sound: the load-bearing direction `D_A ⊆ S(A,2)` via the unique parse is correct, the worked example exercises the version-masquerade boundary faithfully, and every invariant conjunct is addressed (directly, vacuously, or by frame). I found no proof gap, no missing boundary, and no invalid cross-reference (all numbered references are to foundation ASNs).

The note carries the anti-bloat classifier; one finding falls under that lens.

## REVISE

### Issue 1: Ownership claim restated as grounding-prose after its derivation is complete
**ASN-0103, "Ownership and Immediate Referability"**: The first paragraph rigorously derives the result and closes it — "By transitivity of the prefix order, `pfx(π) ≼ A ≼ d`, hence `owns(π, d) ≡ pfx(π) ≼ d`... and it is the ownership guarantee CREATENEWDOCUMENT delivers." The following paragraph then restates the same result: "Over its own state, what creation guarantees is the structural ownership `pfx(π) ≼ d`, together with the design intent that no document exists except as a number forked beneath an owning account."
**Problem**: The structural-ownership claim is fully discharged in the preceding paragraph. The second paragraph repeats `pfx(π) ≼ d` verbatim, wrapped in a Nelson quote and design-intent commentary ("the owned-number tree *is* the record of ownership, not a side table"), without advancing the formal argument. This is the "two paragraphs say the same thing in different words" pattern — formal result, then prose restatement — the kind of meta-prose a precise reader skips past.
**Required**: Keep one. Either fold the single substantive architectural point (ownership intrinsic to the address, not external metadata) into the derivation paragraph as one clause, or drop the restatement. Do not state the guarantee twice.

## OUT_OF_SCOPE

### Topic 1: Effective-owner derivability via entity/registry coupling
**Why out of scope**: The ASN correctly proves only structural ownership `pfx(π) ≼ d` and notes that `ω_{Σ'}(d) = ω_Σ(A)` plus O5 grounding quantify over ASN-0042's registry `B`, absent from this state. The coupling that would make the effective-owner reading derivable is genuinely new territory (already captured as Open Question 6), not a defect here.

### Topic 2: Recovery, concurrency, and removal of created documents
**Why out of scope**: Partial-failure recovery, concurrent same-account creation ordering, and removal-vs-permanence of never-populated documents are raised in Open Questions and belong to future ASNs.

VERDICT: REVISE
