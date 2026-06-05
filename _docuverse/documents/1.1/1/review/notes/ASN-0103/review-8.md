# Review of ASN-0103

## REVISE

### Issue 1: Cross-account distinctness rests on an unproven (and predicate-level false) non-nesting premise

**ASN-0103, "Effect One: One Address Is Baptised," Freshness paragraph**: "Cross-account collisions are excluded by partition independence (T10): `d` extends the account prefix `A`, and any address under a different account `A' ≠ A` is prefix-incomparable to it, hence distinct."

**Problem**: T10 (PartitionIndependence) requires its two prefixes to be *non-nesting* (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). The argument applies it with `p₁ = A`, `p₂ = A'` but never establishes that distinct accounts are prefix-incomparable — and this does *not* follow from the `Account` predicate alone. `Account(t) ≡ T4-valid(t) ∧ zeros(t) = 1` (ASN-0045), and the addresses `[N, 0, 5]` and `[N, 0, 5, 3]` are both T4-valid, both have `zeros = 1`, hence both satisfy `Account(·)` — yet `[N, 0, 5] ≺ [N, 0, 5, 3]`. So "`A' ≠ A`" does not entail "prefix-incomparable to `d`." Non-nesting of distinct allocated accounts holds only because the account sub-allocator `A_account(N)` emits uniform-length `[N, 0, j]` addresses — an account-provisioning fact that is explicitly **out of scope** for this ASN and is nowhere invoked. As written, the proof imports a false intermediate lemma ("distinct accounts are prefix-incomparable") that a reader could carry forward.

**Required**: Derive cross-account distinctness from the guarantee the ASN already cites for `d`'s uniqueness — GlobalUniqueness (ASN-0034) and B8 (ASN-0040), which make every baptismal event produce an address distinct from every other regardless of which account it sits under — and drop (or replace) the T10/non-nesting sentence. If the T10 route is retained, the account non-nesting premise must be discharged, which requires the out-of-scope account-allocator uniform-length property; the GlobalUniqueness route avoids that dependency entirely.

## OUT_OF_SCOPE

(none — the ASN correctly defers forking, content allocation, link creation, node/account provisioning, and the registry-coupled `ω`-valued ownership statement, and does not introduce claims for them.)

VERDICT: REVISE
