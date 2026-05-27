# Review of ASN-0101

## REVISE

### Issue 1: D0's reduction proof inappropriately invokes S8a

**ASN-0101, "Justification of the reduction" (D0 preconditions)**: "the foundation premise S8a forces every component of `v` strictly positive (`v_j ≥ 1`), in particular ruling out a zero at any middle position"

**Problem**: S8a (ASN-0036) quantifies over `v ∈ dom(M(d))` — V-positions already in the document's arrangement. The reduction is operating in the opposite direction: it ranges over *arbitrary candidate tumblers* `v` with `subspace(v) = S` and `s ≤ v < r`, trying to *prove* such candidates must lie in `V_S(d)`. Invoking S8a on `v` before establishing `v ∈ V_S(d)` is circular — and the universal quantifier of the precondition specifically includes candidate tumblers that are not yet known to be in any arrangement. The same flaw recurs at "then `v_{j_0} ≥ 2` by positivity" in the m_S ≥ 3 branch.

**Required**: Replace the S8a appeal with a T1-only derivation. At any middle position j (where s_j = r_j = 1), if v_j = 0 then position j is the first divergence between v and s with v_j < s_j, giving v < s (T1 case (i)) — contradicting s ≤ v. If v_j ≥ 2 then position j is the first divergence between v and r with v_j > r_j, giving v > r — contradicting v < r. Hence v_j = 1. This argument uses only T1's lex order applied to s and r's known structural forms; S8a is not needed.

### Issue 2: D9's quantification is not restricted to d'' ∈ dom(Σ.M)

**ASN-0101, D9 statement**: "For every link ℓ ∈ dom(L), every slot i, every DEL[d, σ] transition Σ → Σ', and every document d''"

**Problem**: `project(L(ℓ).eᵢ, d'', Σ)` is defined only when `d'' ∈ dom(Σ.M)` (ASN-0098's project definition: "defined when d ∈ dom(Σ.M)"). For d'' ∉ dom(Σ.M), both `project(L(ℓ).eᵢ, d'', Σ)` and `project(L'(ℓ).eᵢ, d'', Σ')` are undefined, and the asserted equality compares two undefined expressions. The first bullet ("If d'' ≠ d: project(...) = project(...)") is ill-formed for d'' outside dom(Σ.M).

**Required**: Restrict the outer quantification to d'' ∈ dom(Σ.M), or add an explicit frame note (analogous to ASN-0098's LP4 frame note) recording that the lemma is stated for d'' ∈ dom(Σ.M) and lifts via D4 to d'' ∈ dom(Σ.M) ∩ dom(Σ'.M). The justification's appeal to D5 ("M'(d'') = M(d'') by D5") is already conditioned on d'' ∈ dom(M), so the restriction belongs in the statement.

VERDICT: REVISE
