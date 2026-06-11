# Review of ASN-0111

Before the verdict, a record of what was actually checked, since CONVERGED is only as good as the checking behind it.

**Verified line by line:**

- **RL0 / wp derivation.** The substitution `wp(result := readlink(a, Σ), R_ok) ≡ a ∈ dom(Σ.L)` is correct, the guard in `R_ok` does make the dereference well-formed on every state, and the two wps are genuinely complementary. The insufficiency argument is sound: Σ₀ is reachable (the `→*` closure is reflexive), `dom(Σ₀.L) = ∅`, so any satisfiable address-only predicate has a witness falsifying sufficiency at `(a, Σ₀)`.
- **Structural screen well-definedness.** The chain `T4-valid(a) ∧ zeros(a) = 3 ⟹ #E(a) ≥ 1` is correctly discharged from T4a/T4b/T4c, and the example `[1, 0, 0, 2, 0, 3]` does fail T4 at the adjacent-zero clause, so left-to-right evaluation short-circuits as claimed. All four necessity citations (L0b, L1, L0, L1b) are correct.
- **RL4 witness construction.** I re-derived the bootstrap chain (`inc([1], 2) = [1.0.1]`, zeros 1; `inc([1.0.1], 2) = [1.0.1.0.1]`, zeros 2; parent and freshness conjuncts discharged at each step). The branch-then-converge argument is sound: K.λ's precondition constrains the value only through L3, both branches agree on `dom(L)` and `dom(M)`, so the step at `c = inc(a', 0)` is enabled identically and allocates the same address. `a' ∈ coverage(ℓ_c.e₂)` holds by PrefixSpanCoverage plus reflexivity of `≼`. The flattening-reader refutation follows. SOV's vacuity argument for J0/J1★/J1'★ is correct for K.δ/K.λ-only composites (a freshly registered document contributes an empty content-subspace range, so J1★ stays vacuous).
- **RL5 permanence families.** I recomputed all three example addresses: `[1.0.1.0.1.0.2.1.1]` (E = [2,1,1], screen passes, excluded by LP-Sub's `#E = 2` form of F), `[2.0.1.0.1.0.2.1]` (screen passes; the L1a → P8 → P8 → NodeLineage chain correctly refutes at `[2]₁ ≠ 1`), and `[1.0.1.1.0.1.0.2.1]` (zeros at 2, 5, 7, non-adjacent; U = [1,1]). The account induction is complete: accounts arise only via k = 2 from a node (user field `[1]` by TA5(d)) or k = 0 from an account (TA5(c) + TA5-SigValid modify only the terminal component, preserving `#U`); the k = 1 branch takes only document operands and case (i) makes nodes; K.δ is the only E-extending transition.
- **Exhaustiveness of the split.** The residual-class allocatability construction is sound at each stratum: node baptism needs only `N(a)₁ = 1` (since `n₀ = [1]` has length 1, `n₀ ≼ N(a)` is exactly that test); the account and document chains stay contiguous because K.δ's freshness conjunct, via FrontierEquivalence, lets `inc(·, 0)` fire only at frontiers, so "reached or already present" is justified; every zero-free document field is realised by the alternating k = 1 / k = 0 scheme; the element step correctly gets `j₀ < k` from `a ∉ dom(Σ.L)` plus ChainMembershipForOrigin's contiguous-prefix form.
- **Worked read.** Arithmetic checks out: `[1.0.1.0.1.0.1.1] ⊕ δ(2, 8) = [1.0.1.0.1.0.1.3]`; the two-subtree decomposition of the half-open interval via PrefixSpanCoverage is correct; the three F-candidates in `coverage(F)` match LP-Fin Corollary (n = 2 and n = 1 respectively). The reachability route is now fully discharged: J0/J1★/J1'★ at the three K.α composites, J2/ContractionIsolation for the K.μ⁻ steps (with the strict-contraction precondition satisfied at `n' = 0 < 2` and `0 < 1`, and D-CTG★/D-MIN★ vacuous on the emptied subspace), P2/P4★/P7a at subsequent boundaries, and SOV for the bare K.λ steps. The orphan hypothesis is consistent with the constructed state.
- **Boundary cases.** Absent address (⊥), Σ₀, empty connective endsets, ghost type, arity > 3, nested link target, frontier address read before/after its allocating step, orphaned link — all covered in the text.
- **Standards.** Only foundation ASNs are cited; no foundation notation is reinvented; the concrete example exercises every load-bearing postcondition; the caching trichotomy supplies the non-trivial consequence analysis the wp's simplicity would otherwise leave missing. I also checked for anti-bloat patterns per the standing classifier: the SOV lead-in and the single "proved below" forward reference are brief orientation, not deferral chains; I found no relocated-finding residue, no duplicated paragraphs, and no defensive meta-prose rising to a finding. (One note examined and deliberately not flagged: `F` names both the substrate-emittable set in RL5 and the from-endset in the worked read — but both notations are mandated by their respective foundations, the contexts are disjoint, and the only available "fix" would be exactly the kind of disambiguating meta-prose the anti-bloat discipline removes.)

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Distinguishability of value-identical links from read results alone
**Why out of scope**: The ASN's third open question — whether the read contract should surface the address alongside the value so that two links with identical recorded structure are distinguishable from results — is a caller-protocol design decision for a future ASN, not a defect in this one; `readlink` as specified is value-returning and correct on its own terms.

### Topic 2: Validity/currency semantics of a read relationship
**Why out of scope**: What a reader may conclude about a relationship's continued resolvability requires arrangement consultation, which is FOLLOWLINK territory (explicitly excluded by the scope list); RL6 correctly stops at "recorded, not resolved."

### Topic 3: Caching under replication
**Why out of scope**: The RL5 caching discipline is sound for the single-server, sequentially-ordered state of SequentialTransitionAxiom; staleness across replicas belongs to the inter-server protocol (BEBE), excluded by the scope list.

VERDICT: CONVERGED
