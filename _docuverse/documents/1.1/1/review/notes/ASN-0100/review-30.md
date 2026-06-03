# Review of ASN-0100

I read the ASN as a specification of INSERT's per-state effect, checked each invariant-preservation argument, re-derived the worked examples, and audited the cross-citations to ASN-0082's I3 family. The operation logic, region disjointness (S2), chain-shift identity, sequential-structure (D-SEQ★/D-CTG★/D-MIN★), projection-shift correspondence, and both wp derivations all check out. The append, interior, beginning, and empty-document cases are each handled explicitly and the example arithmetic is correct. One genuine internal contradiction surfaced in the I3 citation scope.

## REVISE

### Issue 1: I3-C listed as an affirmed companion lemma, then declared not-preserved
**ASN-0100, §Discovering the Three Effects → Effect Three ("Scope of ASN-0082's I3 against INSERT's post-state")**: "This ASN cites ASN-0082's I3 only for its positive shift clause and the affirmative companion lemmas (I3-L, I3-X, I3-D, **I3-C**, I3-VD, I3-VP, I3-fin, I3-S2, I3-S3, I3-S7) that govern the regions ASN-0082's model does cover."

**Problem**: I3-C (PostInsertionContentFrame) asserts `Σ'.C = Σ.C` — the entire content store is unchanged. INSERT extends `dom(C)` by the `n` freshly allocated addresses, so I3-C is **false** for INSERT. The ASN itself states this two paragraphs later: "ASN-0082's I3-C (PostInsertionContentFrame), asserting exact equality `Σ'.C = Σ.C` for its shift-only model, is strictly stronger than INSERT's content frame and is not preserved here." The same lemma is therefore listed as both *affirmed* and *not preserved*. Unlike I3-VD/I3-VP/I3-fin/I3-S2/I3-S3 (which have a coherent "shift-only portion" the ASN supplements), I3-C is a global content-store-equality claim with no partial reading — there is no region of INSERT's post-state where `Σ'.C = Σ.C` holds.

**Required**: Move I3-C from the affirmative companion-lemma list into the disclaimed list alongside I3-V, I3-CS (and the redundant I3-CX). The affirmed content-store guarantee for INSERT is the *pointwise* frame `(A a ∈ dom(C): C'(a)=C(a))` (S0/P0), not the *exact-equality* frame I3-C.

### Issue 2: I3-S7 cited as discharging dom(C)-ranging invariants via a premise INSERT breaks
**ASN-0100, §Verifying the Invariants → Post-state V-position well-formedness**: "ASN-0082's I3-VD ..., I3-fin ..., and **I3-S7 (PostInsertionAllocationInvariants)** discharge their respective post-state predicates over ASN-0082's *shift-only* post-state — Left + Shifted-right + cross-subspace."

**Problem**: I3-S7 (S7a, S7b, S7d) ranges over `dom(C)`, not over V-position regions; its ASN-0082 proof is justified "trivially by I3-C (`dom(C') = dom(C)`, per-address values unchanged)." Since INSERT invalidates I3-C (Issue 1), I3-S7's own justification does not transfer, and there is no "Left + Shifted-right + cross-subspace" partition of `dom(C)` for it to range over — the framing is category-confused. The pre-existing-address portion of S7a/S7b/S7d is in fact preserved, but by direct S0/P0 inheritance, not by I3-S7. (The new-address contribution is correctly re-verified separately in the same section via `origin(a_k)=d`, C1, C1b, C1c.)

**Required**: Drop the I3-S7 citation for the dom(C)-ranging invariants and state plainly that S7a/S7b/S7d on pre-existing addresses follow from S0/P0 (pointwise preservation), with the fresh `a_k` discharged by the explicit C1/C1b/C1c argument already given.

## OUT_OF_SCOPE

None beyond the topics the ASN already bounds (DELETE, COPY, REARRANGE, link-subspace insertion, version derivation, replication) — each is correctly declared out of scope.

VERDICT: REVISE
