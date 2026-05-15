# Review of ASN-0058

## REVISE

### Issue 1: ContentReference's implicit preconditions through "T12 holds"

**ASN-0058, ContentReference Definition (Resolution section)**: "(ii) T12 (ASN-0034) holds"

**Problem**: The shorthand "T12 holds" implicitly asserts T12's preconditions Pos(ℓ) and actionPoint(ℓ) ≤ #u, which are load-bearing throughout the resolution proofs. C0's proof silently relies on Pos(ℓ) — it cites "ActionPoint's postcondition (ASN-0034) gives 1 ≤ actionPoint(ℓ) ≤ #ℓ", but ActionPoint's postcondition requires Pos(t) as a precondition. A downstream consumer building on ContentReference must follow the chain ContentReference → T12 → Span definition to determine what they must verify of σ. Other preconditions (i, iii) are stated explicitly; (ii) is the lone outlier.

**Required**: Either (a) replace clause (ii) with the explicit preconditions: "Pos(ℓ), actionPoint(ℓ) ≤ #u", removing the T12 indirection (T12's postconditions are then derivable rather than asserted); or (b) keep "T12 holds" but add a parenthetical: "(equivalently: Pos(ℓ), actionPoint(ℓ) ≤ #u)".

VERDICT: REVISE
