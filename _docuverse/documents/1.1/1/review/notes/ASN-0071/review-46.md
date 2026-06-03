# Review of ASN-0071

## REVISE

### Issue 1: "interior-action-point rejection" names a case the ASN neither defines nor demonstrates
**ASN-0071, A cross-depth query**: "Every document above has common content depth `m_C = 2`, so neither the cross-depth subtree capture (`#u < m`) nor the interior-action-point rejection (`#u ≥ 3`) can be exercised against an actual arrangement — both require a deeper source."
**Problem**: The vspec preconditions only require `actionPoint(ℓ) = #u ≥ 2`. There is no rejection mechanism in this ASN keyed on `#u ≥ 3`, and the spec never *rejects* unresolvable input — it silently filters (F-FILT). The phrase is grouped with the cross-depth case as something requiring "a deeper source," but a precondition rejection (if that is what is meant) depends on the vspec's own `ℓ`, not on the source depth at all. The d_E construction then exercises the cross-depth capture but never demonstrates any "interior-action-point rejection." This is a dangling reference to a case the ASN does not specify.
**Required**: Either remove the mention, or, if there is a genuine precondition consequence worth stating (e.g., a vspec whose action point is interior to `#u` is excluded by `actionPoint(ℓ) = #u`), state it as a claim and demonstrate it — and stop calling silent filtering "rejection."

### Issue 2: "why the axiom is needed" meta-prose around S3★-aux
**ASN-0071, The operation (F-CONTENT)**: "S3★ is conditional — it routes positions whose subspace is `s_C` or `s_L` but is silent on any V-position of a third subspace; to conclude that *every* image of `M(d)` lands in `dom(C) ∪ dom(L)` we also invoke S3★-aux (SubspaceExhaustiveness, ASN-0047), which forecloses a third subspace."
**Problem**: This is the "explains why the axiom is needed rather than what it says" pattern. A precise reader needs only the citation `ran(M(d)) ⊆ dom(C) ∪ dom(L)` by S3★ ∧ S3★-aux; the paragraph spends three clauses justifying *that S3★-aux is cited at all*.
**Required**: Replace with the bare entailment: "By S3★ ∧ S3★-aux, `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)`."

### Issue 3: interpretive essay content in a derivation slot
**ASN-0071, Resolution**: "The query thus reads charitably — as 'find documents containing the content at whatever positions of `σ` are currently bound' — rather than insisting on total resolvability."
**Problem**: F-FILT already carries the operative claim (positions outside `dom(M(d_s))` contribute nothing). The "reads charitably / rather than insisting" framing is interpretive prose that does not advance the derivation. A reader following the resolve-equivalence argument must skip past it.
**Required**: Drop the framing sentence; let F-FILT state the behavior.

## OUT_OF_SCOPE

### Topic 1: relationship between current-state result and historical relation R
**Why out of scope**: Correctly deferred to Open Questions; connecting `find` to the permanent provenance relation is new territory, not an error here.

### Topic 2: rejection-vs-filter policy for unresolvable positions
**Why out of scope**: The decision of when to reject rather than filter is correctly named as an Open Question — but see Issue 1, where the prose pre-empts that question with a term ("rejection") the spec does not earn.

VERDICT: REVISE
