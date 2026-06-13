# Review of ASN-0132

The note is in good shape: every claim is either derived in full or grounded in a foundation result, the worked example is internally consistent and exercises the static rulings cleanly, and all cross-ASN references are to foundation ASNs (ASN-0034/0036/0043/0047/0058/0086/0093/0098/0121/0127). I re-verified the example's arithmetic (`coverage(F) = […1.5, …1.13)`, `nullified(Σ)={a₂}`, `addressable(Σ)={a₁,a₃,a₄,a_R}`, count `=2`, all-wildcard `=4`, `q_H'` zero) and it holds. The findings below are about the one place where the proof obligation outruns the proof, plus an example-coverage gap and one accretion pattern.

## REVISE

### Issue 1: CN-MONO derives the ordinary-link increment in full but discharges the retraction-link increment by citation — and the two cases differ in a load-bearing way

**ASN-0132, "Retraction and permanence" (CN-MONO derivation)**: the ordinary case is established by the explicit step
> "Its addressability is fixed too: because `ℓ` is not a retraction, `L_R^{Σ'} = L_R^Σ`, so the nullified set restricted to the old domain is unchanged, `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)`, and each pre-existing `a` is addressable at `Σ'` exactly when it was at `Σ`."

while the retraction case is delegated:
> "Its increment is governed not by FL-WP(a) but by FL-WP(b) (ASN-0121): because creating it *grows* `L_R^{Σ'}` rather than leaving it fixed, the precondition carries an additional *self-retraction* conjunct requiring the fresh address to lie outside its own to-coverage…"

**Problem**: The "pre-existing contributions are unmoved" sub-step — the heart of the net-`+1` argument — is established for the ordinary case *precisely* because `L_R^{Σ'} = L_R^Σ` makes collateral nullification impossible. For a fresh retraction link this premise fails: `L_R^{Σ'} = L_R^Σ ∪ {(b, F', G')}`, so the new tuple's to-coverage `G'` can nullify a *pre-existing, currently-counted* link `a` (any `a ∈ coverage(G')`), dropping it from `addressable(Σ')` and lowering the pre-existing total. The prose names only the *self*-retraction conjunct (b nullifying itself); it never addresses this *collateral* nullification of other counted links. The net `+1` for the retraction case is in fact rescued solely by the CN-MONO precondition "no currently-counted link becomes nullified," but the derivation never makes that connection. This is exactly the "show each case where they differ" situation: the ordinary case is unconditionally clean, the retraction case is clean only under the precondition, and the differing element is unproved.

**Required**: Walk the retraction sub-case explicitly: state that creating `b` grows `L_R`, so `nullified` may gain pre-existing members on `dom(Σ.L)`; invoke the CN-MONO precondition to fix `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` (no currently-counted link withdrawn), thereby preserving the pre-existing total; then add `b`'s own contribution via FL-WP(b). Make plain that the precondition is vacuous for the ordinary case but load-bearing here.

### Issue 2: The worked example exercises only single-state (static) claims; CN-MONO's increment and CN-STAB's invariance are never verified against a transition

**ASN-0132, "A census, computed"**: the example fixes one state `Σ` and reads contributions off `sat`/`addressable`, verifying CN-UNIT, CN-RETRACT, CN-ORPHAN, CN-ZERO, and the home slot.

**Problem**: The note's most intricate claim — CN-MONO, the only one carrying a weakest-precondition derivation — is never checked against a concrete before/after. Likewise CN-STAB (invariance under a link-store-preserving edit) is asserted and derived but not instantiated. For a *counting* operation the dynamic behaviour ("the number goes from N to N+1 when…") is the defining content; verifying it concretely is what the depth/concrete-example standard asks for, and the static example does not reach it.

**Required**: Extend the worked example with at least one transition — e.g., a `K.λ` creating a fresh `a₅` homed at `d₁` with a from-endset touching `F` (count `2 → 3`, instantiating the wp `sat(a₅,q,Σ') ∧ ¬(E … ∈ L_R^Σ :: a₅ ∈ coverage(G'))`), and a `K.μ⁻` content-deletion on `d₁` that leaves `Σ.L` fixed (count stays `2`, instantiating CN-STAB). Ideally also a retraction `K.λ` whose `G'` covers a counted link, to exhibit the collateral case from Issue 1.

### Issue 3 (anti-bloat): CN-MONO contains a roadmap paragraph that pre-announces and partially duplicates the derivation that immediately follows it

**ASN-0132, "Retraction and permanence"**: 
> "…and the exact four-set increment, retraction-coverage condition and all, is FL-WP(a) (ASN-0121), which the next paragraph derives in full. We can make the increment exact by a weakest-precondition step."

**Problem**: This is a within-document forward signpost ("which the next paragraph derives in full") sitting in a summary paragraph that states the increment is FL-WP(a) just before the next paragraph derives the same wp. The reader must skip past the announcement to reach the actual reasoning; the signpost advances nothing. (The four "*That same realisation…*" implementation notes are a related repeated-shape accretion; notes 2 and 3 — "drives the count and the enumeration through one shared matching routine" and "recomputes the count at each inquiry" — are one-sentence and thin, though note 1's dedup-defect observation is substantive and should stay.)

**Required**: Drop the "which the next paragraph derives in full" signpost and let the roadmap paragraph lead directly into the derivation, or fold the high-level argument into the derivation paragraph so the wp is stated once.

## OUT_OF_SCOPE

### Topic 1: An invariant linking the address-set (content-identity) count to a position/V-spec count
The ASN correctly scopes V-to-I resolution as upstream ("it produces `q`") and parks the cross-regime agreement invariant in Open Question 1. This is genuinely new territory (a count phrased over arrangement positions), not a defect here.

### Topic 2: Federated counting across independently administered stores
Deferred to Open Question 6, and the Scope section places replication/inter-server protocol (BEBE) out of scope. Correctly handled as an open question rather than a claim.

VERDICT: REVISE
