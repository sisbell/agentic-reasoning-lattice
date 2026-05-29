# Review of ASN-0036

## REVISE

### Issue 1: `v₁`/`v₂` overload V-position names against component-subscript notation
**ASN-0036, S8-depth formal contract and D-CTG-depth proof**: "`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ subspace(v₁) = subspace(v₂) : #v₁ = #v₂)`" and, in D-CTG-depth, "two positions v₁ and v₂ with v₁ < v₂ … (v₁)ᵢ = (v₂)ᵢ".
**Problem**: Throughout the rest of the ASN `vₖ` denotes the *k-th component* of tumbler `v` (S8a: "the subspace identifier `v₁`"; D-MIN: "`min(V_1(d))₁ = 1`"; the S8 lemma: "`v_m`"). Here `v₁`, `v₂` are instead *distinct whole V-positions*, with their components then written `(v₁)ᵢ`. A reader must disambiguate "first component of v" from "first V-position" on a per-occurrence basis. The S8-depth *prose* statement already avoids this by using `u, w`; the formal contract and D-CTG-depth do not.
**Required**: Use distinct names (e.g., `u, w`) for the quantified V-positions in S8-depth's formal contract and in D-CTG-depth, reserving subscripts for components.

### Issue 2: S8a's Depends entry re-derives the proof it sits beside
**ASN-0036, S8a Depends**: "NAT-discrete … instantiated at `m = 0`, supplies the `n ≠ 0 ⟹ n ≥ 1` fact that discharges the positivity step: `vᵢ ≠ 0` (delivered by `zeros(v) = 0`) gives `vᵢ ≥ 1`, hence `(A i : … : vᵢ > 0)`."
**Problem**: The two-line S8a proof already states exactly this chain ("`zeros(v) = 0` forces each to be `≠ 0`, hence `≥ 1` by NAT-discrete … instantiated at `m = 0`"). The Depends entry restates the derivation verbatim in a slot whose job is to *name* the dependency and its role, not re-run the inference. This is the duplication the anti-bloat classifier targets — the same statement in two slots of one property.
**Required**: Reduce the NAT-discrete Depends entry to its role ("supplies `n ≠ 0 ⟹ n ≥ 1` at `m = 0`"); let the proof carry the derivation.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG/D-MIN/S2 and subspace alignment
The final two Open Questions (editing operations preserving contiguity; subspace-alignment enforcement) correctly point at INSERT/DELETE/COPY frame conditions, which are explicitly out of scope. Listing them as questions is appropriate; no claim is made, so nothing to fix here.

### Topic 2: Computability/cost of the sharing inverse
The Open Question on the cost bound for "which documents reference I-address `a`" is genuinely new territory (indexing cost model), not a gap in this ASN's invariants.

VERDICT: REVISE
