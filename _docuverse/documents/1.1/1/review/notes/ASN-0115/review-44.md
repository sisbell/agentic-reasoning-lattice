# Review of ASN-0115

I checked R0–R11, the Confinement lemma, and every worked instance. The mathematics is sound: Confinement follows cleanly from T5/TumblerAdd; the `act` override is correctly analyzed (too-deep is a vacuous no-op, too-shallow is the operative case); R6's no-interior-hole guarantee holds across all sub-cases; R8's link-vacuity via CL-OWN + CL-UNIQ is correct; R11's wp decomposition is right. The boundary cases (empty spec-set, terminal overrun, orphaned content) are handled. All dependencies are foundation ASNs. One proof case is under-specified, and the prose carries two accretions of the kind this note's classifier targets.

## REVISE

### Issue 1: R7 proof omits the operative sub-case of the non-empty-restriction branch
**ASN-0115, §Repeatability (R7)**: "depth-compatibility then holds-or-fails identically, and where it holds act is the equal restriction's (equal, non-empty) domain."

**Problem**: The non-empty-restriction case splits into two differing sub-cases, and only one is shown. The restriction `Σ.M(dⱼ)|⟦σⱼ⟧` is exactly the *geometric* intersection `dom(M(dⱼ)) ∩ ⟦σⱼ⟧` — which is non-empty in the **too-shallow** case (`#s < m_S`), the very case the override exists for. Concretely with `m_S = 3`, `V_S(d) = {[S,1,k] : 1 ≤ k ≤ n_S}`, `s = [S,1]` (`#s = 2`), `ℓ = [0,w]` (`w ≥ 1`): every `[S,1,k] ∈ ⟦σ⟧` (position 2 decides), so the restriction equals all of `V_S(d)` (non-empty), yet depth-compatibility fails (`#s = 2 ≠ 3 = m_S`) and the override forces `act = ∅`. The proof establishes the load-bearing fact (`m_S(dⱼ) = #v` equal at both states ⟹ branch agrees) but spells out only "where it holds." It leaves the fails-branch — non-empty restriction yet `act = ∅` at both via override — implicit. By the "show each case" standard, the differing sub-case must be stated, especially since it is the non-trivial one (the override discarding a non-empty restriction is the whole point of the override).

**Required**: Add the fails-branch consequence: where depth-compatibility fails identically at both states, both take the override and `act(ρⱼ,Σ) = ∅ = act(ρⱼ,Σ')`, so the active sets still agree despite the non-empty restriction.

### Issue 2: R8 restates the non-disclosure conclusion and adds out-of-scope positioning
**ASN-0115, §What co-delivery does with transclusion (R8)**: box — "The sharing is a fact of resolution, not of the delivered output: each item carries the value Σ.C(a), never the address a (R1) ... discloses nothing about the shared origin (cf. R9)." Prose — "deliver performs no comparison of the two resolutions, it concatenates two independently computed items (R0). Nelson's promise that the system 'will also reveal and clarify commonalities between documents and among versions' (3/4) is kept by operations that compare addresses, not by RETRIEVEV, whose content payload is value-only."

**Problem**: The prose paragraph re-derives the box's non-disclosure conclusion — "no comparison" restates R0's concatenation, and "content payload is value-only" restates the box's "carries the value, never the address." The only genuinely new content is the per-position (vs. joint) resolution point. The closing Nelson-"commonalities" sentence positions RETRIEVEV against address-comparing operations (e.g., the out-of-scope SHOWRELATIONOF2VERSIONS); it advances no claim of this ASN — R1 already fixes the payload as value-only.

**Required**: Keep the per-position-resolution observation; drop the restatement of R0/R1 and the cross-operation positioning sentence.

### Issue 3: pure-query purity stated four ways with a component inventory
**ASN-0115, §What a spec-set is, and what delivery is**: "deliver(R, Σ) reads the state and produces no transition: no component of Σ is modified — neither the content store Σ.C, nor the link store Σ.L, nor any arrangement Σ.M(d), nor any other component. The operation does not appear in the substrate's transition vocabulary at all; it is a function of state, not a state transition (cf. ASN-0086, Observe)."

**Problem**: Purity is asserted in five overlapping forms (no transition / no component modified / a component-by-component inventory / not in the transition vocabulary / function-of-state-not-transition). The inventory "neither Σ.C, nor Σ.L, nor any Σ.M(d), nor any other component" is a use-site enumeration that adds nothing beyond "modifies no component."

**Required**: Collapse to one statement, e.g. "deliver is a pure query: a function of state that modifies no component and appears in no transition (cf. ASN-0086, Observe)."

## OUT_OF_SCOPE

The note's Open Questions (inline provenance, permitted failure, dangling references under relaxed S3★, channel faithfulness, subspace-straddling spans) correctly defer new territory to future ASNs; none is an error here. No claim in the ASN reaches into the listed out-of-scope operations.

VERDICT: REVISE
