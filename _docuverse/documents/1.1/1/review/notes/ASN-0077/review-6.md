# Review of ASN-0077

## REVISE

### Issue 1: O2 case split exhaustiveness not justified
**ASN-0077, claim O2 derivation**: "Two cases by subspace of vⱼ. *Content block* (`subspace(vⱼ) = s_C`)... *Link block* (`subspace(vⱼ) = s_L`)..."
**Problem**: The two-case split asserts `subspace(vⱼ) ∈ {s_C, s_L}` is exhaustive, but does not cite the foundation invariant that delivers this. ASN-0047's S3★-aux (`(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`) is exactly what makes the case split exhaustive, and it is the precondition that licenses skipping a third case.
**Required**: Cite S3★-aux (ASN-0047) at the case-split step to discharge exhaustiveness.

### Issue 2: O0 (b) "sole modifier" framing rests on a wording that is not literally true
**ASN-0077, claim O0 derivation (b)**: "K.λ is the sole elementary transition in ASN-0047 that modifies dom(L): every other elementary transition (K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ) holds L' = L in frame..."
**Problem**: The foundation extracts for K.μ⁺, K.μ⁻, and K.ρ do not explicitly include `L' = L` in their frame clauses (only K.α, K.δ, K.μ⁺_L, K.μ~ do). The argument depends on these transitions' *effects* not touching L (M, R, etc.) rather than on an explicit frame clause. The conclusion is correct, but the stated premise is not. A Dijkstra-style audit reading the foundation literally will mark this as untrue.
**Required**: Either (i) reword to "every other elementary transition leaves L unchanged by its effect clause (no clause mentions L)" with a per-transition effect check, or (ii) ground the conclusion entirely on L1c, which independently identifies every `ℓ ∈ dom(L)` with a K.λ event via `t₀ = origin(ℓ)`, removing the need for the "sole modifier" deduction.

### Issue 3: Singleton I-span #b > #a case omits allocator-identification chain
**ASN-0077, "Edge cases" / "Singleton I-span", case `#b > #a`**: "Hence `origin(b) = origin(a)` by S7's structural projection... Write `d = origin(a) = origin(b)`. By SubAllocatorAxiom (ASN-0047), clauses (b)–(d), `d`'s content sub-allocator `A_C(d)` is T10a-conforming with first emission `[d.0.s_C.1]` of length `#d + 3`. Both `a` and `b` are outputs of `A_C(d)`."
**Problem**: The step from "`origin(a) = origin(b) = d`" to "Both `a` and `b` are outputs of `A_C(d)`" compresses two distinct foundation citations into one: (i) S7a (DocumentScopedAllocation, ASN-0036) — `a` was allocated by the document `d`; (ii) SubAllocatorAxiom (ASN-0047) — `d`'s content allocations route through `A_C(d)` specifically (not through `A_L(d)`, since `a ∈ dom(C)`, by L14 / L0 disjointness). The cited SubAllocatorAxiom clauses (b)–(d) supply length info but not the identification of `A_C(d)` as `a`'s producing allocator.
**Required**: Make the chain explicit: `a ∈ dom(C) ∧ origin(a) = d → a` allocated under `d` (S7a) → `a` produced by `A_C(d)` (SubAllocatorAxiom (a): `A_C(d)` is the sub-allocator producing every `a` with `subspace_I(a) = s_C` and `origin(a) = d`).

### Issue 4: O3 V-span sub-claim treats `origin(M(d)(v))` as well-defined without discharging domain membership
**ASN-0077, claim O3 derivation, V-span lift**: "By the pointwise claim, `origin(M(d)(v))` reads only the value `M(d)(v)`, which the restriction supplies."
**Problem**: For `origin(M(d)(v))` to be defined, `M(d)(v)` must lie in `dom(C) ∪ dom(L)` — origin's stated domain. This is S3★ (ASN-0047), and O7's derivation does invoke S3★ at exactly this step, so the omission in O3 is a missed citation, not a missed fact. A reader checking O3 in isolation will not see what guarantees that the pointwise projection is applicable.
**Required**: Cite S3★ in O3's V-span derivation at the step where `origin(M(d)(v))` is asserted to be well-defined.

## OUT_OF_SCOPE

### Topic 1: Cross-subspace I-span semantics (Open Question 1)
**Why out of scope**: ASN-0077 deliberately defines `origins_I` to project through `dom(C)` only, silently dropping link addresses. This is acknowledged as a design choice with an explicit open question. The current ASN is internally consistent.

### Topic 2: Transitive provenance reporting (Open Question 2)
**Why out of scope**: O4 establishes that SHOWORIGIN names the original allocator, not the chain of intermediate documents. A complementary "chain-reporting" operation would be a separate ASN.

### Topic 3: Native vs. transcluded distinction within a single document (Open Question 3)
**Why out of scope**: SHOWORIGIN reports origin sets without partitioning by native/transcluded provenance. A separate operation could partition.

### Topic 4: Historical containment via Σ.R (Open Question 5)
**Why out of scope**: SHOWORIGIN_V reads from current arrangement `M(d)`; provenance relation `R` is a separate state component and warrants its own access operation.

VERDICT: REVISE
