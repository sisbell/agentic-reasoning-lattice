# ASN-0100: INSERT Operation

*2026-05-27*

## The Question

When new content is inserted at a position in a document's Vstream, what is the precise post-state? Three sub-questions structure the inquiry:

- *What is allocated* — what new state appears in the content store and in the document's arrangement?
- *What shifts* — which existing V→I mappings change position, and by how much?
- *What invariants must hold after completion* — and atomically, with no observable intermediate state in which some invariant is violated?

The answer must be sharp enough that an implementation can be measured against it, and abstract enough that two implementations meeting the spec are externally indistinguishable.

## Background: The Two-Stream Asymmetry

The foundation distinguishes two address spaces. The content store `C : T ⇀ Val` assigns content values to I-addresses; once `a ∈ dom(C)`, the binding is permanently fixed (S0). The arrangement `M(d) : T ⇀ T` assigns I-addresses to V-positions within document `d`; arrangements are mutable, but only in a controlled way.

INSERT acts on both, but asymmetrically. It *grows* `C` by appending fresh entries; it never alters existing entries, never reassigns I-addresses, never identifies one I-address with another. It *grows and rearranges* `M(d)`; it never alters the underlying I-addresses, only the V-positions at which they are observed.

This asymmetry is the architectural pivot. Existing content keeps its permanent I-address across INSERT. Its V-position within `d` may shift, but the I-address — and the value stored there — is invariant. Since links attach to I-addresses (not V-positions), insertion cannot break them. The I-address is the *identity* of a piece of content; the V-position is the *current location* of that identity within an arrangement.

We shall see that every constraint on INSERT — what may shift, what must be preserved, what counts as atomic — flows from this single asymmetry.

## The Operation's Inputs

INSERT takes three arguments: a target document `d ∈ dom(M)`, a V-position `p` at which the insertion begins, and a sequence of new content values `⟨v₀, v₁, …, v_{n−1}⟩` with `n ≥ 1`.

We restrict attention to the *content subspace* `s_C` of `d` — Nelson's text content. (The link subspace `s_L` is governed by a structurally similar but distinct extension operation; the present analysis does not cover it.)

The position `p` must be a *valid insertion position* in `V_{s_C}(d)`. We unpack this:

  `subspace(p) = s_C ∧ #p = m_C`

where `m_C` is the common depth of `V_{s_C}(d)` enforced by S8-depth (FixedDepthVPositions, ASN-0036) on the text subspace. For non-empty `V_{s_C}(d)` with current cardinality `N = |V_{s_C}(d)|`, the precondition is the binary predicate `ValidInsertionPosition(d, p)` (ASN-0036), which unpacks to:

  `p ∈ {shift(min(V_{s_C}(d)), j) : 0 ≤ j ≤ N}`

**Notational convention** (used throughout this ASN). We adopt `shift(t, 0) := t` as a notational extension of OrdinalShift (ASN-0034), which is defined only for `n ≥ 1`. This convention is consistent with OrdinalShiftBase (ASN-0058), whose definition `t + 0 = t` establishes the identity behaviour at offset zero under the `+` notation; we lift the same identity to the `shift(·, ·)` notation for uniform exposition. With this convention, the `j = 0` admissible position above resolves to `shift(min, 0) = min(V_{s_C}(d))` — insertion at the very beginning. The convention is used throughout the per-region clauses (Insertion at `k = 0` resolves to `M'(d)(p) = a_0`) and in the S8a, OrdAddHom, and ord-extraction analyses that follow.

This yields `N + 1` admissible positions: `j = 0` inserts before the first character, `j = N` after the last, and `j ∈ {1, …, N−1}` in the interior.

For empty `V_{s_C}(d)`, the precondition is the ternary predicate `ValidFirstInsertionPosition(d, p, m)` (ASN-0036): the caller chooses a depth `m ≥ 2` and the single admissible position is `[s_C, 1, …, 1]` of length `m`. The post-state has `V_{s_C}(d') ≠ ∅`, at which point S8-depth fixes `m_C = m` for `d` at every state in which `V_{s_C}(d)` remains non-empty — every subsequent text-subspace position in `d` must have depth `m` as long as that condition holds, since S8-depth is a per-state invariant under ValidComposite★ (ASN-0047). If a subsequent K.μ⁻ later empties `V_{s_C}(d)`, S8-depth holds vacuously at that state and imposes no constraint on `m_C`; a fresh INSERT into the then-empty text subspace re-enters `ValidFirstInsertionPosition(d, p, m')` with a caller-chosen `m'` that need not equal the prior `m`.

The condition `n ≥ 1` rules out a degenerate empty-insertion case. The values `v_k` must be elements of the content type `Val`; the abstract specification places no further constraint on their structure.

These preconditions are necessary; we shall verify they are jointly sufficient.

## Discovering the Three Effects

We reason from the intent backward to the formal specification. INSERT splices `n` new content units into `d`'s arrangement at V-position `p`. Three effects must obtain together.

### Effect One: Allocation

The new content units do not exist in `dom(C)` before the operation. Nelson is unambiguous (Q1, Q5, Q8): INSERT creates *new* content with *fresh* I-addresses. The operation does not reuse, alias, or identify with any pre-existing I-address.

The freshness comes from `d`'s content sub-allocator `A_C(d)`, by the substrate's allocation discipline (ASN-0093). We require `n` addresses, produced by `n` successive K.α firings under the substrate's transition vocabulary:

  `a_k = A_C(d)`'s `k`-th emission across the composite, for `0 ≤ k < n`

The freshness of each `a_k` is established against the state immediately preceding its K.α firing — not against the operation's pre-state Σ. Concretely, if Σ_k denotes the substrate state after K.α has fired for `a_0, …, a_{k−1}`, then K.α's precondition requires `a_k ∉ dom(Σ_k.C) ∪ dom(Σ_k.L)`. The two clauses of this conjunction are discharged by different substrate facts.

The `a_k ∉ dom(Σ_k.C)` clause holds by ChainEnumerationInjectivity (ASN-0093), which makes the chain enumeration `n ↦ t_n` injective: `a_k = t_{m_d + k + 1}` (where `m_d` is the chain index of the last emission already in `dom(Σ.C)` for origin `d`, or 0 if none), and the new index `m_d + k + 1` is strictly greater than every prior index, so `a_k` is distinct from `a_0, …, a_{k−1}` and from every pre-existing chain emission of `A_C(d)`. By ChainMembershipForOrigin (ASN-0093), the only content-store elements with `origin(·) = d` are chain elements of `A_C(d)`, and cross-origin elements of `dom(Σ_k.C)` are distinct from `a_k` by SubAllocatorAxiom.Disjointness (ASN-0047) — `dom(A_C(d)) ∩ dom(A_C(d')) = ∅` for `d ≠ d'`. Combined with FirstEmissionFreshness (ASN-0093) for the boundary case `m_d = 0`, the first conjunct is discharged.

The `a_k ∉ dom(Σ_k.L)` clause is discharged by subspace separation. By SubAllocatorAxiom.Subspace (ASN-0047), `a_k` is produced by `A_C(d)` and so satisfies `subspace_I(a_k) = s_C`; every `ℓ ∈ dom(Σ_k.L)` satisfies `subspace_I(ℓ) = s_L` by L0 (SubspacePartition; ASN-0047); and `s_C ≠ s_L` by SC-NEQ (ASN-0093). Hence `a_k ∉ dom(Σ_k.L)`. (This conclusion is consistent with L14, StoreDisjointness; ASN-0093, and with DisjointSubAllocatorChains; ASN-0093 — both follow from the same subspace separation — but neither directly entails the clause for `a_k` since `a_k ∉ dom(Σ_k.C)` already, so L14's per-state disjointness at `Σ_k` carries no constraint between `a_k` and `dom(Σ_k.L)`.)

Both conjuncts together discharge K.α's freshness precondition at each of the `n` firings.

By the chain discipline (ChainPrefixExtension, ChainEnumerationInjectivity; ASN-0093), every `a_k` has `origin(a_k) = d`, satisfies `b_C(d) ≼ a_k` (extending the content sub-allocator anchor), and is structurally produced by the sub-allocator's `inc(·, 0)` chain. The addresses `a_0, a_1, …, a_{n−1}` form a contiguous initial-segment extension of the chain: `a_{k+1} = inc(a_k, 0)` for `0 ≤ k < n − 1`, and `a_0` is either `[d.0.s_C.1]` (if `d` had no prior content emissions, per K.α's first-emission predicate in ASN-0093) or `inc(a_prev, 0)` where `a_prev = max{a ∈ dom(Σ.C) : origin(a) = d}` (per K.α's subsequent-emission predicate in ASN-0093).

The post-state content store:

  `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}`
  `C'(a_k) = v_k` for `0 ≤ k < n`
  `C'(a) = C(a)` for `a ∈ dom(C)`

The third clause is the most important. The pre-existing content is *not touched*. Its values are preserved bit-for-bit; its addresses persist in the post-state. This is the foundational permanence guarantee S0.

### Effect Two: Placement

The new I-addresses must appear at V-positions `p, shift(p, 1), …, shift(p, n−1)`. Reading `shift(p, 0) = p` per OrdinalShiftBase (ASN-0058), the mapping is exact:

  `(A k : 0 ≤ k < n : M'(d)(shift(p, k)) = a_k)`

By OrdAddHom clause (b) (ASN-0036) applied to `w = δ(k, m_C)`, every `shift(p, k)` for `k ≥ 1` lies in the same subspace as `p`: `subspace(shift(p, k)) = s_C`. The result-length identity of TumblerAdd (ASN-0034) gives `#shift(p, k) = m_C`. For `k = 0`, `shift(p, 0) = p` shares subspace and depth with `p` trivially. Each `shift(p, k)` satisfies S8a (VPositionWellFormedness, ASN-0036): zero-free, depth `≥ 2`, all components positive. The justification routes through `p`'s own S8a, which is supplied by the insertion-position precondition directly — `ValidInsertionPosition` postcondition (b) (ASN-0036) in the non-empty case, or `ValidFirstInsertionPosition` postcondition (b) (ASN-0036) in the empty case. Both predicates assert S8a as their (b) postcondition unconditionally; the set-membership characterisation `p ∈ V_{s_C}(d) ∪ {[s_C, 1, …, 1]}` would fail for the append case (`p_m = N + 1` places `p` outside both `V_{s_C}(d) = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ N}` and the singleton `{[s_C, 1, …, 1]}` unless `N = 0`), so we appeal to the predicates' postconditions directly. The shift's tail component `p_{m_C} + k ≥ 1` then transfers S8a to `shift(p, k)`: zeros remain zero (the leading components of `p` are `1` by ValidInsertionPosition/ValidFirstInsertionPosition postcondition (d), and the tail is positive), depth is preserved at `m_C ≥ 2`, all components remain strictly positive. The new V-positions are well-formed inhabitants of `V_{s_C}(d')`.

### Effect Three: Shift

Every existing V-position `v ∈ V_{s_C}(d)` with `v ≥ p` must remap. The content there does not change — it keeps its I-address — but its V-position advances by `n`:

  `(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p :: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

This clause is exactly the I3 postcondition (PostInsertionShift) of ASN-0082, instantiated for the text subspace `S = s_C` of `d`. I3's preconditions are discharged as follows: (i) `d` is a document — from INSERT's precondition `d ∈ dom(M)`; (ii) `M(d) : T ⇀ T` — from the substrate's typing of `M(d)`; (iii) `#p ≥ 2 ∧ subspace(p) = S ≥ 1` — from INSERT's preconditions `subspace(p) = s_C` (with `s_C ≥ 1` by SubspaceConventionAxiom, ASN-0093) and `#p = m_C ≥ 2` (in the non-empty case, `m_C ≥ 2` follows from pre-state S8a, ASN-0036, on `V_{s_C}(d)`; in the empty case, the caller's chosen `m ≥ 2` enters directly); (iv) depth-compatibility — `(V_{s_C}(d) ≠ ∅ ⟹ #p = #v` for any `v ∈ V_{s_C}(d))` — from S8-depth (ASN-0036) fixing `#v = m_C` across `V_{s_C}(d)` and INSERT's `#p = m_C`, with the implication vacuous in the empty case; (v) `n ≥ 1` — matches INSERT's precondition. The right region is the source of the shift; the shifted-right region is its image. The two are related by the order-preserving (TS1, ShiftOrderPreservation; ASN-0034) and injective (TS2, ShiftInjectivity; ASN-0034) shift map. The image of the shift map is exactly `{[s_C, 1, …, 1, k + n] : p_m ≤ k ≤ N}` when we write `p = [s_C, 1, …, 1, p_m]` with `p_m ∈ {1, …, N+1}`.

ASN-0082's `M'(d)` and INSERT's `M'(d)` agree exactly on the shift-image positions because both apply the same shift rule on the Right region; INSERT additionally introduces Insertion positions `shift(p, k)` for `0 ≤ k < n` that are disjoint from the shift-images (by the pairwise-disjointness argument below for S2). I3 establishes the shift-image clause unchanged in either model; the Insertion positions are an additional, independent contribution that INSERT specifies and ASN-0082's model omits.

**Scope of ASN-0082's I3 against INSERT's post-state.** ASN-0082 specifies a *shift-only* operation whose post-state is structurally smaller than INSERT's: ASN-0082's `M'(d)` covers Left, Shifted-right, and cross-subspace positions only, with no Insertion region. Three of I3's sibling postconditions (I3-V, I3-CS, I3-CX) characterise that shift-only `M'(d)` in ways that *fail* if read literally as predicates on INSERT's `M'(d)`:

- *I3-V (PostInsertionVacating).* I3-V quantifies over `v ∈ dom(M(d))` (pre-state positions) with `subspace(v) = S` and `v ≥ p` that are not the image of any pre-state shift, concluding `v ∉ dom(M'(d))`. The conflict with INS.M-insert arises precisely at Insertion positions `shift(p, k)` that *coincide with pre-state positions* — concretely, those with `k ≤ N − p_m` in the non-empty case, since `shift(p, k) = [s_C, 1, …, 1, p_m + k]` is a pre-state position iff `p_m + k ≤ N`. For each such coinciding position, I3-V's "not a shift image" hypothesis is satisfied (`shift(p, k) ≠ shift(u, n)` for any `u ≥ p`, since `shift(u, n)` has last component `u_m + n ≥ p_m + n > p_m + k`), forcing `shift(p, k) ∉ dom(M'(d))` and directly contradicting INS.M-insert. The append case (`p_m = N + 1`, where `N − p_m = −1` admits no valid `k`) and the empty case (`V_{s_C}(d) = ∅`, where I3-V's pre-state quantifier ranges over the empty set) produce no such coincidences and are unaffected by I3-V's quantifier; only the beginning and interior cases (`p_m ≤ N`) exhibit the conflict, and they do so only at the specific Insertion positions identified above.
- *I3-CS (PostInsertionDomainClosureSubspace).* I3-CS asserts that every position in `dom(M'(d))` within subspace `S` is either a pre-state position with `v < p` or a shift `shift(u, n)` of a pre-state `u ≥ p`. Applied to INSERT, this would again exclude the Insertion positions — they are neither pre-state nor shift-images of pre-state positions.
- *I3-CX (PostInsertionDomainClosureCross).* I3-CX asserts that every position in `dom(M'(d))` in a subspace other than `S` was already in `dom(M(d))`. This clause does hold of INSERT's `M'(d)` (INSERT adds no positions outside `s_C`), but it is a redundant statement of the cross-subspace frame, not an additional contribution.

This ASN cites ASN-0082's I3 only for its positive shift clause and the affirmative companion lemmas (I3-L, I3-X, I3-D, I3-C, I3-VD, I3-VP, I3-fin, I3-S2, I3-S3, I3-S7) that govern the regions ASN-0082's model does cover. I3-V, I3-CS, and the redundant I3-CX are *disclaimed*: they describe a hypothetical shift-only operation whose post-state is properly contained in INSERT's, and they do not hold of INSERT's `M'(d)`. The Insertion region's contribution to each invariant is verified independently below, alongside the shift-only contributions inherited from I3.

For positions `v ∈ V_{s_C}(d)` with `v < p` (the left region), the arrangement is unchanged (I3-L, PostInsertionLeftFrame; ASN-0082).

For positions in subspaces other than `s_C` — including the link subspace — the arrangement is unchanged (I3-X, PostInsertionCrossSubspaceFrame; ASN-0082).

For other documents `d' ≠ d`, the arrangement is unchanged (I3-D, PostInsertionCrossDocumentFrame; ASN-0082).

Pre-existing content store entries are preserved pointwise — every `a ∈ dom(C)` has `a ∈ dom(C')` with `C'(a) = C(a)` (S0, ContentImmutability; ASN-0036, and P0, ContentPermanence; ASN-0047) — discharged by INS.C's third clause. INSERT extends `dom(C)` by the freshly allocated addresses (Effect One), so the store itself is *not* unchanged; ASN-0082's I3-C (PostInsertionContentFrame), asserting exact equality `Σ'.C = Σ.C` for its shift-only model, is strictly stronger than INSERT's content frame and is not preserved here.

These exhaust the cases.

## The Operation: Formal Contract

INSERT is a **substrate composite** in the sense of ValidComposite★ (ASN-0047) — a finite sequence of elementary transitions drawn from the substrate's K-vocabulary, governed at the composite boundary by the coupling constraints J0, J1★, J1'★. It is *not* a new elementary primitive; the substrate transition vocabulary is not amended.

The operative substrate is ValidComposite★ (ASN-0047), whose vocabulary is `{K.α (amended), K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻ (amended), K.μ~, K.ρ}`. Document registration in this framework is K.δ in its IsDocument sub-case. The K.σ operation introduced in ASN-0093 is the document-registration primitive of that ASN's standalone substrate formulation — distinct from, and not composed with, ValidComposite★. Where this ASN cites ASN-0093 (for ChainEnumerationInjectivity, FirstEmissionFreshness, SubAllocatorAxiom, etc.), it draws on ASN-0093's lemmas about allocator chains, not its standalone composite vocabulary. INSERT itself is governed entirely by ValidComposite★ and admits no K.σ firing.

We state INSERT as a composite `Σ →* Σ'`.

**Operation:** `INSERT(d, p, ⟨v_0, …, v_{n−1}⟩)`

**Substrate Decomposition.** INSERT realises as the following sequence of elementary transitions, in order:

1. **`n` successive K.α firings** allocating fresh content addresses `a_0, a_1, …, a_{n−1}` from `A_C(d)`. Each K.α firing satisfies its freshness precondition against the intermediate state immediately preceding it (justified by ChainEnumerationInjectivity; ASN-0093 — see Effect One above).
2. **One K.μ⁻ on `d`** retaining the Left prefix of `V_{s_C}(d)` (with `n'_{s_C} = p_m − 1`) and retaining all of `V_{s_L}(d)` (with `n'_{s_L} = n_{s_L}`). The canonical decomposition omits this step in three cases, distinguished by whether the omission is *forced* (no admissible K.μ⁻ firing exists under the canonical retention parameters and INSERT's frame) or a *canonical-decomposition choice* (an alternative decomposition with different K.μ⁻ retention parameters could fire K.μ⁻ and reach the same Σ' via a subsequent K.μ⁺ rebuild, but the canonical decomposition omits K.μ⁻ for parsimony):

   *(i.a) — Forced by precondition.* When both `V_{s_C}(d) = ∅` and `V_{s_L}(d) = ∅`, `dom(M(d)) = ∅` and K.μ⁻'s precondition fails. K.μ⁻ cannot fire under any decomposition.

   *(i.b) — Forced omission.* When `V_{s_C}(d) = ∅` and `V_{s_L}(d) ≠ ∅`, K.μ⁻'s `dom(M(d)) ≠ ∅` precondition holds, but `n_{s_C} = 0` forces the content-subspace retention parameter `n'_{s_C} ∈ {0, …, 0}` to equal `n_{s_C}`, foreclosing strict shrinkage in `s_C`. K.μ⁻'s strict-shrinkage clause `(E S :: n'_S < n_S)` therefore reduces to `n'_{s_L} < n_{s_L}`, and any such firing shrinks `V_{s_L}(d)`, violating INS.frame.subspace at the composite boundary. So no admissible K.μ⁻ firing strictly shrinks `s_C` while preserving `s_L`, and K.μ⁻ is omitted — matching case (i.a)'s forced omission, with the same effect as case (ii)'s reduction of the strict-shrinkage clause to `s_L`. The Insertion region is added by step 3's K.μ⁺ alone, leaving `V_{s_L}(d)` untouched.

   *(ii) — Canonical-decomposition choice (both `V_{s_L}(d) ≠ ∅` and `V_{s_L}(d) = ∅` sub-cases).* When `p_m = N + 1` (append case — Left = entire pre-state `V_{s_C}(d)`), the canonical retention `n'_{s_C} = N = n_{s_C}` forecloses strict shrinkage in `s_C` *under the canonical parameters*, so the strict-shrinkage clause `(E S :: n'_S < n_S)` reduces, under the canonical retention, to `n'_{s_L} < n_{s_L}`. Under the canonical retention this leaves no admissible K.μ⁻ firing consistent with INSERT's frame (when `V_{s_L}(d) ≠ ∅`, the only admissible firing shrinks `s_L` and violates INS.frame.subspace; when `V_{s_L}(d) = ∅`, the only admissible firing requires `n'_{s_L} < n_{s_L} = 0`, which has no solution in ℕ). However, the canonical retention is not the only available choice: an alternative decomposition could fire K.μ⁻ with `n'_{s_C} < N` (admissible by K.μ⁻'s precondition, since case (ii)'s defining condition `p_m = N + 1 ≥ 2` requires `N ≥ 1`, so `s_C` is non-empty) and `n'_{s_L} = n_{s_L}` (preserving the link subspace). This alternative satisfies K.μ⁻'s strict-shrinkage clause via `s_C` alone, and is admissible identically in both sub-cases: the `V_{s_L}(d) = ∅` sub-case sets `n'_{s_L} = n_{s_L} = 0` trivially, and the `V_{s_L}(d) ≠ ∅` sub-case sets `n'_{s_L} = n_{s_L}` to preserve `s_L`. A subsequent K.μ⁺ then re-adds the discarded `s_C` positions before adding Insertion (K.μ⁺'s content-subspace restriction admits these additions), reaching the same Σ'. The omission of K.μ⁻ in case (ii) is therefore a canonical-decomposition parsimony choice in both sub-cases — the alternative decomposition is admissible under K.μ⁻ + K.μ⁺ for both — rather than a forced consequence of either sub-case.
3. **One K.μ⁺ on `d`** adding *exactly* the Insertion V-positions (mapping `shift(p, k) ↦ a_k` for `0 ≤ k < n`) and the Shifted-right V-positions (mapping `shift(v, n) ↦ M(d)(v)` for each `v ∈ V_{s_C}(d)` with `v ≥ p`), and no other V-positions in subspace `s_C`. This is a *contract-level constraint* on step 3, not an entailment of K.μ⁺'s vocabulary precondition: K.μ⁺'s precondition (ASN-0047) is permissive — it admits any new V-positions in `s_C` with images in `dom(C)` provided the resulting `M'(d)` satisfies D-CTG★ and D-MIN★. INSERT's contract restricts this freedom by mandating that step 3's K.μ⁺ firing add *precisely* the Insertion and Shifted-right V-positions enumerated above and no additional `s_C` positions. The exhaustiveness clause (INS.M-exhaustive) is derived from this contract-level constraint plus step 2's removal of the Right region: K.μ⁻ retains exactly the Left prefix (when it fires) or leaves the pre-state intact (when omitted, the Right region of `V_{s_C}(d)` is empty by the case-routing analysis), and step 3's constrained K.μ⁺ adds precisely Insertion and Shifted-right. By construction the post-state `V_{s_C}(d') =` Left ∪ Insertion ∪ Shifted-right. All additions in step 3 are in subspace `s_C`, as required by K.μ⁺'s content-subspace restriction (ASN-0047), and are exactly the positions enumerated by INS.M-insert and INS.M-shift.
4. **`n` successive K.ρ firings** recording provenance pairs `(a_k, d)` for `0 ≤ k < n`.

Each intermediate state in this sequence satisfies the per-state invariants (Class (a) of ASN-0047); the composite-boundary properties (Class (b): P4★, P4a, P7a) are discharged at the boundary `Σ →* Σ'` by the constraints J0, J1★, J1'★.

**State Preconditions** (evaluated against the operation's pre-state Σ):
- `d ∈ dom(M)` (so K.α, K.μ⁺, K.ρ all have their `d ∈ E_doc` precondition met; K.μ⁻ when fired further requires `dom(M(d)) ≠ ∅`, satisfied in cases that invoke it)
- `subspace(p) = s_C`
- `#p = m_C` (the common depth of `V_{s_C}(d)` if non-empty per S8-depth, ASN-0036; the caller's chosen depth `m ≥ 2` if empty)
- `p` is a valid insertion position: either `ValidInsertionPosition(d, p)` (ASN-0036) for non-empty `V_{s_C}(d)` — equivalently `p ∈ {shift(min(V_{s_C}(d)), j) : 0 ≤ j ≤ |V_{s_C}(d)|}` reading `shift(t, 0) = t` per OrdinalShiftBase (ASN-0058) — or `ValidFirstInsertionPosition(d, p, m)` (ASN-0036) for empty `V_{s_C}(d)`, equivalently `p = [s_C, 1, …, 1]` of depth `m`
- `n ≥ 1`
- `v_k ∈ Val` for each `0 ≤ k < n`

**Environmental Assumptions** (properties of the substrate execution environment, not of the pre-state):
- **Composite atomicity.** No elementary transition of any other composite interleaves between INSERT's elementaries that touches the resources INSERT depends on. The required atomicity scope is precisely two-fold: (i) `A_C(d)`'s chain emission state — concretely, the set `{a ∈ dom(C) : origin(a) = d}` consulted by K.α's subsequent-emission predicate to determine the next chain element — must not advance between INSERT's K.α firings, and (ii) `M(d)`'s text subspace `V_{s_C}(d)` must not be modified between INSERT's elementaries. SequentialTransitionAxiom (ASN-0093) supplies elementary-level atomicity (each individual elementary transition is uninterruptible), but composite-level atomicity over these specific resources is a stronger property the substrate environment must provide. Where the atomicity is violated on (i) or (ii) — concurrent INSERTs on the same document, for example — the chain index `m_d` consulted by K.α can advance mid-composite via another composite's K.α on the same `A_C(d)`, or the text-subspace arrangement can shift mid-composite, and the freshness and placement arguments above no longer determine the post-state from the operation's pre-state alone. The post-state in that case is governed by the actually-committed transitions, not by the contract specified here. Concurrent operations *outside* this required atomicity scope are admissible: concurrent K.λ firings (affecting `A_L(d)`'s chain and `dom(L)`) do not interfere because every `a_k` produced by `A_C(d)` satisfies `subspace_I(a_k) = s_C`, disjoint from K.λ's link emissions by L0 + SC-NEQ (ASN-0047, ASN-0093); concurrent K.μ⁺_L or K.μ⁻ on `M(d)`'s link subspace do not interfere because INSERT modifies only the text subspace; and concurrent operations on any document `d' ≠ d` do not interfere by SubAllocatorAxiom.Disjointness and the cross-document frame.

The distinction matters for backward reasoning: wp-style derivation of INSERT's preconditions applies to state preconditions, which are predicates on Σ. The composite-atomicity environmental assumption is not such a predicate — it constrains the substrate's execution model, not the state — and so it sits outside the wp calculus. An implementation must establish it by construction (single-threaded serialisation, per-document locking restricted to `d`'s text-subspace arrangement and content sub-allocator chain `A_C(d)`, or any other mechanism preventing inter-composite elementary interleaving over the two resources named in (i) and (ii) above).

**Effect — Content Store:**
Let `a_0, a_1, …, a_{n−1}` denote the `n` successive emissions of `A_C(d)` produced by the K.α firings of step 1. Then:

  `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}`
  `(A k : 0 ≤ k < n : C'(a_k) = v_k)`
  `(A a : a ∈ dom(C) : C'(a) = C(a))`

**Effect — Arrangement of `d`, text subspace:**
Three disjoint regions:

  *Left* — `(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v < p :: v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`

  *Insertion* — `(A k : 0 ≤ k < n :: shift(p, k) ∈ dom(M'(d)) ∧ M'(d)(shift(p, k)) = a_k)` — reading `shift(p, 0) = p` per OrdinalShiftBase (ASN-0058).

  *Shifted right* — `(A v : v ∈ dom(M(d)) ∧ subspace(v) = s_C ∧ v ≥ p :: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v))`

  *Exhaustiveness* (INS.M-exhaustive) — `(A v : v ∈ dom(M'(d)) ∧ subspace(v) = s_C :: v ∈ Left ∪ Insertion ∪ Shifted-right)`, where Left, Insertion, and Shifted-right denote the three V-position sets defined by the per-region clauses above. Equivalently, `V_{s_C}(d') =` Left positions ∪ Insertion positions ∪ Shifted-right positions, with no additional `s_C` positions in the post-state.

The exhaustiveness clause follows from the substrate decomposition by case analysis on whether K.μ⁻ fires. When K.μ⁻ fires (the canonical interior and `j = 0` cases), it retains exactly the Left prefix of `V_{s_C}(d)` and removes the Right region; step 3's K.μ⁺ then adds *precisely* the Insertion and Shifted-right positions and no others, by the contract-level constraint on step 3 stated above (K.μ⁺'s permissive vocabulary precondition admits additional `s_C` positions, but INSERT's contract narrows the admitted firings to those adding exactly Insertion ∪ Shifted-right). The post-state therefore satisfies `V_{s_C}(d') =` Left ∪ Insertion ∪ Shifted-right by direct union. When K.μ⁻ is omitted (cases i.a, i.b, ii of the substrate decomposition), the pre-state `V_{s_C}(d)` positions are preserved unchanged because no other elementary step removes them: K.α and K.ρ have frame `(A d :: M'(d) = M(d))` (ASN-0047), and K.μ⁺ is purely extending (its precondition mandates `dom(M'(d)) ⊃ dom(M(d))` with image preservation on the existing domain). Step 3's K.μ⁺ adds precisely the Insertion and Shifted-right positions, both of which lie in subspace `s_C`. In each K.μ⁻-omitted case the Right region of the pre-state `V_{s_C}(d)` — the set `{v ∈ V_{s_C}(d) : v ≥ p}` — is empty: cases (i.a) and (i.b) have `V_{s_C}(d) = ∅`, so no V-position satisfies `v ≥ p`; case (ii) has `p_m = N + 1`, so no `v ∈ V_{s_C}(d)` (with last components in `{1, …, N}`) satisfies `v ≥ p`. The preserved pre-state positions are therefore exactly the Left region, and the post-state Shifted-right region is correspondingly empty, so again `V_{s_C}(d') =` Left ∪ Insertion ∪ Shifted-right. The S2 functionality argument in §Arrangement functionality below depends on this exhaustiveness — pairwise disjointness of Left, Insertion, and Shifted-right closes only because no fourth region of `s_C` positions exists in the post-state.

**Effect — Provenance:**

  `R' = R ∪ {(a_k, d) : 0 ≤ k < n}`

The composite-boundary coupling J1★ (ExtensionRecordsProvenanceContentSubspace; ASN-0047) requires every newly-arranged content-subspace I-address to have its provenance pair in `R'`. For Insertion positions, the K.α-allocated `a_k` is freshly placed and was not previously in `ran(M(d))`, so J1★ requires `(a_k, d) ∈ R'` — discharged by step 4. For Shifted-right positions, `M(d)(v) = a` was already in `ran(M(d))` at the pre-state, so J1★ imposes no obligation. Conversely, J1'★ (ProvenanceRequiresExtensionContentSubspace; ASN-0047) requires every new `R'` entry to correspond to a newly-arranged content-subspace I-address — discharged because each `(a_k, d)` is added in step 4 precisely as `a_k` is placed by step 3's K.μ⁺ at a content-subspace V-position. J0 (AllocationRequiresPlacement; ASN-0047) requires every newly allocated `a_k ∈ dom(C') \ dom(C)` to be placed in some `M'(d')`'s range — discharged by step 3's K.μ⁺ placing each `a_k` at `shift(p, k)`.

**Frame Conditions:**
- `L' = L`. The link store is unchanged: no K.λ fires in the decomposition, so `dom(L)` and every link value persist by L12 (LinkImmutability; ASN-0093).
- `E' = E`. The entity set is unchanged: no K.δ fires in the decomposition (`dom(M)` is governed via K.δ-IsDocument under ValidComposite★; INSERT registers no new document and creates no new node, account, or non-document entity).
- `dom(M') = dom(M)`. As a specialisation of `E' = E` for the document subset: no new document is registered.
- `(A d' : d' ∈ dom(M) ∧ d' ≠ d : M'(d') = M(d'))`. Other documents' arrangements are unchanged (K.α, K.μ⁻, K.μ⁺, K.ρ all carry `(A d' : d' ≠ d :: M'(d') = M(d'))` as their explicit per-step frame in ASN-0047).
- `{v ∈ dom(M'(d)) : subspace(v) ≠ s_C} = {v ∈ dom(M(d)) : subspace(v) ≠ s_C} ∧ (A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ s_C : M'(d)(v) = M(d)(v))`. Other subspaces of `d` — in particular `V_{s_L}(d)` — are unchanged both as sets (no new non-`s_C` positions appear in `dom(M'(d))`, and no existing ones are removed) and pointwise (existing mappings preserve their images). Step 2's K.μ⁻ (when fired) preserves the link subspace by `n'_{s_L} = n_{s_L}`; step 3's K.μ⁺ adds only content-subspace V-positions (per the K.μ⁺ amendment in ASN-0047), so the set-equality direction holds in both directions.

## A Worked Example

We instantiate INSERT to make the three regions concrete.

**Interior insertion.** Let `d` be a document with `V_{s_C}(d) = {[1,1], [1,2], [1,3], [1,4], [1,5]}` (so `m_C = 2`, `N = 5`), with arrangement:

  `M(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [1,3] ↦ a₃, [1,4] ↦ a₄, [1,5] ↦ a₅}`

Invoke `INSERT(d, [1,3], ⟨v₀, v₁⟩)` with `n = 2`. The position `p = [1,3]` corresponds to `j = 2` (since `shift([1,1], 2) = [1,3]`), interior to the `N + 1 = 6` valid positions. The substrate composite fires:

1. **Two K.α firings.** A_C(d) emits `a_{new0}` and `a_{new1} = inc(a_{new0}, 0)`, both fresh.
2. **K.μ⁻ on `d`** retains the Left prefix `V_{s_C}(d)` with `n'_{s_C} = 2`: post-step the text-subspace is `{[1,1], [1,2]}`. Link subspace retained at `n'_{s_L} = n_{s_L}`.
3. **K.μ⁺ on `d`** adds five V-positions: `[1,3] ↦ a_{new0}` and `[1,4] ↦ a_{new1}` (Insertion), and `[1,5] ↦ a₃`, `[1,6] ↦ a₄`, `[1,7] ↦ a₅` (Shifted right).
4. **Two K.ρ firings** record `(a_{new0}, d)` and `(a_{new1}, d)` in R.

The post-state arrangement:

  `M'(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [1,3] ↦ a_{new0}, [1,4] ↦ a_{new1}, [1,5] ↦ a₃, [1,6] ↦ a₄, [1,7] ↦ a₅}`

Verifying the three regions:
- *Left:* `{[1,1] ↦ a₁, [1,2] ↦ a₂}` — matches `{v < p}` via INS.M-left.
- *Insertion:* `{[1,3] ↦ a_{new0}, [1,4] ↦ a_{new1}}` — matches `shift(p, k) ↦ a_k` for `k ∈ {0, 1}` via INS.M-insert; note `shift([1,3], 0) = [1,3]` by OrdinalShiftBase.
- *Shifted right:* `{[1,5] ↦ a₃, [1,6] ↦ a₄, [1,7] ↦ a₅}` — matches `shift(v, 2) ↦ M(d)(v)` for `v ∈ {[1,3], [1,4], [1,5]}` via INS.M-shift.

The last-component values in `V_{s_C}(d')` are `{1, 2, 3, 4, 5, 6, 7}` — sequential, contiguous, starting at 1, satisfying INS.inv.seq with new cardinality `N + n = 7`.

*Projection-shift correspondence (INS.proj).* Suppose a link `ℓ ∈ dom(L)` has a slot with endset `e_1` delivered by the canonical span `(a_2, δ(3, #a_2))`, whose coverage is the half-open tumbler interval `coverage(e_1) = [a_2, a_5)` (since `a_5 = a_2 ⊕ δ(3, #a_2)`; ASN-0098). This interval strictly contains `{a₂, a₃, a₄}` — by T5 (ASN-0034) it also holds every descendant of `a₂, a₃, a₄`. The quantity that equals the three-element set is the *intersection with the range*: `coverage(e_1) ∩ ran(M(d)) = {a₂, a₃, a₄}`, the three I-addresses of the pre-state range that fall in the interval. **Tightness precondition of the trace below, grounded in the example's substrate state.** We construct `Σ_{e_1}` — the state at which `e_1` was incorporated into `ℓ` via K.λ — concretely. Let `Σ_{e_1}` be the substrate state of `d` immediately after `M(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [1,3] ↦ a₃, [1,4] ↦ a₄, [1,5] ↦ a₅}` had been established (the pre-state of our INSERT) and *before* any subsequent K.α firing of INSERT advances `A_C(d)`'s chain. At `Σ_{e_1}`, the content addresses `a₁, a₂, a₃, a₄, a₅ ∈ dom(Σ_{e_1}.C)` are all present — they were placed there by prior K.α firings constituting the chain of `A_C(d)` (per ChainMembershipForOrigin; ASN-0093), with structural form `aᵢ = [d.0.s_C.i]` for `1 ≤ i ≤ 5`. The endset `e_1`'s delivering span `(a_2, δ(3, #a_2))` has start `a_2 ∈ dom(Σ_{e_1}.C)`, width `δ(3, #a_2)` of length `#a_2 = #d + 3` (so the action point equals the length — canonical), and reach `a_2 ⊕ δ(3, #a_2) = a_5`. By LP-Fin Corollary (CanonicalIntervalCharacterisation; ASN-0098), the F-candidates in the half-open interval `[a_2, a_2 ⊕ δ(3, #a_2))` are exactly `{[d.0.s_C.2], [d.0.s_C.3], [d.0.s_C.4]} = {a_2, a_3, a_4}`. All three are members of `dom(Σ_{e_1}.C)` by construction. Therefore the tightness conditions of ASN-0098 hold: the span is canonical (width is `δ(3, #a_2)`), the start lies in `dom(Σ_{e_1}.C) ∪ dom(Σ_{e_1}.L)`, and every F-candidate in the interval lies in `dom(Σ_{e_1}.C) ∪ dom(Σ_{e_1}.L)`. We conclude `tight(e_1, Σ_{e_1})` (ASN-0098). This is the load-bearing assumption that makes `N_I = ∅` concrete via LP19a (TightFreshness; ASN-0098); we trace the non-tight alternative at the end of this example. We trace the projection through the composite.

Pre-state `project(ℓ, 1, d, Σ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e_1)} = {[1,2], [1,3], [1,4]}`, since the I-addresses of `ran(M(d))` lying in `coverage(e_1) = [a_2, a_5)` are exactly `coverage(e_1) ∩ ran(M(d)) = {a₂, a₃, a₄}`. Partition into regions relative to `p = [1,3]`: `P_0^L = {[1,2]}` (the single position with `v < p`); `P_0^R = {[1,3], [1,4]}` (positions with `v ≥ p`); `P_0^{s_L} = ∅` (the link subspace is empty for this example).

Step 1 (K.α firings): `Σ.M(d)` unchanged, projection unchanged at `{[1,2], [1,3], [1,4]}` by LP6.

Step 2 (K.μ⁻): `V_{s_C}(d_intermediate) = {[1,1], [1,2]}`. The projection contracts to `P_0 ∩ R_kept = {[1,2]}` by LP10 — the Right contributions `[1,3]` and `[1,4]` temporarily disappear.

Step 3 (K.μ⁺): adds Insertion positions `{[1,3] ↦ a_{new0}, [1,4] ↦ a_{new1}}` and Shifted-right positions `{[1,5] ↦ a₃, [1,6] ↦ a₄, [1,7] ↦ a₅}`. By LP9, the new projection contributions are exactly those new V-positions whose image lies in `coverage(e_1) = [a_2, a_5)`. Among Insertion: by LP19a (TightFreshness; ASN-0098) applied to the tightness assumption `tight(e_1, Σ_{e_1})`, the freshly allocated `a_{new0}, a_{new1}` cannot lie in `coverage(e_1)` — so `a_{new0}, a_{new1} ∉ coverage(e_1)` and `N_I = ∅`. Among Shifted-right: `a₃, a₄ ∈ coverage(e_1)` (both lie in `[a_2, a_5)`) but `a₅ ∉ coverage(e_1)` (it is the exclusive upper bound), so `N_S = {[1,5], [1,6]}`.

The projection grows to `{[1,2]} ∪ ∅ ∪ {[1,5], [1,6]} = {[1,2], [1,5], [1,6]}`.

Step 4 (K.ρ firings): projection unchanged by LP14.

Post-state `project(ℓ, 1, d, Σ') = {[1,2], [1,5], [1,6]}`. Apply the region-aware shift map `π`: π is identity on `P_0^L = {[1,2]}`, giving `{[1,2]}`; π is `shift(·, 2)` on `P_0^R = {[1,3], [1,4]}`, giving `{[1,5], [1,6]}`. The combined image `π(project(ℓ, 1, d, Σ)) = {[1,2], [1,5], [1,6]}` matches `project(ℓ, 1, d, Σ')` exactly. Since `N_{ℓ,1} = N_I = ∅` in this tight-endset case, INS.proj's general form `π(project) ∪ N_{ℓ,i}` resolves to `π(project)`. The projection has shifted with the content; the link has tracked it.

*Non-tight alternative.* If `tight(e_1, Σ_{e_1})` (ASN-0098) does not hold, LP19a does not apply, and a freshly allocated `a_{new0}` or `a_{new1}` may land in `coverage(e_1)`. ASN-0098's tight definition distinguishes two failure modes. *Failure mode (a) — non-canonical span:* `e_1` is incorporated with a span `(s, ℓ_w)` whose width `ℓ_w` is not an ordinal displacement of length `#s` (i.e., not of the form `δ(n, #s)` for any `n ≥ 1`). Such spans are unconditionally non-tight: LP-Fin (IntervalFinitude; ASN-0098) gives `|F ∩ [s, s ⊕ ℓ_w)| = ℵ₀`, so no finite `dom(Σ_{e_1}.C) ∪ dom(Σ_{e_1}.L)` can satisfy tightness's F-candidate-coverage clause. *Failure mode (b) — F-candidate gap:* `e_1` is incorporated with a canonical span `(s, δ(n, #s))`, but some F-candidate in `[s, s ⊕ δ(n, #s))` is missing from `dom(Σ_{e_1}.C) ∪ dom(Σ_{e_1}.L)`. Concretely for this example: suppose `e_1` is delivered by the canonical span `(a_2, δ(3, #a_2))` with `coverage(e_1) = [a_2, a_5)`, but `a_4` had not yet been allocated at the state `Σ_{e_1}` of `e_1`'s incorporation. Then `a_4 ∈ F ∩ [a_2, a_2 ⊕ δ(3, #a_2))` is missing from `dom(Σ_{e_1}.C)`, making the span non-tight under mode (b). In either failure regime, LP19a is inapplicable and `N_I ⊆ {[1,3], [1,4]}` may be non-empty, with each `[1, 3 + k]` contributing iff `a_{new k} ∈ coverage(e_1)`. The post-state `project(ℓ, 1, d, Σ') = {[1,2], [1,5], [1,6]} ∪ N_I` could include up to two additional positions. The INS.proj general form `π(project) ∪ N_{ℓ,i}` captures both regimes; the tight case is the special simplification with `N_I = ∅`.

*Discoverability (INS.inv.discov).* Pre-state `discoverable_from(ℓ, d, Σ)` holds because the projection was non-empty. Post-state `project(ℓ, 1, d, Σ') = {[1,2], [1,5], [1,6]} ≠ ∅`, so `discoverable_from(ℓ, d, Σ')` also holds. The link is preserved across the operation; the coverage targets `{a₂, a₃, a₄}` are still in `ran(M'(d)) = {a₁, a₂, a_{new0}, a_{new1}, a₃, a₄, a₅}`.

*Provenance discharge (J1★, J1'★).* Pre-state `R` need not contain `(a_{new0}, d)` or `(a_{new1}, d)`, since `a_{new0}` and `a_{new1}` are freshly allocated by step 1's K.α firings and were not in `dom(Σ.C)`. Post-state `R' = R ∪ {(a_{new0}, d), (a_{new1}, d)}` by step 4's two K.ρ firings. We trace the boundary obligations:
- *J1★ (ExtensionRecordsProvenanceContentSubspace).* For each I-address `a` in `ran(M'(d))` that was not in `ran(M(d))` via a content-subspace V-position pre-state: the freshly allocated `a_{new0}` and `a_{new1}` are newly placed at `[1,3]` and `[1,4]` respectively (Insertion region). J1★ requires `(a_{new0}, d), (a_{new1}, d) ∈ R'` — discharged. For Shifted-right placements `[1,5] ↦ a₃, [1,6] ↦ a₄, [1,7] ↦ a₅`: each I-address `a₃, a₄, a₅` was already in `ran(M(d))` via the pre-state content-subspace V-positions `[1,3], [1,4], [1,5]`, so J1★ imposes no obligation (the pair `(a_k, d)` for `k ∈ {3,4,5}` is already in `R` by pre-state P4★).
- *J1'★ (ProvenanceRequiresExtensionContentSubspace).* For each new R'-entry `(a_{new0}, d), (a_{new1}, d)`: a corresponding newly-arranged content-subspace I-address exists at `[1,3]` and `[1,4]` respectively — discharged.
- *J0 (AllocationRequiresPlacement).* Each freshly allocated `a_{new0}, a_{new1} ∈ dom(C') \ dom(C)` is placed at `[1,3], [1,4]` respectively in `M'(d)` — discharged.

The composite-boundary coupling triple `{J0, J1★, J1'★}` is satisfied exactly when step 4's K.ρ firings commit, completing the operation.

**Append case (`j = N = 5`).** With the same pre-state, `INSERT(d, [1,6], ⟨v₀⟩)` (where `[1,6] = shift([1,1], 5)` is one past the last position). The Right region is empty; no K.μ⁻ fires (Left = entire `V_{s_C}(d)`). Composite: one K.α + one K.μ⁺ adding `[1,6] ↦ a_{new0}` only + one K.ρ. Post-state `V_{s_C}(d') = {[1,1], …, [1,6]}` with `a₁, …, a₅, a_{new0}` as images.

**Empty-document first insertion.** Let `d` have `V_{s_C}(d) = ∅` and additionally `V_{s_L}(d) = ∅` (so the document's arrangement is entirely empty). Invoke `INSERT(d, [1,1], ⟨v₀, v₁, v₂⟩)` with `m = 2` (caller-chosen depth) and `n = 3`. The position `p = [1,1]` is the unique value admitted by `ValidFirstInsertionPosition(d, p, 2)` (ASN-0036). K.μ⁻ is omitted per case (i.a) of the substrate decomposition above (`dom(M(d)) = ∅` makes K.μ⁻'s precondition fail, forcing omission). Case (i.b) — `V_{s_C}(d) = ∅` but `V_{s_L}(d) ≠ ∅` — produces the same INSERT post-state shape on the content subspace: the operation's text-subspace effect (Insertion at `shift(p, k) ↦ a_{new k}`, empty Left, empty Shifted-right) depends only on `V_{s_C}(d) = ∅`, not on whether `V_{s_L}(d)` is empty; the link subspace is preserved verbatim by the cross-subspace frame in either sub-case. The composite reduces to:

1. **Three K.α firings.** `A_C(d)` emits `a_{new0} = [d.0.s_C.1]` (first-emission predicate fires since `{a' ∈ dom(Σ.C) : origin(a') = d} = ∅`), then `a_{new1} = inc(a_{new0}, 0)`, then `a_{new2} = inc(a_{new1}, 0)`. Each freshly satisfies K.α's freshness precondition by ChainEnumerationInjectivity and FirstEmissionFreshness (ASN-0093).
2. **One K.μ⁺ on `d`** adding three V-positions: `[1,1] ↦ a_{new0}`, `[1,2] ↦ a_{new1}`, `[1,3] ↦ a_{new2}`. All in subspace `s_C` per the K.μ⁺ amendment.
3. **Three K.ρ firings** recording `(a_{new0}, d)`, `(a_{new1}, d)`, `(a_{new2}, d)` in R.

The post-state arrangement:

  `M'(d) = {[1,1] ↦ a_{new0}, [1,2] ↦ a_{new1}, [1,3] ↦ a_{new2}}`

with `V_{s_C}(d') = {[1,1], [1,2], [1,3]}` and `m_C = 2` fixed by S8-depth (ASN-0036) for `d` at every subsequent state in which `V_{s_C}(d)` remains non-empty. Verifying the three regions: *Left* is empty (no pre-state position with `v < p`); *Insertion* is `{[1,1] ↦ a_{new0}, [1,2] ↦ a_{new1}, [1,3] ↦ a_{new2}}` matching `shift(p, k) ↦ a_k` for `k ∈ {0, 1, 2}` (with `shift([1,1], 0) = [1,1]` by OrdinalShiftBase); *Shifted right* is empty (no pre-state position with `v ≥ p`).

*Cross-subspace and cross-document frames (empty case).* `V_{s_L}(d) = ∅` is preserved trivially: K.μ⁺'s content-subspace restriction adds no `s_L` positions, so `V_{s_L}(d') = ∅` matches. Other subspaces are vacuous. Other documents `d' ≠ d` have `M'(d') = M(d')` by each elementary step's cross-document frame.

*Discharge of J0, J1★, J1'★ (empty case).* The boundary couplings discharge analogously to the interior case. J0 (AllocationRequiresPlacement; ASN-0047) requires each freshly allocated `a_{new0}, a_{new1}, a_{new2} ∈ dom(C') ∖ dom(C)` to be placed in some `M'(d')`'s range — discharged by step 2's K.μ⁺ placing each at `[1,1], [1,2], [1,3]` respectively. J1★ (ExtensionRecordsProvenanceContentSubspace; ASN-0047) requires every newly-arranged content-subspace I-address (not previously in `ran(M(d))` via a content-subspace V-position) to have its provenance pair in R'. Pre-state `ran(M(d)) = ∅` (the arrangement was empty), so every Insertion image is "newly-arranged"; step 3's three K.ρ firings discharge J1★ for all three pairs. J1'★ (ProvenanceRequiresExtensionContentSubspace; ASN-0047) requires every new R' entry to correspond to a newly-arranged content-subspace I-address — each `(a_{new k}, d)` added in step 3 corresponds to the placement `[1,1+k] ↦ a_{new k}` added in step 2. The boundary triple `{J0, J1★, J1'★}` is satisfied when step 3's K.ρ firings commit.

*Empty-arrangement vs. fresh-allocator-state sub-case.* The example above has both `V_{s_C}(d) = ∅` (empty arrangement) and `{a' ∈ dom(Σ.C) : origin(a') = d} = ∅` (fresh allocator state). These two conditions are independent and select different aspects of the operation: *empty arrangement* (`V_{s_C}(d) = ∅`) is the precondition that selects `ValidFirstInsertionPosition(d, p, m)` over `ValidInsertionPosition(d, p)` and forces the V-position `p = [1, 1]`; *fresh allocator state* (`{a' ∈ dom(Σ.C) : origin(a') = d} = ∅`) is the K.α first-emission predicate that determines `a_{new0} = [d.0.s_C.1]` exactly. Consider the alternative sub-case where `d` has prior content emissions in `dom(C)` that are not currently arranged — for example, content allocated by an earlier INSERT and later removed from `M(d)` by a K.μ⁻, leaving the addresses permanent in `C` (by P0) but the arrangement empty. Concretely, suppose `dom(C)` contains `[d.0.s_C.1], [d.0.s_C.2]` from a prior INSERT both subsequently dropped from `M(d)`. Then the empty-arrangement precondition still holds (selecting `ValidFirstInsertionPosition`), but K.α's first-emission predicate is false; instead the subsequent-emission predicate fires `a_{new0} = inc(max{a' ∈ dom(C) : origin(a') = d}, 0) = inc([d.0.s_C.2], 0) = [d.0.s_C.3]`, continuing the existing chain rather than producing `[d.0.s_C.1]` (which is already taken). The generic notation `a_{new k}` covers both sub-cases; the V-position assignments `[1, 1] ↦ a_{new0}`, `[1, 2] ↦ a_{new1}`, `[1, 3] ↦ a_{new2}` are determined by the empty-arrangement condition, while the actual address values are determined by the chain state. The post-state predicates (D-CTG★, D-MIN★, D-SEQ★, S8a, S8-depth) hold uniformly in either sub-case; J0, J1★, J1'★ discharge identically (the fresh `a_{new k}` are by definition outside `ran(M(d)) = ∅` regardless of whether they are first emissions or chain continuations).

## Verifying the Invariants

The post-state Σ' must satisfy every system invariant. We verify the principal ones.

### Permanence of existing content (S0, P0)

The content-store effect's third clause asserts `(A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a))`. This is S0 (ContentImmutability; ASN-0036), equivalently P0 (ContentPermanence; ASN-0047), which subsumes S0 ∧ S1. The first clause `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}` adds new addresses without removing any; the new addresses are fresh by ChainEnumerationInjectivity and FirstEmissionFreshness (ASN-0093), so no overwrite occurs. Store monotonicity `dom(C) ⊆ dom(C')` follows.

Each per-step K.α firing preserves S0 by its own frame (its effect adds a new binding without modifying existing ones); K.μ⁻, K.μ⁺, K.ρ have frame `C' = C` and so preserve S0 trivially. The composite preserves S0 by composition.

The consequence Nelson emphasises (Q5): a reader holding any pre-state I-address `a ∈ dom(C)` retrieves the same value `C'(a) = C(a)` from the post-state. The reader needs no knowledge of where in any document's Vstream that content now lies.

### Cross-document independence (Q3)

The frame `(A d' : d' ≠ d : M'(d') = M(d'))` directly enforces independence: no document other than `d` has its arrangement altered. Coupled with `L' = L` and content-store preservation, this means that any document `d'` that transcludes content from `d` continues to map the same V-positions to the same I-addresses, and those I-addresses continue to resolve to the same values.

The two documents may share I-addresses through transclusion, but the cross-document frame and content preservation together ensure that the shared I-addresses' values and the *other* document's mappings are unaffected.

The cross-document independence extends to link projection. For any link `ℓ ∈ dom(L)` and any document `d' ≠ d`, the projection from `d'` is unchanged: `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)`. This is LP4 (ArrangementSpecificity; ASN-0098) applied to the unchanged `M'(d') = M(d')` together with LP5 (CrossDocumentIndependence; ASN-0098) on the substrate's cross-document frame. See the *Projection-shift correspondence* clause below in §Coverage and link discoverability for the full per-document derivation.

### Arrangement functionality (S2)

We verify that `M'(d)` is a function (S2, ArrangementFunctionality; ASN-0036): no V-position has two distinct image I-addresses.

The Left, Insertion, and Shifted-right regions are pairwise disjoint as sets of V-positions. Writing `p = [s_C, 1, …, 1, p_m]`:

- *Left ∩ Insertion = ∅.* Left positions have last component `< p_m`; Insertion positions have last component in `{p_m, p_m + 1, …, p_m + n − 1}`. The component arithmetic splits on `k`, since `δ(k, m_C)` is defined only for `k ≥ 1` (OrdinalDisplacement, ASN-0034). For `k = 0`, OrdinalShiftBase (ASN-0058) gives `shift(p, 0) = p`, so the final component is `(shift(p, 0))_{m_C} = p_m`. For `1 ≤ k < n`, the OrdinalShift definition `shift(p, k) = p ⊕ δ(k, m_C)` (ASN-0034) and TumblerAdd's piecewise rule (ASN-0034) at action point `m_C` apply: positions `1, …, m_C − 1` are inherited from `p`, and the final component is `(shift(p, k))_{m_C} = p_{m_C} + δ(k, m_C)_{m_C} = p_m + k`. Across both cases the last component ranges over `{p_m, p_m + 1, …, p_m + n − 1}` for `0 ≤ k < n`.

- *Insertion ∩ Shifted-right = ∅.* Insertion positions have last component in `{p_m, …, p_m + n − 1}`. Shifted-right positions image `v` with last component `v_m ≥ p_m` to `shift(v, n) = v ⊕ δ(n, m_C)`; by the same TumblerAdd rule (ASN-0034), the last component of `shift(v, n)` is `v_m + n`. Since `v_m ≥ p_m` and `n ≥ 1`, every Shifted-right last component satisfies `v_m + n ≥ p_m + n`, strictly greater than every Insertion last component.

- *Left ∩ Shifted-right = ∅.* Left last components are `< p_m`; Shifted-right last components are `≥ p_m + n ≥ p_m + 1`.

Within each region the mapping is uniquely defined: Left and Shifted-right by `M(d)` applied to a unique source position — for Shifted-right, source uniqueness follows from TS2 (ShiftInjectivity; ASN-0034) once its equal-length precondition is met: by S8-depth (FixedDepthVPositions; ASN-0036) all pre-state `s_C` positions share the common depth `m_C`, so for any pair of pre-state Right sources `v₁, v₂ ∈ V_{s_C}(d)` with `v₁ ≥ p` and `v₂ ≥ p`, `#v₁ = #v₂ = m_C` satisfies TS2's precondition; TS2 then yields injectivity — distinct sources `v₁ ≠ v₂` yield `shift(v₁, n) ≠ shift(v₂, n)`. Insertion images are uniquely indexed by `k`. The pairwise-disjoint and uniquely-defined regions together exhaust `V_{s_C}(d')` by INS.M-exhaustive — no fourth region of `s_C` positions exists in the post-state to violate functionality. So `M'(d)` is a well-defined function.

I3-S2 (PostInsertionFunctionality; ASN-0082) covers a structurally smaller post-state — the *shift-only* model whose post-state domain ranges over three regions (shifted, left, cross-subspace) per I3-CS and I3-V. It discharges functionality on the Left + Shifted-right + cross-subspace portion of INSERT's post-state, but does *not* cover the Insertion region — the freshly placed V-positions `shift(p, k)` for `0 ≤ k < n` lie outside I3's post-state by I3-CS's domain closure. The Insertion region's contribution to functionality is verified by the explicit pairwise-disjointness argument above. For other subspaces and other documents, `M'` equals `M`, which is already a function by the pre-state S2.

### Referential integrity (S3★)

We verify the generalised content-and-link form S3★ (GeneralizedReferentialIntegrity; ASN-0047): `(A v ∈ dom(M'(d)) : (subspace(v) = s_C ⟹ M'(d)(v) ∈ dom(C')) ∧ (subspace(v) = s_L ⟹ M'(d)(v) ∈ dom(L')))`.

For Left and Shifted-right content-subspace positions: the image is `M(d)(v')` for some pre-state position `v' ∈ dom(M(d))` with `subspace(v') = s_C`, so by pre-state S3★ the image lies in `dom(C)`, and by P0 (ContentPermanence; ASN-0047) `dom(C) ⊆ dom(C')`.

For Insertion positions: the image is `a_k ∈ dom(C')` by the content-store effect.

For positions in subspaces other than `s_C` of `d` (notably `s_L`), and for positions in other documents: unchanged by frame; S3★ follows from the pre-state combined with link-store immutability `L' = L`.

I3-S3 (PostInsertionReferentialIntegrity; ASN-0082) discharges referential integrity over the Left + Shifted-right + cross-subspace portion of the post-state (the regions ASN-0082's shift-only model covers); the Insertion region's contribution is verified explicitly above by the freshness of each `a_k ∈ dom(C')`.

### Sequential text-subspace structure (D-CTG★, D-MIN★, D-SEQ★)

We verify the per-subspace forms D-CTG★ (PerSubspaceContiguity), D-MIN★ (PerSubspaceMinimumPosition), and D-SEQ★ (PerSubspaceSequentialPositions) from ASN-0047 for the text subspace `s_C` of `d` post-state.

Suppose `V_{s_C}(d) = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ N}` with `N ≥ 1` (by pre-state D-SEQ★), and `p = [s_C, 1, …, 1, p_m]` with `p_m ∈ {1, …, N+1}`. Then:

- Left positions: `{[s_C, 1, …, 1, k] : 1 ≤ k < p_m}` — empty if `p_m = 1`.
- Insertion positions: `{[s_C, 1, …, 1, p_m + j] : 0 ≤ j < n} = {[s_C, 1, …, 1, k] : p_m ≤ k < p_m + n}`.
- Shifted-right positions: `{[s_C, 1, …, 1, k + n] : p_m ≤ k ≤ N} = {[s_C, 1, …, 1, k] : p_m + n ≤ k ≤ N + n}` — empty if `p_m = N + 1`.

Their union is `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}`, which is exactly the sequential structure required by D-SEQ★ with new cardinality `N + n`. The minimum `[s_C, 1, …, 1]` is in the union, so D-MIN★ holds. The integer range `{1, …, N + n}` of last-component values is contiguous, so D-CTG★ holds.

For the empty pre-state case (`V_{s_C}(d) = ∅`) with `p = [s_C, 1, …, 1]` of caller-chosen depth `m ≥ 2` (via ValidFirstInsertionPosition; ASN-0036): the post-state has only the Insertion region (Left and Shifted-right are empty). The Insertion positions are `shift(p, k) = [s_C, 1, …, 1, 1 + k]` for `0 ≤ k < n`, by OrdAddHom for `k ≥ 1` (where `shift(p, k) = p ⊕ δ(k, m)` agrees with `p` on positions `1, …, m − 1` and adds `k` to position `m`) and by OrdinalShiftBase (ASN-0058) for `k = 0` (where the convention `shift(p, 0) = p` resolves the position to `p` itself, which is `[s_C, 1, …, 1, 1] = [s_C, 1, …, 1]` since `p_m = 1`). Since `p_m = 1` (the unique valid first position has last component 1), the last components of the Insertion positions are `{1 + 0, 1 + 1, …, 1 + (n − 1)} = {1, 2, …, n}` and the leading `m − 1` components are all `1` throughout.

Post-state `V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ n}`. We verify each predicate:

- *D-MIN★:* the minimum of `V_{s_C}(d')` under T1 is the position with the smallest last component, namely `[s_C, 1, …, 1, 1] = [s_C, 1, …, 1]` of depth `m`. This matches D-MIN★'s required form `[s_C, 1, …, 1]`.
- *D-CTG★:* the last-component values `{1, 2, …, n}` form a contiguous integer range with no gaps; T1 makes the V-ordering on a fixed-prefix, fixed-depth subspace agree with the integer ordering on the last component, so contiguity holds.
- *D-SEQ★:* the explicit form `V_{s_C}(d') = {[s_C, 1, …, 1, k] : 1 ≤ k ≤ n}` matches D-SEQ★ with `n_{s_C} = n` and depth `m_{s_C} = m`.
- *S8-depth:* every position in `V_{s_C}(d')` has length `m`. Pre-state `V_{s_C}(d) = ∅` imposes no depth constraint, so the post-state's `m_{s_C} := m` is the first occurrence — the freedom afforded by ValidFirstInsertionPosition's depth parameter. From this point onward, S8-depth — a per-state invariant under ValidComposite★ — fixes `m_{s_C} = m` for `d` at every state in which `V_{s_C}(d)` remains non-empty; every subsequent text-subspace operation on `d` must use depth `m` as long as that condition holds. (If a subsequent K.μ⁻ empties `V_{s_C}(d)`, S8-depth becomes vacuous at that state, freeing a later first-insertion to choose a different `m'`.)
- *S8a:* each Insertion position `[s_C, 1, …, 1, k]` is zero-free (subspace identifier `s_C ≥ 1` and all other components `1`), has length `m ≥ 2`, and has all components strictly positive.

The empty case differs from the non-empty case in that no Left or Shifted-right regions appear and no K.μ⁻ fires in the composite (per the case (i.a)/(i.b) routing above), but the post-state invariants are verified by the same predicate checks on the post-state's exhibited form.

### Post-state V-position well-formedness (S8-depth, S8a, S8-fin) and S7 invariants

ASN-0082's I3-VD (PostInsertionDepthUniformity), I3-VP (PostInsertionWellFormedness), I3-fin (PostInsertionFiniteness), and I3-S7 (PostInsertionAllocationInvariants) discharge their respective post-state predicates over ASN-0082's *shift-only* post-state — Left + Shifted-right + cross-subspace. They do not cover INSERT's Insertion region: the freshly placed V-positions `shift(p, k)` for `0 ≤ k < n` and the freshly allocated I-addresses `{a_0, …, a_{n−1}}` lie outside I3's post-state by I3-CS's domain closure. The Insertion-region contribution is verified explicitly below.

- *S8-depth (FixedDepthVPositions, ASN-0036; cf. I3-VD).* Split the verification by `k`. At `k = 0`: `shift(p, 0) = p` by OrdinalShiftBase (ASN-0058), so `#shift(p, 0) = #p = m_C` directly from `p`'s precondition (`#p = m_C` from INSERT's preconditions, supplied either by S8-depth on the non-empty pre-state or by the caller's `ValidFirstInsertionPosition` depth choice). At `k ≥ 1`: by the OrdinalShift definition (ASN-0034), `shift(p, k) = p ⊕ δ(k, m_C)`; TumblerAdd's result-length identity (ASN-0034) gives `#shift(p, k) = #δ(k, m_C) = m_C`. In both cases, every Insertion position has depth `m_C`, matching the depth that I3-VD already establishes for Left and Shifted-right positions and the cross-subspace depths preserved by I3-X. S8-depth holds across all subspaces of the post-state.

- *S8a (VPositionWellFormedness, ASN-0036; cf. I3-VP).* Split the verification by `k`. At `k = 0`: `shift(p, 0) = p` by OrdinalShiftBase (ASN-0058), so S8a transfers directly from `p`'s S8a — `p` itself satisfies S8a (zero-free, depth `≥ 2`, all components strictly positive) by ValidInsertionPosition postcondition (b) (ASN-0036) in the non-empty case, or by ValidFirstInsertionPosition postcondition (b) (ASN-0036) in the empty case. At `k ≥ 1`: TumblerAdd's piecewise rule (ASN-0034) applied to `shift(p, k) = p ⊕ δ(k, m_C)` at action point `m_C` copies the leading `m_C − 1` components from `p`, which are all `1` (since `p` is a valid insertion position of the form `[s_C, 1, …, 1, p_m]` per ValidInsertionPosition's postcondition (d), ASN-0036, or `[s_C, 1, …, 1]` per ValidFirstInsertionPosition's postcondition (d), ASN-0036); the final component is `p_m + k ≥ p_m ≥ 1`. So `zeros(shift(p, k)) = 0`, `#shift(p, k) = m_C ≥ 2`, and every component is strictly positive. In both cases S8a holds on Insertion positions; combined with I3-VP on Left + Shifted-right + cross-subspace, S8a holds across the post-state. (This subsumes the empty-case S8a verification above, factoring out the Insertion-region argument as a general property of `shift(p, k)` independent of whether the Left and Shifted-right regions are non-empty.)

- *S8-fin (FiniteArrangement, ASN-0036; cf. I3-fin).* The Insertion region contributes exactly `n` new V-positions to `dom(M'(d))`. The pre-state `dom(M(d))` is finite by pre-state S8-fin; the post-state `dom(M'(d))` is the union of finite Left + finite Shifted-right + finite Insertion (cardinality `n`) + finite cross-subspace contributions, hence finite.

- *S7 invariants (S7a, S7b, S7c, S7d, and the derived theorem S7, ASN-0036; cf. I3-S7).* The predicates range over `dom(C)` and the document set. Every pre-state `a ∈ dom(C)` inherits S7a–S7d at the post-state by the pointwise S0/P0 preservation already established under §Permanence and the unchanged document set. For each freshly allocated `a_k ∈ dom(C') ∖ dom(C)`: `origin(a_k) = d ∈ dom(M')` discharges S7a (DocumentScopedAllocation) by K.α's emission discipline (ASN-0093); `zeros(a_k) = 3` discharges S7b (ElementLevelIAddresses) by ChainUniformZeroCount (ASN-0093) — every element of `A_C(d)` has `zeros = 3`; `#E(a_k) ≥ 2` discharges S7c (ElementFieldDepth) since `A_C(d)`'s first emission has `#E = 2` (SubAllocatorAxiom.FirstEmission, ASN-0093) and every subsequent emission via `inc(·, 0)` preserves length (TA5(c), ASN-0034); S7d (DocumentAllocationDiscipline) holds at `d` by pre-state inheritance — `d ∈ dom(M)` was a document-allocation event under T10a with `zeros(d) = 2` and T4-validity (M0, ASN-0093). The derived theorem S7 (StructuralAttribution) follows by composition.

- *P6 (ExistentialCoherence, ASN-0047).* `(A a ∈ dom(C') :: origin(a) ∈ E'_doc)` (where `E_doc` is the document subset of `E`). We first make explicit the substrate identification on which the argument depends. *Identification.* Under ValidComposite★ (ASN-0047), the document subset of the entity set `E_doc` coincides with the document arrangement domain `dom(M)`: every `d ∈ E_doc` is allocated with `M(d) = ∅` initialised by K.δ-IsDocument (ASN-0047), and `M`'s domain is extended only by K.δ in its IsDocument sub-case. So `E_doc = dom(M)` is an invariant of ValidComposite★, holding at every state. This identification holds at the pre-state Σ and at the post-state Σ' because both are ValidComposite★ states. Now the argument: every pre-state `a ∈ dom(C)` inherits P6 from the pre-state because `dom(C) ⊆ dom(C')` and `origin(a)` is a property of the address `a` itself (an invariant of the addressing scheme, by S7 / StructuralAttribution), unchanged across the composite; meanwhile `E' = E` by INS.frame.E (no K.δ fires), so `E'_doc = E_doc`, and pre-state `origin(a) ∈ E_doc` lifts to `origin(a) ∈ E'_doc`. For each freshly allocated `a_k ∈ dom(C') ∖ dom(C)`: `origin(a_k) = d` by K.α's emission discipline (ASN-0093); INSERT's precondition gives `d ∈ dom(M)`, which by the identification yields `d ∈ E_doc`; INS.frame.E gives `E_doc = E'_doc`; hence `d ∈ E'_doc`, so `origin(a_k) ∈ E'_doc`. P6 is preserved across the composite.

### Per-subspace span decomposition (S8★)

S8★ (PerSubspaceSpanDecomposition; ASN-0047) requires that each per-subspace arrangement `M'(d)|_{V_S(d')}` admit a finite block decomposition satisfying ASN-0036's S8 conditions. The post-state's standing preconditions for M2 (DecompositionExistence; ASN-0058) — S8-fin, S2, S3★, S8a, S8-depth, S7b, S7c — are all verified above (under §Arrangement functionality, §Referential integrity, §Sequential text-subspace structure, §Post-state V-position well-formedness, and §S7 invariants), so the existence of a block decomposition for `M'(d)|_{V_{s_C}(d')}` follows from M2 directly. The link-subspace branch S8★ requires for `M'(d)|_{V_{s_L}(d')}` is discharged by the trivial length-1 decomposition (per ASN-0047), inherited unchanged from the pre-state by the cross-subspace frame `V_{s_L}(d') = V_{s_L}(d)`.

The text-subspace decomposition has a particularly simple form: the Insertion region `{(shift(p, k), a_k) : 0 ≤ k < n}` forms a single correspondence run `(p, a_0, n)`. The V-positions are consecutive `shift(p, k)` (each obtained from `p` by advancing the last component by `k`, by the OrdinalShift definition; ASN-0034), and the I-addresses are consecutive chain emissions `a_k` of `A_C(d)` with `a_{k+1} = inc(a_k, 0)` (by Effect One). The I-adjacency `a_{k+1} = a_k + 1` (in ordinal-shift notation, identifying `inc(·, 0)` on a T4-valid same-length successor with the ordinal-shift operation) is the M-adjacency required by M7's merge condition (ASN-0058), so the `n` Insertion blocks merge into a single length-`n` block. The Left and Shifted-right portions are derived from the pre-state decomposition as follows. A pre-state block `(v', a', m')` whose V-extent straddles `p` — i.e., `v' < p` and `p ≤ shift(v', m' − 1)` — is first split at the interior offset `c := p_m − v'_m ∈ {1, …, m' − 1}` via M4 (ASN-0058), yielding a Left piece `(v', a', c)` and a Right piece `(shift(v', c), a' + c, m' − c)`. After all straddling pre-state blocks are split, every remaining pre-state block lies entirely below `p` (a Left block) or entirely at or above `p` (a Right block). The Left blocks transfer unchanged to the post-state; each Right block `(v', a', m')` becomes a Shifted-right block `(shift(v', n), a', m')` — V-start advanced by `n`, with I-start and width unchanged (shift acts only on V-positions, not on I-addresses; the width is the count of mapped positions, which is the same as in the source block). The post-state decomposition is finite and well-defined; its existence is also guaranteed independently by M2 applied to the post-state.

S8★ is preserved.

### Cross-subspace isolation

The frame `(A v : v ∈ dom(M(d)) ∧ subspace(v) ≠ s_C : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))` directly preserves all subspaces of `d` other than the text subspace. In particular, `V_{s_L}(d') = V_{s_L}(d)`, and link-subspace mappings are unchanged.

The isolation has a structural foundation independent of the explicit frame. The shift operation `shift(v, n) = v ⊕ δ(n, #v)` modifies only the last component of `v` at depth `m_C`. Even if it were applied to a position in `V_{s_L}(d)`, by OrdAddHom (b clause) the subspace identifier — the first component — would be preserved; the position would not migrate to the text subspace. But INSERT never applies shift to non-text positions in the first place. The subspace identifier is part of the V-position's structure, and INSERT's shift is scoped strictly to `s_C`.

Gregory's implementation realises this isolation via a two-blade "knife" whose blades bracket the text subspace; link-subspace crums are classified as outside the shift region and are uniformly left untouched. The structural property is what we verify abstractly; the knife is one (efficient) implementation.

### Link store unchanged (L12, L0, L1, L3)

`L' = L` directly preserves every link's address and value. Every `ℓ ∈ dom(L)` has `L'(ℓ) = L(ℓ)` — endsets are pointwise preserved. The element-level structure L1 and the N-endset structure L3 range over `dom(L)` alone, which is unchanged, so they hold of `L'` trivially.

The subspace partition L0 requires more care, because it has two conjuncts: `(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)` and `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)`. The first conjunct ranges over `dom(L)`, unchanged, and so is discharged trivially. The second conjunct ranges over `dom(C)`, which INSERT *extends* by the fresh content addresses `a_0, …, a_{n−1}` (INS.C) — it is therefore not a property of `L` alone. For each freshly allocated `a_k`, `subspace_I(a_k) = s_C` holds by SubAllocatorAxiom.Subspace (ASN-0047) / DisjointSubAllocatorChains (ASN-0093): every address `a_k` is produced by `d`'s content sub-allocator `A_C(d)`, and every output of `A_C(d)` carries subspace identifier `s_C`. The pre-existing entries of `dom(C)` satisfy the conjunct by the pre-state invariant. Hence L0's content clause is preserved.

### Coverage and link discoverability

For every link `ℓ ∈ dom(L)` and every slot `i`, the endset `Σ.L(ℓ).e_i` is a set of spans. Each span `(s, ℓ_w)` denotes `{t ∈ T : s ≤ t < s ⊕ ℓ_w}` — a purely combinatorial property of the span representation, consulting no state component (definition of `coverage` in ASN-0098). Since `L' = L`, every link value is unchanged at every slot, so coverage is unchanged: by LP3★ (MultiStepCoverageInvariance; ASN-0098), `coverage(Σ'.L(ℓ).e_i) = coverage(Σ.L(ℓ).e_i)` for every link and every slot. (LP3★ extends to multi-step compositions, so it discharges the property across the substrate composite, not just per-step.)

**Projection-shift correspondence (postcondition).** For every link `ℓ ∈ dom(L)`, slot `i`, and document `d' ∈ dom(M)`:

  `project(ℓ, i, d', Σ') = π(project(ℓ, i, d', Σ)) ∪ N_{ℓ,i}`

where:
- *For `d' ≠ d`:* `π` is the identity and `N_{ℓ,i} = ∅`, so `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)` — by frame `M'(d') = M(d')` together with LP4 (ArrangementSpecificity; ASN-0098) and LP5 (CrossDocumentIndependence; ASN-0098).
- *For `d' = d`, link subspace:* the link-subspace contribution is unchanged (frame), so `π` is the identity on link-subspace contributions and `N_{ℓ,i}` contributes none.
- *For `d' = d`, text subspace:* `π` is the *region-aware shift map* — identity on the Left region (`v < p`) and `shift(·, n)` on the Right region (`v ≥ p`). The Right branch of `π` closes within subspace `s_C`: for every `v ∈ V_{s_C}(d)` with `v ≥ p`, by OrdAddHom (b clause, ASN-0036) applied to `shift(v, n) = v ⊕ δ(n, m_C)` (a displacement with `δ(n, m_C)_1 = 0`), `subspace(shift(v, n)) = subspace(v) = s_C`, so `shift(v, n) ∈ V_{s_C}(d')`. `N_{ℓ,i} ⊆ {shift(p, k) : 0 ≤ k < n}` is the set of newly placed V-positions in `V_{s_C}(d')` whose image `a_k` happens to lie in `coverage(Σ'.L(ℓ).e_i)`.

The derivation tracks `project(ℓ, i, d, ·)` through each intermediate state of the substrate decomposition. Let `e_i := Σ.L(ℓ).e_i` denote the slot's endset; LP3★ (MultiStepCoverageInvariance; ASN-0098) gives `coverage(Σ_j.L(ℓ).e_i) = coverage(e_i)` at every intermediate `Σ_j`, so we write `coverage(e_i)` unambiguously throughout.

Step 0 — pre-state:

  `P_0 := project(ℓ, i, d, Σ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e_i)}`

Partition `P_0` into:
- `P_0^L := {v ∈ P_0 : subspace(v) = s_C ∧ v < p}` (Left contributions)
- `P_0^R := {v ∈ P_0 : subspace(v) = s_C ∧ v ≥ p}` (Right contributions)
- `P_0^{s_L} := {v ∈ P_0 : subspace(v) = s_L}` (link-subspace contributions)

By S3★-aux (SubspaceExhaustiveness; ASN-0047), `dom(M(d)) ⊆ V_{s_C}(d) ∪ V_{s_L}(d)`, so `P_0 = P_0^L ∪ P_0^R ∪ P_0^{s_L}` is exact.

Step 1 — after each K.α firing:

  `project(ℓ, i, d, Σ_α_k) = project(ℓ, i, d, Σ_α_{k−1}) = … = P_0`

by LP6 (ContentAllocationInvariance; ASN-0098): K.α modifies only C and has frame `(A d :: M'(d) = M(d))`, so the projection is unchanged at every K.α intermediate.

Step 2 — after K.μ⁻ (when fired). K.μ⁻ retains `R_kept := L ∪ V_{s_L}(d)` where `L := {v ∈ V_{s_C}(d) : v < p}`; the Right region is removed from `dom(M(d))`. By LP10 (ContractionMonotonicity; ASN-0098), the projection contracts to its intersection with the kept domain:

  `project(ℓ, i, d, Σ_μ⁻) = P_0 ∩ R_kept = P_0^L ∪ P_0^{s_L}`

— the Right contributions are temporarily removed; Left and link-subspace contributions are preserved.

When K.μ⁻ does *not* fire (cases i.a, i.b, ii of the substrate decomposition), `Σ_μ⁻` does not exist as a distinct state and the flow passes from `Σ_α_n` directly to `Σ_μ⁺`. In all three K.μ⁻-omitted cases `P_0^R = ∅`: cases (i.a) and (i.b) both have `V_{s_C}(d) = ∅`, so no V-position satisfies `v ∈ V_{s_C}(d) ∧ v ≥ p`; case (ii) has `p_m = N + 1`, so no `v ∈ V_{s_C}(d)` (with last components in `{1, …, N}`) satisfies `v ≥ p`. The projection at the post-Step-1 state is therefore `P_0 = P_0^L ∪ P_0^R ∪ P_0^{s_L} = P_0^L ∪ P_0^{s_L}` — identical in form to the K.μ⁻-fired formula above. Steps 3 and 4 below proceed uniformly from this expression regardless of whether Step 2 fired.

Step 3 — after K.μ⁺. K.μ⁺ adds two disjoint sets of new V-positions:
- *Insertion positions* `I := {shift(p, k) : 0 ≤ k < n}`, each mapping `shift(p, k) ↦ a_k`
- *Shifted-right positions* `S := {shift(v, n) : v ∈ V_{s_C}(d) ∧ v ≥ p}`, each mapping `shift(v, n) ↦ M(d)(v)`

By LP9 (ExtensionMonotonicity; ASN-0098), the projection grows by exactly those new V-positions whose image lies in `coverage(e_i)`:

  `project(ℓ, i, d, Σ_μ⁺) = project(ℓ, i, d, Σ_μ⁻) ∪ N_I ∪ N_S`

where:
- `N_I := {shift(p, k) : 0 ≤ k < n ∧ a_k ∈ coverage(e_i)}` — Insertion contributions
- `N_S := {shift(v, n) : v ∈ V_{s_C}(d) ∧ v ≥ p ∧ M(d)(v) ∈ coverage(e_i)} = {shift(v, n) : v ∈ P_0^R}` — Shifted-right contributions

Substituting:

  `project(ℓ, i, d, Σ_μ⁺) = P_0^L ∪ P_0^{s_L} ∪ N_I ∪ {shift(v, n) : v ∈ P_0^R}`

Step 4 — after each K.ρ firing:

  `project(ℓ, i, d, Σ_ρ_k) = project(ℓ, i, d, Σ_μ⁺) = … = project(ℓ, i, d, Σ')`

by LP14 (ProvenanceRecordingInvariance; ASN-0098): K.ρ modifies only R and has frame `(A d :: M'(d) = M(d))`, so the projection is unchanged.

Combining:

  `project(ℓ, i, d, Σ') = P_0^L ∪ {shift(v, n) : v ∈ P_0^R} ∪ P_0^{s_L} ∪ N_I`

Identifying π as the region-aware shift map (identity on Left and link-subspace contributions, `shift(·, n)` on Right contributions) and setting `N_{ℓ,i} := N_I`:

  `π(P_0) := P_0^L ∪ {shift(v, n) : v ∈ P_0^R} ∪ P_0^{s_L}`

  `project(ℓ, i, d, Σ') = π(project(ℓ, i, d, Σ)) ∪ N_{ℓ,i}`

The K.μ⁻ step's "temporary retraction" of `P_0^R` from the intermediate projection is *cancelled* by K.μ⁺'s reintroduction of those V-positions at shifted addresses: the Right contributions disappear at `Σ_μ⁻` (because their V-positions are removed from `dom(M(d))`) and reappear at `Σ_μ⁺` at the V-positions `shift(v, n)` (with the same I-addresses `M(d)(v)`). The cancellation is exact because K.μ⁺ adds *exactly* the shifted V-positions `{shift(v, n) : v ∈ V_{s_C}(d) ∧ v ≥ p}` with the same image mapping, so every Right contribution to the projection is recovered at its shifted V-position.

*Consequence — preservation of pre-state discoverability:*

  `discoverable_from(ℓ, d', Σ) ⟹ discoverable_from(ℓ, d', Σ')`

Every pre-state V-position contributing to projection is mapped (by π or identity) to a post-state V-position with the same I-address, so the non-emptiness of any pre-state projection slot transfers to the post-state.

*Consequence — fresh-address discoverability (the `N_{ℓ,i}` term):* A fresh `a_k` lies in `coverage(Σ'.L(ℓ).e_i)` only if the endset includes `a_k` in its span coverage. For *tight* endsets — those bounded to address ranges already populated at the time the endset was incorporated — this cannot happen: by LP19a (TightFreshness; ASN-0098), the freshness of `a_k` against the endset's incorporation state places it outside the tight coverage, so `N_{ℓ,i} = ∅`. For non-tight endsets, a fresh `a_k` may indeed land in coverage, and this is by intent: non-tight endsets are designed to capture later-allocated content within their declared range. LP19 (TightEndsetBoundaryExclusion; ASN-0098) specialises this to K.μ⁺ steps of the composite: V-positions newly added by K.μ⁺ whose image was freshly allocated by a prior K.α step of the composite are excluded from any pre-existing tight endset's projection.

### Provenance (R, P4★, P4a, P7a)

The provenance relation `R ⊆ T_elem × E_doc` (ASN-0047) records which documents have ever contained which I-addresses. INSERT's effect on R is `R' = R ∪ {(a_k, d) : 0 ≤ k < n}`, realised by `n` K.ρ firings in step 4 of the substrate composite.

The composite-boundary coupling J1★ (ExtensionRecordsProvenanceContentSubspace; ASN-0047) requires every newly-arranged content-subspace I-address with no pre-state arrangement under `d` to have its provenance pair in `R'`. For Insertion positions, the freshly allocated `a_k` was not in any `ran(M(d))` pre-state. We discharge this by the same machinery used in §Effect One: at the moment of `a_k`'s K.α firing, the freshness precondition `a_k ∉ dom(Σ_k.C) ∪ dom(Σ_k.L)` holds (by the chain-injectivity and subspace-disjointness arguments of §Effect One, with FirstEmissionFreshness covering only the boundary case `m_d = 0`); by P0 (ContentPermanence; ASN-0047) applied along `Σ →* Σ_k`, this lifts to `a_k ∉ dom(Σ.C)`; and by pre-state S3★ (GeneralizedReferentialIntegrity; ASN-0047), `ran(M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)`, whence `a_k ∉ ran(M(d))`. So J1★ requires `(a_k, d) ∈ R'` — discharged by step 4. For Shifted-right positions, `M(d)(v) = a` was already arranged at some content-subspace V-position `v ∈ dom(M(d))`, so J1★'s requirement of "not previously arranged in d's content subspace" is false, and no new R entry is required for these. The pair `(a, d)` was already in R via the historical state (preserved by P2, ProvenancePermanence; ASN-0047).

J1'★ (ProvenanceRequiresExtensionContentSubspace; ASN-0047) requires every new R' entry to correspond to a newly-arranged content-subspace I-address. Each `(a_k, d)` added in step 4 corresponds to the placement `shift(p, k) ↦ a_k` introduced by step 3's K.μ⁺ — satisfied.

P4★ (ProvenanceBoundsContentSubspace; ASN-0047): `Contains_C(Σ') ⊆ R'`. Pre-state P4★ gives `Contains_C(Σ) ⊆ R`. The post-state's content-subspace arrangement adds n new pairs (one per Insertion position with image `a_k`); each is in R' via step 4. So P4★ holds.

P4a (HistoricalFidelity; ASN-0047): every `(a, d) ∈ R'` has a historical state in which `a` was in d's content-subspace range. For pre-state `(a, d) ∈ R`, P4a inherits. For each new `(a_k, d)` added in step 4, the historical state is the substrate state at the end of step 3, in which `a_k ∈ ran(M'(d))` at the Insertion position.

P7 (ProvenanceGrounding; ASN-0047): `(A (a, d') ∈ R' :: a ∈ dom(C'))` — every R' entry's first component is in the post-state content store. For pre-state pairs `(a, d') ∈ R`, P7 inherits: pre-state P7 gives `a ∈ dom(C)`, and `dom(C) ⊆ dom(C')` by P0 (ContentPermanence; ASN-0047). For each new R' entry `(a_k, d)` added by step 4's K.ρ firings, the forced ordering *K.α(a_k) before K.ρ(a_k, d)* (established under §Atomicity) guarantees `a_k ∈ dom(Σ_4.C) ⊆ dom(C')` at the moment of the K.ρ firing; since `a_k` is in fact added to `dom(C)` by step 1's K.α firing and never removed thereafter, `a_k ∈ dom(C')` at the post-state. P7 holds.

P7a (ProvenanceCoverage; ASN-0047): every `a ∈ dom(C')` has some `d` with `(a, d) ∈ R'`. Pre-state P7a covers `dom(C)`; each new `a_k ∈ dom(C') \ dom(C)` is paired with `d` in step 4.

### What is *not* allocated

INSERT does *not* allocate new documents (`dom(M') = dom(M)`), does *not* allocate new links (`L' = L`), and does *not* allocate I-addresses outside `dom(C)`'s content subspace (every `a_k` has `subspace_I(a_k) = s_C`). The allocation footprint is precisely `n` content-subspace I-addresses scoped to `d`.

## Atomicity and Canonical Order

Nelson requires that after INSERT, the system is in "canonical order" — every structural invariant holds simultaneously. INSERT is a substrate composite governed by ValidComposite★ (ASN-0047), and its atomicity is the *composite-boundary* form: per-state invariants (Class (a) of ASN-0047 — S2, S3★, S8-depth, S8a, D-CTG★, D-MIN★, D-SEQ★, L0, L12, L14, …) hold at *every* state including each intermediate within the composite; composite-boundary properties (Class (b) — P4★, P4a, P7a) and the coupling constraints (J0, J1★, J1'★) hold at the boundary between Σ and Σ'.

We verify that each intermediate state in INSERT's substrate decomposition satisfies the per-state invariants.

ASN-0047's ExtendedReachableStateInvariants enumerates ~28 per-state invariants. Many are trivially preserved by frame at every intermediate of INSERT's decomposition because the state components they constrain are never modified. We group these by the state component they range over:

- *Entity-set invariants* — P8 (EntityHierarchy), NodeLineage (NodeDescentFromBootstrap), M0 (DocumentTumblerWellFormed; ASN-0093). The entity set E (equivalently `dom(M)` for documents under ValidComposite★) is unchanged at every intermediate: no K.δ fires, no K.σ fires. Each invariant is a predicate over E (or `dom(M)`) and so holds at every intermediate by inheritance from the pre-state.
- *Content-allocation invariants* — S4 (OriginBasedIdentity; ASN-0036). S4 ranges over `dom(C)`, not over E or `dom(M)`, so the "no K.δ fires, no K.σ fires" frame reasoning above does not apply — INSERT extends `dom(C)` by `n` fresh addresses via K.α firings, and S4 must be discharged against the changed `dom(C)` at every intermediate. The discharge proceeds in three parts at the `k`-th K.α intermediate state Σ_{α,k}. (i) *Pre-state pairs remain distinct.* For `a₁, a₂ ∈ dom(Σ.C)`, pre-state S4 gives `a₁ ≠ a₂`; P0 (ContentPermanence; ASN-0047) keeps both in `dom(Σ_{α,k}.C)` with the same identities, so distinctness transfers unchanged. (ii) *New addresses are distinct from pre-state addresses.* Each freshly emitted `a_j` (for `0 ≤ j ≤ k`) satisfies K.α's freshness precondition `a_j ∉ dom(Σ_{α,j−1}.C) ∪ dom(Σ_{α,j−1}.L)` at its own emission state (discharged in §Effect One via ChainEnumerationInjectivity and FirstEmissionFreshness; ASN-0093), so `a_j ∉ dom(Σ.C)` by P0 along `Σ →* Σ_{α,j−1}`. (iii) *The freshly emitted addresses are pairwise distinct.* For any pair `0 ≤ i < j ≤ k`, ChainEnumerationInjectivity (ASN-0093) supplies `a_i = t_{m_d + i + 1} < t_{m_d + j + 1} = a_j` under the tumbler order T1 (strict monotonicity of the chain enumeration), so `a_i ≠ a_j` by T1 irreflexivity. Together (i)–(iii) discharge S4 at every K.α intermediate. The subsequent K.μ⁻, K.μ⁺, and K.ρ firings have frame `C' = C` and so inherit S4 trivially.
- *Link-store invariants* — L0 (SubspacePartition), L1 (LinkElementLevel), L1a (LinkScopedAllocation), L1b (LinkElementFieldDepth), L1c (LinkAllocatorConformance), L3 (NEndsetStructure), L-fin (LinkStoreFiniteness), L12 (LinkImmutability), CL-OWN (LinkSubspaceOwnership), CL-UNIQ (LinkSubspacePositionUniqueness). The link store L is unchanged at every intermediate: no K.λ fires. L1, L1a, L1b, L1c, L3, L-fin, and L12 range over `dom(L)` alone and inherit from the pre-state. L0 is the exception: its first conjunct `(A a ∈ dom(L) :: subspace_I(a) = s_L)` ranges over the unchanged `dom(L)` and inherits trivially, but its second conjunct `(A a ∈ dom(C) :: subspace_I(a) = s_C)` ranges over `dom(C)`, which the K.α firings extend. For each freshly emitted `a_k`, `subspace_I(a_k) = s_C` by SubAllocatorAxiom.Subspace (ASN-0047) / DisjointSubAllocatorChains (ASN-0093) — `a_k` is an output of `d`'s content sub-allocator `A_C(d)`; pre-existing entries inherit from the pre-state. So L0's content clause holds at every K.α intermediate, and the subsequent K.μ⁻, K.μ⁺, K.ρ firings leave `dom(C)` unchanged (`C' = C`) and inherit it. CL-OWN and CL-UNIQ constrain link-subspace V-position mappings; the link subspace `V_{s_L}(d)` is preserved by every step (K.α and K.ρ leave M untouched; K.μ⁻ retains `V_{s_L}(d)` with `n'_{s_L} = n_{s_L}`; K.μ⁺ adds only content-subspace positions per the ASN-0047 amendment). The link-subspace mappings are therefore unchanged across the composite, and CL-OWN, CL-UNIQ inherit from the pre-state.
- *Content-store finiteness* — C-fin (ContentStoreFiniteness). The pre-state has `|dom(C)| < ∞`; each K.α firing adds exactly one address; n is finite. So `|dom(C')| ≤ |dom(C)| + n < ∞` at every intermediate.
- *Subspace exhaustiveness* — S3★-aux (SubspaceExhaustiveness). At every intermediate, `V_{s_C}(d)` and `V_{s_L}(d)` together cover `dom(M(d))` because the K.μ⁻ and K.μ⁺ steps add and remove only positions with subspace ∈ {s_C, s_L} (the K.μ⁺ amendment restricts new V-positions to `subspace = s_C`; K.μ⁻'s per-subspace retention preserves the same partition). Other documents' arrangements are unchanged. So S3★-aux holds.

These invariants are not re-verified in the per-step analysis below, which focuses on the invariants whose preservation requires non-trivial argument under INSERT's specific composition.

- *After each of the `n` K.α firings of step 1.* `dom(C)` extends by one fresh `a_k` with `origin(a_k) = d`; `M(d)` is unchanged. Per-state invariants on M (S2, S3★, S8a, S8-depth, S8-fin, D-CTG★, D-MIN★, D-SEQ★) hold trivially because M is unchanged. S8a in particular continues to hold of every pre-existing V-position by hypothesis on the pre-state; S8-depth continues to fix the same `m_C` (resp. `m_L`) per subspace because `dom(M(d))` is unchanged. Per-state invariants on C (C-fin, S7a, S7b, S7c) hold because each `a_k` is a well-formed content-subspace address with `zeros(a_k) = 3` and `#E(a_k) ≥ 2`, satisfying the per-address conditions. P6 (ExistentialCoherence; ASN-0047) holds at this intermediate because `origin(a_k) = d ∈ dom(M)` by INSERT's precondition, and `E` (equivalently `dom(M)` for documents) is unchanged at every intermediate by INS.frame.E. P7 (ProvenanceGrounding; ASN-0047) holds at this intermediate because R is unchanged by K.α; for each pre-state pair `(a, d') ∈ R`, `a ∈ dom(C)` by pre-state P7 and `dom(C)` only grows. L14 holds because `a_k ∉ dom(L)` (K.α's freshness precondition). L0's content clause holds because `subspace_I(a_k) = s_C` (SubAllocatorAxiom.Subspace / DisjointSubAllocatorChains — `a_k` is an output of `A_C(d)`), so every entry of the extended `dom(C)` still carries subspace identifier `s_C`. The composite-boundary properties (J0, J1★, P4★) are not yet required to hold at this intermediate — `a_k` is in `dom(C)` but not yet placed, which J0 would forbid at a composite boundary, but the intermediate is interior to the composite.

- *After step 2's K.μ⁻ (when fired).* `V_{s_C}(d_intermediate)` reduces to the Left prefix `{[s_C, 1, …, 1, k] : 1 ≤ k < p_m}`, which is sequential, contiguous, and starts at the minimum — D-SEQ★, D-CTG★, D-MIN★ all hold on the content subspace. Each retained position is a subset of the pre-state's `V_{s_C}(d)`; S8a (zero-free, depth `≥ 2`, all components positive) inherits unchanged from the pre-state, and every retained position has length exactly `m_C`, so S8-depth holds in subspace `s_C` with `m_C` unchanged. The link subspace is retained verbatim (`n'_{s_L} = n_{s_L}`): `V_{s_L}(d_intermediate) = V_{s_L}(d)` pointwise (positions and images alike). Per-state invariants on the link subspace at the intermediate are inherited bit-for-bit from the pre-state: S8a and S8-depth (with `m_L` unchanged) follow from the unchanged set; D-CTG★, D-MIN★, and D-SEQ★ on `V_{s_L}(d_intermediate)` each follow from their pre-state forms applied to the unchanged set — D-CTG★ because the same positions retain the same contiguity structure under the V-ordering, D-MIN★ because `min(V_{s_L}(d_intermediate)) = min(V_{s_L}(d))` is preserved, and D-SEQ★ because the enumeration `V_{s_L}(d) = {[s_L, 1, …, 1, k] : 1 ≤ k ≤ n_{s_L}}` carries over unchanged. CL-OWN and CL-UNIQ on the link-subspace mappings also inherit verbatim. S8-fin holds because `dom(M(d_intermediate))` is a subset of the finite pre-state `dom(M(d))`. S3★ holds because retained images are unchanged and S3★ held of the pre-state. P4★ (composite-boundary) would not hold at this intermediate if it required all post-state ran(M(d)) entries to be in R — but R has not yet been extended; the obligation is delegated to the composite boundary.

- *After step 3's K.μ⁺.* `V_{s_C}(d_intermediate)` extends to the full post-state `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}`, satisfying D-SEQ★, D-CTG★, D-MIN★. Every newly added V-position is one of the Insertion positions `shift(p, k) = [s_C, 1, …, 1, p_m + k]` for `0 ≤ k < n` or one of the Shifted-right positions `shift(v, n) = [s_C, 1, …, 1, v_m + n]` for `v ∈ V_{s_C}(d)` with `v ≥ p`. For each, we verify S8a and S8-depth explicitly:
   - *Insertion positions.* Split by `k`. At `k = 0`: `shift(p, 0) = p` by OrdinalShiftBase (ASN-0058); `#shift(p, 0) = #p = m_C` preserves S8-depth, and S8a transfers directly from `p`'s own S8a (`p = [s_C, 1, …, 1, p_m]` is zero-free, depth `m_C ≥ 2`, all components positive by ValidInsertionPosition/ValidFirstInsertionPosition postcondition (b), ASN-0036). At `k ≥ 1`: `shift(p, k) = p ⊕ δ(k, m_C)` by the OrdinalShift definition (ASN-0034). By TumblerAdd's result-length identity, `#shift(p, k) = m_C` — S8-depth's per-subspace fixed depth `m_C` for `s_C` is preserved. By OrdAddHom (b clause, ASN-0036), `subspace(shift(p, k)) = subspace(p) = s_C ≥ 1`. The leading `m_C − 1` components are inherited from `p` and are all `1` (since `p = [s_C, 1, …, 1, p_m]`); the final component is `p_m + k ≥ p_m ≥ 1`. So `zeros(shift(p, k)) = 0` and every component is strictly positive — S8a holds.
   - *Shifted-right positions.* For `v = [s_C, 1, …, 1, v_m] ∈ V_{s_C}(d)` with `v ≥ p`, the pre-state S8a ensures `v_m ≥ 1`. `shift(v, n) = v ⊕ δ(n, m_C)` has length `m_C` (S8-depth preserved), subspace `s_C` (OrdAddHom (b)), leading components all `1`, and final component `v_m + n ≥ 1 + 1 = 2 > 0`. So `zeros(shift(v, n)) = 0` and S8a holds.

  Every newly arranged content-subspace I-address is in `dom(C)` already (the freshly allocated `a_k` from step 1, or the pre-existing M(d)(v) for Shifted-right) — S3★ holds. S8-fin holds because `dom(M(d_intermediate))` is finite — it grows by at most `n + |R|` positions where `R` is the pre-state Right region, both finite. J0 (composite-boundary) is now satisfied: each `a_k ∈ dom(C')` has a placement at `shift(p, k)`.

- *After each of the `n` K.ρ firings of step 4.* R extends by one `(a_k, d)` pair. The composite-boundary coupling J1★ requires every newly-arranged content-subspace I-address to be in R'; after all `n` firings, J1★ holds. P4★ (`Contains_C(Σ') ⊆ R'`) holds because every content-subspace range entry of M'(d) is either a pre-state entry (already in R via pre-state P4★) or an Insertion-region freshly allocated `a_k` (now in R via step 4). P4a (HistoricalFidelity) holds because each `(a_k, d) ∈ R'` corresponds to the substrate state at the end of step 3 where `a_k ∈ ran(M'(d))`. P7 (ProvenanceGrounding; ASN-0047) holds at this intermediate because the new R-entry `(a_k, d)` satisfies `a_k ∈ dom(C)` — by the forced ordering of step 1's K.α(a_k) firing before step 4's K.ρ(a_k, d) firing — and pre-state R entries inherit by P0; the per-state predicate P7 is therefore preserved across each K.ρ commit.

The decomposition is admissible under ValidComposite★ because (i) every elementary transition's per-step precondition is met at its intermediate state, and (ii) the composite-boundary coupling constraints J0, J1★, J1'★ hold at the boundary `Σ →* Σ'`.

The composite is *not* admissible in alternative decompositions that would break a per-state invariant at an intermediate:

- *K.μ⁺ before K.α* (place `a_k` before allocating it). K.μ⁺'s precondition requires `a ∈ dom(C)` for every new mapping. The intermediate before K.α has `a_k ∉ dom(C)`, so K.μ⁺ cannot fire — the decomposition is ill-typed.

- *K.μ⁺ without prior K.μ⁻ in an interior insertion.* K.μ⁺ extends `dom(M(d))`; it preserves existing mappings. To map both `[s_C, 1, …, 1, p_m]` to `M(d)([s_C, 1, …, 1, p_m])` (the original content) and to `a_0` (the new content) would violate S2 — per-state functionality. So shift via K.μ⁻ + K.μ⁺ is *required*, not an implementation choice.

- *K.μ⁻ retaining strictly less than the Left prefix.* Both retention parameters of K.μ⁻ are admissible across `{0, 1, …, n_S}` per K.μ⁻'s precondition. A decomposition with `n'_{s_C} = 0` (full content-subspace shrinkage) is well-typed: the intermediate has `V_{s_C}(d_intermediate) = ∅` and satisfies D-CTG★, D-MIN★, D-SEQ★ vacuously. The subsequent K.μ⁺ may re-add the full sequential run `{[s_C, 1, …, 1, k] : 1 ≤ k ≤ N + n}` starting from the minimum, mapping each position to the appropriate I-address. The K.μ⁺ precondition requires only that the resulting M'(d) satisfies D-CTG★ and D-MIN★ — it does not require new positions to be added only at the high end. Such alternative decompositions are admissible and reach the same Σ'.

The post-state Σ' is *uniquely determined* by the operation contract; the substrate decomposition that realises it is not. We verify uniqueness component by component.

  *Content store.* Every admissible decomposition fires exactly `n` K.α steps in their forced order (per the K.α strict-order argument below — the `k`-th firing must produce the determined chain element `t_{m_d + k + 1}` of `A_C(d)`). So `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}` with each `a_k` determined uniquely by the pre-state's chain index `m_d` (read from `Σ.C`) and the inputs; the value `C'(a_k) = v_k` is set by the K.α firing's value parameter `v_k` from INSERT's input sequence. The frame of every other elementary step (K.μ⁻, K.μ⁺, K.ρ) leaves C unchanged, so `C'(a) = C(a)` for `a ∈ dom(C)` is preserved by composition.

  *Arrangement of `d`.* At the boundary, `V_{s_C}(d')` equals Left ∪ Insertion ∪ Shifted-right by INS.M-left, INS.M-insert, INS.M-shift; these three regions and the mapping on each are fully determined by `p`, `n`, the determined `a_k`, and the pre-state `V_{s_C}(d)`. Any admissible decomposition reaches this M'(d) at the boundary because the K.μ⁻ + K.μ⁺ pair must (i) remove every pre-state position with `v ≥ p` and reintroduce it at `shift(v, n)` (forced by INS.M-shift), (ii) introduce each Insertion position `shift(p, k) ↦ a_k` (forced by INS.M-insert), and (iii) leave the Left region intact (forced by INS.M-left). Whether the K.μ⁻ retention parameter is `n'_{s_C} = p_m − 1` (retain Left) or `n'_{s_C} = 0` (retain nothing), the K.μ⁺ step (or steps) must re-add exactly the missing positions to satisfy the boundary, so the final M'(d) is identical in either decomposition.

  *Arrangement of other documents.* `M'(d') = M(d')` for `d' ≠ d` by every elementary step's frame, regardless of decomposition.

  *Other components.* `L' = L`, `E' = E`, `dom(M') = dom(M)` by the frame of every elementary step in the composite (no K.λ, no K.δ, no K.σ fires); `R' = R ∪ {(a_k, d) : 0 ≤ k < n}` because step 4 adds exactly these `n` pairs in some order — set union being order-independent, R' is identical across decompositions.

Two representative comparisons confirm: a decomposition with `n'_{s_C} = p_m − 1` (the canonical choice) and one with `n'_{s_C} = 0` (full shrinkage) reach different intermediate states (the latter has empty V_{s_C} at the intermediate, the former retains the Left prefix), but both arrive at the same Σ'. K.μ⁻ retention parameters may range over `{0, 1, …, p_m − 1}` for the content subspace, K.μ⁺ may be split across multiple firings, and K.α + K.ρ firings may be reordered to a degree (described below), provided each intermediate satisfies the per-state invariants.

Among the elementary firings, three forced orderings arise from K.α firings and a fourth arises from K.μ⁻'s relationship to K.μ⁺ when K.μ⁻ fires. Every remaining pair commutes at the per-state level.

The three K.α-induced forced orderings:

- *K.α(a_k) before K.α(a_{k+1}).* The forced ordering arises from K.α's side-effect dependency through `dom(C)`, not from definitional precedence between chain elements. The chain elements `t_{m_d + 1}, t_{m_d + 2}, …` are determinately fixed by ChainEnumerationInjectivity (ASN-0093) as a strictly increasing enumeration of `A_C(d)`'s emissions, independent of which K.α firing produces them. What forces the ordering is K.α's *consultation* of `dom(C)`: K.α's subsequent-emission predicate (ASN-0093) computes its output as `inc(max{a' ∈ dom(C) : origin(a') = d}, 0)`. The first K.α firing of INSERT consults `dom(C)` and finds the chain index `m_d` (the number of pre-existing `A_C(d)` emissions), then either fires the first-emission case (when `m_d = 0`, producing `[d.0.s_C.1] = t_1`) or the subsequent-emission case (producing `t_{m_d + 1}`). The output of this first K.α firing — call it `a_0` — is committed to `dom(C)` by SequentialTransitionAxiom (ASN-0093) before any further transition can observe state. The second K.α firing then consults the *updated* `dom(C)` (which now includes `a_0` by the side-effect of the prior commit), finds the new max element to be `a_0`, and produces `inc(a_0, 0) = t_{m_d + 2}`. The ordering is forced by the sequential side-effect dependency: the second firing's output depends on `dom(C)`'s state, which is changed by the first firing's commit. Were the firings reordered, the second firing would still consult `dom(C)` and find chain index `m_d` (the pre-state's), still produce `t_{m_d + 1}`; this "second" firing would then collide with the still-pending "first" firing's intended output. The forced order is dictated by which firing's commit observes which `dom(C)` state, not by any definitional dependency of `a_1`'s value on `a_0`'s prior `dom(C)` membership.

- *K.α(a_k) before K.μ⁺ placing `a_k`.* K.μ⁺'s precondition requires each new mapping's image to be in `dom(C)`. If K.μ⁺ attempted to add `shift(p, k) ↦ a_k` before the K.α firing that produces `a_k`, the intermediate would have `a_k ∉ dom(C)` and the per-step precondition would fail.

- *K.α(a_k) before K.ρ(a_k, d).* K.ρ's precondition requires `a ∈ dom(C)`. K.ρ(a_k, d) firing before K.α(a_k) would find `a_k ∉ dom(C)` and the per-step precondition would fail.

The fourth, conditional on K.μ⁻ firing:

- *K.μ⁻ before K.μ⁺* (whenever K.μ⁻ fires in the composite — that is, for interior insertions and for `j = 0` insertions, where the Right region is non-empty and `n'_{s_C} < n_{s_C}` is required). K.μ⁺'s extension precondition requires `(A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))` — that is, K.μ⁺ preserves the image of every V-position already in the document's arrangement. Consider firing K.μ⁺ before K.μ⁻ for any interior insertion: at least one position `v ∈ V_{s_C}(d)` with `v ≥ p` is in the pre-K.μ⁺ domain `dom(M(d))` and would need to receive a new image under K.μ⁺. Concretely, at `j ∈ {0, …, N−1}` the position `shift(p, 0) = p` (when `j = 0`) or `p` itself (interior) is in pre-state `dom(M(d))` with `M(d)(p) ≠ a_0`, so K.μ⁺ attempting to add `p ↦ a_0` would violate its functional-extension precondition. K.μ⁻ must fire first to remove the Right region from `dom(M(d))`, so that K.μ⁺'s subsequent additions extend a domain disjoint from the Right region. The forced ordering is conditional: when K.μ⁻ is omitted (the `j = N` append case and the empty pre-state case), there is no fourth ordering, because K.μ⁺ adds positions only outside the existing domain.

Every remaining pair commutes at the per-state level:

- *K.μ⁻ commutes with every K.α.* K.μ⁻'s precondition `dom(M(d)) ≠ ∅` depends only on M, not on C; its effect modifies M only. K.α's precondition (freshness against `dom(C) ∪ dom(L)`) and its chain emission discipline depend only on C and L. Neither operation's precondition is sensitive to the other's effect, and both can fire in either order against the same pre-state without violating any per-state invariant.

- *K.ρ commutes with K.μ⁻ and K.μ⁺.* K.ρ's precondition depends only on C and the entity set; its effect modifies only R. K.μ⁻ and K.μ⁺ modify only M and depend (besides M itself) on C only for K.μ⁺'s `a ∈ dom(C)` clause. K.ρ does not consult M; K.μ⁻ and K.μ⁺ do not consult R. J1★ is a composite-boundary coupling, not a per-state invariant — it constrains `R'` at the boundary, but does not require K.ρ(a_k, d) to fire after K.μ⁺ within the composite. As long as both K.α(a_k) and K.ρ(a_k, d) commit somewhere in the composite (in that order), J1★ is satisfied regardless of K.ρ's position relative to K.μ⁺. Concretely, K.ρ(a_k, d) may fire *before* K.μ⁺ places `a_k` at `shift(p, k)`: the composite-boundary couplings J0, J1★, J1'★ are evaluated at the final state Σ', at which both the K.ρ-deposited pair `(a_k, d) ∈ R'` and the K.μ⁺-deposited placement `shift(p, k) ↦ a_k ∈ M'(d)` have committed, irrespective of their intermediate order; the boundary observes the joint final commit, so the ordering K.ρ-before-K.μ⁺ is admissible exactly because the boundary couplings do not consult intermediate states. *This admissibility relies on composite-level atomicity (INS.pre).* If K.ρ(a_k, d) fires before K.μ⁺ places `a_k`, the intermediate state between K.ρ and K.μ⁺ has `(a_k, d) ∈ R` but `a_k ∉ ran(M(d))` — a state that *would* violate J1'★ (ProvenanceRequiresExtensionContentSubspace; ASN-0047) if it were observable as a composite boundary. Under INS.pre's composite-atomicity precondition, no other composite can observe this intermediate as a boundary candidate — INSERT's elementaries are a contiguous run in the global transition order over the resources INSERT depends on (item (i) of INS.pre, the `A_C(d)` chain emission state, and item (ii), `M(d)`'s text subspace; R is implicitly within the atomicity envelope for INSERT-discharged J1'★ pairs because R-entries with `(a_k, d)` for fresh `a_k` are coupled to the same `A_C(d)` chain). So J1'★ is enforced only at INSERT's final state Σ' under INS.pre, at which both `(a_k, d) ∈ R'` and `shift(p, k) ↦ a_k ∈ M'(d)` have committed, and the boundary obligation is satisfied. Without composite-atomicity, the K.ρ-before-K.μ⁺ ordering is unsafe: another composite checking J1'★ at the intermediate would witness the unmatched R-entry. Under the weaker substrate environment, the canonical K.ρ-after-K.μ⁺ ordering (step 4 after step 3 in the canonical decomposition) is the only safe choice — it ensures every R-entry is matched by a placed I-address at every intermediate, not merely at the composite boundary.

- *K.ρ firings commute among themselves.* Different K.ρ firings have independent effects on R (set union is order-independent), and a later K.ρ(a_k, d) firing does not modify the precondition of any other K.ρ.

The canonical decomposition (steps 1–4 above) places K.ρ firings at the end purely for exposition; an alternative decomposition could interleave K.ρ(a_k, d) immediately after K.α(a_k), or fire it after K.μ⁻ but before K.μ⁺, without compromising any invariant or boundary obligation.

This is what Nelson calls "all changes, once made, leave the file remaining in canonical order, which was an internal mandate of the system." Implementations realise the composite via transactional sequencing, locking, copy-on-write, or log-and-commit — but the choice of decomposition is below the level of abstraction at which INSERT is specified. External observers see the composite boundary; the intermediate states are not externally observable.

The contract distinguishes two atomicity levels. *Elementary-level atomicity* — each individual elementary transition `Σ_i → Σ_{i+1}` is uninterruptible and totally ordered against every other — is supplied unconditionally by SequentialTransitionAxiom (ASN-0093). *Composite-level atomicity* — no elementary transition of any other composite interleaves between INSERT's elementaries — is *not* entailed by SequentialTransitionAxiom; it is a stronger property that the substrate environment must supply, and INSERT requires it as a precondition (see the composite atomicity assumption in the Operation's Formal Contract). Without composite-level atomicity, two concurrent INSERT composites on the same document would interleave their K.α firings: each consults the chain index `m_d` of `A_C(d)` at the moment of its own K.α, and the determined `a_k` of one composite would shift if another composite committed an intervening chain emission. The freshness argument still holds for each individual K.α (its precondition is evaluated against the actual immediately-preceding state, not against the operation's pre-state Σ), but the post-state Σ' is then a joint product of both composites, not the contract specified here.

The composite-atomicity precondition is therefore part of INSERT's specification, not an implementation footnote. An abstract specification of a substrate composite is well-defined only over a substrate environment providing this property, and the substrate must mark how it does so (single-threaded serialisation, per-document locking, or any other mechanism that prevents inter-composite elementary interleaving on the affected document and its allocator chain).

## Weakest-Precondition Analysis

The verification above proceeds forward — from preconditions and substrate effects to the post-state. We can also reason backward from a desired postcondition to the pre-state condition that secures it. This is Dijkstra's `wp` calculus, and we apply it to two non-trivial postconditions.

**Discoverability preservation.** Consider the postcondition `discoverable_from(ℓ, d, ·)` for a fixed link `ℓ ∈ dom(L)` and the operation's target document `d`. We compute:

  `wp(INSERT(d, p, ⟨v_0, …, v_{n−1}⟩), discoverable_from(ℓ, d, ·))`

By LP12 (DiscoverabilityCharacterisation; ASN-0098), `discoverable_from(ℓ, d, Σ')` is equivalent to `(E i : coverage(Σ'.L(ℓ).e_i) ∩ ran(Σ'.M(d)) ≠ ∅)`. By LP3★ (MultiStepCoverageInvariance; ASN-0098), `coverage(Σ'.L(ℓ).e_i) = coverage(Σ.L(ℓ).e_i)` since INSERT does not alter `L`. By the post-state's M-effect, `ran(M'(d)) = ran(M(d)) ∪ {a_k : 0 ≤ k < n}` — the pre-existing range augmented by the freshly allocated I-addresses. The wp expands to:

  `(E i : coverage(Σ.L(ℓ).e_i) ∩ (ran(Σ.M(d)) ∪ {a_k : 0 ≤ k < n}) ≠ ∅)`

which distributes to:

  `discoverable_from(ℓ, d, Σ) ∨ (E i, k : 0 ≤ k < n : a_k ∈ coverage(Σ.L(ℓ).e_i))`

The second disjunct — fresh-address capture — collapses to `false` for any *tight* endset `e_i` (with `tight(e_i, Σ_{e_i})` evaluated at the state of `e_i`'s incorporation). LP19a (TightFreshness; ASN-0098) establishes that a freshly allocated `a_k` cannot lie in a tight endset's coverage, because `a_k ∉ dom(Σ_{e_i}.C) ∪ dom(Σ_{e_i}.L)` by Store Monotonicity★ and the freshness of K.α's emission against the operation's pre-state. Thus, when every slot of `Σ.L(ℓ)` is tight at its incorporation state, the wp simplifies to:

  `wp(INSERT(d, p, ⟨v_0, …, v_{n−1}⟩), discoverable_from(ℓ, d, ·)) ≡ discoverable_from(ℓ, d, Σ)`

— a non-trivial conclusion: discoverability of a tight-endset link from `d` is preserved exactly when it held at the pre-state. INSERT neither creates nor destroys discoverability for tight links; it is transparent to them.

**P4★ for a specific I-address.** Consider the postcondition `(a, d) ∈ R'` for a fixed I-address `a` and target document `d`. We compute:

  `wp(INSERT(d, p, ⟨v_0, …, v_{n−1}⟩), (a, d) ∈ R')`

By the post-state's R-effect, `R' = R ∪ {(a_k, d) : 0 ≤ k < n}` where `a_0, …, a_{n−1}` are the freshly allocated content addresses. Thus `(a, d) ∈ R'` holds iff `(a, d) ∈ R` or `a ∈ {a_0, …, a_{n−1}}`. The second disjunct depends on the K.α emission discipline: `a = a_k` for some `k` iff `a` is the `(m_d + k + 1)`-th element of the chain `A_C(d)` (where `m_d` is the chain index of the last emission already in `dom(Σ.C)` for origin `d`). For a fixed `a`, this is a structural predicate on the pre-state: either `a` lies in `dom(C)` already (and is *not* a freshly allocated address — the second disjunct fails) or `a` is one of the next `n` chain elements of `A_C(d)` that K.α will produce. The wp is therefore:

  `(a, d) ∈ R  ∨  a ∈ {next n chain elements of A_C(d) starting from chain index m_d + 1}`

where the second-disjunct chain elements are determined by `Σ.C` and the chain enumeration of `A_C(d)`. The pre-state condition is operationally decidable: the chain index `m_d` is recoverable from `Σ.C` via the chain enumeration, and the next `n` chain elements are then determined.

This wp captures both the substrate's effect on R and the structural determinism of the K.α firings — the pre-state condition is a Boolean combination of a pre-state predicate (`(a, d) ∈ R`) and a substrate-derivable property (chain membership), reflecting INSERT's combined provenance-recording and fresh-allocation behaviour.

## Position Constraints

We claim INSERT is permitted at any valid insertion position — beginning, middle, end, and on the first insertion into an empty document. The empty and non-empty cases use *different* precondition predicates with different operational characters.

**Non-empty case (predicate `ValidInsertionPosition(d, p)`, ASN-0036).** For non-empty `V_{s_C}(d)` with cardinality `N`, the `N + 1` valid positions correspond to:

- `j = 0`: insertion at the very beginning. Left is empty (no `v < p`); the entire pre-state text subspace shifts by `n`. K.μ⁻ in the composite shrinks `V_{s_C}(d)` to `∅` (`n'_{s_C} = 0`); K.μ⁺ re-adds Insertion + Shifted-right at the original positions advanced by `n`.
- `j = N`: insertion at the end (append). Shifted-right is empty (no `v ≥ p`, since `p = shift(min, N)` and `max(V_{s_C}(d)) = shift(min, N−1) < p`); no shift occurs. K.μ⁻ is *omitted* from the composite (no strict shrinkage required); K.μ⁺ adds only the Insertion positions at the high end of the existing sequence.
- `j ∈ {1, …, N−1}`: interior insertion. Both Left and Shifted-right are non-empty; both are realised through K.μ⁻ (retaining Left) + K.μ⁺ (adding Insertion + Shifted-right).

The non-empty case's depth parameter is fixed by S8-depth (ASN-0036): `m_C` is the common depth of the pre-state `V_{s_C}(d)`, and the caller cannot choose otherwise.

**Empty case (predicate `ValidFirstInsertionPosition(d, p, m)`, ASN-0036).** For empty `V_{s_C}(d)`, the unique valid position is `[s_C, 1, …, 1]` of caller-chosen depth `m ≥ 2`. This case has operationally distinct features from the non-empty case:

- The precondition is the *ternary* predicate `ValidFirstInsertionPosition(d, p, m)`, which takes `m` as a third argument (the chosen depth), versus the *binary* `ValidInsertionPosition(d, p)`.
- The depth `m` is an operational input chosen by the caller; the strand model fixes only the lower bound `m ≥ 2`.
- K.μ⁻ is *omitted* from the composite (pre-state has nothing to retain — `dom(M(d))` may still contain link-subspace positions, but `V_{s_C}(d) = ∅` means K.μ⁻ cannot strictly shrink the content subspace while preserving the link subspace).
- The post-state, with `V_{s_C}(d') ≠ ∅` for the first time, triggers S8-depth's enforcement of `m_C = m` for all subsequent text-subspace operations on `d`.

The two cases share the post-condition shape (Left ∪ Insertion ∪ Shifted-right partition with appropriate emptiness), but their precondition predicates and composite structures differ.

The edge cases within each case (Left empty, Shifted-right empty) require no special handling in the post-condition specification: the universal forms of the three regions handle them uniformly, with quantifier-bounded clauses vacuously satisfied when a region is empty.

The "no positional constraint" intent (Q6) is borne out: the operation is uniformly defined across the position space. The specific *append* operation Nelson lists as a separate convenience (APPEND) is the `j = N` case of INSERT — distinct in name only, since the caller does not need to know `N` if a separate API offers append directly, but identical in semantic effect.

## INSERT vs. COPY: Identity Through Allocation

Nelson (Q8) distinguishes INSERT from COPY — two operations that may produce visually identical Vstream effects but completely different Istream consequences. We address the distinction only to fix the identity character of INSERT; COPY's full operation specification is out of scope for this ASN.

INSERT allocates *fresh* I-addresses for new content. The defining clause of the content-store effect — `dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}` with each `a_k` fresh — is the structural guarantee that the new content is new. Each `a_k` has `origin(a_k) = d`: attribution accrues to `d`'s owner, royalties (if priced) flow to `d`'s account.

Two independent users who INSERT the word "the" into their respective documents produce two distinct addresses, two distinct origins; neither is a copy or transclusion of the other. The system tracks identity by allocation event, not by value. If their bytes happen to coincide — both authors wrote "the" — the system observes this as two unrelated allocations, not one shared content.

COPY (out of scope here) creates V→I mappings to *existing* I-addresses without allocating new content. The original document remains the home of the bytes; attribution stays with the original author. The Vstream effect can be made indistinguishable from an INSERT — the same V-positions populated with the same visible content — but the underlying Istream identity is fundamentally different.

### Derived corollaries of INS.identity

The identity-by-allocation property has explicit consequences for the system. We derive three.

*Corollary (cross-document allocation independence).* If two distinct documents `d_1 ≠ d_2` each invoke INSERT with the same value sequence `⟨v_0, …, v_{n−1}⟩` at any positions, they produce two disjoint sequences of fresh I-addresses `⟨a_0^{(1)}, …, a_{n−1}^{(1)}⟩` and `⟨a_0^{(2)}, …, a_{n−1}^{(2)}⟩` with `origin(a_k^{(1)}) = d_1 ≠ d_2 = origin(a_k^{(2)})`. The two address sets are disjoint by SubAllocatorAxiom.Disjointness (ASN-0047): `dom(A_C(d_1)) ∩ dom(A_C(d_2)) = ∅` for `d_1 ≠ d_2`. Value coincidence at `Σ.C(a_k^{(1)}) = Σ.C(a_k^{(2)})` is observable but does not produce identity — the system observes it as two unrelated allocations.

*Corollary (version chain independence).* When a version `d_v = inc(d_src, 1)` is derived from `d_src` (out of scope here, but a substrate operation under K.δ-IsDocument) and subsequently INSERT is invoked on `d_v`, the freshly allocated `a_k` come from `A_C(d_v)` with `origin(a_k) = d_v ≠ d_src`. The original `d_src` retains its allocated content unchanged; the version's new content has its own attribution. This corollary depends on the per-document sub-allocator existence guaranteed by SubAllocatorAxiom for each `d_v ∈ E_doc` (ASN-0047).

*Corollary (link survivability through value coincidence).* If a tight endset `e` was incorporated at state `Σ_e` (with `tight(e, Σ_e)`), and a subsequent INSERT in any document produces a fresh `a_new` whose value `Σ'.C(a_new) = Σ_e.C(a')` for some `a' ∈ coverage(e)`, then `a_new ∉ coverage(e)`. By LP19a (TightFreshness; ASN-0098), tight endsets cannot accidentally capture freshly allocated content — the endset's coverage is a set of I-addresses, not a set of values, and a fresh `a_new` is by construction outside `dom(Σ_e.C) ∪ dom(Σ_e.L)` and therefore outside the tight coverage. The link does not silently expand to capture the new (coincidentally identical) content.

The identity-by-allocation property of INSERT is foundational. All higher-level properties of the system — traceability of content to its author, royalty accounting, link survivability, version comparison via shared identity — depend on it. An implementation that silently de-duplicated content during INSERT (identifying identical bytes from independent allocations) would violate this property and corrupt every dependent guarantee. The specification therefore forbids it: each `a_k` is a *fresh* address, produced by `A_C(d)`'s allocator chain, with no negotiation of equivalence.

## Bounding the Scope

The specification given here is INSERT for the content subspace. It does not cover:

- Insertion into the link subspace; the foundation's `K.μ⁺_L` is a structurally different operation with its own semantics, and link allocation through `K.λ` differs from content allocation through `K.α` in the requirement of an N-endset value structure.
- COPY, which creates V→I references without content allocation. Out of scope.
- DELETE and REARRANGE; these are governed by other transitions in the substrate's vocabulary.
- Version derivation. INSERT does not create versions; a separate K.δ-style entity-creation operation handles that.
- Inter-server replication. The specification describes INSERT within a single local state; cross-server propagation is the BEBE protocol's concern.

What the specification *does* cover is the precise per-state effect of one INSERT on one document at one position, including every invariant that must continue to hold after the operation.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| INS.def | INSERT(d, p, ⟨v_0, …, v_{n−1}⟩) is a substrate composite Σ →* Σ' under ValidComposite★ (ASN-0047), realised as n K.α + (optional K.μ⁻) + K.μ⁺ + n K.ρ | introduced |
| INS.pre | INSERT preconditions: d ∈ dom(M); p valid in text subspace of d (binary predicate ValidInsertionPosition for non-empty case, ternary predicate ValidFirstInsertionPosition(d, p, m) with caller-chosen m ≥ 2 for empty case); n ≥ 1; v_k ∈ Val; composite-atomicity assumption (no other composite's elementary transitions interleave between INSERT's elementaries on the affected document and its content sub-allocator chain) | introduced |
| INS.alloc | INSERT allocates exactly n fresh I-addresses from d's content sub-allocator A_C(d); each a_k satisfies origin(a_k) = d; each K.α firing satisfies its freshness precondition against its own intermediate state by ChainEnumerationInjectivity and FirstEmissionFreshness (ASN-0093) | introduced |
| INS.C | dom(C') = dom(C) ∪ {a_0, …, a_{n−1}}; C'(a_k) = v_k; ∀a ∈ dom(C): C'(a) = C(a) | introduced |
| INS.M-left | Text-subspace positions v < p in dom(M(d)) appear unchanged in M'(d) | introduced |
| INS.M-insert | M'(d)(shift(p, k)) = a_k for 0 ≤ k < n, reading shift(p, 0) = p per OrdinalShiftBase (ASN-0058) | introduced |
| INS.M-shift | For v ∈ V_{s_C}(d) with v ≥ p: shift(v, n) ∈ dom(M'(d)) ∧ M'(d)(shift(v, n)) = M(d)(v); discharged by I3 (ASN-0082) | introduced |
| INS.M-exhaustive | (A v : v ∈ dom(M'(d)) ∧ subspace(v) = s_C :: v ∈ Left ∪ Insertion ∪ Shifted-right); the post-state's text-subspace domain contains no s_C positions beyond the three regions, discharged by the substrate decomposition's K.μ⁻ + K.μ⁺ steps adding precisely those positions | introduced |
| INS.R | R' = R ∪ {(a_k, d) : 0 ≤ k < n}; discharges composite-boundary couplings J0, J1★, J1'★ (ASN-0047) | introduced |
| INS.frame.subspace | Non-content subspaces of d are unchanged (bidirectionally): {v ∈ dom(M'(d)) : subspace(v) ≠ s_C} = {v ∈ dom(M(d)) : subspace(v) ≠ s_C}, and M'(d) agrees with M(d) pointwise on that set. No new non-s_C positions appear; no existing ones are removed | introduced |
| INS.frame.doc | Other documents' arrangements are unchanged: ∀d' ≠ d: M'(d') = M(d') | introduced |
| INS.frame.L | L' = L: link store entirely unchanged | introduced |
| INS.frame.E | E' = E: entity set unchanged (no K.δ in the decomposition); specialises to dom(M') = dom(M) for documents | introduced |
| INS.frame.dom | dom(M') = dom(M): no new documents registered | introduced |
| INS.inv.immut | Content immutability S0 (ASN-0036) / P0 (ASN-0047) preserved: dom(C) ⊆ dom(C') and pointwise values preserved | introduced |
| INS.inv.identity | Permanent I-address identity preserved: ∀a ∈ dom(C): a ∈ dom(C'), C'(a) = C(a), origin(a) unchanged | introduced |
| INS.inv.func | M'(d) is a function (S2 preserved); Left, Insertion, Shifted-right regions are pairwise disjoint by TumblerAdd component arithmetic, with Shifted-right source uniqueness by TS2 (ASN-0034) | introduced |
| INS.inv.refint | Referential integrity S3★ (ASN-0047) preserved: ran(M'(d)) ⊆ dom(C') ∪ dom(L') per-subspace; discharged also by I3-S3 (ASN-0082) | introduced |
| INS.inv.seq | D-CTG★, D-MIN★, D-SEQ★ (ASN-0047) preserved in text subspace: V_{s_C}(d') is sequential with cardinality \|V_{s_C}(d)\| + n | introduced |
| INS.inv.depth | S8-depth (ASN-0036) preserved: in non-empty case m_C is unchanged; in empty case the first insertion fixes m_C = m for d at every subsequent state in which V_{s_C}(d) remains non-empty (a later K.μ⁻ emptying V_{s_C}(d) makes S8-depth vacuous and permits a different depth on the next first-insertion) | introduced |
| INS.inv.cross-subspace | Cross-subspace isolation: V_{s_L}(d') = V_{s_L}(d) with mappings unchanged | introduced |
| INS.inv.cross-doc | Cross-document isolation: arrangements of all d' ≠ d unchanged | introduced |
| INS.inv.coverage | Endset coverage unchanged for every link by LP3★ (ASN-0098): coverage depends only on L, which is preserved | introduced |
| INS.inv.discov | Pre-state discoverability preserved: every link discoverable from any document at Σ remains discoverable at Σ' | introduced |
| INS.proj | Projection-shift correspondence: project(ℓ, i, d', Σ') = π(project(ℓ, i, d', Σ)) ∪ N_{ℓ,i} where π is region-aware (identity on Left, shift-by-n on Right, identity for d' ≠ d and link subspace) and N_{ℓ,i} ⊆ {shift(p, k) : 0 ≤ k < n} captures Insertion images whose fresh a_k lies in coverage; N_{ℓ,i} = ∅ for tight endsets by LP19a (ASN-0098) | introduced |
| INS.atomicity | INSERT's substrate composite preserves per-state invariants (Class (a) of ASN-0047) at every intermediate state; composite-boundary properties (Class (b) — P4★, P4a, P7a) and coupling constraints (J0, J1★, J1'★) hold at the boundary Σ →* Σ'. Elementary-level atomicity is supplied by SequentialTransitionAxiom (ASN-0093); composite-level atomicity (no inter-composite interleaving) is required as a precondition (see INS.pre) and is a property of the substrate environment | introduced |
| INS.position | INSERT permitted at any valid position: N+1 valid positions under ValidInsertionPosition for non-empty V_{s_C}(d), plus single first-insertion position under ValidFirstInsertionPosition(d, p, m) with caller-chosen m ≥ 2 for empty case | introduced |
| INS.identity | INSERT creates fresh content identity: each a_k is a new allocation with origin(a_k) = d; INSERT cannot identify new content with any pre-existing I-address regardless of value coincidence | introduced |
| INS.identity.crossdoc | Cross-document allocation independence: two distinct documents inserting identical values produce disjoint fresh I-address sequences with distinct origins (by SubAllocatorAxiom.Disjointness, ASN-0047) | introduced |
| INS.identity.version | Version chain independence: INSERT on a derived version d_v allocates from A_C(d_v) with origin = d_v ≠ origin of d_v's source document | introduced |
| INS.identity.tightsurv | Link survivability through value coincidence: tight endsets cannot accidentally capture freshly allocated content by LP19a (ASN-0098) | introduced |

## Open Questions

- INSERT requires composite-level atomicity as a precondition (see INS.pre). What is the minimum substrate machinery that secures this property without forcing global serialisation — per-document locking on `d`, per-allocator-chain locking on `A_C(d)`, or something weaker? And what must an implementation provide to recover canonical order after a partial failure during the substrate composite?
- What invariants must an analogous insertion operation preserve when the target is the link subspace rather than the text subspace?
- Is INSERT closed under composition with itself — i.e., if `Σ →INSERT→ Σ_1 →INSERT→ Σ_2`, is there always a single INSERT from `Σ` to `Σ_2`, or do the intermediate effects accumulate in ways that no single INSERT can reproduce?
- What does the abstract specification say about concurrent INSERTs targeting the same V-position from independent agents — must the system serialise them, and if so, on what basis is the order chosen?
- What derived properties of a document — current size, last-modified marker, total I-address footprint — does INSERT update, and which of these are part of the abstract state versus derivable from it?
- What abstract guarantee constrains the order in which the K.α firings of step 1 of the substrate composite may be interleaved with the K.ρ firings of step 4, and does any such reordering produce an externally observable difference?
