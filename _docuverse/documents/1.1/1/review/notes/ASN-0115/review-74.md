# Review of ASN-0115

## REVISE

No issues found. The verification work performed, so the verdict is grounded:

**Confinement lemma.** Checked the T5 application: `p ≼ s` is immediate, `p ≼ reach(σ)` follows from TumblerAdd's prefix-copy region (`rᵢ = aᵢ` for `i < actionPoint(ℓ) = m`) plus `#reach = #ℓ = m ≥ m − 1`, and `s ≤ t ≤ reach(σ)` follows from the half-open denotation. The `m = 2` boundary (`#p = 1`) satisfies T5's `#p ≥ 1` precondition. Sound.

**The `act` override.** The deep-case (`#s > m_S(d)`) argument that the geometric intersection is independently empty is complete: both sub-cases close — `m_S(d) < m − 1` contradicts Confinement's length bound, and `m_S(d) = m − 1` forces `v = p` by Prefix-at-equal-length, whence `v < s` by T1 case (ii) against `v ≥ s`. The shallow-case discontinuity example (`[S, 1]` vacuums a depth-3 subspace, `[S, 2]` captures nothing) is a genuine concrete witness, not meta-prose. The non-`{s_C, s_L}` subspace case is correctly dispatched through S3★-aux forcing `V_S(d) = ∅`, the first disjunct of `depthcompat`, and Confinement-disjointness.

**UnitSpec.** All four parts check: (a) shape from S8a plus `δ(1, #v)` properties; (b) S8-depth pins `m_S(d) = #v`; (c) both bounds — reflexivity for the lower, and the prefix-at-pinned-equal-depth collapse `t = v` for the upper; (d) exhaustiveness via S3★-aux.

**Nominal extent (§Exactness).** I verified the biconditional in every branch, including the two it does not name explicitly: depth-compatible with `V_S(d) = ∅` (slice non-empty, nothing bound, both sides false) and depth-compatible with a non-canonical start (slice disjoint from `V_S(d)`, both sides false). The slice cardinality `ℓ_{#ℓ}` holds without canonicality (Confinement pins the prefix; the last component ranges over `[s_{#s}, s_{#s} + ℓ_{#ℓ})`), and the `s_{#s} + ℓ_{#ℓ} − 1 ≤ n_S` form is correctly guarded by the canonical start that non-empty `act` forces. The forward deferral to the R6 frontier analysis is backed: the cited lemma ("active positions are exactly the bound members of the bindable slice") is actually established there, in both inclusions.

**R6 frontier analysis.** The canonical-start derivation from `act ≠ ∅` is sound; the bound-iff-`k ≤ n_S` characterization makes interior holes impossible and the unbound portion a contiguous terminal tail; the `act = ∅ ∧ V_S(d) ≠ ∅` parenthetical correctly renders the terminal-overrun half vacuous rather than overclaiming. The depth-incompatible and `V_S(d) = ∅` branches are each handled, not merged by "similarly."

**R7.** Both cases of the proof are present. The non-empty-restriction case correctly extracts a shared bound position to pin `m_S(dⱼ)` identically at both states, making `depthcompat` hold-or-fail identically — including the subtle sub-case where the restriction is non-empty yet the override discards it at both states. The M1 lift is composed per atomic step explicitly; the S0 lift over the finite sequence is immediate under SequentialTransitionAxiom. The non-biconditional caveat with the S4 rebinding witness is correct and correctly bounded.

**R8.** The subspace-sharing dispatch is complete: S3★-aux supplies the two-valued subspace premise, and the contrapositive of S3★ against SD closes each direction. The link-vacuity argument is fully discharged — CL-OWN forces `d = d'`, CL-UNIQ forces `v = v'` — and both are per-state invariants of reachable states, which the standing reachability precondition licenses.

**R11.** The wp is genuinely non-trivial: necessity and sufficiency of the single condition (i) are both argued, the store-membership conjunct is correctly shown redundant via S3★, and the postcondition is correctly pinned to source-address rather than value-appearance, with the S4 coincidence explicitly excluded from the converse.

**Worked instances.** All five check arithmetically — in particular the R6 instance's interval (`reach = [1, 7]`, slice `{[1,2]…[1,6]}`, `act` cut at the frontier `n_1 = 4`), its deeper-tumbler remark (`[1,2,1]` via T1 cases (ii)/(i)), and the R8 instance's reverse-order concatenation against V-magnitude.

**Boundaries.** Empty spec-set (`p = 0`), empty arrangement (subsumed by `V_S(d) = ∅`), zero-width spans (excluded by `Pos(ℓ)`), duplicate specs, and the document-allocation boundary R6 explicitly does not cover are all settled.

**Citations and anti-bloat.** Every cross-ASN reference resolves to a foundation ASN; no notation reinvention found. I scanned for forward-reference accretion per the classifier: the design-rationale prose around the override carries a concrete discontinuity witness and a proved equivalence (substantive, not defensive); the UnitSpec introduction advances the definition's content; the single forward-leaning paragraph (nominal extent) defers to analysis that genuinely exists downstream and states its bridging lemma inline. No paragraph re-litigates a case its carrier excludes; no duplicated prose pairs found.

## OUT_OF_SCOPE

### Topic 1: Single-span subspace straddling
**Why out of scope**: The ASN excludes boundary-crossing spans by the ordinal-level discipline and composes per-subspace spans instead; what delivery must guarantee for a straddling span is correctly parked in Open Questions as future territory.

### Topic 2: Transmission-channel faithfulness and inline provenance
**Why out of scope**: R2's frame limit and R9's kind-asymmetry correctly stop at the denotation of `deliver`; channel guarantees and inline-provenance obligations are new design territory, properly listed as open questions rather than claimed.

VERDICT: CONVERGED
