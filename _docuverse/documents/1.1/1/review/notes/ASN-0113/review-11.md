# Review of ASN-0113

## REVISE

### Issue 1: Worked-instance reach annotations are dimensionally inconsistent at depth `m_S = 2`

**ASN-0113, "A worked instance" (and "A one-member instance")**: The general form in W3 is `reach(ext(d, S)) = [S,1,…,1,1+n_S]`, where the interior `1,…,1` segment has length `m_S − 2`. At the worked depth `m_S = 2` that segment is **empty**, so the canonical reach is `[S, 1+n_S]`. But the worked computations annotate it with a spurious interior `1`:

- `"Its reach is [1,1] ⊕ [0,5] = shift([1,1], 5) = [1,6] = [s_C,1,1+n_{s_C}]"` — the right side `[s_C,1,1+n_{s_C}]` reads literally as the depth-3 tumbler `[1,1,6]`, which is **not** `[1,6]`.
- `"its reach is [2,3] = [s_L,1,1+n_{s_L}]"` — `[s_L,1,1+n_{s_L}] = [2,1,3] ≠ [2,3]`.
- (one-member instance) `"Its reach is [1,1] ⊕ [0,3] = [1,4] = [s_C,1,1+n_{s_C}]"` — `[1,1,4] ≠ [1,4]`.

**Problem**: The note's stated purpose for the worked instances is to "check the key postconditions against specific tumblers." Equating a depth-2 tumbler (`[1,6]`, `[2,3]`, `[1,4]`) to a depth-3 literal (`[1,1,6]`, etc.) is a concrete inconsistency in exactly the verification meant to ground W3. The depth-3 instance (`reach = [S,1,3] = [S,1,1+n_S]` with one correct interior `1`) is consistent, which confirms the `m_S = 2` cases over-instantiated the general schematic.

**Required**: At `m_S = 2` the canonical reach annotation is `[s_C, 1+n_{s_C}]` (no interior component): write `[1,6] = [s_C, 1+n_{s_C}]`, `[2,3] = [s_L, 1+n_{s_L}]`, `[1,4] = [s_C, 1+n_{s_C}]`. Either drop the spurious `1` or annotate with the explicit "(empty interior segment at `m_S = 2`)" caveat.

## OUT_OF_SCOPE

The Open Questions (version-fork permanence, consumer reading of an omitted member as zero, transclusion stability, consistency with a single overall extent, and convention extension beyond text/links) are correctly deferred and align with the declared scope exclusions (ASN-0112 overall extent, replication, version comparison). No misplaced claims found.

Note on what was checked and held: W4's ExactCoverage (the joint use of both bounds via T5, with the explicit caveat that the lower bound alone is insufficient), W5's biconditional (forward via W4/D-SEQ★ min-anchoring; converse via order-convexity with the `{[S,1],[S,3]}` counterexample), W10/W11's avoidance of T7 (correctly grounded in `t₁ = S` + SC-NEQ, with the zeros-bearing denotation example), W12's reachability via *valid* composites discharging J0 ∧ J1★ ∧ J1'★ (content via coupled K.α+K.μ⁺+K.ρ, links via uncoupled K.λ+K.μ⁺_L), and W15's handling of joint K.μ⁻ contraction are all sound.

VERDICT: REVISE
