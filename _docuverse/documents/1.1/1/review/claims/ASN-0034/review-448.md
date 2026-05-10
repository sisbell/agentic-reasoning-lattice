# Local Review — ASN-0034 (cycle 2)

*2026-04-23 16:42*

37 claims (AllocatedSet, GlobalUniqueness, NAT-addassoc, NAT-cancel, NAT-card, NoDeallocation, PartitionMonotonicity, ReverseInverse, T1, T10a.4, T10a.5, T10a.7, T10a.8, T12, T2, T4, T4a, T4b, T4c, T5, T6, T7, T8, T9, TA-LC, TA-MTO, TA-assoc, TA1, TA1-strict, TA4, TA5-SigValid, TA5a, TS3, TS4, TS5, TumblerAdd, TumblerSub)

## REVISE

### NAT-cancel

#### Symmetric absorption is derivable from right cancellation and NAT-closure's left identity
**Class**: REVISE
**Issue**: The narrative justifies stating all four clauses independently by noting that commutativity is not axiomatized, so "neither [absorption] form is derivable from the other." That justification is correct for the pair of absorption clauses taken in isolation, but it does not cover derivability from the cancellation clauses plus NAT-closure. The symmetric-form absorption `n + m = m ⟹ n = 0` is in fact derivable from the right-cancellation clause together with NAT-closure's left-identity `0 + n = n`: assume `n + m = m`; NAT-closure gives `0 + m = m`, hence `n + m = 0 + m`; right cancellation with `p := 0` yields `n = 0`. So one of the four posited axioms is redundant, and the narrative's reason for stating it independently does not hold up. (Note the asymmetry: the standard-form absorption `m + n = m ⟹ n = 0` is *not* similarly derivable — it would require a right identity `m + 0 = m`, which NAT-closure explicitly declines to axiomatize, so the standard form is genuinely independent.)
**Required**: Either (a) drop the symmetric-form summand-absorption clause from both the narrative and the *Axiom:* contract bullet, since it is a theorem of right cancellation plus NAT-closure's left identity, not an independent axiom; or (b) keep it but rewrite the justification paragraph to state the correct reason each clause is listed — standard absorption is independent because no right identity is available, right cancellation is independent because commutativity is not axiomatized, and symmetric absorption is retained for symmetry/convenience even though it follows from right cancellation and the left identity (and say so). The current wording conflates two distinct questions (derivability between the two absorption forms, vs. derivability of each form from the rest of the axiom system) and gets the second one wrong for the symmetric form.

VERDICT: REVISE

### TA5-SigValid

#### Non-standard field name "Guarantee" in Formal Contract
**Class**: REVISE
**Issue**: The Formal Contract uses `*Guarantee:*` for the output bullet. The standard field vocabulary used throughout the dependencies (TA5-SIG, T0, T4, NAT-order, NAT-zero) and the review checklist's field list is `Preconditions | Postconditions | Invariant | Frame | Axiom | Definition`. "Guarantee" is not on this list. TA5-SIG itself, the closest sibling, uses `*Postconditions:* 1 ≤ sig(t) ≤ #t`. Mixing vocabularies breaks uniform downstream consumption and review.
**Required**: Rename `*Guarantee:*` to `*Postconditions:*` (and pluralize `*Precondition:*` → `*Preconditions:*` to match the dependencies' convention).

### T4a

#### Vestigial strict-positivity argument; misdescribed NAT-discrete / NAT-zero uses
**Class**: REVISE
**Issue**: The setup paragraph argues "Every index not in `{s₁, …, s_k}` is a non-zero position; by T0 the carrier is ℕ, NAT-zero gives `0 ≤ tᵢ`, and NAT-discrete at `m = 0` rules out `0 ≤ tᵢ < 1` under `tᵢ ≠ 0`, so such a position carries a strictly positive value." The conclusion `tᵢ ≥ 1` is never used downstream — the Forward and Reverse derivations only ever say "`tᵢ` is a non-zero component" / "index `j` is a zero position" (the contrapositive of the zero-index defining predicate `tᵢ = 0`), never `tᵢ ≥ 1`. The Depends descriptions reflect this vestigial derivation: NAT-zero is described as supplying `0 ≤ tᵢ`, and NAT-discrete is described as converting `0 ≤ tᵢ ∧ tᵢ ≠ 0` into `tᵢ ≥ 1`. Meanwhile, the places NAT-discrete is *actually* load-bearing are not described in its Depends entry:
- Forward (i) contradiction and Reverse Interior: deriving `s_{i+1} ≥ s_i + 2` from `s_{i+1} > s_i` (gives `s_{i+1} ≥ s_i + 1` by NAT-discrete) plus `s_{i+1} ≠ s_i + 1` (gives `s_{i+1} > s_i + 1`, then NAT-discrete again).
- Reverse first segment: "`t₁ ≠ 0`, so index 1 is not a zero position, and therefore `s₁ ≥ 2`" — this step is `s₁ ≥ 1` (range) + `s₁ ≠ 1` (non-zero at 1) ⟹ `s₁ > 1` ⟹ `s₁ ≥ 2` via NAT-discrete.
- Reverse last segment: "`s_k ≤ #t − 1`" similarly needs NAT-discrete to step `s_k < #t` to `s_k ≤ #t − 1`.

As written, NAT-zero has no actual use in the T4a argument, and NAT-discrete's actual uses are undocumented in Depends.
**Required**: Either (a) delete the strict-positivity paragraph and the NAT-zero dependency entry, and rewrite the NAT-discrete entry to describe its real uses (promoting strict inequalities `s_{i+1} > s_i`, `s₁ > 1`, `s_k < #t` to their `+1` forms); or (b) keep the paragraph only if it is genuinely needed and explicitly invoke `tᵢ ≥ 1` somewhere in the proof. Update the Depends descriptions to match whichever choice is made, so reviewers can cross-check declared uses against proof steps.

VERDICT: REVISE

### T6

#### NAT-closure not declared in Depends
**Class**: REVISE
**Issue**: T6's proof and postconditions use the numerals `1`, `2`, `3` directly (e.g., `zeros(a) ≥ 1`, `zeros(a) ≥ 2`, `zeros(t) = 3`) and construct `m + 1` in "terminates in at most `m + 1` steps." These numerals must be grounded as ℕ-elements, and successor addition requires closure under `+`. Sibling claims T4, T4a, T4b all declare NAT-closure for exactly this purpose (e.g., T4b: "grounding the numeral `2 := 1 + 1 ∈ ℕ`"). T6 inherits the presence-pattern thresholds via T4b but still uses the numerals directly in the Formal Contract postconditions (e.g., `zeros(a) ≥ 1 ∧ zeros(b) ≥ 1`) and in the index-range quantifier `(A k : 1 ≤ k ≤ #D(b) : ...)`. The Depends list omits NAT-closure entirely, breaking the stated practice of this lattice.
**Required**: Add NAT-closure to the Depends list with a justification line (numerals `1, 2, 3 ∈ ℕ` via `1 ∈ ℕ` and closure of ℕ under addition; successor `m + 1 ∈ ℕ` in the termination-bound exposition).

## OBSERVE

### NAT-card

#### Loose domain phrasing in formal contract disambiguation
**Class**: OBSERVE
**Issue**: The formal contract closes with "`|·|` acts on subsets of ℕ and is distinct from T0's tumbler-length `#·`". Read strictly, "subsets of ℕ" would include infinite subsets (e.g., ℕ itself, or the evens) — but the axiom only constrains `|S|` when `S ⊆ {1, …, n}` for some `n ∈ ℕ`. The narrative is more precise: "well-defined total function on subsets of every initial segment `{1, …, n}`". The disambiguation sentence's purpose is a type distinction (sets vs sequences) rather than a domain assertion, so this is loose phrasing rather than a correctness error, but "subsets of bounded initial segments of ℕ" or "finite subsets of ℕ" would match the actual axiom domain.

#### n = 0 edge case not explicitly addressed
**Class**: OBSERVE
**Issue**: The axiom quantifies `(A n ∈ ℕ : S ⊆ {1, 2, …, n} :: …)` and NAT-zero puts `0 ∈ ℕ`, so `n = 0` is in scope. Under the conventional reading where `{1, 2, …, 0} = ∅`, the only admissible `S` is `∅`, and everything lines up (`|∅| = 0 ≤ 0`). The claim does not explicitly call out this boundary, and "`{1, 2, …, n}` — built from `1 ∈ ℕ` and successor" in the NAT-closure justification reads most naturally for `n ≥ 1`. The claim is not wrong — it simply relies on the reader to unfold `n = 0` consistently.

VERDICT: OBSERVE

### TA5-SigValid

#### Invocation of TA5-SIG precedes its existence witness
**Class**: OBSERVE
**Issue**: The proof writes "Since `t_{#t} > 0`, by TA5-SIG, `sig(t) = max(S)`" before it has exhibited that `#t` is a valid index (i.e., `1 ≤ #t ≤ #t`). TA5-SIG's nonzero branch is gated on `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`, not on `t_{#t} ≠ 0` in isolation; the witness `i = #t` is only justified in the following sentence via T0's `#t ≥ 1`. The content is present but the ordering invokes the conclusion before the witness has been assembled. A stricter reader would establish `#t ∈ S` first, then invoke TA5-SIG.

VERDICT: REVISE

### TA5a

#### NAT-discrete listed in Depends but not invoked in proof steps
**Class**: OBSERVE
**Issue**: The Depends bullet declares NAT-discrete's role as "with NAT-zero yields non-zero ⇒ strictly positive on ℕ," and the preamble announces this reading "via NAT-zero's `0 ≤ n` and NAT-discrete instantiated at `m = 0`." But no proof step actually routes through that non-zero⇒positive conversion. The only place a ≠-0 conclusion is derived is in case `k = 0`, where `t_{sig(t)} + 1 ≠ 0` is obtained from `t_{sig(t)} + 1 > t_{sig(t)} ≥ 0` — NAT-zero plus NAT-addcompat's strict successor inequality, with no appeal to NAT-discrete.

#### Failure bullet silent on `k = 2 ∧ zeros(t) = 3`
**Class**: OBSERVE
**Issue**: The Failure bullet states only "For `k ≥ 3`, `inc(t, k)` violates T4 (adjacent zeros create an empty field)." But the iff in the Guarantee also implies failure at `k = 2` when `zeros(t) = 3`, because `zeros(t') = zeros(t) + 1 = 4 > 3` violates T4's zero-count clause. The Failure bullet does not mention this second failure regime, which has a different proximate cause (zero-count overflow, not adjacency) than the `k ≥ 3` case.

#### T4(iii) `t'_1 ≠ 0` not explicitly discharged in cases `k = 0, 1, 2`
**Class**: OBSERVE
**Issue**: The proof walks through T4's zero-count, adjacency, and boundary-`t'_{#t'}` clauses in each of the three preservation cases, then concludes "T4 preserved." Clause T4(iii) `t'_1 ≠ 0` is never explicitly addressed. It is derivable — for `k = 1, 2` by TA5(b) and T4(iii) on `t`; for `k = 0` by TA5(b) when `sig(t) ≠ 1` and by `t'_{sig(t)} = t_{sig(t)} + 1 ≠ 0` at the edge case `#t = 1`, `sig(t) = 1` — but the edge-case thread for `k = 0` with `#t = 1` is not spelled out.

#### T4a citation is for flavor, not for a proof step
**Class**: OBSERVE
**Issue**: T4a is listed in Depends with the role "supporting the case `k ≥ 3` interpretation that adjacent zeros create an empty field." The proof's `k ≥ 3` case discharges violation by instantiating T4(ii) directly at `i = #t + 1`. The "empty field" reading appears only in the Failure bullet's parenthetical. T4a is not load-bearing for any step of the `k ≥ 3` argument; its presence in Depends is a narrative cross-reference rather than a cited lemma.

VERDICT: OBSERVE

### T10a.7

#### "Equivalently" misstates the relationship between the two postcondition forms
**Class**: OBSERVE
**Issue**: The Postcondition lists two forms joined by "Equivalently": the injection form `(A m, n ≥ 0 : m ≠ n : tₘ ≠ tₙ)` and the strict-monotone form `(A m, n ≥ 0 : m < n : tₘ < tₙ)`. These are not logically equivalent. The strict-monotone form is strictly stronger: it implies injection (via NAT-order trichotomy + T1 irreflexivity), but injection alone does not give strict monotonicity. The proof does establish the stronger form (the base case and inductive step both yield `tₘ < tₙ`), so what is exported is correct; only the "Equivalently" label misdescribes the logical relationship. A downstream reader could reasonably cite the stronger form, but the justification for doing so is "the proof establishes it," not "the two clauses are equivalent."

#### Induction principle on ℕ not cited in Depends
**Class**: OBSERVE
**Issue**: The proof proceeds "by induction on the gap `d = n - m ≥ 1`". Induction on ℕ is not supplied by any cited dependency (NAT-order gives irreflexivity/transitivity/trichotomy/disjointness but not induction; NAT-wellorder, which could ground induction via least-element, is not cited). This is consistent with the project-wide convention in T10a, T10a.3, T10a.4, T10a.5, and T10a.8, which all induct without citing an induction axiom, so treating ℕ-induction as primitive reasoning appears to be an established pattern. Noted only because it is the single step in the proof without an explicit justifying dependency.

VERDICT: OBSERVE

### T9

#### Proof duplicates T10a.7's work rather than citing it
**Class**: OBSERVE
**Issue**: T10a.7's equivalent postcondition is stated as "(A m, n ≥ 0 : m < n : tₘ < tₙ)" — which is literally T9's claim after unwrapping `allocated_before(a, b)` into `a = tᵢ, b = tⱼ, i < j`. T9 declares T10a.7 as a dependency but then reproves the same induction (base case via TA5(a), step via TA5(a) + T1(c) transitivity) that T10a.7 already carries out. A one-line invocation of T10a.7 suffices; the current proof replays its machinery. Not a correctness issue — the reproof is valid — but the dependency is cited for well-definedness only, while its central postcondition is the headline result.

#### "The same argument applies within each child allocator's domain" is redundant
**Class**: OBSERVE
**Issue**: The proof fixes a witnessing allocator `A` (abstract, via T10a.6) and inducts over `dom(A)`. The trailing sentence "The same argument applies within each child allocator's domain starting from its base `c₀ = inc(t, k')`" is already covered — `A` ranges over every allocator in 𝒯, including child allocators. The sentence reads as if child allocators need a separate argument, which they do not.

VERDICT: OBSERVE

### AllocatedSet

#### "Current frontier" phrasing in spawn clause
**Class**: OBSERVE
**Issue**: The activation predicate's transition clause glosses "s → s' spawns A" as "the child-spawning step `inc(spawnPt(A), spawnParam(A))` applied to parent(A)'s current frontier". This is inconsistent with (a) the earlier state-model sentence that uses a generic "inc(t, k') with k' ∈ {1,2}" and (b) T10a, which lets `spawnPt(A)` be any element of `dom(parent(A))`, not necessarily the current frontier — e.g., T9 explicitly motivates a spawn from an older element, "2.1.1 may be created after 2.2". The activation reasoning doesn't depend on spawnPt being the frontier, so the content is correct; the phrasing is sloppy.

#### T0(a), T0(b) declared but not visibly used
**Class**: OBSERVE
**Issue**: The depends list cites T0(a) (UnboundedComponentValues) with the rationale "underwriting the inexhaustibility of the sibling `inc(·,0)` chain" and T0(b) (UnboundedLength) with "allocator nesting via deep increments is not capped". The reasoning in this claim never instantiates either unboundedness witness: it only uses finite-index access `tᵢ` for `0 ≤ i ≤ nₛ(A)` and the `inc(·,0)` generator (inherited through T10a/TA5). These look defensive rather than load-bearing.

#### Activation well-definedness as a state function
**Class**: OBSERVE
**Issue**: The paragraph "Hence on every s reachable from s₀ the set {A : activated(A,s)} is determined by induction on any transition path from s₀" asserts path-independence without argument. Since the state s is stipulated to encode "which allocators have been activated", `activated(A, s)` reads off the state, and the inductive clauses function as a consistency constraint on transitions. The claim blurs definition and constraint. The at-most-once appeal at the end of the paragraph addresses non-revisitation, not path-independence per se.

#### parent(A) activation prerequisite for spawn
**Class**: OBSERVE
**Issue**: "s → s' spawns A" is described as the transition that applies `inc(spawnPt(A), spawnParam(A))`. An implicit precondition is that `parent(A)` is already activated at s and that `spawnPt(A) ∈ domₛ(parent(A))` — otherwise the spawn has no grounding in the realized tree. The claim doesn't state this, though it is forced by the state model and T10a.

VERDICT: OBSERVE

### TumblerSub

#### T3 reverse-direction depends entry unused
**Class**: OBSERVE
**Issue**: The Depends entry for T3 lists "reverse direction: length inequality implies tumbler inequality," but the proof does not invoke `#a ≠ #b ⟹ a ≠ b`. `a ≠ w` is derived once at the top via T3's forward-contrapositive direction from "not zero-padded-equal"; the sub-case analyses use ZPD-minimality, T1, and zero-padding — not T3's length-inequality direction. Only the forward direction is load-bearing.

#### "T3 (contrapositive)" step compresses a padding lemma
**Class**: OBSERVE
**Issue**: The step "Since zpd is defined, a and w are not zero-padded-equal (ZPD), so by T3 (contrapositive) a ≠ w" silently uses the implication `a = w ⟹ zpd(a,w) undefined`. That implication requires T3's `a = w ⟹ #a = #w ∧ aᵢ = wᵢ` plus a brief padding observation (equal length + equal components ⟹ padded projections coincide everywhere on {1,…,L}). The conclusion is correct; the attribution elides one step.

#### "w < a via T1 case (i), wₖ < aₖ" skips the trichotomy discharge
**Class**: OBSERVE
**Issue**: In Divergence case (i) for `(w, a)`, the claim writes "Since w < a via T1 case (i), wₖ < aₖ." The step actually goes: Divergence case (i) forces any T1 witness to be case (i) (case (ii) would require shared-position agreement, contradicting `wₖ ≠ aₖ` at shared `k`); uniqueness of the least-disagreement position pins the witness to `k`; then NAT-order trichotomy on `(wₖ, aₖ)` with `w < a` excludes `aₖ < wₖ` (which would witness `a < w`). The conclusion is valid, but the discharge of "T1(i) with witness exactly `k`" is suppressed.

#### Definition slot phrases `L` as "longer" when `#a = #w`
**Class**: OBSERVE
**Issue**: Postcondition wording "#(a ⊖ w) = L (the longer of #a and #w, named by NAT-order trichotomy per the Definition)" uses "longer" where case (α) has `#a = #w`. The parenthetical pointer to the Definition rescues the precision, but the gloss is mildly imprecise on the equal-length branch.

VERDICT: OBSERVE

### NoDeallocation

#### Quantifier scope over 𝒮 vs. reachable states
**Class**: OBSERVE
**Issue**: The axiom quantifies `(A op ∈ Σ, s ∈ 𝒮 :: op(s) defined ⟹ …)`. But AllocatedSet defines `activated(A, s)` — and hence `allocated(s)` — "by induction on the reachable-state graph rooted at s₀," noting explicitly that `allocated(s)` "is well-defined on all reachable states." For `s ∈ 𝒮` not reachable from s₀, `allocated(s)` is not guaranteed to be defined by the supplied dependency, so the axiom's conclusion `allocated(s) ⊆ allocated(op(s))` is not obviously type-correct over the full state space. In practice `s₀` is reachable and transitions preserve reachability, so the effective statement is the one about reachable states. A tighter quantification — `s reachable from s₀` — would match AllocatedSet's scope exactly. An incorrect fix (e.g., broadening AllocatedSet to all of 𝒮) would be worse than leaving the looseness, so logged as OBSERVE.

#### Framing: axiom on Σ vs. consequence of AllocatedSet's transition clause
**Class**: OBSERVE
**Issue**: AllocatedSet already describes every state transition as either (a) advancing an allocator's frontier by one `inc(·, 0)` (adding `t_{nₛ(A)+1}` to `domₛ(A)`), (b) spawning a child allocator (augmenting the activated set and thus the union), or (c) non-allocating (leaving every realized domain unchanged). Under this construction, `allocated(s) ⊆ allocated(op(s))` is a derivable monotonicity result, not purely an axiom. The claim's framing as "design constraint accepted as an axiom" is still defensible — it records the closure of Σ under non-removing transitions — but the distinction between "axiom on Σ's closure" and "consequence of the transition clause's enumeration" could be made sharper. Not a correctness defect.

VERDICT: OBSERVE

### T4c

#### Exhaustion duplicates T4's exported Consequence
**Class**: OBSERVE
**Issue**: T4 already exports `zeros(t) ∈ {0, 1, 2, 3}` as a Consequence in its own Formal Contract, derived by the same iterated trichotomy + NAT-discrete chain that T4c reproduces nearly verbatim. T4c could simply cite T4's Consequence rather than re-deriving it from scratch, which would also let T4c shed NAT-card, NAT-zero, NAT-discrete, and most of NAT-order/NAT-closure from its Depends slot (only the injectivity branch genuinely needs NAT-addcompat, NAT-order transitivity, and the numerals). The duplication is not unsound — both derivations rely on the same axioms — but it inflates the dependency surface and the proof body. Logged as observation; correctness is intact.

VERDICT: OBSERVE

### T6

#### NAT-card not declared but zeros(·) cardinality re-used
**Class**: OBSERVE
**Issue**: T6 uses `zeros(a) ≥ 1`, `zeros(a) ≥ 2`, `zeros(t) = 3` as type-correct comparisons in ℕ. The type `zeros(t) ∈ ℕ` is axiomatized by NAT-card in T4. T4b re-declares NAT-card even though T4 establishes it. T6 consumes the presence pattern through T4b's postcondition, which already packages `zeros(t) ∈ ℕ` membership, so strict re-declaration is arguably unnecessary — but it departs from sibling practice. Noting for consistency, not correctness.

#### NAT-discrete cited as support for decidable ℕ-equality
**Class**: OBSERVE
**Issue**: Ingredient 3 says "Decidability of equality on ℕ follows from NAT-order's trichotomy together with NAT-discrete." Exactly-one trichotomy on its own decides equality (exactly one of `m < n`, `m = n`, `n < m` holds); density of the order would not obstruct decidability of `=`. NAT-discrete does appear earlier in Ingredient 1 (promoting non-zero to strictly positive) and is genuinely needed for bounded-step termination of the componentwise loop. The "forecloses density for Ingredient 3" role stated in the Depends bullet is a weaker justification than the citation suggests. Not incorrect — just imprecisely framed.

VERDICT: REVISE

### T7

#### Strict positivity attributed loosely
**Class**: OBSERVE
**Issue**: The proof twice attributes strict positivity of non-separator components to just T0 ("By T0, every component lies in ℕ, so every non-separator component is strictly positive") and "T0 and T4's role-assignment". T0 alone fixes the carrier as ℕ, which includes 0; bridging from "in ℕ and non-zero" to "strictly positive" requires NAT-zero's disjunction or a direct appeal to T4's Axiom clause "0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ at every position present." The conclusion is available — T4 is already in Depends and its Axiom directly supplies strict positivity — but the citation chain as written skips the step.

#### NAT-addassoc appeals are no-ops under left-associativity
**Class**: OBSERVE
**Issue**: The two appeals to NAT-addassoc — "rewrite as `(α + β) + 2 = (α + β') + 2`" and "rewrite as `(α + β + γ) + 3 = (α + β + γ') + 3`" — are trivial under the standard left-associative reading of `+`, where `α+β+2` already parses as `(α+β)+2` and `α+β+γ+3` as `((α+β)+γ)+3`. The right cancellations at `m=2` and `m=3` and the subsequent left cancellations at `m=α` and `m=α+β` all apply without regrouping. The extra explicitness is defensible but NAT-addassoc is not doing load-bearing work here; the Depends entry could be dropped without affecting the proof.

#### Case-1 appeal to T3 is the reverse-direction contrapositive
**Class**: OBSERVE
**Issue**: In Case 1 the step "by hypothesis `a[p] ≠ b[p]`, so by T3, `a ≠ b`" uses the contrapositive of T3's reverse direction (`a = b ⟹ a_i = b_i`). That is supported because T3 is a biconditional, but the proof never states that `p ≤ #a` and `p ≤ #b` so that `a[p]` and `b[p]` are both well-defined at the common index. It follows implicitly from `δ ≥ 1`/`δ' ≥ 1` (giving `p = α+β+γ+4 ≤ #a`) established earlier, but the Case 1 paragraph does not surface this check.

VERDICT: OBSERVE

### TA1

#### "Least j" qualifier is unnecessary and not directly exported by T1
**Class**: OBSERVE
**Issue**: The proof opens Case (i) with "there exists a least `j ≤ min(#a, #b)` with `aⱼ < bⱼ` and `aᵢ = bᵢ` for `i < j`." T1's contract only guarantees existence of *a* witness `k` satisfying its case (i) conditions, not specifically the least such. Selecting the least would require an additional appeal (e.g., to NAT-wellorder, as T1's own trichotomy proof does internally). However, the TA1 argument never actually uses minimality — in every sub-case the agreement clause `aᵢ = bᵢ for i < j` is applied at `i < k` or `i = k < j` directly. The word "least" is thus harmless surplus; existence of any witness suffices.

VERDICT: OBSERVE

### TA1-strict

#### Dangling prose after the formal contract
**Class**: OBSERVE
**Issue**: The claim ends with an incomplete sentence after the formal contract: "But TA1 alone does not guarantee that addition *advances* a position. It preserves relative order between two positions but is silent about the relationship between `a` and `a ⊕ w`. We need:" — the colon terminates mid-thought, and the reference to "TA1" (vs. this claim's label TA1-strict) is inconsistent. If this is a transition to a sibling claim in the ASN, it belongs outside TA1-strict's claim section; if it's the start of a forgotten addendum, it should be completed or deleted.

#### T3 listed as dependency but not directly invoked
**Class**: OBSERVE
**Issue**: The Depends list names T3 (CanonicalRepresentation) with justification "backs Divergence's exhaustiveness at the case-(ii) rule-out." The proof does not cite T3 directly — it consumes Divergence's exhaustiveness as a postcondition of Divergence, which internally rests on T3. Other dependencies (T0, T1, Divergence, TA-Pos, ActionPoint, TA0, TumblerAdd, NAT-order, NAT-addcompat, NAT-cancel) are all directly invoked in the proof body. Listing T3 transitively is non-uniform with neighboring claims and adds a dependency that the reasoning does not itself exercise.

VERDICT: OBSERVE

### TS4

#### Implicit reflexivity of ≤ in fourth precondition discharge
**Class**: OBSERVE
**Issue**: The proof's fourth TA-strict precondition check reads: "From OrdinalDisplacement's exported postcondition `actionPoint(δ(n, m)) = m`. Since #v = m, we have m ≤ m." The final step weakens the equality `actionPoint(δ(n, m)) = #v` (via m = #v) to `actionPoint(δ(n, m)) ≤ #v`, which uses reflexivity of `≤` — an immediate consequence of NAT-order's defining clause `m ≤ n ⟺ m < n ∨ m = n`. NAT-order is not declared in TS4's Depends. Sibling claims in this region (OrdinalShift, OrdinalDisplacement, ActionPoint) explicitly cite NAT-order when weakening equalities to `≤`. The omission is minor and the underlying inference is standard, but a precise reader notices the missing citation.

#### Range-predicate binding of m
**Class**: OBSERVE
**Issue**: The claim range `v ∈ T ∧ n ∈ ℕ ∧ n ≥ 1 ∧ #v = m` treats `#v = m` as binding m (as explained in the dummy-variable paragraph), yet the range never asserts `m ∈ ℕ` or `m ≥ 1` directly — these are instead recovered from T0. This convention works, but it places `m` in an unusual position: the universal quantifier binds m while the range predicate forces m = #v uniquely. An equivalent phrasing `(A v, n : v ∈ T ∧ n ∈ ℕ ∧ n ≥ 1 : shift(v, n) > v)` with `m = #v` as a local abbreviation in the proof would be cleaner. Does not affect correctness; flagged for the record.

VERDICT: OBSERVE

### TS5

#### Substitution naming confuses TS3 invocation
**Class**: OBSERVE
**Issue**: "Invoke TS3 (ShiftComposition) at u = v, a = n₁, b = d" introduces parameter names `u, a, b` that do not match TS3's actual parameters `v, n₁, n₂`. The reader has to guess that `u ↔ v`, `a ↔ n₁`, `b ↔ n₂`. Worse, `u` is reused a few lines later with a different meaning (`Let u = shift(v, n₁)`). The application is correct, but the notation invites misreading. Cleaner: "Invoke TS3 at substitution n₂ ↦ d".

#### Postcondition `<` vs proof's `>` — converse conversion implicit
**Class**: OBSERVE
**Issue**: The proof concludes `shift(v, n₂) = shift(u, d) > u = shift(v, n₁)`, in `>`-form inherited from TS4. The claim's postcondition uses `<`: `shift(v, n₁) < shift(v, n₂)`. The bridge (`a > b ⟺ b < a` on T) is standard, but no dependency in this claim grounds the tumbler order or its converse relation — the worked example does cite T1 for lexicographic ordering, yet T1 is absent from Depends. Either state the postcondition in `>`-form to match TS4, or add T1 as the grounding source for `<` on T.

VERDICT: OBSERVE

20 verified, 34 observed, 4 found.
