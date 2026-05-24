# Review of ASN-0094

## REVISE

### Issue 1: Appendix's `(Peano-pred)` order-conformance derivation is incomplete

**ASN-0094, Appendix: Local NAT Primitives**, in the `(Peano-pred)` clause:
> "the predecessor `m'` satisfies `n ≤ m'`: from `n < m = m' + 1`, NAT-discrete's contrapositive at `n, m' + 1` gives `n + 1 ≤ m' + 1`; by successor injectivity (applied to the inequality `n + 1 ≤ m' + 1`'s case-equality branch, or via NAT-addcompat's order-compatibility of addition reversed at the `+ 1` argument) reduces this to `n ≤ m'`."

**Problem**: The brief invocation handles only the equality sub-case of `n + 1 ≤ m' + 1` (via successor injectivity). The strict sub-case `n + 1 < m' + 1` is not explicitly handled, and "NAT-addcompat's order-compatibility reversed" is not derived from the listed foundation axioms — NAT-addcompat is stated forward-direction only. The full argument requires either (a) explicit case-split on NAT-order's `≤` defining clause, treating equality via successor injectivity and the strict case via trichotomy plus the appendix's derived strict-monotonicity-of-addition plus irreflexivity, or (b) explicit derivation of "reversed NAT-addcompat" before invoking it.

**Required**: Walk both sub-cases of `n + 1 ≤ m' + 1` explicitly:
- Equality sub-case (`n + 1 = m' + 1`): apply successor injectivity to get `n = m'`, hence `n ≤ m'`.
- Strict sub-case (`n + 1 < m' + 1`): apply trichotomy on `n, m'`; the `m' < n` branch yields `m' + 1 < n + 1` by the strict-monotonicity derived later in the appendix, composing with `n + 1 < m' + 1` to violate irreflexivity; the remaining branches `n < m'` and `n = m'` both yield `n ≤ m'`.

This matters because the order-conformance consequence is consumed by NAT-sub's *Case B* to license the IH invocation at the predecessor; downstream proofs (LinkAddressNotPrefixOfEmit's Step II.0 suffix-length construction, Step II.1's `zeros(w) = 0` closure) cite NAT-sub by name, so the appendix gap propagates if NAT-sub is to be derived rather than treated as an axiomatized primitive.

### Issue 2: Sh4 idempotency contract's "Contract correctness is independent of clause (d)" claim has implicit reasoning

**ASN-0094, Sh4 idempotency contract clause (i.a)**:
> "Contract correctness is independent of clause (d) on the new emission's F. The contract's correctness — that the candidate set `C(F, G, Σ)` it computes equals the specified `{τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F) ∧ slot_addrs(G_τ) = slot_addrs(G)}` — does not depend on whether the new emission's F satisfies Sh-conf clause (d); it depends only on (i.a)'s Observe returning a finite over-approximation and (i.b)'s post-filter exactly testing slot-address-set equality."

**Problem**: The claim asserts correctness without showing the reverse-inclusion `{τ ∈ A_K^Σ : slot_addrs(F_τ) = slot_addrs(F) ∧ slot_addrs(G_τ) = slot_addrs(G)} ⊆ C(F, G, Σ)` holds independent of clause (d). The argument requires noting that for every τ in the specified set, Observe_K returns τ because `slot_addrs(F) ⊆ coverage(F_τ)` holds by reflexivity of ≼ at each `x ∈ slot_addrs(F)` (since `x ∈ {t : x ≼ t} ⊆ coverage(F_τ)` when `slot_addrs(F) = slot_addrs(F_τ)`). The reflexivity argument doesn't require `x ∈ A^Σ`, so the inclusion holds at any state.

**Required**: A one-sentence justification noting the reflexivity-of-≼ argument that closes the reverse inclusion at every τ in the specified set, independent of whether the pattern addresses are allocated. This makes the "independent of clause (d)" claim verifiable without the reader having to construct the argument.

### Issue 3: SubstrateConsumerActiveSubsetCompatibility's exhaustiveness proof has an underspecified step

**ASN-0094, Lemma — SubstrateConsumerActiveSubsetCompatibility, Path (a)**:
> "Consider a hypothetical layer-side mutation of `X` that changes its value between two otherwise-identical reachable states `Σ_a, Σ_b` with `Σ_a.C = Σ_b.C, Σ_a.M = Σ_b.M, Σ_a.L = Σ_b.L` and `X(Σ_a) ≠ X(Σ_b)`."

**Problem**: The argument presupposes the existence of two reachable states with identical `(Σ.C, Σ.M, Σ.L)` projections but differing `X(·)` values. This existence is not derived from the framework's transition vocabulary; it is asserted as a hypothetical. The framework's `↦` Definition (consumed via the *DomExtendingTransition* and *BroadExtension* definitions of ASN-0086) only commits to transitions touching `(Σ.C, Σ.M, Σ.L)` — `X` outside the scaffolding interface is not part of `↦`'s vocabulary, so there is no transition mechanism in the framework's scope that updates `X` without touching `(Σ.C, Σ.M, Σ.L)`.

**Required**: Either (a) explicitly qualify the hypothetical as "for layers admitting transitions outside `↦`'s scope" so the reader understands the construction is at the consuming layer's side, not the framework's; or (b) replace Path (a) with a direct semantic argument that `φ_S`'s value on a `↦`-reachable state cannot depend on data outside `(Σ.C, Σ.M, Σ.L)` if `φ_S` is preserved under the framework's `⊥`-extension. The current formulation leaves it ambiguous whether the exhaustiveness proof relies on a transition vocabulary the framework doesn't formally admit.

### Issue 4: Sh4 Case D's case-description equation `A_R^{Σ'} = (A_R^Σ ∪ {τ_new}) \ leaving` lacks a derivation step

**ASN-0094, Sh4 preservation proof, Case D**:
> "the post-step active subset is `A_R^{Σ'} = (A_R^Σ ∪ {τ_new}) \ leaving` where `leaving := {τ ∈ A_R^Σ : addr(τ) ∈ coverage(G_{τ_new})}`"

**Problem**: This equation is presented as a structural fact established by "Lemma — RetractionSelfFreshness (... τ_new ∈ A_R^{Σ'})" combined with "nullified(·)-membership filtering". But the framework's `A_K^Σ` Definition (ASN-0086) computes the active subset from `L_K^Σ` filtered by `nullified(Σ)` — the post-step nullified set is `nullified(Σ') = nullified(Σ) ∪ {a ∈ A_rel^{Σ'} : a ∈ coverage(G_{τ_new})}`, and the active subset becomes `A_R^{Σ'} = {τ ∈ L_R^{Σ'} : addr(τ) ∉ nullified(Σ')}`. The equation `A_R^{Σ'} = (A_R^Σ ∪ {τ_new}) \ leaving` is the unfolding of this, but the equivalence relies on (i) `{τ_new} \ leaving = {τ_new}` (since τ_new ∉ A_R^Σ, hence τ_new ∉ leaving) and (ii) `{τ ∈ A_R^Σ : addr(τ) ∉ coverage(G_{τ_new})} = A_R^Σ \ leaving`. Neither step is shown explicitly.

**Required**: A short derivation step unfolding the equation against ASN-0086's `A_K^Σ` Definition: `A_R^{Σ'} = (A_R^Σ \ leaving) ∪ {τ_new} = (A_R^Σ ∪ {τ_new}) \ leaving` (the second equality holds because `τ_new ∉ leaving` follows from τ_new being absent from A_R^Σ by RetractionSelfFreshness's freshness clause). This makes Case D's structural claim verifiable from ASN-0086's stated definition rather than left as an implicit set-theoretic identity.

### Issue 5: Worked example for Case 3 Sub-case 3b is omitted

**ASN-0094, AllocatedAddressAntichain proof**:
> "The general subspace-contradiction route (Steps 3.1, 3.2, 3.3b) remains in the formal proof above because the lemma is stated against the bare L1b hypothesis (where `#E(·) ≥ 2` does not force length equality on either side), but no concrete worked example is supplied for Sub-case 3b: on the substrate-conforming layer the case is unreachable by either route, and any illustrative example would necessarily exhibit a configuration the substrate never produces."

**Problem**: The framework explicitly omits a concrete walkthrough for Sub-case 3b, citing unreachability. But the lemma's *formal proof* commits to handling Sub-case 3b through Steps 3.1, 3.2, 3.3b. Without a worked example matching the symbol-by-symbol parallel to Sub-case 3a (the rationale for Sub-case 3a's worked example: "exhibit the cross-domain contradiction concretely"), the proof's symmetry claim — that Steps 3.3a and 3.3b parallel each other modulo identifier substitution — is harder to verify by a reader exercising the proof on concrete values. The "Dependence audit on Step 3.3" preamble identifies three sites where domain membership is consulted, but the reader has no concrete companion example to anchor the audit.

**Required**: Either (a) supply a worked example for Sub-case 3b at the same depth as Sub-case 3a's example (using a hypothetical configuration that exhibits the steps without claiming substrate-reachability), explicitly framing it as a *counterfactual* walk to validate the proof's symmetry, or (b) restructure the omission with a clearer justification — e.g., note that since Sub-case 3a's worked example is "an example the substrate never produces" too (it exhibits a configuration that AllocatedAddressAntichain itself rules out), the asymmetry in the worked-example coverage is artificial.

## OUT_OF_SCOPE

The Open Questions section already documents the framework's scope boundaries (cross-process consistency, ghost-targeting slot semantics, `(0, 0)` shapes, composite shapes, per-K opt-in promotion to a sixth shape component). No additional out-of-scope topics surfaced during this review.

VERDICT: REVISE
