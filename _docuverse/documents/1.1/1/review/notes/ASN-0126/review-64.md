# Review of ASN-0126

I worked through the gate construction (`→_sh`, `K.λ_sh`), the registry component and P1, the wp refinement of ASN-0086's Case 2, the projection bridge, and P3/P5/P6 with their inductions, and re-ran the worked illustration (addresses, `a_emit` chain, the born-nullified landing failure). The substantive machinery is sound: the frame transfer of R-Scope is valid (the wrapper and Nullify reproduce the same `dom(Σ'.L)`, and R-Scope's conclusion reads only that set and `a`'s subtree), the wp `K registered ∧ Sh-conf ∧ d ∈ dom(Σ.M) ∧ C2 ∧ C3` is correct, RegisteredAdmissible correctly transfers non-emptiness from `K_j` to `K` via coverage, and the worked born-nullified scenario checks out (C3 false at `Σ₁` because `g ∈ coverage(G_rng)`).

One issue, squarely in this note's anti-bloat scope.

## REVISE

### Issue 1: The Single-source frame argument re-derives the very intersection it commits to not re-deriving

**ASN-0126, Single-source (final sentence)**: "The argument is uniform across both branches of R-Scope's disjunctive P-tgt — `a ∈ A_rel^Σ` (P1) and the self-emit `a = a_emit(Σ, d_retr)` — since the post-state domains coincide whichever target `a` is named: in the self-emit branch the fresh emitter *is* `a`, so `a` enters `dom(Σ'.L)` as its own witness, while R0a (FlatLinkDomain) places every pre-existing link address off `a`'s subtree, leaving the intersection the singleton `{a}` there too."

**Problem**: Two sentences earlier the note commits to transferring R-Scope "by a frame argument simpler than re-deriving the intersection," and the frame argument it gives is already complete and target-independent: the wrapper and Nullify call `a_emit` on the same `(Σ, d_retr)`, `a_emit` is blind to F (and to the target), so both yield `dom(Σ'.L) = dom(Σ.L) ∪ {a_emit(Σ, d_retr)}`, hence the same `A_rel^{Σ'}`; R-Scope's conclusion reads only that set and `a`'s subtree, so it transfers. R-Scope is a foundation lemma already stated and proven for Nullify over *both* P-tgt branches (it quantifies over "`a ∈ A_rel^Σ` (P1) *or* `a = a_emit(Σ, d_retr)` (self-emit)"), so the self-emit branch needs no separate handling.

The final sentence nonetheless re-derives R-Scope's conclusion in the self-emit branch — "`a` enters `dom(Σ'.L)` as its own witness ... R0a places every pre-existing link address off `a`'s subtree, leaving the intersection the singleton `{a}`." That is exactly the intersection re-derivation the method was chosen to avoid, and it duplicates R-Scope's own internal argument. It reads as content carried over from the pre-revision "R-Scope transfer derivation" that the frame argument was meant to replace, rather than removed.

There is also a mis-attachment: the lead-in promises that "the post-state domains coincide whichever target `a` is named" — a target-independent fact, already secured by `a_emit`'s blindness to the target — but the payload after the colon instead argues that the *intersection is `{a}`*, a different proposition that R-Scope already supplies.

**Required**: Delete the final sentence. The two preceding sentences already discharge both P-tgt branches uniformly, since R-Scope (foundation) covers both branches for Nullify and the wrapper reproduces `A_rel^{Σ'}` regardless of which target is named. If a one-line branch-uniformity remark is still wanted, state only that `a_emit(Σ, d_retr)` does not depend on the target `a`, so the post-state link domain is identical across both branches — without invoking R0a to re-establish the singleton intersection.

VERDICT: REVISE
