# Review of ASN-0053

This is a mature, largely rigorous ASN — the foundation discharges (WR, S5, S9) are careful and the worked examples are concrete and correct. I verified the major proofs (WR's D2 discharge, S1/S3/S4 constructions, S5's TA-assoc/TA-LC chain, S9's six-case exhaustiveness, S11d's table) and found them sound. The findings below are isolated.

## REVISE

### Issue 1: S7's exact-representation impossibility is argued on the wrong axis and the characterization is misleading

**ASN-0053, S7 (*CoveringExistence*), "Why exact representation fails in general"**: "For any P that is not itself a union of subtree-convex intervals (in particular any finite P containing an isolated position with deeper interior points), no span-set denotes P exactly; the inclusion ⟦Σ⟧ ⊇ P is the strongest finite guarantee available."

**Problem**: Every span denotes an **infinite** set. For any span (s, ℓ), the proper deeper extensions s.0, s.0.0, s.0.0.0, … all lie strictly between s and reach(s, ℓ): each agrees with s on positions 1..#s and at k = actionPoint(ℓ) ≤ #s has component sₖ < sₖ + ℓₖ = reachₖ, so each is < reach and > s (prefix). There are infinitely many. Hence ⟦Σ⟧ is infinite for every non-empty Σ, and **no** non-empty finite P can satisfy ⟦Σ⟧ = P — the obstruction is the finite-vs-infinite mismatch, not subtree-convexity.

The given characterization obscures this. "Subtree-convex intervals" are themselves infinite, so *no* finite P is ever a union of them; the qualifier "P that is not a union of subtree-convex intervals" silently covers all finite P while the prose presents it as a special class. Worse, the parenthetical "in particular any finite P containing an isolated position with deeper interior points" implies the failure is specific to isolated positions — but by T0(b) *every* tumbler has deeper interior points, so this condition holds for every non-empty finite P. The reader is led to believe some finite configurations are exactly representable; none are.

The singleton sub-argument (reach ≠ t.0) is correct but proves only that {t} is unrealizable, then asserts the general claim. This is the "by similar reasoning" gap — the general statement is stronger than what is shown and is framed imprecisely.

**Required**: Replace the subtree-convexity framing with the direct fact: span denotations are infinite (every span contains the infinitely many proper deeper extensions of its start below its reach), so no non-empty finite P is exactly representable. Drop the misleading "union of subtree-convex intervals" / "isolated position" characterization, or restate it precisely.

### Issue 2: WR notation slip

**ASN-0053, "The reach function" / WR**: "So start ⊕ width determines reach (by definition of ⊕), and start ⊕ reach determines width (by D2)."

**Problem**: "start ⊕ reach" is meaningless — reach is a position, not a displacement, and the recovery is reach ⊖ start (precisely what WR states). The first clause is correct; the second abuses ⊕ where it means "start and reach jointly determine width."

**Required**: Write "start and reach determine width (by D2, via reach ⊖ start)."

### Issue 3: Motivational meta-prose around the S6 definition (anti-bloat)

**ASN-0053, S6 (*LevelConstraint*)**: "This equal-length condition recurs throughout the algebra, so we name it now."

**Problem**: This sentence explains *why* the definition is introduced rather than advancing its content — the anti-bloat pattern "prose around a definition explains why it is needed rather than what it says." The recurrence is self-evident from the subsequent uses.

**Required**: Delete the sentence; the definition stands on its own.

## OUT_OF_SCOPE

### Topic 1: Cross-level intersection and split at finer hierarchical levels
The level-uniformity precondition pervading S1, S3–S5, S8, S10, S11 excludes cross-level spans. The ASN correctly defers this (Open Questions on cross-level intersection and finer-level split points). Not an error here — it is properly scoped future work.

VERDICT: REVISE
