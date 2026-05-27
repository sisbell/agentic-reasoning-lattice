# Review of ASN-0099

## REVISE

### Issue 1: ComprehensionInvariantUnderΣL cited at F11 and F19-filt where its stated hypothesis is not satisfied
**ASN-0099, Persistent Discoverability (F11 derivation)**: "LP13 ... supplies the multi-step per-link guarantee `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`. ComprehensionInvariantUnderΣL's chain then gives per-slot coverage equality at Σ and Σ'..."

**Same issue at F19-filt derivation**: "F19-filt follows from LP13 + ComprehensionInvariantUnderΣL applied to the filtered universal..."

**Problem**: ComprehensionInvariantUnderΣL is stated as the meta-lemma "If Σ.L = Σ'.L as partial functions, then [comprehension equality]." Its hypothesis is full extensional equality of the link store — both domain equality and per-link value equality on a shared domain. LP13 (UnconditionalLinkPersistence, ASN-0098) supplies only the per-link consequences (`a ∈ dom(Σ'.L)` and `Σ'.L(a) = Σ.L(a)` for the specific `a ∈ dom(Σ.L)`) — globally only `dom(Σ.L) ⊆ dom(Σ'.L)`, since K.λ steps in the reachable sequence `Σ →* Σ'` can grow `dom(L)`. The meta-lemma's stated hypothesis is therefore not satisfied at F11 and F19-filt.

The proofs are nonetheless sound. They use only the per-link chain: `Σ'.L(a) = Σ.L(a)` → component-wise tuple equality (L6) → per-slot endset equality → per-slot coverage equality (coverage determinism) → match-status equality (F1's existential structure for F11; filter-universal preservation for F19-filt). This per-link reasoning is the *tail* of the meta-lemma's derivation, applied per `a` rather than universally on `dom(Σ.L)`. The citation conflates the per-link substep with the meta-lemma's full hypothesis.

By contrast, F8, F9, F9-cor, F9★, F15, F17 cite the meta-lemma correctly — their contexts establish `Σ.L = Σ'.L` from A1 or from a determinism hypothesis on the query. Only F11 and F19-filt have the mismatched citation.

**Required**: One of:
- (a) Introduce a per-link sub-lemma (e.g., **PerLinkInvarianceUnderValuePreservation**: "for `a ∈ dom(Σ.L) ∩ dom(Σ'.L)` with `Σ'.L(a) = Σ.L(a)`, `matches(a, I, Σ) ⟺ matches(a, I, Σ')`"), derivable from L6 + coverage determinism + F1's structural form. Cite this sub-lemma at F11 and F19-filt instead of the meta-lemma.
- (b) Restructure ComprehensionInvariantUnderΣL to comprise an explicit per-link primitive plus a comprehension-composition step, and cite only the per-link primitive at F11 and F19-filt.
- (c) Derive F11 and F19-filt directly from LP13 + L6 + coverage determinism, omitting the meta-lemma citation entirely. F19-filt currently leans on this citation to discharge the filter-universal preservation, so option (c) requires showing the universal-preservation step explicitly.

VERDICT: REVISE
