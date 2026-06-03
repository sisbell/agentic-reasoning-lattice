# Review of ASN-0077

I read the full ASN and checked the proofs of O0–O14 (with corollaries, multi-step companions, the two wp characterisations, both edge-case batteries, and the worked example) against the foundation contracts.

## Verification performed

- **Foundation discipline.** Every external citation resolves to a listed foundation (ASN-0034/0036/0040/0047/0053/0058/0098). `L1b` and `C1b`, referenced for `#E ≥ 2`, are confirmed members of ASN-0047's `ExtendedReachableStateInvariants` list, so the citations are legitimate even though their standalone statements weren't extracted. No non-foundation cross-reference appears in the body, and no foundation notation is reinvented.
- **Singleton I-span proof.** The three length cases (`#b < #a` excluded via T1 case-(i) divergence at `k ≤ #b < #a` driving `a⊕ℓ < b`; `#b = #a` by T3; `#b > #a` by prefix-coincidence + zero-count balance) are each fully expanded — including the `actionPoint(ℓ) = #a ≤ #a` boundary and the NAT-discrete squeeze at position `#a`. No "similarly," no unstated case.
- **O2 / equivalence chain.** M-int's interval precondition (`vⱼ ≤ vⱼ+i < vⱼ+nⱼ` via TS5) and M16a's two-conjunct precondition are both discharged before use; the content/link split is exhaustive by S3★-aux; the chain correctly notes O2 (not M16a alone) discharges the link-block collapse.
- **O11 / O11' (⊇) direction.** The impossibility of newly-added positions falling in `⟦σ⟧` is established by the cross-state depth identification (`m' = m` from S8-depth over `V_{s_C}|_Σ ⊆ V_{s_C}|_{Σ'}`, using state-independence of `subspace`/`#`) and by C0a subspace confinement — and crucially it invokes *pre-state* precondition (vi). Sound.
- **Closure handling.** O11★/O11'★/O11★★ rest on the binary `modifies-M(d)` / `leaves-M(d)-fixed` partition rather than a transition-vocabulary enumeration, so the proofs are robust to vocabulary extensions. The negative claims O13 (admissibility loss under K.μ⁻) and O14 (incomparability under K.μ~) correctly bound the preservation regime, each with a concretely-discharged witness in the worked example (K.μ~ admissibility clauses (a)/(b)/(c) verified individually).
- **Boundaries.** Empty I-span intersection, empty-document inadmissibility, empty-restriction-in-nonempty-document (non-empty via TA-strict + (vi)), link-subspace V-span trivialising to `{d}`, and cross-subspace I-span dropping link addresses are all addressed.
- **wp analysis is non-trivial.** The single-origin wp is evaluated at both a falsifying (`σ_cover`, multi-origin) and satisfying (`σ_{d₁only}`) configuration; the membership wp is checked against the `d_q = d₂` falsifier, which is the operational confirmation of O4 (no chain walking).

I found no hand-wave, no skipped case, no checkmark-as-proof, and no over-claim. The minor imprecision in O1(c) ("the outputs of A_C(d)" where the class is those outputs lying in `⟦σ⟧ ∩ dom(C)`) is disambiguated by its own derivation context and does not affect correctness.

## OUT_OF_SCOPE

### Topic 1: Reporting link origins from an I-span
**Why out of scope**: The I-span lift restricts to `dom(C)` by definitional choice; the cross-subspace case is explicitly deferred to Open Question 1. This is new territory, not an error.

### Topic 2: Surfacing the intermediate transclusion chain; native-vs-transcluded distinction; historical containment from Σ.R
**Why out of scope**: Each is named as a separate operation in the Open Questions and correctly excluded from SHOWORIGIN's direct-answer contract.

VERDICT: CONVERGED
