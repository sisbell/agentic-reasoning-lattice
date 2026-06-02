# Review of ASN-0086

## REVISE

### Issue 1: CoverageEqualityDecidable declines to derive its load-bearing step
**ASN-0086, Lemma CoverageEqualityDecidable**: "A gap `(c_k, c_{k+1})` is empty exactly when `c_{k+1}` is the immediate T1-successor `c_k.0` of `c_k` (the zero-extension; ASN-0034, TA5 note) — we cite that characterization rather than re-derive it — decided by the single T2 comparison `c_{k+1} = c_k.0`."

**Problem**: The lemma is a *constructive decidability* claim; its sole non-mechanical step is deciding whether an open gap contains a tumbler. That step is discharged by an explicit refusal to prove ("we cite that characterization rather than re-derive it"), and the cited source is the **TA5 prose note** of ASN-0034 — not a formal contract postcondition. No foundation claim has "immediate successor = `t.0`" as a postcondition; it appears only in the discussion prose. A decidability lemma cannot rest its one interesting inference on an underived appeal to prose. This is precisely "no proof by 'we cite rather than derive.'"

**Required**: Derive the characterization inline from T1 (it is short): `t < t.0` by T1 case (ii); any `s` extending `t` satisfies `s ≥ t.0` (case (i) at the appended position); any `s` not extending `t` with `s > t` diverges at some `k ≤ #t` with `s_k > t_k = (t.0)_k`, giving `s > t.0`; hence nothing lies strictly between `t` and `t.0`. Then `c_k.0` itself serves as the in-gap witness for non-empty gaps. Alternatively, if coverage-equality decidability is not load-bearing for any R-invariant, move the lemma to OUT_OF_SCOPE as an implementation-mechanics claim.

### Issue 2: Citation-bookkeeping meta-prose (anti-bloat)
**ASN-0086, Fact — HomeOriginCoincidence**: "We cite this fact at each site below rather than re-derive it." **And CoverageEqualityDecidable**: "we cite that characterization rather than re-derive it."

**Problem**: These sentences describe the document's *citation discipline*, not the reasoning. They advance no claim and force the reader to skip past bookkeeping to reach the argument — the accretion pattern this note is classified to surface. A fact is either cited at its point of use or not; announcing a citation policy is noise.

**Required**: Delete the policy sentences. Cite HomeOriginCoincidence at each use site (already done); the meta-announcement is redundant. For CoverageEqualityDecidable, the deletion is subsumed by fixing Issue 1.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity model for Emit vs. Observe
The Open Questions ask whether Emit must be atomic w.r.t. concurrent Observe and what consistency model governs `A_K` transitions. This is a substrate-concurrency concern requiring a transition-interleaving model not present here; correctly deferred.

### Topic 2: Elevating the unit-depth retraction discipline to a substrate guarantee
Whether a designated retraction K-operation should enforce unit-depth to-spans at the substrate (closing the address-vs-shape gap the wp Case 2 domain restriction depends on) is genuinely new substrate design, not a defect in this note's layer-level treatment.

VERDICT: REVISE
