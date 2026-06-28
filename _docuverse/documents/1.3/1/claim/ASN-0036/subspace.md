**subspace (VPositionSubspaceIdentifier).** A V-position carries its subspace identity in its own leading component; we make that reading explicit, naming the projection the arrangement-contiguity invariants downstream will range over. For any tumbler `v` of depth `#v ≥ 1`, define:

`subspace(v) = v₁`

extracting the subspace identifier as the first component of a V-position. Both symbols on the right-hand side are T0's (CarrierSetDefinition, ASN-0034): `#·` is T0's length operator `#· : T → ℕ`, and `v₁` is the value at index `1` of T0's component projection `i ↦ vᵢ : {j ∈ ℕ : 1 ≤ j ≤ #v} → ℕ`. We observe that this projection returns a component at index `1` exactly when `1` lies in its index domain `{j ∈ ℕ : 1 ≤ j ≤ #v}` — that is, when `#v ≥ 1`, which is the depth guard the definition states. So `subspace(v)` is well-defined precisely under that guard; and since T0's nonemptiness clause `(A a ∈ T :: 1 ≤ #a)` already forces `#v ≥ 1` for every `v ∈ T`, the read is total on the carrier. We introduce no structure of our own: `subspace` is T0's first-component projection under a name chosen for the role its value plays, so that subspace membership is a direct read of an address component rather than a lookup against any external structure.

*Formal Contract:*

- *Definition:* For any tumbler `v ∈ T` with `#v ≥ 1`, `subspace(v) = v₁` — the value at index `1` of T0's component projection `i ↦ vᵢ`. The depth guard `#v ≥ 1` is the well-definedness condition placing index `1` in that projection's index domain `{j ∈ ℕ : 1 ≤ j ≤ #v}`; T0's nonemptiness clause `1 ≤ #v` discharges it for every `v ∈ T`, so `subspace` is total on the carrier. The definition introduces no constraint of its own beyond naming this first component the V-position's subspace identifier.

- *Depends:*
  - T0 (CarrierSetDefinition, ASN-0034) — supplies the component projection `i ↦ vᵢ : {j ∈ ℕ : 1 ≤ j ≤ #v} → ℕ`, whose value at index `1` is `subspace(v) = v₁`, and the length operator `#·`, against which the depth guard `#v ≥ 1` — the well-definedness condition placing index `1` in that projection's index domain — is read. These are the two foundation symbols the definition consumes; grounding them at this definition site is what lets every downstream claim that reads `v₁` through `subspace` rest on a defined symbol.
