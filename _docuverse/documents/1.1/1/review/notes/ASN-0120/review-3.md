# Review of ASN-0120

## REVISE

### Issue 1: Resolution's containment `ρ(R, Σ) ⊆ dom(Σ.C)` is not discharged for partial spans

**ASN-0120, "What the endset arguments name" / ML1**: the spec-set restricts only the *start* of each V-span — "content-subspace (subspace(u_j) = s_C), level-uniform (#ℓ_j = #u_j) and T12-well-formed" — and then ML1 claims "By generalized referential integrity (S3★) applied to the content-subspace V-positions the spec restricts to (subspace(v) = s_C ⟹ …), ρ(R, Σ) ⊆ dom(Σ.C)."

**Problem**: The step "the spec restricts to content-subspace V-positions (subspace(v) = s_C)" is asserted, not established, and it does not follow from the stated precondition. `ρ` filters by `v ∈ dom(Σ.M(d_j)) ∧ v ∈ ⟦σ_j⟧` only — nothing forces `subspace(v) = s_C`. Level-uniformity (`#ℓ_j = #u_j`) plus T12 permits the displacement `ℓ_j` to have action point `k < m`. With `k < m` the interval `[u_j, u_j ⊕ ℓ_j)` is *not* confined to first-component `s_C`: e.g. `ℓ_j = [c, 0, …, 0]` (action point 1) gives `u_j ⊕ ℓ_j = [s_C + c, 0, …, 0]`, so an active link-subspace V-position such as `[s_L, 1]` can satisfy `u_j ≤ v < u_j ⊕ ℓ_j`. By S3★ its image lies in `dom(Σ.L)`, so `ρ(R, Σ) ⊄ dom(Σ.C)` and ML1/ML2's `coverage(e_j) ∩ dom(Σ.C) = ρ(R_j, Σ)` fails.

The natural fix would be ASN-0058's C0 (OrdinalDisplacementNecessity), which forces action point `= m` — but C0 holds only for a *well-formed content reference* (every depth-`m` position active), and the ASN deliberately drops that condition to admit partial spans ("we diverge from `resolve` … `ρ` filters to the currently-active positions … resolves *partial* spans"). So C0 is unavailable exactly where it is needed.

This is the load-bearing step of the S0/S3★ revision and propagates into ML9 Fact (a), where "every supplied spec is content-subspace … so every covered tumbler carries `subspace_I = s_C`" is reasserted on the same unjustified basis.

**Required**: Strengthen the spec-set precondition so each `ℓ_j` is an ordinal displacement `δ(n_j, m)` (equivalently `actionPoint(ℓ_j) = #u_j`), which confines `⟦σ_j⟧` to subspace `s_C`; *or* add `subspace(v) = s_C` directly to `ρ`'s filter. Then derive `ρ(R, Σ) ⊆ dom(Σ.C)` from S3★ explicitly. Show the confinement step rather than asserting it.

### Issue 2: `enabled(makelink)` omits source-document definedness

**ASN-0120, ML9**: "`enabled(makelink(d, R₁, R₂, R₃)) ≡ d ∈ dom(Σ.M) ∧ ρ(R₃, Σ) ≠ ∅`."

**Problem**: The wp's right-hand side evaluates `ρ(R_i, Σ) ∩ ran(Σ.M(d'))` for `i = 1, 2, 3`. For `ρ(R_i, Σ)` to be *defined*, every source document named in `R_i` must satisfy `d_j ∈ dom(Σ.M)`. The enabledness guard captures this only for `R₃` (implicitly, via `ρ(R₃) ≠ ∅`) and not for `R₁`, `R₂`. The commit that introduced these guards intends `enabled` to fold in the operation's full precondition; as written it is incomplete for the from/to arguments.

**Required**: Either fold "all source documents of `R₁, R₂, R₃` are allocated" into `enabled(makelink)`, or state explicitly that valid spec-set arguments presuppose source-document allocation (so definedness of every `ρ(R_i, Σ)` is part of well-formed input) and that `enabled` therefore omits it by convention.

## OUT_OF_SCOPE

### Topic 1: Meaning of an empty from/to endset and identity-distinctness of duplicate MAKELINK calls
**Why out of scope**: These are correctly deferred in Open Questions (empty non-type endset semantics; distinctness of identical-argument calls) and concern downstream link semantics rather than the recording act this ASN specifies.

### Topic 2: Endsets reaching into the link subspace (link-to-link)
**Why out of scope**: Explicitly deferred; well-formed resolution of link-subspace endset arguments is new territory, not an error here.

VERDICT: REVISE
