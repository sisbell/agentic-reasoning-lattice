# Review of ASN-0101

## REVISE

### Issue 1: D8's enumerated per-state invariant groups omit S7d (and mislabel L14)
**ASN-0101, D8, "Groups (ii)–(iii)"**: "The membership of the two groups: *Group (ii)* ... M0, S4, S7a, S7b, C1, C1b, C1c, C2, L0, L1, L1a, L1b, L1c, L3, SD, L-fin, C-fin ... *Group (iii)* ... M1, C0, P0, P1, P2, P3, P6, P7, P8, and L12a, L12b."

**Problem**: D8 claims to cover "every foundation per-state invariant that the pre-state was required to satisfy," and the phrase "The membership of the two groups:" presents the enumeration as exhaustive. But ASN-0047's `ExtendedReachableStateInvariants` theorem — the source of the per-state invariant set — lists **S7d** (DocumentAllocationDiscipline) as a per-state invariant, and S7d appears in neither Group (i), (ii), nor (iii). S7d predicates over document tumblers / `dom(M)`, which D0's frame fixes (`dom(M') = dom(M)`, `E' = E`), so it is trivially preserved and belongs in Group (ii)/(iii) — but the exhaustiveness claim is currently false as written. Separately, D8 cites the ASN-0047 theorem as the invariant source yet enumerates store disjointness under ASN-0093's label "SD" rather than the theorem's label "L14"; a reader matching D8's list against the cited theorem cannot confirm L14 is covered without knowing SD ≡ L14.

**Required**: Add S7d to the Group (ii)/(iii) enumeration with the frame-fixed discharge, and either use the label L14 (matching the cited ASN-0047 theorem) or note explicitly that SD is ASN-0093's name for L14.

### Issue 2: Defensive citation-choice aside in the containment reduction
**ASN-0101, "Justification of the reduction"**: "each component `v_j` is a natural number by T0 (CarrierSetDefinition, ASN-0034) — we ground `v`'s components in T0 rather than S8a because `v` is an arbitrary candidate tumbler, not yet known to inhabit `V_S(d)`, so its well-formedness cannot be assumed."

**Problem**: The clause after the em-dash explains *why a particular foundation is cited instead of another* rather than advancing the argument — a defensive justification anticipating a reviewer's objection. The bare citation "each component `v_j` is a natural number by T0" is self-sufficient; the meta-explanation is the kind of around-the-claim prose the anti-bloat pass targets.

**Required**: Delete the "we ground ... rather than S8a because ..." clause; the T0 citation stands on its own.

## OUT_OF_SCOPE

### Topic 1: Causal ordering across transcluding documents
**Why out of scope**: D5 establishes structural independence of DELETE across documents; relating two documents' deletions causally (Open Question 5) is downstream versioning/observation machinery, correctly deferred rather than specified here.

VERDICT: REVISE
