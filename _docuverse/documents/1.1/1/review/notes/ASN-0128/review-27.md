# Review of ASN-0128

The technical core held up under checking: I0a's two inclusions, I1a's induction (including the K ~ R case), I6's wp in both directions and both idem flags, DR's C3-emptiness derivation (distinctness plus R0a antichain at the constructed post-state), the hit-branch re-establishment of single-tuple scope, BH2's termination bound, the D2/D3 bridge at F-denoting states, and the example section's scenarios all verify against the cited foundations and transfer clauses (RP-a/b/c applied at the correct strength in each case). The remaining issues are the forward-reference accretion this note's classifier flags: duplicated convention statements and rationale previews that a reader must skip past to follow the claims.

## REVISE

### Issue 1: The unmarked-selector convention is stated four times
**ASN-0128, View selection / Default predicates / D1 / D3**: View selection commits "a call that omits the selector reads `default`." The Default predicates preamble restates it — "the unmarked forms denote the `default` reading note-wide, given by BH1's Rewrite scope" — D1 restates it again ("the unmarked call `members(K)` reads `default` (View selection)"), and D3 restates it a fourth time ("executed at the surface, where an unmarked call reads `default` (View selection)").
**Problem**: One sentence of convention, four statements across two sections. The preamble's and D1's instances are pure restatement-with-citation; the preamble additionally re-defers to BH1's Rewrite scope for content View selection already pinned. This is the "same thing in different words" accretion pattern, compounded across three sites.
**Required**: State the convention once, in View selection. The Default predicates preamble and D1 cite "(View selection)" without re-deriving the rule. D3 keeps only its load-bearing content — that the unmarked composition is a *different* query — which needs the citation, not the restatement.

### Issue 2: Two forward deferrals to "The exposed signature" restate its content
**ASN-0128, AD / Idem operational semantics preamble / The exposed signature**: AD states "the exposed `Emit_K` takes F and G as finite address sets and deposits their encodings (the exposed signature, Idem operational semantics)"; the idem-section preamble states "Throughout, a surface call presents its content as finite address sets, and `F, G` name their canonical encodings (`enc`, AD) — the exposed signature below fixes the type"; The exposed signature then defines the same fact in full ("a partial operation presenting `(d, X_F, X_G)`, whose emitted endsets are the canonical encodings...").
**Problem**: The surface's address-set presentation is stated three times, two of them deferring forward to the third — the "multiple paragraphs in different sections defer to the same downstream location" pattern named by the anti-bloat pass. The reader encounters the encoding fact twice as preview before reaching its definition.
**Required**: One full statement at the definition site (The exposed signature, or AD if the encoding is deemed AD's property). The other two sites carry a bare citation, not a restatement of the signature's content.

### Issue 3: I0's closing sentence duplicates its own opening rationale and previews I1's
**ASN-0128, I0**: "We reject the finer criterion on that property, taken together with I1's pricing of what coverage-keying then suppresses: the resolution it would add distinguishes tuples no argument can select between, while the suppression it costs is explicit in I1's hit clause and avoidable at the source by irredundant presentation."
**Problem**: The same paragraph already states, before the case analysis, "but under it the active subset could hold coverage-equal tuples that no argument selects between" — the closing sentence repeats this verbatim in substance ("tuples no argument can select between"). It additionally imports I1's suppression-cost-and-avoidability content, which I1's hit clause then states in full ("and the loss is avoidable at the source: where emitters present coverage-irredundant address lists..."). The rejection rationale is thus stated twice inside I0 and the avoidability point twice across I0 and I1 — relocated rationale rather than advanced argument.
**Required**: Keep the rationale, state each half once: I0 closes with the case analysis's own conclusion (argument-blindness of the matching surfaces) plus a single citation to I1 for the cost side; the irredundant-presentation avoidability analysis lives only in I1's hit clause.

## OUT_OF_SCOPE

### Topic 1: Specification of the serializing authority
I4 presupposes "a serializing authority orders the two calls before either becomes a step" and analyzes the resulting interleavings correctly. What that authority is — admission control, fairness, whether the dedup check and the step it guards are atomic with respect to other writers — is unspecified.
**Why out of scope**: `→_sh` inherits ASN-0086's sequential model by construction; a concurrency model is new machinery, not a gap in this note's per-interleaving analysis, which is complete on its own terms.

### Topic 2: Mid-batch observability of `retract_stale`
BH4 fixes the stale set at batch entry, permits interleaving, and shows every constituent is admitted. What an interleaved `Observe_K` sees mid-batch, and whether batch-level atomicity is ever a substrate obligation, is not addressed.
**Why out of scope**: the note explicitly commits the batch as a step sequence, not an atomic operation; isolation semantics over multi-step surface operations are a successor's territory.

VERDICT: REVISE
