Reading the ASN as a system, tracking the precondition chains across claim boundaries, and checking each proof step against the cited foundations.

The bulk of the ASN is sound. The S8 chain-decomposition proof is well-constructed: succ injectivity via TS2 is correctly grounded in the unconditional depth-preservation frame (OrdShiftHom / TA0), not S8-depth's domain-restricted quantifier; the `shift(t, 0) := t` convention is explicitly introduced as an axiom before being invoked; the case split between i = 0 (convention) and i ≥ 1 (TS3) is exhaustive; OrdShiftHom parts (a) and (b) are invoked with their preconditions satisfied at each step; and the partition argument is constructive and complete. S3's inductive case split maps exactly onto AX-2's range selector. OrdShiftHom part (b)'s zero-count collapse through T4 and NAT-card's k = 0 case is correctly handled.

Two observations follow.

### `subspace` definition has no Formal Contract
**Class**: OBSERVE
**Foundation**: T0 (CarrierSetDefinition)
**ASN**: `subspace (VPositionSubspaceIdentifier)` — "For any tumbler `v` of depth `#v ≥ 1`, define: `subspace(v) = v₁`"
**Issue**: `subspace` is a named operator cited in the Depends of both S8-depth and OrdShiftHom, yet it carries no Formal Contract — no Depends (T0 supplies the `v₁` component projection), no formal preconditions block, no postconditions. Each citing claim describes what `subspace` provides ("supplies the projection `subspace(t) = t₁`"), but `subspace`'s own entry provides no corresponding grounding of the component projection in T0.
**What needs resolving**: Add a minimal Formal Contract to `subspace`: Preconditions (`v ∈ T` — T0's nonemptiness axiom `#a ≥ 1` guarantees `#v ≥ 1` for all `v ∈ T`, so no separate depth precondition is needed), Depends (T0 for the component projection `i ↦ vᵢ` at `i = 1`), and Postconditions (`subspace(v) = v₁ ∈ ℕ`).

### S8's Depends omits T0 despite direct use of `#·` in the Frame
**Class**: OBSERVE
**Foundation**: T0 (CarrierSetDefinition)
**ASN**: S8 (CorrespondenceRunPartition), Frame — "`#succ(v) = #v`" and body proof — "write `m = #v`, which by S8-depth is the common depth"
**Issue**: T0 supplies `#·: T → ℕ`, which appears as a first-class operator in S8's Frame condition (`#succ(v) = #v`) and directly in the proof body (`m = #v`). T0 is absent from S8's Depends. The specific result `#shift(v,1) = #v` is delivered by OrdShiftHom's frame (tracing to TA0 → T0), so T0 is accessible transitively — but the Frame and body write `#·` as a stand-alone operator rather than as a packaged postcondition of OrdShiftHom, which is the pattern that triggers direct citation elsewhere (S8a and S8-fin both cite T0 explicitly for the same operator in their own formal statements).
**What needs resolving**: Add T0 (CarrierSetDefinition, ASN-0034) to S8's Depends, noting it supplies the length operator `#·: T → ℕ` appearing directly in the Frame condition and in the body's introduction of `m`.

VERDICT: OBSERVE