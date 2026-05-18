# Channel Assignment — ASN-0047 review-101

**Date:** 2026-05-18 03:01

## Issue 1: P4★/P4a/P7a misclassified in per-state invariant list
Reason: The proof's Class (a)/Class (b) partition already distinguishes per-state from composite-boundary invariants; the fix is restating the theorem to match the proof's existing structure. Internal — no external evidence needed.

## Issue 2: Interior replacement example overstates intermediate-state requirements
Reason: The notation disambiguation point (c) and the proof's Class (b) treatment already establish P4★ as a composite-boundary invariant; the fix reframes the verification prose to match. Internal — derivable from existing ASN content.

## Issue 3: Replacement composite description glosses K.α and K.ρ
Reason: The interior worked example already shows the K.α + K.μ⁻ + K.μ⁺ + K.ρ shape for fresh-content replacement, and J1★ + J0 require those couplings; the fix is to align the *Elementary transitions* prose with the established couplings. Internal.

## Issue 4: K.μ~ link-subspace fixity depends on pre-state CL-UNIQ — dependency chain implicit
Reason: Both the fixity lemma's Step 4 and the inductive CL-UNIQ structure are already in the ASN; the fix is making the implicit dependency explicit in the proof's K.μ~ paragraph. Internal.

## Issue 5: K.δ case (ii) k=2 activation discharge is dense
Reason: The ASN claims account/document sub-allocators activate when their parent entity enters E, but doesn't ground this in T10a's spawn discipline or in an explicit axiom. Resolving requires implementation evidence on whether the granfilade pre-readies child sub-allocators upon parent entity creation, plus design intent on hierarchical activation cascade.
Nelson question: Does the hierarchical baptism design intend that placing an entity into E simultaneously activates its child sub-allocators (account-of-node, document-of-account), or are child sub-allocators activated by a separate event at the first descent?
Gregory question: In udanax-green, when a node or account is created in the granfilade, are the account or document sub-allocators under it immediately available to accept inc-emissions, or is there a separate activation/registration step before the first child can be allocated?

## Issue 6: L3 narrowing from foundation arity ≥3 to exactly 3 — local-extension inconsistency
Reason: The choice between local-strengthening framing and revising foundation L3 depends on whether any version of the system ever admitted arity > 3. Both design intent and implementation evidence bear on this.
Nelson question: Was the link design ever intended to admit more than three endsets, or has the structure always been exactly the triple (F, G, Θ) — from-set, to-set, type-set?
Gregory question: Does the udanax-green link data structure support more than three endsets per link, or is the arity fixed at exactly three (F, G, Θ) throughout the implementation?
