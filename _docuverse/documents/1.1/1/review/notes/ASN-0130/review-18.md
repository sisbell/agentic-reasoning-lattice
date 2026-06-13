# Review of ASN-0130

The core machinery is sound. I checked the load-bearing proofs in detail — PR2's event-wise acyclicity argument (including self-reference exclusion via the dedup-miss condition and the unconstructibility of cycles), PR3a's expansion well-typing (the WT-α / WT-W / PC2-substitution induction discharges correctly, last-parameter-first, with the freshness provisos doing exactly the capture-avoidance work claimed), the PR0 and PR5a weakest-precondition derivations (the first-disjunct lift is genuinely correct — a standing tuple satisfies the state-predicate `POST-ref`/`POST-cert` independent of the call), the PR-SIG stratification (well-founded on first-registration order, independent of `sig`, so no circularity with PR2), and the boundary cases the rubric demands (empty `A_def`→cond (0); `k=0` closed terms; self/cyclic/frontier-ghost references→cond (iv) and PR2; born-nullified deposits; de-registered-but-evaluable definitions; view-dependent and non-Boolean certification refusals). I found no correctness defect.

The note carries the anti-bloat classifier, and the residual findings are all prose: meta-commentary and redundant restatement that a precise reader must work around.

## REVISE

### Issue 1: wp derivation justified by contrast with a discarded draft

**ASN-0130, PR0 (wp derivation)**: "This is the branch the unlifted `VALID ∧ (…)` form wrongly excluded — a call may fail validation (a referent since de-registered, condition (iv)) yet leave `a`'s own standing registration untouched, POST-ref true while `VALID` is false."

**Problem**: The clause "This is the branch the unlifted `VALID ∧ (…)` form wrongly excluded" specifies nothing about the system; it corrects a rejected formulation of the wp. This is the reviser-drift pattern — a prior correction absorbed as commentary rather than removed. The substantive content (a validation-failing call can leave a standing registration intact, so `POST-ref` holds while `VALID` is false) is what motivates lifting the first disjunct clear, and it stands on its own. PR5a inherits the same framing ("the already-certified disjunct likewise lifted clear of CVALID … the case a later de-registration of `a`'s `pdef` tuple realizes").

**Required**: State the first disjunct's rationale positively — the standing tuple satisfies the postcondition regardless of the call's verdict — and drop the reference to the "unlifted form."

### Issue 2: non-load-bearing historical excursion embedded in a normative claim

**ASN-0130, PR-VIEW**: "(Motivating precedent, not load-bearing — the derivation rests on PC3 alone: Xanadu's read side already puts scope in the reader's hands, in udanax-green every link query carrying its own scope, each specset naming its own document or version per call, historical versions queryable on the same footing as current ones, with no backend-held "current" substituted for the caller's choice, and link filtering likewise front-end work, the reader's sieve; the definition layer inherits that published-artifact semantics.)"

**Problem**: This is a multi-clause essay on udanax-green's read-side philosophy sitting inside the PR-VIEW view-transparency claim, with the author's own disclaimer that the derivation does not rest on it. It is essay content in a structural slot, and the commit history ("demote PR-VIEW motivating precedent") shows it was relocated to a parenthetical rather than removed — exactly the "relocated rather than removed" pattern. By its own admission it advances no reasoning, so demotion did not retire the cost; a reader still skips it to reach the load-bearing "the `view` argument is inert" claim.

**Required**: Remove the precedent. If a one-line motivation is wanted, "scope is the reader's, fixed per evaluation" suffices; the historical detail belongs nowhere in the normative text.

### Issue 3: PS2 re-characterizes ST⁺ already defined in PR5

**ASN-0130, PS2**: "Asserts **ST⁺** certification of the *expansion* … per-instantiation ⊤-stability under PD0's rules (ASN-0129) with PR5's parameter reading, a *sound superset* of literal PD0-ST (not literal ST-class membership), the two coinciding only at `k = 0`."

**Problem**: The "sound superset of literal PD0-ST (not literal ST-class membership), coinciding only at `k = 0`" property is PR5's content, re-derived here in the class-registration slot — two paragraphs saying the same thing. The `k=0`-coincidence point is stated three times total (PR5 main, PR5 *Parameters*, PS2). A DEF slot should state the convention (shape, idem, slot meaning, what the tuple asserts) and point to PR5 for the characterization, not restate it.

**Required**: Reduce PS2's assertion to "Asserts ST⁺ certification (PR5) of the view-independent expansion of the definition at `a`," and keep the sound-superset / `k=0` characterization in PR5 alone (stated once).

## OUT_OF_SCOPE

None. The note's own Open Questions (naming, cross-substrate portability, dangling live references, certificate classes beyond ST) and "What this note doesn't cover" (concrete byte encoding, activation, certifier internals) capture the genuine future territory; no additional deferral is needed.

VERDICT: REVISE
