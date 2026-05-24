# Review of ASN-0094

## REVISE

### Issue 1: NAT-sub appendix's derivation of right-identity glosses over successor injectivity
**ASN-0094, Appendix: Local NAT Primitives, "Derivation of an auxiliary right-identity-and-successor-distributivity bundle"**: "Both lemmas are proved jointly by induction on n: the joint induction's base (n = 0) discharges right-identity via NAT-closure's additive identity 0 + 0 = 0 at the m = 0 instance and via (Peano-rec) at m to extend"

**Problem**: The inductive step extending right-identity from `m` to `m+1` (deriving `(m+1) + 0 = m+1`) cannot close from {NAT-closure, Peano-rec, IH} alone. Peano-rec at substitution `(m, n) := (m+1, 0)` gives `(m+1) + 1 = ((m+1) + 0) + 1`, but cancelling `+1` to obtain `m+1 = (m+1) + 0` requires successor injectivity — itself derivable only by a multi-step argument from NAT-discrete's contrapositive (`m < n ⟹ m+1 ≤ n`), NAT-addcompat's strict-successor inequality (`n < n+1`), and NAT-order's irreflexivity/transitivity. None of this is shown. The "(Peano-rec) at m to extend" phrasing is too compressed to make the bridge visible. The bundle is presented as self-closing via Peano-rec, which it is not.

The conclusion (right-identity, ℕ-commutativity, ℕ-associativity, NAT-sub) is standard arithmetic and undisputed; the issue is the *derivation path*. Since LinkAddressNotPrefixOfEmit's Step II.0 (suffix-length definition via NAT-sub) and Step II.1 (additivity via NAT-card, which the appendix derives from the same chain) feed EffectiveWpSimplification's Step 1, the gap is load-bearing for the framework's wp simplification.

**Required**: Either (a) derive successor injectivity inline from NAT-discrete + NAT-addcompat + NAT-order, then apply it to Peano-rec to close the right-identity inductive step explicitly; or (b) acknowledge right-identity as an additional Peano-core foundation primitive alongside (Peano-rec), with the rigorous derivation deferred to a foundation extension. The current text reads as if Peano-rec self-suffices for the inductive step, which it does not.

## OUT_OF_SCOPE

### Topic 1: Cross-process concurrency for layer-discipline contracts
**Why out of scope**: The framework explicitly commits to single-process substrate scope. The Sh4 idempotency contract, FDD functional-dependency contract, and single-home commitment all reduce atomicity to within-call sequentiality of Observe and Emit. Distributed-emitter coordination is flagged as [scope boundary] in Open Questions.

### Topic 2: Per-shape uniformity at the body-shape level
**Why out of scope**: The framework deliberately downgrades body-shape-level convergence between shape-mate catalog rows from a commitment to a hand-curation aspiration. The catalog's current convergence (DirectedPair/Resolution sharing five base templates; the two `(0, 1)` rows sharing `is_K`) is exhibited rather than mechanically guaranteed. A future catalog row at the same shape proposing divergent bodies would violate no framework gate.

### Topic 3: Target-domain symbol for dom(Σ.M) container addresses
**Why out of scope**: Shape constraints cannot target document-level containers (zeros = 2). The framework provides symbols only for `A_doc = dom(Σ.C)`, `A_rel = dom(Σ.L)`, and their union. This is documented as a structural limit; a layer needing container-targeting relations must designate a content address per container.

VERDICT: REVISE
