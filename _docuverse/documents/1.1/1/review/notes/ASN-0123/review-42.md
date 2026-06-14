# Review of ASN-0123

I checked the load-bearing proofs — VN-B1's induction over K.δ arrivals, SA's antichain argument, the G2 range-preservation necessity, V-WF's clause-1/clause-2 discharge (both branches), V8's coverer-set equality, and V9's structural O5(ii)/severance derivation. They hold. The boundary cases the topic demands (empty source `n=0`, links-only source via V2b, base-document truncation, iterated owned forks, cross-owner severance) are all addressed, and the three worked instances verify V2/V4/V5/V9/V9w/V10/V13 against concrete addresses. Two issues remain, both narrow.

## REVISE

### Issue 1: Open question OQ3 contradicts the settled position in V2b / V10(iv)

**ASN-0123, "Open Questions" (OQ3) vs. V10(iv) and V2b**:

OQ3: "Must any guarantee carry a source's link-subspace arrangement across a fork, or is content-anchored discoverability the complete obligation?"

V10(iv): "The guarantee is precisely over content anchors: links anchored to content the version transcludes, which is what the design owes **and all it owes**."

V2b: "Cross-fork connectivity therefore has exactly one channel, content anchoring, and V10 shows that channel **is total over what the question asks of it**."

**Problem**: OQ3 lists as open the exact completeness the body asserts as established. V2b proves link-subspace carry is *impossible* (`origin(ℓ) = d_src ≠ v` under CL-OWN and K.μ⁺_L's precondition), and V10(iv) declares content-anchoring "all it owes." A reader cannot tell whether the fork's link obligation is settled (V10(iv)/V2b) or open (OQ3). "across a fork" scopes OQ3 to this operation, the same scope V10(iv) closes — so the two collide on the same word, "obligation."

**Required**: Reconcile. Either drop OQ3 (the fork's link obligation is discharged by V2b + V10), or reword it to the part the note has *not* settled — whether some *future, non-fork* mechanism should make links-about-links themselves versionable (which is distinct from, and does not reopen, the fork's content-anchoring obligation). As written, the note answers its own open question affirmatively in the body.

### Issue 2: The link-subspace-exclusion fact accretes across G2 / V2 / V2b / V10(iv); G2 previews V2b's proof

**ASN-0123, G2 ("Deriving the Operation")**: "Transcribing it is not merely omitted; it is impossible — no reachable transition can seat a foreign-origin link in v's link subspace (V2b, ForeignLinkExclusion, proves this from CL-OWN and K.μ⁺_L's `origin(ℓ) = d` precondition)."

**Problem**: The single structural fact "the version's link subspace cannot carry the source's links" is asserted in G2 (with a forward reference), in V2's "Content subspace only" gloss, formalized in V2b, and re-applied in V10(iv). The G2 parenthetical does more than cite forward — it reproduces V2b's *proof basis* ("from CL-OWN and K.μ⁺_L's `origin(ℓ) = d` precondition") before V2b appears. This is the forward-reference accretion the anti-bloat mode targets: the derivation section previews the claim's internals rather than deriving the *necessity* (that content-anchoring is the only channel) and deferring the *impossibility* to V2b by bare citation.

**Required**: In G2, state that link-subspace transcription is impossible and cite V2b for it, without restating V2b's proof mechanism. Let V2b carry CL-OWN and the K.μ⁺_L precondition once.

## OUT_OF_SCOPE

Nothing to add — the note delimits scope cleanly (document-from-scratch, comparison, content/link operations, delivery, replication), and the cross-owner branch's reliance on the document namespace `S(pfx(π),2)` having a well-defined frontier is correctly discharged through ASN-0047's FrontierEquivalence/ChildSpawnFreshness rather than re-proving a contiguity analog (which the cross-owner allocation, needing only freshness and not rank/navigation, does not require — the asymmetry with the proven version-namespace VN-B1 is justified, not a gap).

VERDICT: REVISE
