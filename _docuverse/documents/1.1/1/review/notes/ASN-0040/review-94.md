# Review of ASN-0040

The mathematics here is sound. I checked the proofs of S0, B5, B5a, B6 (both directions), B7 (all three cases), B1, B10, B_fin, Bop freshness, B8, and B9, and worked the trace. The contiguous-prefix invariant (B1) — the one most often hand-waved — is proved completely across the m=0, m≥1, target-namespace, other-namespace, and frame-operation cases. B7's case split (length split / equal-length parents / unequal-length nesting parents) is exhaustive and each branch is discharged with actual work. Bop's freshness argument correctly covers the case where the candidate could already lie in s.B via *any* namespace, not just its own. No correctness defect found.

The remaining findings are residual meta-prose (this note carries `review-mode.anti-bloat`) and one scope item.

## REVISE

### Issue 1: B6(i) note ends with a back-reference that restates the proof
**ASN-0040, after the B7 proof (B6(i) load-bearing paragraph)**: "The T4-validity of p' (B6(i)) — forbidding a zero final component — is exactly the hypothesis the unequal-length case above relies on."
**Problem**: The aliasing counterexample (`([1,0],1)` vs `([1],2)`) in this paragraph is substantive — it demonstrates why B6(i) is necessary, with a concrete witness. But the final sentence adds nothing: it merely points back at the unequal-length case of the B7 proof and re-asserts what that case already established (T4 forbids a zero last component). This is the "two paragraphs say the same thing" / use-site back-reference pattern.
**Required**: Keep the counterexample; delete the closing back-reference sentence.

### Issue 2: S(p,d) contract embeds a proof sketch in the postcondition slot
**ASN-0040, S(p,d) Formal Contract, Postconditions**: "...`sig(cₙ) = #p + d`... (The sig identity holds because the ordinal n ≥ 1 occupies the final position #p + d, which is therefore the rightmost nonzero component.)"
**Problem**: A justification belongs in the proof body, not parenthetically inside the postconditions list. The inductive proof above already establishes `sig(cₙ) = #p + d`. The parenthetical is essay content in a structural slot.
**Required**: Remove the parenthetical from the contract; the proof already carries it.

### Issue 3: B4 and Bop cross-defer their content
**ASN-0040, B4**: "baptize(p, d)(s) = s', where the registry update `s'.B` is the action specified by Bop below." **ASN-0040, Bop**: "ATOMIC: B4."
**Problem**: B4's stated postcondition forward-defers the registry action to Bop, while Bop defers atomicity back to B4. Neither states its own claim self-containedly. B4's actual content (single Σ-edge, no intermediate observable state) is self-contained in its prose, so the contract line need not borrow Bop's `s.B ∪ {next(...)}`.
**Required**: Make B4's contract assert only the one-edge/no-intermediate-state property; let Bop state the registry postcondition outright and cite B4 only for atomicity.

## OUT_OF_SCOPE

### Topic 1: B3 (Ghost Validity) constrains content storage
**Why out of scope**: Content storage and the `Occupied` predicate are deferred (scope list: "content storage and retrieval"). B3 is carefully framed as a *forward requirement* on the future content-storage ASN rather than a definition, which is a defensible device — but the formal obligation `Occupied(t,s) ⟹ t ∈ s.B` is a claim about content storage and should live in (or be re-derived by) that ASN. The ghost-element motivation can remain here informally; the formal predicate and constraint belong downstream.

### Topic 2: S1 (StreamPrefix) has no consumer in this ASN
**Why out of scope**: S1 is proved but not cited by any later proof here (B7 uses the S(p,d) element form directly). It is a natural property a downstream ASN (e.g., ownership or subtree containment) may need, so it is not an error — just note that nothing in ASN-0040 currently depends on it.

VERDICT: REVISE
