# Channel Assignment — ASN-0086 review-176

**Date:** 2026-06-01 10:32

## Issue 1: P2 over-billed as a Nullify precondition; the "three named conditions" enumeration misrepresents the actual precondition structure
Reason: Internal — the fix is a restructuring of the definition's precondition enumeration using facts the ASN already proves (R-Scope's arity-independence, wp Case 1's PC conjunct and P2 absence). No design intent or implementation evidence is needed.

## Issue 2: The substrate-conformance/NestedLinkWitness partiality rationale is restated at three sites
Reason: Internal — consolidating three restatements of the same off-chain-edge rationale into one canonical site (the Remark) with citations is a pure deduplication using existing ASN content. No external channel needed.
