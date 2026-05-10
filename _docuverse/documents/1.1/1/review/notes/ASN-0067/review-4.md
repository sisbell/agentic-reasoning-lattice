# Review of ASN-0067

## REVISE

### Issue 1: Incorrect justification for intermediate-state reachability
**ASN-0067, Elementary Decomposition, Case 1 (between Steps 2 and 3)**: "This intermediate state is reachable by a valid composite (J0, J1, J1' all hold since ran(M) is preserved and R is unchanged)"
**Problem**: ran(M) is NOT preserved after K.μ⁻. Contraction removes B_post entries from dom(M(d)), which can remove I-addresses from ran(M(d)) — any I-address that appeared exclusively in B_post blocks and not in B_pre is lost from the range. The coupling constraints hold, but for a different reason: they hold *vacuously*. J0: dom(C₁) \ dom(C₀) = ∅ (no content allocated). J1: ran(M₁(d)) ⊆ ran(M₀(d)) so ran(M₁(d)) \ ran(M₀(d)) = ∅ (no new I-addresses). J1': R₁ = R₀ so R₁ \ R₀ = ∅ (no new provenance). None of these require ran(M) to be preserved.
**Required**: Replace "since ran(M) is preserved and R is unchanged" with a correct justification: "J0, J1, and J1' all hold vacuously: no content is allocated (dom(C) unchanged), no I-address is newly introduced into any arrangement (K.μ⁻ can only reduce the range), and no provenance pair is added (R unchanged)."

### Issue 2: C12a equality condition incomplete
**ASN-0067, Provenance Completeness**: "with equality when no resolved I-address already appeared in ran(M(d))"
**Problem**: The bound |new provenance pairs| ≤ w is correct. But the equality condition requires an additional clause: the resolved blocks must contain no duplicate I-addresses. When a content reference sequence names overlapping V-spans in the same source document, the composite resolution can include the same I-address in multiple blocks. The provenance set {(a, d) : a ∈ ran(M'(d)) \ ran(M(d))} counts each distinct I-address once, but w counts every occurrence across all resolved blocks. So |{...}| < w even when every resolved I-address is new to ran(M(d)), if any I-address appears in multiple resolved blocks.
**Required**: Amend the equality condition: "with equality when no resolved I-address already appeared in ran(M(d)) and no I-address appears in more than one resolved block."

### Issue 3: C5 prose contradicts elementary decomposition
**ASN-0067, Displacement**: "COPY removes no existing V→I mapping from M(d)"
**Problem**: The elementary decomposition explicitly removes V→I mappings via K.μ⁻ (Step 1 of Case 1 removes all B_post entries). The mappings are re-established at shifted V-positions in Step 2 (K.μ⁺), so the I-address information is preserved — but specific V→I pairs at positions ≥ v are deleted and replaced. The formal statement is correct: it says every I-address in ran(M(d)) has a witness in ran(M'(d)), allowing the V-position to change. The prose claims no mapping is removed, which is false at the level of individual (v, M(d)(v)) pairs.
**Required**: Align the prose with the formal statement. For example: "Every I-address in the pre-state arrangement is preserved in the post-state arrangement: no content is lost, only relocated."

## OUT_OF_SCOPE

### Topic 1: D-CTG status in the invariant hierarchy
**Why out of scope**: The ASN correctly observes that D-CTG is violated in intermediate states of the COPY composite, establishing that D-CTG is not an invariant of all reachable states but a design constraint preserved at operation endpoints. This raises a foundation-level question: what predicate characterizes D-CTG's actual status? The ReachableStateInvariants theorem (ASN-0047) does not include D-CTG, yet COPY's precondition P.2 requires it. The gap — D-CTG is assumed but never guaranteed by the foundation — belongs in a future ASN that defines the relationship between operation-endpoint properties and inter-operation invariants.

### Topic 2: Concurrent COPY semantics
**Why out of scope**: The ASN correctly identifies this as an open question. The ValidComposite framework provides only sequential correctness. The observation that K.μ⁻ produces a D-CTG-violating reachable state makes this particularly pressing for concurrent systems, but it requires a concurrency model not present in the current foundation.

VERDICT: REVISE
