# Review of ASN-0094

## REVISE

### Issue 1: ShapeWellFormedness biconditional reading is awkward and requires disambiguation prose

**ASN-0094, ShapeWellFormedness Definition**: "is *syntactically well-formed* iff `t_F = - ⟺ c_F = 0` and `t_G = - ⟺ c_G = 0`."

**Problem**: The biconditional requires the entire "Reading of the biconditional" paragraph to disambiguate that it tests the *literal* registry value `0`, not the broader set `{0, 0|1}`. The reading "biconditional fires only on literal 0, vacuous under `0|1`" is non-standard. A reader's natural interpretation of `c_F = 0` as a Boolean equality test on `c_F`'s value would conflict with the intended semantics under `c_F = 0|1`. The Provenance shape `(1, 0|1, A, A, ⊤)` only escapes ill-formedness via this non-standard reading.

**Required**: Replace the biconditional with two explicit implications: `c_F = 0 ⟹ t_F = -` and `t_F = - ⟹ c_F = 0`. State directly that `0|1` is a distinct registry value from `0`, so neither implication fires at `c_F = 0|1`, leaving `t_F` free to take any of `A_doc, A_rel, A`. The two-implication form removes the disambiguation burden.

### Issue 2: Sh4 layer-discipline contract operates on potentially undefined inputs

**ASN-0094, Sh4 contract clause (i.a)**: "Query `Observe_K(slot_addrs(F), slot_addrs(G), oper)` — a well-typed call... (the layer's caller must hand `Emit_K` canonical-form F and G or fail Sh-conf clauses (a)/(b); the contract here is evaluated on the same canonical-form values the caller intends to emit)."

**Problem**: The contract executes *before* Sh-conf's gates. If the caller hands a non-canonical F, then `slot_addrs(F)` is undefined, the contract's behavior is undefined, and the Sh-conf rejection downstream is never reached because the contract has already taken an undefined step. The chain "the caller commits to canonical form" is a layered assumption that the contract itself does not verify. The same gap applies to FDD's contract.

**Required**: Either (a) explicitly specify that Sh-conf clauses (a) and (b) execute before the Sh4 contract clauses (i)–(iii) — making `slot_addrs` well-defined by precondition — or (b) bake a canonical-form pre-check into clause (i) itself. The current phrasing leaves ordering implicit.

### Issue 3: FunctionalDependencyDiscipline preservation delegated by hand-wave

**ASN-0094, FunctionalDependencyDiscipline preservation**: "We omit the formal Cases A/B/C bookkeeping; the structure is identical to Sh4's modulo this substitution of `C_fd` for `C`."

**Problem**: This is exactly the "by similar reasoning" pattern the rubric calls out. The argument for Case D exclusion (shape-tuple inequality with R) is given explicitly, but the positive claim that A/B/C preserve FDD under the substitution is asserted, not shown. A reader cannot verify by inspection that FDD's broader candidate set `C_fd` (matching F-slot only) does not break some step of the original A/B/C arguments — e.g., the argument in Case B that `C = ∅` plus IH gives distinctness on `A_K^Σ ∪ {τ_new}` depends on what `C` measures.

**Required**: Either execute Cases A/B/C explicitly for FDD (one paragraph each), or extract a precise lemma: "Sh4's preservation argument is invariant under substituting any predicate `P` satisfying [stated properties] for the slot-pair-match predicate, and FDD's from-slot-equality predicate satisfies these properties." Then cite the lemma.

### Issue 4: A_doc/A_rel naming inherited from ASN-0086 conflicts with prose "document" usage

**ASN-0094, throughout the catalog and walkthroughs**: "DirectedPair (1, 1, A_doc, A_doc, ⊤)" with prose "doc-to-doc directed pair"; worked example "pre-allocate `d_1, d_2 ∈ A_doc^{Σ_0}`" with prose "a comment about a document".

**Problem**: ASN-0086 defines `A_doc^Σ = dom(Σ.C)` — content addresses, distinct from `dom(Σ.M)` (document-level container addresses). ASN-0094's prose refers to "documents" in ways that suggest document-level reasoning (e.g., "is this document classified as K"), but the catalog's `A_doc` symbol targets content addresses. The framework provides no target-domain symbol for `dom(Σ.M)` addresses — shape constraints cannot target document-level containers at all. A reader interpreting "DirectedPair (A_doc, A_doc)" as "between document containers" misreads the framework's reach.

**Required**: Add a sentence at the catalog introduction: "Throughout this catalog, `A_doc` denotes content addresses (per ASN-0086, `A_doc^Σ = dom(Σ.C)`), not document-level container addresses (which live in `dom(Σ.M)` and are not directly targetable by shape constraints)." Without this, the framework's reach — what it can constrain — is ambiguous on every catalog row.

### Issue 5: Multi-slot Observe_K over-approximation generalized implicitly

**ASN-0094, Sh4 contract clause (i.a)**: "...the Observe over-approximates exact slot-set equality by `slot_addrs(F_τ) ⊇ slot_addrs(F)` (each x ∈ slot_addrs(F) is forced to also lie in slot_addrs(F_τ))..."

**Problem**: The over-approximation argument's per-element step ("for each x ∈ slot_addrs(F), x ∈ A^Σ by Sh-conf (d); the pattern x ∈ coverage(F_τ) requires some y ∈ slot_addrs(F_τ) with y ≼ x; by AllocatedAddressAntichain at x, y = x") is justified for the single-slot case. For shapes with `c_F = *` admitting `n ≥ 2` slot addresses, the multi-element generalization is asserted parenthetically but not written. The Retraction shape uses `c_F = *`, so this case is part of the framework's reach.

**Required**: Spell out the per-element multi-slot argument explicitly in clause (i.a). One additional sentence suffices ("Apply AllocatedAddressAntichain at each x ∈ slot_addrs(F) separately; quantifying gives slot_addrs(F) ⊆ slot_addrs(F_τ).").

### Issue 6: No worked example exercises `c_F = *` with non-empty F

**ASN-0094, worked examples**: The Retraction shape has `c_F = *`, and the framework's Sh0–Sh3 are stated for arbitrary cardinality. Worked examples only exercise `n ∈ {0, 1}`: K=comment uses `c_F = 1`; Nullify uses `F = ∅` (the `n = 0` boundary).

**Problem**: The framework's invariants are stated for any cardinality matching `c_F`, but only `n ∈ {0, 1}` cases are concretely verified. An attributed retraction with non-empty F (e.g., `F = {(d_retractor, δ(1, #d_retractor))}` for `n = 1`, or two attributers for `n = 2`) is mentioned in prose under Retraction but never exercised. The multi-slot over-approximation argument from Issue 5 particularly applies to this case.

**Required**: Add a worked example exercising attributed retraction at Retraction's shape with `slot_addrs(F) = {d_attr1}` (n=1) and/or `{d_attr1, d_attr2}` (n=2). Verify Sh-conf admittance and Sh0 directly on the resulting `A_R^Σ`.

### Issue 7: K = comment worked example does not derive emission addresses

**ASN-0094, Worked Example K = comment**: "Let the result be Σ_1 with new tuple `τ_1` at address `a_1 := addr(τ_1)`."

**Problem**: The K=comment example introduces `a_1, a_2` as abstract names without deriving them from K.λ's first/subsequent emission rule. The Coverage walkthrough (Additional Worked Examples) does derive these explicitly as `[d_K.0.s_L.1]` and `inc(a_1, 0)`. The asymmetry leaves the main worked example less self-contained — Issue 5/Issue 6 verification depends on knowing exactly what address each emission lands at, which the example does not show.

**Required**: Compute `a_1 = [home_K.0.s_L.1]` from K.λ's first-emission branch (`{ℓ' ∈ dom(Σ.L) : origin(ℓ') = home_K} = ∅` at Σ_0) and `a_2 = inc(a_1, 0)` from the subsequent-emission branch. Match the Coverage walkthrough's level of detail.

### Issue 8: "(b')" reference in Sh5 status is an undefined editing artifact

**ASN-0094, Sh5 status (b)**: "The discipline is what makes Sh5's per-shape organization falsifiable in the sense of (b'): a catalog row with diverging base templates from a shape-mate row would visibly violate the discipline."

**Problem**: There is no `(b')` defined anywhere in Sh5 or the surrounding text. The status splits into `(a) META observation` and `(b) META discipline`; `(b')` appears to be a typo for `(b)`. The reference distracts readers searching for what `(b')` refers to.

**Required**: Replace `(b')` with `(b)` or rephrase to "in the sense of the discipline (b)".

## OUT_OF_SCOPE

### Topic 1: Closure theorem for the composition language
**Why out of scope**: Whether composed predicates strictly extend the atomic template language is acknowledged in Consequence (b) as not established. This is future framework work.

### Topic 2: Cross-process consistency of the shape registry
**Why out of scope**: Lifetime constancy is asserted within a single process. Cross-process synchronization belongs to a distributed-substrate framework not yet specified.

### Topic 3: Additional shape rows for unhandled cardinality patterns
**Why out of scope**: The catalog enumerates rows demanded by present-day templates. Many-to-many shapes (`(*, *, ·, ·, ·)`) and similar are future catalog extensions.

### Topic 4: Ghost-targeting in slot positions
**Why out of scope**: Listed explicitly as an open question. Admitting unallocated slot addresses requires a separate design.

### Topic 5: Sixth shape component for opt-in disciplines
**Why out of scope**: Listed explicitly as an open question. Promoting FDD/SingleHomeCoverageDiscipline to first-class shape components is a future refactoring decision.

VERDICT: REVISE
