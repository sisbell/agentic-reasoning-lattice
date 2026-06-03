# Review of ASN-0100

## REVISE

### Issue 1: Internal contradiction on whether I3-S7 (ASN-0082) is cited

**ASN-0100, §Discovering the Three Effects → Effect Three (Shift)**: the disclaiming paragraph states that INSERT cites the *affirmative companion lemmas*:

> "This ASN cites ASN-0082's I3 only for its positive shift clause and the affirmative companion lemmas (I3-L, I3-X, I3-D, I3-VD, I3-VP, I3-fin, I3-S2, I3-S3, **I3-S7**) that govern the regions ASN-0082's model does cover."

But §Verifying the Invariants → "Post-state V-position well-formedness (…) and S7 invariants" states the opposite, twice:

> "ASN-0082's I3-S7 is not cited here — its own justification rests on I3-C (Σ'.C = Σ.C), which INSERT breaks; instead, S7a/S7b/S7d on pre-existing addresses follow from pointwise S0/P0 preservation, and the fresh a_k are discharged by the explicit C1/C1b/C1c argument below. ASN-0082's I3-S7 is not cited here."

**Problem**: I3-S7 is listed among the lemmas the ASN *does* cite in Effect Three, and explicitly disclaimed in the invariants section. The decoupling of I3-S7 from the (disclaimed) I3-C shift-only frame was evidently applied to the invariants section but the Effect Three roster was left stale. The framing in Effect Three ("govern the regions ASN-0082's model does cover") is also inapt for I3-S7, which ranges over `dom(C)` and the document set, not over V-position regions — exactly the reason the later section gives for not citing it. All other lemmas in that roster (I3-L, I3-X, I3-D, I3-VD, I3-VP, I3-fin, I3-S2, I3-S3) are treated consistently between the two sections; I3-S7 is the lone contradiction.

**Required**: Remove I3-S7 from the affirmative-companion list in Effect Three (and, if desired, note there that the S7-family invariants are discharged separately in §Verifying the Invariants without recourse to ASN-0082's I3-S7, since its derivation rests on the I3-C frame INSERT breaks).

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
