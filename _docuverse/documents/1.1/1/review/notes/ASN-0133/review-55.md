# Review of ASN-0133

I worked through every proof — Q0's view-rewrite (the four view-parameterized atoms, the six UV-rewritten collections, the `elems(chain)` route, the value-preservation at Σ\*), Q-EXT's at-most-once, Q5's injection, Q5a's union bound and its open/closed asymmetry, and Q6's three obstruction cases and the H-SFAIR closure. The technical core is sound; the heterogeneous-rewrite worked example computes correctly, and the cmt/res registry's acyclic-coupling argument holds. Two findings.

## REVISE

### Issue 1: H-FIN is declared as a hypothesis and then never used — the bridge from "finitely many real fires" to operational halting is never drawn

**ASN-0133, RG (declaration) / Q6 / Worked composition**: RG bolds "**(H-FIN, fire finiteness.)** *Every* `Post_ρ`-satisfying emission set is finite — equivalently, every admissible fire's *step run* (its own `→_sh` steps) terminates." The worked composition then concludes "the registry's real fires are finite, its *work* terminates," and Q6's package list states "the package makes the registry's *work* finite."

**Problem**: H-FIN appears exactly once — at its declaration — and is cited by no subsequent claim. The termination results bound only the *count of real fires* (Q5: ≤ |W(σ)|; Q5a: ≤ Σ_ρ|⋃_k[D_ρ]|; Q6: a last real fire at index N). But a finite fire-count entails that the registry actually halts — reaches the inert tail in finite time, executes finitely many `→_sh` steps, emits finite work — only if *each* fire is a finite step run, which is precisely H-FIN. Without it, a single atomic fire (H-ATOM) could be an infinite step run, and σ would stall at it with a finite real-fire count yet the registry never reaching N. So Q6's "last real fire at index N," the worked example's "its *work* terminates," and Q6's "makes the registry's *work* finite" all silently consume H-FIN. The omission is conspicuous because H-FIN's sibling H-ATOM *is* invoked repeatedly ("atomic against environment interleaving (H-ATOM)," "trivially atomic by H-ATOM") — one of the two fire-level hypotheses is load-bearing in the prose, the other invisible, though H-FIN is exactly the premise the operational conclusion rests on.

**Required**: Where "work terminates"/"work finite" / "inert tail past N" is concluded, draw the H-FIN step explicitly — e.g., "by H-FIN each real fire is a finite step run, so finitely many real fires reach the inert tail in finitely many `→_sh` steps." Alternatively, if H-FIN is meant only as a well-definedness condition on *fire* (a fire *is* a finite step run by RG's own phrasing), say so and confine the conclusions to fire-counts rather than operational halting — as written, the "work" claims outrun their cited premises.

### Issue 2: minor meta-prose accretion (anti-bloat classifier)

**ASN-0133, SC / Q6 proof closing**: The note is largely clean on this axis, but two fragments are removable.

**Problem**:
- **SC**: "The three canonical bodies below satisfy it by construction (...), so the constraint costs the vocabulary nothing; Q9 is where it does its work." The clause "costs the vocabulary nothing; Q9 is where it does its work" is a defensive reassurance plus a forward pointer that adds nothing to the S-monotonicity definition itself.
- **Q6 proof, final sentence**: "...only a further hypothesis... *reaches and holds* quiescence over a non-grow-only domain, **case (2) reaching one unaided but unable to hold it, case (3) reaching none**." The bolded tail restates verdicts already given verbatim in each case's own description ("quiescence *is reached*... but not *held*"; "quiescence is *not reached*"). The "re-entry at top level (Q1), all-SF stops neither" framing earns its place; the per-case re-statement does not.

**Required**: Trim the SC reassurance/forward-pointer and the per-case restatement in the Q6 proof's closing sentence.

## OUT_OF_SCOPE

The deferrals — scheduler construction, the serialization that discharges H-ATOM, the turn/serialization model H-SFAIR's satisfiability needs, stochastic bodies, activation/governance, the environment/workload model, and the five open questions — are correctly placed at the protocol/implementation layer above the substrate. No in-scope topic is wrongly deferred, and the note specifies system guarantees (the recognizable `quiescent_R ∈ PL` predicate, the conditional termination theorems) abstractly rather than drifting into mechanics.

VERDICT: REVISE
