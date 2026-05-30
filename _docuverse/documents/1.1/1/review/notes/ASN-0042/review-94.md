# Review of ASN-0042

The mathematics is sound — I checked O2 (longest-match well-definedness), O3/O8 (refinement and irrevocability), O6 (account-field determinacy), O10 (unilateral fork), and the NestingByDelegation/PrefixBaptismCoupling inductions, and each discharges its conjuncts with genuine case work and a concrete worked example. The findings below are the bloat/reviser-drift patterns the `review-mode.anti-bloat` classifier asks for, plus one clarity defect that is a real readability hazard.

## REVISE

### Issue 1: Gap-numbered delegation conditions with edit-history justification
**ASN-0042, O15 (PrincipalClosure)**: "The condition labels (i)–(iv), (vi), (viii) are preserved from an earlier formulation in which the now-removed (v) and (vii) appeared; the gaps are intentional, since downstream proofs cite these labels."
**Problem**: Non-sequential labels `(i),(ii),(iii),(iv),(vi),(viii)` are a reviser-drift residue (git history shows (v)/(vii) were absorbed into (viii)), and the sentence documents the *edit*, not the spec. Separately, condition (iii) inside the existential (`π' ∈ Π_{Σ'} ∖ Π_Σ`) merely restates the outer quantifier's own restriction — a redundant slot kept alive only to preserve numbering.
**Required**: Renumber the six conditions (i)–(vi) sequentially, update the citations in O3, O7(c), O8, DelegatorAllocatesPrefix, and the NestingByDelegation proof, drop redundant (iii), and delete the gap-justification sentence.

### Issue 2: Consumer-inventory and "why-needed" prose in Definition (delegated)
**ASN-0042, Definition (delegated)**: "Condition (viii) is the single load-bearing structural gate: since next(Σ.B, p, d) = c_{hwm+1} ∈ S(p, d), B6 sufficiency discharges T4-validity of pfx(π'), and B1/B2 discharge freshness…" and "Condition (iv) … is genuinely needed and is not implied by (viii) — B6(iii) bounds only zeros(p) + (d − 1) ≤ 3."
**Problem**: The first enumerates what (viii) discharges for downstream consumers (a use-site inventory inside a definition); the second is a defensive "why this clause is needed" justification. Neither advances what the conditions *say*. The (iv)-necessity argument is correct (B6 admits `zeros(c_n) = zeros(p)+(d−1) ≤ 3`, so zeros could be 2) but belongs at most as a one-line parenthetical, not a labeled essay.
**Required**: State the six conditions plainly. Move the T4/freshness discharge into the single proof that actually uses it (DelegatorAllocatesPrefix and O7(a)); reduce the (iv) necessity to one clause or delete.

### Issue 3: Duplicated finite-path induction reassurance
**ASN-0042, State Axioms**: "Induction over reachable states does not require an external 'finitely many transitions' axiom — it is induction over the path length, which is by definition a natural number."
**ASN-0042, OwnershipDomainPermanence★ proof**: "composition of finite transition sequences yields a finite transition sequence."
**Problem**: The same proof-technique reassurance ("the path is finite, so induction is fine") is stated in two sections. Two paragraphs saying the same thing.
**Required**: State once (the reachability convention paragraph is sufficient); remove the restatement.

### Issue 4: Symbol-collision disambiguation parentheticals
**ASN-0042, OwnershipDomain definition**: "(the principal argument distinguishes this from T10a's allocator dom(A), which enumerates a per-stream chain {tₙ : n ≥ 0})."
**ASN-0042, Notation**: "(B0 of ASN-0040, not T8's allocator-domain monotonicity)."
**Problem**: Defensive notation-disambiguation that does not advance any claim; the foundation symbols are already distinguished by name and arity. This pattern recurs (the script-𝒮 vs S note is inherited from the foundation, but these two are introduced here).
**Required**: Drop or compress to a bare symbol reference.

### Issue 5: Implementation evidence narrated three times with a back-pointer
**ASN-0042, O6 Structural Provenance**: "read directly by tumbleraccounteq (the lockstep mantissa walk described under O1a)."
**Problem**: The `tumbleraccounteq` lockstep mantissa walk is described at O1, re-described at O1a, then deferred to at O6. Implementation evidence is legitimate content, but the same mechanism narrated three times — with O6 pointing "described under O1a" — is duplication plus a deferral.
**Required**: Describe the decision procedure once (at O1); later sites cite the source without re-narrating the algorithm.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer reconciling provenance (O6) with effective owner (O2)
**Why out of scope**: The ASN correctly excludes transfer (no codebase mechanism) and logs it as an Open Question; the divergence of inalienable provenance from effective ownership is genuinely new territory, not a defect here.

VERDICT: REVISE
