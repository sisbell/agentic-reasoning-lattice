# Review of ASN-0069

## REVISE

### Issue 1: J1★ discharge in the non-empty composite verification omits the `d ≠ d_new` branch
**ASN-0069, §"The Fork Composite", *Coupling at (Σ, Σ^{(2+n)})***: "J1★ holds because every `a` with `(E v ∈ dom(M^{(2+n)}(d_new)) : subspace(v) = s_C ∧ M^{(2+n)}(d_new)(v) = a)` had `(a, d_new)` recorded by some K.ρ step..."

**Problem**: J1★ is universally quantified over `d ∈ E'_doc`, but the non-empty verification discharges only `d = d_new`. The `d ≠ d_new` branch (vacuous because the fork's frame leaves `M'(d) = M(d)`, so no content-range-new `a` arises) is never stated. This is precisely a missing quantifier case. The asymmetry is visible against the *empty*-case verification, which correctly handles both branches: "for every `d ≠ d_new`, K.δ's frame gives `M^{(1)}(d) = M(d)`, so no `a` is in `ran(M^{(1)}(d)) \ ran(M(d))`." The non-empty check should reach the same completeness.

**Required**: Add the `d ≠ d_new` branch to the non-empty J1★ discharge (vacuous by the K.μ⁺/K.ρ frame on documents other than `d_new`), matching the empty-case treatment.

### Issue 2: V11a re-derives prefix-order transitivity inline — generic foundation algebra in an operation ASN
**ASN-0069, V11a derivation**: "We first verify that `≼` is transitive by unfolding the Prefix definition (ASN-0034). Suppose `a ≼ b` and `b ≼ c`. By Prefix... composing the two component equalities gives `cᵢ = aᵢ`."

**Problem**: Transitivity of `≼` is a property of the foundation's Prefix relation, proved here entirely from ASN-0034 primitives (NAT-order, T3) with no fork-specific content. This is exactly the generic tumbler algebra that should not live in a CREATENEWVERSION ASN. The Prefix foundation contract does not currently expose transitivity, so the inline proof signals a foundation gap rather than fork reasoning — the fix is to expose/cite a foundation `≼`-transitivity lemma, not to carry six lines of order-algebra in the version-fork derivation.

**Required**: Replace the inline transitivity proof with a citation to a foundation result; if ASN-0034 does not provide `≼` transitivity, flag that as the foundation gap to close rather than re-proving it here.

### Issue 3: V9a is largely an ASN-0047 restatement plus a forward pointer to V9b
**ASN-0069, V9a**: "The provenance relation `R ⊆ T × E_doc` (ASN-0047) holds only containment pairs `(a, d)`... carries no inter-document derivation edge... What the I-address *does* fix — that `origin(a) ≠ d_new` for any forked-in address — is recorded separately in V9b."

**Problem**: The opening sentences restate ASN-0047's own definition of `R` ("records that document `d` contained I-address `a`"), and the property closes by forward-pointing to V9b for the load-bearing fact. The genuinely fork-specific content ("a fork's K.ρ records containment, not how `a` was acquired") is one sentence; the surrounding material is foundation restatement and a cross-property pointer — the forward-reference accretion this review is tasked to surface.

**Required**: Trim V9a to its fork-specific claim; drop the restated `R` semantics and the "recorded separately in V9b" pointer.

## OUT_OF_SCOPE

### Topic 1: K.μ⁻ middle-deletion expressibility in the worked example
**ASN-0069, §"Worked Example", *Subsequent edits***: "A middle-only deletion such as removing `[s_C, 2]` while keeping `[s_C, 3]` is not expressible as a K.μ⁻ at all."
**Why out of scope**: This is a claim about contraction/DELETE mechanics, which the Scope section excludes. It is illustrative rather than a formal Vn claim, but its placement imports excluded-operation semantics into the fork example.

VERDICT: REVISE
