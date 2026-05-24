# Review of ASN-0094

## REVISE

### Issue 1: Citation precision in LinkAddressNotPrefixOfEmit Step II.2
**ASN-0094, LinkAddressNotPrefixOfEmit Step II.2**: "By T4b (UniqueParse, ASN-0034) applied independently to `b` and `a`, the field projections occupy fixed positional ranges keyed off the shared zero positions: `N(b)` and `N(a)` both occupy positions `1..n_1 − 1`..."
**Problem**: T4b's postcondition states "fields(t) is well-defined and uniquely computable" but the explicit positional formula (segments between zeros) is the content of T4a (SyntacticEquivalence: "maximal contiguous sub-sequence of non-zero positions delimited by the zeros") combined with T4b's uniqueness. The same issue appears in AllocatedAddressAntichain Step 3.2 ("E(x) occupies positions `n_3 + 1 .. #x`").
**Required**: Cite "T4a + T4b" (or T4a + T4b + T4c for the level-to-segment mapping) wherever the proof consumes the positional formula. T4b alone provides only uniqueness, not the formula.

### Issue 2: Appendix NAT-sub Case A — implicit "0 is least element of ℕ"
**ASN-0094, Appendix Case A of existence**: "Base. `m = 0`: by `n ≤ m = 0` and NAT-order on ℕ, `n = 0`"
**Problem**: The step `n ≤ 0 ⟹ n = 0` requires that no natural lies strictly below 0. This is not enumerated among the listed NAT axioms (NAT-order's trichotomy alone admits `n < 0`); it can be derived (e.g., NAT-closure's additive identity makes 0 the carrier's "small end" via well-ordering on `{n ∈ ℕ : n + 0 = n}`), but the appendix neither cites nor proves it. The Peano-rec clause is explicitly admitted as a gap; this implicit clause is not.
**Required**: Either add a one-line derivation ("By NAT-wellorder applied to ℕ, the least element exists; NAT-closure's identity forces it to be 0; so `n ≥ 0` for all `n ∈ ℕ`") or admit this as a second Peano-core supplement alongside (Peano-rec).

### Issue 3: Counterfactual #w ≥ 2 example exhibits a path the main proof doesn't take
**ASN-0094, LinkAddressNotPrefixOfEmit "Sub-case II.B example with `#w ≥ 2`"**: The example constructs a counterfactual `a` (admitted not K.λ-emittable) and closes the contradiction at Step II.1's zero-count additivity, *not* via the home-equality contradiction at Steps II.2–II.3 that the main proof's Sub-case II.B argument actually walks.
**Problem**: A reader following the worked example sees the additivity step rule out the case at Step II.1 and may infer this is how the proof closes Sub-case II.B in general. The proof's actual main path always reaches Steps II.2–II.3 (under the hypothesis `zeros(a) = zeros(b) = 3`, additivity forces `zeros(w) = 0` rather than producing a contradiction at Step II.1). The "Structural observation" and "Why the general additivity argument is preserved" paragraphs document this but require a re-read.
**Required**: Either (a) relocate the `#w ≥ 2` example to a sub-section titled "Generality witness (counterfactual)" so it's not read as a substrate-reachable example, or (b) supplement with a substrate-reachable `#w = 1` example walked through Steps II.1–II.3 inclusive (currently only Step II.0 and the direct position-6 verification are exhibited at `#w = 1`).

### Issue 4: Carve-outs in Sh5(b) audit discipline are not enumerated as categories
**ASN-0094, Sh5(b) "Catalog-wide citation audit" preamble**: The audit table treats two carve-outs — meta-operators (Boolean connectives, set-comprehensions, `argmax`, etc.) and "Common base-machinery accessors" (`A_K^Σ`, `addr(τ)`, `slot_addrs(·)`, `δ(1, #·)`) — as exempt from categories (i)–(iv) of the discipline.
**Problem**: The discipline's "literal name-citation for data symbols" rule appears to be exhaustive at four categories, but in practice the audit walks past five sources (the four categories + base-machinery + meta-operators). A future catalog extension proposing a template citing, say, `coverage(·)` (PrefixSpanCoverage-adjacent) would not obviously qualify — it's neither shape-component, K's name, scaffolding, opt-in, parametric, meta-operator, nor in the four enumerated base-machinery accessors. The catalog author then needs to decide whether to add it to the base-machinery list or reject it.
**Required**: Promote the carve-outs to enumerated categories (v) meta-operators and (vi) framework-internal base-machinery accessors (enumerated explicitly), so the discipline's category set is exhaustive and the audit table's row-by-row check has a fixed reference list.

### Issue 5: Sh4 Case D "Subset-closure derivation" lifts pairwise distinctness from S = A_R^Σ ∪ {τ_new} but the IH only covers A_R^Σ
**ASN-0094, Sh4 Case D**: "Pairwise distinctness on `A_R^Σ ∪ {τ_new}` is established by the IH (which gives pairwise distinctness on A_R^Σ) together with τ_new's slot-pair distinctness from every member of A_R^Σ (the IH is the *off-diagonal* content of Sh4's universal — see the *Universal scope* clarification above — and τ_new's diagonal `(τ_new, τ_new)` case is trivially satisfied by reflexivity of `addr(τ_new) = addr(τ_new)`)."
**Problem**: The off-diagonal content needs both `(τ, τ_new)` and `(τ_new, τ)` directions — Sh4's body is symmetric but stated as a universal over ordered pairs. The step's "τ_new's slot-pair distinctness from every member of A_R^Σ" covers `(τ_new, τ)` direction (no τ in A_R^Σ shares τ_new's slot-pair); the symmetric `(τ, τ_new)` direction also closes from the same fact by symmetry of equality, but the proof should note this explicitly (or pre-symmetrize by noting Sh4's predicate is symmetric in its operands).
**Required**: One line: "the symmetric `(τ, τ_new)` pair closes by symmetry of the slot-pair-equality conjunct" — or pre-state that Sh4's body is symmetric so the off-diagonal is covered uniformly by the single check.

## OUT_OF_SCOPE

### Topic 1: Multi-process atomicity protocol for Sh4 idempotency contract
**Why out of scope**: The framework explicitly commits single-process scope and flags multi-process consistency as a scope boundary. Extending to multi-process substrates requires a coordination protocol not in this ASN's brief.

### Topic 2: Mechanical body-shape uniformity at shape-mate rows
**Why out of scope**: Sh5(a) deliberately downgrades this from commitment to aspiration. A future draft sharpening to a procedural recipe is recorded as open work; the present ASN's hand-curation approach is internally consistent.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: Listed as open design question. The current ASN's commitment to `slot_addrs(F) ⊆ t_F^Σ` (allocated-only) is deliberate; admitting ghost-targeting is future work.

### Topic 4: (0, 0) shapes and sixth-component opt-in registry
**Why out of scope**: Both listed as Open Questions; current bipartite catalog suffices for the present predicate templates.

VERDICT: REVISE
