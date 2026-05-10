# Local Review — ASN-0034 (cycle 1)

*2026-04-23 18:20*

81 claims

## REVISE

### NAT-discrete

#### Equivalence of the two axiom forms unjustified
**Class**: REVISE
**Issue**: The Axiom slot lists two forms joined by "equivalently":
`(A m, n ∈ ℕ :: m < n ⟹ m + 1 ≤ n)` and `(A m, n ∈ ℕ :: m ≤ n < m + 1 ⟹ n = m)`.
Neither the narrative nor the contract establishes the equivalence. The equivalence is not free from the body alone — it relies on NAT-order's exactly-one trichotomy, irreflexivity, and disjointness of `<` and `=` (for the direction "¬(m+1 ≤ n) via trichotomy ⟹ n < m+1" and for discharging `m < n` under `n = m` via irreflexivity). Bundling two non-trivially-equivalent propositions under "Axiom" with "equivalently" leaves the axiomatic commitment ambiguous: a downstream consumer cannot tell whether both are posited or one is derived.
**Required**: Pick one form as the *Axiom* (the standard choice is `m < n ⟹ m + 1 ≤ n`) and promote the other to a *Consequence* with a brief derivation citing the NAT-order clauses actually used (irreflexivity, exactly-one trichotomy, disjointness). The narrative should include the short bidirectional argument that currently is missing.

#### Depends rationale for NAT-order understates what is used
**Class**: REVISE
**Issue**: The Depends entry for NAT-order cites only "the non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`)". Once the equivalent form is treated as a Consequence, NAT-order is also used for (i) exactly-one trichotomy on `(m+1, n)` to obtain `n < m+1` from `¬(m+1 ≤ n)`, (ii) irreflexivity to contradict `m < m` when `n = m` is substituted into `m < n`, and (iii) disjointness of `<` and `=` in the trichotomy closure. The current rationale hides these usages.
**Required**: Expand the NAT-order Depends rationale to state that the equivalence also draws on NAT-order's irreflexivity, exactly-one trichotomy, and disjointness clauses — not only the `≤` definition.

VERDICT: REVISE

### T0(b)

#### Missing dependency declarations
**Class**: REVISE
**Issue**: The proof uses two facts not supplied by the single declared dependency T0. (a) "each component `dᵢ = 1 ∈ ℕ`" requires `1 ∈ ℕ`, which is NAT-closure's export — T0 uses it internally but does not re-export it to downstream consumers. (b) The step "`#t = n`, and `n ≥ n`" invokes reflexivity of `≥` on ℕ, which is supplied by NAT-order (the non-strict total order). Neither NAT-closure nor NAT-order appears in the Depends list, yet both are load-bearing in the construction and the final inequality.
**Required**: Extend Depends to include NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the witness components `dᵢ = 1`; and NAT-order (NatStrictTotalOrder) — supplies reflexivity `n ≥ n` used to discharge `#t ≥ n`.

VERDICT: REVISE

### NAT-addcompat

#### Depends blurb for NAT-order omits the strict relation `<`
**Class**: REVISE
**Issue**: The NAT-order depends bullet reads: "supplies the non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`), used in the antecedents `p ≤ n` and the consequents `m + p ≤ m + n` and `p + m ≤ n + m` of both compatibility clauses." It only accounts for the two compatibility clauses. The third axiom clause, `n < n + 1`, uses the primitive strict relation `<` — NAT-order's actual root symbol — and that usage is not declared in the depends blurb. The narrative paragraph similarly says the strict successor inequality "uses that same closed addition together with NAT-closure's `1 ∈ ℕ`" without naming NAT-order as the source of `<`. A downstream reader auditing what each dependency supplies would see no declared grounding for `<` in `n < n + 1`, so the axiom body cannot "be read without silently importing" NAT-order's primitive — exactly the guarantee the depends slot is meant to provide.
**Required**: Extend the NAT-order depends bullet (and the matching narrative sentence) to record that NAT-order also supplies the primitive strict order `<`, used in the strict successor inequality `n < n + 1`. For example: "supplies the primitive strict order `<` (used in `n < n + 1`) and its non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`, used in the antecedents `p ≤ n` and the consequents `m + p ≤ m + n` and `p + m ≤ n + m` of both compatibility clauses)."

VERDICT: REVISE

### T3

#### Narrative conflates extensional equality with canonical normalization
**Class**: REVISE
**Issue**: The claim is labeled "CanonicalRepresentation" / "Canonical form" and motivates itself through Gregory's `tumblerjustify`, leading-zero handling, and `iszerotumbler` misclassification. But the formal content — `a = b ⟺ #a = #b ∧ (A i : ... : aᵢ = bᵢ)` — is only extensional sequence equality, which is trivially given by T0 defining `T` as finite sequences over ℕ. Extensional equality does not establish that each "value" has a unique canonical representative; that would require an equivalence on sequences (e.g., collapsing leading-zero variants) plus a normalization selecting a unique witness. As stated, every sequence is its own element of `T`, so `[0,0,5]` and `[0,7]` are already distinct, and no normalization is needed or established. A downstream consumer citing T3 as a "canonical representation" guarantee will be misled.
**Required**: Either (a) rename the claim to "ExtensionalEquality" / "SequenceEqualityIsComponentwise" and drop the `tumblerjustify`/zero-detection motivation (it belongs with a separate claim about comparison-function correctness under normalization), or (b) strengthen T3 to actually assert canonical representation: introduce a value-denotation relation on sequences and posit a normalization function whose image is a set of unique representatives, with the corresponding proof obligations. Do not present a trivial extensionality fact under a label that promises normalization.

#### "Extensional definition of sequence equality" not supplied by T0
**Class**: REVISE
**Issue**: The proof ends with "the biconditional restates the extensional definition of sequence equality," and the Depends line says T0 gives "extensional definition of sequence equality for T." But T0 only says `T` is the set of nonempty finite sequences over ℕ with a length operator `#·` and projection `·ᵢ`; it does not state that two sequences with equal length and equal components are equal. The forward direction of the proof ("they are identical as sequences by extensional equality") therefore appeals to a principle not actually in T0's contract. It is a standard assumption about finite sequences, but as written the dependency chain has a gap.
**Required**: Either add extensional equality of finite sequences to T0's axiom explicitly (e.g., "sequences `a, b` are equal iff `#a = #b` and `aᵢ = bᵢ` for `1 ≤ i ≤ #a`"), or declare T3 itself as an `*Axiom:*` of sequence extensionality rather than deriving it, and update the Depends note accordingly.

#### Formal contract field mismatch
**Class**: REVISE
**Issue**: The formal contract lists `*Postcondition:*`. But T3 has no preconditions/inputs/operation — it is a universally quantified property of the carrier set. Under the checklist's field definitions, this is either an `*Axiom:*` (if taken as sequence extensionality by design) or at most a theorem stated as a bare biconditional. "Postcondition" implies there was an operation with a pre-state, which there isn't here.
**Required**: Replace `*Postcondition:*` with `*Axiom:*` (if adopting extensionality as primitive — see prior finding) or restructure as a plain theorem statement matching the other derived claims in the ASN.

VERDICT: REVISE

### NAT-sub

#### Right-telescoping presumes undeclared addition-order interaction
**Class**: REVISE
**Issue**: The clause `(A m, n ∈ ℕ :: (m + n) − n = m)` has no precondition, yet for `(m + n) − n` to denote an ℕ-element via this same axiom's conditional closure, `m + n ≥ n` must hold. Neither declared dependency supplies this. NAT-closure gives only the signature `+ : ℕ × ℕ → ℕ`, `1 ∈ ℕ`, and left identity `0 + n = n`; NAT-order says nothing about `+`. The fact `m + n ≥ n` (for all m, n ∈ ℕ) is nowhere grounded — it requires addition monotonicity or an additive-dominates-right-operand lemma that simply does not exist in the declared foundations. The narrative never mentions that the telescoping clause requires `m + n ≥ n` and never cites where this is established.
**Required**: Either (a) add a precondition `m + n ≥ n` to the right-telescoping clause, making it `(A m, n ∈ ℕ : m + n ≥ n : (m + n) − n = m)` with an accompanying missing-claim tag for the undeclared fact, or (b) depend on (and create, if absent) a NAT claim establishing `m + n ≥ n` for all m, n ∈ ℕ, and cite it explicitly both in the narrative grounding paragraph and in Depends.

#### Signature of `−` is never posited in the Formal Contract
**Class**: REVISE
**Issue**: NAT-closure opens its Axiom slot with `+ : ℕ × ℕ → ℕ` and NAT-order opens with `< ⊆ ℕ × ℕ` — a deliberate register the narrative here explicitly invokes for other primitives. NAT-sub introduces `−` as a brand-new primitive but the Formal Contract lists no signature clause for it. The only indirect typing is conditional closure `m ≥ n ⟹ m − n ∈ ℕ`, which constrains the codomain at defined inputs but does not posit `−` as a function (i.e., single-valued on its domain of definition). Consequently the narrative's assertion that `m − n` is *unique* is not entailed by the Formal Contract: existence plus right-inverse together do not give uniqueness without right-cancellation of `+`, which is not declared anywhere.
**Required**: Add an explicit signature clause to the Axiom slot, e.g. `− : {(m, n) ∈ ℕ × ℕ : m ≥ n} → ℕ` (partial binary operation), so that single-valuedness — and hence the uniqueness claimed in the narrative — is established by positing rather than by derivation from non-existent cancellation.

### TA5-SIG

#### m ≥ 2 step uses uncited NAT-addcompat clause
**Class**: REVISE
**Issue**: The derivation `i₀ + 1 ≤ m then yields m ≥ 2 ≥ 1` asserts `m ≥ 2`, which requires `2 ≤ i₀ + 1` (obtained from `1 ≤ i₀` via right order compatibility of addition). The Depends citation for NAT-addcompat names only the *strict successor inequality* clause (`n < n + 1`), not right order compatibility (`p ≤ n ⟹ p + m ≤ n + m`). Since the rest of the reasoning uses NAT-sub's conditional closure, right-inverse, and strict-monotonicity preconditions — all of which only require `m ≥ 1`, not `m ≥ 2` — the stronger inequality is both ungrounded in cited clauses and unnecessary. The claim's convention elsewhere (e.g., NAT-sub's citation enumerating conditional closure, right-inverse, right telescoping, strict monotonicity individually) is to name each clause used; NAT-addcompat's citation departs from that convention here.
**Required**: Either (a) weaken the intermediate statement to `m ≥ 1`, deriving it from the already-cited strict successor inequality `i₀ < i₀ + 1` chained with `i₀ + 1 ≤ m` and `1 ≤ i₀` via NAT-order transitivity; or (b) expand the NAT-addcompat Depends citation to include the right order compatibility clause and note its role in lifting `1 ≤ i₀` to `2 ≤ i₀ + 1`.

VERDICT: REVISE

### TA5a

#### T4(iii) `t'₁ ≠ 0` never verified
**Class**: REVISE
**Issue**: The opening enumerates T4's four conditions: "(i) zeros(t) ≤ 3, (ii) no two zeros adjacent, (iii) t₁ ≠ 0, (iv) t_{#t} ≠ 0", and the subsequent cases substantively discharge (i), (ii), and (iv) — but (iii) is never explicitly verified in any of the cases k=0, k=1, k=2. For k=0 the component at index 1 could be touched when sig(t) = 1 (i.e., when #t = 1), where t'₁ = t₁ + 1; the argument that t'₁ + 1 ≠ 0 (via NAT-closure + NAT-zero + NAT-addcompat) happens to run for position sig(t) generically but is never instantiated at position 1. For k=1 and k=2, TA5(b) gives t'₁ = t₁ so (iii) is transferred from T4(iii) for t, but this transfer is also not stated. "T4 preserved unconditionally" is therefore overstated: the argument as written covers (i), (ii), (iv) only.
**Required**: Add an explicit line per case deriving t'₁ ≠ 0 — in k=0, split on sig(t)=1 (giving t'₁ = t₁ + 1 ≠ 0 by the same NAT chain used at sig(t)) vs sig(t)≠1 (giving t'₁ = t₁ ≠ 0 by TA5(b) and T4(iii) on t); in k=1 and k=2, cite TA5(b) on the original-position range 1 ≤ i ≤ #t together with T4(iii) on t.

#### T4a declared in Depends but not used in the proof
**Class**: REVISE
**Issue**: The Depends bullet for T4a describes it as "supporting the case k ≥ 3 interpretation that adjacent zeros create an empty field." But the actual case k ≥ 3 argument instantiates T4(ii) directly at i = #t + 1 to derive the contradiction ¬(0=0 ∧ 0=0); T4a's field-segment-non-emptiness equivalence is never invoked. The *Failure* entry's phrase "adjacent zeros create an empty field" is interpretive prose, not a proof step. This is a declared-but-unused dependency — the proof would read identically if T4a were removed from Depends.
**Required**: Either remove T4a from Depends (the proof uses T4(ii) directly), or rewrite the k ≥ 3 step to actually cite T4a — e.g., by reading the two adjacent zeros as witnessing an empty interior field segment and citing T4a's forward direction to convert that into the T4(ii) violation.

### T10a

#### NAT-sub declared in T10a.3 depends but not used in reasoning
**Class**: REVISE
**Issue**: The Formal Contract for T10a.3 declares `NAT-sub (closure and right-telescoping for the subtraction form)`. The narrative argument for length separation, however, proceeds entirely additively: `k' ≥ 1` (via T0, NAT-zero, NAT-discrete) is lifted to `#t + 1 ≤ #t + k'` by NAT-addcompat's left order-compatibility, and `#t < #t + 1` by its strict successor inequality. No subtraction form appears anywhere in the T10a.3 narrative — there is no "subtraction form" of the separation statement to ground. Per the declared-vs-used check, NAT-sub should not be in the depends list.
**Required**: Remove NAT-sub from T10a.3's *Depends*, or — if the intent is to expose the separation as `#output(B) − #output(A) > 0` — add the explicit subtraction derivation in the narrative and retain NAT-sub accordingly.

#### T10a-N *Depends* mismatched with narrative
**Class**: REVISE
**Issue**: T10a-N's narrative explicitly references TA5a and Consequence 4 (= T10a.4): "`k' ∈ {1, 2}` is necessary for T4 preservation (Consequence 4, TA5a)… root T4 initialization seeds Consequence 4." Neither TA5a nor T10a.4 appears in T10a-N's declared *Depends*. Conversely, T10 is declared in T10a-N's *Depends* but no clause of the T10a-N narrative cites T10 (the necessity argument is entirely internal to T10a.2 / TA5 / Prefix / Consequences 4 and 5).
**Required**: Add `TA5a` and `T10a.4` to T10a-N's *Depends*; remove `T10` if it is not actually load-bearing in the necessity argument, or add the explicit citation showing where T10 is invoked.

VERDICT: REVISE

### T10a.7

#### Subtraction in the induction lacks a declared NAT dependency
**Class**: REVISE
**Issue**: The proof parameterizes its induction via "the gap `d = n - m ≥ 1`" and, in the inductive step, forms `n - 1` and asserts `(n - 1) - m = d` and `m < n - 1 < n`. These are natural-number subtraction facts (closure of subtraction under `m < n`, successor subtraction, `(n-1)-m = (n-m)-1`), none of which are discharged by the five declared dependencies (T10a, TA5(a), T1(a), T1(c), NAT-order). NAT-order supplies only order properties; it does not provide subtraction or `m < n ⟹ ∃d ≥ 1 : n = m + d`. T10a.3 establishes the precedent of citing NAT-sub / NAT-closure / NAT-addcompat when such arithmetic is invoked; T10a.7's contract omits them despite the proof using them.
**Required**: Either (a) add the missing arithmetic dependencies (NAT-sub for subtraction closure and telescoping; NAT-closure / NAT-addcompat for the `n - 1` manipulation) and cite them at the point of use, or (b) reformulate the induction to avoid subtraction entirely — e.g., induct on `d ≥ 1` over the statement `(A m ≥ 0 :: tₘ < t_{m+d})`, with base `d = 1` via TA5(a) and step `t_{m+(d+1)} = inc(t_{m+d}, 0) > t_{m+d}` chained with IH via T1(c). Option (b) is cleaner and keeps the dependency list minimal.

### T10a.3

#### NAT-discrete path to `d_B − d_A ≥ 1` has a logical gap
**Class**: REVISE
**Issue**: The local-monotonicity paragraph asserts: "NAT-sub's conditional-closure … places `d_B − d_A ∈ ℕ`; NAT-zero gives `0 ≤ d_B − d_A`; NAT-discrete at `m = 0` rules out `0 ≤ d_B − d_A < 1`, yielding `d_B − d_A ≥ 1`." NAT-discrete at `m = 0` says `0 ≤ n < 1 ⟹ n = 0` — it does not by itself rule out the interval, it only collapses it to `{0}`. To get `d_B − d_A ≥ 1` from the declared axioms one must still exclude `d_B − d_A = 0`, which requires NAT-sub's right-inverse (`0 + d_A = d_B ⟹ d_A = d_B`) plus NAT-order irreflexivity against `d_B > d_A`, or NAT-closure's left-identity — none of these are declared or invoked here. The direct route is NAT-sub's *strict positivity* (`m > n ⟹ m − n ≥ 1`), which is also not in the dependency narrative ("conditional closure and right telescoping").
**Required**: Replace the NAT-discrete step with a cite to NAT-sub's strict-positivity clause (and add it to the NAT-sub dependency line), or spell out the missing contradiction step using right-inverse + irreflexivity and add those to NAT-sub's and NAT-order's dep entries.

### T10a.6

#### Witness-uniqueness corollary missing from formal contract
**Class**: REVISE
**Issue**: The narrative explicitly establishes a "Consequence (witness uniqueness)": "When `same_allocator(a, b)` holds, the allocator `A` with `a, b ∈ dom(A)` is unique." T10a's own contract for T10a.6 also lists this as an exported postcondition ("Witness-uniqueness corollary: `same_allocator(a, b)` determines the witnessing A uniquely"). T10a.7 relies on this corollary to lift per-chain injectivity into single-valued indices `(i, j)` as functions of `(a, b)`. But T10a.6's own Formal Contract lists only `dom(X) ∩ dom(Y) = ∅` as postcondition — the corollary is not exported, so downstream consumers cannot cite it.
**Required**: Add the witness-uniqueness corollary to the Postcondition field, e.g.: "`dom(X) ∩ dom(Y) = ∅`; equivalently, for every `a` there is at most one `A ∈ 𝒯` with `a ∈ dom(A)`, so `same_allocator(a, b)` determines the witnessing `A` uniquely."

VERDICT: REVISE

### AllocatedSet

#### State definition and activation predicate are mutually circular
**Class**: REVISE
**Issue**: The state definition says "`s ∈ 𝒮` is the configuration of the allocator tree: which allocators have been activated and, for each allocator A, the count `nₛ(A) ≥ 0`", so activation is a *component* of the state — effectively a projection `s ↦ {A : activated in s}`. But the Activation predicate section then defines `activated : 𝒯 × 𝒮 → {⊤, ⊥}` "by induction on the reachable-state graph rooted at s₀", as if it were an auxiliary property computed from the transition history. Either the state encodes activation (and the "inductive definition" is really a consistency constraint on Σ that transitions must satisfy) or activation is derived inductively from transitions (and the state must *not* pre-declare it). The claim conflates both framings, leaving the primary object undefined.
**Required**: Pick one framing. Either (a) make activation a projection of the state and rephrase the "inductive definition" as admissibility constraints on Σ's transitions (each `op ∈ Σ` must preserve/extend activation exactly per the base and transition clauses); or (b) define state as just `{nₛ(A) : A ∈ 𝒯}` without activation, and derive `activated(A, s)` as a predicate, showing it is a well-defined function of `s` alone.

#### Path-independence of the activation induction is asserted without proof
**Class**: REVISE
**Issue**: The claim states "on every s reachable from s₀ the set `{A ∈ 𝒯 : activated(A, s)}` is determined by induction on **any** transition path from s₀". If a single state s is reachable via two distinct transition paths `π₁` and `π₂`, the inductive construction must assign the same activation set along both. Persistence (α) plus no-spontaneous-activation (β) imply monotone growth along each path, but do not by themselves force the two paths' activation sets to coincide at a shared endpoint. The state-level count `nₛ(A)` also reappears at s regardless of path, but the claim never connects the count-reappearance fact to path-equivalence of activation.
**Required**: Either establish path-independence explicitly (e.g., `activated(A, s)` iff some prefix of any reaching path spawns A, and show equivalence across paths), or — under framing (a) above — drop the inductive construction and state that Σ is defined so that `activated(A, s)` is a function of s determined by the state's activation component, with the base/transition clauses imposed as transition admissibility.

#### Frame condition on non-allocating transitions absent from Formal Contract
**Class**: REVISE
**Issue**: The narrative says "Non-allocating transitions leave every realized domain unchanged", which is a frame claim used implicitly when arguing `allocated` evolves only via the two listed allocation-affecting shapes. The Formal Contract lists only Definitions, Postconditions, and Depends — it contains no Frame or Invariant field capturing this guarantee. Downstream consumers that rely on "`domₛ(A)` stable across non-allocating transitions" have no contractual handle.
**Required**: Add a Frame (or Invariant) item to the Formal Contract, e.g., "*Frame:* for every non-allocation-affecting transition s → s' and every A ∈ 𝒯, `domₛ(A) = domₛ'(A)` and `activated(A, s) ≡ activated(A, s')`; thus `allocated(s) = allocated(s')`."

#### "parent(A)'s current frontier" invokes a notion not defined in T10a
**Class**: REVISE
**Issue**: The "s → s' spawns A" clause says the transition "applies `inc(spawnPt(A), spawnParam(A))` to parent(A)'s current frontier, producing A's base address". T10a only requires `spawnPt(A) ∈ dom(parent(A))` — it does not require that `spawnPt(A)` be the *frontier* (i.e., the last-produced sibling `t_{nₛ(parent(A))}`) at the moment of the spawning transition. Without that admissibility condition, the clause "applied to parent(A)'s current frontier" is ill-defined: inc is applied to `spawnPt(A)` specifically, not to an arbitrary frontier. If the author intends that A can only be spawned when parent(A)'s chain has advanced to `spawnPt(A)`, that should be the admissibility precondition and be stated formally, not described by the slogan "current frontier".
**Required**: State the admissibility condition directly in the transition-clause definition: "s → s' spawns A" iff the transition applies `inc(spawnPt(A), spawnParam(A))` in state s where `spawnPt(A) = t_{nₛ(parent(A))}` (the last realized sibling of parent(A) in s), producing A's base as the first element of `dom(A)`. Either remove the "frontier" language or formalize it.

#### `nₛ(A)` is referenced for non-activated allocators but left undefined
**Class**: REVISE
**Issue**: The Formal Contract writes "*Realized domain:* `domₛ(A) = {t₀, …, t_{nₛ(A)}}` where `tᵢ₊₁ = inc(tᵢ, 0)`" for every `A ∈ 𝒯`, but `nₛ(A)` is introduced as "the count of sibling increments performed" — which is only meaningful when A is activated. For non-activated A the value is implicitly 0 (per the narrative's implicit convention) or undefined. The narrative filters by `activated(A, s)` when unioning, so the issue is harmless in `allocated(s)`, but `domₛ(A)` for non-activated A is exported as an object in the contract without a stated value.
**Required**: Either restrict the Realized domain definition to activated A (i.e., `domₛ(A)` is defined only when `activated(A, s)`), or set `domₛ(A) = ∅` for non-activated A and state that explicitly.

### TumblerSub

#### Gap from `rₖ ≥ 1` to `rₖ ≠ 0` is unjustified
**Class**: REVISE
**Issue**: The Pos(a ⊖ w) argument states: "rₖ = aₖ − wₖ ≥ 1 by NAT-sub (strict positivity) ... The result is not the zero tumbler, whence Pos(a ⊖ w) (TA-Pos)." TA-Pos requires exhibiting an index i with `¬(rᵢ = 0)`, not an index with `rᵢ ≥ 1`. The inferential step `rₖ ≥ 1 ⟹ rₖ ≠ 0` is skipped. Unfolding `1 ≤ rₖ` via NAT-order's `≤`-defining clause yields `1 < rₖ ∨ 1 = rₖ`; substituting `rₖ = 0` produces `1 < 0 ∨ 1 = 0`, of which NAT-zero's consequence only excludes the first disjunct. The stated dependencies do not axiomatize `1 ≠ 0`, so the bridge must be argued from first principles rather than left implicit.
**Required**: Supply the missing step. A clean route: NAT-sub right-inverse gives `(aₖ − wₖ) + wₖ = aₖ` from `aₖ ≥ wₖ`; supposing `rₖ = aₖ − wₖ = 0`, NAT-closure's left-identity `0 + wₖ = wₖ` rewrites the sum to `wₖ = aₖ`, contradicting `aₖ > wₖ` via NAT-order disjointness. Then the exhibited `rₖ ≠ 0` discharges TA-Pos. Add NAT-closure's left-identity and the right-inverse clause of NAT-sub to the cited uses if not already covered.

### D1

#### TumblerSub precondition b ≥ a silently discharged
**Class**: REVISE
**Issue**: The proof writes "Define w = b ⊖ a" and immediately invokes TumblerSub's component formulas and postconditions, but never discharges TumblerSub's precondition `a ≥ w` (in its notation) — i.e., `b ≥ a` in D1's notation. The derivation is short (a < b unfolds T1's abbreviation `a ≤ b ≡ a < b ∨ a = b`, so a ≤ b, hence b ≥ a) but the proof elsewhere discharges comparably short inferences explicitly (e.g. "bₖ ≥ aₖ via NAT-order from bₖ > aₖ", "Since k ≤ #a, TA0's precondition is satisfied"). Leaving this one silent is inconsistent with the proof's own rigor standard and hides a precondition a downstream consumer must verify. The Depends entry for T1 mentions only "derives aₖ < bₖ from a < b" and the TumblerSub entry does not acknowledge this precondition discharge.
**Required**: Add an explicit sentence deriving b ≥ a from the precondition a < b (via T1's ≥ abbreviation), and update T1's Depends note to list this additional use.

### T6

#### NAT-card used but not declared in Depends
**Class**: REVISE
**Issue**: Ingredient 2 explicitly states "Let `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` as in T4 (with `|·|` the cardinality of a finite subset of ℕ, distinct from T0's tumbler-length `#·`), computable by one scan." This directly invokes NAT-card's axiomatization of `|·|` as a cardinality operator with codomain ℕ, and the postcondition formulas use `zeros(t) ≥ 1`, `zeros(t) ≥ 2`, `zeros(t) = 3` as comparisons in ℕ that require `zeros(t) ∈ ℕ` — a typing fact NAT-card supplies. T4a and T4b both re-declare NAT-card when inheriting zeros from T4; T6 follows the same reliance but omits the declaration.
**Required**: Add `NAT-card (NatFiniteSetCardinality, this ASN)` to the Depends list, explaining that it grounds `|·|` and the typing `zeros(t) ∈ ℕ` that underwrites the threshold comparisons in Ingredient 2 and in postconditions (b)–(d).

### T7

#### T0 miscited as source of strict positivity
**Class**: REVISE
**Issue**: The proof asserts "By T0, every component lies in ℕ, so every non-separator component is strictly positive" and, later, "at j, one tumbler has 0 and the other has a non-separator component, strictly positive by T0 and T4's role-assignment." The depends entry also declares "T0 (CarrierSetDefinition) — components lie in ℕ; supplies strict positivity of non-separator components." T0's Axiom only fixes the carrier as ℕ and gives component projection/length; it does not supply strict positivity of non-zero ℕ-elements. Moving from "n ∈ ℕ ∧ n ≠ 0" to "0 < n" needs NAT-zero's disjunction `0 < n ∨ 0 = n` (combined with n ≠ 0) or NAT-discrete at m=0 — neither is declared. T4's Axiom does supply `0 < N_i, 0 < U_j, 0 < D_k, 0 < E_l` at non-separator positions, so the strict-positivity fact is available via T4; but the proof's citation routes it through T0, which cannot carry it.
**Required**: Replace the "By T0 ... strictly positive" phrasing with a citation of T4's Axiom (its 0 < N_i/U_j/D_k/E_l clauses at non-separator positions), or add NAT-zero (or NAT-discrete) as a direct dependency and justify strict positivity as "n ∈ ℕ ∧ n ≠ 0 ⟹ 0 < n" via NAT-zero's disjunction. Correct the T0 depends entry to remove the strict-positivity role attribution, leaving only ℕ-typing of components.

#### NAT-order missing as direct dependency
**Class**: REVISE
**Issue**: The proof relies pervasively on the `<`/`≤`/`≥` relations on ℕ — `α, β, γ, δ ≥ 1`, the ascending-order pairing of separator-position sets (requiring the sets' canonical sorted enumerations), and `p_a ≠ p_b` comparisons. T4, T4a, T4b all declare NAT-order directly when they use these relations, following the ASN's precedent of naming direct suppliers rather than relying on transitive carriage. T7 uses these relations in its own proof text — it does not merely cite a postcondition in which they already appear — yet NAT-order is not in the Depends list.
**Required**: Add NAT-order (NatStrictTotalOrder) to the Depends list, with a one-line role describing its use: supplying `<`/`≤` on ℕ for the zero-count bound, the ascending pairwise matching of separator-position sets, and the `≥ 1` field-length inequalities locally unpacked from T4a's conclusion.

#### NAT-closure missing as direct dependency
**Class**: REVISE
**Issue**: The proof uses the numerals `1`, `2`, `3`, `4` as ℕ-elements (`α, β, γ, δ ≥ 1`; separator positions `α + 1`, `α + β + 2`, `α + β + γ + 3`; first element-field position `α + β + γ + 4`) and repeatedly invokes additive closure on ℕ to form these sums. NAT-closure grounds `1 ∈ ℕ`, `2 := 1 + 1`, `3 := 2 + 1`, `4 := 3 + 1`, and the closure of `+` on ℕ needed to type-check each of these sums. T4, T4a, T4b each declare NAT-closure directly when using these numerals. T7 makes the same use without declaring it.
**Required**: Add NAT-closure (NatArithmeticClosureAndIdentity) to the Depends list, role: grounds the numerals 2, 3, 4 in ℕ and closes ℕ under addition so that the separator-position expressions `α + 1`, `α + β + 2`, `α + β + γ + 3` and the element-field position `α + β + γ + 4` are typed within ℕ.

### TA-PosDom

#### Silent precondition: `1 ≤ k` for T1 case (ii) witness `#z + 1`
**Class**: REVISE
**Issue**: T1's definitional schema requires the existential witness `k` to satisfy `1 ≤ k` at the top level, in addition to the case-specific clause `k = m + 1 ≤ n`. In Case `#z < k`, the proof exhibits witness `#z + 1` and discharges the case-(ii) clause via NAT-discrete (`#z + 1 ≤ #t`), but never discharges `1 ≤ #z + 1`. This is not automatic from the declared dependencies: deriving `1 ≤ #z + 1` from `1 ≤ #z` (T0) requires `#z ≤ #z + 1`, which needs NAT-addcompat's `n < n + 1` (with NAT-order's `≤`-defn) — NAT-addcompat is not in the Depends list.
**Required**: Either (a) add NAT-addcompat to the Depends and insert a line in Case `#z < k` deriving `1 ≤ #z + 1` from T0's `1 ≤ #z` via NAT-addcompat's `#z < #z + 1` and NAT-order transitivity; or (b) discharge `1 ≤ #z + 1` by another route and cite the axiom used.

### TA3

#### Missing TumblerSub precondition-consequence in dependency description
**Class**: REVISE
**Issue**: The proof repeatedly invokes the fact that when `zpd(a, w)` is defined, `a_{dₐ} > w_{dₐ}` follows from the precondition `a ≥ w`. This is used at least three times:
(1) In the preamble to sub-cases B2–B4: *"if b were zero-padded-equal to w, then at dₐ, `a_{dₐ} > w_{dₐ} = b_{dₐ}`"* — the strict `a_{dₐ} > w_{dₐ}` is unjustified without citing TumblerSub's precondition consequence.
(2) In Sub-case B3: *"a ≥ w requires `a_{dₐ} ≥ w_{dₐ}` — contradiction."* Lexicographic `≥` on tumblers does not give component-wise inequality in general; the step is sound only via TumblerSub's consequence "zpd defined ⟹ `a_k > w_k`."
(3) In Sub-case B4: *"since b ≥ w forces `b_{d_b} > w_{d_b}`"* — again the strict inequality comes from TumblerSub's precondition consequence applied to `(b, w)`.
The TumblerSub entry in Depends only credits *"zero-padding, three-phase formula, length-pair dispatch naming L_{x,w}"* and omits this precondition consequence. It also omits the postcondition `Pos(a ⊖ w)` when `zpd` is defined, which the proof uses in A1, A3, and B1 to conclude `b ⊖ w` is positive.
**Required**: Extend the TumblerSub dependency bullet to enumerate the precondition consequence (`zpd(x, w)` defined under `x ≥ w` ⟹ `x_{zpd(x,w)} > w_{zpd(x,w)}`) and the conditional postcondition `Pos(x ⊖ w)` when `zpd(x, w)` is defined; and replace the imprecise "a ≥ w requires `a_{dₐ} ≥ w_{dₐ}`" / "b ≥ w forces `b_{d_b} > w_{d_b}`" wording with explicit citations of that consequence.

### TA7a

#### Title/Narrative vs Actual Theorem Mismatch
**Class**: REVISE
**Issue**: The claim is labeled `SubspaceClosure` and opens with "the result must remain in that subspace ... Text positions must not cross into link space." But the two quantified statements only conclude `o ⊕ w ∈ T` and `o ⊖ w ∈ T`, not `∈ S`. The proof itself exhibits counterexamples where the result exits S: "Counterexample: `[5, 3] ⊖ [5, 1] = [0, 2] ∈ T, ∉ S ∪ Z`", and the `#w > m` preliminary also produces results "in T \ S". A consumer citing TA7a for "subspace closure" will find only `T`-closure plus conditional S-postconditions scattered through the contract. Either the name/framing or the top-level formal statement is wrong.
**Required**: Reconcile the discrepancy. Either (a) rename the claim and rewrite the opening paragraph to describe what is actually proved (T-closure with refined S/Z-residency per case), or (b) strengthen the top-level conjuncts to a genuine S-closure statement under tighter preconditions (e.g., enforce tail-positivity of `w` for ⊕ and rule out the `k = 1, d > 1` and `#w > m` cases for ⊖), and relocate the T-only residues to explicit sub-claims.

#### ⊖ precondition admits non-element-local displacements
**Class**: REVISE
**Issue**: The prose constrains element-local displacements by `1 ≤ k ≤ m`, but the ⊖ conjunct reads `(A o ∈ S, Pos(w) : o ≥ w ⟹ o ⊖ w ∈ T)` — no `k ≤ m` bound. With `o ∈ S` and `w` having `k = actionPoint(w) > m`, we have `wᵢ = 0` for `1 ≤ i ≤ m` (ActionPoint), so `o > w` via T1 at position 1, i.e., `o ≥ w` is satisfied. The conjunct therefore quantifies over displacements that violate the stated "element-local" restriction. The closing prose ("The restriction to element-local displacements is necessary …") asserts a restriction the conjunct does not enforce.
**Required**: Add `actionPoint(w) ≤ #o` to the ⊖ conjunct's preconditions (matching the ⊕ conjunct), or drop the element-local framing and justify the stronger quantification.

## OBSERVE

### NAT-order

#### Disjointness axiom is derivable from irreflexivity
**Class**: OBSERVE
**Issue**: The disjointness axiom `(A m, n ∈ ℕ : m < n : m ≠ n)` is derivable from irreflexivity under standard first-order logic with equality (Leibniz substitution): if `m < n` and `m = n`, substituting gives `m < m`, contradicting irreflexivity. Listing it as a separate axiom rather than a derived fact is non-minimal. This does not affect soundness — the explicit axiom may be preferred for clarity of the exactly-one derivation, which uses disjointness directly without invoking equality substitution. A reader tracking primitive vs. derived commitments may want a note marking the choice.

VERDICT: OBSERVE

### NAT-closure

#### Variable shadowing in successor-closure instantiation
**Class**: OBSERVE
**Issue**: The phrase "instance of the codomain commitment at `(m, n) := (n, 1)`" reuses `n` as both a formal parameter on the left and a free variable on the right of the substitution. The signature `+ : ℕ × ℕ → ℕ` was not presented with named parameters, so introducing `(m, n)` here and then shadowing `n` in the same assignment is momentarily confusing. The mathematical content is correct — the reader recovers the intent — but a reader checking the substitution mechanically has to pause.

VERDICT: OBSERVE

### TA-Pos

#### Non-standard formal contract field label
**Class**: OBSERVE
**Issue**: The formal contract uses `*Complementarity:*` as a field label for the derived statement `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`. This statement is proved from the Definition via classical DeMorgan duality, not posited — it is a derived fact. The established convention in the dependencies (NAT-zero exports `¬(n < 0)` under `*Consequence:*`; NAT-order exports exactly-one trichotomy under `*Consequence:*`) uses the `Consequence` label for exactly this kind of lifted-from-axiom statement. Using a bespoke `Complementarity` label departs from that convention and from the review-checklist field inventory (Preconditions, Postconditions, Invariant, Frame, Axiom, Definition; Consequence is the precedent for derived exports). Downstream consumers citing "the Consequence of TA-Pos" will not find a Consequence field. Soundness is not affected; the derived equivalence is correctly stated and its proof (DeMorgan + classical double-negation) is valid.

VERDICT: OBSERVE

### ActionPoint

#### Brief contradiction in the "wᵢ = 0 for 1 ≤ i < actionPoint(w)" step
**Class**: OBSERVE
**Issue**: The derivation concludes "i would be a member of S with i < actionPoint(w), contradicting (A n ∈ S :: actionPoint(w) ≤ n)" without explicitly discharging how `actionPoint(w) ≤ i` combined with `i < actionPoint(w)` yields a contradiction. The reader must replay the same ≤-unfolding + irreflexivity/transitivity machinery that was just worked out for uniqueness. Since the technique was spelled out immediately above, reusing it by reference is reasonable but the step is strictly briefer than the rest of the derivation.

#### Implicit typing steps
**Class**: OBSERVE
**Issue**: Two small typing steps are implicit rather than cited: (a) for `i` in `1 ≤ i < actionPoint(w)`, membership in S requires `i ≤ #w`, which follows by chaining `i < actionPoint(w) ≤ #w` but is not spelled out; (b) instantiating NAT-zero's axiom and NAT-discrete at `n = w_{actionPoint(w)}` requires `w_{actionPoint(w)} ∈ ℕ`, which follows from T0's clause `aᵢ ∈ ℕ at each i ∈ {1, …, #a}` but is not explicitly invoked. T0 is already declared so no dependency is missing; the derivation simply elides the typing witnesses.

VERDICT: OBSERVE

### T0(a)

#### Strict-inequality symbol `>` in postcondition is not directly grounded by a declared dependency
**Class**: OBSERVE
**Issue**: The postcondition and proof step (iii) both use `>` (in `t'.dᵢ > M` and `M + 1 > M`), but none of the three declared dependencies supplies the symbol `>` explicitly. NAT-addcompat gives the strict successor inequality as `n < n + 1`, i.e. `M < M + 1`. The proof tacitly converts this to `M + 1 > M`, relying on the universal convention that `>` is the converse of `<` (the latter supplied by NAT-order, itself reached only transitively through NAT-addcompat). A reader following the dependency chain strictly has to import the `>`-as-converse convention on faith. The claim is sound as written — this is a notational grounding observation, not a correctness defect.

VERDICT: OBSERVE

### NAT-card

#### T0 dependency used only for disambiguation remark
**Class**: OBSERVE
**Issue**: T0 is declared in Depends but is invoked only by the trailing disambiguation sentence "The operator `|·|` is distinct from T0's tumbler-length `#· : T → ℕ`, which acts on sequences." The axiom body, formal contract clauses (`|S| ∈ ℕ`, enumeration characterisation, upper bound), and their groundings all close under NAT-order, NAT-closure, and NAT-zero alone. Structurally this makes a NAT-layer axiom cite a T0-layer axiom to support a footnote, reversing the normal layering (T0 itself cites NAT-order and NAT-closure, so there is no circularity, but the coupling is unusual).

#### Construction of initial segment `{1, 2, …, n}` at n = 0
**Class**: OBSERVE
**Issue**: The axiom universally quantifies `n ∈ ℕ`, and NAT-zero forces `0 ∈ ℕ`, so `n = 0` is in scope. The notation `{1, 2, …, n}` is not defined for `n = 0` by the claim; the body only says the segment is "built from the `1 ∈ ℕ` posited by NAT-closure and the successor operation closed over ℕ by NAT-closure," which suggests a construction that starts at `1` and cannot terminate below `1`. A reader has to supply the convention `{1, …, 0} = ∅` (under which `S = ∅`, the empty enumeration applies, and `|∅| = 0 ≤ 0`) to close the case. Making `{1, …, n}` the bounded comprehension `{m ∈ ℕ : 1 ≤ m ≤ n}` (well-typed from NAT-order's `≤` and NAT-closure's `1 ∈ ℕ`) would fix the meaning uniformly across `n ∈ ℕ` including `n = 0`.

#### Well-formedness of "strictly increasing enumeration" over-attributed to the total-order discipline
**Class**: OBSERVE
**Issue**: The narrative states that "NAT-order's strict-total-order discipline (irreflexivity, transitivity, trichotomy `m < n ∨ m = n ∨ n < m`) is what makes 'strictly increasing enumeration' a well-formed predicate on ℕ-indexed sequences." Well-formedness of the predicate `s₁ < s₂ < … < s_k` only requires NAT-order's first clause `< ⊆ ℕ × ℕ` (so `sᵢ < sᵢ₊₁` is a well-typed atomic formula). Irreflexivity, transitivity, and trichotomy are properties that give the predicate its intended strength — e.g. trichotomy is what lets one read "strictly increasing" as excluding equality — not what makes it well-formed. The claim itself then correctly notes these properties are not appealed to in deriving uniqueness of `k` or the upper bound, so the attribution in the body is slightly overstated relative to what is actually used.

#### Successor phrased as a separate operation rather than an instance of `+`
**Class**: OBSERVE
**Issue**: The body refers to "the successor operation closed over ℕ by NAT-closure," but NAT-closure's contract exports `+ : ℕ × ℕ → ℕ` and `1 ∈ ℕ` (successor is the codomain commitment instantiated at `(n, 1)`, as NAT-closure's own narrative states). Calling it "the successor operation" as though it were a separately posited primitive is loose. If the initial segment is instead read as `{m ∈ ℕ : 1 ≤ m ≤ n}`, no successor construction is needed and the phrasing can be dropped entirely.

VERDICT: OBSERVE

### T4

#### Notational clash: `k` used for both zero count and D-field subscript
**Class**: OBSERVE
**Issue**: The Axiom schema opens with "for each `k ∈ ℕ` with `0 ≤ k ≤ 3` at which `zeros(t) = k`" and then closes with "In every case, `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` at every position present." The `k` in `Dₖ` is a meta-index ranging over positions within the D-field, while the outer `k` ranges over `{0,1,2,3}` as the zero count. Same collision appears in the body paragraph introducing the maximal form. Readable from context, but the free-variable reuse is awkward in an axiom meant to be cited verbatim.

#### Left-identity step elided in first NAT-discrete application
**Class**: OBSERVE
**Issue**: The Exhaustion argument at `m = 0` says "`0 < zeros(t)`, which NAT-discrete promotes to `1 ≤ zeros(t)`." NAT-discrete at `(m, n) := (0, zeros(t))` actually yields `0 + 1 ≤ zeros(t)`; bridging to `1 ≤ zeros(t)` requires `0 + 1 = 1`, i.e., NAT-closure's left-identity `0 + n = n` at `n := 1`. For the later steps, numeral abbreviations `2 := 1 + 1` and `3 := 2 + 1` are stated explicitly, but no analogous bridge is stated at `m = 0`. The NAT-closure dependency justification likewise mentions only the numerals 2 and 3 — not the left-identity clause used at the base step.

#### "k+1 field segments" count stated without derivation
**Class**: OBSERVE
**Issue**: The body prose asserts that the field segments are "`k+1` of them when `zeros(t) = k`, separated by the zeros" without a derivation. The count follows from the four axiom clauses (no-adjacent-zeros plus non-zero first/last forces each zero to sit between two non-empty runs), but the argument is implicit here. Not load-bearing on T4's own Consequence — T4a is cited as handling segment non-emptiness — so this is motivation-level prose rather than a gap in the formal contract.

VERDICT: OBSERVE

### Prefix

#### Quantifier typing inconsistency within the contract
**Class**: OBSERVE
**Issue**: The reflexivity postcondition is written with explicit typing — `(∀t ∈ T :: t ≼ t)` — but the proper-prefix length postcondition is stated schematically as `p ≺ q ⟹ #p < #q` with no outer `(∀ p, q ∈ T :: …)` binder. The intended reading is clearly "for all `p, q ∈ T`", but two peer postconditions in the same Formal Contract use different binding conventions.

#### Quantifier symbol diverges from dependency register
**Class**: OBSERVE
**Issue**: The Definition writes `(∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)` using `∀`, whereas T0, T3, and NAT-order (and T0's note on bounded quantifiers of the form `(Q i : 1 ≤ i ≤ #a : …)`) all use `A` as the universal quantifier marker. Soundness is unaffected, but the symbol choice is inconsistent with the surrounding register.

#### "Requires" softens a definitional biconditional
**Class**: OBSERVE
**Issue**: The narrative reads "A proper prefix `p ≺ q` *requires* `p ≼ q` with `p ≠ q`", which reads as a necessary condition rather than a definition. The Formal Contract's Definition slot correctly gives the biconditional (`iff`), so soundness is intact — the phrasing in the prose is just weaker than the formal clause it is meant to summarize.

#### Symmetry of equality used silently when invoking T3
**Class**: OBSERVE
**Issue**: The proper-prefix-length derivation applies T3 to conclude `p = q` from `#p = #q` plus the prefix condition `(∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. T3's postcondition is stated with orientation `aᵢ = bᵢ` (instantiating `a = p`, `b = q` yields `pᵢ = qᵢ`), so the step implicitly appeals to symmetry of `=`. Trivially valid, but the orientation flip is not acknowledged.

VERDICT: OBSERVE

### NAT-sub

#### "Left-inverse characterisation" label is imprecise
**Class**: OBSERVE
**Issue**: Both `(m − n) + n = m` and `n + (m − n) = m` are right-inverse equations (each asserts that the result of adding `n` — on some side — to `m − n` recovers `m`). Calling the second form "left-inverse characterisation" conflates the syntactic position of the summand with an inverse direction. In group-theoretic terminology, both exhibit `m − n` as an inverse of the translation-by-`n` map; the distinction is which side the `n` is written on.
**Required**: (omit)

VERDICT: REVISE

### T4a

#### NAT-discrete usage scope in Depends rationale
**Class**: OBSERVE
**Issue**: The NAT-discrete Depends note restricts its usage to "the Reverse derivations" and enumerates three specific +1-promotions there. But the Forward direction for Condition (i) also implicitly relies on NAT-discrete: the step "Then i and i + 1 are consecutive zero positions — say s_j = i and s_{j+1} = i + 1" depends on the fact that no zero position lies strictly between i and i+1, which in turn rests on NAT-discrete's "no natural strictly between n and n+1" content (formally: if s_m is a zero position with s_j < s_m ≤ s_j + 1 = i + 1, then s_m = s_j + 1 by NAT-discrete's equivalent form `m ≤ n < m + 1 ⟹ n = m`). The dependency itself is declared, so the claim remains grounded; only the "in the Reverse derivations" scope statement is narrower than the actual usage footprint.

VERDICT: OBSERVE

### NAT-cancel

#### Loose attribution in mirror-form derivation
**Class**: OBSERVE
**Issue**: The claim states the mirror form `n + m = m ⟹ n = 0` "is a theorem of the three clauses above together with NAT-closure." The derivation shown only uses right cancellation (one clause) plus NAT-closure's left identity — left cancellation and absorption play no role. The statement is technically correct (a weaker provenance than needed) but imprecise about which axioms are actually invoked.

VERDICT: OBSERVE

### T1

#### Informal use of `>` without abbreviation in formal contract
**Class**: OBSERVE
**Issue**: Case 1 of part (b) writes "Part (a) gives ¬(a < a) and ¬(a > a)" but the Formal Contract's Abbreviations list only defines `≤` (as `< ∨ =`) and `≥` (as converse of `≤`); `>` on T is not introduced. A careful reader parses `a > a` as shorthand for the reverse-direction collapse `b < a` under `a = b`, which reduces to `a < a` and is thereby covered by irreflexivity, but the symbol itself is technically ungrounded in the listed abbreviations. Soundness is unaffected: the substitution is transparent, and the three mutual-exclusion clauses of trichotomy all reduce to `¬(a < a)` under `a = b`.

VERDICT: OBSERVE

### TA5a

#### Case k=0 "No new adjacencies arise" is under-justified
**Class**: OBSERVE
**Issue**: The single sentence "No new adjacencies arise" dispatches T4(ii) for case k=0. The supporting reasoning — that the zero-index set of t' equals that of t (sig(t) is not a zero position in either, and all other positions are unchanged by TA5(b)), so every adjacency pattern in t' matches one in t where T4(ii) already forbids them — is already assembled in the preceding sentence's zero-set equality argument, but the connection is not drawn.
**Required**: omit for OBSERVE.

VERDICT: REVISE

### T10

#### Unused minimality clause
**Class**: OBSERVE
**Issue**: The proof establishes "`p₁ᵢ = p₂ᵢ` for `1 ≤ i < k`" alongside `p₁ₖ ≠ p₂ₖ`, but the `< k` minimality clause is never used in the subsequent steps. Only `p₁ₖ ≠ p₂ₖ` and `k ≤ ℓ ≤ min(m, n)` are cited to derive `aₖ ≠ bₖ`. The min-witness could equally well be picked as any `j ∈ {j : 1 ≤ j ≤ ℓ ∧ p₁ⱼ ≠ p₂ⱼ}`; well-ordering gives minimality "for free" but the narrative suggests it carries proof weight it does not.

#### "Reverse direction of T3" framing
**Class**: OBSERVE
**Issue**: The proof concludes "By the reverse direction of T3, `a ≠ b`." What is actually invoked is the *contrapositive* of the reverse direction: T3's reverse states `a = b ⟹ (#a = #b ∧ (∀i) aᵢ = bᵢ)`, so component disagreement at a valid index (here `k ≤ min(#a, #b)`, which holds since `k ≤ ℓ ≤ min(m, n) ≤ min(#a, #b)`) forces `a ≠ b`. The reasoning is sound, but the reference collapses a contrapositive step that a strict reader would write explicitly.

VERDICT: OBSERVE

### T10a.7

#### "Equivalently" in the postcondition conflates injectivity with strict monotonicity
**Class**: OBSERVE
**Issue**: The postcondition states the injectivity form, then says "Equivalently, `(A m, n ≥ 0 : m < n : tₘ < tₙ)`." In general, injectivity and strict monotonicity are not equivalent — strict monotonicity is strictly stronger. They coincide here only because TA5(a) guarantees consecutive-step monotonicity, which is context the word "Equivalently" silently assumes. The proof in fact establishes the stronger monotonicity form and then derives injectivity; the contract could more accurately say "the proof establishes the stronger strict-monotone form `m < n ⟹ tₘ < tₙ`, which with T1(a) implies injectivity."

VERDICT: REVISE

### T10a.3

#### Additive-nesting induction gestured, not carried out
**Class**: OBSERVE
**Issue**: "By induction on `d`, the descendant at depth `d` has sibling length `γ + k'₁ + … + k'_d`" — no base case or step is supplied, only the single-step parent→child case is shown in the preceding paragraph. Given that is precisely the inductive step and T10a.1 carries uniformity within each level, the claim is sound, but the proof would read more cleanly if the base (`d = 0`: root siblings have length `γ`) and step (IH at depth `i` plus the already-proved single-step result) were written explicitly.

#### "Outputs at different depths never collide" reads unrestricted
**Class**: OBSERVE
**Issue**: The postcondition sentence "cumulative length is strictly increasing with depth, so outputs at different depths never collide" sits immediately after the lineage-parametrised length formula, so the intended reading is within-lineage. A cross-lineage reading is false (two siblings' `k' = 1` children both have length `γ + 1`). A short qualifier ("along the lineage") would close the ambiguity.

VERDICT: REVISE

### T9

#### Proof redundantly re-proves T10a.7's postcondition
**Class**: OBSERVE
**Issue**: T10a.7's Formal Contract states its postcondition as "The map `n ↦ tₙ` is injective: `(A m, n ≥ 0 : m ≠ n : tₘ ≠ tₙ)`. Equivalently, `(A m, n ≥ 0 : m < n : tₘ < tₙ)`." The proof of T9 re-derives exactly this equivalent form by induction on `d = j − i` using TA5(a) for the base/step and T1(c) for transitivity — which is verbatim T10a.7's own proof. Given T10a.7 is already declared as a dependency, T9 reduces to: "Let `a = tᵢ`, `b = tⱼ` with `i < j` (indices well-defined by T10a.6, T10a.7). By T10a.7, `tᵢ < tⱼ`, i.e., `a < b`." The current induction duplicates work already done upstream. The claim is sound as written; this is a structural observation, not a correctness defect.

VERDICT: OBSERVE

### AllocatedSet

#### `op(s) defined` and `s ∈ dom(op)` duplication adds no content
**Class**: OBSERVE
**Issue**: Both the narrative and the Formal Contract's "Transition vocabulary" bullet repeat "The predicate `op(s) defined` abbreviates `s ∈ dom(op)`; when it holds, `op(s) ∈ 𝒮` is the unique successor state." The abbreviation is never used subsequently in the claim — "s → s'" is the relation actually employed. The `op(s) defined` notation is dead weight.

#### Reachable-state containment (iii) is trivially entailed by (i)
**Class**: OBSERVE
**Issue**: Postcondition (iii) states `dom(A) ⊇ ⋃{domₛ(A) : s reachable from s₀}`. This is an immediate corollary of (i) (since each `domₛ(A) ⊆ dom(A)`). Listing it as a distinct postcondition is defensible for highlighting the liveness-gap caveat, but a reader may expect (iii) to carry independent content. A one-line note that (iii) is the set-union form of (i) with the reverse inclusion left to a separate liveness ASN would make the structure explicit.

VERDICT: REVISE

### Divergence

#### T1 listed as dependency but not logically invoked
**Class**: OBSERVE
**Issue**: The Depends entry for T1 says "Divergence formalizes T1's 'first divergence position'; case (i) corresponds to T1 case (i) and case (ii) (with sub-cases (ii-a)/(ii-b)) corresponds to T1 case (ii)." This is motivational/structural parallelism, not a logical use. The reasoning establishes the definition, uniqueness, existence, exclusivity, exhaustiveness, and symmetry using T0, T3, NAT-order, NAT-wellorder, and NAT-closure — T1's postconditions (irreflexivity/trichotomy/transitivity of `<` on T) are never invoked. Divergence is a symmetric structural relation on sequences, not a consequence of the lex order; indeed, case (ii) here covers both length orderings whereas T1(ii) only captures one. The cross-reference is useful as reading guidance but is not a logical dependency.

#### Case (ii) preamble "if #a ≠ #b" is weaker than the sub-case hypotheses
**Class**: OBSERVE
**Issue**: In both the narrative and the Formal Contract's Definition, case (ii) opens with "if `#a ≠ #b`, NAT-order's trichotomy … leaves exactly one of `#a < #b` or `#b < #a`." The sub-cases (ii-a)/(ii-b) then silently conjoin the shared-position agreement `(A i : 1 ≤ i ≤ min(#a,#b) : aᵢ = bᵢ)` into their hypotheses. A strict reader might infer that `#a ≠ #b` alone suffices to enter case (ii), when in fact case (ii) fires only when lengths differ *and* shared positions agree (the remaining configuration — differing lengths with a shared mismatch — is handled by case (i), not a failed case (ii)). The definition is not wrong under charitable reading, but a cleaner opening such as "if `#a ≠ #b` and `(A i : 1 ≤ i ≤ min(#a,#b) : aᵢ = bᵢ)`" would prevent misreading.

#### "Unique least index" phrasing in postcondition is redundant
**Class**: OBSERVE
**Issue**: The postcondition states `divergence(a, b) = k` is "the unique least index satisfying `1 ≤ k ∧ k ≤ #a ∧ k ≤ #b ∧ aₖ ≠ bₖ ∧ (A i : 1 ≤ i < k : aᵢ = bᵢ)`." The conjunction includes prior agreement, which the uniqueness proof shows permits at most one `k`; "least" on a singleton is trivially satisfied. The load-bearing "leastness" property lives in the weaker set `S = {i : 1 ≤ i ≤ min(#a,#b) ∧ aᵢ ≠ bᵢ}` (via NAT-wellorder in the existence argument), not in the conjunction. Either phrasing ("unique index satisfying the full conjunction" or "least index in `S`") is clean; conjoining "unique least" is loose.

VERDICT: OBSERVE

### TumblerSub

#### Appeal to "T1 case (i)" in Divergence case (i) leaves witness identification implicit
**Class**: OBSERVE
**Issue**: In Divergence(w, a) case (i), the proof writes "Since `w < a` via T1 case (i), `wₖ < aₖ`." T1's definition asserts existence of *some* witness K for `w < a`; identifying K with the Divergence position k requires an argument (prefix agreement at positions `< k` means T1 case (ii) with K = #w+1 is incompatible with k ≤ #w at which w,a disagree, and T1's witness uniqueness from the trichotomy proof forces K = k). The conclusion is correct but the identification is not spelled out.

#### NAT-discrete is used directly, not only transitively
**Class**: OBSERVE
**Issue**: The Depends entry for NAT-discrete says "Required in scope for the consumed T1 and ActionPoint contracts." In fact, sub-case (ii-b)'s elimination relies on NAT-discrete *directly*: the hypothesis `#a < #w` must be lifted to `#a + 1 ≤ #w` to witness T1 case (ii). The declaration underreports the role — NAT-discrete is a direct use in this proof, not merely an in-scope transitive dependency.

VERDICT: REVISE

### TA2

#### Redundant proof reconstruction
**Class**: OBSERVE
**Issue**: TumblerSub's own narrative already establishes `a ⊖ w ∈ T` and `#(a ⊖ w) = L` — its body says verbatim: "Each component of the result is a natural number: for `i < k`, `rᵢ = 0 ∈ ℕ` by NAT-zero; at the divergence point, `rₖ = aₖ − wₖ ∈ ℕ` by NAT-sub, ... The length `L ≥ 1` since T0 gives `#a ≥ 1` and `#w ≥ 1` ... Hence `a ⊖ w ∈ T` by T0." And its postconditions export exactly `a ⊖ w ∈ T, #(a ⊖ w) = L`. TA2's proof retraces every one of these steps (no-divergence zero tumbler, pre-divergence zeros, divergence point via T1 case split, tail typing) rather than citing TumblerSub's postcondition. Soundness is not affected — TA2 is a correct weaker re-export — but the proof could collapse to a one-line citation of TumblerSub's postcondition together with the T1-derived inequality, and the current duplication invites drift if TumblerSub's body is later tightened without touching TA2.

#### NAT-zero cited via "0 ≤ aₖ" phrasing
**Class**: OBSERVE
**Issue**: In sub-case (ii), the proof writes "From NAT-zero's `0 ≤ aₖ`..." but NAT-zero's axiom is stated as `0 < n ∨ 0 = n`; the `0 ≤ aₖ` form requires unfolding through NAT-order's `≤`-defining clause. The subsequent clause does invoke NAT-order to perform the unfolding, so the chain is sound, but attributing `0 ≤ aₖ` to NAT-zero alone is slightly loose — NAT-zero directly supplies `0 < aₖ ∨ 0 = aₖ`, from which excluding `aₖ = 0` yields `0 < aₖ` without any NAT-order step. The `≤` detour is avoidable.

VERDICT: OBSERVE

### D0

#### Component formula for i > k omits zero-padding qualifier
**Class**: OBSERVE
**Issue**: The proof states "wᵢ = 0 for i < k, wₖ = bₖ − aₖ, wᵢ = bᵢ for i > k" when reading off displacement components, but in sub-case (β) where #b < #a, positions #b+1 through L = #a lie beyond b's native length. TumblerSub assigns the zero-padded value (0) there, not bᵢ. The subsequent length-only argument ("TumblerSub extends the result with trailing zeros to length #a") handles sub-case (β) correctly via T3, so the conclusion is sound — but the component formula line itself is phrased as if both operands had native components at all L positions. TumblerSub's own write-up explicitly qualifies these as "zero-padded values throughout"; preserving that qualifier (or writing `ŵᵢ`, `b̂ᵢ` for padded projections) would avoid a reader inferring bᵢ past #b.

VERDICT: OBSERVE

### D1

#### Opaque "equality disjunct" remark in case-(ii) elimination
**Class**: OBSERVE
**Issue**: The closing sentence of the case-(ii) elimination — "The case-hypothesis #a ≠ #b excludes the equality disjunct" — does not cleanly slot into either sub-case elimination. Sub-case (ii-a) is ruled out by k = #a + 1 vs k ≤ #a alone, and sub-case (ii-b) is ruled out by #b < #a vs #a ≤ #b via trichotomy alone; neither uses any "equality disjunct" argument. The remark is either (a) a redundant note that Divergence's case (ii) already excludes #a = #b by its own hypothesis, or (b) a stray observation that #a ≤ #b combined with being in case (ii) implies #a < #b — a fact the elimination does not need. Either way, a reader pauses trying to locate what the sentence discharges. Logic is sound, but the phrasing invites confusion.

VERDICT: REVISE

### D2

#### Dead derivation of #w = #b
**Class**: OBSERVE
**Issue**: In Step 2, the line "TumblerAdd's result-length identity yields #w = #(a ⊕ w) = #b" derives a fact that is never used in the subsequent cancellation step. TA-LC's preconditions (Pos(w), actionPoint(w) ≤ #a, and a ⊕ w = a ⊕ (b ⊖ a)) do not require #w = #b as a separate input, and TumblerAdd already appears as a dependency for the parallel derivation for b ⊖ a. The line is harmless but adds reasoning overhead without load-bearing use.

#### Redundant re-derivation of Pos(b ⊖ a)
**Class**: OBSERVE
**Issue**: The step "By NAT-sub, (b ⊖ a)ₖ ∈ ℕ and (b ⊖ a)ₖ ≥ 1, so Pos(b ⊖ a)" re-derives a fact that TumblerSub's formal contract already supplies as a postcondition ("when zpd(a, w) is defined: Pos(a ⊖ w)"). Since the proof has already established that zpd(b, a) = k is defined (case (i)), Pos(b ⊖ a) follows by direct citation of TumblerSub, without needing NAT-sub's strict positivity inline. Not unsound, just belt-and-suspenders.

VERDICT: OBSERVE

### T10a.8

#### Loose citation in the strict-positivity chain
**Class**: OBSERVE
**Issue**: The step "NAT-addcompat gives `(tₙ)_{sig(tₙ)} < (tₙ)_{sig(tₙ)} + 1`; combined with NAT-zero, `(tₙ₊₁)_{sig(tₙ)} > 0`" is loosely cited. NAT-zero alone does not promote `n < n + 1` to `n + 1 > 0`; the conclusion needs transitivity of `<` (NAT-order) chained with the previously established `(tₙ)_{sig(tₙ)} ≥ 1 > 0`. A cleaner route is NAT-addcompat's left order-compatibility lifting `1 ≤ (tₙ)_{sig(tₙ)}` to `2 ≤ (tₙ)_{sig(tₙ)} + 1`, then NAT-discrete/NAT-zero to land at `> 0`. Soundness is unaffected since the prior `≥ 1` is already in hand, but the citation is misleading.

VERDICT: OBSERVE

### NoDeallocation

#### Axiom status versus AllocatedSet's transition characterization
**Class**: OBSERVE
**Issue**: AllocatedSet already states "each allocation-affecting transition either advances some allocator's frontier by one `inc(·, 0)` step ... or spawns a child allocator" and "non-allocating transitions leave every realized domain unchanged." Combined with the activation predicate's persistence clause ("activated(A, s) ⟹ activated(A, s')"), this entails `allocated(s) ⊆ allocated(op(s))` for every `op ∈ Σ`. So NoDeallocation, as written, is derivable from AllocatedSet rather than an independent axiom. Framing it as "accepted as an axiom" is defensible only if AllocatedSet's transition enumeration is read as descriptive (shape of known ops) rather than normative (closing Σ). A note clarifying which reading is intended — or rephrasing as a theorem with AllocatedSet supplying the cases — would sharpen the export.

VERDICT: OBSERVE

### OrdinalDisplacement

#### Irreflexivity-to-inequality step underspecified
**Class**: OBSERVE
**Issue**: The step "By NAT-order's irreflexivity, `n ≠ 0`" (from `0 < n`) is a correct inference but requires an implicit substitution-for-contradiction: assume `n = 0`, rewrite `0 < n` to `0 < 0` via indiscernibility of `=`, contradict `¬(0 < 0)`. NAT-order's disjointness axiom `(A m, n ∈ ℕ : m < n : m ≠ n)` — already available through the declared NAT-order dependency — would yield `0 ≠ n` directly from `0 < n` at `(m, n) := (0, n)` without the substitution detour. Dependent claims like ActionPoint spell such substitutions out explicitly; this claim condenses it into a one-line appeal. Sound as written, but tighter grounding is available.

#### Pos witness requires unremarked reflexivity of ≤
**Class**: OBSERVE
**Issue**: The inference "the m-th component is nonzero, whence Pos(δ(n, m)) by TA-Pos" instantiates TA-Pos's existential at `i = m`, which requires `1 ≤ m ≤ #δ(n, m)`. `1 ≤ m` is the precondition; `m ≤ #δ(n, m)` = `m ≤ m` uses reflexivity of `≤` (from NAT-order's `m ≤ n ⟺ m < n ∨ m = n` with the `m = n` disjunct at `m = m`). Not called out, and the quantifier-range check against `#δ(n,m) = m` is left implicit.

VERDICT: OBSERVE

### T5

#### Elided unfolding of `a ≤ b` and `b ≤ c` in subcases
**Class**: OBSERVE
**Issue**: In subcases 1a and 1b, the proof concludes "b < a... contradicts a ≤ b" and "c < b... contradicts b ≤ c" without unfolding `≤`. The full step requires expanding `a ≤ b` as `a < b ∨ a = b` (T1 abbreviation), then in the `a < b` branch invoking T1 trichotomy's disjointness `¬(a < b ∧ b < a)`, and in the `a = b` branch deriving `bₖ = aₖ = pₖ` against `bₖ < pₖ` (NAT-order irreflexivity, or T3). The reasoning is sound and the dependencies (T1 trichotomy postcondition is part of the cited T1 ASN; NAT-order is listed) cover it, but spelling out the case-split would match the granularity of T1's own proof and make T1's trichotomy postcondition (not just cases (i) and (ii)) visible in the depends list.

VERDICT: OBSERVE

### PrefixOrderingExtension

#### "Least position" overstates what T1 supplies
**Class**: OBSERVE
**Issue**: The proof writes "By T1, `p₁ < p₂` gives a least position `k ≥ 1`..." T1's contract supplies an existential witness `k`, not "the least". Leastness is established inside T1's trichotomy proof (via NAT-wellorder), but it is not in T1's exported postcondition. The proof here does not actually require leastness — any witness `k` either falls under case (i) or under case (ii) where p₁ ≼ p₂ would follow, so non-nesting forces every witness into case (i). The wording is harmless but slightly overstates the contract being cited.

#### Postcondition phrasing "a < b under T1"
**Class**: OBSERVE
**Issue**: The contract's postcondition reads "`a < b` under T1." Other contracts in the dependency set use bare relational statements (e.g., T1's postconditions list `(A a ∈ T :: ¬(a < a))` without an "under …" suffix). The qualifier is non-load-bearing since `<` is the only strict order on T defined in scope, but it deviates from the surrounding contract style.

#### Implicit ℕ-order transitivity in length composition
**Class**: OBSERVE
**Issue**: The proof concludes "Since `k ≤ min(#a, #b)`, T1 case (i) yields `a < b`," which silently composes `k ≤ m` (from H2) with `m ≤ #a` (from Prefix's `#p ≤ #q`) via transitivity of `≤` on ℕ — a NAT-order fact that is neither cited nor declared in *Depends*. Both `T1` and `Prefix` declare NAT-order themselves, so the fact is reachable, but the contract here does not flag NAT-order as a direct dependency. This is the conventional "ℕ basics are implicit" style and is unlikely to confuse a reader, but a strict reading of the dependency contract would name it.

VERDICT: OBSERVE

### PartitionMonotonicity

#### Redundant re-derivation of T10a.2
**Class**: OBSERVE
**Issue**: The "Sibling prefixes are non-nesting" block re-proves from scratch (via TA5(c) uniform length, TA5(a) strict monotonicity, and Prefix's `p ≺ q ⟹ #p < #q`) exactly what T10a.2 (NonNestingSiblingPrefixes) already establishes. Citing T10a.2 once would replace three paragraphs. T10a.2 is not even listed in the declared `*Depends:*`, despite being precisely the needed lemma.

#### Distinctness citation uses TA5(a) where T10a.7 is cleaner
**Class**: OBSERVE
**Issue**: In "Total ordering → Uniqueness within a reach", distinctness of `u ≠ u'` for `u, u' ∈ dom(cᵢ)` is attributed to "(TA5(a))". TA5(a) gives only adjacent-step strict inequality `tₙ < tₙ₊₁`; non-adjacent distinctness requires T1 transitivity plus T1 irreflexivity, or equivalently T10a.7 (EnumerationInjectivity). T10a.7 is not listed in `*Depends:*`. The conclusion is correct but the single-axiom citation is under-resourced.

#### Precondition implicitly requires `p` to lie in an allocator's domain
**Class**: OBSERVE
**Issue**: The Preconditions say "a partition with prefix `p ∈ T`; up to two child-spawning events from `p`". For T10a to permit spawning *from* `p`, `p` must lie in `dom(parent)` — i.e., `p` must be an allocated address. This is load-bearing for the "Total ordering" section's claim that "`p` is itself an allocated address in `subtree(p)`", yet it is not stated as a precondition; the reader must infer it from the phrase "as permitted by T10a".

#### Termination argument understates the induction
**Class**: OBSERVE
**Issue**: The termination paragraph ("every allocated tumbler has finite length, the nesting depth within any sub-partition is bounded") conflates per-tumbler finiteness with the boundedness of the whole nesting depth. What actually justifies the induction is that the chain from `p` to any particular allocated `a` extends length strictly at each spawn, so the depth `≤ #a − #p`; the induction is well-founded on each witnessing `a`, not uniformly on the sub-partition. The rigor of the induction is intact but the stated reason is imprecise.

VERDICT: OBSERVE

### TA3-strict

#### Setup parenthetical takes a detour through `a > w`
**Class**: OBSERVE
**Issue**: In "Setup for remaining cases," the justification "`a_{d_a} > w_{d_a}` (from `a > w`, via T3's contrapositive giving `a ≠ w`, then T1 trichotomy)" derives `a > w` but doesn't explicitly name the downstream step. The strict inequality at `d_a` is actually TumblerSub's consequence under precondition `a ≥ w` (which is given directly) — so the T3/T1 chain to upgrade `a ≥ w` to `a > w` is not strictly needed. The reasoning is sound; TumblerSub is properly listed in Depends. Pure phrasing.

#### Case A: "(b, w) diverges at j" leaves `zpd(b, w) = j` implicit
**Class**: OBSERVE
**Issue**: In Case A, the step "`w_j = a_j < b_j`, so `(b, w) diverges at j` and `(b ⊖ w)_j = b_j - w_j > 0`" silently fixes `zpd(b, w) = j` to apply TumblerSub's component rule. The argument that (i) padded `b_i = w_i` for `i < j` (via `b_i = a_i` from T1 case (i) combined with `a` zpd-equal `w`) and (ii) padded `b_j ≠ w_j` at `j` — hence `zpd(b, w) = j` by minimality — is correct but compressed. A reader has to reconstruct why zpd is defined for `(b, w)` at exactly `j` (including the `j > #w` sub-case where `a_j = 0` forces `b_j ≠ 0 = ŵ_j`). Soundness not affected.

VERDICT: OBSERVE

### TA-strict

#### TA0 dependency redundancy
**Class**: OBSERVE
**Issue**: The dependency on TA0 is justified as supplying `a ⊕ w ∈ T` "so T1's ordering applies to the left-hand side," but TumblerAdd — already cited as the source of the ordering postcondition — itself exports `a ⊕ w ∈ T` as its first postcondition. TA0 is a sibling re-export of that same fact, so routing through it is slightly redundant rather than citing TumblerAdd directly. Soundness is unaffected.

VERDICT: OBSERVE

### T4b

#### NAT-discrete citation is redundant for ℕ⁺ placement
**Class**: OBSERVE
**Issue**: T4b's Depends entry for NAT-discrete states its role is "at m = 0, promotes non-zero components to strictly positive, placing the image of each projection in the all-ℕ⁺-component subset of T." But T4 defines ℕ⁺ = {n ∈ ℕ : 0 < n}, and for a non-separator component tᵢ (with tᵢ ∈ ℕ by T0 and tᵢ ≠ 0 by separator definition), NAT-zero's disjunction `0 < tᵢ ∨ 0 = tᵢ` alone suffices — the equality branch is excluded, leaving `0 < tᵢ`, which directly witnesses ℕ⁺ membership. NAT-discrete at m = 0 only adds the equivalent `1 ≤ tᵢ` reformulation, which is not used in the derivation. Position-inequality manipulations like `s_{j+1} ≥ s_j + 2` come from T4a (which carries its own NAT-discrete dependency for that promotion), not from T4b directly. The NAT-discrete dependency is therefore surplus, though declaring it does not affect soundness.

VERDICT: OBSERVE

### T4c

#### Exhaustion duplicates T4's Consequence
**Class**: OBSERVE
**Issue**: T4's Formal Contract already exports `zeros(t) ∈ {0, 1, 2, 3}` as a *Consequence:* for every T4-valid tumbler, derived by exactly the same argument (NAT-zero + NAT-order trichotomy + NAT-discrete + NAT-card's codomain) that T4c reproduces verbatim. T4c declares T4 in Depends, so it could just cite T4's Consequence and shed the NAT-zero, NAT-discrete, NAT-card, NAT-closure dependencies from the exhaustion step — none of them are needed anywhere else in T4c except injectivity (which uses NAT-closure/NAT-addcompat/NAT-order only). As written, T4c re-derives what T4 already guarantees, and the dependency list is padded accordingly.

#### Definitional content lives in Postconditions
**Class**: OBSERVE
**Issue**: The narrative states explicitly that "The four biconditionals are the definition of the labels" and that T4c is "a pure definition of labels on whatever T4-valid tumblers exist." T4's prose also calls T4c "the single definitional site" for the four predicates `t is a node address`, `t is a user address`, etc. These predicates have no prior introduction; they originate here. Encoding them solely in the *Postconditions:* field works, but a *Definition:* field — for instance, `(A t ∈ T : t is T4-valid :: t is a node address ⟺ zeros(t) = 0, t is a user address ⟺ zeros(t) = 1, t is a document address ⟺ zeros(t) = 2, t is a element address ⟺ zeros(t) = 3)` — would make the definitional status of the biconditionals explicit and separate the *introduction* of the four label predicates from the *exhaustion/injectivity* theorem that the claim proves about them.

VERDICT: OBSERVE

### T6

#### "T3-canonical" as a precondition is vacuous
**Class**: OBSERVE
**Issue**: The Preconditions read "`a, b ∈ T` satisfy T3 (CanonicalRepresentation) and T4 (HierarchicalParsing)." T3's Axiom is that tumbler equality is sequence equality — a universal property of `T`, not a predicate that some `t ∈ T` can fail. Every `a ∈ T` "satisfies" T3 by definition of the carrier, so the clause carries no content beyond `a, b ∈ T`. The T4-validity requirement does the actual work.
**Required**: (omit for OBSERVE)

#### Quantifier range omitted in Ingredient 3
**Class**: OBSERVE
**Issue**: "Sequences `S = (s₁, ..., sₘ)` and `R = (r₁, ..., rₙ)` are equal iff `m = n` and `(A i : sᵢ = rᵢ)`." The bound on `i` is left implicit; elsewhere in the claim (e.g., case (d) postcondition) the range is given explicitly as `1 ≤ i ≤ m`. The omitted range is recoverable from context but breaks the otherwise pedantic quantifier style.
**Required**: (omit for OBSERVE)

VERDICT: REVISE

### T7

#### Redundant NAT-addassoc invocation
**Class**: OBSERVE
**Issue**: The proof invokes NAT-addassoc to "rewrite as `(α + β) + 2 = (α + β') + 2`" and analogously "`(α + β + γ) + 3 = (α + β + γ') + 3`." Under the conventional left-associative reading of `α + β + 2`, these expressions are already `(α + β) + 2` and `(α + β + γ) + 3` syntactically, making the NAT-addassoc step vacuous. If the ASN's convention is left-associative (as is the usual mathematical default, and as appears elsewhere), NAT-addassoc is not load-bearing here and right cancellation at `m = 2` / `m = 3` applies directly to the as-written sums. Declaring NAT-addassoc as a dependency and invoking it in the proof is sound but not strictly needed; flagging so that either the convention is stated and the step dropped, or the step is kept but its role (converting from some non-default grouping) is made explicit.

#### T1 referenced in closing paragraph without dependency declaration
**Class**: OBSERVE
**Issue**: The final paragraph states "T1 places all text addresses (subspace 1) before all link addresses (subspace 2) within the same document, because `1 < 2` at the subspace position — a consequence of the lexicographic order, not an assumption." T1 is referenced by name but not declared in the Depends slot. The sentence reads as descriptive commentary rather than as part of T7's formal contract — its truth is not used to discharge the proof of the postcondition `a.E₁ ≠ b.E₁ ⟹ a ≠ b` — so this is not a soundness issue for T7 itself. Flagging so the intent is explicit: either mark the paragraph as non-normative commentary (and leave the Depends list alone), or promote the ordering statement to a genuine T7-exported Consequence with T1 declared as a direct dependency.

VERDICT: REVISE

### TA-PosDom

#### NAT-order dependency label understates usage
**Class**: OBSERVE
**Issue**: The NAT-order Depends entry says "`<`/`≤` transitivity and irreflexivity used both in the least-element witness and in the case analyses." The case split `#z ≥ k` versus `#z < k` is justified by at-least-one trichotomy (the partition is not derivable from transitivity and irreflexivity alone). The label reads tighter than the actual use.

VERDICT: REVISE

### TA-RC

#### Pos(w) not explicitly discharged before TumblerAdd invocation
**Class**: OBSERVE
**Issue**: The postcondition conjunct `Pos(w)` appears in the formal contract, and TumblerAdd/ActionPoint/TA0 all require `Pos(w)` as a precondition. The proof implicitly licenses this via "action point k = 2, since w₁ = 0 and w₂ = 2 > 0" but never cites TA-Pos explicitly to conclude `Pos(w)` from the exhibited component `w₂ = 2 ≠ 0`. A strict reader would expect a single line instantiating TA-Pos's existential at `i = 2` before using `actionPoint(w)` or TumblerAdd.

#### T0 membership of exhibited tumblers not stated
**Class**: OBSERVE
**Issue**: The postcondition quantifies over `a, b, w ∈ T`. The proof says "We exhibit three specific tumblers" but does not explicitly invoke T0 to justify that `[1,3,5]`, `[1,3,7]`, `[0,2,4]` are finite sequences over ℕ with length ≥ 1 — the membership is evident but not discharged against T0, which is not listed in *Depends* either.

VERDICT: OBSERVE

### TA-dom

#### Dependency justification describes TumblerAdd's proof, not TA-dom's
**Class**: OBSERVE
**Issue**: TA-dom's proof is a one-line re-export ("Immediate from TumblerAdd's … postcondition"). It does not itself perform any case analysis or invoke T3 directly. Yet two of the depends entries describe steps internal to TumblerAdd's proof rather than steps of TA-dom's own reasoning:
- TA0 is justified as "supplies `a ⊕ w ∈ T` (so T1's ordering applies on the left) and `#(a ⊕ w) = #w` (consumed by T3 in the equality case)" — but `a ⊕ w ∈ T` is already a direct postcondition of TumblerAdd (which is the sole arithmetic source), and the "equality case" lives inside TumblerAdd's proof, not TA-dom's.
- T3 is justified as "equality-from-component-agreement-and-equal-length, used when `aᵢ = 0` for all `i ≤ k`" — this describes an internal sub-case of TumblerAdd's derivation of `a ⊕ w ≥ w`. TA-dom does not itself branch on that sub-case.

The claim remains correct because all cited dependencies are available transitively, and the T1 entry (for the meaning of `≥`) is genuinely required by TA-dom as stated. But the justifications blur the line between "consumed by this claim's proof" and "consumed by the source postcondition's proof," which is mildly misleading for a re-export wrapper.

VERDICT: OBSERVE

### TA1

#### "Least j" framing is stronger than T1 provides
**Class**: OBSERVE
**Issue**: The proof states "there exists a least `j ≤ min(#a, #b)` with `aⱼ < bⱼ` and `aᵢ = bᵢ` for `i < j`". T1 case (i) merely provides an existential witness `k` with the agreement-before property — T1's definition does not promise a *least* such position. The proof does not use leastness anywhere (sub-case `j > k` only relies on agreement for `i < j`, which is T1's witness property, not minimality), so the word "least" is harmless but overstates what T1 exports.

#### Bound `j ≤ #w` left implicit when witnessing T1(i) on results
**Class**: OBSERVE
**Issue**: In sub-case `j < k`, the proof concludes "Position `j` witnesses T1 case (i): `a ⊕ w < b ⊕ w`" without stating the bound `j ≤ #(a ⊕ w) = #w` required by T1(i). It is derivable (`j < k ≤ #w` via ActionPoint's postcondition `actionPoint(w) ≤ #w` and NAT-order), but the reader must reconstruct it. A one-clause note would make this witness application airtight.

#### `≤` abbreviation not called out in T1 Depends rationale
**Class**: OBSERVE
**Issue**: The postcondition `a ⊕ w ≤ b ⊕ w` is an instance of T1's `≤` abbreviation — it is the disjunction of the strict-branch conclusions (sub-cases `j < k`, `j = k`) with the equality-branch conclusions (Case (ii), sub-case `j > k`). T1 is declared in Depends with rationale "case analysis on `a < b`; case (i) concludes strict ordering of results", which omits the role T1's `≤` abbreviation plays in assembling the final postcondition from strict and equality branches.

VERDICT: OBSERVE

### TA3

#### Sub-case B3 derivation of `dₐ ≤ #w` is tacit
**Class**: OBSERVE
**Issue**: The B3 argument concludes `a_{dₐ} < b_{dₐ} = w_{dₐ}` treating `w_{dₐ}` as a native component, but when `dₐ > #w`, `w_{dₐ}` is padded `0` and the equation `a_{dₐ} < 0` is vacuously impossible. The proof does not spell out that `dₐ ≤ #w` is forced here. The conclusion is still obtained (the contradiction in either branch reaches TumblerSub's consequence), but a reader has to reconstruct why the `dₐ > #w` side is closed off.

VERDICT: REVISE

### TA7a

#### Missing T3 dependency for component-equality conclusion
**Class**: OBSERVE
**Issue**: In the "Case `k = 1`, no divergence" branch, the narrative concludes "#o = #w = m, L = m, and o = w". The step from componentwise agreement plus equal length to tumbler equality is T3 (CanonicalRepresentation). T3 is not listed in Depends. TumblerSub/TA2 both declare T3 for analogous reasoning.
**Required** (if desired): Add T3 (CanonicalRepresentation) to Depends, or reword the branch to rely solely on TumblerSub's direct construction of the zero tumbler without invoking `o = w`.

#### "No-op" framing is misleading
**Class**: OBSERVE
**Issue**: For `k ≥ 2` with `#w ≤ m`, the proof says "the result equals `o` — a no-op, in S." This is not a subtraction no-op in the usual sense; it is a consequence of TumblerSub's divergence-at-1 branch setting `r_d = o_d − 0 = o_d` and `rᵢ = oᵢ` elsewhere. A reader who expects `o ⊖ w = o ⟺ w = 0` will be surprised that e.g. `[3, 4] ⊖ [0, 2] = [3, 4]`.
**Required** (optional): Replace "a no-op" with something like "the result is `o` itself, because divergence occurs at position 1 where `w₁ = 0`."

#### Quantifier notation `Pos(w)` in the bound-variable slot
**Class**: OBSERVE
**Issue**: The conjuncts write `(A o ∈ S, Pos(w) : k ≤ #o ⟹ o ⊕ w ∈ T)`. The bound-variable slot normally holds typings (e.g., `w ∈ T`), not predicates. `Pos(w)` is effectively a precondition; placing it beside `o ∈ S` conflates typing with predication and leaves `w`'s membership in `T` tacit.
**Required** (optional): Rewrite as `(A o ∈ S, w ∈ T : Pos(w) ∧ actionPoint(w) ≤ #o : o ⊕ w ∈ T)` and similarly for ⊖.

VERDICT: REVISE

### TS1

#### OrdinalDisplacement preconditions not explicitly discharged
**Class**: OBSERVE
**Issue**: The proof cites OrdinalDisplacement's postconditions three times ("δ(n, m) ∈ T", "Pos(δ(n, m))", "actionPoint(δ(n, m)) = m") but never explicitly discharges OrdinalDisplacement's four preconditions (n ∈ ℕ, m ∈ ℕ, n ≥ 1, m ≥ 1). The two that are not transferred from TS1's own hypotheses — m ∈ ℕ (from T0's length typing `#·: T → ℕ`) and m ≥ 1 (from T0's nonemptiness axiom `#a ≥ 1`) — are left for the reader to supply. These discharges are mechanical and both supporting axioms appear in the declared depends list (T0), so the conclusion stands; only the exposition is loose.

#### NAT-wellorder declared as a transitive-only dependency
**Class**: OBSERVE
**Issue**: The depends entry for NAT-wellorder reads "least-element principle underwriting Divergence case (i)'s well-defined index k." TS1's narrative does not invoke NAT-wellorder directly; it consumes Divergence case (i) as a black-box contract that already delivers k. The least-element construction of k lives inside Divergence's own proof, not inside TS1's reasoning. Listing it here records a transitive dependency rather than a direct one. Other transitive NAT dependencies of Divergence (e.g., NAT-closure for the `#a + 1` typing in case (ii)) are not carried forward in the same way, so the convention is uneven.

VERDICT: OBSERVE

### TS4

#### Missing direct declaration of T1 for the `>` symbol
**Class**: OBSERVE
**Issue**: The claim statement and postcondition use `>` (`shift(v, n) > v`, `v ⊕ δ(n, m) > v`), yet the depends list does not declare T1 (LexicographicOrder) directly; the semantics of `>` arrive only transitively through TA-strict. The claim's own convention for symbol grounding is otherwise strict — TA-Pos and ActionPoint are listed directly for `Pos(·)` and `actionPoint(·)` even though TA-strict already depends on them. For consistency, T1 could be listed as a direct depend on the same grounds (the target symbol `>` appearing in TS4's exported postcondition).

#### `#v = m` as a precondition is a binding, not a caller obligation
**Class**: OBSERVE
**Issue**: The formal contract lists `#v = m` among preconditions. Since `m` is a dummy bound by the claim's quantifier range and equals `#v` by the range predicate itself, it is not an independent obligation on the caller — it is an abbreviation. The narrative correctly says "the dummy `m` abbreviates `#v`," but the formal contract line reads as if the caller must establish an equality between an externally chosen `m` and `#v`. A caller with `v ∈ T, n ∈ ℕ, n ≥ 1` already obtains the conclusion without any `m`-level obligation; a "where m = #v" annotation, as OrdinalShift uses in its Definition line, would be clearer.

VERDICT: OBSERVE

30 verified, 78 observed, 32 found.
