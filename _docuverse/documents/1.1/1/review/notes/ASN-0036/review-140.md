# Review of ASN-0036

I checked each proof (S1, S4, S5, S7, S8, D-CTG-depth, D-SEQ) and the partition argument. The mathematics is sound — the within/across-subspace uniqueness lemma, the infinite-intermediate construction in D-CTG-depth, and the NAT-discrete/NAT-order chain in the S8 case `j = m` all hold. My findings are accretion and dead scaffolding, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Residual correspondence-run scaffolding in S8
**ASN-0036, S8 (Singleton span partition)**: "This is the singleton (`n = 1`) instance of a more general notion of *correspondence run* `(v, a, n)` ... The existence and uniqueness of *maximal* runs (`n > 1`) ... this ASN does not discharge; we defer it to the Open Questions."
**Problem**: The most recent revision dropped correspondence-run scaffolding and restated S8 as a pure singleton partition, but this paragraph survived. It introduces a notion the ASN never uses, never discharges, and forwards to the Open Questions — exactly the reviser-drift pattern of prose deferring to a downstream location. S8 is now a self-contained partition claim; the generalization is noise the reader must skip past.
**Required**: Delete the paragraph. The Open Question on maximal-run decomposition already records the deferred work; the body need not announce it.

### Issue 2: S9 is a numbered slot with no formal content
**ASN-0036, S9 (Two-stream separation)**: "S9 is S0 read directionally ... and adds no formal content beyond S0; we name it only because Nelson emphasises this separation."
**Problem**: A numbered property whose own prose admits it states nothing beyond S0 is meta-prose justifying its existence rather than advancing reasoning. Either it carries a distinct directional obligation (an arrangement-only transition theorem with its own proof) or it is S0.
**Required**: Either give S9 a distinct formal statement and discharge it, or fold the Nelson remark into S0's discussion and drop the numbered slot.

### Issue 3: S7c and `subspace_I` are introduced but unconsumed
**ASN-0036, S7c (Element-field depth) and the `subspace_I(a) = E(a)₁` definition**: "We write `subspace_I(a) = E(a)₁` for the first component of an I-address element field ..."
**Problem**: Neither S7c nor `subspace_I` is used by any proof in this ASN — S7's proof invokes S7a, S7b, S7d only. The single consumer of both is the Open Question on subspace alignment. Introducing a design requirement plus a projection solely to feed a future-work question is premature scaffolding.
**Required**: Remove S7c and the `subspace_I` definition, or have an in-ASN claim actually consume them. If they exist only to set up a future ASN, they belong in that ASN.

### Issue 4: Forward pointer in the D-CTG preamble
**ASN-0036, end of D-CTG section**: "At depth m ≥ 3, D-CTG combined with S8-fin forces a stronger restriction: all positions ... must share components 2 through m − 1 — see D-CTG-depth below."
**Problem**: The sentence states D-CTG-depth's conclusion and then points forward to it; the claim is restated at its own site immediately after. Minor, but it is duplicated content with a "see below."
**Required**: Drop the preview sentence; let D-CTG-depth state itself.

## OUT_OF_SCOPE

### Topic 1: ValidInsertionPosition / ValidFirstInsertionPosition preservation
These predicates characterize well-formed positions (state structure), so defining them here is defensible. But their operational payload — whether INSERT at such a position preserves D-CTG/D-MIN/S2 — is correctly punted to the Open Questions and the operations layer. No revision needed; flagging only to confirm the predicates' preservation behavior is not expected in this ASN.

META: Not applicable — the ASN remains a state-and-invariant specification; the findings are accreted prose and unused scaffolding, all fixable without terminating the note.

VERDICT: REVISE
