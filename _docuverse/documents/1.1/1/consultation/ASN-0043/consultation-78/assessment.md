# Channel Assignment — ASN-0043 review-78

**Date:** 2026-05-30 09:13

## Issue 1: L1b carries a "why the axiom is needed" rationale paragraph
Reason: Pure prose-trimming. The invariant `#E(a) ≥ 2` and the subspace-stability claim are already present; the fix removes a counterexample walkthrough and use-site pointer. The retained sentence relies only on TA5/`inc(·,0)` mechanics already cited from ASN-0034. Internal.

## Issue 2: L1c preamble and "Joint floor with L1b" are meta-prose / reviser drift
Reason: Editorial deletion of content-free framing and a cross-invariant reconciliation paragraph. Whether the `n ≥ 2` floor is encoded as a clause inside the existential is a structural choice derivable from L1b, which already asserts `#E(a) ≥ 2`. Internal.

## Issue 3: Home and Ownership re-derives the L1c `s = h(a)` postcondition
Reason: The `s = h(a)` postcondition is already named and proven in L1c; the fix replaces a re-walk of the CPP/chain reasoning with a single citation. No new content required. Internal.

## Issue 4: L7 "Scan of the L-invariants" restates every invariant
Reason: The load-bearing observation (no invariant references directional/source-target roles) is verifiable by inspecting L0–L14 as already stated in the ASN. Collapsing the line-by-line restatement needs nothing external. Internal.

## Issue 5: Open Questions item justifies document organization
Reason: Removing a document-organization open-question and optionally attaching a one-clause provenance note to the PrefixSpanCoverage axiom. The axiom's "no link-specific content" characterization is self-evident from its statement. Internal.
