# Review of ASN-0075

## REVISE

### Issue 1: The "P4★ is boundary-only, discharged by D-BOUND" explanation is stated three times
**ASN-0075, D-EXH note / D-BOUND axiom / supplementary lemma**: D-EXH's "reachability hypothesis is load-bearing… discharged structurally at every SHOWDELETIONS invocation by D-BOUND below"; D-BOUND's "D-EXH's composite-boundary hypothesis is discharged at every invocation by D-BOUND, not by run-time verification…"; the supplementary lemma's "By D-BOUND, every SHOWDELETIONS invocation observes a composite-boundary pre-state, so the lemma's hypothesis is automatically discharged at every invocation."
**Problem**: The same fact — P4★ holds only at composite boundaries, and D-BOUND supplies that hypothesis — is restated in three sections. This is the anti-bloat "multiple paragraphs deferring to the same downstream location / saying the same thing in different words" pattern.
**Required**: State the boundary dependency once (at D-BOUND, the axiom that introduces it). At the use sites (D-EXH, supplementary lemma) cite D-BOUND in a clause, not a paragraph.

### Issue 2: D-BOUND axiom is wrapped in "why the axiom is needed" meta-prose
**ASN-0075, D-BOUND**: "This is a system-level discipline that mirrors Nelson's command-level statelessness, where each protocol command… The axiom is part of the operation's contract: D-EXH's composite-boundary hypothesis is discharged… not by run-time verification or by appeal to informal 'operational scope.'"
**Problem**: The axiom's content is "the pre-state is a composite-boundary state." The Nelson-statelessness analogy and the "not by run-time verification or by appeal to informal 'operational scope'" clause are protocol-rationale and defensive prose (reads as a response to a prior finding), not statement of what the axiom says.
**Required**: Reduce D-BOUND to its statement plus the single load-bearing consequence (it discharges D-EXH's hypothesis). Drop the statelessness analogy and the run-time-verification disclaimer.

### Issue 3: Forward references force the reader to scan downstream to follow the proofs
**ASN-0075, D-EXH ("by D-BOUND below"), wp section ("(D-OBS below)"), Foundation Recap ("The justification appears in §D-SUBSP")**
**Problem**: D-EXH (the second lemma) depends on D-BOUND, which is not defined until the operation section several pages later; the wp derivation depends on D-OBS, defined near the end. The proofs cannot be followed in document order.
**Required**: Order the document so a claim's premises precede it — D-BOUND before D-EXH, D-OBS before the wp computations — or inline the needed property at the use site. Forward "below" pointers are a symptom that the dependency order is inverted.

### Issue 4: D-ACT deferral paragraph enumerates downstream machinery the operation does not use
**ASN-0075, D-ACT**: "…the run-decomposition it would rely on — mapping blocks and their unique maximally-merged canonical form (ASN-0058, M11…, M12…), with contiguous same-origin grouping licensed by ASN-0058 (M16…) — and the span representation of each resulting run (ASN-0053, σ.denotation) are material for a span/bundle-algebra treatment, not for this operation spec."
**Problem**: This is a deferral that catalogues foundation claims (M11/M12/M16/σ.denotation) which the operation never invokes, purely to say "this belongs elsewhere." It is forward-reference accretion — it advances the argument no further than "the abstract output fixes only the set of I-addresses."
**Required**: Keep the one load-bearing sentence (packaging is a representation choice, not part of the contract). Delete the inventory of unused downstream machinery.

### Issue 5: The `subspace_I(a) = s_C` conjunct is redundant wherever it is guarded by `a ∈ dom(C)`
**ASN-0075, "The Three States of Content," D-EXH, DeletedFromAWithB/DeletedFromBWithA**: each predicate or set is guarded by "`a ∈ dom(C)` ∧ `subspace_I(a) = s_C`."
**Problem**: By ASN-0047's ContentAllocationSubspacePrecondition (every `a ∈ dom(C)` has `subspace_I(a) = s_C`), the second conjunct is entailed by the first. The D-EXH proof never uses it (it derives `subspace(v) = s_C` of the V-position from the L14/S3★ chain instead). A carried, never-discharged conjunct is noise.
**Required**: Either drop `subspace_I(a) = s_C` as derivable from `a ∈ dom(C)`, or state once (where the predicates are introduced) that it is implied by L0 and not repeated.

### Issue 6: D-DISCR's "Notational convention" inflates the bundling rules into rationale prose
**ASN-0075, D-DISCR notational convention**: "J0 is a composite-boundary coupling evaluated only between the initial and final states of a composite, so the K.μ⁺ need not immediately succeed K.α within the composite — other elementary steps may intervene — but it must lie in the same composite for J0 to be discharged at the boundary."
**Problem**: The histories need only the rule "K.α must be bundled with K.μ⁺/K.ρ in one composite (else J0 fails)." The elaboration about whether K.μ⁺ "immediately succeeds" K.α restates J0's evaluation semantics — already fixed by ASN-0047's ValidComposite★ — and does not advance the witness construction.
**Required**: Reduce to the single rule actually used by Histories 1–2 (the K.α/K.μ⁺/K.ρ bundling and the K.δ-account-precursor shorthand). Drop the re-derivation of J0's boundary-evaluation semantics.

## OUT_OF_SCOPE

### Topic 1: Multi-document families and third-document witnesses
The Open Questions on "more than two documents" and "deleted from both, current in a third" are correctly posed as future work; the binary asymmetric-pair operation is self-contained here. No action needed.

### Topic 2: Span-packaged / V-order-meaningful presentation of the output
Whether the deletion set admits a finite span presentation, and what witness V-order guarantees yield a meaningful reading sequence, is genuinely new territory (span/bundle-algebra over the output). Correctly deferred — see Issue 4 for trimming the in-spec deferral prose, but the topic itself is rightly out of scope.

VERDICT: REVISE
