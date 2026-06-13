# Channel Assignment — ASN-0123 review-6

**Date:** 2026-06-13 00:03

## Issue 1: The node-tier cross-owner fork mints two entities, contradicting `E' = E ∪ {v}`, V0, and V1
Reason: The contradiction and its resolution are internal to the note. The two-entity mint is forced by the ASN's own apparatus — `inc` reaching only `k ≤ 2`, the zeros hierarchy (node=0, account=1, document=2), and P1 permanence — all already present. The fix is likewise derivable from existing material: the Scope clause already excludes document-creation-from-nothing, the delegation machinery (O12–O15) already supplies how a node-tier principal obtains an account, and PS already frames forking as an account-holder activity ([LM 4/17]). The author can restrict VERSION's single-mint guarantee to forkers holding a document-creation namespace and treat the prior account establishment as out-of-scope setup (option A), or case-split the entity-count claims and resolve `Π' = Π` / V9(b) against whether `a_acct` is registered (option B) — either choice is a formal-hygiene decision the note can make from its own definitions and the established hierarchy, with no new design intent or implementation evidence required.
