# Cone Review — ASN-0034/T1 (cycle 1)

*2026-04-25 17:33*

Reading the ASN as a system. Cycle 1 covered the proof walks and dependency chains; checking for new issues, particularly around prose hygiene and definition consistency.

### Use-site inventory in NAT-carrier prose
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: NAT-carrier (NatCarrierSet) — the body of NAT-carrier contains:
> "Every Cartesian product `ℕ × ℕ` (NAT-order's `< ⊆ ℕ × ℕ`, NAT-closure's `+ : ℕ × ℕ → ℕ`), every membership `x ∈ ℕ` (NAT-zero's `0 ∈ ℕ`, NAT-closure's `1 ∈ ℕ`), and every set-builder `{j ∈ ℕ : ...}` (T0's index domain ...) presupposes this primitive commitment."

and the follow-up paragraph:

> "No further structure on `ℕ` is asserted here. The strict order `<` is introduced by NAT-order, the constants `0` and `1` by NAT-zero and NAT-closure respectively, ..."

**Issue**: The first paragraph is a use-site inventory (where NAT-carrier is consumed downstream); the second is an inverse-dependency catalogue (what *other* ASNs add to ℕ). Both explain why NAT-carrier exists in the dependency graph rather than what its single axiom (`ℕ is a set`) says. The actual claim is one line, but the reader must skip past two paragraphs of meta-prose to confirm that. This is the "new prose around an axiom explains why the axiom is needed rather than what it says" pattern called out as reviser drift. Soundness is unaffected; the claim's body is just buried.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 392s*
