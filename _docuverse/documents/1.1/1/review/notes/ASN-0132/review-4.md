# Review of ASN-0132

I checked each claim against its cited foundations and re-ran the load-bearing derivations. The substantive checks:

- **CN-MONO's WP derivation** — I verified the pre-existing-link stability (`Σ'.L(a) = Σ.L(a)` by L12/LP13; `sat` stable by CN-LOC; `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` because `ℓ` ordinary gives `L_R^{Σ'} = L_R^Σ`), the new-link contribution reducing to `sat(ℓ,q,Σ') ∧ ¬(E (b,F',G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))`, and the collapse to `sat(ℓ,q,Σ')` under unit-depth discipline (the `t ≼ ℓ` with `t ∈ dom(Σ.L)`, `ℓ ∈ dom(Σ'.L)`, R0a antichain argument). This matches FL-WP(a) exactly. The earlier F-LAMBDA/E-INV misattributions are resolved — the derivation now correctly uses `sat`-level lemmas, not the slot-agnostic `matches`-level ones.
- **CN-UNIT(d)** — confirmed J4 (ForkComposite) = K.δ + K.μ⁺(content) + K.ρ with "no other elementary steps," so `Σ.L` is untouched by forking and the version case correctly reduces to appearance multiplicity (c).
- **The concrete example** — I recomputed `coverage(F) = [1.0.1.0.1.0.1.5, 1.0.1.0.1.0.1.13)` (ordinals 5–12), the five links' contributions, `nullified(Σ) = {a₂}`, `addressable = {a₁,a₃,a₄,a_R}`, and all three count routes to 2. The wildcard census (4), `q_H` (2, all homed at d₁), and `q_H'` (genuine non-degenerate CN-ZERO, d₂ prefix-incomparable to d₁) all check out, including a₄ excluded by FL-RES.
- **Citation hygiene** — every body citation resolves to a foundation ASN (0034/0036/0043/0047/0058/0086/0093/0098/0121/0127). The note uses `sat` rather than re-deriving the four-slot match semantics, respecting the scope boundary with ASN-0121.
- **Implementation notes** correctly ground the abstract claims against Gregory's back end (dedup defect ↔ CN-UNIT; shared routine ↔ CN-SHARED; full-enumeration cost ↔ the cost non-claim) without drifting into mechanics — the CN-* claims remain abstract guarantees about the count as a function of state.

## REVISE

None. The proofs are shown or correctly cited; boundary cases (empty satisfying set → CN-ZERO, all-wildcard → max, empty-coverage slot → FL-EMP, reverse-orphaned link, addressable retraction tuple counted) are each handled; the WP analysis is non-trivial and fully derived; the concrete example verifies the key claims against a specific store; consequences (snapshot vs permanence, existence vs discovery, active-view vs store) are explored in depth.

## OUT_OF_SCOPE

### Topic 1: The six Open Questions the ASN raises
**Why out of scope**: V-spec/address-set count agreement, cross-inquiry concurrency consistency, durable-cache conditions, fragmentation dedup guarantees, count-vs-enumeration cost relationship, and federated count are all correctly externalized as Open Questions rather than smuggled in as claims. They are future territory, not gaps in this ASN. In particular the dedup defect (Open Q #4) is properly framed as a deviation *from* CN-UNIT, not a flaw in it, and the cost relationship (Open Q #5) is explicitly declined as a correctness obligation — the right call, since an implementation that computes the cardinality by materializing the set is correct as to value.

VERDICT: CONVERGED
