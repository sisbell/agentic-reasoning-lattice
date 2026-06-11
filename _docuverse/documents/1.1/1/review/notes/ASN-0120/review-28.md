# Review of ASN-0120

## REVISE

### Issue 1: The worked example stipulates the resolution outputs instead of computing them
**ASN-0120, "A worked example"**: "*Arguments.* `from = R₁` resolves to `ρ(R₁, Σ) = {a₁, a₂}`; `to = R₂` resolves to `ρ(R₂, Σ) = {b₁}`; `type = R₃` resolves to `ρ(R₃, Σ) = {θ₁} ≠ ∅`"

**Problem**: The spec-set arguments `R₁, R₂, R₃` are never exhibited — no source V-span `σ_j = (u_j, ℓ_j)` is written down anywhere in the example, and `ρ` is asserted rather than computed. By the ASN's own framing, "the whole content of MAKELINK is a single conversion of coordinates," and that conversion — reading a concrete V-span through a concrete arrangement to recover I-addresses — is exactly the one piece of machinery the example does not exercise. The example verifies the recovery equation, ML0, ML2, ML9, and the edit consequences against *given* resolved sets, so ML1's central mechanism (the active-position filter `v ∈ dom(Σ.M(d_j)) ∧ v ∈ ⟦σ_j⟧`, and `wf` itself) is never instantiated on data. The V-positions `[s_C, 1] ↦ a₁`, `[s_C, 2] ↦ a₂` that would make the computation possible are introduced only later, for the K.μ⁻ edit — the ingredients are present but the demonstration is skipped.

**Required**: Exhibit the three spec-sets concretely and trace one resolution end to end. With the depth-2 arrangement the edit paragraph already names, `R₁ = ⟨(A, ([s_C, 1], δ(2, 2)))⟩` suffices: check `wf` (source allocated, `subspace(u) = s_C`, `#u = 2 ≥ 2`, `ℓ = δ(2, 2)`), compute the interval `⟦σ⟧ = [[1,1], [1,3])`, intersect with `dom(Σ.M(A)) = {[1,1], [1,2]}`, and read the images `{a₁, a₂}` through the arrangement. `R₂` and `R₃` can be stated in one line each. This closes the only gap between the example and the operation's headline claim.

## OUT_OF_SCOPE

### Topic 1: Endset arguments supplied as direct I-addresses (ghost types, L4-general endsets)
**Why out of scope**: The ASN correctly observes that V-spec resolution can only produce content-backed endsets, so the full generality of L4/L9 requires a different argument shape. That is a distinct operation surface, not an error here; the restriction is stated and owned.

### Topic 2: Meaning of the empty non-type endset (one-sided links)
**Why out of scope**: Definedness, L3-legality, and inertness in the discoverability test are all settled in this ASN; what the degenerate connection *asserts* is semantics for a future ASN, and the document already carries it as an Open Question.

### Topic 3: Endset specs reaching into the link subspace (links whose endsets name links)
**Why out of scope**: `wf` excludes these by `subspace(u_j) = s_C`, so the current operation is total on its stated domain; extending resolution to link-subspace targets is new territory, correctly deferred to the second Open Question.

VERDICT: REVISE

The review is otherwise clean, and it is worth recording what held up under pressure: the T5 confinement argument discharging `ρ(R, Σ) ⊆ dom(Σ.C)` is complete; the F-trace (rather than store-trace) form of the recovery equation is justified by a genuine counterexample (the unallocated-frontier leak); the extensional coverage derivation closes both inclusions, including the right-to-left identification of a span's F-trace as a fully-resolved sibling run; the K.μ⁺_L precondition discharge (`a ∉ ran(M(d))` via S3★/S3★-aux split, the depth convention `m = 2` for the first link position) is exact; ML6's necessity-and-sufficiency argument for `ρ(R₃, Σ) ≠ ∅` is tight; and ML9's wp argument correctly handles the `d' = d` boundary by showing the freshly seated `a` is inert on both sides of Fact (a)'s equation. I also checked the document against the anti-bloat patterns: the two forward deferrals target distinct Open Questions, the repeated "L3 constrains only slot 3" observations each do local work (boundary settlement vs. the necessity contrast), and the design-motivation passages (why not store V-positions; why trace on F) are counterexample-driven reasoning, not defensive meta-prose — no accretion findings.
