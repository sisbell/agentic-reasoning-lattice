# Local Review — ASN-0034 (cycle 1)

*2026-04-23 16:03*

81 claims

## REVISE

### NAT-cancel

#### Formal Contract missing Depends slot
**Class**: REVISE
**Issue**: The Formal Contract lists only `*Axiom:*` but no `*Depends:*` slot. The claim uses `+` and `0` as primitive symbols in its axioms; these come from NAT-closure (for `+ : ℕ × ℕ → ℕ`) and NAT-zero (for the literal `0 ∈ ℕ`). NAT-closure itself sets the precedent in this ASN by declaring NAT-zero in its Depends slot with the explicit rationale "without NAT-zero supplying the constant the left-identity clause would reference an ungrounded symbol." The absorption clauses `m + n = m : n = 0` and `n + m = m : n = 0` reference the literal `0` in exactly the same way, so the same grounding obligation applies.
**Required**: Add a `*Depends:*` slot to the Formal Contract. At minimum list NAT-closure (supplier of `+`) and NAT-zero (supplier of the literal `0` used in both absorption forms). Do not rely on transitive reach through NAT-closure for NAT-zero, since the precedent in this ASN is to name the supplier of a literal directly.

### NAT-card

#### Existence of strictly increasing enumeration not justified
**Class**: REVISE
**Issue**: The axiom defines `|S|` as "the unique `k ∈ ℕ` such that `S` admits a strictly increasing enumeration `s₁ < s₂ < … < s_k`". For this definition to be well-posed, both existence and uniqueness of such `k` must be secured. The narrative addresses only uniqueness ("two strictly increasing enumerations of the same set must agree element-by-element"); existence — that every `S ⊆ {1, …, n}` admits *some* strictly increasing enumeration — is never grounded. The available dependencies (NAT-order, NAT-closure, NAT-zero) give a strict total order and `0, 1, +`, but no induction principle or well-foundedness of `<` on ℕ, which is what is actually needed to produce an enumeration (e.g., by repeatedly extracting the minimum of `S \ {s₁, …, s_{i-1}}`).
**Required**: Either (a) state existence explicitly as part of the axiom (treating `|·|` as a primitive operator postulated to satisfy the enumeration characterisation) and drop the appeal to "uniquely determined"; or (b) declare a dependency that supplies the ingredient needed to construct the enumeration (e.g., induction on ℕ, well-foundedness of `<`, or a minimum-of-finite-subset guarantee) and outline the construction.

#### Uniqueness argument outruns trichotomy alone
**Class**: REVISE
**Issue**: The narrative says uniqueness of `k` follows "under NAT-order's trichotomy". Trichotomy lets one compare any two naturals, which is enough to conclude `s₁ = t₁` when both are the minimum of a two-element set, but it is not enough to conclude that two strictly increasing enumerations of the same finite set agree element-by-element at all indices and have the same length. That step requires induction on `k` (or on `|S|`), which is not among the declared dependencies. The "agree element-by-element" appeal is therefore under-justified given the imports.
**Required**: Either tighten the dependency list to declare the induction/well-foundedness principle actually used, or demote the uniqueness argument to a posit inside the axiom (so the narrative is not owed a derivation).

#### Upper bound `|S| ≤ n` asserted without derivation
**Class**: REVISE
**Issue**: The formal contract lists `(A n ∈ ℕ : S ⊆ {1, 2, …, n} :: |S| ≤ n)` as part of the axiom, and the narrative asserts it as a conclusion ("and `|S| ≤ n` for every such `S`"). From the enumeration characterisation, `|S| ≤ n` follows by observing `s_i ≥ i` (since `s₁ ≥ 1` and `s_{i+1} > s_i`) and then `k = s_k · 1 ≤ s_k ≤ n` — an argument that uses induction over `i` plus arithmetic on successor, beyond what trichotomy + left-identity supply directly. The narrative neither offers this derivation nor frames `|S| ≤ n` as an additional axiom clause with its own justification.
**Required**: Either present `|S| ≤ n` as an independent axiom clause (and say so in the body) with the ingredients it rests on, or derive it from the enumeration characterisation using an induction principle that is added to Depends.

### TA5-SigValid

#### NAT-order missing from Depends
**Class**: REVISE
**Issue**: The proof uses `≤` and its properties extensively but NAT-order is not declared in Depends. Specific uses: (a) NAT-zero's axiom is the disjunction `0 < n ∨ 0 = n`; reading it as `0 ≤ t_{#t}` requires NAT-order's definition `m ≤ n ⟺ m < n ∨ m = n`. (b) The final step concludes `sig(t) = #t` from `sig(t) ≥ #t` and `sig(t) ≤ #t` — antisymmetry of `≤`, supplied by NAT-order (via trichotomy). (c) The `1 ≤ i ≤ #t` range clause throughout uses `≤`.
**Required**: Add NAT-order to Depends with roles: supplies `≤` (via `m ≤ n ⟺ m < n ∨ m = n`) used for `0 ≤ t_{#t}`, the TA5-SIG bound `sig(t) ≤ #t`, and `#t ∈ S` via `1 ≤ #t ≤ #t`; supplies antisymmetry to combine `sig(t) ≥ #t` and `sig(t) ≤ #t` into `sig(t) = #t`.

#### NAT-discrete role is incorrect / unnecessary
**Class**: REVISE
**Issue**: The proof describes NAT-discrete's role as "at `m = 0`, converts `0 ≤ t_{#t}` with `t_{#t} ≠ 0` into `t_{#t} > 0`". NAT-discrete's form `m ≤ n < m+1 ⟹ n = m` requires the upper bound `t_{#t} < 1` as a hypothesis, which the proof never establishes. The conversion is achieved directly from NAT-zero: its axiom `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` combined with `t_{#t} ≠ 0` eliminates the equality disjunct, giving `0 < t_{#t}`. No NAT-discrete step is needed.
**Required**: Rewrite step 4 of the proof to argue directly from NAT-zero's disjunction form: "NAT-zero supplies `0 < t_{#t} ∨ 0 = t_{#t}`; T4's `t_{#t} ≠ 0` excludes the equality branch, leaving `0 < t_{#t}`." Drop NAT-discrete from Depends, or — if a discreteness-based route is preferred — fix the role description to actually name what NAT-discrete discharges.

### T10a.4

#### Spawning point written as base in inductive step
**Class**: REVISE
**Issue**: The inductive step concludes "Hence `inc(b, k')` satisfies T4 and serves as the child allocator's base," but T10a defines a child's base as `inc(spawnPt(A), spawnParam(A))` where `spawnPt(A) ∈ dom(parent(A))` — not necessarily the parent's base `b`. The proof has just argued the right preparation ("Every `t` in the depth-`d` allocator's domain is T4-valid"), but the conclusion reverts to `b`. The base address `b` is only one element of `dom(parent)`; a child can be spawned from any `t ∈ dom(parent)`, including post-`inc(·,0)` elements, so writing the child base as `inc(b, k')` is literally false for those cases. This also matters for the `k' = 2` guard: T10a enforces `zeros(t) ≤ 2` at the actual spawning point `t`, not at `b`; TA5a's preservation envelope must be instantiated at that `t` as well.
**Required**: Replace `inc(b, k')` in the conclusion with `inc(t, k')` (for the spawning point `t ∈ dom(A)`), and make explicit that the induction's extended hypothesis — every `t ∈ dom(A)` is T4-valid — is what licenses applying TA5a at `t`, with T10a's `zeros(t) ≤ 2` guard invoked at that same `t` when `k' = 2`.

### T10a.7

#### NAT-order used but not declared
**Class**: REVISE
**Issue**: The proof opens with "By trichotomy of `<` on ℕ, either `m < n` or `n < m`" — a direct invocation of NAT-order's trichotomy on natural-number indices `m, n`. NAT-order is not listed in the Depends field of the Formal Contract (only T10a, TA5, and T1 are listed). T1's own proof is careful to cite NAT-order for exactly this step; T10a.7 omits it.
**Required**: Add NAT-order (or NatStrictTotalOrder) to the Depends list with the usage annotation "trichotomy on ℕ indices — resolves `m ≠ n` into `m < n ∨ n < m`". Update the summary depends entry in T10a's table accordingly.

### AllocatedSet

#### Formal contract buries postconditions under *Definitions*
**Class**: REVISE
**Issue**: The *Formal Contract* lists only *Definitions* and *Depends*. But items (i) `domₛ(A) ⊆ dom(A)`, (ii) initial-segment structure, (iii) reachable-state containment, the initial-state equality `allocated(s₀) = {t₀}`, and the *Transfer of T9* statement are not definitions — they are consequences the claim proves and that downstream claims will need to cite. They are currently embedded inside the "Domain embedding" bullet under *Definitions*, so downstream citations cannot cleanly point at "AllocatedSet's postcondition on initial-segment structure" vs. "AllocatedSet's definition of domₛ(A)."
**Required**: Split the *Formal Contract* into *Definitions* (state space, transition vocabulary, domₛ(A), allocated(s), state transition) and *Postconditions* (initial state `allocated(s₀) = {t₀}`; (i) inclusion; (ii) initial-segment structure with preserved enumeration indices; (iii) reachable-state containment of `dom(A)`; T9 transfer to realized allocations). Leave "Domain embedding" in *Definitions* only if it is recast as pure setup, with the three conclusions moved out.

#### "Activated" predicate is used but never defined
**Class**: REVISE
**Issue**: `allocated(s) = ⋃ { domₛ(A) : A activated in s }` is the central definition, but "A activated in s" is not given a formal definition as a state predicate. The prose mentions that s₀ activates the root and that allocation-affecting transitions "spawn a child allocator," but there is no formalization of how activation evolves across transitions (e.g., "A activated in s' iff A activated in s or s → s' spawns A"). Without this, `allocated(s)` is not well-defined on non-initial states from this claim alone.
**Required**: Add a formal definition of the activation predicate, either as a dynamic rule (root activated at s₀; activation persists; child activated exactly when parent performs the spawning inc(·, k′) with k′ > 0) or as a fixpoint over the reachable transition graph. Either surface it in the contract *Definitions* or reference a dependency that supplies it.

### NAT-addassoc

#### Missing Depends in formal contract
**Class**: REVISE
**Issue**: The claim's `*Formal Contract:*` lists only `*Axiom:*` but omits a `*Depends:*` slot. The axiom clause `(A m, n, p ∈ ℕ :: (m + n) + p = m + (n + p))` references both `ℕ` and the binary operation `+`. Neither is introduced by this claim: `+ : ℕ × ℕ → ℕ` is posited by NAT-closure (which itself depends on NAT-zero and NAT-order for `ℕ`). Without a `*Depends:*` entry the `+` symbol in the axiom is ungrounded at the contract level, and the exported contract diverges from the convention visible in NAT-closure's own contract (which does list `*Depends:*`). A downstream claim citing NAT-addassoc cannot determine from the contract alone that `+` is the NAT-closure operation and not some other `+`.
**Required**: Add a `*Depends:*` entry under the formal contract listing NAT-closure (supplies `+ : ℕ × ℕ → ℕ`, the operation whose associativity is posited). If the project convention also requires transitive acknowledgement of the carrier, note NAT-zero / NAT-order via NAT-closure's own depends chain; otherwise a single NAT-closure entry suffices.

### T5

#### Missing NAT-order and NAT-wellorder in depends
**Class**: REVISE
**Issue**: The proof invokes well-ordering of ℕ to pick "the least index in `{1, ..., #p}` with `bₖ ≠ pₖ`" (Case 1), and invokes trichotomy on ℕ to conclude "exactly one of `bₖ < pₖ` or `bₖ > pₖ` holds". Both are genuine uses of NAT-wellorder and NAT-order respectively. The Depends list names only Prefix, T1(i), T1(ii), and T3 — neither NAT-wellorder nor NAT-order appears. T1's own contract cites both explicitly for the same moves, so the omission here is a contract gap rather than a stylistic variance.
**Required**: Add NAT-order (NatStrictTotalOrder) — trichotomy used to dichotomize `bₖ ≠ pₖ` into `bₖ < pₖ ∨ bₖ > pₖ`, and `≤`/`<` clauses used throughout for length reasoning. Add NAT-wellorder (NatWellOrdering) — least-element principle used in Case 1 to select the minimal divergence index `k`.

### T12

#### Formal Contract uses non-standard field name "Premise"
**Class**: REVISE
**Issue**: The Formal Contract opens with `*Premise:*` listing `s ∈ T`, `ℓ ∈ T`, `Pos(ℓ)`, and `actionPoint(ℓ) ≤ #s`. These are preconditions, and every dependency cited (Span, T0, T1, TA0, TA-strict) uses the standard field name `*Preconditions:*`. The checklist enumerates the permitted fields as Preconditions, Postconditions, Invariant, Frame, Axiom, Definition — "Premise" is not among them. The narrative itself consistently calls these "the preconditions of Definition (Span)," so the contract field name drifts from the narrative's own terminology.
**Required**: Rename `*Premise:*` to `*Preconditions:*` in the Formal Contract. Content need not change.

VERDICT: REVISE

### T2

#### Missing NAT-discrete dependency for Case 2 prefix sub-cases
**Class**: REVISE
**Issue**: In Case 2 sub-cases `m < n` and `n < m`, the proof invokes T1 case (ii) ("T1 case (ii) gives `a < b`" and "T1 case (ii) with roles swapped gives `b < a`"). T1 case (ii) requires a witness `k` with `k = m + 1 ≤ n` (resp. `k = n + 1 ≤ m`). The proof supplies `m < n` (resp. `n < m`) but never bridges to `m + 1 ≤ n` (resp. `n + 1 ≤ m`). That bridge is exactly NAT-discrete's forward direction `m < n ⟹ m + 1 ≤ n`, which T1's own proof declares and uses for the same step. T2's Depends list omits NAT-discrete.
**Required**: Either (a) add `NAT-discrete (NatDiscreteness)` to the Depends list, citing the forward direction `m < n ⟹ m + 1 ≤ n` as the bridge from the case hypothesis to T1 case (ii)'s arithmetic witness; or (b) derive the required inequality explicitly from already-declared dependencies if possible (NAT-order alone does not appear to suffice, since `<` is primitive and `≤` is only `< ∨ =`).

VERDICT: REVISE

### T4b

#### Exhaustion gap: well-definedness on the full T4-valid subset is asserted without grounding exhaustion
**Class**: REVISE
**Issue**: The Definition stipulates `dom(N)` = the T4-valid subset (and `dom(U)`, `dom(D)`, `dom(E)` as specified subsets thereof), and the narrative concludes "each projection is well-defined and unique on its stated domain." For `N` to be a function on all T4-valid `t`, the per-`k` case enumeration (`k = 0, 1, 2, 3`) must cover every T4-valid `t` — i.e. `zeros(t) ∈ {0,1,2,3}` for every T4-valid `t`. This is exhaustion, and it requires NAT-discrete applied to the `0 ≤ zeros(t) ≤ 3` bound (or, equivalently, citing T4's Exhaustion Consequence). But T4b explicitly says "exhaustion of `zeros(t) ∈ {0,1,2,3}` over the T4-valid subdomain is not asserted here and is discharged downstream by T4c's Exhaustion paragraph." This creates two problems:
(a) T4b asserts well-definedness on a domain that requires exhaustion, while simultaneously declining to establish exhaustion — internally inconsistent.
(b) The deferral is forward (to downstream T4c), even though T4's own Formal Contract already exports `zeros(t) ∈ {0,1,2,3}` as a Consequence — a citable upstream fact. The T4 dependency line lists only `zeros(t) ≤ 3`, boundary clauses, no-adjacent-zeros, and separator role — not T4's Exhaustion Consequence.
**Required**: Either (i) cite T4's Exhaustion Consequence (`zeros(t) ∈ {0,1,2,3}` for every T4-valid `t`) directly in the T4 Depends entry and use it to collapse the per-`k` case construction into full coverage of `dom(N)`; or (ii) cite NAT-discrete applied to the bound `0 ≤ zeros(t) ≤ 3` with `zeros(t) ∈ ℕ` to derive exhaustion locally. Remove the forward deferral to "T4c's Exhaustion paragraph" — the downstream claim cannot ground T4b's own well-definedness postcondition.

VERDICT: REVISE

### TS4

#### TA-strict has four preconditions, not two
**Class**: REVISE
**Issue**: TA-strict's Formal Contract lists four preconditions: `a ∈ T`, `w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #a`. TS4's proof says "Apply TA-strict with a = v and w = δ(n, m). Two preconditions:" and discharges only `Pos(δ(n, m))` and `actionPoint(δ(n, m)) ≤ #v`. The membership precondition `w ∈ T`, i.e. `δ(n, m) ∈ T`, is not discharged anywhere in the proof, and the OrdinalDisplacement depends entry lists only `Pos(δ(n, m))` and `actionPoint(δ(n, m)) = m` among the postconditions it supplies — `δ(n, m) ∈ T` (which is in fact an OrdinalDisplacement postcondition) is absent. OrdinalShift's postcondition `shift(v, n) ∈ T` is about `v ⊕ δ(n, m)`, not `δ(n, m)`, so it does not cover this gap.
**Required**: Expand the proof to cite four preconditions: `v ∈ T` from TS4's precondition; `δ(n, m) ∈ T` from OrdinalDisplacement's postcondition; `Pos(δ(n, m))` and `actionPoint(δ(n, m)) ≤ #v` as already shown. Update the OrdinalDisplacement entry in the depends list to include the `δ(n, m) ∈ T` postcondition among those it supplies.

## OBSERVE

### ActionPoint

#### T0 dependency description omits wᵢ ∈ ℕ
**Class**: OBSERVE
**Issue**: The Depends entry for T0 lists "supplies T, #w, component projection wᵢ, and the commitment that the index domain `{1, …, #w}` of w lies in ℕ." The derivation instantiates NAT-zero's `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` at n = w_{actionPoint(w)} and NAT-discrete's forward direction at m = 0, n = w_{actionPoint(w)}; both instantiations require w_{actionPoint(w)} ∈ ℕ, which is supplied by T0's clause "aᵢ ∈ ℕ at each i ∈ {1, …, #a}" — but this commitment is not mentioned in the T0 dependency role, only the index-domain commitment is. The dependency role undersells what T0 is actually delivering here.

#### Implicit i ≤ #w in the "wᵢ = 0 for i < actionPoint(w)" argument
**Class**: OBSERVE
**Issue**: The sub-argument "otherwise i would be a member of S with i < actionPoint(w)" assumes, for 1 ≤ i < actionPoint(w), that i ≤ #w so that i satisfies S's range predicate. This follows from actionPoint(w) ≤ #w combined with transitivity of ≤, but is not spelled out. Minor; the step is easily reconstructed.

VERDICT: OBSERVE

### NAT-addcompat

#### NAT-order Depends description omits `<` usage
**Class**: OBSERVE
**Issue**: The Depends bullet for NAT-order only justifies it via the non-strict `≤` used in the compatibility clauses: "supplies the non-strict companion `≤`... used in the antecedents `p ≤ n` and the consequents `m + p ≤ m + n` and `p + m ≤ n + m`". It omits that NAT-order also supplies the strict-order primitive `<` that appears in the third clause `n < n + 1`. Similarly, the narrative paragraph says the strict successor inequality "uses that same closed addition together with NAT-closure's `1 ∈ ℕ`" but never attributes the `<` symbol to NAT-order. The dependency is correctly declared, so the axiom body remains readable — only the gloss is incomplete.

VERDICT: OBSERVE

### NAT-sub

#### Signature of `−` not posited in opening register
**Class**: OBSERVE
**Issue**: NAT-order opens with `< ⊆ ℕ × ℕ` and NAT-closure opens with `+ : ℕ × ℕ → ℕ` before constraining the primitive. NAT-sub has no analogous signature clause introducing `−`. The prose says subtraction is "a partial binary operation" but the formal contract's first clause is already the conditional-closure axiom `(A m, n ∈ ℕ : m ≥ n : m − n ∈ ℕ)`, which conflates signature and closure. Readable, but departs from the register the supporting prose itself invokes when citing NAT-closure's opening register.

#### Redundant conjunct in strict monotonicity antecedent
**Class**: OBSERVE
**Issue**: Strict monotonicity lists `m ≥ p ∧ n ≥ p ∧ m < n` as antecedent. Given `m ≥ p` and `m < n`, transitivity in NAT-order yields `p ≤ m < n`, hence `p < n`, hence `n ≥ p` via the `≤`-definition. The `n ≥ p` conjunct is derivable from the other two and could be dropped; it is retained only to make both subtractions' definedness visually apparent on the antecedent face.

#### Right telescoping implicitly asserts `m + n ≥ n`
**Class**: OBSERVE
**Issue**: `(A m, n ∈ ℕ :: (m + n) − n = m)` is stated unconditionally. Under conditional closure, `(m + n) − n ∈ ℕ` is only guaranteed when `m + n ≥ n`. The axiom therefore implicitly co-posits `m + n ≥ n` alongside the equation (the RHS `m ∈ ℕ` plus the equation forces the LHS into ℕ). The fact `m + n ≥ n` is not established by NAT-order, NAT-closure, or any declared dependency, so telescoping carries this as a tacit side-assertion rather than a derived consequence. Legitimate as an axiom, but the side-assertion is worth recording.

VERDICT: OBSERVE

### TA5-SIG

#### Implicit transitivity in `m ≥ 2 ≥ 1`
**Class**: OBSERVE
**Issue**: The chain `m ≥ 2 ≥ 1` — derived from `i₀ ≥ 1` and `i₀ + 1 ≤ m` — bundles two moves that are not individually cited: (a) lifting `1 ≤ i₀` to `2 ≤ i₀ + 1` (right order compatibility of addition, NAT-addcompat), and (b) transitivity of `≤` (derivable from NAT-order's transitivity of `<` plus its definitional `≤`-clause, but not itemized in NAT-order's Consequence slot). The NAT-addcompat citation lists only *strict successor inequality* as the usage, so right order compatibility — if invoked here — is not declared. A leaner route that uses only strict successor inequality (`i₀ < i₀ + 1`, hence `i₀ ≤ i₀ + 1`) and transitivity of `≤` would avoid the `2` intermediary entirely and reach `m ≥ 1` directly; that is the fact the subsequent NAT-sub closure actually needs.

#### Implicit `i + 1 ≥ 1` discharge
**Class**: OBSERVE
**Issue**: The strict-monotonicity application "at `p = 1`, with both `i + 1 ≥ 1` and `m ≥ 1`" discharges `i + 1 ≥ 1` without derivation. For `i ∈ S` (so `i ≥ 1`), this needs either transitivity of `≤` applied to `1 ≤ i ≤ i + 1` (via strict successor inequality) or addcompat right order compatibility applied to `0 ≤ i`. Routine, but elided — consistent with the terseness already flagged above.

VERDICT: OBSERVE

### NAT-cancel

#### Summand absorption as independent axiom vs. consequence of cancellation
**Class**: OBSERVE
**Issue**: The standard-form absorption `m + n = m ⟹ n = 0` is derivable from left cancellation together with NAT-closure's left-identity clause `0 + n = n`: rewrite `m` on the right as `m + 0` (using right identity) — but this ASN does not posit `n + 0 = n` (NAT-closure explicitly notes the mirrored clause is not axiomatized). So standard-form absorption is *not* derivable from the stated left cancellation alone. Symmetric-form absorption `n + m = m ⟹ n = 0`, however, *is* derivable from right cancellation plus NAT-closure's left identity: `n + m = m = 0 + m`, then right-cancel `m`. The claim's rationale ("neither form is derivable from the other" due to absent commutativity) is correct as stated between the two absorption forms, but it does not acknowledge that symmetric-form absorption is derivable from right cancellation + left identity, so it need not be posited as an independent axiom.
**Required**: (omit — observation only; positing a theorem as an axiom is redundant but not incorrect)

VERDICT: REVISE

### T3

#### Axiom vs Postcondition classification
**Class**: OBSERVE
**Issue**: The review checklist gives T3's exact shape as the canonical *Axiom* example ("(a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b) ≡ (a = b)"). The claim encodes extensional equality of sequences, which is a fundamental assertion of how equality on T is defined, not a derived input/output guarantee. The current contract uses *Postcondition*, which is defensible given the proof-from-T0 framing, but treating this as an Axiom (or at minimum adding that label) would more faithfully mirror the checklist's intent and signal to downstream consumers that this is definitional extensionality rather than a computed result.

#### Ellipsis in informal claim statement
**Class**: OBSERVE
**Issue**: The narrative form `a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b` uses `n` without binding it: when `#a ≠ #b`, the `aₙ = bₙ` conjuncts are ill-defined on the shorter sequence. The Formal Contract's postcondition correctly uses bounded quantification `(A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`, so the formal content is precise, but the informal statement relies on the reader silently resolving the ambiguity via the `#a = #b` conjunct.

VERDICT: OBSERVE

### T1

#### Non-standard "Abbreviations" field in Formal Contract
**Class**: OBSERVE
**Issue**: The Formal Contract introduces `a ≤ b` and `a ≥ b` under a field labeled "Abbreviations", which is not one of the prescribed fields (Preconditions, Postconditions, Invariant, Frame, Axiom, Definition). The analogous content in the NAT-order dependency is placed under "Definition" (`(A m, n ∈ ℕ :: m ≤ n ⟺ m < n ∨ m = n)` etc.). Folding these into the existing "Definition" slot would align with the format used by the upstream foundation.

#### Case k₁ < k₂ transitivity: existence-of-component argument is compressed
**Class**: OBSERVE
**Issue**: In sub-case `k₁ < k₂` of transitivity, the text writes "the existence of `cₖ₁` gives `k₁ ≤ p`". The underlying reasoning — that `k₂ ≤ p` holds in both witness cases of `b < c` (via (i) `k₂ ≤ p` directly, via (ii) `k₂ = n+1 ≤ p`), so `k₁ < k₂ ≤ p` yields `k₁ ≤ p` — is not spelled out. The conclusion is correct but the bound `k₂ ≤ p` is silently extracted. A one-line justification would close the gap.

#### "Resolves m ≠ n into m < n ∨ n < m" step is redundant in Case 3
**Class**: OBSERVE
**Issue**: In Case 3, clause (β) already yields `m < n` and clause (γ) already yields `n < m` by the preceding derivation. The subsequent sentence "NAT-order's trichotomy at `(m, n)` resolves `m ≠ n` into `m < n ∨ n < m`" merges the two sub-branches and re-derives what each branch independently established. This is harmless but slightly obscures that the post-split `if m < n` / `if n < m` corresponds exactly to the (β)/(γ) branch already under examination.

VERDICT: OBSERVE

### NAT-card

#### T0 dependency is disambiguation-only
**Class**: OBSERVE
**Issue**: The T0 dependency is justified solely by the disambiguation remark "distinct from T0's tumbler-length `#·`". Nothing in the axiom body, the enumeration characterisation, or the upper bound consumes T0's content; T0 is cited only to note that `|·|` is a different operator from `#·`. This is a weaker coupling than the other three dependencies, which supply symbols `<`, `≤`, `1`, `0` used in the axiom itself. Leaving it in is defensible (disambiguation is a real reader service), but the review should note that T0 could be demoted from Depends to a prose cross-reference without weakening the formal contract.

VERDICT: REVISE

### TA5-SigValid

#### "Guarantee" non-standard field name
**Class**: OBSERVE
**Issue**: The Formal Contract uses a `*Guarantee:*` field. The review checklist and neighboring contracts (TA5-SIG, T4) use `*Postconditions:*` for what the claim ensures after its preconditions hold. "Guarantee" is not one of the enumerated field names.

#### T0 nonemptiness role not declared
**Class**: OBSERVE
**Issue**: The proof step "The index `#t` belongs to this set" requires `1 ≤ #t` so that `#t ∈ {i : 1 ≤ i ≤ #t}`. That bound comes from T0's nonemptiness clause `1 ≤ #a`, but the T0 Depends role only mentions "fixes the carrier as ℕ, giving `t_{#t} ∈ ℕ`".

VERDICT: REVISE

### TA5a

#### T4a dependency declared but not invoked in proof
**Class**: OBSERVE
**Issue**: T4a is listed in *Depends:* with the note that it supports "the case `k ≥ 3` interpretation that adjacent zeros create an empty field." But the proof of case `k ≥ 3` proceeds directly via T4(ii) — "Instantiating T4(ii) at `i = #t + 1` gives `¬(0 = 0 ∧ 0 = 0)`, which fails" — and never invokes T4a's non-empty-field-segment reading. The parenthetical gloss in the *Failure:* bullet ("adjacent zeros create an empty field") is descriptive commentary rather than a logical step citing T4a. The proof is correct without T4a; the dependency is gestural.

#### Guarantee and Failure used as contract fields
**Class**: OBSERVE
**Issue**: The *Formal Contract:* ends with *Guarantee:* and *Failure:* rather than *Postconditions:*. The biconditional `inc(t, k)` satisfies T4 iff `k ∈ {0, 1}`, or `k = 2 ∧ zeros(t) ≤ 2` is a postcondition and the *Failure:* line is just the negation direction of the same iff. Content is complete; the field naming departs slightly from the checklist's enumerated fields (Preconditions, Postconditions, Invariant, Frame, Axiom, Definition). Parallel claims in the same ASN use these names too, so this is a corpus-wide style note rather than a local defect.

VERDICT: OBSERVE

### T10a

#### NAT-sub declared but not used in T10a.3
**Class**: OBSERVE
**Issue**: T10a.3's Depends lists "NAT-sub (closure and right-telescoping for the subtraction form)", but the proof of Consequence 3 establishes `#inc(t, k') > #t` purely via NAT-addcompat (strict successor and left order-compatibility); the additive across-d-levels form `m + k'₁ + … + k'_d` also uses no subtraction. The postcondition is stated in additive form, so no subtraction enters. The NAT-sub citation appears vestigial from an earlier subtraction-form formulation.

#### T10 cited in T10a-N Depends without being used
**Class**: OBSERVE
**Issue**: T10a-N's Depends list ends with a bare "T10." Unlike the other entries, it carries no gloss. T10 (PartitionIndependence) is a downstream consumer of T10a.2/T10a.5 — it doesn't participate in the necessity argument, which relaxes the sibling restriction and derives `a₁ ≺ a₂` by TA5(b)/TA5(d)/NAT-addcompat/Prefix. Including T10 invites a reader to search for where T10 is invoked and find nothing.

#### Asymmetric treatment of necessity components in T10a-N
**Class**: OBSERVE
**Issue**: The label "Necessity" and the result label "T10a-N (Necessity of sibling restriction)" name only one of the four axiom components — `k = 0`. The other three components (`k' ∈ {1, 2}`, at-most-once, root T4 initialization) are discussed in a closing paragraph that says they "serve distinct purposes" with pointers to Consequences 4 and 5, but no relaxation-counterexample is shown for any of them. This is consistent with the stated scope (the theorem label commits only to `k = 0`), but a reader may read the opening sentence "We establish eight consequences … then prove the sibling restriction necessary" as promising a broader necessity treatment than what is delivered.

#### Axiom Depends vs. Postcondition Depends split
**Class**: OBSERVE
**Issue**: The Formal Contract's axiom line declares only `T4, TA5, TA5a` as Depends — the minimum needed to read the axiom statement. The foundations that power the derivations (T0, T1, T3, Prefix, NAT-zero/discrete/closure/addcompat, TA5-SigValid) appear only in per-postcondition Depends lists. This is a consistent and defensible structure, but it means a reader scanning only the axiom line underestimates T10a's true transitive closure. Not a correctness issue — worth logging in case the pipeline ever aggregates only the axiom Depends.

VERDICT: OBSERVE

### T10a.3

#### Local monotonicity uses NAT-discrete via a path with a gap
**Class**: OBSERVE
**Issue**: The chain "NAT-sub's conditional-closure ... places `d_B − d_A ∈ ℕ`; NAT-zero gives `0 ≤ d_B − d_A`; NAT-discrete at `m = 0` rules out `0 ≤ d_B − d_A < 1`, yielding `d_B − d_A ≥ 1`" skips a step. NAT-discrete's equivalent form `0 ≤ n < 1 ⟹ n = 0` only rules out the half-open interval; to conclude `d_B − d_A ≥ 1` one still needs `d_B − d_A ≠ 0`, which follows from `d_B > d_A` plus a left-inverse step on subtraction. NAT-sub already provides the one-step path: strict positivity (`m > n ⟹ m − n ≥ 1`) instantiated at `m = d_B, n = d_A` yields `d_B − d_A ≥ 1` directly. The conclusion is sound; the chosen derivation just leaves an uncited intermediate.

#### Iterated lift in local monotonicity restates the running-sum bound
**Class**: OBSERVE
**Issue**: "Iterated NAT-addcompat order-compatibility across the `d_B − d_A` terms lifts each `1 ≤ k'_i` to `k'_{d_A+1} + … + k'_{d_B} ≥ d_B − d_A`" is the same induction proved in detail earlier for the prefix sum, applied to the sub-range `[d_A+1, d_B]`. Citing the prior sub-lemma rather than re-naming it "iterated" would make the dependency on the previously-established induction explicit.

#### Right-telescoping invocation reorders the sum implicitly
**Class**: OBSERVE
**Issue**: The application "NAT-sub's right-telescoping at `m = k'_{d_A+1} + … + k'_{d_B}, n = γ + k'₁ + … + k'_{d_A}` gives `#output(B) − #output(A) = k'_{d_A+1} + … + k'_{d_B}`" matches the form `(m + n) − n = m`, but the actual dividend `γ + k'₁ + … + k'_{d_B}` is `n + m`, not `m + n`. The rearrangement uses associativity/commutativity of `+` that aren't cited from NAT-closure. Conclusion is correct; the rearrangement is left tacit (consistent with the codebase's usual handling).

VERDICT: OBSERVE

### T10a.4

#### Non-standard "Proof structure" field in Formal Contract
**Class**: OBSERVE
**Issue**: The Formal Contract lists a *Proof structure* field, which is not among the standard fields (Preconditions, Postconditions, Invariant, Frame, Axiom, Definition). The content (induction on depth, base, step references) is accurate but duplicates the *Proof.* paragraph and sits outside the contract schema used by sibling claims.

VERDICT: REVISE

### T10a.7

#### Induction principle on ℕ left implicit
**Class**: OBSERVE
**Issue**: The proof proceeds "by induction on the gap `d = n - m ≥ 1`" with a base case at `d = 1` and step from `d` to `d + 1`. The induction principle itself is not cited, nor is the arithmetic on ℕ justifying `n - 1 ≥ m` when `d ≥ 2` or `(n-1) - m = d` when the current gap is `d+1`. Similar proofs in this ASN (e.g., T10a.5) make the NAT axioms they use explicit. Leaving induction and subtraction implicit here is a minor precision gap, not a correctness issue.

VERDICT: REVISE

### T9

#### Proof duplicates T10a.7
**Class**: OBSERVE
**Issue**: The inductive proof of T9 is essentially a verbatim replay of T10a.7's proof (same base case via TA5(a), same inductive step via TA5(a) + T1(c), and T10a.7's postcondition explicitly records the equivalent form `(A m, n ≥ 0 : m < n : tₘ < tₙ)`). Given that T9 already declares T10a.6 and T10a.7 as dependencies — the former to fix the witnessing `A` from `(a, b)`, the latter to fix indices — T9 reduces to one line: by T10a.6 pick the unique `A` with `a, b ∈ dom(A)`; by T10a.7 applied at `(i, j)` with `i < j`, `tᵢ < tⱼ`, i.e., `a < b`. The induction is redundant.

#### "Same argument applies within each child allocator's domain"
**Class**: OBSERVE
**Issue**: The closing sentence of the proof — "The same argument applies within each child allocator's domain starting from its base `c₀ = inc(t, k')`" — is not establishing a further case. The claim is quantified per-allocator, and every child allocator is already "an allocator `A`" for which the enumeration `t₀, t₁, …` is defined by T10a with base `c₀`. The remark is restating scope rather than discharging an additional obligation; readable as hand-waving.

#### Context paragraph mixes T1 case (ii) with T10a dynamics
**Class**: OBSERVE
**Issue**: The paragraph "When a parent forks a child via `inc(·, k')` … `2.1 < 2.1.1 < 2.2` by T1 case (ii)" motivates the per-allocator framing. The ordering `2.1 < 2.1.1` is via T1 case (ii) (prefix), but `2.1.1 < 2.2` is T1 case (i), not T1 case (ii). Minor imprecision in the illustrative aside; does not affect the formal content.

VERDICT: OBSERVE

### AllocatedSet

#### nₛ(A) when A is not activated
**Class**: OBSERVE
**Issue**: nₛ(A) is described as "the count of sibling increments performed" but its value when A is not activated in s is unspecified. The union in `allocated(s)` restricts to activated A, so this does not cause unsoundness, yet downstream claims that quantify over arbitrary A ∈ 𝒯 may encounter an undefined nₛ(A) without warning.

#### "Frontier" used without definition
**Class**: OBSERVE
**Issue**: "advances some allocator's frontier by one inc(·, 0) step" uses *frontier* as a primitive. The intended meaning — the maximal-index element t_{nₛ(A)} of domₛ(A) — is recoverable from context, but the term is not formally introduced here or in the listed dependencies.

VERDICT: REVISE

### Divergence

#### Case (ii) hypothesis understates its scope
**Class**: OBSERVE
**Issue**: The stated hypothesis of case (ii) is only "`#a ≠ #b`", but the sub-cases (ii-a)/(ii-b) each carry an additional shared-position agreement clause `(A i : 1 ≤ i ≤ min(#a,#b) : aᵢ = bᵢ)`. When `#a ≠ #b` AND a shared-position mismatch exists, the hypothesis of case (ii) holds yet neither sub-case is satisfied — no value is delivered by (ii) in that configuration. The definition is still total because case (i) covers it and mutual-exclusivity is ultimately argued against the sub-cases, not against the header. Readers would be better served by an explicit "and case (i) does not apply" rider (or equivalently lifting the agreement conjunct into the header), matching T1's cleaner single-`∃ k` structure.

#### Uniqueness of the NAT-wellorder least element is implicit
**Class**: OBSERVE
**Issue**: The symmetry argument in case (i) concludes that "NAT-wellorder returns the same least element" when S is swap-invariant. NAT-wellorder as stated asserts *existence* of a least element, not uniqueness; uniqueness follows from NAT-order antisymmetry (via the trichotomy/irreflexivity chain). The inference is routine and correct, but the dependency on NAT-order for least-element uniqueness is not called out in the symmetry paragraph the way it is in the uniqueness paragraph for `k, k'`.

VERDICT: OBSERVE

### ZPD

#### Formal Contract uses non-standard field names
**Class**: OBSERVE
**Issue**: The `*Formal Contract:*` block uses `*Domain:*`, `*Codomain:*`, and `*Partiality:*` — none of which appear in the standard field list (Preconditions, Postconditions, Invariant, Frame, Axiom, Definition). The dependency Divergence uses `*Preconditions:*` and `*Postconditions:*` for analogous content. `Domain: a ∈ T, w ∈ T` fits cleanly under Preconditions; `Codomain` and `Partiality` fit under Postconditions. The content is complete and correct; only the naming deviates from the surrounding ASN convention.

#### Symmetry postcondition argument compresses the padded-projection invariance
**Class**: OBSERVE
**Issue**: The symmetry sketch says "sub-cases (β) and (γ) swap under exchange, yielding the same `L`; the disagreement predicate is symmetric," but does not explicitly note that the padded sequences `â`, `ŵ` are built from operand-specific values, so under operand exchange the sequence formerly called `â` is the one now called `ŵ'` (and vice versa), giving the same index set `{k : âₖ ≠ ŵₖ} = {k : ŵ'ₖ ≠ â'ₖ}`. The argument is correct but the rename step is left to the reader. No correctness issue.

#### Relationship-to-Divergence case (i) minimality argument is implicit
**Class**: OBSERVE
**Issue**: For Divergence case (i), the text states "the padded projections coincide with the native projections through `1, ..., k`, so `zpd(a, w) = divergence(a, w) = k`." The minimality step — that no `k' < k` can witness `âₖ' ≠ ŵₖ'` because Divergence's universal `(A i : 1 ≤ i < k : aᵢ = bᵢ)` transports through the coinciding native/padded values — is left implicit. The conclusion `min = k` therefore rides on a one-line coincidence claim. The reasoning is sound; only the presentation is terse.

VERDICT: OBSERVE

### TumblerSub

#### Compressed link from `w < a` to `wₖ < aₖ` in Divergence case (i)
**Class**: OBSERVE
**Issue**: The line "Since `w < a` via T1 case (i), `wₖ < aₖ`, whence `aₖ > wₖ`" elides two steps. First, that `w < a` must be witnessed by T1 case (i) rather than case (ii) — this follows because Divergence case (i) supplies a shared-position mismatch `wₖ ≠ aₖ` with prior agreement, ruling out the proper-prefix shape of T1(ii). Second, that the T1(i) witness lands at the same `k` as Divergence's index — this follows from the uniqueness of Divergence's least mismatch. The reader can reconstruct both steps, but neither is named.

#### `0 ≤ aₖ` cited from NAT-zero
**Class**: OBSERVE
**Issue**: The clause "From NAT-zero's `0 ≤ aₖ` and NAT-order's `m ≤ n ⟺ m < n ∨ m = n`, the divergence `aₖ ≠ 0` leaves `0 < aₖ`" attributes `0 ≤ aₖ` to NAT-zero. NAT-zero's axiom is `0 < n ∨ 0 = n`; its `≤` form arises only after applying NAT-order's `≤`-definition. The chain still lands at `0 < aₖ` correctly, but the citation packaging suggests NAT-zero exports `≤` directly when in fact NAT-order is doing the lifting.

#### Symmetry of Divergence and ZPD invoked silently
**Class**: OBSERVE
**Issue**: Case analysis is opened on the pair `(w, a)` ("Two Divergence cases arise for the pair `(w, a)`") but then the conclusion `zpd(a, w) = divergence(a, w) = k` is stated for `(a, w)`. The reorientation relies on Divergence's symmetry `divergence(a, b) = divergence(b, a)` and ZPD's symmetry; both are postconditions of the dependencies but neither is named at the moment of use.

VERDICT: OBSERVE

### D0

#### T0 not declared in Depends
**Class**: OBSERVE
**Issue**: The proof and formal contract use T0-supplied constructs — membership `a, b ∈ T`, lengths `#a`, `#b`, component projections `aᵢ`, `bᵢ` — throughout (e.g., "ℕ-typed components", "T0's definition of T"). Sibling claims in this region (T1, T3, TumblerAdd, TumblerSub, TA2, etc.) uniformly declare T0. D0 omits it. Not a correctness gap — T0 is implicit — but an audit-trail inconsistency.

#### Terse step from Divergence case (i) to `aₖ < bₖ`
**Class**: OBSERVE
**Issue**: The sentence "We are therefore in case (i) … with `aᵢ = bᵢ` for `i < k` and `aₖ ≠ bₖ`. Since `a < b`, T1 case (i) gives `aₖ < bₖ`." skips the step that T1's witness position for `a < b` must coincide with Divergence's `k`. The argument (if T1's witness `k'` were `< k` or `> k`, it would contradict Divergence case (i)'s agreement/disagreement profile; if at `k`, T1 case (ii) is ruled out by `k ≤ #a`) is valid but left implicit. Alternative terse phrasing: "NAT-order trichotomy at `(aₖ, bₖ)` together with `aₖ ≠ bₖ` leaves `aₖ < bₖ` or `bₖ < aₖ`; the latter would witness `b < a` via T1 case (i) at `k`, contradicting `a < b` by NAT-order's trichotomy on the order." Not wrong, just compressed.

#### L used in postconditions without local definition
**Class**: OBSERVE
**Issue**: The formal contract postcondition `#(b ⊖ a) = L` references `L` with the parenthetical "per TumblerSub's length-pair dispatch at `(#b, #a)`". `L` is a local label to TumblerSub's trichotomy, not an imported term. The parenthetical makes the meaning recoverable, so this is readable; a fully self-contained postcondition would spell out `L = #b` when `#a ≤ #b`, `L = #a` when `#b < #a`.

VERDICT: OBSERVE

### NAT-addassoc

#### Narrative does not justify axiom status
**Class**: OBSERVE
**Issue**: The claim body is a single sentence stating associativity, with no accompanying discussion of *why* this is posited directly rather than derived. NAT-closure's body, by contrast, carefully explains the register in which `+` is posited, why NAT-zero is declared in Depends, and why the mirrored right-identity is intentionally not axiomatized. NAT-addassoc's minimal prose is correct but out of step with the surrounding claims' level of self-documentation; a reader of the contract alone cannot tell whether associativity is deliberately taken as primitive (the Peano-style derivation via induction having been set aside) or whether derivation work was simply deferred.

VERDICT: REVISE

### GlobalUniqueness

#### Case 5 final-line phrasing blurs two distinct contradictions
**Class**: OBSERVE
**Issue**: Case 5 closes with "Every pair in Case 5 thus satisfies `#a ≠ #b`; by T3, `a ≠ b`." The sub-case analysis actually contradicts the assumed length-equality in three different ways: (i) `k'₁ = k'₂` contradicts `#p₁ < #p₂` via NAT-cancel, (ii) `k'₁ < k'₂` contradicts assumed equality via chained ≤/< compatibility, and (iii) `k'₁ > k'₂` (the `(2,1)` case) derives different zero counts, contradicting Case 5's same-zero-count hypothesis rather than directly producing a length-equality contradiction. The proof acknowledges this inside the `(2,1)` sub-case ("contradicting Case 5's same-zero-count assumption"), but the blanket closing sentence reads as if all three sub-cases refuted the length-equality assumption directly. The conclusion `#a ≠ #b` nonetheless holds because all three sub-cases rule out `#p₁ + k'₁ = #p₂ + k'₂` (either by internal contradiction or by falsifying the ambient Case-5 hypothesis).

#### "T4 clause (iii)" is a local numbering not fixed by T4's contract
**Class**: OBSERVE
**Issue**: Case 5's `(2,1)` sub-case cites "T4 clause (iii) `t_{#t} ≠ 0`". T4's Formal Contract writes the field-segment constraint as an unnumbered conjunction (`zeros(t) ≤ 3; adjacency-ban; t₁ ≠ 0; t_{#t} ≠ 0`). The (iii) labeling is a reasonable reading of the last three conjuncts ("field-segment constraint"), but the enumeration is not declared in T4's contract, so the citation is locally unambiguous only because `t_{#t} ≠ 0` appears nowhere else in T4.

#### Case 5 preamble paragraph is subsumed by the general analysis
**Class**: OBSERVE
**Issue**: The first paragraph of Case 5 ("Let the parent have base `t₀` with `#t₀ = γ`...") proves length separation for the direct parent-child subset of the nesting-prefix case. The subsequent "For the general nesting-prefix pair" paragraph then re-proves a strictly more general statement that covers the preamble. The preamble reads as motivation but can be mistaken for an independent case; a reader checking exhaustiveness may try to match it against the later argument.

VERDICT: OBSERVE

### T5

#### `#p ≥ 1` mismatch between statement and contract
**Class**: OBSERVE
**Issue**: The claim statement says "For any tumbler prefix `p`", with no length restriction, but the proof opens "Let `p` be a tumbler prefix with `#p ≥ 1`" and the formal contract repeats `#p ≥ 1`. If `#p = 0` is admissible under T0, the set `{t ∈ T : p ≼ t}` becomes all of T (vacuously contiguous) and is skipped silently; if empty sequences are excluded at T0, the restriction is redundant. Either way the statement and contract should agree on whether the bound is a precondition or an automatic consequence.

#### Case 2 framing as "impossible" is slightly loose
**Class**: OBSERVE
**Issue**: The proof concludes "Since Case 2 is impossible, `p ≼ b` holds in all cases." Case 2 is not impossible in isolation — `#b < #p` is a well-formed condition on tumblers. What is impossible is *Case 2 under the preconditions* `p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c`. The phrasing reads as if `#b < #p` were structurally ruled out, rather than ruled out by the joint hypotheses. A tighter phrasing would say "Case 2 contradicts the hypotheses, so `#b ≥ #p`, and Case 1 applies."

VERDICT: REVISE

### PartitionMonotonicity

#### Decomposition of the partition is hand-waved
**Class**: OBSERVE
**Issue**: In the "Total ordering" section, the *Existence* argument asserts "every such `a` was produced by an allocator descended from `p`" and that "the lineage from `p` to `a`'s producer first leaves `p` through one of the two child-spawning increments." This is the key decomposition — that every allocated `a` with `p ≼ a`, `a ≠ p`, lies in `reach(c₁) ∪ reach(c₂)` — and the justification is implicit. It requires (a) ruling out non-ancestor/non-descendant allocators via the cross-allocator prefix-incomparability consequence (T10a.5), (b) ruling out ancestors of `A` by length separation (T10a.3), and (c) an induction showing that along any spawning chain, once a base fails to extend `p` (because it was spawned from a sibling of `p`), no descendant base does either (TA5(b) preserves positions `1..#p`, carrying the divergence at position `#p` forward). The claim is sound given T10a, but neither T10a.3 nor T10a.5 is cited here, and the chain-of-spawning argument is left implicit.

#### T5 declared but not load-bearing
**Class**: OBSERVE
**Issue**: T5 is cited at the opening ("By T5 (prefix convexity), this set forms a contiguous interval... No address from outside the partition can interleave between two addresses inside it") and listed in *Depends*. The remaining proof, however, establishes total ordering over allocated addresses by (i) Sibling non-nesting + PrefixOrderingExtension, (ii) Cross-param ordering via T1 case (i) at position `#p+1`, (iii) Structural induction with root preceding descendants via T1 case (ii), and (iv) T9 for per-allocator consistency. Contiguity of `subtree(p)` under T1 is not used in these steps — it is a rhetorical framing of why the partition "holds together," not a premise consumed by the proof chain.

#### Redundant spawning-chain reasoning in cross-param ordering
**Class**: OBSERVE
**Issue**: The argument for `a_{#p+1} ≥ 1` when `a ∈ subtree(u)`, `u ∈ dom(c₁)` traces "a chain of child-spawning and sibling increments in descendant allocators" with TA5(b)/TA5(c) invocations, and symmetrically for the `c₂` side. Since `u ≼ a` and `#u = #p+1`, Prefix alone gives `a_{#p+1} = u_{#p+1} ≥ 1` directly; analogously for `c₂`, `v ≼ b` with `#v = #p+2 > #p+1` gives `b_{#p+1} = v_{#p+1} = 0`. The framing via allocator lineage is also mildly misleading because `reach(c) = ⋃_{s ∈ dom(c)} subtree(s)` is a static set that contains tumblers not produced by any allocator; the positional property follows from the prefix relation, not from a production trace.

VERDICT: OBSERVE

### Span

#### Missing postcondition: membership of start position
**Class**: OBSERVE
**Issue**: The claim defines `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}` but does not establish any postconditions. The natural fact `s ∈ span(s, ℓ)` — equivalently, that a span is nonempty and contains its start — is immediate from `s ≤ s` (via T1's `≤` abbreviation `s < s ∨ s = s`, with the right disjunct trivial) and `s < s ⊕ ℓ` (from TumblerAdd's `a ⊕ w > a` postcondition under the stated preconditions). Leaving it implicit forces every downstream claim that reasons about span membership to rederive it.

#### Missing postcondition: set-theoretic typing
**Class**: OBSERVE
**Issue**: No postcondition states `span(s, ℓ) ⊆ T`. It is trivial from the set-builder `{t ∈ T : …}`, but the formal contract of a definitional claim typically exports the type fact so downstream obligations can cite it by label rather than by unfolding the definition.

#### No proof block for well-formedness of the defining set
**Class**: OBSERVE
**Issue**: The definition references `s ⊕ ℓ` inside the upper bound `t < s ⊕ ℓ`. Well-formedness of that bound rests on TA0 giving `s ⊕ ℓ ∈ T` under the four listed preconditions (whose instantiation is described in the depends line for TA0). A one-line derivation making this explicit — "the set is well-formed because TA0 at `(a,w) := (s,ℓ)` delivers `s ⊕ ℓ ∈ T`, placing the upper bound in the domain of `<` from T1" — would match the explicit style used in sibling claims (ActionPoint, TumblerAdd) and remove the reader's obligation to reconstruct why the set-builder is not circular.

VERDICT: OBSERVE

### TA-strict

#### TA0 dependency redundant with TumblerAdd
**Class**: OBSERVE
**Issue**: TA0 is listed as a dependency with the rationale that it supplies `a ⊕ w ∈ T` "so T1's ordering applies to the left-hand side." But TumblerAdd is already cited and directly exports both `a ⊕ w ∈ T` and `a ⊕ w > a` as postconditions. The ordering fact that TA-strict re-labels is established inside TumblerAdd's own proof (via T1 case (i) at position k), so the well-typedness of `>` at `(a ⊕ w, a)` is already bundled into the fact being re-exported. Citing TA0 adds a second path to the same guarantee rather than a distinct obligation.

VERDICT: OBSERVE

### T4c

#### Exhaustion duplicates T4's exported Consequence
**Class**: OBSERVE
**Issue**: T4's Formal Contract already exports `zeros(t) ∈ {0, 1, 2, 3}` as a Consequence, with a nearly word-for-word identical iterated-trichotomy derivation. T4c is declared to depend on T4, yet redoes the whole exhaustion argument from NAT-zero/NAT-order/NAT-discrete primitives instead of citing T4's Consequence. The proof works, but the redundancy bloats T4c and obscures the actual new content (the label-distinctness argument). Since T4 is in Depends, the Exhaustion paragraph could collapse to "By T4's exhaustion Consequence, `zeros(t) ∈ {0, 1, 2, 3}`." The corresponding NAT-zero / NAT-discrete / NAT-order-trichotomy entries in Depends would then be justified only by their use in Injectivity (where they are not in fact used), so some could be dropped as well.

#### Left identity `0 + 1 = 1` is used implicitly at the base of the injectivity chain
**Class**: OBSERVE
**Issue**: Injectivity instantiates NAT-addcompat's `n < n + 1` at `n = 0` to obtain `0 < 1`. Strictly, that instantiation gives `0 < 0 + 1`; rewriting to `0 < 1` requires NAT-closure's left-identity clause `0 + n = n` at `n = 1`. The subsequent links `1 < 1 + 1 = 2` and `2 < 2 + 1 = 3` fall out from the numeral definitions `2 := 1 + 1`, `3 := 2 + 1`, but the `0 < 0 + 1 = 1` step uses the left-identity and the NAT-closure Depends bullet only mentions "grounding the numerals…", not the left-identity unfolding. A one-clause mention ("and NAT-closure's left identity `0 + 1 = 1`") would make the chain airtight without changing the reasoning.

VERDICT: OBSERVE

### T6

#### Role of NAT-discrete in Ingredient 3's equality-decidability citation
**Class**: OBSERVE
**Issue**: Ingredient 3 says "Decidability of equality on ℕ follows from NAT-order's trichotomy together with NAT-discrete." Trichotomy plus disjointness already separates `m = n` from `m < n` and `n < m`; NAT-discrete's role here (foreclosing density) is not explicit. NAT-discrete seems more relevant to termination bounds (`m + 1` step count) than to the equality-decidability step it is credited with.

#### Attribution of "unambiguous partiality" to T4a
**Class**: OBSERVE
**Issue**: Ingredient 1 reads "Field absence is encoded by partiality of the projection (unambiguous by T4a, since every present segment is non-empty)." The unambiguity of "partial ⟺ absent" is established by T4b's presence-pattern postcondition (domains fixed by `zeros(t)` thresholds). T4a's non-emptiness of present segments rules out a different ambiguity (empty-but-present vs absent). The citation is essentially right but slightly misattributed.

#### Informal "m + 1 steps" complexity uses NAT-closure implicitly
**Class**: OBSERVE
**Issue**: The proof discusses termination in "at most m + 1 steps" using the successor term `m + 1`. Grounding `1 ∈ ℕ` and closure under `+` comes from NAT-closure, which is not declared in Depends. Since the termination bound is metalevel/complexity commentary (not a formal postcondition), this is a minor citation gap rather than a correctness break.

#### "T1 orders tumblers" opening reference
**Class**: OBSERVE
**Issue**: The section opens "T1 orders tumblers; T6 decides containment" but T1 does not appear in the provided dependencies and is not used in the proof. This is prose scene-setting, not a dependency citation; acceptable but worth noting since a reader may expect T1 to be load-bearing.

VERDICT: OBSERVE

### T7

#### Overstated strict positivity is unnecessary and depends on undeclared NAT-zero
**Class**: OBSERVE
**Issue**: The proof asserts "By T0, every component lies in ℕ, so every non-separator component is strictly positive" and later "one tumbler has `0` and the other has a non-separator component, strictly positive by T0 and T4's role-assignment." Strict positivity (`0 < tᵢ`) does not follow from `tᵢ ∈ ℕ ∧ tᵢ ≠ 0` without NAT-zero's disjunction `0 < n ∨ 0 = n` (as used in T4, T4a, T4b). NAT-zero is not declared in T7's depends. However, the argument does not actually need strict positivity — only `tᵢ ≠ 0` at the position `j` is needed to conclude `a[j] ≠ b[j]` (since the other tumbler has `0` there), and that non-zero condition is directly supplied by T4's separator/non-separator role assignment. So the claim is correct, but the attribution "strictly positive by T0" is stronger than the proof needs and stronger than T0 alone supports.

VERDICT: OBSERVE

### TA1-strict

#### Dangling text after Formal Contract
**Class**: OBSERVE
**Issue**: The claim section ends with the Formal Contract block (Preconditions, Depends, Postconditions), then emits additional narrative — "But TA1 alone does not guarantee that addition *advances* a position. It preserves relative order between two positions but is silent about the relationship between `a` and `a ⊕ w`. We need:" — that terminates mid-sentence with "We need:" and nothing following. This reads as transition text to a subsequent claim that has bled into this claim's section. It is not a correctness issue for the TA1-strict argument, but it is a structural artifact that a reader will trip over. Additionally the text refers to "TA1 alone" while the claim label is "TA1-strict" — minor naming inconsistency.

VERDICT: OBSERVE

### TA7a

#### Quantifier form in displayed formulas binds only one variable
**Class**: OBSERVE
**Issue**: The two displayed formulas `(A o ∈ S, Pos(w) : k ≤ #o ⟹ o ⊕ w ∈ T)` and `(A o ∈ S, Pos(w) : o ≥ w ⟹ o ⊖ w ∈ T)` mix a binding (`o ∈ S`) with a predicate (`Pos(w)`) in the binder slot, leaving `w` free. Other ASN formulas in this region use the strict `(A vars : range : body)` form (compare NAT-addcompat: `(A m, n, p ∈ ℕ : p ≤ n : m + p ≤ m + n)`). Intent is clear from the narrative ("w is a positive tumbler"), but the formula would be more correctly written `(A o ∈ S, w ∈ T : Pos(w) ∧ k ≤ #o : o ⊕ w ∈ T)`.

#### Claim heading overpromises relative to the formal statement
**Class**: OBSERVE
**Issue**: The heading "Subspace closure" and intro — "the result must remain in that subspace. Text positions must not cross into link space, and vice versa" — suggests S-closure, but the displayed formulas only establish T-closure. S-membership is conditional (tail positivity of w for ⊕; case-analysis for ⊖, with explicit T\S and Z branches in the postconditions). The Frame clause carries the "no subspace crossing" meaning; the ordinal-positivity strand of "S-closure" is genuinely not closed. Reader is forced to the contract to discover this.

#### ZPD and Divergence used in the narrative but not declared
**Class**: OBSERVE
**Issue**: Conjunct 2 speaks of "find divergence d" and the "no divergence branch", directly mirroring TumblerSub's ZPD/Divergence machinery, but the Depends list omits ZPD and Divergence. They are pulled in transitively through TumblerSub, but TA2 — which uses the same machinery — re-declares ZPD explicitly. Analogous redeclaration here would make the Depends list self-contained.

#### Redundant "m ≥ 1" stipulation
**Class**: OBSERVE
**Issue**: The opening of the claim states "ordinal `o = [o₁, ..., oₘ]` (where `m ≥ 1`)". Since `o ∈ T`, T0's `(A a ∈ T :: 1 ≤ #a)` already guarantees `m ≥ 1`. The parenthetical is harmless but redundant with T0, which is already declared.

VERDICT: OBSERVE

### TS3

#### Numeral `2` is not a foundation primitive
**Class**: OBSERVE
**Issue**: The right-side order chain reads `n₁ + n₂ ≥ 1 + n₂ ≥ 2 ≥ 1`, but the NAT foundation posits only `0 ∈ ℕ` (NAT-zero) and `1 ∈ ℕ` (NAT-closure) as numerals; `2` is not introduced. The Depends entry for NAT-addcompat writes the same chain correctly as `n₁ + n₂ ≥ 1 + n₂ ≥ 1 + 1 ≥ 1`, so the proof body and the contract disagree on notation.

#### Transitivity of ≤ attributed to transitivity of <
**Class**: OBSERVE
**Issue**: The chain `n₁ + n₂ ≥ 1 + n₂ ≥ 1 + 1 ≥ 1` is composed three links of `≤`. The claim's NAT-order Depends line says "defining clause ... and transitivity of `<` compose the chain." Chaining `≤` requires a four-way case split over the defining-clause unfolding (two uses of substitution under equality, one use of `<`-transitivity). The cited apparatus does cover it, but the prose elides the case split.

VERDICT: OBSERVE

### TS4

#### Dummy `m` inflates the Formal Contract precondition list
**Class**: OBSERVE
**Issue**: The quantifier range treats `m` as a dummy abbreviating `#v`, so `#v = m` is a binding clause, not an independent requirement. The Formal Contract nonetheless lists it among Preconditions as `#v = m`, which reads as an extra constraint the caller must satisfy. The substantive preconditions are only `v ∈ T, n ∈ ℕ, n ≥ 1`.

#### Reflexivity step unlabelled
**Class**: OBSERVE
**Issue**: "Since #v = m, we have m ≤ m" silently uses reflexivity of `≤` on ℕ from NAT-order (via `m ≤ n ⟺ m < n ∨ m = n` with the right disjunct). NAT-order is not declared in the depends list. The step is correct, but the missing citation is a minor accounting gap.

VERDICT: REVISE

45 verified, 73 observed, 16 found.
