# Regional Review — ASN-0034/OrdinalDisplacement (cycle 1)

*2026-04-24 06:33*

### Redundant derivation of `0 < 1` in OrdinalDisplacement

**Class**: REVISE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity) — its *Axiom* bullet directly posits `0 < 1` as "distinctness of the two named constants".
**ASN**: OrdinalDisplacement's derivation of `n ≥ 1 ⟹ n ≠ 0` opens with: *"NAT-addcompat's `(A n ∈ ℕ :: n < n + 1)` at n = 0 gives `0 < 0 + 1`. NAT-closure posits `1 ∈ ℕ` directly, licensing its additive identity `(A n ∈ ℕ :: 0 + n = n)` to be instantiated at n = 1; this gives the equality `0 + 1 = 1`, and rewriting `0 < 0 + 1` by it yields `0 < 1`."*
**Issue**: NAT-closure already axiomatizes `0 < 1` directly — the claim's own declared depends includes it. The ASN instead re-derives `0 < 1` by a detour through NAT-addcompat's successor inequality at n = 0 followed by the additive-identity rewrite `0 + 1 = 1`. This detour is pure reviser drift: prose that does not advance reasoning, a derivation of an already-axiomatized fact. It also props up a NAT-addcompat dependency in the Depends block that exists only to supply this redundant step (the cited role — *"supplies `0 < 0 + 1`, the pre-rewrite form of the anchor"* — has no downstream use). The ActionPoint derivation of `1 ≤ w_{actionPoint(w)}` uses the NAT-discrete + additive-identity pattern because it genuinely needs to lift `0 < n` to `1 ≤ n`; OrdinalDisplacement only needs the anchor `0 < 1` and has it directly.
**What needs resolving**: Replace the three-step detour in OrdinalDisplacement's promotion with a direct citation of NAT-closure's `0 < 1` axiom, and remove NAT-addcompat from the *Depends* list (verify no other step in the derivation uses it).

### ActionPoint's S ⊆ ℕ justification over-explains immediate set-builder membership

**Class**: OBSERVE
**Foundation**: T0 (CarrierSetDefinition) — index-domain commitment.
**ASN**: ActionPoint's derivation: *"The set S = {i ∈ ℕ : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0} is a nonempty subset of ℕ: nonempty by TA-Pos, and a subset of ℕ by construction (the carrier `i ∈ ℕ` is licensed by T0's commitment that the index domain `{1, …, #w}` of w lies in ℕ)."*
**Issue**: The set-builder notation opens with `i ∈ ℕ`, which makes `S ⊆ ℕ` immediate by the definition of set-builder abstraction — no T0 "licensing" is needed. T0's index-domain commitment is load-bearing elsewhere (typing `wᵢ ∈ ℕ` in the `1 ≤ w_{actionPoint(w)}` step) but not here. The parenthetical is a use-site inventory masquerading as a justification. Soundness is unaffected; the claim reads as a defensive over-justification.

### Dangling "shift" reference in δₙ notation note

**Class**: OBSERVE
**Foundation**: (none — internal)
**ASN**: OrdinalDisplacement closes with: *"When the depth is determined by context (typically m = #v for the tumbler being shifted), we write δₙ."* The section header is *"Ordinal displacement and shift."*
**Issue**: No shift operation is defined in the shown content, and no tumbler-shifting caller appears in this ASN. The notation note and the section title promise a shift operator whose body is absent, leaving the δₙ shortcut grounded in context that does not exist within the ASN as presented. If the shift lives in a downstream ASN, the forward reference is fine but should be stated as such; if it was intended to appear here, it is missing.

VERDICT: REVISE
