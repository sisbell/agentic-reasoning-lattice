# Review of ASN-0043

## REVISE

### Issue 1: L12 carries a forward-reference / downstream-consumer note that does not advance the immutability claim
**ASN-0043, L12 (LinkImmutability)**: "Link permanence protects meta-link references: since links are addressable by L13, a link that persists in `Σ.L` keeps every meta-link pointing to it well-defined."
**Problem**: This is exactly the flagged anti-bloat pattern — a claim's exposition enumerating a downstream consumer (L13 meta-links) via a forward reference, rather than advancing what L12 says. L12's content is the two-part permanence statement (address endures, value fixed); the Nelson/Gregory evidence already grounds it. The meta-link sentence is a benefit-of-the-claim aside the precise reader must skip to follow the immutability argument, and it imports L13 (defined later) into L12's slot.
**Required**: Delete the sentence. If the meta-link well-definedness consequence is worth stating, it belongs at L13 (where addressability is established), not threaded backward into L12.

### Issue 2: L9 and L11b assert "Σ′ extending Σ" (`⊒`, StateExtension) but never discharge its conjuncts
**ASN-0043, L9 and L11b**: both conclude existence of a "`Σ' extending Σ`" (`Σ' ⊒ Σ`, StateExtension), e.g. L9: "there exists ... a conforming state `Σ'` extending `Σ` (`Σ' ⊒ Σ`, StateExtension)".
**Problem**: StateExtension is a *defined relation* with three explicit conjuncts (monotone growth and agreement on the shared domain for `Σ.C`, `Σ.M`, `Σ.L`). The proofs establish invariant conformance via FSP and (for L9) ghost disjointness, but never check the `⊒` conjuncts. The data is present — `Σ'.C = Σ.C`, `Σ'.M = Σ.M`, `Σ'.L = Σ.L ∪ {fresh ↦ …}` — so the conclusion is trivially true, but the named relation appearing in the existential is asserted without being discharged.
**Required**: Add the one-line discharge in each proof: `C` and `M` unchanged ⇒ equality on shared domain; `L` grows only at a fresh address ⇒ monotone with agreement on `dom(Σ.L)`; hence `Σ' ⊒ Σ`.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace residence
The disjointness results (L1d(b), L14, L14a) are scoped to the `s_C`-resident slice; lifting them to all of `dom(Σ.C)` requires a content-side invariant fixing a global content subspace. The ASN correctly defers this to the first Open Question.
**Why out of scope**: A content-store invariant is ASN-0036 territory, not a defect in the link model; the scoping here is deliberate and honest.

VERDICT: REVISE
