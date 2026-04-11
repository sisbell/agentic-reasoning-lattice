**S8-depth-C1 (IAddressRunUniformity).** All I-addresses within a correspondence run share the same tumbler depth and prefix, differing only at the element ordinal.

*Theorem.* Let `(v, a, n)` be a correspondence run in `Σ.M(d)`, so that `Σ.M(d)(v + k) = a + k` for all `0 ≤ k < n` (S8-depth(c)). We prove that for every `0 ≤ k < n`: (a) `#(a + k) = #a`, (b) `(a + k)ᵢ = aᵢ` for all `1 ≤ i < #a`, and (c) the element subspace identifier is preserved.

For `k = 0`, all three claims hold trivially since `a + 0 = a` (S8-depth(b)).

For `k ≥ 1`, `a + k = a ⊕ δ(k, #a)` where `δ(k, #a) = [0, ..., 0, k]` is the ordinal displacement of length `#a` (S8-depth(b)). The action point of `δ(k, #a)` — the index of the last non-zero component — is `#a`, which is the final position. By TumblerAdd (PositionAdvance, ASN-0034), components before the action point are copied unchanged from the first operand. Therefore `(a + k)ᵢ = aᵢ` for all `1 ≤ i < #a`, establishing (b). The result has length `max(#a, #δ) = #a`, establishing (a).

For (c), S7c guarantees that element-field depth `δ ≥ 2`, so the element subspace identifier `E₁` occupies a component strictly before the action point. TumblerAdd's prefix rule copies it unchanged, giving `subspace(fields(a + k).element) = subspace(fields(a).element)` for all `0 ≤ k < n`. ∎

*Formal Contract:*
- *Precondition:* `(v, a, n)` is a correspondence run in `Σ.M(d)` (S8-depth(c)), `a ∈ dom(Σ.C)` satisfying S7c
- *Guarantees:* For all `0 ≤ k < n`: (a) `#(a + k) = #a`; (b) `(a + k)ᵢ = aᵢ` for `1 ≤ i < #a`; (c) `subspace(fields(a + k).element) = subspace(fields(a).element)`
- *Dependencies:* S8-depth(b), S8-depth(c), TumblerAdd (ASN-0034), S7c
