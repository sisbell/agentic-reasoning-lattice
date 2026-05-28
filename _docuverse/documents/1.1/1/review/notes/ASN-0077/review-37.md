# Review of ASN-0077

## REVISE

### Issue 1: L1b misattributed as the source of `zeros(x) = 3` for links
**ASN-0077, O0(a) and O3**: "For `x ∈ dom(L)`, L1b (ASN-0047) gives `zeros(x) = 3`."
**Problem**: By this ASN's own `b_C(d), b_L(d)` definition, L1b is cited for the *element-field depth* property: "link addresses have `#E ≥ 2` (L1b)." L1b is the link analogue of S7c (`#E ≥ 2`), not a `zeros = 3` claim. The `zeros(ℓ) = 3` fact is supplied by SubAllocatorAxiom (c) ("Every output of d's sub-allocators is T4-valid with `zeros(·) = 3`") and the Allocator-hierarchy output characterisation. O0(a) is load-bearing for the entire dom(L) extension, so the citation must be correct.
**Required**: Cite SubAllocatorAxiom (c) (or L0 plus the allocator-output characterisation) for `zeros(x) = 3` on `dom(L)`, and reserve L1b for `#E ≥ 2`.

### Issue 2: Working-frame vocabulary is declared narrower than the closure arguments require
**ASN-0077, O0(b)/O0a**: "the working frame's elementary transition vocabulary is ASN-0047's transitions (K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.μ⁺_L, K.ρ)" — yet K.σ is then handled "outside ASN-0047's transition vocabulary," and O0a/O0(c)/O11★★ all enumerate K.σ as part of the system.
**Problem**: The closure arguments (O0a, O0(c) totality) and the absorption case in O11★★ require an *exhaustive* enumeration of the complete transition vocabulary. The ASN both declares the frame as the 8 ASN-0047 transitions and silently extends it with K.σ. The soundness of "the only source of growth in `dom(L)` is K.λ" depends on the enumeration being complete, so the frame must be stated unambiguously as `{ASN-0047 transitions} ∪ {K.σ}` and asserted complete.
**Required**: State the complete transition vocabulary once, explicitly including K.σ, and assert exhaustiveness; do not describe the frame as "ASN-0047's transitions" while reasoning over a larger set.

### Issue 3: O11★ / O11'★ re-derive well-formedness preservation incompletely instead of citing O11.1
**ASN-0077, O11★ (step)**: "the common depth `m` in subspace `u₁` is fixed by S8-depth across the chain (K.μ⁺ additions enter `s_C` at the prevailing content depth, parallel to ... O11's sub-case (a))."
**Problem**: Corollary O11.1 (stated earlier) discharges exactly this obligation for both `u₁ = s_C` and `u₁ = s_L`. O11★'s inline argument addresses only the `s_C` common depth and leaves the `u₁ = s_L` case ("K.μ⁺ adds no link positions, so link depth unchanged") implicit. Since the corollary exists precisely to be cited here, the partial re-derivation is both redundant and incomplete.
**Required**: Replace the inline depth argument in O11★ and O11'★ with a citation to O11.1 covering both subspace cases.

### Issue 4: O2 content-block step under-states M16a's precondition
**ASN-0077, O2 (content block)**: "S3★ at `vⱼ+i ∈ dom(M(d))` gives `aⱼ+i ∈ dom(C)`. This discharges M16a's precondition at `(aⱼ, i)`."
**Problem**: M16a (OriginInvarianceUnderShift) requires *both* `aⱼ ∈ dom(C)` and `aⱼ+i ∈ dom(C)`. The text discharges only `aⱼ+i ∈ dom(C)`. The `aⱼ ∈ dom(C)` conjunct follows from the same step at `i = 0`, but this is not stated.
**Required**: Note explicitly that the `i = 0` instance supplies `aⱼ ∈ dom(C)`, completing M16a's precondition.

## OUT_OF_SCOPE

### Topic 1: Reporting link origins from an I-span
**Why out of scope**: The I-span lift restricts to `dom(C)` by definitional choice (cross-subspace edge case), dropping link origins. This is correctly deferred to Open Question 1; it is a future extension, not an error here.

### Topic 2: Historical containment via `Σ.R`
**Why out of scope**: SHOWORIGIN reports current origin, not the documents that have ever contained the content. The ASN correctly isolates this as a distinct operation over the provenance relation (final Open Question), outside the present scope.

VERDICT: REVISE
