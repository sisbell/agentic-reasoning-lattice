# Review of ASN-0115

I checked the mathematics carefully before turning to the prose, because the anti-bloat classifier should not distract from correctness. The technical content holds up:

- **Confinement lemma** — the T5/TumblerAdd argument is sound; `p ≼ s` and `p ≼ reach(σ)` are correctly established, and T5 with `s ≤ t ≤ reach(σ)` yields `p ≼ t`. The `m ≥ 2` precondition is supplied by the V-spec.
- **R6 act=∅ analysis** — the three-way case split (V_S(d)=∅ / act≠∅ canonical-start / act=∅-but-V_S(d)≠∅) is complete; the derivation that `act ≠ ∅` forces `s = [S,1,…,1,s_{m_S}]` (via D-SEQ★ on a witness `v ∈ act ⊆ V_S(d)` plus Confinement) is correct, and the "no interior hole, only terminal overrun" conclusion lands.
- **R7 comparability** — the necessity of `Σ →* Σ'` (vs. mere co-reachability) is genuine: on divergent branches the same tumbler can be allocated with different values, so equal arrangement restrictions would *not* force equal content. The proof gets this right.
- **R8 link-vacuity** — CL-OWN forcing `d = d'` then CL-UNIQ forcing `v = v'` correctly establishes that distinct link positions cannot share an address; the content/link dispatch via S3★/SD/S3★-aux is valid.
- **R11 permanence** — the K.μ⁻ frame argument and the "single live condition" wp are correct.

I found no correctness defect, no missing boundary case, and the depth requirements (worked instances for R6/R8/R9/R10/R11, a non-trivial wp in R11, derived consequences) are met. The REVISE items below are all anti-bloat trims, per the active `review-mode.anti-bloat` classifier — forward/cross-reference meta-prose that orients rather than reasons.

## REVISE

### Issue 1: Downstream-consumer justification in the V-spec definition
**ASN-0115, "What a spec-set is" (depth-compatibility clause)**: "This is the same discipline ASN-0058's ContentReference imposes (`#ℓ = #u = m`...); **it is what lets R6 below reason about `⟦σ⟧` and `V_S(d)` at a single shared depth.**"
**Problem**: The depth-compatibility constraint's content is `#s = m_S(d)`. The trailing clause justifies the constraint by naming its downstream consumer (R6), which is the "definition's introduction enumerating downstream consumers" pattern. Removing it loses no reasoning — R6 invokes depth-compatibility on its own.
**Required**: Drop "it is what lets R6 below reason about `⟦σ⟧` and `V_S(d)` at a single shared depth"; keep the constraint and, if desired, the ContentReference parallel.

### Issue 2: Cross-reference editorializing on the empty-spec-set boundary
**ASN-0115, R0 (empty-request boundary)**: "...so `deliver(⟨⟩, Σ) = ⟨⟩` — the empty spec-set is a valid request whose delivery succeeds and returns nothing, **the companion at the request level to R6's partial-success discipline within a spec.**"
**Problem**: The boundary `deliver(⟨⟩, Σ) = ⟨⟩` is settled by the definition; the "companion to R6's partial-success discipline" clause characterizes a relationship to a downstream claim without advancing the derivation. It is orientation, not reasoning.
**Required**: End the sentence at "succeeds and returns nothing."

### Issue 3: Use-site inventory of sibling claims in the R9 worked instance
**ASN-0115, R9 worked instance (closing)**: "...exactly the dual obligation R9 names, shown here for **the multi-origin case that R8 (single shared origin) and R11 (single forked lineage) do not exercise.**"
**Problem**: The worked instance already demonstrates R9's dual obligation. The appended inventory of what R8 and R11 do/do-not exercise is cross-claim orientation that does not bear on the instance's correctness — the "use-site inventory" pattern.
**Required**: End at "exactly the dual obligation R9 names." If a contrast is wanted, it belongs (once) in the Synthesis, not appended to a worked instance.

### Issue 4: Justifying the practice of stating a frame
**ASN-0115, pure-query frame paragraph**: "We record this as a frame rather than leave it implicit in the functional notation, **matching the convention the project's other query operation states explicitly (ASN-0086, Observe: 'Observe leaves Σ unchanged').**"
**Problem**: The load-bearing content is "RETRIEVEV is a pure query; no component of Σ is modified; it is a function of state, not a transition." The closing clause justifies the *practice* of recording the frame by citing precedent — meta-prose about presentation, not about RETRIEVEV.
**Required**: State the frame; drop the precedent justification (or reduce to a bare parenthetical cite if the Observe analogy is genuinely wanted).

## OUT_OF_SCOPE

Nothing to add. The five Open Questions correctly defer the out-of-scope territory (inline provenance, fail-vs-partial, dangling references, channel faithfulness, straddling spans) to future ASNs, and no claim trespasses into the excluded operations (RETRIEVEDOCVSPAN, READLINK, etc.). R10's decision to deliver link *references* and defer link *structure* to READLINK is consistent with the declared scope.

VERDICT: REVISE
