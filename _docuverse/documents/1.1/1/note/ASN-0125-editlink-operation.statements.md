# ASN-0125 Claim Statements

*Source: ASN-0125-editlink-operation.md (revised 2026-06-12) — Extracted: 2026-06-13*

## EL0 — MutationExclusion (LEMMA, lemma)

For reachable `Σ₀`, `a ∈ dom(Σ₀.L)`, `ℓ₀ = Σ₀.L(a)`, and `w ≠ ℓ₀`:

Let `R_mut ≡ a ∈ dom(L) ∧ L(a) = w` and `J ≡ a ∈ dom(L) ∧ L(a) = ℓ₀`.

`J` holds at `Σ₀` by construction. By L12 (LinkImmutability) closed under `→*` — LP13 (UnconditionalLinkPersistence, ASN-0098) at `a`:

> `(A Σ' : Σ₀ →* Σ' : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = ℓ₀)`

Since `[J ⟹ ¬R_mut]` (a partial function has one value per key, and `w ≠ ℓ₀`), and `J` holds at every state of every schedule from `Σ₀`:

For every finite program `S` over the closed elementary vocabulary, `wp(S, R_mut)` evaluated at `Σ₀` is `false`.

---

## EL1 — IntentInvisibility (LEMMA, lemma)

Both descriptions — "I edited the link at `a`, producing the corrected value `ℓ'` homed at `d_s`" and "I created a brand-new link with value `ℓ'` homed at `d_s`" — denote the very same transition instance, `K.λ(d_s, a_emit(Σ, d_s), ℓ')`, applied to the very same state, hence they produce the same post-state `Σ₁`.

Emission alone records no relationship: for the post-state `Σ₁` of any single link allocation, every state predicate — and hence every observation, present or future — is invariant under whether the allocation was an edit of some existing link or an independent creation.

Consequently: value resemblance carries no relational information — the store legitimately holds distinct addresses with identical values (L11b, NonInjectivity, ASN-0043), and the state after a resembling independent creation coincides with the state after an unasserted "edit." There is no predicate of `Σ₁` that holds iff `ℓ'` "was derived from" `Σ.L(a)`.

---

## EL2 — NoInPlaceCarrier (LEMMA, proposition)

In every reachable state, the supersession record can live:

*(a) Not in the original's value.* `Σ.L(a)` is fixed by L12 from the moment of creation. No "superseded-by" annotation can ever be attached to `a`.

*(b) Not appended to the successor's value later.* The same invariant binds the successor the instant it exists: its slots are fixed at emission.

*(c) Not in the address relation between them.* Every allocated link address is an emission of its home document's flat sibling chain `A_L(d)` — first emission `[d.0.s_L.1]` with element-field depth `#E = 2`, successors by `inc(·, 0)` which preserves length (FirstEmission, ChainDiscipline, TA5(c), ASN-0093) — and at every reachable state the homed links form a contiguous initial segment of that chain (ChainMembershipForOrigin, ASN-0093). So every allocated link address has `#E = 2` exactly, while a nested version-of-link address would need `#E ≥ 3`. Stronger: `dom(Σ.L)` is a tumbler-prefix antichain (R0a, FlatLinkDomain, ASN-0086) — no allocated link address prefixes another. The address relation between any two allocated links carries exactly two readable facts: whether they share a home (T6-decidable from the prefixes), and, within one home, their emission order (T9, ASN-0034). Neither is semantic.

*(d) Not in an index marker.* The stored entities are exhausted by `dom(Σ.C) ∪ dom(Σ.L)` (L14, DualPrimitive, ASN-0043); the entity set `E` holds organizational addresses with no payload; the provenance relation `R` holds (content-address, document) pairs whose precondition `a ∈ dom(C)` excludes link targets outright (`K.ρ`, ASN-0047, with SD store disjointness); arrangement entries are V→I bindings within one document. There is no status field anywhere, and the only systematic asymmetry between two link entries is their addresses — case (c).

The record must therefore be a freshly allocated entity.

---

## RQ1–RQ7 — RecordRequirements (REQ, requirements)

Seven requirements on any carrier of the supersession relationship:

- **RQ1 (Post-hoc assertability).** The relationship must be assertable at any state where both endpoints exist — not only at the successor's creation.
- **RQ2 (Open authorship).** Any principal with a home document may assert.
- **RQ3 (Attribution).** The asserter must be decidable from the record alone.
- **RQ4 (Non-destructive disputability).** A claim must be withdrawable from current standing, and contestable, without erasing it or either endpoint.
- **RQ5 (Endpoint frame).** Asserting must modify neither endpoint.
- **RQ6 (Decidable specificity).** The relationship must be recognizable as supersession specifically — distinguishable from comment, counterpart, or coincidence — by the substrate's interpretation-free mechanisms: address and coverage comparison, never content exegesis. And it must be refinable: a correction is not a restyling, and the vocabulary must be able to grow subtypes.
- **RQ7 (Plurality).** Arbitrarily many claims over the same endpoints, including mutually contradictory ones, must be co-representable. Competing claims are resolved socially, never structurally.

---

## EL3 — RelationSpaceNecessity (LEMMA, theorem)

Under this substrate, any carrier satisfying RQ1–RQ7 is a freshly allocated link-store entity, distinct from both endpoints, referencing each endpoint by address through its endsets, and bearing its kind as the coverage class of a designated slot — that is, a typed link-to-link tuple.

Derivation:

RQ1 and RQ2 require the carrier to be created by a transition at arbitrary later states by arbitrary principals — so it is a fresh store entity; the vocabulary offers exactly two entity-creating store writers, `K.α` (content) and `K.λ` (links); `K.δ` and `K.ρ` were closed off in EL2(d).

RQ6 eliminates the content store: a claim encoded as content bytes has, to the substrate, no structure beyond an address and an origin — type machinery reads slot-3 *coverage* only (L8, TypeByAddress, ASN-0043). So the carrier is a link.

RQ1 makes it a link other than the successor — a third entity — since the successor's slots close at its birth (EL2(b)). Its reference to the endpoints must be substrate-visible, and the one mechanism links have for referencing anything is endset coverage; endsets may target link addresses (L4(c), ASN-0043), with the unit-depth span at an address as the canonical reference (L13, R5).

RQ6 fixes how the kind is carried: the only interpretation-free, decidable, refinable kind mechanism is the coverage class of the type slot (L8; decidability by CoverageEqualityDecidable, ASN-0086; refinement by prefix containment, L10).

RQ4 is satisfied because the carrier has its own address: it can be individually targeted while L12 holds it and both endpoints in the permanent record. RQ3 is its home prefix (T4b projection, decidable by T6). RQ5 is `K.λ`'s frame. RQ7 is freshness: every claim is a new address.

The genuinely distinct candidates were three: carry the claim in the value space (a slot of the successor), in the address space (nesting), or in the relation space (a typed tuple). The value space fails RQ1, RQ2, RQ4, and RQ7. The address space fails RQ1 and RQ2 (EL2(c) shows the substrate never reaches such an address, and an existing link can never retroactively become a version-of), fails RQ4 absolutely (baptized addresses are irrevocable — B0, T8, ASN-0040/0034), and fails RQ6 (one relation kind hard-wired into namespace structure, no siblings, no subtypes).

---

## Df-CLS — SupersessionClass (DEF, definition)

Fix a coverage class `[K_sup]`, `K_sup ∈ T_admissible`, with `coverage(K_sup) ≠ coverage(R)` — distinct from the retraction class (ASN-0086).

> `S^Σ := L_{K_sup}^Σ`

is the *supersession slice* at `Σ` — the historical record of claims.

> `A_sup^Σ := A_{K_sup}^Σ = {(b, F, G) ∈ S^Σ : b ∉ nullified(Σ)}`

is its operative subset. The members of `S^Σ` are called *claims*.

---

## Df-DIR — ClaimDirectionality (DEF, definition)

For a claim `(b, F, G) ∈ S^Σ`: the from-set `F` covers the *superseding* link, the to-set `G` the *superseded* — read "`F` replaces `G`."

This aligns with the layer's RetractionDirectionality (ASN-0086): the to-side is the side acted upon. A withdrawal with no replacement is not a degenerate supersession but a retraction, class `[R]`; the two acts remain distinct relations, and asserting the first never performs the second.

---

## Df-DISC — EditDiscipline (DEF, definition)

A state `Σ` is *edit-disciplined* iff:

*(i)* it is unit-depth-retraction-disciplined (ASN-0086), and

*(ii)* every claim conforms to the *claim schema*:

> `(A (b, F, G) ∈ S^Σ : (E x, y ∈ dom(Σ.L) : x ≠ y ∧ F = {(x, δ(1, #x))} ∧ G = {(y, δ(1, #y))}))`

— both endsets are canonical unit-depth spans at link-store addresses, and the claim is irreflexive. (Self-supersession `x = y` is excluded as vacuous; cycles of length ≥ 2 are deliberately not excluded — they are reverts.)

A layer is edit-disciplined iff every state it reaches is.

---

## EL4 — SingleTarget (LEMMA, lemma)

Each *schema-conforming* claim determines its endpoints uniquely — the argument is per-claim, invoking no whole-state discipline hypothesis.

For `e = (b, F, G) ∈ S^Σ` whose endsets meet the Df-DISC(ii) form with witnesses `x, y` (so `F = {(x, δ(1,#x))}`, `G = {(y, δ(1,#y))}`, `x, y ∈ dom(Σ.L)`, `x ≠ y`):

> `coverage(F) ∩ dom(Σ.L) = {x}`  and  `coverage(G) ∩ dom(Σ.L) = {y}`

*Proof.* `coverage({(x, δ(1, #x))}) = {t : x ≼ t}` (PrefixSpanCoverage, ASN-0043); for `t ∈ dom(Σ.L)` with `x ≼ t`, the antichain R0a forces `t = x`. Both facts are properties of the single claim `e` and of `dom(Σ.L)` at the ambient reachable state.

We may therefore write `addr(e) = b`, `new(e) = x`, `old(e) = y` as total accessors on any schema-conforming claim at any reachable state.

Write `Ŝ^Σ = {e ∈ S^Σ : e is schema-conforming}` for the schema-conforming claims; at an edit-disciplined state every claim conforms, so `Ŝ^Σ = S^Σ`.

---

## Df-SUCC — SuccessorRelations (DEF, definition)

At any state `Σ`, ranging over the schema-conforming claims `Ŝ^Σ` (EL4), on which `old`/`new`/`addr` are total:

> `succ_h(Σ) = {(old(e), new(e)) : e ∈ Ŝ^Σ}`  — the historical relation;

> `succ_o(Σ) = {(old(e), new(e)) : e ∈ Ŝ^Σ ∧ addr(e) ∉ nullified(Σ)}`  — the operative relation.

Both are finite (L-fin) relations on `dom(Σ.L)`, with `succ_o(Σ) ⊆ succ_h(Σ)`.

Restricting the comprehension to `Ŝ^Σ` keeps the relations total at every reachable state: the accessors are undefined on a non-conforming `[K_sup]`-class tuple — multi-span, or covering several link addresses or none — and a bare `K.λ` can emit one. At an edit-disciplined state `Ŝ^Σ = S^Σ`, so the comprehensions range over the whole supersession slice and coincide with the unrestricted reading.

---

## EL5 — RecordMonotonicity (LEMMA, lemma)

For every `Σ →* Σ'`:

*(a)* `S^Σ ⊆ S^{Σ'}`, `Ŝ^Σ ⊆ Ŝ^{Σ'}`, and `succ_h(Σ) ⊆ succ_h(Σ')`.

The slice inclusion is R3 (TypedSliceMonotonicity, ASN-0086) at `[K_sup]`, lifted across `→*` by finite composition; schema-conformance rides along, being value-and-domain-determined — a conforming claim's witnesses satisfy `x, y ∈ dom(Σ.L) ⊆ dom(Σ'.L)`, so it stays conforming at `Σ'` with the same `old`/`new`. Claims accumulate; none is ever lost.

*(b)* `nullified(Σ) ⊆ nullified(Σ')`.

The `[R]`-slice likewise only grows, so nullification is one-way (R6a, ASN-0086): a claim once retracted from operative standing never silently regains it (re-assertion is a new claim at a fresh address — the shape of R6c).

*(c)* `succ_o` is neither monotone nor antitone: emission adds operative pairs (EL6), `Nullify` removes them. The operative relation is the one revisable view; the historical relation is the unrevisable record.

---

## ASSERTop — AssertSup (DEF, operation)

Precondition: `x, y ∈ dom(Σ.L) ∧ x ≠ y ∧ d_a ∈ dom(Σ.M)`

> `assert_sup(x, y, d_a) ≜ Emit_{K_sup}(Σ, d_a, {(x, δ(1, #x))}, {(y, δ(1, #y))})`

One `K.λ` at home `d_a`, emitting the claim "`x` supersedes `y`" at the fresh address `b = a_emit(Σ, d_a)`. The spans are T12-well-formed (`Pos(δ(1, #x))`; action point `#x ≤ #x`), the slots are endsets, the arity is 3, and slot 3 is `K_sup ≠ ∅`, so `K.λ`'s L3 precondition is discharged.

---

## EL6 — AssertionContract (LEMMA, theorem)

When invoked at a reachable `Σ` satisfying its precondition, `assert_sup(x, y, d_a)` yields `Σ'` with:

*(i) Allocation.* Exactly one fresh address: `b ∉ dom(Σ.L) ∪ dom(Σ.C)` (emission freshness, ASN-0093), `home(b) = d_a`.

*(ii) Record.* `e_b = (b, {(x, δ(1,#x))}, {(y, δ(1,#y))}) ∈ S^{Σ'}` with `new(e_b) = x`, `old(e_b) = y`; hence `(y, x) ∈ succ_h(Σ')`.

*(iii) Active at birth.* If `Σ` is edit-disciplined, `b ∉ nullified(Σ')`, so `(y, x) ∈ succ_o(Σ')`. (ASN-0086 wp Case 2 under its disciplined simplification: the pre-existing-retraction conjunct holds vacuously at disciplined states, and `K_sup ≁ R` discharges the self-nullification guard.)

*(iv) Frame.* `Σ'.C = Σ.C`, `Σ'.M = Σ.M`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`; every prior link-store entry — `x` and `y` in particular — is unchanged.

*Unconditionally,* `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)`: the lone new tuple has slot-3 coverage `coverage(K_sup) ≠ coverage(R)`, so the `[R]`-slice does not grow and the nullification status of no pre-existing address changes — the superseded `y` is exactly as active as before.

*Under edit-discipline on `Σ`,* the full `nullified(Σ') = nullified(Σ)` follows: the only candidate new member is the fresh `b`, and the unit-depth retraction discipline together with the antichain R0a discharges wp Case 2's third conjunct (ASN-0086) — every pre-existing `[R]`-tuple's to-coverage is a unit-depth subtree rooted at a single existing link address, and the fresh `b ∉ dom(Σ.L)` is prefix-incomparable to each (R0a at `Σ'`), so no such to-coverage reaches `b` and `b ∉ nullified(Σ')`.

*(v) Discipline and permanence.* `Σ'` is edit-disciplined when `Σ` was; and at every `Σ' →* Σ''`, `e_b ∈ S^{Σ''}` with value fixed and `(y, x) ∈ succ_h(Σ'')` (EL5a).

---

## EDITop — Editlink (DEF, operation)

Precondition: `a ∈ dom(Σ.L) ∧ d_s, d_a ∈ dom(Σ.M) ∧ ℓ' L3-conforming ∧ DC(ℓ')`

> `editlink(a, ℓ', d_s, d_a) ≜`
> `  a' := a_emit(Σ, d_s);  Σ₁ := K.λ(d_s, a', ℓ');`
> `  (Σ₂, b) := assert_sup(a', a, d_a) at Σ₁;`
> `  return (Σ₂, a', b)`

The *discipline-conformance precondition* `DC(ℓ')` — a value-level predicate whose witnesses are drawn from the editlink pre-state `Σ`:

> if `coverage(ℓ'.e₃) = coverage(K_sup)`, then
> `(E x, y ∈ dom(Σ.L) : x ≠ y ∧ ℓ'.e₁ = {(x, δ(1, #x))} ∧ ℓ'.e₂ = {(y, δ(1, #y))})`;

> if `coverage(ℓ'.e₃) = coverage(R)`, then `(E t ∈ dom(Σ.L) : ℓ'.e₂ = {(t, δ(1, #t))})`.

If `coverage(ℓ'.e₃)` is neither `coverage(K_sup)` nor `coverage(R)`, `DC(ℓ')` is vacuous.

`assert_sup`'s precondition is discharged at `Σ₁`: `a' ∈ dom(Σ₁.L)` by the emission, `a ∈ dom(Σ₁.L)` by monotonicity, `a' ≠ a` by freshness, `d_a ∈ dom(Σ₁.M)` by M1.

---

## EL7 — EditContract (LEMMA, theorem)

When invoked at a reachable `Σ` satisfying its precondition, `editlink(a, ℓ', d_s, d_a)` yields `Σ₂` with:

*(i) What is allocated.* Exactly **two** fresh link-subspace addresses — the successor `a'` on `A_L(d_s)` and the claim `b` on `A_L(d_a)` — pairwise distinct from each other and from everything prior. No content address, no entity, no provenance entry, no arrangement change:

> `Σ₂.C = Σ.C ∧ Σ₂.M = Σ.M ∧ Σ₂.E = Σ.E ∧ Σ₂.R = Σ.R`

*(ii) The new reading.* `Σ₂.L(a') = ℓ'`, `home(a') = d_s`. The successor is born unlisted: the fresh `a'` lies in no arrangement range — `ran(Σ₂.M(d)) = ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)` (S3★), which `a'` is fresh against — so `listed(a', d, Σ₂)` is false for every `d`.

*(iii) The relationship.* `(a, a') ∈ succ_h(Σ₂)`, witnessed by the claim at `b`; at edit-disciplined `Σ`, also `(a, a') ∈ succ_o(Σ₂)`.

*(iv) The frame on the original.* `Σ₂.L(a) = Σ.L(a)` unconditionally (L12); listing is untouched (both steps frame `M`). `nullified(Σ₂) = nullified(Σ)` holds under edit-discipline on `Σ` and non-retraction successor value: neither fresh address `a'` nor `b` is caught by any pre-existing `[R]`-tuple's unit-depth to-coverage (freshness + R0a, the wp Case 2 argument of EL6(iv) applied at each of the two emissions, the intermediate `Σ₁` disciplined by EL7(vi)).

*(v) Permanence.* At every `Σ₂ →* Σ₃`: `a`, `a'`, `b` all persist with fixed values, and `(a, a') ∈ succ_h(Σ₃)`.

*(vi) Discipline preservation.* `Σ₂` is edit-disciplined when `Σ` is. Step 1, the bare `K.λ(d_s, a', ℓ')`, preserves Df-DISC: every prior claim keeps its witnesses (`x, y ∈ dom(Σ.L) ⊆ dom(Σ₁.L)`, values fixed by L12), every prior retraction likewise persists, and the one new value `ℓ'` at `a'` is governed by `DC(ℓ')` with witnesses pinned at `dom(Σ.L) ⊆ dom(Σ₁.L)`. The conformance transfers: if `ℓ'`'s slot-3 coverage is `coverage(K_sup)`, `DC(ℓ')` supplies `x, y ∈ dom(Σ.L) ⊆ dom(Σ₁.L)` with `x ≠ y`, and since `a' ∉ dom(Σ.L)` is fresh, neither witness is `a'`; if `coverage(R)`, `DC(ℓ')` supplies `t ∈ dom(Σ.L) ⊆ dom(Σ₁.L)`; if neither, Df-DISC constrains it not. Step 2, `assert_sup`, preserves edit-discipline by EL6(v).

---

## EL8 — ClaimStanding (LEMMA, theorem)

For every claim `e ∈ S^Σ` in a disciplined state:

*(a)* it is permanent in membership and value (EL5a);

*(b)* it is attributed: `home(addr(e)) = N(addr(e)).0.U(addr(e)).0.D(addr(e))` is computable from the address alone by field projection (T4b), decidably (T6), and identifies the document under whose prefix the claim was allocated. Resolving a home further to a named principal is an optional ASN-0042 overlay, not a function of `Σ`;

*(c)* it is open: the schema imposes no relation among `home(addr(e))`, `home(old(e))`, `home(new(e))` — first-party, second-party, and third-party claims are structurally identical, differing only in their visible provenance;

*(d)* it is itself addressable: `addr(e) ∈ dom(Σ.L)`, so claims can be the targets of endsets (L4(c)) — endorsed, disputed, commented, retracted (`Nullify`), or themselves edited (`editlink` applies to a claim, `DC` permitting) — with no new machinery;

*(e)* it is a claim, not a verdict: the substrate records who said what and adjudicates nothing.

---

## Definition — Listed

> `listed(t, d, Σ)` iff `(t, d) ∈ Contains(Σ)` (ASN-0047, CurrentContainment)

equivalently: `t ∈ ran(Σ.M(d))`, since `dom(Σ.M) = E_doc` (M1) discharges the `d ∈ E_doc` conjunct for every `d` ranged over.

Structural fact: for a link, only its home can list it — a link-subspace image has `origin = d` (CL-OWN, ASN-0047, with HomeOriginCoincidence), and a content-subspace image lies in `dom(C)` (S3★), which is disjoint from `dom(L)` (SD).

---

## EL9 — ThreeAxes (LEMMA, theorem)

For a link `a ∈ dom(Σ.L)`:

*(1) Resolution — permanent and unconditional.*

> `(A Σ' : Σ →* Σ' : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))`

Nothing gates the lookup: no arrangement state, no activity status, no provenance appears in it.

*(2) Listing — mutable in both directions.* The home registry is current view, not record. `K.μ⁻` de-lists (existence: contract the link subspace below `a`'s position and re-extend the survivors in order — each re-seating satisfies `K.μ⁺_L`'s precondition in turn, and D-SEQ★ shapes the result); `K.μ⁺_L` re-lists (`origin(a) = d ∧ a ∉ ran(M(d))` holds after de-listing).

*(3) Activity — monotone downward, per claim.*

> `active(a, Σ) ≡ a ∉ nullified(Σ)`

can only fall (EL5b), by an explicit, itself-permanent, itself-attributed retraction tuple; restoration is re-assertion at a fresh address, never reinstatement in place (R6c).

The axes are independent, and — by EL6(iv) — superseding moves none of them.

---

## EL10 — PositionEpochality (LEMMA, theorem)

Listing positions are not identifiers. There exist reachable `Σ →* Σ' →* Σ''`, a document `d`, a position `v`, and links `ℓ₁ ≠ ℓ₂` — both permanently resolvable throughout — with:

> `Σ.M(d)(v) = ℓ₁,  v ∉ dom(Σ'.M(d)),  Σ''.M(d)(v) = ℓ₂`

*Construction.* Let `d` list two links, `V_{s_L}(d) = {[s_L,1], [s_L,2]}` with `[s_L,2] ↦ ℓ₁`, and let `ℓ₂` be homed at `d` but unlisted (a bare `K.λ`). Apply `K.μ⁻` with link-subspace retention `n'_{s_L} = 1` (content retained in full); then `K.μ⁺_L` for `ℓ₂`: the substrate assigns `v_ℓ = shift(max(V_{s_L}(d)), 1) = shift([s_L,1], 1) = [s_L,2]` — the very position `ℓ₁` vacated, now bound to `ℓ₂`.

Corollary: surviving references must bind addresses, never positions. The claim schema (Df-DISC) already complies; the construction shows the compliance is load-bearing.

---

## EL11 — TwoRegimeDiscovery (LEMMA, theorem)

*(a) Contextual (arrangement-gated).* For a disciplined claim `e` and any document `d`:

> `project(Σ.L(addr(e)).e₂, d, Σ) ≠ ∅ ⟺ listed(old(e), d, Σ)`

*Proof.* By LP12 (ASN-0098): the left side is `coverage(G) ∩ ran(Σ.M(d)) ≠ ∅` with `G` the to-set. `coverage(G) = {t : old(e) ≼ t}` (EL4's computation). Any member of `ran(Σ.M(d))` lies in `dom(Σ.C) ∪ dom(Σ.L)` (S3★). No content address extends `old(e)` (writing `y = old(e)`, a `t ≽ y` has `E(t)₁ = s_L` contradicting `E(t)₁ = s_C` for content addresses; SC-NEQ). A link address extends `y` only if equal (R0a). So the intersection is `{y} ∩ ran(Σ.M(d))`, nonempty iff `y` is listed — and by Df-LISTED only at `d = home(y)`. Symmetrically for the from-side and `new(e)`.

*(b) Archival (arrangement-independent).* The predicates `e ∈ Ŝ^Σ` and `old(e) = y` are functions of stored values, decidable by coverage comparison (CoverageEqualityDecidable; T2 span membership; EL4). The claim sets

> `in(y, Σ) = {e ∈ Ŝ^Σ : old(e) = y}`  and  `out(x, Σ) = {e ∈ Ŝ^Σ : new(e) = x}`

are computable from `Σ.L` alone — this is `Observe_{K_sup}` at pattern `Ĝ = {y}` (resp. `F̂ = {x}`), view `hist`, filtered by the decidable schema-conformance predicate (a no-op at disciplined states), consulting no arrangement. The supersession question is answerable, completely and decidably, at every state, whatever every arrangement says.

---

## EL12 — ForkPermanence (LEMMA, theorem)

Two editors independently superseding the same link produce a permanent, co-visible fork.

Run `editlink(a, ·, ·, ·)` twice from any disciplined reachable state, in any combination of homes: freshness yields distinct successors `a'₁ ≠ a'₂` and distinct claims `e₁ ≠ e₂` (same home: the chain advances past the first emission; different homes: cross-document disjointness with T10); both `(a, a'₁)` and `(a, a'₂)` enter `succ_h` — permanently (EL5a) — and `succ_o` at birth (EL6(iii), the second invocation's active-at-birth conclusion resting on EL7(vi): the first `editlink` leaves the intermediate state edit-disciplined); and the vocabulary contains no transition that merges, ranks, or removes either.

The complete competing-claim set, with asserters, is one archival query: `in(a, Σ)`.

Without the assertion steps the same two emissions leave `succ_h` untouched: by EL1 the "fork" of intentions never existed in state. Fork visibility is exactly assertion-deep.

---

## EL13 — TemporalErasure (LEMMA, theorem)

Cross-home claim order is not a fact of the state. For `d₁ ≠ d₂ ∈ dom(Σ.M)` and values `v₁, v₂`, the two interleavings of the emissions commute to the same state:

> `K.λ(d₂, a_emit(·, d₂), v₂) ∘ K.λ(d₁, a_emit(·, d₁), v₁) (Σ) = K.λ(d₁, a_emit(·, d₁), v₁) ∘ K.λ(d₂, a_emit(·, d₂), v₂) (Σ)`

*Proof.* `a_emit(Σ', d)` depends only on the `d`-homed subset of `dom(Σ'.L)` (ASN-0086, EmitAddress, with HomeOriginCoincidence); an emission homed at `d₁` leaves the `d₂`-homed subset unchanged, so each address is the same in both orders; the enabledness of each step consults only its own home's set and `dom(M)`; and the two map-unions at distinct fresh keys commute, all other components being framed.

Consequently no function of the final state — no selector, no tie-break, no "latest" — distinguishes which of two cross-home claims was asserted later.

Within one home the opposite holds: the chain enumeration is strictly increasing (T9; ChainEnumerationInjectivity, ASN-0093), so claims homed at one document are totally ordered by their addresses — per-home "latest" is well-defined and state-recoverable, per-document-chain only.

A per-asserter "latest" is a state function only when the asserter homes all its claims at a single document; under an ASN-0042 ownership overlay, owner domains span many documents, so cross-home order is likewise unrecoverable. Any definable global tie-break ranks namespaces, not times.

---

## Df-CUR — CurrencyQuery (DEF, definition)

For `y ∈ dom(Σ.L)`:

> `reach_o(y, Σ)` is the least subset of `dom(Σ.L)` containing `y` and closed under `succ_o(Σ)`-images — finite and computable (the closure grows within finite `dom(Σ.L)`; bound function `|dom(Σ.L)| − |computed set|`).

The *current successors* of `y` are the operative sinks reachable from it:

> `current(y, Σ) = {z ∈ reach_o(y, Σ) : ¬(E w :: (z, w) ∈ succ_o(Σ))}`

---

## EL14 — CurrencyRelational (LEMMA, theorem)

`current` is a total, computable, *set-valued* query, and the set is irreducibly a set:

*(a)* `|current(y, Σ)| = 1` at states with one asserted, unretracted, linear chain from `y`; and `current(y, Σ) = {y}` when `y` has no operative successor — an unedited link is its own current version.

*(b)* `|current(y, Σ)| ≥ 2` at any fork state (EL12).

*(c)* `current(y, Σ) = ∅` is reachable: assert `x` supersedes `y`, then assert `y` supersedes `x` (a revert, by anyone). Both claims are permanent; while both are operative, `reach_o(y) = {y, x}` has no sink. The repair is not deletion (there is none) but demotion: `Nullify` one claim, and a sink — hence a current — reappears. The two-view structure (operative vs. historical) makes the standoff survivable: the operative graph is repairable precisely because the historical graph is not.

*(d)* No canonical selector exists. Any selector is a function of the state; "the most recently asserted" is not such a function across homes (EL13); forcing `|current| = 1` as an invariant would require refusing well-formed emissions or erasing claims — the substrate does neither. The layer owes the reader disclosure, not decision: `current(y, Σ)` entire, each member with its supporting claims and their homes (EL8b), the original always still readable beside them (EL9(1)), and any narrowing applied as the reader's declared policy.

---

## EL15 — ChainConnectivity (LEMMA, theorem)

For a chain of asserted edits `a₀, a₁, …, aₙ` with each `(aᵢ, aᵢ₊₁) ∈ succ_h(Σ)`:

*(a)* every member is permanently resolvable at its own address with its original value (EL0) — the far end of history is never lost;

*(b)* every asserted hop is permanently in `succ_h` (EL5a), so *historical connectivity is monotone*: the `succ_h`-component of any member never loses a node or an edge at any future state;

*(c)* every hop is locally recoverable from either endpoint alone — `in(aᵢ, Σ)` and `out(aᵢ, Σ)` are single arrangement-free observations (EL11b) — so the historical component is traversable edge-by-edge in both directions from any member, with no privileged entry point;

*(d)* what is **not** guaranteed is completeness and operative integrity: an edit whose author omitted the assertion contributes no hop (EL1), and a nullified claim drops from `succ_o` while remaining in `succ_h`. Member-to-ends traversability of the *operative* chain is therefore a derived property — holding exactly when the chain was fully asserted and no hop demoted — and is not an unconditional invariant.

---

## EL16 — ReferenceSurvival (LEMMA, theorem)

Let `c ∈ dom(Σ.L)` be any link with `a ∈ coverage(Σ.L(c).eᵢ)` for some slot `i` — a pre-existing reference to the original, made by anyone, anywhere. Across `editlink(a, ℓ', d_s, d_a)` and arbitrary further evolution `Σ →* Σ'`:

*(i)* the referring slot is unchanged in value and coverage (L12; LP2, LP3★) — nobody's context is rewritten by someone else's edit;

*(ii)* the referent still resolves, to the identical value:

> `Σ'.L(a) = Σ.L(a)` (EL0)

— the reference means today what it meant when made;

*(iii)* the road forward exists and is one observation long:

> `in(a, Σ') ∋ e` with `new(e) = a'`, attributed to `home(addr(e))`

— the reference reaches the successor not by being re-pointed but by composition with the record.

**Mutation** (excluded by EL0) would preserve the reference's spelling while silently re-pointing its meaning — every citation, comment, and dispute attached to `a` would come to qualify content its authors never saw. **Silent re-creation** — step 1 of EDITop without step 2 — passes (i) and (ii) vacuously and fails (iii): the successor exists, fresh and disconnected, indistinguishable from a stranger (EL1); the old references keep their exact referent and gain no road anywhere. The asserted edit is the unique regime preserving both the exact past and the reachable future.
