# Review of ASN-0117

## REVISE

### Issue 1: The "binding versus being" theme is restated across four sites, and the dedicated section contains an imprecise claim

**ASN-0117, "A span, not a position: binding versus being"**: "A single position binds no content, so a position-deletion would reveal nothing underneath; only a span, with extent, separates binding from being."

**Problem**: (a) This is the fourth restatement of the binding-vs-being distinction — already made in "What is removed, and what must survive," in P1, and in DEL-REMOVE. The section adds a Nelson quote and re-narrates P0+P1 without advancing the argument. (b) The quoted claim is imprecise to the point of being wrong on the model's own terms: under `M(d)(q_J) = a_J`, a single V-position *does* bind content (it maps to an I-address). The operation deletes spans of width `c ≥ 1`, and even the `c = 1` case removes one binding `q_J ↦ a_J` while `a_J` survives — i.e., a single-position deletion already "separates binding from being," directly contradicting "only a span, with extent, separates binding from being."
**Required**: Delete the section or fold its one non-redundant sentence into "What is removed." Remove or correct the "single position binds no content" claim.

### Issue 2: P1 is a relabeling of DEL-REMOVE; the claim set also has a numbering gap

**ASN-0117, P1 (ArrangementContraction)**: "DEL-REMOVE, read as a guarantee about binding rather than being. ... The count-and-label form of that removal, and why it is robust against within-document sharing, are established once at DEL-REMOVE above."

**Problem**: P1 introduces no content beyond DEL-REMOVE — it explicitly defers its substance ("established once at DEL-REMOVE above") and supplies only a semantic reframe. Two labeled claims carry one fact. Separately, the introduced claims run P0, P1, P2, P4, P5 — P3 is absent (an editing artifact from the recent "absorb P3 into P0" revision), leaving an unexplained gap a reader must reconcile.
**Required**: Either give P1 independent content or drop the label and keep DEL-REMOVE. Renumber to close the P3 gap or note the absorption.

### Issue 3: DEL-REMOVE carries a defensive formulation-justification paragraph

**ASN-0117, DEL-REMOVE**: "We state removal as a count plus top-`c` label vacancy rather than as the absence of each old pair, because a deleted-span label `q_k`..."

**Problem**: The kernel (per-pair absence fails under within-document sharing) is load-bearing, but it is delivered as a multi-sentence defense of why the claim is phrased one way and not another — meta-prose about formulation choice rather than the guarantee itself. Combined with P1's back-reference to it, the same point is litigated twice.
**Required**: Compress to the one-clause invariant statement plus a single parenthetical noting the sharing case; drop the comparative justification of the rejected phrasing.

## OUT_OF_SCOPE

### Topic 1: Deletion at element-field depth `m > 2`
**Why out of scope**: The operation is correctly scoped to the depth-2 text case inherited from foundation ASN-0082, whose contraction is itself `#p = 2`. Generalizing to deeper version chains requires new foundation displacement work, not a revision here.

### Topic 2: Deletion of link-subspace positions
**Why out of scope**: DELETE's precondition fixes `S = s_C`. Removing a link from a document's arrangement (subspace `s_L`) is a distinct link operation, future territory.

The core construction is sound: the K.μ⁻+K.μ⁺ decomposition (and the lone-K.μ⁻ `R = ∅` realization) is faithful to ASN-0082's displacement; the coupling discharge (J0/J1★/J1'★ vacuous) and the entity/provenance/link frames are correctly justified; boundary cases (suffix delete, delete-everything, leading-span, within-document sharing) are exercised; and the wp analysis on per-link discoverability is genuinely non-trivial and correct. The remaining issues are prose accretion and one imprecise sentence.

VERDICT: REVISE
