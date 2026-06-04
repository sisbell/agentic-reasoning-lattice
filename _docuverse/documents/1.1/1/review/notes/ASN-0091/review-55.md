# Review of ASN-0091

## REVISE

### Issue 1: Chaining lemma applied to claims it does not cover
**ASN-0091, Composition Across Multi-Step REARRANGE Sequences**: "Every ★ form whose single-step claim is a preserved equality follows from this lemma by induction: RE-C★, RE-L★, RE-R★, RE-dom★, RE-ran★, RE-μ★, RE-cov★, RE-disc★, RE-proj★, RE-sub★, and RE-origin★..."

**Problem**: The document-parameterised chaining lemma is stated for "any quantity that is a function of `Σ.M(d)` alone" yielding a *preserved equality* `X(Σ_n, d) = X(Σ_0, d)`. Most of the listed ★ forms do not meet that hypothesis:
- RE-C★, RE-L★, RE-R★ are functions of `C`, `L`, `R` — not `M(d)`.
- RE-cov★ is a function of `Σ.L` — not `M(d)`.
- RE-origin★ is state-independent (a function of the address) — not `M(d)`.
- RE-disc★ is a biconditional depending jointly on `Σ.L` (via coverage) and `ran(M(d))`; it follows from RE-cov★ + RE-ran★ via LP12, not from the lemma alone.
- RE-proj★ is a *transport* (`project(e,d,Σ_n) = (π̂_n ∘ ⋯ ∘ π̂_1)(project(e,d,Σ_0))`), not a preserved equality; the lemma produces `X(Σ_n)=X(Σ_0)` and cannot yield a transport.

The table's per-claim provenance column is correct (e.g. RE-C★ "from RE-C", RE-proj★ "from RE-proj + RE-other"), so the prose contradicts the table.

**Required**: Restrict the lemma's stated coverage to the M(d)-function preserved-equality claims (RE-dom★, RE-ran★, RE-μ★, RE-sub★). State separately that the component-global claims (RE-C★/L★/R★/cov★) and RE-origin★ chain by the trivial "RA-frame fixes the component at every step" induction, that RE-disc★ chains via RE-cov★ + RE-ran★, and that RE-proj★ is the composition of per-step transports.

### Issue 2: The π-non-identity vs net-effect distinction is restated across multiple paragraphs
**ASN-0091, REARRANGE as Vstream-Only Operation**: the distinction between "π non-identity as a permutation of V-positions" and K.μ~ clause (ii)'s "`M'(d) ≠ M(d)`" is stated three times — "The two come apart whenever the affected-range value sequence is invariant under the cut-induced block permutation"; then "The realisation therefore splits on net effect: in the non-trivial case... and in the collapse case..."; then "REARRANGE_K carries no non-triviality precondition: it remains defined wherever R-PRE holds, collapsing to the identity precisely on affected ranges fixed by the cut-induced permutation."

**Problem**: The concrete S5 collapse witness is substantive and earns its place, but the framing sentences surrounding it repeat the same claim (REARRANGE_K may collapse to identity; the realiser then needs no work) in three reformulations. With the anti-bloat classifier active, this is accreted meta-prose the reader must work past.

**Required**: Keep the concrete S5 witness and a single statement of the case split; remove the repeated reformulations.

### Issue 3: RE-proj's "abstract / every realisation" provenance leans on a K.μ~-scoped lemma
**ASN-0091, Projection Transports Along π**: "This is ASN-0098's LP11 (ReorderingBijection) instantiated... LP11's hypotheses are exactly RA-π... so the conclusion holds for every realisation, not only REARRANGE_K."

**Problem**: LP11 is stated in the foundation for *K.μ~ transitions*. The claim that RE-proj holds for *every* Vstream-only realiser (the "abstract" provenance) re-runs LP11's proof for arbitrary realisers rather than applying its statement. The text already reproduces the derivation chain (`v ∈ project ⟺ ... ⟺ π(v) ∈ project'`), so it has the abstract argument in hand.

**Required**: Present the three-line derivation from RA-π + coverage state-independence as the abstract proof, and cite LP11 only as the REARRANGE_K (K.μ~) instance — or restrict RE-proj's provenance to the K.μ~ realiser.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: Correctly deferred by the ASN's second Open Question; CS3 fixes the cut subspace to `s_C`, so link-subspace reordering is a future operation, not a gap in this note.

### Topic 2: Joint reconstitution of a split same-source transcluded span
**Why out of scope**: RE-trans establishes per-fragment origin (RE-origin); whether two fragments jointly reconstitute the source span is correctly routed to the first Open Question.

VERDICT: REVISE
