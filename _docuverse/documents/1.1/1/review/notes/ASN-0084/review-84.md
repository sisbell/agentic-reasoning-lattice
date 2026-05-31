# Review of ASN-0084

I read this as a layered arrangement-rearrangement spec over the Strand Model (ASN-0036) and Tumbler Algebra (ASN-0034). I checked the operation definition, the well-definedness lemmas, the two permutation lemmas, referential integrity, the run-decomposition transformation, and traced all six worked examples against the postconditions.

## What I verified

**Operation is fully pinned down.** REARRANGE_K determines Σ' uniquely: C' = C (frame c), M'(d') = M(d') for d'≠d (frame b), dom(M'(d)) = dom(M(d)), and M'(d) is covered exactly once by R-EXT/R-P1/R-P2 (or R-S1–S3) plus R-FRAME(a). R-PIV/R-SWP discharge totality with the half-open interval tiling [p, p+w_β) ⊎ [p+w_β, …) closing at ord(c_{n−1}). Partiality is stated against R-PRE(K).

**Boundary cases are present, not hand-waved.** The standards demand empty/minimum/first/last; the ASN supplies them: minimum V_S(d) with w_α=w_β=1 and both exteriors empty (boundary example); empty-right-exterior dispatched via EXT-VAC with the c_{n−1} ≤ N+1 bound proved from R-PRE(iv); the three μ-displacement sub-cases (w_β>w_α forward, w_β=w_α fixed, w_β<w_α backward) each traced; and a non-S (link-subspace) position carried verbatim with T10 cross-group disjointness.

**The hard proof (R-BLK) holds.** Phase 1's "process cuts in index order = process against original B" argument is correct (left pieces lie below later cuts by CS2). The "Outside ⋃V(bₖ)" sub-case is correctly confined to c_{n−1} alone via steps (1)–(3). S8-uniq is reconstructed from bijectivity of π|_{V_S(d)} plus verbatim non-S carry, with cross-group disjointness from non-nesting prefixes [1,…]/[2,…] (T10). R-COMM's same-region precondition is genuinely discharged at every use (runs lie in one region after splitting).

**Foundation usage is consistent.** ord, truncated subtraction, and the singleton↔ℕ identification are defined locally and justified — the foundation exports neither a tail projection nor a shift-amount inverse, so this is not reinvention of TumblerSub (which returns a tumbler, not the displacement count). The depth-agnostic transfer of TS3 to I-address arithmetic in Split/Merge is correctly noted (Extended Associativity was framed for depth-2 V-positions; Split/Merge apply it to depth-3 I-addresses).

I could not find a missing case, an unproved conjunct, a circular dependency (R-NS reads π's non-S branch from the definition and gets M'=M from the frame — it does not prove what R-PPERM assumes), or a "by similar reasoning" elision. The anti-bloat patterns I looked for (use-site inventories, "why the clause is needed" essays, duplicate downstream deferrals, imagined excluded cases) are at most marginal here: R-CS3 is a genuine necessity lemma with a concrete counterexample (precedent: foundation T10a-N), the EXT-VAC and Width-positivity derivations are load-bearing for R-BLK and the boundary example, and the recently revised I-address paragraph advances the argument rather than restating it.

## OUT_OF_SCOPE

### Topic 1: Composition of rearrangements; k>4 cuts; canonical-partition recovery procedure
**Why out of scope**: These are new territory (multi-operation algebra, generalized cut classes, the merge-to-fixpoint procedure) and are already captured in this ASN's Open Questions, not defects in the present operation.

VERDICT: CONVERGED
