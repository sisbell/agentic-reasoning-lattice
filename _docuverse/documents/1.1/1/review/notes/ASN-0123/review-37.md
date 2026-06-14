# Review of ASN-0123

I checked the load-bearing proofs (SA, VN-B1, the `nextv` frontier identity, V-WF's two-clause composite discharge, V8's coverer-set equality, V9's structural O5(ii) maximality and the severance theorem, V9w's boundary-conditioned P4★ use, V10/G2's SA-closes-the-subtree argument, V13's J1★/J1'★ pinning) and the boundary cases (n=0 empty source, first fork, cross-owner first vs. later document, shared content with |A| < n). The reasoning is sound and the cases are covered; the foundation citations are used consistently and the cross-transition-system reproofs (VN-B1, V0-via-GlobalUniqueness, the PS registry-coverage bridge) carry their non-transfer justifications. I found no correctness, depth, or self-containment defect. The one finding is a prose-economy item the active anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: P-tier's annotation and V0 mutually defer while both restating the single-mint / node-tier-exclusion argument

**ASN-0123, The Operation (P-tier annotation) and V0**:

P-tier annotation: "P-tier is the operation's domain delimiter, well-formed because ω(d_src) is defined at every reachable state … its second the cross-owner fork, which falls on an account-tier forker alone (zeros(pfx(π)) = 1), holding the allocation to a single identity (V0). A node-tier non-owner … lies outside the domain: reaching a document from a node prefix would first baptize an intermediate account — a second permanent entity (P1), breaking the single-mint guarantee — so it must establish an account first…"

V0: "The count is exactly one in both branches: … the cross-owner branch's restriction to an account-tier forker (zeros(pfx(π)) = 1) makes its allocation a single document K.δ … — the node-tier path, lacking that namespace, is excluded from the operation's domain (P-tier)."

**Problem**: The "account-tier ⇒ single mint" and "node-tier excluded" content is stated in both places, and the two passages defer to each other in a loop — P-tier cites V0 for "single identity," V0 cites P-tier for "excluded from the operation's domain." The node-tier branch is then explained at paragraph length inside the operation contract's precondition slot, i.e. an excluded-case essay sitting in a structural slot, deferring downstream while restating the same conclusion. This is the "essay content in structural slots," "imagines a case the precondition already excludes," and "two paragraphs say the same thing while deferring to the same location" pattern compounded. (The neighboring clarifications in the same annotation — no source authority required, empty source admitted at n=0 — are legitimate statements of what the operation does and does not require; the finding is the node-tier/single-mint duplication, not those.)

**Required**: Let the count argument live once, in V0 (the FreshUnique claim that actually proves "exactly one identity"); reduce the P-tier annotation to a terse domain statement with a single reference to V0 for why the second disjunct is account-tier-only. The well-formedness note ("ω(d_src) defined at every reachable state") can be a parenthetical clause rather than a sentence.

## OUT_OF_SCOPE

None to add. I considered whether the cross-owner branch's identity allocation (a fresh document in π's `A_doc` namespace) drifts into CREATENEWDOCUMENT (ASN-0103) territory, but it is correctly retained here: it is Nelson's "versioning by inclusion" ([LM 2/32–2/40]), and the note specifies it as VERSION's cross-owner case rather than re-specifying document-creation-from-scratch — it consumes the document sub-allocator as a primitive only. The note's eight open questions already capture the genuinely deferred topics (concurrent-fork serialization, derivation-direction recovery, link-subspace carry-through, windowing).

VERDICT: REVISE
