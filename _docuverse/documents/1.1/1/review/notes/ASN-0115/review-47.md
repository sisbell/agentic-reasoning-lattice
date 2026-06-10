# Review of ASN-0115

## REVISE

### Issue 1: Depth-compatibility is folded into V-spec well-formedness as an undefined-state "minting-time requirement" that no claim uses

**ASN-0115, "What a spec-set is, and what delivery is"**: "We further require *depth compatibility* with the named subspace: ... when `S` is already populated in `d` (`V_S(d) ≠ ∅`) the start must match that subspace's common depth, `#s = m_S(d)` ... This depth match is a *minting-time* requirement on a well-formed V-spec. ... The depth conjunct is therefore re-evaluated at each consulting state, not fixed at mint."

**Problem**: Every *other* conjunct of V-spec well-formedness is a timeless structural property of the pair `(d, σ)` — the S8a shape of the start, level-uniformity, ordinal-level — with the one exception of document allocation `d ∈ dom(Σ.M)`. The allocation conjunct is *monotone* (M1, ArrangementMonotonicity), so "checked at minting" legitimately transfers to every later consulting state and the claims may assume it. The depth conjunct is **not** monotone — the ASN itself stresses `m_S(d)` is re-pinned after a full clearance — and this breaks the treatment two ways:

1. *Ill-defined.* The well-formedness predicate references `m_S(d)`, a state-dependent quantity, at a state ("minting time") that the formalism never defines or parameterizes. `deliver(R, Σ)` takes a consulting state `Σ` and nothing else; there is no minting-state argument anywhere. A well-formedness predicate whose truth value depends on an unformalized state is not well-defined.

2. *Inert.* `deliver`, `act`, and every claim R0–R11 consult only the *consulting-state* `depthcompat(ρ, Σ)` inside the `act` override — never the minting-time gate. In particular R6's canonical-start derivation (`act ≠ ∅ ⟹ s = [S, 1, …, 1, s_{m_S}]`) is driven by D-SEQ★ on a bound position at `Σ`, not by minting-time depth; and R7's repeatability proof re-derives equal-or-failing `depthcompat` at the two consulting states from S8-depth on a shared bound position. Nothing leans on the gate.

The contrast with the monotone allocation conjunct is exactly what exposes the defect: allocation can be checked once because it transfers; depth cannot, so it is re-checked, and the "requirement" half is then pure overhead. The result is dual machinery — a well-formedness gate plus the `act` override — whose first half is never load-bearing, accompanied by defensive re-explanation in the V-spec paragraph and again in the `act` override discussion ("the override only bites when the start has gone too shallow ... when the start is too deep ... vacuous no-op").

**Required**: Drop depth-compatibility from V-spec well-formedness. Define a V-spec by its timeless structural conditions plus the monotone allocation conjunct `d ∈ dom(Σ.M)`, so the predicate is fixed without reference to any "minting" state. Let `act`'s consulting-state `depthcompat(ρ, Σ)` be the sole depth check (it already is, formally), and collapse the re-evaluation prose into that single definition. The claims are unaffected, since they already use only the `act` form.

## OUT_OF_SCOPE

The ASN's own Open Questions correctly defer the genuinely-future topics (inline provenance carriage, fail-outright conditions, dangling references under relaxed S3★, delivery-channel faithfulness, and the single straddling span crossing both subspaces). None of these is an error in this ASN, and the body does not over-reach into them — R10 in particular delivers a link *reference* and explicitly disclaims reading link structure (READLINK, out of scope). No additional out-of-scope concerns.

VERDICT: REVISE
