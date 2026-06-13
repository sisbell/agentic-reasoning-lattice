# Review of ASN-0132

This note specifies a counting operation that is, at its core, `|findlinks_FTT(q, Σ)|`. Most of it is consequence-derivation, and most of that is sound: CN-DEF's well-definedness, CN-LOC, CN-UNIT (all four units, including the careful J4 argument that forking allocates no link), CN-ENUM, CN-ZERO, CN-MONO's wp derivation, and the worked example all check out against the foundations. I verified the example's arithmetic (the `δ(8,8)` reach, `a₄`'s divergence above the upper bound at the document component, the singleton `nullified = {a₂}`, the home-set membership tests for `d₁` vs `d₂`) and it holds. The findings below are one internal contradiction and three prose items the anti-bloat classifier asks for.

## REVISE

### Issue 1: CN-RETRACT's prose contradicts CN-RETRACT

**ASN-0132, CN-RETRACT discussion**: "A count taken against the active view excludes the withdrawn link at once; a count that could be taken against a prior view, **or that scopes its home-set to a context that still holds the link, would still include it.**"

**Problem**: This contradicts the claim it explains. CN-RETRACT states a nullified link "contributes `0` to `countlinks_FTT(q, Σ)` for **every** `q`." The home-set `H` is a component of `q`. The counted set is `{a : a ∈ addressable(Σ) ∧ sat(a, q, Σ)}`; a nullified `a` is excluded by the `a ∈ addressable(Σ)` restriction *before* `sat` — and hence the home-clause `liftH` — is ever evaluated. No choice of home-set can re-include it: nullification is global (R6a never shrinks `nullified`; FL-RET excludes from every `q` forever), not per-document or per-context. The sentence appears to import CN-STAB's *true* statement — that a **non-nullified** reverse-orphaned link is still counted under a home-bounded `q` — into the CN-RETRACT setting, where the link is nullified and the statement is false. This is precisely the reviser-drift pattern: a paragraph imagining a case (home-set re-inclusion) that the operation's own definition (addressable-filtering before `sat`) already excludes.

**Required**: Delete the clause "or that scopes its home-set to a context that still holds the link." The "prior view" clause is salvageable (an earlier-state count *did* include the link); the home-set clause is not.

### Issue 2: CN-SNAP's implementation note asserts deferred federation semantics

**ASN-0132, CN-SNAP implementation note**: "In the distributed setting the same definition holds against whatever model of the store a server currently presents, so even absent any edit the number a server reports is the size of the satisfying set *as that server currently sees it*. The snapshot semantics of CN-SNAP is thus visible twice: across edits in time, and across the inevitable lag of a replicated model."

**Problem**: The ASN lists "replication and inter-server protocol (BEBE)" as out of scope and defers "What must a federated count guarantee across independently administered stores" to an explicit open question. This aside nonetheless makes a guarantee-flavored federated assertion ("the same definition holds against whatever model … a server currently presents"), pre-empting the deferred work in prose. It advances no in-scope reasoning about the count and reaches into territory the ASN itself says it is not settling.

**Required**: Trim to the in-scope point — the count is a function of whichever `Σ` is observed — and drop the replicated-model elaboration, leaving federation to the deferred ASN.

### Issue 3: Placement-justification and prompt-framing meta-prose

**ASN-0132, CN-SNAP**: "This is the right place to record what permanence does and does not cover, because the question invites the confusion."

**Problem**: This sentence justifies its own placement and references the prompt rather than advancing a guarantee — the meta-prose the anti-bloat mode targets. It is one instance of a pervasive essay-framing around "the question" ("the case the question presses hardest," CN-ORPHAN; "what the question asks last," cost section; "The three rulings the question presses hardest on," worked-example intro). The substantive content these sentences carry (permanence guarantees existence, not reported counts) is fine; the scaffolding is skippable.

**Required**: State the point directly ("Permanence guarantees what exists and can be found again; a count is recomputed per inquiry") and drop the placement-justification and prompt-referencing connectives.

### Issue 4: Resolution principle restated rather than referenced (minor)

**ASN-0132, "A remark on the request as given"** vs **CN-STAB caveat**: "Any discrepancy a reader perceives between two such requests lives in the resolution, never in the count" / "only a position-phrased re-resolution can appear to move the count, and that appearance is the request changing, not the link."

**Problem**: The same insight — apparent count change under re-phrasing is a resolution artifact, not a count/link change — is stated twice in different sections. The "remark" establishes the principle; CN-STAB's caveat re-states it instead of pointing back to it. Mild, but it is the named "two paragraphs say the same thing" pattern.

**Required**: Have CN-STAB's caveat invoke the already-established resolution principle by reference rather than re-deriving it in fresh words.

## OUT_OF_SCOPE

The deferred topics — the V-spec/address-set invariant, cross-inquiry concurrency, count caching, fragmentation-dedup, cost-asymmetry, and federated counts — are correctly carried as Open Questions rather than smuggled into claims. No additional future-ASN territory to flag; the scope boundary is well-matched (Issue 2 excepted, where prose crosses it).

VERDICT: REVISE
