# Review of ASN-0058

## REVISE

### Issue 1: M12 introduction carries a dependency inventory that does not advance the proof
**ASN-0058, M12 (CanonicalUniqueness), introductory paragraph**: "The proof factors into two sub-lemmas: M12a (...) and M12b (...). M12a's 'Equal starts' leans on M-int (TumblerIntervalCharacterization) for the structural reduction; M12b uses TumblerAdd's prefix-copy and unit-shift inversion directly."
**Problem**: The first sentence is a legitimate roadmap. The second is a use-site inventory: it enumerates which upstream lemmas each sub-lemma will invoke. M12a and M12b each cite their own dependencies at the point of use ("M-int applied with x = v₁...", "OrdShiftHom gives..."), so this advance listing carries no reasoning the reader needs before reaching those steps. It is the kind of forward-reference accretion the anti-bloat classifier targets.
**Required**: Delete the second sentence; keep the one-sentence factoring roadmap.

### Issue 2: C1a re-derives M7f's internal proof structure instead of citing it
**ASN-0058, C1a (RestrictionDecomposition), "Extension of M11/M12"**: "The proof carries over verbatim to any finite partial function f : T ⇀ T for which B1–B3 are interpreted with f in place of M(d): M7f's case-split on 0 ≤ k < n₁+n₂ discharges B3 for β₁ ⊞ β₂ using only B3 for β₁ and β₂ together with M-aux, and the B1/B2 argument depends only on V(β₁ ⊞ β₂) = V(β₁) ∪ V(β₂)."
**Problem**: The load-bearing claim is "M7f's verification depends only on B1–B3 and the definitions of V(β) and ⊞, hence generalizes to any f satisfying B1–B3." That claim is made in the preceding clause. The trailing rehearsal of M7f's case-split and B1/B2 argument reproduces M7f's proof internals — a use-site inventory of a cited lemma's structure. A reader can confirm the generalization by reading M7f; restating its skeleton here is redundant accretion.
**Required**: Keep the assertion that M7f's verification uses only B1–B3 and the block definitions (and therefore generalizes); drop the rehearsal of its case-split and B1/B2 mechanics.

## OUT_OF_SCOPE

### Topic 1: I-space discontinuity structure at canonical boundaries
**Why out of scope**: The Open Questions already flag this as future work (forward gap vs. arbitrary jump); it is new territory, not a defect in the present claims.

VERDICT: REVISE
