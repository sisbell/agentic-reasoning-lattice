# Review of ASN-0084

## REVISE

### Issue 1: Cut ordinals are used as positive naturals, but CS1–CS4 permit a zero second component
**ASN-0084, "Cut Points and the Region Partition" (CS1–CS4) and "Consequences of R-PRE" (Width positivity)**: CS3 fixes `subspace(cᵢ) = 1` and CS4 fixes `#cᵢ = 2`, so each cut is `cᵢ = [1, q]` — but nothing in CS1–CS4 requires `q ≥ 1`. The width arithmetic then asserts "this coincides with ord(c_i) < ord(c_{i+1}) ∈ ℕ⁺" and the count identity "the count of V-positions in [c_i, c_{i+1}) equals ord(c_{i+1}) − ord(c_i)".

**Problem**: The singleton-tumbler identification and truncated subtraction are defined only on `{[k] : k ∈ ℕ⁺}`. If a cut had `ord = 0` (e.g. `c₀ = [1,0]`), then `ord(c₀) ∉ ℕ⁺` and the width formula `w_α = ord(c₁) − ord(c₀)` would *over*count: the actual V-positions in `[c₀, c₁)` are those with ordinal in `[1, ord(c₁))` (V-positions are zero-free by S8a), giving `ord(c₁) − 1`, not `ord(c₁) − 0`. The two collapse only because R-PRE(iv) silently excludes a zero-ordinal `c₀` (the position `[1,0]` would satisfy R-PRE(iv)'s antecedent `subspace = 1 ∧ #v = 2 ∧ c₀ ≤ v < c_{n−1}` yet cannot lie in `V_S(d)`, falsifying the precondition). That exclusion is load-bearing for every width identity and is never stated.

**Required**: Either add a clause to the CutSequence definition requiring the second component positive (zero-free, matching S8a), or add an explicit "cut positivity" consequence deriving `ord(cᵢ) ∈ ℕ⁺` from R-PRE(iv) before the width arithmetic relies on it. As written, the count-equals-ordinal-difference step is a claim, not a derivation, for the only inputs (`ord(cᵢ) = 0`) that would break it.

### Issue 2: "Subspace confinement" in Consequences of R-PRE restates SUBCONF (anti-bloat)
**ASN-0084, "Consequences of R-PRE," *Subspace confinement* sub-paragraph**: "Any cut-relative shift `c_i + j` retains subspace S: by CS3, subspace(c_i) = S, and SUBCONF gives subspace(c_i + j) = subspace(c_i) = S."

**Problem**: SUBCONF already states `subspace(v + n) = subspace(v)` for any `v` with `#v ≥ 2`. Since `#cᵢ = 2` (CS4), the sub-paragraph is SUBCONF instantiated at `v = cᵢ` composed with CS3 — a one-line corollary expanded into a labeled paragraph that advances no new reasoning. Under the note's anti-bloat classifier, this is a restatement, not a step.

**Required**: Delete the sub-paragraph or compress to a single inline clause where `c_i + j` first appears (R-PIV/R-SWP already cite Extended Associativity for the same destinations; subspace confinement of cuts can ride along there).

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4
**Why out of scope**: The ASN's two primitives (3-cut pivot, 4-cut swap) are self-contained; generalizing the displacement structure to k > 4 is new territory, correctly listed in Open Questions.

### Topic 2: Text subspaces with depth m₁ > 2
**Why out of scope**: The depth-2 restriction is declared as an explicit scope narrowing, not an error. Lifting it (variable-depth ordinal arithmetic) is a future ASN.

VERDICT: REVISE
