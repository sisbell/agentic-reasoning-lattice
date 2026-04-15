# Cone Review — ASN-0034/D0 (cycle 1)

*2026-04-15 14:05*

I've read the full ASN carefully, tracing every identifier, precondition chain, and cross-reference. Let me check the formal statements and project model for context.

### D0's proof delegates subtraction well-definedness to "TA2" — an identifier that does not exist in the ASN

**Foundation**: TumblerSub postcondition `a ⊖ w ∈ T`
**ASN**: D0 (DisplacementWellDefined) — *"the subtraction w = b ⊖ a is a well-defined tumbler in T by TA2"*
**Issue**: D0's proof cites "TA2" as the authority for `b ⊖ a ∈ T`. No property in the ASN carries the identifier TA2. The identifiers present are T0, T1, T3, TA0 (WellDefinedAddition), TumblerAdd, TumblerSub, D0, and the PositiveTumbler definition. The intended referent is almost certainly TumblerSub — whose postcondition establishes `a ⊖ w ∈ T` under `a ≥ w (T1)`, which is exactly the fact D0 needs at that step — but TumblerSub is never assigned the code TA2 anywhere in the document. The proof chain from D0's hypotheses (`a < b`, hence `b ≥ a`) through to its first postcondition (`b ⊖ a ∈ T`) passes through a reference that cannot be resolved by reading the ASN as written.

**What needs resolving**: Either assign TumblerSub the code TA2 (if that is the intended naming scheme, paralleling TA0 for addition), or replace the citation "by TA2" in D0's proof with "by TumblerSub."
