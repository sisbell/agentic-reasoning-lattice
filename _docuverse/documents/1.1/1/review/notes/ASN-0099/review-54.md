# Review of ASN-0099

## REVISE

### Issue 1: Meta-lemma overview mis-assigns F19's dependency, contradicting F19's own derivation

**ASN-0099, "Determinism and Comprehension Invariance" (the paragraph naming instances of ComprehensionInvariantUnderΣL)**: "F17 and F19 invoke ComprehensionInvariantUnderΣL against the substitution Σ' = post-state of a transition preserving Σ.L. F11 and F19-filt instead invoke the per-link primitive, since their hypotheses supply only per-link value preservation rather than full Σ.L = Σ'.L."

**Problem**: F19 (ResultSetMonotonicity) is quantified over *every reachable* `Σ →* Σ'`, and reachable sequences may contain K.λ steps that grow `dom(Σ.L)`. The meta-lemma ComprehensionInvariantUnderΣL requires `Σ.L = Σ'.L` (it explicitly opens the comprehension over a *shared* index set `dom(Σ.L) = dom(Σ'.L)`), which fails exactly when K.λ fires. So F19 *cannot* invoke ComprehensionInvariantUnderΣL. This is internally contradicted twice over: (i) F19's own stated derivation is "Direct from F11 + the definition of findlinks" — i.e., the per-link route, not the meta-lemma; and (ii) F19-filt, which carries the *same* reachable-sequence quantifier as F19, is correctly placed in the per-link group in the very same sentence, with the very reason ("only per-link value preservation rather than full Σ.L = Σ'.L") that applies equally to F19. The grouping "F17 and F19" appears to be a slip for "F17 and F18" (F18, ScopedSurvivability, is across an atomic K.μ-family step that genuinely preserves Σ.L).

**Required**: Move F19 from the ComprehensionInvariantUnderΣL group to the per-link (PerLinkInvarianceUnderValuePreservation) group alongside F11 and F19-filt, and replace "F17 and F19" with the operations that actually preserve `Σ.L` across the cited substitution (F17 and F18). Confirm the corrected text is consistent with F19's "Direct from F11" derivation.

## OUT_OF_SCOPE

### Topic 1: Semantics of querying with I-addresses outside dom(Σ.C) ∪ dom(Σ.L)
**Why out of scope**: `findlinks(I, Σ)` is total over `I ⊆ T` as a comprehension, but the *intended* meaning of ghost-I queries is a separate concern. The ASN correctly defers it to Open Questions rather than over-specifying here.

META: not applicable — the ASN defines abstract state operations (the FINDLINKS comprehension), a conformance contract, and invariance/monotonicity guarantees, staying within system-guarantee territory and explicitly leaving mechanism unspecified.

VERDICT: REVISE
