# Review of ASN-0086

## REVISE

### Issue 1: R0 proof has substantive gaps

**ASN-0086, R0 (TupleAddressFreshness)**: The proof chains L1c → GlobalUniqueness → L-fin → T0(a) → "the L11b witness construction." This skips several required steps.

**Problems**:
1. L11b's witness shows that for any *existing* link, a value-duplicate can be allocated at a fresh address. R0 generalizes to *arbitrary* `(F, G, K)`, not the value of any existing link. The generalization is not derived.
2. L1a (LinkScopedAllocation) requires that the fresh address be under an *allocated document*. R0's statement has no precondition `dom(Σ.M) ≠ ∅`; with an empty arrangement family, no link allocation is admissible, and R0's existential fails.
3. The proof asserts "the set of valid link addresses within any document's link subspace is countably infinite" but does not connect T0(a)/T0(b) to the specific subset that is simultaneously (i) T4-valid, (ii) T10a-conforming under an existing document, (iii) in subspace `s_L`, and (iv) satisfying `#E(a) ≥ 2`. The connection is sketchable but not sketched.
4. Invariants L0, L1, L1a, L1b for the new address are not verified — the proof relies on "L11b witness preserves all invariants" without showing why that generalizes to arbitrary `(F, G, K)`.
5. The non-emptiness of `K` (required by L3, NEndsetStructure) is not derived. It does follow from `K ∈ T_cat` plus L3 on the witnessing emission, but the chain is not stated.

**Required**: Either add an explicit precondition `dom(Σ.M) ≠ ∅` and walk through the chain construction explicitly, verifying each L-invariant against the new emission; or strengthen L11b in ASN-0043 to handle arbitrary `(F, G, K)` and cite that directly.

### Issue 2: R4 proof overstates L14's actual content

**ASN-0086, R4 (TupleAddressDisjointness)**: "By L14 (DualPrimitive, ASN-0043), `dom(Σ.C) ∩ dom(Σ.L) = ∅`."

**Problem**: L14 in ASN-0043 actually states scoped disjointness: `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅`. The global form (which R4 asserts) only follows "whenever every content address is `s_C`-resident" — a hypothesis ASN-0036 does not enforce universally. The proof asserts the conclusion that L14 *defers*.

**Required**: Either (a) introduce an explicit hypothesis that all content is `s_C`-resident in ASN-0086's setup, then derive R4 from L0 + T7 + that hypothesis; or (b) restate R4 as scoped disjointness matching L14's actual content.

### Issue 3: T7 cited by incorrect name

**ASN-0086, R4 commentary**: "By T7 (SubspaceDisjointness, ASN-0034), addresses in different subspaces are permanently distinct as tumblers..."

**Problem**: T7 in ASN-0034 is named `FirstElementFieldDistinction`. There is no claim named `SubspaceDisjointness` in the foundation. The cited content (distinct first element-field components imply distinct tumblers) does belong to T7, but the name is wrong.

**Required**: Cite as `T7 (FirstElementFieldDistinction, ASN-0034)`.

### Issue 4: T_cat bootstrap problem in Emit_K precondition

**ASN-0086, Definition of Emit_K**: "For `K ∈ T_cat` and finite endsets `F, G`..." and "T_cat = {Θ ∈ Endset : (E a ∈ dom(Σ.L) :: |Σ.L(a)| ≥ 3 ∧ Σ.L(a).type = Θ)}".

**Problem**: T_cat is the set of types *currently in use* at some state. Emit_K's precondition `K ∈ T_cat` therefore cannot be satisfied for any type that has not yet been used. A genuinely new type cannot be introduced — the operation is impossible for it. This is acknowledged in open question 7 but the formal precondition remains unworkable.

**Required**: Either (a) relax Emit_K's precondition to `K ∈ Endset` with `K ≠ ∅` (so the resulting state's T_cat includes K post-emission), or (b) make T_cat state-parameterized and clarify which state's catalog the precondition references. The current statement is structurally circular.

### Issue 5: R ∈ T_cat fails at empty initial state

**ASN-0086, Definition of RetractionType**: "Fix a designated type `R ∈ T_cat` reserved for retraction."

**Problem**: At any state with no retraction yet emitted, `R ∉ T_cat` by the Definition of T_cat. The "fix `R ∈ T_cat`" prose conflicts with T_cat's evaluation as "types actually in use." For the active subset `A_K^Σ` to be well-defined at the initial state (Σ_0 with empty Σ.L), R6 must hold even when `R ∉ T_cat`.

**Required**: Either (a) define `L_R` independently of T_cat membership (it is well-defined as ∅ when no retraction exists), or (b) define T_cat to include reserved types regardless of use. The Definition as written is inconsistent at the initial state.

### Issue 6: L_K silently restricts to arity exactly 3, not arity ≥ 3

**ASN-0086, Definition of TypedRelation**: `L_K = {(a, F, G) : a ∈ dom(Σ.L) ∧ Σ.L(a) = (F, G, K) ∧ |Σ.L(a)| ≥ 3}`.

**Problem**: The pattern match `Σ.L(a) = (F, G, K)` constrains the link to be exactly a 3-tuple. If `|Σ.L(a)| > 3`, then `Σ.L(a)` is a 4-tuple (or longer) and cannot equal a 3-tuple. So the clause `|Σ.L(a)| ≥ 3` is redundant — it really should be `= 3`. The text "For the rest of this development we restrict attention to standard-triple links — those with `|Σ.L(a)| ≥ 3`" further muddles this: standard-triple means arity = 3 (per ASN-0043's StandardTriple convention), and the Definition silently excludes higher-arity links from L_K. Higher-arity links exist in `dom(Σ.L)` (admitted by L3) but are not members of any `L_K`.

**Required**: Change `|Σ.L(a)| ≥ 3` to `|Σ.L(a)| = 3` in the Definition, and clarify in prose that L_K's construction restricts to arity 3 and higher-arity links are not covered.

### Issue 7: State-dependence of A, A_doc, A_rel not made explicit

**ASN-0086, Definition — AddressUniverse, Partition**: `A = dom(Σ.C) ∪ dom(Σ.L)`, `A_doc = dom(Σ.C)`, `A_rel = dom(Σ.L)`.

**Problem**: All three are functions of state Σ — they grow as the system evolves. The notation lacks a Σ subscript, suggesting state-independence. Later statements such as "tuple addresses and document addresses are disjoint" make sense only when read state-by-state.

**Required**: Either consistently write `A^Σ`, `A_doc^Σ`, `A_rel^Σ`, or include a one-line note that all three are state-dependent and the symbols `A`, `A_doc`, `A_rel` denote their evaluation at the ambient state.

### Issue 8: Worked sketch does not address coverage-extension nullification

**ASN-0086, Worked Sketch Step 1**: "nullified(Σ_1) = {a₁} — `a₁` is in the to-set's coverage."

**Problem**: By PrefixSpanCoverage, `coverage({(a₁, δ(1, #a₁))}) = {t ∈ T : a₁ ≼ t}`, which contains *every* tumbler extending `a₁`. The Definition of `nullified(Σ)` intersects with A_rel, so the actual `nullified(Σ_1)` is `{a ∈ A_rel : a₁ ≼ a}`. If any other link address extends `a₁` (e.g., a sub-allocator scenario), that address is also nullified by the same retraction. The sketch presents `nullified(Σ_1) = {a₁}` without arguing why no other A_rel element extends `a₁`.

**Required**: Either (a) note that under T10a's allocator discipline, no two distinct link addresses are in a prefix relationship (by T10a.5 CrossAllocatorIncomparability, ASN-0034, when not in ancestor-descendant), so the single-address conclusion is justified; or (b) revise the example to use a span construction whose coverage is exactly `{a₁}` rather than `{t : a₁ ≼ t}`.

### Issue 9: R6a proof treats coverage as state-dependent

**ASN-0086, R6a proof**: "By R2, coverage(G') evaluated at Σ' equals coverage(G') evaluated at Σ (the endset value is preserved)."

**Problem**: `coverage : Endset → ℘(T)` is a pure function on endset values — it has no state argument. The proof phrasing suggests otherwise. What the proof actually needs is: the endset value `G'` is preserved by R2, hence `coverage(G')` (a single set, computed once from G') is the same set referenced in both `nullified(Σ)` and `nullified(Σ')`.

**Required**: Reword as: "By R2, the endset `G'` stored at `b` is preserved across Σ → Σ'; `coverage(G')` is a function of `G'` alone, so the membership condition `a ∈ coverage(G')` evaluates identically in both states."

### Issue 10: Emit_K signature omits state transition

**ASN-0086, Definition of Emit_K**: `Emit_K(F, G) → A_rel`.

**Problem**: The operation transforms Σ → Σ' as well as producing an address. The signature shown gives only the return type. The body of the Definition does describe the state transition, but a reader scanning signatures sees only "address out, nothing in" — confusing for an operation that is the primary state mutator.

**Required**: Adjust the signature to reflect state effect — e.g., `Emit_K : Σ × Endset × Endset → Σ' × A_rel` — or annotate the signature line with "(state transition)".

### Issue 11: Implicit assumption of s_C-resident content not stated as hypothesis

**ASN-0086, throughout**: The proofs of R4 and the surrounding commentary about "residence in disjoint subspaces (s_C and s_L)" assume content addresses occupy subspace s_C.

**Problem**: ASN-0036 supplies S7c which defines `subspace_I(a)` for `a ∈ dom(Σ.C)` but does not constrain its value to s_C globally. S7a, S7b, S7c, S7d together do not entail `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`. ASN-0086 nonetheless treats this as automatic in its discussion of disjoint subspaces.

**Required**: State as an explicit setup assumption at the start of the ASN: "We work in systems satisfying ASN-0043 and additionally `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)` — globally s_C-resident content." This makes R4 derivable as stated, and aligns with the structural argument given.

### Issue 12: R5's META status and the gap from "no derived constraint" to permission

**ASN-0086, R5 (TupleSelfTargeting)**: "...nothing in L0–L14, L-fin, S0–S3 forbids `coverage(F) ∩ A_rel ≠ ∅` or `coverage(G) ∩ A_rel ≠ ∅`."

**Problem**: R5 is correctly classified META, but the justification appeals to absence of constraint from a *specific list*. Are these the only invariants? What about S7a–S8 in ASN-0036, or L8–L14a (e.g., L14a explicitly forbids transclusion to link addresses — does this affect endset references to link addresses through M(d)? No, because L14a is about M, not L)? The list-of-invariants argument is verifiable but should be exhaustive over the foundation invariants actually in scope, not partial.

**Required**: Extend the cited list to all invariants of ASN-0036 and ASN-0043 that mention endsets, coverage, or link-address membership; verify each. Alternatively, cite the positive permission directly: L4(c) explicitly states cross-subspace endsets are permitted and L13 establishes link addresses as valid span targets — these two together *grant* the construction; absence-of-constraint is a weaker argument than presence-of-permission.

## OUT_OF_SCOPE

### Topic 1: Concurrency and atomicity of Emit/Observe

**Why out of scope**: The substrate operates over a single state at a time; concurrent access is acknowledged in open question 5. This ASN appropriately abstracts away the concurrency model.

### Topic 2: Multi-arity typed relations beyond arity 3

**Why out of scope**: The ASN restricts to standard triples by design and acknowledges higher-arity extension as open question 2.

### Topic 3: Type catalog extension across uncoordinated layers

**Why out of scope**: Open question 7 explicitly defers this. The bootstrap problem in Issue 4 above is a separate issue (the formal definition is internally inconsistent), but the broader question of dynamic catalog extension is correctly out of scope.

### Topic 4: Cardinality bounds on nullified(Σ) relative to dom(Σ.L)

**Why out of scope**: Open question 6 raises this; it is a substrate-design question beyond the relational vocabulary's structural claims.

VERDICT: REVISE
