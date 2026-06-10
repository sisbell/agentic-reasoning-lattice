# Review of ASN-0115

I reviewed this note as a delivery-semantics specification, checking each of R0–R11 against the substrate invariants it invokes, with particular attention to the `act` override mechanism (where the depth predicate reads state the well-formedness conditions don't fix), the boundary cases, and the anti-bloat classifier this note carries.

## Verification performed

I checked the load-bearing proofs in detail and found them sound:

- **Confinement lemma** (via T5): `p = [s₁,…,s_{m−1}] ≼ s`, `p ≼ reach(σ)` (ordinal-level reach copies the prefix), and `s ≤ t ≤ reach(σ)` give `p ≼ t` by T5. `#p = m−1 ≥ 1` holds since `m ≥ 2`. Correct, and correctly generalizes ASN-0058's C0a without reinventing it.

- **The override "bites only when `#s < m_S(d)`"**: I confirmed that for `#s > m_S(d)` the geometric branch `dom(M(d)) ∩ ⟦σ⟧` is already empty (any depth-`m_S` member of `⟦σ⟧` would force `m_S = m−1`, but that member equals `p < s`, excluded), so the override only changes the outcome when the start is too shallow. The added "shallow-depth guard" rationale is a correct, non-obvious claim, not reviser drift.

- **R6 no-interior-hole**: correctly scoped to the bindable slice (depth-`m_S`, subspace-`S`). `act ≠ ∅` pins the canonical start `s = [S,1,…,1,s_{m_S}]`, the slice is `{[S,1,…,1,k] : s_{m_S} ≤ k < s_{m_S}+ℓ_{m_S}}`, and D-SEQ★ makes `k ≤ n_S` bound, so unbound members are exactly the tail `k > n_S`. The deeper-named-positions disclaimer is explicit and correct. Holds for both subspaces (D-SEQ★ covers `s_L` via CL-UNIQ).

- **R7 repeatability**: the hard step — `act` agrees despite the depth predicate reading the whole subspace state — is handled correctly. A shared bound position in `⟦σⱼ⟧` fixes `m_S(dⱼ) = #v` at both states (S8-depth), making depth-compat hold-or-fail identically; the non-empty-restriction-but-override-fires case (`#v > #s`) is explicitly covered; the empty-restriction case yields `act = ∅` whichever branch each state takes. Comparability (not mere common ancestor) is correctly identified as necessary for S0 to fix content values.

- **R8 link vacuity**: the S3★/SD contrapositive dispatch fixing `subspace(v) = subspace(v')`, and the CL-OWN (`d = d'`) + CL-UNIQ (`v = v'`) argument forbidding distinct link positions from sharing an address, are both correct. Transclusion is genuinely confined to content.

- **R11 wp + worked instance**: the deletion-vs-removal distinction, the single live condition (i) decomposing into S3★-membership + S0-immutability, and the orphan-then-deliver-via-surviving-version scenario all check out.

Boundary coverage is complete for a query operation: empty spec-set (`p=0 ⟹ ⟨⟩`), empty/unallocated-subspace document, span starting before all positions, terminal overrun past the frontier, out-of-range subspace start (`act = ∅` via S3★-aux + Confinement), depth mismatch, transclusion, multi-origin, subspace crossing, and orphaned content. Worked instances are present for R6, R8, R9, R10, R11 and verify against the implementation evidence.

All referenced ASNs (0034, 0036, 0043, 0045, 0047, 0053, 0058, 0082, 0086, 0093, 0098) are foundation ASNs, so no improper cross-references. The note is appropriately abstract — R1–R11 are implementation-independent obligations — so no META concern.

## REVISE

None.

On the anti-bloat front: the justificatory asides I examined (the depth-compat mutability rationale, the "harmless other-subspace start" paragraph, the transmission-channel scope limit in §Faithfulness, the "not by D-SEQ★" clarification in R6, the synthesis recap) are each either a statement of what the operation does or does not do, a concrete boundary analysis, Nelson motivation, or implementation evidence — categories the anti-bloat carve-out explicitly protects — and each is in its correct slot. The git history shows recent cycles already tightened the `act` prose and dropped redundant depth-case material; I did not have to skip past meta-prose to follow any claim. Flagging the remaining protected prose would be a false positive.

## OUT_OF_SCOPE

The note's own Open Questions already defer the genuinely future topics (inline provenance recoverable from the delivered stream, permitted failure semantics, behavior under relaxed S3★/dangling references, channel faithfulness, and subspace-straddling spans). These are correctly held out rather than half-specified, and the Scope section correctly excludes the sibling RETRIEVE/FIND operations without smuggling claims about them into this note.

VERDICT: CONVERGED
