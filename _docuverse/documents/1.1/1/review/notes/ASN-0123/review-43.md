# Review of ASN-0123

I checked the operation's realizability and every V-claim proof against the foundations. The technical content is sound: VN-B1's four-case induction is complete and the freshness/operand constraints are correctly traced; the cross-owner O5(ii) maximality theorem and the severance proof (V9) both close their branches; V-WF discharges ValidComposite★'s two clauses including the n=0 boundary; SA, V8's coverer-set equality, and V10's biconditional all hold; the two worked instances correctly verify V2/V13/V9w/V10 against concrete addresses, including the `|A| < n` shared-address case and the severance-vs-carry-through orthogonality. Boundary cases (empty source, first vs. subsequent version, node-tier owner, node-tier non-owner exclusion, iterated forks) are covered. No correctness defects found.

The note carries `review-mode.anti-bloat`, and the findings below are restatement patterns, not logic gaps.

## REVISE

### Issue 1: P-tier's domain semantics are stated twice in immediate succession
**ASN-0123, "The Operation" (precondition block and the dashed paragraph that follows it)**:

Inline annotation: *"P-tier ω(d_src) = π ∨ zeros(pfx(π)) = 1 (the operation's domain: the forker owns the source — served at any tier — or, forking across ownership, already holds a document-creation namespace; the identity clause branches on the same guard)"*

A few lines later: *"P-tier is the operation's domain delimiter ... its first disjunct serves the owned fork at any forker tier, its second the cross-owner fork, restricted to an account-tier forker ..."*

**Problem**: The domain-delimiter role and the meaning of both disjuncts ("owned at any tier," "cross-owner account-tier") are spelled out in the inline gloss and then re-spelled in the following paragraph. The inline note is not a label-then-detail setup; it already explains the disjuncts the paragraph re-explains. A precise reader reads the same content twice in one screen. (V0's later mention — "P-tier is what confines the operation to these two branches ... for the reason given there" — correctly defers rather than re-explains, so it is not part of this finding.)
**Required**: State the disjunct semantics once. Reduce the inline annotation to naming P-tier as the domain condition and let the paragraph carry the explanation (which alone adds the well-formedness note, the "mints exactly one identity" point, and the node-prefix exclusion).

### Issue 2: V2 and V5 each state their shared conclusion in full
**ASN-0123, V2 (the "Snapshot" gloss) and V5**:

V2: *"the version captures the source as it stands at the fork, which with V5's orthogonality means successive forks bracketing an edit hold different snapshots under consecutive ranks."*

V5: *"Two forks separated only by an edit of the source transcribe different snapshots (V2) yet take consecutive ranks; the address arithmetic never looks at the arrangement."*

**Problem**: The joint conclusion — *forks bracketing a source edit → different snapshots under consecutive ranks* — is stated in full in both places, each citing the other for the half it is borrowing. The cross-reference is correct; the duplication is that both also restate the whole conclusion.
**Required**: Have each claim assert only its own contribution (V2: the snapshot is fork-time; V5: rank is content-blind) and defer the composite observation to a single site.

## OUT_OF_SCOPE

(none — the note scopes itself cleanly; editing, comparison, link creation, delivery, and replication are touched only through frame conditions, and the open questions stake out future territory without smuggling in current gaps.)

VERDICT: REVISE
