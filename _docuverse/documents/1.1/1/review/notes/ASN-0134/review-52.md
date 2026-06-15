# Review of ASN-0134

This is strong, careful work. The operation/step seam is handled honestly (G1 confluence is correctly scoped to a *fixed* raw-step set, with the operation-level order-dependence isolated afterward in §4); the serializability-vs-SC distinction is proven with a genuine third-party cycle witness rather than asserted; the linearizable-but-not-SC claim is correctly grounded in pipelining (real-time ⊊ program order); the canonical-vs-settled gap (§2), the both-miss interleaving (G2/instance i), and the target-residence race are all real and well-argued; and §7/§8 supply concrete address-level grounding. The findings below are duplication, one notational off-by-one, and meta-prose — the issues the anti-bloat classifier asks for — not defects in the core argument.

## REVISE

### Issue 1: §3's first two paragraphs duplicate each other
**ASN-0134, §3**: Paragraph 1 — *"The substrate models no per-agent program order over an agent's issues and preserves none; §4's cross-home liberation places a pipelining agent's two distinct-home operations at ≺-incomparable indices the linearization may resolve either way."* Paragraph 2 — *"What the substrate does not do … is track or enforce each agent's program order: §4's cross-home liberation places an agent's two distinct-home operations at ≺-incomparable indices the linearization may resolve either way (G0)."*
**Problem**: The trailing sentence is near-verbatim in both paragraphs ("§4's cross-home liberation places … two distinct-home operations at ≺-incomparable indices the linearization may resolve either way"), and the surrounding claim ("program order is not preserved") is stated twice. Both paragraphs also restate the pipelining client model already given in G0's box. This is the "two paragraphs say the same thing in different words" pattern.
**Required**: Collapse the two setup paragraphs into one; state the program-order/≺-incomparable point once and let G0's box carry the formal version.

### Issue 2: A6 pre-establishes the preservation arguments; §5's W0/W1 re-derive them, with placement meta-prose
**ASN-0134, A6 (§2)**: *"Their preservation under any interleaving is the earliest model-intrinsic result, established here ahead of the two sections that use it: the allocator deposits only at the next sibling of a home's current chain-maximum (inc(max,·)) … so a gapless initial segment stays a gapless initial segment step by step."*
**ASN-0134, W1 (§5)**: *"A6 established the preservation ahead of its consumers — the inc(max,·) allocator lands each S-allocation at the next slot … while no step removes one (C0/L12) and every other step frames the population (H0), so a gapless prefix stays gapless under any interleaving — and W1's part is the classification that argument yields."*
**Problem**: The gaplessness-preservation argument (inc(max,·) lands at next slot; C0/L12 remove nothing; H0 frames other homes) is given in full in A6 and re-derived in full in W1. W0 does the same for C0/L12/M1 (A6's transition clause transfers them via B2/RP-b; W0 re-argues "each step adjoins or frames, no removal"). The note narrates its own redundancy — "established here ahead of the two sections that use it" and "A6 established the preservation ahead of its consumers" are pure document-placement meta-prose, the exact accretion the anti-bloat classifier targets.
**Required**: Let A6 carry the preservation argument once; W0/W1 should cite A6 and state only their *new* content — W1's "collision, never a hole" failure-mode analysis and the Gregory counter-style-allocator contrast, W0's "needs only A0" classification — without re-deriving. Delete the "established here ahead of …" / "ahead of its consumers" placement prose.

### Issue 3: W1's recurrence "inc(slot φ, 0) = slot φ+1" overloads φ and reads as off-by-one
**ASN-0134, W1 (§5)**: *"the inc(max,·) allocator lands each S-allocation at the next slot inc(slot φ, 0) = slot φ+1"*
**Problem**: §4 binds `φ_S(d, Σ) = |P_S(d, Σ)|` and states *"the next emission lands at chain slot φ_S(d, Σ)"* — i.e. with φ filled slots (positions `0 … φ−1`), the frontier max is at slot `φ−1` and the next, empty slot is `φ`. The correct next-emission recurrence is therefore `inc(slot φ−1, 0) = slot φ`. W1 instead writes `inc(slot φ, 0) = slot φ+1`, which under §4's binding increments the *empty* next-slot and deposits at `slot φ+1`, skipping slot φ — literally describing a gap, the opposite of the gaplessness W1 is arguing. The intent is the generic chain recurrence (`chain_d(φ) → chain_d(φ+1)`), but reusing the bound symbol φ (= |P_S|) as a free index right after binding it makes the formula read as an off-by-one. A6's "inc(max,·)" states the same fact without the clash.
**Required**: Drop the formula in favor of A6's "inc(max,·) = next slot," or write `inc(slot φ−1, 0) = slot φ`, or rebind the generic index to a fresh symbol.

### Issue 4: §2 over-restates the canonical-vs-settled point
**ASN-0134, §2**: the paragraph from *"But A6 is a statement about structure …"* through *"… closed by construction."*
**Problem**: The load-bearing insight — *"incompleteness is not a property of the state at all, but a relation between the state and a batch … invisible from inside the snapshot"* — is genuine and earns its place, as do the two concrete examples (3-of-5 `retract_stale`, halted content run). But it is bracketed by echoes that add no new facet: *"Canonicity does not encode 'more is coming'"* and *"An observation is therefore never corrupt, yet its canonicity does not certify that it is final"* restate the same point already made by "Nothing in it is marked 'mid-batch.'"
**Required**: Keep the relation-not-property formulation and the examples; trim the two echo sentences.

## OUT_OF_SCOPE

The note's deferrals are correctly placed, not misclassified claims: cross-server composition of per-home orders (Open Question 6, with G1 named as the seam), reader-side multi-step batch atomicity (Open Question 4), and out-of-order-retraction semantics (Open Question 8) all belong in future notes, and the "What this note does not cover" section properly excludes scheduler fairness, rule bodies, BEBE, and the concrete CC mechanism. No action.

META: not applicable — MIC is an abstract contract any realization must meet (it explicitly forbids itself any mechanism), so this is a system-guarantee note, not implementation mechanics; it has not drifted.

VERDICT: REVISE
