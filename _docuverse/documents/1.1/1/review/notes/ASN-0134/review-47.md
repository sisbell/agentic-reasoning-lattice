# Review of ASN-0134

I checked the load-bearing proofs (A4, A6's reachability/transfer argument, H0/H1/H2's commute-conflict structure, G1(i) validity and G1(ii) confluence, H3's two-mode commutation, the §4 order-dependence families incl. G2, V2's strict-implication chain with both converse witnesses, and SAFE) and the worked addresses in §7 and the §8 trace. The technical content is sound — the per-home/global partition is correctly drawn, the step-vs-operation seam is honestly maintained, the boundaries (first-emission, empty stale set, m=0/m=1 batches) are covered, and the wp for clause 2 is non-trivial. The note is a consistency/isolation model stated as a contract over any realization, not implementation mechanics — so no META.

The findings below are anti-bloat (the note carries `review-mode.anti-bloat`): meta-prose accreted around forward references. None touches the substance, the Nelson/Gregory grounding, or the concrete examples.

## REVISE

### Issue 1: Use-site inventory announcing downstream consumers of the K.σ conditional
**ASN-0134, §4**: "we state the realization conditional **here, once**, for H3, clause 2, and SAFE(c) all to reference."
**Problem**: This enumerates downstream consumers (H3, clause 2, SAFE(c)) instead of advancing the conditional's meaning — the exact "definition's introduction enumerates downstream consumers" pattern. Worse, the "once" is not honored: H3 re-states the load-bearing half in both its statement ("per-account serialization rendering same-account creations ≺-comparable, so distinct creators hold distinct committed d") and its proof ("cross-account on a shared-frontier realization, distinct by construction on a collision-free one"). So the note announces a single statement site while spreading the statement across three.
**Required**: Drop the "for H3, clause 2, and SAFE(c) all to reference" clause. State the conditional once; let clause 2 and SAFE(c) cite it by their existing bare "(§4/H3)" pointers, and trim H3's restatement to a citation rather than a re-derivation.

### Issue 2: A6 defensive non-enumeration plus use-site deferral
**ASN-0134, §2 (A6)**: "We do not enumerate the package, because the argument does not turn on the roster… B2/RP-a carry *every* per-state stack invariant to 𝔼's states whether we name it or not… The conjuncts §2 actually leans on are re-cited at their use sites — P6 (ReachableConformance…) is the representative case."
**Problem**: The load-bearing argument is three clauses: every `Σ_k` is `→_sh*`-reachable (the prefix witnesses it), so by B2/RP-a every per-state invariant holds, and canonicity is single-state because each conjunct reads only `Σ_k` and the constant `R₀`. The rest — "we do not enumerate, because the argument does not turn on the roster," "whether we name it or not," "re-cited at their use sites," "representative case" — justifies the *structure of the proof* rather than proving anything, and a reader must skip it to reach the argument. The "re-cited at use sites" is itself a deferral.
**Required**: Keep the reachability⟹invariants step and the single-state (`Σ_k` + `R₀`) point. Cut the non-enumeration justification and the use-site deferral.

### Issue 3: Recurring meta-framing that justifies the note's own structure
**ASN-0134, multiple sites**:
- §9: "The reader who wants the one-sentence form of this entire note can take it from the wp:"
- §5: "W5 deserves a word, because 'audit/active-slice coincidence' is where one might fear a read could see a tuple that is both present and absent."
- §8: "It is worth grounding V2 once in an explicit trace, in §7's style, because the error it warns of is the note's subtlest postcondition, one a concrete trace makes checkable."

**Problem**: Each is a self-referential justification for the material that follows. The material is substantive and should stay — the one-line wp summary, the slice-coherence clarification, and especially the V2 trace (a concrete example the review standards require). But the framing talks *about* the note rather than advancing the claim, and is skippable noise.
**Required**: Present the wp summary, the W5 clarification, and the V2 trace directly; drop the "The reader who wants…", "deserves a word, because…", and "It is worth grounding… because…" framings. (This flags placement/framing only — not the trace or examples, which are correctly required content.)

## OUT_OF_SCOPE

No additional out-of-scope items. The note scopes its excluded topics correctly: scheduler/fairness, agent activation/rule bodies, inter-server/BEBE, the concrete mechanism, and predicate cost are all held in "What this note does not cover," and the cross-server-G1, weakest-exclusion-primitive, and reader-side batch-atomicity questions are held as Open Questions rather than asserted as claims. None of A0–SAFE strays into mechanism or scheduler territory — MIC is explicitly a contract, not an implementation.

VERDICT: REVISE
