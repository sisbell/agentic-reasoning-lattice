# Review of ASN-0047

## REVISE

### Issue 1: Same downstream location deferred to from multiple sections (forward-reference accretion)
**ASN-0047, *Decomposition of K.μ~* (Step (A), Case `s_L`)**: "Pointwise link fixity (clause (v), `π(v) = v`) for these sources is established once in *Link-subspace fixity and realisation*, sub-steps (1)–(4) below ... and is invoked here rather than re-run."
**ASN-0047, *Necessity and sufficiency of the precondition***: "Necessity relies on link-subspace fixity, which is established for realisable π via CL-UNIQ at `Σ` inside the realisability argument (*Link-subspace fixity and realisation*, sub-step (4))".
**Problem**: Two sections (and Step (A) Case `s_L`, the Necessity paragraph) defer to the same `(1)–(4)` sub-steps with prose explaining *that* they defer and *why they don't re-run it*. This is the "multiple paragraphs in different sections defer to the same downstream location" pattern flagged for this classifier — the reader must hold the forward pointer across three sites to follow the link-fixity argument.
**Required**: State link-subspace fixity once (the `M'(d)|_{dom_L} = M(d)|_{dom_L}` + CL-UNIQ result) and let the dependent sections cite the lemma by name without the "established once … invoked here rather than re-run" meta-prose.

### Issue 2: Defensive meta-prose in the Notation section
**ASN-0047, *Notation* (Subspace-position correspondence)**: "Their correspondence `subspace(v) = subspace_I(a)` for `M(d)(v) = a` is not notation but a derived consequence; it is established at S3★ (*Generalized referential integrity*) from S3★ + L0 + S3★-aux."
**Problem**: A Notation entry that announces it is "not notation but a derived consequence" and forward-points to its own discharge site is meta-prose about placement, not content. The correspondence is re-derived in full at S3★; the Notation paragraph adds only the disclaimer.
**Required**: Either give the projection signatures plainly (no derivation claim) or drop the entry and introduce the correspondence at S3★ where it is proved.

### Issue 3: K.μ⁺ amendment enumerates a sibling transition's obligations
**ASN-0047, *K.μ⁺ amendment (ContentSubspaceRestriction)***: "K.μ⁺_L discharges the parallel contiguity and minimum-position obligations when the link subspace is the one extended."
**Problem**: This sentence sits inside K.μ⁺'s amendment but describes what a *different* transition (K.μ⁺_L) is responsible for. It does not advance K.μ⁺'s own argument — the preceding sentence already established that K.μ⁺ leaves `V_{s_L}(d)` framed. It is cross-reference noise of the kind the classifier asks to surface.
**Required**: Delete the K.μ⁺_L sentence; the frame argument for `V_{s_L}(d)` already closes K.μ⁺'s link-subspace obligation, and K.μ⁺_L's obligations belong in K.μ⁺_L.

### Issue 4: `dom(M(d)) ≠ ∅` is "derived" in K.μ⁻ but checked as a precondition in the worked example
**ASN-0047, K.μ⁻ definition**: "The strict-contraction constraint forces `n_S ≥ 1` for that S, hence `V_S(d) ≠ ∅` and a fortiori `dom(M(d)) ≠ ∅`, discharging the effect clause's satisfiability".
**ASN-0047, *Worked example: link allocation and arrangement*, Step 5**: lists "`dom(M(d)) ≠ ∅`: ✓ — `V_{s_C}(d) ∪ V_{s_L}(d) = {...}` is non-empty" as an explicit precondition check.
**Problem**: The definition states non-emptiness is *derived* from the strict-contraction choice and not a separate precondition; the worked example presents it as an independently-checked precondition. A reader reconciling the two cannot tell whether non-emptiness is an obligation the caller must verify or a consequence of the retention-count choice.
**Required**: Pick one framing. If derived, drop the standalone check in Step 5 (or label it "derived, not checked"); if a precondition, list it explicitly in K.μ⁻'s precondition block.

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement contraction with renumbering
**Why out of scope**: K.μ⁻ models link-subspace contraction by suffix removal only; interior withdrawal with compaction/renumbering (the implementation's `DELETEVSPAN`) is genuinely new operational territory, and the ASN already records it as an Open Question. Not an error in this ASN.

### Topic 2: Address-space exhaustion / fresh-address availability
**Why out of scope**: SubAllocFresh discharges freshness against the finite current store; whether allocation can fail under a bounded implementation is the T0-violation concern owned by ASN-0034 and listed here as an Open Question. Future ASN territory, not a gap in this one.

VERDICT: REVISE
