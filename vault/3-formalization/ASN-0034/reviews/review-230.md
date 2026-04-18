# Cone Review — ASN-0034/T10a.2 (cycle 2)

*2026-04-18 03:28*

### Prefix reflexivity cited by T10a.6 is not exported by Prefix's formal contract

**Foundation**: Prefix (PrefixRelation)

**ASN**: T10a.6 (DomainDisjointness), Case 2 narrative: *"T10a.5 + Prefix reflexivity — cross-allocator prefix-incomparability (T10a.5) is contradicted by `t ≼ t` were `t` shared."* The formal contract's Depends list names this explicitly: *"Prefix (reflexivity of ≼)"*.

Prefix's own formal contract, however, exports only:
- *Definition:* `p ≼ q` iff `#p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`.
- *Derived postcondition:* `p ≺ q ⟹ #p < #q`.

Reflexivity `t ≼ t` is nowhere listed among Prefix's derived postconditions.

**Issue**: T10a.6 Case 2 cites a named property of Prefix — "reflexivity of ≼" — as the second premise that, combined with T10a.5, yields the domain-disjointness contradiction. But Prefix's contract does not export reflexivity; it exports only the proper-prefix length postcondition. A downstream consumer reading Prefix's contract in isolation will not find the property that T10a.6 claims to invoke. The same gap exists for any place the ASN implicitly relies on `t ≼ t` to bridge T10a.5's prefix-incomparability to domain-element distinctness (the natural hook-up to T10's `p₁ ≼ a, p₂ ≼ b` preconditions when one takes `p₁ = a` and `p₂ = b`).

Reflexivity is definitionally immediate — `#t ≤ #t` by NAT-order and `tᵢ = tᵢ` by equality reflexivity — but the contract convention in this ASN requires derived consequences that downstream proofs cite by name to appear as explicit postconditions, not be left to the reader to re-derive from the definition.

**What needs resolving**: Prefix must either (a) export reflexivity `(∀t ∈ T :: t ≼ t)` as an explicit derived postcondition with its supporting citation chain (NAT-order reflexivity of `≤` on ℕ; equality reflexivity at each component), making it available to T10a.6's Depends by name; or (b) T10a.6 Case 2's proof must unfold the Prefix definition inline and discharge the `t ≼ t` step against Prefix's Definition clause together with NAT-order and equality reflexivity directly, removing the "reflexivity of ≼" cite from its Depends.

## Result

Cone converged after 3 cycles.

*Elapsed: 1874s*
