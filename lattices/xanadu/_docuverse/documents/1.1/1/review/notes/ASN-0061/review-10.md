# Review of ASN-0061

## REVISE

### Issue 1: D-PRE(iii) makes an unverified assertion about link-subspace deletion

**ASN-0061, Precondition section**: "subspace(p) = S where S ≥ 1 (text subspace; link-subspace deletion follows the same structure but we derive text-subspace first)"

**Problem**: The parenthetical claims link-subspace deletion "follows the same structure" without verification. It does not. In the extended framework (ASN-0047), the re-addition step for link-subspace positions requires K.μ⁺_L — a different elementary transition from K.μ⁺ — with different preconditions (monotonic link address ordering, `origin(ℓ) = d`). The link subspace also carries the additional invariant CL-OWN (link-subspace ownership), which K.μ⁺_L must preserve and whose preservation is not addressed anywhere in this ASN. The "same structure" claim is false at the transition level even if the three-region partition and shift logic carry over.

**Required**: Either (a) remove the claim entirely and restrict D-PRE(iii) to text subspace: "subspace(p) = S where S = s_C", noting link-subspace deletion is deferred; or (b) verify the link-subspace decomposition using K.μ⁻ + K.μ⁺_L with CL-OWN preservation.

### Issue 2: State model and framework scope are not declared

**ASN-0061, opening section**: "We work with system state Σ = (C, E, M, R) per ASN-0047."

**Problem**: ASN-0047 exports two state models: the basic state (C, E, M, R) with `ValidComposite` and `ReachableStateInvariants`, and the extended state (C, L, E, M, R) with `ValidComposite★` and `ExtendedReachableStateInvariants`. The ASN says "per ASN-0047" without specifying which. It then references the K.μ⁻ amendment — "The K.μ⁻ amendment (ASN-0047) requires D-CTG as a postcondition for contraction" — which belongs to the extended framework, while the invariant preservation section verifies only `ReachableStateInvariants` (the basic list). The basic K.μ⁻ already requires D-CTG and D-MIN as postconditions; the amendment reference is unnecessary and creates ambiguity about which framework governs.

The practical consequence: the extended invariants (L0, L1, L1a, L3, L12, L14, CL-OWN, S3★, S3★-aux, P3★, P4★, P5★) are not verified. All are trivially preserved — L' = L follows from the K.μ⁻ and K.μ⁺ frames, and D-XS covers CL-OWN — but this should be stated, not left implicit.

**Required**: One of: (a) Elevate to extended state Σ = (C, L, E, M, R). Add `L' = L` to D-CF. Add a paragraph to invariant preservation noting that all L-series invariants hold by L-in-frame and that S3★ holds by S3 (content subspace, verified) plus D-XS (link subspace, unchanged). Remove the K.μ⁻ amendment reference (basic K.μ⁻ suffices). Or (b) explicitly state that the ASN uses the pre-extension basic state model and that extended-framework verification is deferred, and remove the amendment reference.

## OUT_OF_SCOPE

### Topic 1: Generalization to V-position depth greater than 2

**Why out of scope**: D-PRE(iv) restricts to `#p = 2` (ordinal depth 1). The ASN correctly identifies this as a genuine limitation: at ordinal depth > 1, TumblerSub applied to ordinals like `[1, 1, k]` with displacement `[0, 0, c]` diverges at position 1 (where `1 ≠ 0`), producing `[1, 1, k]` unchanged — the subtraction never reaches the last component. So D-SEP's round-trip property fails, and the gap-closure shift cannot be expressed as `ord(v) ⊖ w_ord`. D-SEQ (ASN-0036) shows that V-positions at any depth are sequential in the last component, so the generalization is structurally plausible but requires a new arithmetic operation (last-component subtraction) not currently in the tumbler algebra.

VERDICT: REVISE
