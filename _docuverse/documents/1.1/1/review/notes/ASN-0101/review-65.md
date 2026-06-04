# Review of ASN-0101

This ASN is substantively rigorous. The core proofs — the containment-precondition reduction, D1's gap-closure bijection (TS1/TS2 generalised from `m=2` to arbitrary `m_S`), D8's three-group invariant coverage, the D11 weakest-precondition derivations, and the D10 induction over DEL-extended traces — are complete and correct. I checked D8's invariant list against ASN-0047's ExtendedReachableStateInvariants theorem: all 32 per-state invariants are accounted for, and the source-correspondence argument correctly handles the `Q ∩ X` re-mapping subtlety for S3★, S8★(c), CL-OWN, and CL-UNIQ. The three worked examples (content depth-3, link depth-2, cross-document transclusion) exercise the non-trivial clauses. The arithmetic in the boundary cases checks out.

My findings are confined to the meta-prose / forward-reference patterns the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Intra-claim navigation prose in D10
**ASN-0101, D10**: "The coupling constraints are treated immediately below; the boundary obligations are discharged for DEL-containing composites in the *Composite-boundary obligations* paragraph that follows." and, later, "We argue in two parts: DEL's neutrality, then the boundary derivation."

**Problem**: Both sentences are pure signposting — they announce the order in which the reader will encounter material they are about to read anyway. Neither advances the argument; a reader following D10 must skip past them. This is the navigation/deferral pattern the anti-bloat classifier targets.

**Required**: Delete both sentences. The "(1)…(2)…" enumeration and the "*Composite-boundary obligations.* / *Neutrality.* / *Boundary derivation.*" headers already structure the claim; the prose pointers are redundant scaffolding.

### Issue 2: D8 claim statement carries justification strategy and a forward deferral
**ASN-0101, D8 statement**: "…each universally quantified over every `d ∈ dom(M)` — for the modified document `d` they are preserved by a source-correspondence argument, and for every unmodified document `d' ≠ d` they are inherited pointwise from the pre-state by D5… The composite-boundary properties of ASN-0047 (P4★, P4a, P7a) are not per-state invariants… so DEL's effect on them is established at the composite boundary in D10, not here."

**Problem**: The claim statement should say *what* is preserved; *how* (source-correspondence, pointwise inheritance via D5) belongs in the justification, which already restates it. The "established … in D10, not here" clause is a forward deferral embedded in the statement slot — the same pattern as the LP-family deferral and the internal D10 pointers, compounding the signposting noise around the D8→D10 boundary.

**Required**: Reduce the statement to the invariant enumeration plus the exclusion of P4★/P4a/P7a as non-per-state (a one-clause fact, no "in D10" pointer needed). Move the per-group mechanism description into the justification where it is already given.

## OUT_OF_SCOPE

### Topic 1: Architectural-significance essay prose in D2–D7
Each of D2–D7 carries multiple paragraphs of architectural commentary (the destructive-replacement contrast, transclusion safety, the evolving-braid analogy). This is essay content sitting alongside structural claims, but it largely consists of statements of what the operation does or does not do (e.g., "DELETE frees no storage," "the link is unaware") and concrete contrasts — explicitly carved out from the meta-prose definition — and is consistent with the literate house style of the surrounding specification. Not flagged as bloat; noted only so the distinction is on record.

VERDICT: REVISE
