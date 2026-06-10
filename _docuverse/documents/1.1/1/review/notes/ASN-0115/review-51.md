# Review of ASN-0115

I checked the proofs case by case. The mathematics is in good shape: the Confinement lemma's T5 appeal is sound; R6's "terminal-overrun, never an interior hole" rests correctly on D-SEQ★ contiguity over the bindable depth-`m_S` slice, with the `act = ∅` sub-case dispatched; R7's active-set agreement correctly handles the awkward case where the consulted restriction is non-empty yet the depth override fires identically at both states; R8's link-vacuity (CL-OWN + CL-UNIQ) and subspace-sharing (S3★/SD/S3★-aux) arguments hold; R11's existential witness (the unit span `(v, δ(1,#v))` is always depth-compatible) is consistent. Boundaries — empty request, empty document, unbound start, override-as-no-op — are covered. No correctness gap.

What remains is residual rationale prose in the definitional slot — the very thing the two most recent revise commits ("tighten depth-compat rationale and trim proof prose") were trimming — plus one mischaracterized dependency.

## REVISE

### Issue 1: "tacitly rely on" mischaracterizes the downstream dependency
**ASN-0115, "What a spec-set is" (subspace-`S∉{s_C,s_L}` paragraph)**: "Every spec that contributes material therefore has `S ∈ {s_C, s_L}`, the assumption the depth and `item` reasoning below tacitly rely on."

**Problem**: Neither downstream argument relies on this as a premise.
- The depth reasoning (R6) takes `V_S(d) ≠ ∅` as its substantive hypothesis, which *entails* `S ∈ {s_C, s_L}` by S3★-aux — it derives the fact, it does not assume it.
- `item` totality rests on S3★-aux applied to the *active position* `v ∈ dom(M(d))` (`subspace(v) ∈ {s_C, s_L}`), which is independent of the *start's* subspace `S`; when `S ∉ {s_C, s_L}`, `act = ∅` and `item` is vacuously total.

So the clause both misstates the logical relationship and is a use-site inventory (downstream-consumer enumeration) of the kind the anti-bloat pass targets.

**Required**: Drop the "the assumption … tacitly rely on" clause. The preceding sentence (`act = ∅`, "the spec delivers nothing") already disposes of the `S ∉ {s_C, s_L}` case; no forward inventory is needed.

### Issue 2: design-rationale essay and a compressed claim in the `act` definition
**ASN-0115, `act` definition**: "The override only *bites* when the start has gone too shallow (`#s < m_S(d)`), lest it capture deeper content the citation never named; when the start is too deep (`#s > m_S(d)`) the geometric intersection is already empty by Confinement, so the override is a vacuous no-op there." — and, just above, "defined below and applied inside `act`."

**Problem**: Two distinct defects in a structural (definitional) slot.
- *Essay placement.* The too-shallow/too-deep sub-case decomposition is design rationale, not part of stating `act`; "defined below and applied inside `act`" is a self-forward-reference to a definition that follows two lines later. Both are the meta-prose the `review-mode.anti-bloat` classifier flags.
- *Compressed claim.* "the geometric intersection is already empty by Confinement" is not one step. Confinement gives `p ≼ t ⟹ #t ≥ #s − 1`; a bound subspace-`S` position has depth `m_S(d) < #s`, which forces `m_S(d) = #s − 1`, makes it a *proper* prefix of `s`, hence `< s`, hence outside `⟦σ⟧`. "By Confinement" hides three further steps. This is "X follows from Y" standing in for a proof.

**Required**: Trim the too-shallow/too-deep rationale to what the definition needs and remove the self-forward-reference. If the vacuity observation is kept anywhere, show the length/prefix steps rather than charging it to Confinement alone.

## OUT_OF_SCOPE

None to add — the straddling-span, fail-vs-partial, dangling-reference (relaxed S3★), inline-provenance, and channel-faithfulness topics are correctly deferred to the Open Questions, and the unallocated-document case is correctly excluded by the V-spec precondition (`d ∈ dom(Σ.M)`). No scope drift.

VERDICT: REVISE
