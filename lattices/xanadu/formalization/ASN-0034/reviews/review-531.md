# Regional Review — ASN-0034/T4c (cycle 2)

*2026-04-24 13:12*

Reading the ASN end-to-end against the foundation chain, checking that every inference step is actually licensed by the cited foundations.

### T4 Exhaustion applies NAT-discrete but elides the `0 + 1 = 1` reduction
**Class**: REVISE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity), NAT-discrete (NatDiscreteness)
**ASN**: T4 Exhaustion paragraph: "At `m = 0`: … or `0 < zeros(t)`, which NAT-discrete promotes to `1 ≤ zeros(t)`." T4 Depends (NAT-closure entry): "supplies `1 ∈ ℕ` and closure of ℕ under addition, grounding the numerals `2 := 1 + 1` and `3 := 2 + 1` in ℕ so that `zeros(t) ≤ 3` compares two ℕ-elements."
**Issue**: NAT-discrete's axiom clause is `m < n ⟹ m + 1 ≤ n`. Instantiated at `(m, n) := (0, zeros(t))` it outputs `0 + 1 ≤ zeros(t)`, not `1 ≤ zeros(t)`. Collapsing `0 + 1` to `1` requires NAT-closure's *left additive identity* `0 + n = n` (instantiated at `n := 1`), and this clause is not cited anywhere in T4's Depends list for NAT-closure. The later iterations at `m = 1` and `m = 2` cover `1 + 1 = 2` and `2 + 1 = 3` by the already-declared numeral-definition route (`2 := 1 + 1`, `3 := 2 + 1`), but the `m = 0` step has no such route — it genuinely needs left-identity. The same reduction is explicitly cited in NAT-sub's strict-positivity Consequence ("NAT-discrete at `(m, n) := (0, m − n)` delivers `0 + 1 ≤ m − n`, which NAT-closure's left-identity reduces to `1 ≤ m − n`"), so the pattern is visible elsewhere in the document; T4 omits it.
**What needs resolving**: Either add NAT-closure's left additive identity clause to T4's Depends entry for NAT-closure (and make the prose cite it at the `m = 0` step), or present the Exhaustion's base step in the `+1` form NAT-discrete outputs directly (`0 + 1 ≤ zeros(t)`) and let `1 := 0 + 1` be a numeral-definition move — parallel to how the later steps treat `2 := 1 + 1` and `3 := 2 + 1`.

### T4b attributes "strictly positive" to NAT-discrete when NAT-zero alone suffices
**Class**: REVISE
**Foundation**: NAT-zero (NatZeroMinimum), NAT-discrete (NatDiscreteness)
**ASN**: T4b Derivation: "every non-separator position carries a field component — strictly positive by NAT-zero and NAT-discrete at `m = 0` on T0's carrier ℕ." T4b Depends (NAT-discrete entry): "at `m = 0`, promotes non-zero components to strictly positive, placing the image of each projection in the all-`ℕ⁺`-component subset of `T`." Postconditions: "returns a nonempty finite sequence over `ℕ⁺`" where T4 defines `ℕ⁺ = {n ∈ ℕ : 0 < n}`.
**Issue**: "Strictly positive" — i.e., `0 < tᵢ`, equivalently ℕ⁺ membership under T4's definition — is NAT-zero's output alone: from NAT-zero's axiom `0 < n ∨ 0 = n` at `n := tᵢ`, the equality branch is excluded by `tᵢ ≠ 0` (separator/non-separator distinction), leaving `0 < tᵢ`. NAT-discrete does not "promote non-zero components to strictly positive" — that is precisely the reading NAT-zero already delivers. NAT-discrete would be needed to promote `0 < tᵢ` to the `+1` form `1 ≤ tᵢ`, but the Postconditions target (membership in ℕ⁺ = `{n ∈ ℕ : 0 < n}`) does not require that form. The same structural distinction — NAT-zero raises `n ≠ 0` to `0 < n`; NAT-discrete raises `0 < n` to `1 ≤ n` — is drawn precisely in NAT-sub's strict-positivity Consequence; T4b merges them, attributing to NAT-discrete work that NAT-zero performs.
**What needs resolving**: Either remove NAT-discrete's contribution from the "strictly positive" citation (and drop the corresponding line from Depends if ℕ⁺ membership is the only use of this foundation at T4b), or change the conclusion to the `+1` form `tᵢ ≥ 1` where NAT-discrete's contribution is load-bearing — and align the Postconditions / image description accordingly.

### T4b "never absent" is scoped to the T4-valid subdomain but the formal absence definition is global
**Class**: OBSERVE
**ASN**: T4b body: "The four projections share the T4-valid subset of `T` as the outer domain from which absence is carved… `N` is defined on the whole T4-valid subdomain (`N` is never absent)." Then, later: "A field `X` is *absent in `t`* iff `t ∉ dom(X)`."
**Issue**: Under the formal definition `absent iff t ∉ dom(X)`, `N` *is* absent at every `t ∈ T` that is not T4-valid, because `dom(N)` is the T4-valid subset. The earlier prose "`N` is never absent" is therefore true only when scoped to the T4-valid subdomain, and the parenthetical scope ("on the whole T4-valid subdomain") must be carried by the reader when re-reading the formal definition. A single-meaning-throughout reading prefers either relativising the formal definition to the T4-valid subdomain explicitly, or stating "`N` is never absent on its domain's outer subdomain" rather than "never absent" simpliciter.

VERDICT: REVISE
