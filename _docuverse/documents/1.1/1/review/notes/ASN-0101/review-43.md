# Review of ASN-0101

## REVISE

### Issue 1: The DEL coupling-vacuity point is stated four times
**ASN-0101, "The operation" + D10**: The intro paragraph "The coupling constraints J0, J1★, and J1'★ of ASN-0047's ValidComposite★ ... are vacuous on a one-step composite consisting of a single DEL transition ... The vacuity at the one-step level does not extend automatically to multi-step composites ... D10 below records the precise statement, its scope, and the formal extension" previews a claim that D10 then makes three more times: the vacuity bullets, the "What this does and does not show" paragraph, and the "Consequence" paragraph.

**Problem**: One conceptual point — *DEL is coupling-vacuous in isolation but composites must be checked at their endpoints* — is carried by four separate passages. The intro paragraph is a pure forward reference to D10 that duplicates D10's content; "What this does and does not show" and "Consequence" restate each other (both conclude with "composites that combine DEL with allocation-and-placement steps must be checked at their endpoints"). This is forward-reference accretion: the reader meets the same conclusion four times before and inside D10.

**Required**: State the vacuity-but-not-compositional result once, in D10, with the single K.α→K.μ⁺→DEL counterexample. Delete the intro preview paragraph (the one-step vacuity is not needed to motivate the operation) and fold "What this does and does not show" + "Consequence" into one paragraph.

### Issue 2: D8 Group (ii)/(iii) deferral loop and "enumerated for completeness" inventory
**ASN-0101, D8 Group (ii)**: "By the uniform observation discharged in *Justification (Groups (ii) and (iii))* below, equality of each component propagates every such predicate from `Σ` to `Σ'`; no member requires an individualized argument. The members, enumerated for completeness:"
**ASN-0101, D8 Justification (Groups (ii) and (iii))**: "By the frame argument outlined in each group's description above."

**Problem**: Two patterns compound here. (a) Circular deferral — Group (ii)'s body points forward to the Justification, and the Justification points back to "each group's description above"; neither paragraph carries the argument, they pass it to each other. (b) The substrate chain-discipline lemma list (ChainElementT4Validity, ChainEnumerationInjectivity, DisjointSubAllocatorChains, ChainPrefixExtension, ChainMembershipForOrigin, StoreT4Validity, FirstEmissionFreshness, CrossDocumentDisjointness) is "enumerated for completeness" even though the uniform frame observation discharges the entire class without naming any member. These are ASN-0093 structural lemmas, not members of ASN-0047's per-state invariant theorem; the inventory is a use-site list that does not advance the preservation argument.

**Required**: State the uniform observation once (every Group (ii)/(iii) predicate is over `(C, L, E, R, dom(M))`, all pointwise fixed by D0's frame, so each propagates trivially) and stop. Drop the "enumerated for completeness" chain-lemma roster; if any member needs naming, name only the load-bearing ones the theorem actually requires.

### Issue 3: The recoverability section re-derives version-creation mechanics, and Closing observations re-argues the five-fold theme
**ASN-0101, "A note on recoverability"**: "A version is, in the working framework, a separately addressed document `d_v = inc(d, 1)` — the depth-1 child case of K.δ (ASN-0047) — populated by the J4 ForkComposite (ASN-0047). K.δ alone places `d_v` in `dom(M)` with an empty arrangement ... the J4 composite then uses K.μ⁺ to populate ... and K.ρ to record provenance ..."
**ASN-0101, "Closing observations"**: "Each of the preserved components carries information that *some other party* ... might depend on."

**Problem**: Version creation is OUT OF SCOPE for this ASN, yet the recoverability section walks through K.δ/J4/K.μ⁺/K.ρ version-creation mechanics in detail. DEL's contribution to recoverability is captured entirely by D2 + D5; the version-mechanics walkthrough is scope drift and bloat. Separately, the "Closing observations" essay re-argues the "each preserved component is something another party depends on" theme that D5's "Without D5, a deletion would have to either ..." passage already makes — the same point in different words in two sections.

**Required**: In the recoverability section, reduce the version material to the one load-bearing sentence ("the pre-DELETE arrangement is preserved in any version forked before the DELETE, by D5") without re-specifying how versions are created. Cut the duplicated five-fold-preservation argument from Closing observations or from D5 — keep one.

## OUT_OF_SCOPE

### Topic 1: DEL-then-INSERT exact recovery (Open Question 2)
**Why out of scope**: Whether DELETE followed by insertion at the same V-position recovers the pre-state arrangement depends on INSERT mechanics and fresh-address allocation, which belong to the INSERT ASN. Correctly left as an Open Question, not a claim.

Note: Open Questions 1, 2, and 6 substantially overlap (reconstructibility / DEL-then-insert recovery / full reversibility relative to an observer). Not a REVISE blocker, but consider consolidating to two distinct questions.

META: not applicable — the ASN defines an operation on state with frame conditions and re-established invariants, squarely within specification territory; its issues are prose accretion, not drift.

VERDICT: REVISE
