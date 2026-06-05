# Review of ASN-0103

## REVISE

### Issue 1: First-case (empty account) version dominance is not established

**ASN-0103, "Effect One" — *Strict advance over every prior address under A*** and **CND.monotone**: "d strictly exceeds every document address ever baptised under A (document-chain emission or version), including never-populated ones."

**Problem**: The version-dominance argument is written exclusively for the *subsequent* case. It opens "Write `d = [A, 0, p]`," then derives `i ≤ p − 1 < p` from `d_i ≤ max(D_A) = d_prev = [A, 0, p−1]`. In the first case `D_A = ∅`, there is no `d_prev` and `max(D_A)` is undefined, so this entire chain of reasoning is unavailable. The only thing the ASN says about the first case is in the *Freshness* paragraph — "for the first emission `D_A = ∅`, so `d = inc(A, 2)` is the stream's first element and no document under A precedes it" — which concerns same-allocator (document-chain) ordering only and merely *asserts* (without justification) that "no document under A precedes it." For the broad reading where versions count as documents under A, this assertion is left unproven for the first case. This is exactly the empty/first boundary the review standard mandates checking.

**Required**: Add the one-line observation that closes the gap: if any version `v` existed under A, its root document `d_i = [A, 0, i]` (the bottom of the k=1 fork chain) would persist in E by P1 and hence lie in `D_A`, contradicting `D_A = ∅`. Therefore `D_A = ∅` ⟹ no versions exist under A, and first-case version dominance holds vacuously. State this explicitly so the first emission's `CND.monotone` conjunct (dominance over versions) is discharged, not merely asserted.

## OUT_OF_SCOPE

(none — the "Creation vs Forking" section discusses CREATENEWVERSION only informally for contrast and introduces no forking claims, so it does not violate the scope exclusion.)

Notes that do not rise to REVISE: the proof leans on transitivity of `≼` ("pfx(π) ≼ A ≼ d") which the Prefix foundation contract does not list as an explicit postcondition, but it is an immediate definitional consequence and does not require a separate lemma. The `D_A = E ∩ S(A,2)` reverse-inclusion proof, the length filter excluding versions, the cross-account uniqueness via B7/B8/GlobalUniqueness (correctly avoiding T10's unmet non-nesting premise), the worked example, and the full invariant discharge are all sound and appropriately rigorous.

VERDICT: REVISE
