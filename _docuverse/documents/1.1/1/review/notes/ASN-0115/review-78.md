# Review of ASN-0115

I checked every proof in the note line by line: the Confinement lemma, the force-empty override (both the shallow rationale and the deep-case no-op proof), UnitSpec (a)–(d), the R6 frontier analysis with its nominal-extent corollary, the R7 repeatability argument, the R8 vacuity argument for the link sub-case, and the R11 weakest-precondition analysis. I also re-derived the arithmetic in all four worked instances and ran the anti-bloat sweep the review-mode classifier requests. I found no defect requiring revision. Details on the load-bearing checks:

- **Confinement** is a correct application of T5: `p ≼ s` by construction, `p ≼ reach(σ)` because TumblerAdd copies positions below the action point `m`, and `s ≤ t ≤ reach(σ)` discharges T5's interval hypothesis. The counterexample for non-ordinal-level spans (`s = [1,5]`, `ℓ = [2,0]`, reach `[3,0]`, with `[2,3] ∈ ⟦σ⟧` in `s_L`) computes correctly.
- **The deep-case argument** (`#s > m_S(d)` ⟹ geometric intersection already empty) is complete: the two sub-cases `m_S(d) < m−1` (contradicts Confinement's length bound) and `m_S(d) = m−1` (prefix-at-equal-length forces `v = p`, then `p ≺ s` gives `v < s` against `v ≥ s`) exhaust `m_S(d) ≤ m−1`.
- **UnitSpec** discharges both document conjuncts (via M1's `dom(M) = E_doc` and ASN-0045's Document predicate) and closes the singleton-active-set claim through PrefixSpanCoverage plus S8-depth plus prefix-at-equal-length — every step is cited and valid.
- **R6's frontier analysis** correctly scopes the no-interior-hole claim to the bindable slice, handles all three branches of the `act` definition (including the `act = ∅`-with-`V_S(d) ≠ ∅` parenthetical, where the canonical-start derivation is unavailable), and the slice characterisation `{[S,1,…,1,k] : s_{m} ≤ k < s_{m} + ℓ_{m}}` follows from Confinement without circularity. The attainment biconditional holds in each branch; I verified the degenerate sub-case `s_m > n_S` (whole slice unbound forces `act = ∅`, both sides fail) is consistent.
- **R7** is sound: a shared bound position pins `m_S(dⱼ)` identically at both states, so depth-compatibility holds-or-fails identically; the empty-restriction case yields `act = ∅` in either branch; link items need no store invariant, content items close via S3★ + S0. The explicit counterexample to the converse (S4-permitted equal-valued rebinding) is a genuine derived consequence, not filler.
- **R8's link-vacuity** chain (CL-OWN forces `d = d'`, CL-UNIQ forces `v = v'`) is exactly right, and both invariants are per-state facts of every reachable state per ASN-0047.
- **R11's wp** is genuinely weakest: condition (i) is necessary by the definition of sourcing-through-resolution and sufficient via S3★ + S0, and the note correctly distinguishes source-address from value-appearance (S4).
- **Boundary cases**: empty spec-set (R0), empty arrangement, never-populated subspace, off-convention subspace identifiers (`S ∉ {s_C, s_L}` via S3★-aux), depth mismatch in both directions, terminal overrun, duplicate position named by overlapping specs, and cross-document assembly are all covered. The operation is a pure query, so no invariant-preservation obligations arise.
- **Anti-bloat sweep**: the rationale prose around the `act` override (discontinuity example plus staleness conclusion) is design justification that advances the definition rather than meta-prose; I found no defensive exhaustiveness claims, use-site inventories, duplicated paragraphs, or forward-deferral chains. All cross-ASN references are to foundation ASNs, and no foundation notation is reinvented.

## REVISE

No issues. Every introduced claim (R0–R11) carries an explicit derivation, the two auxiliary lemmas are proved step by step with per-fact citations, four worked instances verify the claims against concrete arrangements, and a non-trivial wp analysis is present.

## OUT_OF_SCOPE

### Topic 1: Rejection semantics for ill-formed requests
The ASN defines `deliver` only over well-formed spec-sets (allocated document, ordinal-level level-uniform span, V-position-shaped start). What the protocol does when handed an ill-formed spec — reject, error, or coerce — is unspecified.
**Why out of scope**: precondition-violating input is a protocol-surface concern for a future operation-contract ASN, not an error in this one; the note's Open Question on outright failure already gestures at it.

### Topic 2: Concrete payload of a link-reference item
R10 fixes that a link position delivers a reference distinguishable in kind from content, but what the reference must carry beyond the address (e.g., enough to invoke a read-by-address operation) is left open.
**Why out of scope**: reading a link's structure by address is READLINK territory (explicitly excluded), and the wire-level shape of `⟨ref, a⟩` belongs with the protocol/translation layer.

### Topic 3: Inline provenance for delivered content
R9 establishes that content-item origin is recoverable only through the resolution mapping, never from the output. Whether delivery must optionally carry origin inline is the note's own first Open Question.
**Why out of scope**: it is a new guarantee a future attribution-delivery ASN would introduce, not a gap in the delivery semantics specified here.

VERDICT: CONVERGED
