# Review of ASN-0132

This is a strong, late-stage ASN. The counting operation is defined as the cardinality of the same satisfying set the enumeration carves out (CN-DEF, CN-SHARED), which makes count-equals-length structural rather than an obligation (CN-ENUM). The unit-of-counting argument (CN-UNIT) walks all four competing units and rejects each by a distinct property; the transition analysis correctly identifies K.λ as the *unique* count-moving transition, backed by F-PRES's exhaustive coverage of the non-K.λ vocabulary (CN-STAB); and the worked example checks out arithmetically against six claims. I verified the example's address structure, coverages, the `nullified`/`addressable` computation, and all four request variants (`q`, `q*`, `q_H`, `q_H'`) — all correct.

I found one genuine skipped step.

## REVISE

### Issue 1: Elided monotonicity step in CN-MONO's unit-depth collapse
**ASN-0132, "Retraction and permanence" (CN-MONO wp derivation)**: "*a unit-depth retraction's to-coverage is a prefix subtree {s : t ≼ s}, so ℓ ∈ coverage(G') would force t ≼ ℓ; but t ∈ dom(Σ.L) and ℓ ∈ dom(Σ'.L) with dom(Σ'.L) a prefix antichain (R0a, ASN-0086) forces t = ℓ, contradicting freshness.*"

**Problem**: R0a is the statement that *dom(Σ'.L)* is a prefix antichain — it forces `t = ℓ` from `t ≼ ℓ` only when **both** `t` and `ℓ` lie in `dom(Σ'.L)`. The sentence establishes `ℓ ∈ dom(Σ'.L)` and `t ∈ dom(Σ.L)`, but not `t ∈ dom(Σ'.L)`. The application of the antichain to the pair `(t, ℓ)` is therefore not licensed by the memberships as stated; it needs the link-store inclusion `dom(Σ.L) ⊆ dom(Σ'.L)`. This is the only micro-step left implicit in an otherwise fully-discharged wp argument (the three "pre-existing contributions unmoved" sub-steps and the `ℓ ∉ nullified(Σ')` reduction are each spelled out and cited). It is minor — the inclusion is immediate, the conclusion `t ⋠ ℓ` is robustly true — but the ASN's own per-step convention (inherited from the foundations' obsessive Depends discharge) makes the omission a small inconsistency with its standard.

**Required**: Insert the inclusion before invoking R0a: "*t ∈ dom(Σ.L) ⊆ dom(Σ'.L) (link-store monotonicity, L12a / Store Monotonicity★, ASN-0098), and ℓ ∈ dom(Σ'.L); R0a applied to dom(Σ'.L) then forces t = ℓ from t ≼ ℓ, contradicting freshness.*"

## OUT_OF_SCOPE

### Topic 1: V-to-I resolution of a content-pointing query into the address-phrased request `q`
**Why out of scope**: The ASN correctly takes `q` as already resolved over addresses and isolates the resolution boundary as upstream; this matches the scope exclusions (content delivery, ASN-0098-layer projection) and Open Question 1. The discrepancy between count-stability and a reader's re-phrasing is correctly attributed to resolution, not to the count.

### Topic 2: Cross-inquiry consistency, caching durability, federation, and cost-vs-enumeration asymmetry
**Why out of scope**: The ASN raises these as Open Questions and declines to elevate cost-asymmetry to a correctness obligation (CN-OBT and the closing section). This is the right call — CN-DEF fixes the *value*; a back end that materialises the set to count it is correct as to value. Federation (BEBE) and concurrency are explicitly excluded by the scope list. No coverage is owed here.

The four-set match semantics, the existence/discovery taxonomy, and link enumeration itself are cited from ASN-0121/ASN-0127 (foundations) rather than rebuilt — correct per scope.

VERDICT: REVISE
