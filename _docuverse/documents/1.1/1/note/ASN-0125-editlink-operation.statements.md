# ASN-0125 Claim Statements

*Source: ASN-0125-editlink-operation.md (revised 2026-06-12) — Extracted: 2026-06-12*

## Definition — MutationPostcondition

For reachable `Σ₀`, link `a ∈ dom(Σ₀.L)`, and intended new value `w ≠ ℓ₀` where `ℓ₀ = Σ₀.L(a)`:

> `R_mut ≡ a ∈ dom(L) ∧ L(a) = w`

The invariant predicate used in the proof:

> `J ≡ a ∈ dom(L) ∧ L(a) = ℓ₀`

First weakening of postcondition (new reading, no address identity):

> `R₁ ≡ (E a' : a' ∈ dom(L) : L(a') = w)`

Second weakening (new reading plus recognized supersession):

> `R₂ ≡ R₁ ∧ "the pair (a, a') stands, in the state, in a relation recognizable as supersession"`

---

## EL0 — MutationExclusion (LEMMA, lemma)

For reachable `Σ₀`, `a ∈ dom(Σ₀.L)`, `ℓ₀ = Σ₀.L(a)`, the predicate `J ≡ a ∈ dom(L) ∧ L(a) = ℓ₀` is inductive over the closed vocabulary (only `K.λ` writes `L`, at fresh keys), so `(A Σ' : Σ₀ →* Σ' : Σ'.L(a) = ℓ₀)` and `wp(S, L(a) = w) = false` at `Σ₀` for every `w ≠ ℓ₀` and every finite program `S` — link mutation is unimplementable, and the original remains readable at its address with its exact value forever.

Formal invariant statement:

> `(A Σ' : Σ₀ →* Σ' : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = ℓ₀)`

Consequence:

> For every finite program `S` over the closed elementary vocabulary, `wp(S, R_mut)` evaluated at `Σ₀` is `false`.

---

## EL1 — IntentInvisibility (LEMMA, lemma)

A successor emission performed "as an edit" and an independent creation with the same parameters are the same transition with the same post-state, so no state predicate (hence no observation) distinguishes them; value resemblance, up to byte-identity (L11b), carries zero relational information; relationships enter the state only by explicit assertion.

Formal statement: For the post-state `Σ₁` of any single link allocation `K.λ(d_s, a_emit(Σ, d_s), ℓ')` applied at `Σ`, every state predicate is invariant under whether the allocation was an edit of some existing link or an independent creation. Equivalently:

> There is no predicate of `Σ₁` that holds iff `ℓ'` "was derived from" `Σ.L(a)`.

Corollary: `dom(Σ.L)` legitimately holds distinct addresses with identical values (L11b, NonInjectivity), and the state after a resembling independent creation coincides with the state after an unasserted "edit."

---

## EL2 — NoInPlaceCarrier (LEMMA, lemma)

The supersession record can live:

*(a) Not in the original's value.* `Σ.L(a)` is fixed by L12 from the moment of creation. No "superseded-by" annotation can ever be attached to `a`.

*(b) Not appended to the successor's value after birth.* The same invariant binds the successor the instant it exists: its slots are fixed at emission.

*(c) Not in the address relation between them.* Allocated link addresses have `#E = 2` on flat home chains and `dom(Σ.L)` is a prefix antichain (R0a), so:
- Every allocated link address has `#E = 2` exactly, while a nested version-of-link address would need `#E ≥ 3`.
- `dom(Σ.L)` is a tumbler-prefix antichain (R0a, FlatLinkDomain) — no allocated link address prefixes another.
- Address structure encodes only same-home and per-home emission order, neither semantic, and version-of-link nesting is unreachable.

*(d) Not in any index marker.* The stored entities are exhausted by `dom(Σ.C) ∪ dom(Σ.L)` (L14, DualPrimitive); there is no status field anywhere; the only systematic asymmetry between two link entries is their addresses.

Conclusion: The record must be a freshly allocated entity.

---

## RQ1–RQ7 — RecordRequirements (AXIOM, axiom)

Any carrier of the supersession relationship must satisfy all seven:

- **RQ1 (Post-hoc assertability).** The relationship must be assertable at any state where both endpoints exist — not only at the successor's creation.
- **RQ2 (Open authorship).** Any principal with a home document may assert.
- **RQ3 (Attribution).** The asserter must be decidable from the record alone.
- **RQ4 (Non-destructive disputability).** A claim must be withdrawable from current standing, and contestable, without erasing it or either endpoint.
- **RQ5 (Endpoint frame).** Asserting must modify neither endpoint.
- **RQ6 (Decidable specificity).** The relationship must be recognizable as supersession specifically — distinguishable from comment, counterpart, or coincidence — by the substrate's interpretation-free mechanisms: address and coverage comparison, never content exegesis. And it must be refinable: the vocabulary must be able to grow subtypes.
- **RQ7 (Plurality).** Arbitrarily many claims over the same endpoints, including mutually contradictory ones, must be co-representable.

---

## EL3 — RelationSpaceNecessity (LEMMA, lemma)

Under this substrate, any carrier satisfying RQ1–RQ7 is a freshly allocated link-store entity, distinct from both endpoints, referencing each endpoint by address through its endsets, and bearing its kind as the coverage class of a designated slot — that is, a typed link-to-link tuple.

Derivation structure:
- RQ1 and RQ2 → carrier is a fresh store entity, created by `K.α` (content) or `K.λ` (links).
- RQ6 eliminates the content store: a claim encoded as content bytes has no structure beyond an address and an origin to the substrate; type machinery reads slot-3 coverage only (L8, TypeByAddress). → The carrier is a link.
- RQ1 makes it a link other than the successor (EL2(b)). → A third entity.
- RQ6 → kind is carried by coverage class of the type slot (L8; decidability by CoverageEqualityDecidable; refinement by prefix containment, L10).
- RQ4 is satisfied because the carrier has its own address: individually targetable by `Nullify` while L12 holds it and both endpoints.
- RQ3 → its home prefix (T4b projection, decidable by T6; ownership by ASN-0042).
- RQ5 → `K.λ`'s frame.
- RQ7 → freshness: every claim is a new address.

Additional conclusion: "A separate supersession link" and "a typed relation" are the same architecture under L8. The genuinely distinct candidates (value space, address space, relation space) are each eliminated:
- Value space fails RQ1, RQ2, RQ4, RQ7.
- Address space fails RQ1, RQ2, RQ4, RQ6, and structurally: an address cannot be false.
- Relation space (typed tuple): the unique compatible carrier.

---

## Definition — SupersessionClass (Df-CLS)

Fix a coverage class `[K_sup]`, `K_sup ∈ T_admissible`, with `coverage(K_sup) ≠ coverage(R)` — distinct from the retraction class (ASN-0086).

> `S^Σ := L_{K_sup}^Σ = {(b, F, G) : b ∈ dom(Σ.L) ∧ |Σ.L(b)| = 3 ∧ Σ.L(b).e₁ = F ∧ Σ.L(b).e₂ = G ∧ coverage(Σ.L(b).e₃) = coverage(K_sup)}`

the *supersession slice* at `Σ` — the historical record of claims.

> `A_sup^Σ := A_{K_sup}^Σ = {(b, F, G) ∈ S^Σ : b ∉ nullified(Σ)}`

the operative subset. Members of `S^Σ` are called *claims*.

---

## Definition — ClaimDirectionality (Df-DIR)

For a claim `(b, F, G) ∈ S^Σ`: the from-set `F` covers the *superseding* link, the to-set `G` the *superseded* — read "`F` replaces `G`."

This aligns with the layer's RetractionDirectionality (ASN-0086): the to-side is the side acted upon.

A withdrawal with no replacement is not a degenerate supersession but a retraction, class `[R]`; the two acts remain distinct relations, and asserting the first never performs the second.

---

## Definition — EditDiscipline (Df-DISC)

A state `Σ` is *edit-disciplined* iff:

*(i)* it is unit-depth-retraction-disciplined (ASN-0086), and

*(ii)* every claim conforms to the *claim schema*:

> `(A (b, F, G) ∈ S^Σ : (E x, y ∈ dom(Σ.L) : x ≠ y ∧ F = {(x, δ(1, #x))} ∧ G = {(y, δ(1, #y))}))`

— both endsets are canonical unit-depth spans at link-store addresses, and the claim is irreflexive. (Self-supersession `x = y` is excluded as vacuous; cycles of length ≥ 2 are deliberately *not* excluded.)

A layer is edit-disciplined iff every state it reaches is.

---

## EL4 — SingleTarget (LEMMA, lemma)

For `e = (b, F, G) ∈ S^Σ` whose endsets meet the Df-DISC(ii) form with witnesses `x, y` (so `F = {(x, δ(1,#x))}`, `G = {(y, δ(1,#y))}`, `x, y ∈ dom(Σ.L)`, `x ≠ y`):

> `coverage(F) ∩ dom(Σ.L) = {x}`   and   `coverage(G) ∩ dom(Σ.L) = {y}`

The argument is per-claim, invoking no whole-state discipline hypothesis.

*Proof sketch.* `coverage({(x, δ(1, #x))}) = {t : x ≼ t}` (PrefixSpanCoverage, ASN-0043); for `t ∈ dom(Σ.L)` with `x ≼ t`, the antichain R0a forces `t = x`. ∎

Corollaries:
- `addr(e) = b`, `new(e) = x`, `old(e) = y` are total accessors on any schema-conforming claim at any reachable state.
- Write `Ŝ^Σ = {e ∈ S^Σ : e is schema-conforming}` for the schema-conforming claims; at an edit-disciplined state `Ŝ^Σ = S^Σ`.

---

## Definition — SuccessorRelations (Df-SUCC)

At any state `Σ`, ranging over the schema-conforming claims `Ŝ^Σ` (EL4), on which `old`/`new`/`addr` are total:

> `succ_h(Σ) = {(old(e), new(e)) : e ∈ Ŝ^Σ}`  — the historical relation

> `succ_o(Σ) = {(old(e), new(e)) : e ∈ Ŝ^Σ ∧ addr(e) ∉ nullified(Σ)}`  — the operative relation

Both are finite (L-fin) relations on `dom(Σ.L)`, with `succ_o(Σ) ⊆ succ_h(Σ)`. At an edit-disciplined state `Ŝ^Σ = S^Σ`, so the comprehensions coincide with the unrestricted reading.

---

## EL5 — RecordMonotonicity (LEMMA, lemma)

For every `Σ →* Σ'`:

*(a)* `S^Σ ⊆ S^{Σ'}`, `Ŝ^Σ ⊆ Ŝ^{Σ'}` (schema-conformance is value-and-domain-determined — a conforming claim's witnesses satisfy `x, y ∈ dom(Σ.L) ⊆ dom(Σ'.L)`, so it stays conforming at `Σ'` with the same `old`/`new`), and `succ_h(Σ) ⊆ succ_h(Σ')`. Claims accumulate; none is ever lost.

*(b)* `nullified(Σ) ⊆ nullified(Σ')`. The `[R]`-slice likewise only grows, so nullification is one-way (R6a, ASN-0086): a claim once retracted from operative standing never silently regains it (re-assertion is a *new* claim at a fresh address — the shape of R6c).

*(c)* `succ_o` is neither monotone nor antitone: emission adds operative pairs (EL6), `Nullify` removes them. The operative relation is the revisable view; the historical relation is the unrevisable record.

---

## Definition — AssertSup (ASSERTop, DEF, OPERATION)

**Precondition:** `x, y ∈ dom(Σ.L)`, `x ≠ y`, `d_a ∈ dom(Σ.M)`.

**Definition:**

> `assert_sup(x, y, d_a) ≜ Emit_{K_sup}(Σ, d_a, {(x, δ(1, #x))}, {(y, δ(1, #y))})`

— one `K.λ` at home `d_a`, emitting the claim "`x` supersedes `y`" at the fresh address `b = a_emit(Σ, d_a)`.

Discharge of `K.λ`'s L3 precondition: the spans are T12-well-formed (`Pos(δ(1, #x))`; action point `#x ≤ #x`), the slots are endsets, the arity is 3, and slot 3 is `K_sup ≠ ∅`.

---

## EL6 — AssertionContract (LEMMA, lemma)

When invoked at a reachable `Σ` satisfying its precondition, `assert_sup(x, y, d_a)` yields `Σ'` with:

*(i) Allocation.* Exactly one fresh address: `b ∉ dom(Σ.L) ∪ dom(Σ.C)` (emission freshness, ASN-0093), `home(b) = d_a`.

*(ii) Record.* `e_b = (b, {(x, δ(1,#x))}, {(y, δ(1,#y))}) ∈ S^{Σ'}` with `new(e_b) = x`, `old(e_b) = y`; hence `(y, x) ∈ succ_h(Σ')`.

*(iii) Active at birth.* If `Σ` is edit-disciplined, `b ∉ nullified(Σ')`, so `(y, x) ∈ succ_o(Σ')`. (ASN-0086 wp Case 2 under disciplined simplification: pre-existing-retraction conjunct holds vacuously, `K_sup ≁ R` discharges self-nullification guard.)

*(iv) Frame — and the independence of axes.* `Σ'.C = Σ.C`, `Σ'.M = Σ.M`, `Σ'.E = Σ.E`, `Σ'.R = Σ.R`; every prior link-store entry is unchanged.

*Unconditionally:* `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` — the lone new tuple has slot-3 coverage `coverage(K_sup) ≠ coverage(R)`, so the `[R]`-slice does not grow and the nullification status of no pre-existing address changes.

*Under edit-discipline on `Σ`:* the full `nullified(Σ') = nullified(Σ)` — the fresh `b ∉ dom(Σ.L)` is prefix-incomparable to each pre-existing `[R]`-tuple's to-coverage (R0a at `Σ'`), so `b ∉ nullified(Σ')`.

**Asserting supersession deactivates nothing.**

*(v) Discipline and permanence.* `Σ'` is edit-disciplined when `Σ` was; and at every `Σ' →* Σ''`, `e_b ∈ S^{Σ''}` with value fixed and `(y, x) ∈ succ_h(Σ'')` (EL5a).

---

## Definition — Editlink (EDITop, DEF, OPERATION)

**Precondition:** `a ∈ dom(Σ.L)`, `d_s, d_a ∈ dom(Σ.M)`, `ℓ' ∈ Link` L3-conforming, `DC(ℓ')`:

> `DC(ℓ')`: if `coverage(ℓ'.e₃) = coverage(K_sup)` then `ℓ'` satisfies the claim schema of Df-DISC(ii); if `coverage(ℓ'.e₃) = coverage(R)` then `ℓ'` satisfies the unit-depth retraction schema.

**Definition:**

> `editlink(a, ℓ', d_s, d_a) ≜`
> `  a' := a_emit(Σ, d_s);  Σ₁ := K.λ(d_s, a', ℓ');`
> `  (Σ₂, b) := assert_sup(a', a, d_a) at Σ₁;`
> `  return (Σ₂, a', b)`

Discharge of `assert_sup`'s precondition at `Σ₁`: `a' ∈ dom(Σ₁.L)` by the emission, `a ∈ dom(Σ₁.L)` by monotonicity, `a' ≠ a` by freshness, `d_a ∈ dom(Σ₁.M)` by M1.

Remarks:
- `ℓ' = Σ.L(a)` is admitted (value-identical successor is a legitimate edit).
- Neither `d_s` nor `d_a` is constrained relative to `home(a)` (third-party edit-by-fork is the same composite).
- A revert: `assert_sup(a, a', d)` — one claim, nothing else, since the "new" value already exists at its permanent address.

---

## EL7 — EditContract (LEMMA, lemma)

When invoked at a reachable `Σ` satisfying its precondition, `editlink(a, ℓ', d_s, d_a)` yields `Σ₂` with:

*(i) What is allocated.* Exactly **two** fresh link-subspace addresses — the successor `a'` on `A_L(d_s)` and the claim `b` on `A_L(d_a)` — pairwise distinct from each other and from everything prior. No content address, no entity, no provenance entry, no arrangement change:

> `Σ₂.C = Σ.C`, `Σ₂.M = Σ.M`, `Σ₂.E = Σ.E`, `Σ₂.R = Σ.R`

*(ii) The new reading.*

> `Σ₂.L(a') = ℓ'`, `home(a') = d_s`

— postcondition `R₁` achieved with a permanent, fresh identity.

*(iii) The relationship.*

> `(a, a') ∈ succ_h(Σ₂)`, witnessed by the claim at `b`

at edit-disciplined `Σ`, also `(a, a') ∈ succ_o(Σ₂)` — postcondition `R₂` achieved as an owned, addressed, class-marked statement.

*(iv) The frame on the original.*

> `Σ₂.L(a) = Σ.L(a)` unconditionally (L12)

`nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` unconditionally (supersession step deactivates nothing — EL6(iv)); under edit-discipline on `Σ` and non-retraction `ℓ'`, the full `nullified(Σ₂) = nullified(Σ)` holds (both fresh addresses escape pre-existing retraction coverage by R0a, the wp Case 2 argument of EL6(iv) applied at each of the two emissions).

*(v) Permanence.* At every `Σ₂ →* Σ₃`: `a`, `a'`, `b` all persist with fixed values, and `(a, a') ∈ succ_h(Σ₃)`.

*(vi) Discipline preservation.* `Σ₂` is edit-disciplined when `Σ` is. Step 1 (`K.λ(d_s, a', ℓ')`) preserves Df-DISC via `DC(ℓ')`. Step 2 (`assert_sup`) preserves edit-discipline by EL6(v).

---

## EL8 — ClaimStanding (LEMMA, lemma)

For every claim `e ∈ S^Σ` in a disciplined state:

*(a)* it is permanent in membership and value (EL5a);

*(b)* it is attributed: `home(addr(e))` is computable from the address alone by field projection (T4b), decidably (T6), and the effective owner follows by prefix (ASN-0042) — the claim is signed by its address;

*(c)* it is open: the schema imposes no relation among `home(addr(e))`, `home(old(e))`, `home(new(e))` — first-party, second-party, and third-party claims are structurally identical, differing only in their visible provenance;

*(d)* it is itself addressable: `addr(e) ∈ dom(Σ.L)`, so claims can be the targets of endsets (L4(c)) — endorsed, disputed, commented, retracted (`Nullify`), or themselves edited (`editlink` applies to a claim, `DC` permitting) — with no new machinery;

*(e)* it is a claim, not a verdict: the substrate records who said what and adjudicates nothing. Recognition of *standing* is structural; recognition of *truth* is the reader's.

---

## Definition — Listed (Df-LISTED)

> `listed(t, d, Σ) ≡ (E v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) = t)`

— `t` appears in `d`'s current arrangement. For a link, only its home can list it: a link-subspace image has `origin = d` (CL-OWN, ASN-0047, with HomeOriginCoincidence), and a content-subspace image lies in `dom(C)` (S3★), which is disjoint from `dom(L)` (SD).

Additionally:

> `active(a, Σ) ≡ a ∉ nullified(Σ)`

---

## EL9 — ThreeAxes (LEMMA, lemma)

For a link `a ∈ dom(Σ.L)`:

*(1) Resolution — permanent and unconditional.*

> `(A Σ' : Σ →* Σ' : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a))` (EL0's invariant `J`)

Nothing gates the lookup: no arrangement state, no activity status, no provenance appears in it.

*(2) Listing — mutable in both directions.* `K.μ⁻` de-lists; `K.μ⁺_L` re-lists. `listed(t, d, Σ)` can both gain and lose truth across reachable transitions, and only at `d = home(a)` (CL-OWN).

*(3) Activity — monotone downward, per claim.*

> `active(a, Σ) ≡ a ∉ nullified(Σ)` can only fall (EL5b), by an explicit, itself-permanent, itself-attributed retraction tuple; restoration is re-assertion at a fresh address, never reinstatement in place (R6c).

The axes are independent, and — by EL6(iv) — *superseding moves none of them*. An edit, as such, leaves the original resolvable, listed, and active.

---

## EL10 — PositionEpochality (LEMMA, lemma)

There exist reachable `Σ →* Σ' →* Σ''`, a document `d`, a position `v`, and links `ℓ₁ ≠ ℓ₂` — both permanently resolvable throughout — with:

> `Σ.M(d)(v) = ℓ₁,   v ∉ dom(Σ'.M(d)),   Σ''.M(d)(v) = ℓ₂`

*Construction.* Let `d` list two links, `V_{s_L}(d) = {[s_L,1], [s_L,2]}` with `[s_L,2] ↦ ℓ₁`, and let `ℓ₂` be homed at `d` but unlisted. Apply `K.μ⁻` with link-subspace retention `n'_{s_L} = 1`; then `K.μ⁺_L` for `ℓ₂`: the substrate assigns `v_ℓ = shift(max(V_{s_L}(d)), 1) = shift([s_L,1], 1) = [s_L,2]` — the very position `ℓ₁` vacated, now bound to `ℓ₂`. ∎

Corollary: Surviving references — the claim schema included — must bind addresses, never positions. Df-DISC's address-binding is load-bearing, not stylistic.

---

## Definition — ArchivalQuerySets

Defined at any reachable state over the schema-conforming claims `Ŝ^Σ`:

> `in(y, Σ) = {e ∈ Ŝ^Σ : old(e) = y}`

> `out(x, Σ) = {e ∈ Ŝ^Σ : new(e) = x}`

These are instances of `Observe_{K_sup}` at pattern `Ĝ = {y}` (resp. `F̂ = {x}`), view `hist`, filtered by the decidable schema-conformance predicate (a no-op at disciplined states).

---

## EL11 — TwoRegimeDiscovery (LEMMA, lemma)

*(a) Contextual (arrangement-gated).* For a disciplined claim `e` and any document `d`, the to-side of `e` projects into `d` iff `d` currently lists the original:

> `project(Σ.L(addr(e)).e₂, d, Σ) ≠ ∅ ⟺ listed(old(e), d, Σ)`

*Proof sketch.* By LP12 (ASN-0098): left side is `coverage(G) ∩ ran(Σ.M(d)) ≠ ∅` with `G` the to-set. `coverage(G) = {t : old(e) ≼ t}` (EL4). Any `t ∈ ran(Σ.M(d))` lies in `dom(Σ.C) ∪ dom(Σ.L)` (S3★); no content address extends `old(e)` (SC-NEQ); a link address extends `old(e)` only if equal (R0a). So the intersection is `{old(e)} ∩ ran(Σ.M(d))`, nonempty iff `old(e)` is listed — and only at `d = home(old(e))` by Df-LISTED. ∎ Symmetrically for the from-side and `new(e)`.

*(b) Archival (arrangement-independent).* The predicates `e ∈ Ŝ^Σ` and `old(e) = y` are functions of stored values, decidable by coverage comparison (CoverageEqualityDecidable; T2; EL4). Hence `in(y, Σ)` and `out(x, Σ)` are computable from `Σ.L` alone, completely and decidably, at every state:

> **The supersession question is answerable, completely and decidably, at every state, whatever every arrangement says.**

---

## EL12 — ForkPermanence (LEMMA, lemma)

Two editors independently superseding the same link produce a permanent, co-visible fork. Running `editlink(a, ·, ·, ·)` twice from any disciplined reachable state, in any combination of homes:
- Freshness yields distinct successors `a'₁ ≠ a'₂` and distinct claims `e₁ ≠ e₂` (same home: chain advances past first emission; different homes: cross-document disjointness with T10).
- Both `(a, a'₁)` and `(a, a'₂)` enter `succ_h` — permanently (EL5a) — and `succ_o` at birth (EL6(iii), with EL7(vi) confirming the intermediate state is edit-disciplined).
- The vocabulary contains no transition that merges, ranks, or removes either.

The complete competing-claim set with asserters is one archival query: `in(a, Σ)`.

Corollary (absence case): Without the assertion steps, the same two emissions leave `succ_h` untouched (EL1). Fork *visibility* is exactly assertion-deep.

---

## EL13 — TemporalErasure (LEMMA, lemma)

For `d₁ ≠ d₂ ∈ dom(Σ.M)` and values `v₁, v₂`, the two interleavings of the emissions commute to the same state:

> `K.λ(d₂, a_emit(·, d₂), v₂) ∘ K.λ(d₁, a_emit(·, d₁), v₁) (Σ) = K.λ(d₁, a_emit(·, d₁), v₁) ∘ K.λ(d₂, a_emit(·, d₂), v₂) (Σ)`

*Proof.* `a_emit(Σ', d)` depends only on the `d`-homed subset of `dom(Σ'.L)` (ASN-0086, EmitAddress, with HomeOriginCoincidence); an emission homed at `d₁` leaves the `d₂`-homed subset unchanged, so each address is the same in both orders; enabledness of each step consults only its own home's set and `dom(M)`; and the two map-unions at distinct fresh keys commute, all other components framed. ∎

Consequences:
- No function of the final state — no selector, no tie-break, no "latest" — distinguishes which of two cross-home claims was asserted later: the trace knows, the state does not.
- Within one home the opposite holds: the chain enumeration is strictly increasing (T9; ChainEnumerationInjectivity, ASN-0093), so claims homed at one document are totally ordered by their addresses — per-home "latest" is well-defined and state-recoverable.
- A per-asserter "latest" is state-recoverable only under the added assumption that the asserter homes all its claims at a single document.
- Any global most-recent-wins rule is undefinable from state; any definable global tie-break ranks namespaces, not times.

---

## Definition — CurrencyQuery (Df-CUR)

For `y ∈ dom(Σ.L)`:

> `reach_o(y, Σ)` is the least subset of `dom(Σ.L)` containing `y` and closed under `succ_o(Σ)`-images — finite and computable (bound function `|dom(Σ.L)| − |computed set|`).

> `current(y, Σ) = {z ∈ reach_o(y, Σ) : ¬(E w :: (z, w) ∈ succ_o(Σ))}`

the *current successors* of `y` — the operative sinks reachable from it.

---

## EL14 — CurrencyRelational (LEMMA, lemma)

`current` is a total, computable, *set-valued* query, and the set is irreducibly a set:

*(a)* `|current(y, Σ)| = 1` at states with one asserted, unretracted, linear chain from `y`; and `current(y, Σ) = {y}` when `y` has no operative successor — an unedited link is its own current version.

*(b)* `|current(y, Σ)| ≥ 2` at any fork state (EL12).

*(c)* `current(y, Σ) = ∅` is reachable: assert `x` supersedes `y`, then assert `y` supersedes `x`. While both claims are operative, `reach_o(y) = {y, x}` has no sink. Repair: `Nullify` one claim → a sink reappears. The two-view structure makes the standoff survivable: the operative graph is repairable precisely because the historical graph is not.

*(d)* No canonical selector exists. Any selector is a function of the state; "the most recently asserted" is not such a function across homes (EL13); and forcing `|current| = 1` as an invariant would require refusing well-formed emissions or erasing claims — the substrate does neither.

---

## EL15 — ChainConnectivity (LEMMA, lemma)

For a chain of asserted edits `a₀, a₁, …, aₙ` with each `(aᵢ, aᵢ₊₁) ∈ succ_h(Σ)`:

*(a)* Every member is permanently resolvable at its own address with its original value (EL0).

*(b)* Every asserted hop is permanently in `succ_h` (EL5a) — *historical connectivity is monotone*: the `succ_h`-component of any member never loses a node or an edge at any future state.

*(c)* Every hop is locally recoverable from either endpoint alone: `in(aᵢ, Σ)` and `out(aᵢ, Σ)` are single arrangement-free observations (EL11b) — the historical component is traversable edge-by-edge in both directions from any member, with no privileged entry point.

*(d)* What is *not* guaranteed: completeness (an unasserted hop contributes nothing — EL1) and operative integrity (a nullified claim drops from `succ_o` while remaining in `succ_h`). Member-to-ends traversability of the *operative* chain is a derived property — holding exactly when the chain was fully asserted and no hop demoted — and any specification that promised it unconditionally would be promising what no implementation of this substrate can keep.

---

## EL16 — ReferenceSurvival (LEMMA, lemma)

Let `c ∈ dom(Σ.L)` be any link with `a ∈ coverage(Σ.L(c).eᵢ)` for some slot `i` — a pre-existing reference to the original. Across `editlink(a, ℓ', d_s, d_a)` and arbitrary further evolution `Σ →* Σ'`:

*(i)* The referring slot is unchanged in value and coverage (L12; LP2, LP3★) — nobody's context is rewritten by someone else's edit.

*(ii)* The referent still resolves, to the identical value:

> `Σ'.L(a) = Σ.L(a)` (EL0)

*(iii)* The road forward exists and is one observation long:

> `in(a, Σ') ∋ e` with `new(e) = a'`, attributed to `home(addr(e))`

— the reference reaches the successor not by being re-pointed but by *composition with the record*.

Failure modes (excluded):
- **Mutation** (excluded by EL0): would preserve the reference's spelling while silently re-pointing its meaning — every citation attached to `a` would qualify content its authors never saw.
- **Silent re-creation** (step 1 without step 2): passes (i) and (ii) vacuously, fails (iii) — the successor exists, fresh and disconnected, indistinguishable from a stranger (EL1); old references keep their exact referent and gain no road anywhere.

The asserted edit is the unique regime preserving both the exact past and the reachable future.
