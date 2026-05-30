# Review of ASN-0084

## REVISE

### Issue 1: Defensive meta-prose closing R-NS(NS-π)
**ASN-0084, R-NS proof, (NS-π)**: "The argument uses only (a) the frame clause of the operation's contract and (b) the first-line stipulation of the bijection definition; no subspace-S content of R-PPERM or R-SPERM is invoked."
**Problem**: This sentence advances no reasoning — the proof already exhibited exactly which facts it used. It is a defensive justification of what the argument does *not* invoke, the precise accretion pattern flagged for this note. A reader must skip it to continue.
**Required**: Delete the sentence.

### Issue 2: R-SP proof defers to itself and editorializes about R-BLK
**ASN-0084, R-SP proof**: "How the rearrangement acts on the runs of the decomposition is characterized separately by R-BLK; that characterization discharges nothing in Q, which asks only about the (maximal) decomposition of M'(d)."
**Problem**: This explains what R-BLK does *not* contribute to Q — defensive meta-prose, not a proof step. R-SP's actual content ("every clause of Q except S8 is discharged by the Invariant preservation paragraph; S8 by Foundation-S8 transport") is a verbatim pointer back to earlier passages, adding only the `wp` framing. The lemma largely restates the "Invariant preservation" paragraph.
**Required**: Drop the R-BLK editorial sentence. Either fold R-SP's content into the Invariant preservation paragraph or have R-SP state the wp result and cite that paragraph once, without re-enumerating the invariant list a second time.

### Issue 3: Foundation-S8 transport is deferred to from four separate locations
**ASN-0084, "Invariant preservation" / R-SP proof / R-BLK / "Canonical decomposition"**: each independently states that post-state S8 (or the maximal-run partition's existence/uniqueness) "follows from foundation S8 (ASN-0036)."
**Problem**: Multiple paragraphs in different sections defer to the same downstream foundation fact — a flagged compounding pattern. The reader meets the same claim four times.
**Required**: Establish the Foundation-S8 transport once and reference that single location from R-SP and R-BLK rather than re-deriving the deferral in each.

### Issue 4: Width derivation duplicated, with a forward reference to R-PRE
**ASN-0084, "Width-ordinal identities" (Cut Points section) vs. "Width positivity" (Consequences of R-PRE)**: The first paragraph opens "Under R-PRE, by R-PRE(iv) and D-SEQ…" and concludes "each width is therefore a well-defined positive natural number (≥ 1)." The Width positivity consequence then re-derives w_α, w_β, w_μ ≥ 1, with Step 1 reading "The Width-ordinal identities above already establish ord(c_{i+1}) − ord(c_i) ≥ 1."
**Problem**: (a) "Width-ordinal identities" sits in a section *before* R-PRE is defined, yet relies on R-PRE(iv) — a forward reference. (b) The "≥ 1" conclusion is established twice; the second occurrence cites the first for Step 1 and only adds the count-equals-ordinal-difference fact in Step 2.
**Required**: Consolidate. State the ordinal-difference identities where they belong (after R-PRE), and derive positivity once rather than asserting "≥ 1" in both places.

### Issue 5: Subspace confinement paragraph is a forward use-site inventory
**ASN-0084, "Consequences of R-PRE", Subspace confinement**: "The rearrangement constructions in this ASN (PivotPostcondition, SwapPostcondition) only assign new I-addresses to V-positions in V_S(d) and leave all other positions fixed (R-FRAME-P, R-FRAME-S), so no position outside subspace S is ever produced."
**Problem**: This enumerates downstream constructions and frame clauses (all defined later) to pre-justify a confinement fact that R-FRAME-P/S already state at their own site. It is a use-site inventory pointing forward, not a step advancing the confinement claim.
**Required**: Keep the object-level statement (cut-relative shifts retain subspace S via OrdShiftHom (a)); remove the forward inventory of PivotPostcondition/SwapPostcondition/R-FRAME.

### Issue 6: Duplicated uniqueness Remarks
**ASN-0084, R-PPERM "Remark (uniqueness scope)" and R-SPERM "Remark (uniqueness scope)"**: The R-SPERM remark reads "As in R-PPERM, π is the unique bijection satisfying M'(d)(π(v)) = M(d)(v) on V_S(d) when M(d) is injective on V_S(d); under S5 sharing it is the canonical fibre-permutation representative…"
**Problem**: Two paragraphs say the same thing in different words; the second is an acknowledged restatement of the first.
**Required**: State the fibre-permutation uniqueness scope once (it is independent of cut count) and reference it from both R-PPERM and R-SPERM.

### Issue 7: Phrasing-bookkeeping aside in R-BLK Phase 1
**ASN-0084, R-BLK Phase 1, "Outside ⋃_k V(b_k)"**: "…so c_{n−1} ∉ V_S(d) is equivalent to ord(c_{n−1}) > N, i.e., c_{n−1} > max(V_S(d)); we use both phrasings interchangeably below."
**Problem**: An explicit note that two phrasings are interchangeable is bookkeeping about prose, not reasoning.
**Required**: Pick one phrasing and use it; delete the interchangeability remark.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: The Open Questions correctly defer the general k-cut class and the closure of rearrangement composition to future work; this ASN scopes itself to n ∈ {3,4}.

### Topic 2: Operational recovery of the canonical maximal partition from B'
**Why out of scope**: R-BLK produces a valid (possibly non-maximal) partition and relies on foundation S8 for existence/uniqueness of the maximal one; the merge-confluence procedure is a legitimate future-ASN concern, not an error here.

VERDICT: REVISE
