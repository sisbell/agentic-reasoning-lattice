# Review of ASN-0086

The mathematics checks out. I verified R0a's two-case antichain argument, R-Scope's "unit-depth span covers a subtree but only `a` is a link address in it" reasoning, the wp derivations (both directions), CoverageEqualityDecidable's cell partition, and the entire five-step worked sketch arithmetic (`a₁ = 1.0.1.0.1.0.2.1` through `a₃ = …2.5`, zeros/element-field projections, coverage memberships). All correct. The findings below are noise/placement issues, which the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Nullify Rationale carries an implementation-mechanics walkthrough in a spec-rationale slot
**ASN-0086, Definition — Nullify, *Rationale***: "udanax-green's link lookup enforces this pre-existence boundary at the granfilade exact-match guard (`tumblereq`, `granf2.c:37`) … this mirrors `docreatelink`'s own allocate-then-lookup sequence (`createorglingranf`'s `insertseq` runs before the `findorgl` exact-match guard, so the just-allocated address satisfies `tumblereq` immediately)."
**Problem**: The abstract authority argument (Nelson's ownership scoping, the ownership-at-Σ vs. ownership-at-commit distinction) is legitimate precondition rationale and justifies the two P-tgt branches on its own. The udanax-green source-line walkthrough (`granf2.c:37`, `docreatelink`, `createorglingranf`, `insertseq`, `findorgl`) restates the same conclusion in implementation terms — it is a system guarantee being re-derived from implementation mechanics, which the reader must skip past to follow the P-tgt design. This is essay content in a rationale slot.
**Required**: Justify P-tgt's two branches from the abstract authority guarantee alone (the Nelson scoping is sufficient). Move the udanax-green correspondence to implementation notes if it must be retained.

### Issue 2: R0 proof narrates the foundation lemma's internal proof structure
**ASN-0086, R0 proof**: "and cites ASN-0093's freshness lemmas for the `dom(Σ.L) ∪ dom(Σ.C)` exclusion, **whose own proofs run the within-document / cross-document (T10) / cross-subspace (T7) case split this fact requires**."
**Problem**: The bolded clause describes how FirstEmissionFreshness/SubsequentEmissionFreshness are proved *inside ASN-0093*. That narration advances nothing in R0's proof — R0 only needs the lemmas' conclusions. Describing a foundation lemma's case split is the meta-prose pattern the classifier flags ("explains the foundation's internals rather than what is used").
**Required**: Cite the two freshness lemmas for the exclusion conclusion and stop; drop the description of their case structure.

### Issue 3: WP Case 1 re-derives R-Scope's scope conclusion rather than citing it
**ASN-0086, Weakest-Precondition Analysis, Case 1**: the "Reduction of the postcondition" paragraph plus the "*P1 branch*" and "*Self-emit branch*" bullets re-run the antichain mechanics — "`A_rel^{Σ'} = A_rel^Σ ∪ {e}`", "R0a's antichain at Σ' then gives `{a' ∈ A_rel^{Σ'} : a ≼ a'} = {a}`" — that R-Scope (SingleTupleScope) already establishes for exactly the P1 and self-emit branches.
**Problem**: The text itself states the weakest precondition "*coincides* with the operation's own precondition `P0 ∧ P-tgt`" and that "Both disjuncts fall under R-Scope," yet still walks the scope derivation per branch. The genuinely wp-specific content — non-redundancy of each disjunct (the ghost-target counterexample; the self-emit realizability) — is worth keeping, but the scope-equality mechanics duplicate R-Scope and force the reader through a second copy of the same argument.
**Required**: Cite R-Scope for `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` on each admissible branch; retain only the weakestness/non-redundancy argument that R-Scope does not supply.

## OUT_OF_SCOPE

### Topic 1: Concurrency, atomicity of Emit vs. Observe, and cardinality bounds on `nullified(Σ)`
**Why out of scope**: These are correctly posed as Open Questions. This note works in ASN-0093's sequential-atomic transition model (SequentialTransitionAxiom); a consistency model for concurrent Observe/Emit and structural ratio bounds on retraction are new territory for a future ASN, not defects here.

META: The ASN defines state (typed relations over the link store), operations (Emit/Observe/Nullify), and invariants (R0–R6) abstractly enough that any conforming implementation must satisfy them — it has not drifted; the single implementation-mechanics paragraph (Issue 1) is local prose, not a structural shift.

VERDICT: REVISE
