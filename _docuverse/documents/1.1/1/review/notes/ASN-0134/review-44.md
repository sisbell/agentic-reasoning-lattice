# Review of ASN-0134

This note's core mechanics — the frontier discipline (H0), the commutation/conflict pair (H1/H2), the per-home-serialization theorem (G1), the verdict-snapshot chain (V2 with its two strictness witnesses), and the worked §7 addresses — are genuinely rigorous, with careful boundary handling (max ∅ at the first-emission boundary, the cross-document-cross-subspace pair `CrossDocumentDisjointness` leaves unnamed) and concrete witnesses where the standard demands them. The findings below are one proof gap at the K.σ seam and a cluster of accretion the `anti-bloat` classifier asks be surfaced at source.

## REVISE

### Issue 1: K.σ-as-`A_doc`-emission is grafted across two state models, and the H0/H1/H2 carry-over is asserted, not derived

**ASN-0134, §4**: "So H0/H1/H2 carry over to `K.σ` *by the same argument* (with `A_doc`'s entity-allocation lemmas standing in for the content/link ones the proofs below cite), the **account as home** and `A_doc` its sub-allocator: two same-account creations read one `A_doc` frontier and collide on one document address by H2's argument one tier up, while creations under distinct accounts commute by H1."

**Problem**: This whole treatment rests on identifying K.σ with an `A_doc` emission, but four things stand against it.

1. **The committed stack's K.σ has no `A_doc`.** §1 commits 𝔼 to "ASN-0093's allocation model carried up through ASN-0086/0126/0128," step vocabulary `K = {K.σ, K.α, K.λ_sh}`. There, K.σ's precondition is bare freshness-by-test — `d ∉ dom(M) ∧ T4-valid(d) ∧ zeros(d) = 2` (ASN-0093 K.σ) — and there is *no* document-allocator-conformance invariant (the stack carries C1c/L1c for content/links but no document analogue). A registered document need not lie on any `A_doc` chain; bare freshness-by-test admits gaps (`d = [1.0.1.0.5]` with `[1.0.1.0.1..4]` absent), which `A_doc`'s contiguous discipline forbids.

2. **`A_doc` lives in a different model.** `A_doc` is ASN-0047's, whose emission operation is K.δ (entity creation into `E_doc`), *not* K.σ. K.δ is not a step of 𝔼, and the committed stack has no entity set `E`. "K.σ is itself a sub-allocator emission... emitted by the account's document sub-allocator `A_doc`" therefore equates an operation of 𝔼 (K.σ → dom(M)) with an operation of a foreign model (`A_doc`/K.δ → `E_doc`), justified only by "Gregory confirms the mechanism is literally the same."

3. **The account-tier collision is an `A_doc` artifact.** "two same-account creations read one `A_doc` frontier and so compute the same document address, a forced collision one tier up" holds only under `A_doc`'s compute-from-frontier rule. Under the committed K.σ's freshness-by-test, two agents need not compute the same `d` at all — they can propose distinct fresh document addresses and never collide. The forced same-address collision H2-one-tier-up depends on, the contract then leans on, does not arise from the operation 𝔼 actually runs.

4. **The carry-over is one sentence for a multi-step obligation.** "by the same argument... `A_doc`'s entity-allocation lemmas standing in for the content/link ones the proofs below cite" names no lemma. The H0/H2 proofs cite specific ASN-0093 lemmas (`ChainMembershipForOrigin`, `FirstEmission`, `SubsequentEmissionFreshness`, `FirstEmissionFreshness`); their `A_doc` counterparts are neither identified nor checked to have the contiguous-prefix/frontier form the proofs require. Per the depth standard, "X carries over by the same argument" is a claim, not a proof.

This propagates: MIC clause 2's account tier, H3(b)'s "necessarily under a *different* account, since per-account serialization makes same-account registrations comparable," and SAFE(c) all inherit the unproven `A_doc` structure.

**Required**: Either (a) derive that the committed substrate's documents are necessarily `A_doc`-conformant — reconcile K.σ-into-dom(M) with `A_doc`-emission and name the ASN-0047 lemmas that discharge the account-tier H0/H2 in that model — or (b) state the dependence conditionally: K.σ's freshness mechanism is left open by ASN-0093, so the account-tier clause-2 obligation binds only realizations (Gregory's among them) that compute document addresses from a shared frontier; a collision-free document-address scheme incurs no such obligation. Option (b) is the honest one absent an amendment to ASN-0093.

### Issue 2: the account-tier H2/H1 claim is restated five times

The proposition "same-account K.σ collide on one `A_doc` frontier; distinct-account creations commute by H1" appears in:

- §4 ¶1: "two same-account creations read one `A_doc` frontier and collide on one document address by H2's argument one tier up, while creations under distinct accounts commute by H1";
- §4 ¶2: "under the `A_doc` realization two same-account creations read one `A_doc` frontier and so compute the same document address, a forced collision one tier up";
- H3: "a same-account `K.σ` reading the same `A_doc` frontier (the account-tier H2 collision...)";
- MIC clause 2: "the frontier-read-and-deposit of any two same-account creations are likewise mutually exclusive";
- SAFE(c): "two same-account `K.σ` steps collide on one document address exactly as two same-`(d, S)` allocations do."

**Problem**: The §4 ¶1/¶2 adjacency is the clearest waste — both assert the carry-over before ¶2 adds its only genuinely new content (the freshness-by-test rejection and its order-dependence). The H3/clause-2/SAFE recurrences are each in a proof/contract/safety slot where restating the operative fact is more defensible, but the source duplication is in §4.

**Required**: State the account-tier carry-over once (the consolidation Issue 1 will force anyway); let ¶2 open directly with the rejection-path content, and let H3/clause 2/SAFE cite the single statement rather than re-derive the collision.

### Issue 3: §4's two closing summaries recap the per-instance conclusions

After the three detailed analyses (instance (i), instance (ii), the target-residence race), §4 closes with two paragraphs — "The honest statement is therefore two-level..." and "Under discipline the three order-dependent instances part company exactly as their own analyses found them — the target-residence race excluded by emit-before-retract, instance (i)'s duplicate by the global per-coverage-class serialization..., instance (ii) reduced by neither, and surface-discipline reaching none."

**Problem**: Each instance's own analysis already states which discipline removes it (instance (i) → clause 7; target-residence → emit-before-retract; instance (ii) → neither) and that its governing read is global. The second closing paragraph is a verbatim-in-substance recap of those conclusions; the first restates the two-families/global-reads split already made in "the toggle is the general fact" within instance (ii). One consolidated summary discharges both.

**Required**: Keep one summary; delete the redundant recap.

### Issue 4: G0's claim statement carries a sequential-consistency essay

**ASN-0134, §3, G0**: "...With program order unconstrained across homes, SC degenerates to bare serializability here — and that degeneration *is* the per-home liberation of §4–§6 read as a consistency level, not a guarantee mislaid."

**Problem**: G0 is a claim slot, but its statement runs a multi-sentence SC excursion that forward-references G1 to justify itself ("G1 below frees every pair of ≺-incomparable cross-home steps...") and closes rhetorically ("not a guarantee mislaid," "read as a consistency level"). The load-bearing content — the order does not preserve one agent's *cross-home* program order, so an agent needing its own cross-home operations ordered must serialize them itself (A7) — is one sentence; the rest is defensive justification and framing in a structural slot.

**Required**: Reduce G0 to the serializability statement plus the one cross-home-program-order sentence; drop the rhetorical closers and the G1 forward-reference (G0 should not depend on a later claim to make its point).

### Issue 5: A6's invariant-taxonomy prose does not advance "every state is canonical"

**ASN-0134, §2, A6**: "ASN-0126's `P2` and ASN-0128's `R2` (shape- and idem-stability) are *cross-state corollaries* of registry-fixity, not single-state conjuncts... The chain-contiguity members hold at every state of `𝔼` by reachability — every valid step deposits at its home's `inc(max,·)` frontier slot, keeping each home's population a gapless prefix under any interleaving."

**Problem**: Two parts of A6's trailing prose do not advance its claim. (a) The P2/R2 "corollaries, not conjuncts" clause is a defensive justification for what the package *excludes* — it answers "why isn't shape-stability a conjunct?" rather than establishing canonicity. (b) The chain-contiguity-via-`inc(max,·)` re-explanation duplicates W3, which gives the same mechanism in full as an induction ("if `P_S(d, ·) = {slot 1, …, slot φ}` is a gapless prefix, the next `S`-allocation lands at slot `φ+1`"). A6 need only assert the chain-contiguity members hold (citing reachability + the transfer lemmas) and leave the mechanism to W3. (The transfer-lemma-per-class mapping later in the paragraph is load-bearing — it justifies that the foundations' invariants reach 𝔼's states — and should stay.)

**Required**: Drop the P2/R2 exclusion-justification (or compress to a parenthetical naming them as registry-fixity corollaries); replace the chain-contiguity mechanism gloss with a bare assertion deferring the proof to W3.

## OUT_OF_SCOPE

None to add. The note's own "What this note does not cover" and the Open Questions correctly defer reader-side batch atomicity (OQ4), durability-as-substrate-predicate (OQ5), cross-server composition (OQ6), static sub-allocator partitioning (OQ7), and out-of-order-retraction exposure (OQ8) without making claims for the listed out-of-scope topics.

VERDICT: REVISE
