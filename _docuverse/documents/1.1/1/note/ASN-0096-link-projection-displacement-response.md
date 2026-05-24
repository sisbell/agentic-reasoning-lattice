# ASN-0096: Link Projection Displacement
*2026-05-24*

## The Problem

A link is established with endsets that identify content at particular addresses in some documents' arrangements. Time passes. The documents are edited — bytes are inserted between linked passages, sections are reordered, content is removed from one document and transcluded into others, new versions are forked off, content from a single endset is split across multiple documents. A reader of the link asks: where do these endsets appear now? What does the link still refer to? What can I rely on?

A naïve design would store V-positions in the link — the document-local positions where the endsets appear at creation time. This fails on first contact with editing: any insertion before a stored V-position shifts that position, and the link silently refers to whatever now sits at the stored position. The link holder cannot rely on the V-position being meaningful across time.

The Xanadu design separates *what is stored in the link* from *what is presented to the reader*. The link stores I-addresses — the permanent identity of the content. The V-position is computed on demand from the document's current arrangement. The arrangement may displace V-positions; the link does not move with them. We call this re-computation the *projection*, and the change in V-position presentation across states the *displacement*.

This ASN states the guarantees that fall out of this design. The aim is to characterize precisely what survives state changes, what displaces, and what a link holder can rely on. We work from the state components defined in ASN-0036 (content store, arrangement), ASN-0043 (link store, endsets, coverage), and ASN-0047 (state transitions), together with the addressing foundation of ASN-0034.

The argument develops in stages. We first fix the state and the projection's type signature, then catalog the six *still-point* invariants of the link itself, then the *operation-to-displacement* mapping over the seventeen FEBE commands, then the *displacement modes* of the projection under arrangement transitions (three pure-atom modes, two composed modes), then derive *survival* and *discoverability* with explicit premise sets and wp computations, then exhibit the three *non-invariants* with witness transitions, then walk a concrete example through atomic decompositions of INSERT and DELETE, and finally enumerate the boundary cases. The claims number twenty-three, organized as three foundational definitions plus twenty named guarantees.

## State Components

The system state Σ contains, among other components:

- `Σ.C : T ⇀ Val`, the content store (ASN-0036, S0–S3);
- `Σ.M : Σ.E_doc → (T ⇀ T)`, the family of arrangements indexed by document (ASN-0036, S2);
- `Σ.L : T ⇀ Link`, the link store (ASN-0043, L12);
- `Σ.E ⊆ T`, the set of allocated entities including `Σ.E_doc` (ASN-0047, P1).

A link at address `ℓ ∈ dom(Σ.L)` is an N-tuple of endsets:

  `Σ.L(ℓ) = (e₁, e₂, e₃, ..., e_N)`   with N ≥ 3

per L3 (ASN-0043). The third slot is the type endset by the StandardTriple convention. Each endset is a finite set of well-formed spans, and its *coverage* is the union of those spans' address denotations (per the coverage definition in ASN-0043). To avoid colliding with the link address `ℓ`, we write span widths as `w` and recall the coverage definition:

  `coverage(e) = (∪ (s, w) : (s, w) ∈ e : {t ∈ T : s ≤ t < s ⊕ w})`

Coverage is a set of I-addresses in tumbler space T. It is determined entirely by the spans of `e` — independent of whether those addresses are currently allocated in `Σ.C`, currently mapped in any arrangement, or referenced by any other link. By L4 (ASN-0043), an endset's spans may reference addresses anywhere in T, including across multiple documents, multiple subspaces, and (with care) future allocations.

A document `d ∈ Σ.E_doc` has an arrangement `Σ.M(d) : T ⇀ T` mapping V-positions to I-addresses. Its image is:

  `ran(Σ.M(d)) = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}`

— the set of I-addresses currently placed somewhere in `d`'s V-space.

## The Projection

The link's endset names a set of I-addresses. The reader looking at a document sees V-positions. The bridge between them is the inverse image of coverage under the arrangement. Before stating the definition we fix the signature so that endset-level, span-level, and address-level projections are not conflated.

**Type signature.** Projection is a *dependent* function: the valid second argument (`d`) and the codomain (V-positions drawn from `d`'s arrangement) both depend on the state argument (`Σ`). State-first presentation makes the dependence explicit:

  `proj : (Σ : State) → Endset → (d : Σ.E_doc) → ℘_fin(dom(Σ.M(d)))`

`State` is the set of reachable system states (ASN-0047). `Endset = ℘_fin(Span)` (ASN-0043, L4) is the only argument whose denotation is state-independent. `Σ.E_doc ⊆ T` — the set of allocated document addresses *in the supplied state* — determines which document arguments are admissible; `dom(Σ.M(d))` — the V-positions actually mapped by `d` in Σ — determines the codomain. We retain the conventional argument order `proj(e, d, Σ)` in subsequent prose for readability, but the underlying signature is the dependent product above. `proj(e, d, Σ)` is *undefined* when `d ∉ Σ.E_doc`. The codomain is a *set*, not a sequence or multiset; no ordering or multiplicity is imposed at this layer (see the open question on projection ordering for whether a higher layer should impose tumbler order on the result). Finiteness follows from the finiteness of `dom(Σ.M(d))` at every reachable state.

The signature is at the *endset* level. Span-level and address-level projection are special cases obtained by restriction, and they carry distinct cardinality semantics that must not be conflated with the endset signature:

- *Span-level projection.* For a single well-formed span `(s, w)`: `proj_span((s, w), d, Σ) := proj({(s, w)}, d, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage({(s, w)})}`. The result is a set of V-positions whose I-addresses fall inside the half-open interval `[s, s ⊕ w)`.
- *Address-level projection.* For a single I-address `a ∈ T`: `proj_addr(a, d, Σ) := {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) = a}`. Because `Σ.M(d)` is a (partial) function from V to I, this is the *fiber* of `a` under the arrangement; in the absence of S5 sharing it has cardinality 0 or 1, and with S5 sharing it may exceed 1 (multiple V-positions may map to the same I-address).
- *Endset projection.* `proj(e, d, Σ) = (∪ s ∈ e : proj_span(s, d, Σ))`. The union over spans, equivalently the set of V-positions whose I-address falls in `coverage(e)`. Cardinality may exceed `|coverage(e)|` under S5 sharing and may fall below it under partial deletion; equality holds only in the special case of injective `Σ.M(d)` with full coverage placement.

Throughout this ASN, "projection" without qualification refers to the endset signature. Gregory's implementation evidence is that udanax-green realizes all three levels through a single dimension-parametric algorithm (`permute()`); the type-level distinction we draw here is a specification-level discipline, not an implementation split.

**Definition (Endset projection).** For an endset `e ∈ Endset`, a document `d ∈ Σ.E_doc`, and a state `Σ`:

  `proj(e, d, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}`

The projection is the set of V-positions in `d` that currently map to an address in `e`'s coverage. By construction `proj` is a function of three arguments: the endset `e`, the context document `d`, and the state `Σ`. It does not consult any V-positions stored in the link — none are stored. It does not consult any historical arrangement — only the current `Σ.M(d)`. It does not consult the link's home document — the projection in `d` is computed from `d`'s own arrangement.

**Definition (Link rendering).** For a link `ℓ ∈ dom(Σ.L)` and a document `d ∈ Σ.E_doc`:

  `render(ℓ, d, Σ) = ⟨proj(Σ.L(ℓ).e₁, d, Σ), proj(Σ.L(ℓ).e₂, d, Σ), ..., proj(Σ.L(ℓ).e_N, d, Σ)⟩`

The rendering presents the link as it currently appears in `d`: a sequence of V-position sets, one per endset, in slot order.

**Definition (Document footprint).** For a link `ℓ ∈ dom(Σ.L)` and a slot index `i ∈ {1, ..., |Σ.L(ℓ)|}`:

  `footprint(ℓ, i, Σ) := {d ∈ Σ.E_doc : proj(Σ.L(ℓ).eᵢ, d, Σ) ≠ ∅}`

The footprint is the set of documents through which the link's `i`-th endset has at least one rendered V-position at state Σ. Like `proj`, it is computed on demand from current state — no per-link "where it appears" cache exists in any state component. Where `render` answers *what V-positions does this endset show in this document*, `footprint` answers *which documents show this endset at all*. We use the footprint primitive in LP-NOD below and in the open question on visibility partition.

The link itself — the value at `ℓ` in `Σ.L` — never directly contains any V-position or any document identity. V-positions appear only at the rendering layer; document membership appears only at the footprint layer. Both are computed on demand from the durable stored value and the documents' current arrangements.

## Operation Families and Displacement Modes

ASN-0047 supplies four arrangement-modifying transition families: K.μ⁺ (positive content arrangement), K.μ⁺_L (positive link arrangement), K.μ⁻ (negative arrangement / contraction), and K.μ~ (rearrangement). The remaining transition atoms (K.α, K.λ, K.δ, K.ρ) do not touch any existing `Σ.M(d)`. We adopt the ASN-0047 atoms in their *pure* form throughout this ASN — that is, K.μ⁺ adds new V→I mappings *without relabeling* any pre-existing V-position; K.μ⁻ realizes `Σ'.M(d) = Σ.M(d) ↾ R` as pure restriction *without relabeling* surviving V-positions; K.μ~ is bijective permutation of `dom(Σ.M(d))` with constant domain. This isolation matters: each pure atom corresponds to exactly one displacement mode, and FEBE-level operations whose effect appears to combine "extend and shift" or "restrict and shift" decompose into a composition of atoms, not into a single non-pure atom.

The seventeen FEBE editing/document commands at the protocol layer (Nelson, LM 4/61: "Of the 17 current commands in XU.87.1, only one command (RETRIEVEV) is concerned with delivery of the actual content fragments") partition cleanly. Eight commands modify a document's arrangement; the remaining nine are read-only searches, retrievals, comparisons, and metadata queries (per Nelson's command roster). LP-MAP catalogs the arrangement-modifying eight; LP-FRAME-READ records the trivial fact about the nine read-only commands.

**LP-MAP (Operation-to-mode surjection over arrangement-modifying commands).** Every arrangement-modifying FEBE command decomposes into a composition of pure atomic transitions K.α, K.λ, K.δ, K.ρ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, each atom inducing exactly one displacement mode on the projection (LP-EXT-PURE, LP-CONTR-PURE, LP-REARR, or LP-FRAME). The composed displacement on the projection follows from applying the atomic modes in sequence:

| FEBE command | Atomic decomposition | Composed projection displacement |
|--------------|----------------------|-----------------------------------|
| INSERT (mid-subspace) | K.α ∘ K.μ~ ∘ K.μ⁺ on d (text subspace) | LP-REARR (within-subspace shift of pre-existing V-positions) followed by LP-EXT-PURE (new V-positions admit coverage iff their fresh I-addresses fall in coverage — typically empty by T9 ForwardAllocation) |
| APPEND | K.α ∘ K.μ⁺ on d (at end of text subspace) | LP-EXT-PURE (no shift needed; appending leaves all pre-existing V-positions fixed) |
| COPY / VCOPY (mid-subspace) | K.μ~ ∘ K.μ⁺ on d (no K.α — re-uses source I-addresses) | LP-REARR followed by LP-EXT-PURE (new V-positions admit coverage iff transcluded I-addresses fall in coverage — non-empty whenever transclusion overlaps an existing endset) |
| COPY / VCOPY (subspace-end) | K.μ⁺ on d (at end of text subspace) | LP-EXT-PURE |
| DELETEVSPAN (interior, with subsequent V-positions to shift) | K.μ⁻ ∘ K.μ~ on d (text subspace) | LP-CONTR-PURE (drop coverage V-positions in the deleted range) followed by LP-REARR (within-subspace shift of surviving V-positions backward) |
| DELETEVSPAN (subspace-tail) | K.μ⁻ on d (text subspace) | LP-CONTR-PURE (no shift; deletion at the end leaves earlier V-positions fixed) |
| REARRANGE (pivot/swap) | K.μ~ on d | LP-REARR |
| MAKELINK | K.λ ∘ K.μ⁺_L on home(ℓ) | LP-EXT-PURE in the link subspace at `home(ℓ)`; LP-FRAME for every text-subspace endset's projection and every other document's projection |
| CREATENEWDOCUMENT | K.δ on E_doc (plus K.α for the document address) | LP-FRAME on every existing document (LP-CROSS); the new document has empty arrangement, so every endset projects to ∅ in the new document at creation |
| CREATENEWVERSION | K.δ ∘ (K.μ⁺ on the new document, copying V→I mappings from the source) | LP-FRAME on the source document; LP-EXT-PURE in the new document for each copied V→I mapping whose I-address is in coverage |

The decomposition justification, atom by atom:

- **K.μ⁺ on d (pure, LP-EXT-PURE).** Adds new V→I mappings to `Σ.M(d)` at V-positions disjoint from `dom(Σ.M(d))`. No pre-existing V-position is relabeled. The projection's existing V-positions are untouched; new V-positions join `proj(e, d, Σ')` iff their I-addresses lie in `coverage(e)`. Statement: `proj(e, d, Σ') = proj(e, d, Σ) ∪ {v_new ∈ dom(Σ'.M(d)) \ dom(Σ.M(d)) : Σ'.M(d)(v_new) ∈ coverage(e)}`. Pure superset relation: `proj' ⊇ proj`.

- **K.μ⁻ on d (pure, LP-CONTR-PURE).** Effect `Σ'.M(d) = Σ.M(d) ↾ R` per ASN-0047 — pure restriction. Surviving V-positions retain their original V-labels (no shift). Statement: `proj(e, d, Σ') = proj(e, d, Σ) ∩ R`.

- **K.μ~ on d (LP-REARR).** Bijective permutation of `dom(Σ.M(d))` with constant domain; surviving V-positions get re-labeled. Statement: `proj(e, d, Σ') = π(proj(e, d, Σ))`.

- **K.μ⁺_L on d (LP-EXT-PURE in link subspace).** Specialization of K.μ⁺ to the link subspace. Adds a new V→I mapping at the end of the link subspace (Gregory's evidence: `findnextlinkvsa` always places links at `vspanreach`). By the disjointness of subspaces (ASN-0036), no text-subspace mapping is touched.

- **K.δ (LP-FRAME on existing documents).** Creates a fresh document address with empty arrangement. For every existing document `d`, `Σ'.M(d) = Σ.M(d)`. The new document `d_new` has `dom(Σ'.M(d_new)) = ∅`, so `proj(e, d_new, Σ') = ∅` for every `e`.

- **K.α, K.λ, K.ρ (LP-FRAME).** Pure allocation transitions. K.α allocates content I-addresses; K.λ allocates link addresses; K.ρ modifies the region store. None touches any `M(d)`.

The FEBE-level *composed* displacements that combine atomic effects — for instance INSERT mid-subspace, which interleaves K.μ~ (shift existing V-positions) and K.μ⁺ (add new mappings at the freed slots) — are recorded as LP-EXT-COMP and LP-CONTR-COMP below.

**LP-FRAME-READ (Read-only commands frame all projections).** The nine read-only FEBE commands — RETRIEVEV, RETRIEVEDOCVSPAN, RETRIEVEDOCVSPANSET, RETRIEVEENDSETS, FINDLINKSFROMTOTHREE, FINDNUMOFLINKSFROMTOTHREE, FINDNEXTNLINKSFROMTOTHREE, FINDDOCSCONTAINING, SHOWRELATIONOF2VERSIONS — modify no state component. By the frame-vacuity of pure observation, `Σ' = Σ` and therefore `(A e, d, ℓ :: proj(e, d, Σ') = proj(e, d, Σ) ∧ Σ'.L(ℓ) = Σ.L(ℓ))`. The seventeen-command surjection is therefore complete: every FEBE command either (a) decomposes via LP-MAP into atoms whose displacement modes are catalogued, or (b) frames all projections by LP-FRAME-READ.

Gregory's implementation evidence corroborates the decomposition: the three POOM-mutating sites in udanax-green — the V-displacement decrement in `deletend` (DELETEVSPAN: the K.μ⁻ part), the V-displacement add in `rearrangend` (REARRANGE: K.μ~), and the V-displacement add in `makegappm` (INSERT/COPY mid-document: the K.μ~ part of the composition) — are the only three points in the codebase where existing POOM crums have their V-coordinates mutated. All other operations (APPEND, COPY at the subspace end, CREATELINK, CREATENEWVERSION) only append new mappings without disturbing existing ones, falling under pure K.μ⁺. The implementation's "compound" deletend (which both removes crums and shifts survivors) and "compound" makegappm (which both shifts existing crums and inserts new ones) are evidence that the FEBE-level operations are composed; the abstract specification decomposes them into the pure atoms whose displacement is each given by exactly one of LP-EXT-PURE, LP-CONTR-PURE, LP-REARR, or LP-FRAME.

## What Is Permanent — The Still Point

Six properties together establish that the link holder's references survive arbitrary state transitions.

**LP-IMM (Endset immutability).** For every state transition `Σ → Σ'` and every `ℓ ∈ dom(Σ.L)`:

  `Σ'.L(ℓ) = Σ.L(ℓ)`

This is L12 (ASN-0043), reasserted here as the foundation of the projection design. The link is value-immutable: every endset in every slot is preserved verbatim. For each `i ∈ {1, ..., |Σ.L(ℓ)|}`:

  `Σ'.L(ℓ).eᵢ = Σ.L(ℓ).eᵢ`

This follows from tuple equality (component-wise) under L6 (ASN-0043) and the link value's invariance under any state transition the system admits.

**LP-COV (Coverage permanence).** Since `coverage` is a deterministic function of the endset (ASN-0043's coverage definition), endset immutability immediately yields coverage permanence:

  `(A Σ → Σ', ℓ ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(ℓ)| :: coverage(Σ'.L(ℓ).eᵢ) = coverage(Σ.L(ℓ).eᵢ))`

The set of I-addresses an endset references is fixed at link creation. No transition can extend, contract, redirect, or relabel coverage.

**LP-CON (Content allocation persistence).** Content at every I-address that has ever been allocated persists with its value. By P0 (ASN-0047) — which subsumes S0 (ASN-0036) — for every `Σ → Σ'`:

  `(A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))`

The statement scopes universally over `dom(Σ.C)`, not over coverage specifically — this matters because, by L4 (ASN-0043), an endset's coverage may reference addresses not yet in `dom(Σ.C)`. Nelson's design intent makes this explicit: "A span that contains nothing today may at a later time contain a million documents" and "these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." Endset spans designate *regions* of tumbler space; whether storage backs a given coordinate is a separate, mutable matter resolved at projection time.

We can therefore partition coverage at any state Σ:

  `coverage(eᵢ) = (coverage(eᵢ) ∩ dom(Σ.C))  ∪  (coverage(eᵢ) \ dom(Σ.C))`

For `a` in the first part — *currently allocated* coverage — LP-CON guarantees that the bytes at `a` are fixed forever and that `a` remains in `dom(Σ'.C)`. For `a` in the second part — *speculative* or *forward-referencing* coverage — LP-CON makes no claim about `a` at Σ, but the moment any subsequent K.α allocates `a` (necessarily with some value `Σ'.C(a)`), the address transitions into the first part and LP-CON guarantees its value persists thereafter. The link does not need updating: the address enters the link's effective referenced set automatically, by virtue of having been in coverage all along.

Two consequences. *First*: the link holder's reliance is that "the content at each currently-allocated address in my coverage is permanent" — never that "every address in coverage holds content at every state." The reliance contract excludes the speculative-coverage region from any content claim at Σ; it asserts only that, *if and when* coverage gets populated, the value persists. *Second*: when a future K.α allocates an I-address that happens to fall within an existing endset's coverage, that allocation becomes part of the link's effective referenced set without modifying the link. The discipline that prevents accidental absorption rests on (i) *ownership scope* — "The owner of a given item controls the allocation of the numbers under it" (LM 4/20) limits who can populate under a given address prefix; (ii) *creator choice* — endsets are span-*sets*, so a creator who wants exact reference (no forward-extension) can specify the union of currently-existing single-byte spans rather than a broad range; and (iii) *query precision* — searches that target a specific subset of coverage use exact-overlap matching, not membership against the full span (cf. LP-DISC, where `discoverable` requires intersection with a specific V-window, not enclosure by the whole coverage). The architecture admits forward-referencing coverage as a designed capability; whether a given specification is *well-behaved* in some application-level sense is a discipline question at the link-creation layer, not an invariant question at the projection or content-store layer.

The coverage is preserved (LP-COV); the content at addresses ever populated within coverage is preserved (LP-CON); the addresses themselves cannot be reused (T8, ASN-0034). Together these give the *identity of what the link references* as an unconditional permanent: each named address either holds nothing yet, or holds a fixed value forever.

**LP-MON (Link store monotonicity).** Once created, a link cannot be removed:

  `(A Σ → Σ' :: dom(Σ.L) ⊆ dom(Σ'.L))`

This is L12a (ASN-0043). The link's address persists; no operation collects link addresses for reuse.

**LP-SLOT (Slot permanence).** The slot index of each endset within a link is positional (L6, ASN-0043). Combining with LP-IMM, the endset at slot `i` of `Σ'.L(ℓ)` is identically the endset at slot `i` of `Σ.L(ℓ)`. The directional roles — source as slot 1, target as slot 2, type as slot 3 under the StandardTriple convention — are invariant across all state transitions. No operation swaps, relabels, or permutes the slots of an existing link.

**LP-TYPE (Type slot permanence).** As the specialization of LP-IMM and LP-SLOT at `i = 3`:

  `(A Σ → Σ', ℓ ∈ dom(Σ.L) :: Σ'.L(ℓ).type = Σ.L(ℓ).type)`

In particular `coverage(Σ'.L(ℓ).type) = coverage(Σ.L(ℓ).type)`, so type identity in the sense of `same_type` (L8, ASN-0043) — equality of coverage on the type slot — is preserved across all state changes. The link's type relation cannot drift.

## What Displaces — The Moving Frame

The arrangement `Σ.M(d)` is the only state component that arrangement transitions modify. By the frame conditions in ASN-0047, the transitions K.μ⁺, K.μ⁺_L, K.μ⁻, and K.μ~ all leave `C, L, E, R` unchanged and affect only `M(d)` for one target document `d`, with `M'(d') = M(d')` for every `d' ≠ d`. The projection `proj(e, d, Σ)` is a function of `Σ.M(d)`; when `Σ.M(d)` changes, the projection can change. We catalog the modes.

**LP-REARR (Displacement under rearrangement).** Let `Σ → Σ'` be a K.μ~ transition on `d` realized by the bijection `π : dom(Σ.M(d)) → dom(Σ'.M(d))` with `Σ'.M(d)(π(v)) = Σ.M(d)(v)` for all `v ∈ dom(Σ.M(d))`. By K.μ~-FIX (ASN-0047), `dom(Σ'.M(d)) = dom(Σ.M(d))`, so `π` is a permutation. For any endset `e`:

  `proj(e, d, Σ')`
  `= {v' ∈ dom(Σ'.M(d)) : Σ'.M(d)(v') ∈ coverage(e)}`
  `= {π(v) : v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(π(v)) ∈ coverage(e)}`     by re-parameterizing v' = π(v)
  `= {π(v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) ∈ coverage(e)}`         by the bijection equation
  `= π(proj(e, d, Σ))`

The projection is displaced by exactly `π`. Its cardinality is preserved (`π` is a bijection). The same I-addresses still appear in `d`'s arrangement; their V-positions have moved. A reader querying through `d` sees the link's endpoints at new V-positions, but the same content — and the link is unchanged.

**LP-CONTR-PURE (Shrinkage under pure contraction).** Let `Σ → Σ'` be a pure K.μ⁻ transition on `d` with retention set `R ⊆ dom(Σ.M(d))` such that `Σ'.M(d) = Σ.M(d) ↾ R` — pure restriction, with no relabeling of surviving V-positions (per K.μ⁻ effect, ASN-0047). For any endset `e`:

  `proj(e, d, Σ')`
  `= {v ∈ R : Σ'.M(d)(v) ∈ coverage(e)}`
  `= {v ∈ R : Σ.M(d)(v) ∈ coverage(e)}`        since Σ'.M(d) and Σ.M(d) agree on R
  `= proj(e, d, Σ) ∩ R`

The projection is the original projection restricted to surviving V-positions. V-positions whose I-addresses were in `coverage(e)` but whose V-positions are no longer in `dom(Σ'.M(d))` are silently dropped from the projection. The I-addresses themselves are unaffected — LP-CON keeps them in `dom(C)` forever; they are simply no longer reachable through `d`'s arrangement at those V-positions. They may still be reachable through other V-positions in `d` (if S5 sharing applies — multiple V-positions can map to the same I-address) or through arrangements of other documents.

This is the partial-survival case. Of the `k` I-addresses in `coverage(e)` originally projected to `k` V-positions in `d`, some `k' ≤ k` survive. The link's endpoint in `d` narrows from `k` V-positions to `k'`, but the link itself is unchanged.

**LP-EXT-PURE (Growth under pure extension).** Let `Σ → Σ'` be a pure K.μ⁺ or K.μ⁺_L transition on `d` introducing new V→I mappings at V-positions disjoint from `dom(Σ.M(d))` — no relabeling of any pre-existing V-position. For any endset `e`:

  `proj(e, d, Σ')`
  `= {v ∈ dom(Σ'.M(d)) : Σ'.M(d)(v) ∈ coverage(e)}`
  `= {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)} ∪ {v_new ∈ dom(Σ'.M(d)) \ dom(Σ.M(d)) : Σ'.M(d)(v_new) ∈ coverage(e)}`
  `= proj(e, d, Σ) ∪ {v_new : Σ'.M(d)(v_new) ∈ coverage(e)}`

In particular `proj(e, d, Σ') ⊇ proj(e, d, Σ)`: the projection grows monotonically, gaining exactly those new V-positions whose I-addresses lie in coverage.

The endset is unchanged: the link did not expand to include new content. The *projection* in this particular document grew because the document's arrangement happens to add a V→I mapping targeting an address that was already in coverage. The most common cause is COPY/VCOPY transcluding content that was already linked — the same I-addresses now mapped at new V-positions in `d`. For INSERT under T9 (ForwardAllocation, ASN-0034), the fresh I-addresses from K.α are strictly greater than every prior allocation, so they typically lie *outside* coverage; the growth term is then empty and `proj(e, d, Σ') = proj(e, d, Σ)`.

The two pure statements LP-EXT-PURE and LP-CONTR-PURE apply when the FEBE-level operation realizes only the pure atom — that is, when the operation does not need to relabel any pre-existing V-position. APPEND, COPY/VCOPY at the subspace end, and CREATENEWVERSION's transclusions are pure K.μ⁺ (no shift). DELETEVSPAN at the subspace tail is pure K.μ⁻ (no shift). MAKELINK is pure K.μ⁺_L (no shift). For mid-subspace INSERT and interior DELETEVSPAN — the FEBE operations that compose pure atoms with K.μ~ — the *composed* statements below apply.

**LP-EXT-COMP (Growth composed with within-subspace shift).** Let `Σ → Σ''` be a composition K.μ~ ∘ K.μ⁺ on `d` realizing FEBE INSERT mid-subspace (or COPY/VCOPY mid-subspace), where K.μ~ relabels pre-existing V-positions in the affected subspace by the bijection `π` (shifting them forward to make room) and K.μ⁺ then introduces new V→I mappings at the freed V-positions. For any endset `e`, applying LP-REARR then LP-EXT-PURE composes:

  `proj(e, d, Σ'') = π(proj(e, d, Σ)) ∪ {v_new ∈ dom(Σ''.M(d)) \ π(dom(Σ.M(d))) : Σ''.M(d)(v_new) ∈ coverage(e)}`

Pre-existing coverage-mapping V-positions move to their π-images; new V-positions are added iff their I-addresses fall in coverage.

**LP-CONTR-COMP (Shrinkage composed with within-subspace shift).** Let `Σ → Σ''` be a composition K.μ~ ∘ K.μ⁻ on `d` realizing FEBE DELETEVSPAN with interior deletion, where K.μ⁻ restricts to `R_ret` and K.μ~ then relabels surviving V-positions in the affected subspace by the bijection `π'` (shifting them backward to close the gap). For any endset `e`, applying LP-CONTR-PURE then LP-REARR composes:

  `proj(e, d, Σ'') = π'(proj(e, d, Σ) ∩ R_ret)`

Surviving coverage-mapping V-positions in `R_ret` are re-labeled by `π'`; dropped V-positions are gone.

The two composed claims hold *as derived consequences* of LP-EXT-PURE, LP-CONTR-PURE, and LP-REARR applied in sequence: the abstract decomposition matches the implementation reality without requiring any non-atomic statement.

**LP-CROSS (Cross-document independence).** For any arrangement transition `Σ → Σ'` whose target document is `d`, and any `d' ≠ d`:

  `(A e :: proj(e, d', Σ') = proj(e, d', Σ))`

Projections are computed per document. A change to `M(d)` cannot affect `proj(e, d', Σ)` for any `d' ≠ d`. The link's rendering in each document depends only on that document's arrangement.

This is what makes the link a *single* object that can be presented through *many* documents: each document's rendering is independent, and edits in one document cannot corrupt the link's appearance in another.

## Survival and Discoverability — Derivation Chains

We now establish two derived guarantees. Each carries an explicit premise set so that a reader can audit which still-point and moving-frame claims are load-bearing, and each is accompanied by a weakest-precondition computation that surfaces the transition predicates strengthening or weakening the guarantee.

**LP-SURV (Survival condition).**

  *Statement.* `proj(e, d, Σ) ≠ ∅  ⟺  ran(Σ.M(d)) ∩ coverage(e) ≠ ∅`

  *Premises (single-state).* The endset projection definition (`proj_def`). At a single state Σ, LP-SURV is an immediate consequence of the definition unfolded against `ran` — no other claim is consumed.

  *Premises (across-transitions specialization).* When we wish to lift LP-SURV across `Σ → Σ'`, we additionally need:
  - LP-COV — `coverage(e)` is the same at Σ and Σ', so the right-hand side's `coverage(e)` term is well-defined and stable;
  - LP-CON — every I-address ever in `coverage(e) ∩ dom(C)` remains in `dom(C')`, so the question of whether a coverage I-address is present in `ran(Σ'.M(d))` is meaningful;
  - LP-IMM — the endset itself is preserved, ensuring the LP-COV consequence has its hypothesis.

  In compact form: `LP-SURV ≡ proj_def ⊨ (proj ≠ ∅ ⟺ ran ∩ coverage ≠ ∅)`; lifting across transitions adds `LP-IMM ⇒ LP-COV ⇒ stability of the coverage term`.

  *Derivation walk.*
  Forward direction (`proj ≠ ∅ ⇒ ran ∩ coverage ≠ ∅`). Assume `proj(e, d, Σ) ≠ ∅`. Pick `v ∈ proj`. By definition of `proj`, `v ∈ dom(Σ.M(d))` and `Σ.M(d)(v) ∈ coverage(e)`. By definition of `ran`, `Σ.M(d)(v) ∈ ran(Σ.M(d))`. Therefore `Σ.M(d)(v) ∈ ran(Σ.M(d)) ∩ coverage(e)`, witnessing non-emptiness.
  Reverse direction (`ran ∩ coverage ≠ ∅ ⇒ proj ≠ ∅`). Pick `a ∈ ran(Σ.M(d)) ∩ coverage(e)`. By definition of `ran`, `(E v ∈ dom(Σ.M(d)) :: Σ.M(d)(v) = a)`. Pick such `v`. Since `a ∈ coverage(e)`, by definition of `proj`, `v ∈ proj(e, d, Σ)`. Therefore `proj(e, d, Σ) ≠ ∅`.

  Nelson's principle "links survive editing if anything is left at each end" reads precisely here: the link's endpoint in `d` is non-empty iff `d`'s arrangement still maps to some address in coverage. Partial survival — when the intersection has shrunk but is still non-empty — is the realistic case.

  *Weakest-precondition computation.* Fix the postcondition `R := proj(e, d, Σ) ≠ ∅`. We compute `wp(K, R)` for each transition family on the target document `d` (transitions on `d' ≠ d` leave `R` unchanged by LP-CROSS):

  - `wp(K.μ⁺ on d, R)` =
    `(E v ∈ dom(Σ.M(d)) :: Σ.M(d)(v) ∈ coverage(e))`
    `∨ (E v_new ∈ (dom(Σ'.M(d)) \ dom(Σ.M(d))) :: Σ'.M(d)(v_new) ∈ coverage(e))`

    The wp weakens via the disjunctive new-mapping clause: K.μ⁺ never falsifies R (it can only add V-positions to `proj`), but it can establish R from the empty case if it transcludes a coverage I-address.

  - `wp(K.μ⁻ on d with retention R_ret, R)` =
    `(E v ∈ R_ret :: Σ.M(d)(v) ∈ coverage(e))`

    The wp strengthens beyond R itself: requires not just *some* coverage-mapping V-position before, but one *surviving* the contraction. K.μ⁻ is the only transition family that can falsify R.

  - `wp(K.μ~ on d, R)` =
    `(E v ∈ dom(Σ.M(d)) :: Σ.M(d)(v) ∈ coverage(e))`
    = R

    K.μ~ is a bijective permutation; the domain is constant and the I-addresses at the V-positions are constant under re-labeling. The wp is exactly R.

  - `wp(K.μ⁺_L on d, R)` = R, for endsets whose coverage is entirely in the text subspace. For link-subspace endsets, the disjunctive new-mapping clause from K.μ⁺ applies, but the new V-position is at the end of the link subspace and its I-address is the newly allocated link address — so R is established when the endset's coverage happens to include the new link address.

  - `wp(K, R) = R` for K ∈ {K.α, K.λ, K.δ, K.ρ} or K on `d' ≠ d`.

  The wp computation surfaces three transition predicates governing LP-SURV:
  - K.μ⁻ alone can weaken R from true to false (by deleting the last coverage-mapping V-position);
  - K.μ⁺ alone can strengthen R from false to true (by inserting a coverage-mapping V-position);
  - K.μ~ and K.μ⁺_L (on text-subspace endsets) preserve R exactly.

  The strengthening direction is the basis of "links survive editing": once R is true at some state, only K.μ⁻ can falsify it, and only by removing the entire intersection. The weakening boundary — `R_ret ∩ proj = ∅` — is exactly the exact-coverage deletion case (see boundary cases).

**LP-DISC (Discoverability via I-address intersection).**

  *Statement.* A link `ℓ` is *discoverable* from a V-span query `(d, [v_lo, v_hi))` at state Σ iff some endset's coverage intersects the I-addresses currently placed in the queried V-range of `d`:

    `discoverable(ℓ, d, [v_lo, v_hi), Σ)`
    `⟺ (E i, v : 1 ≤ i ≤ |Σ.L(ℓ)| ∧ v_lo ≤ v < v_hi ∧ v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(Σ.L(ℓ).eᵢ))`

  *Premises.* Discoverability is non-trivial precisely because it requires both directions of the projection relation to be well-defined:
  - LP-COV — `coverage(Σ.L(ℓ).eᵢ)` is well-defined and stable for every slot i;
  - LP-MON — `ℓ ∈ dom(Σ.L)` so the link's endsets are addressable at the query state (LP-IMM via LP-MON gives stability of the link's value);
  - LP-SLOT — slot indices range over the same domain at every state, so the existential over i is well-formed;
  - LP-CROSS — discoverability in `d` depends only on `Σ.M(d)`, not on any other document's arrangement;
  - The endset projection definition (`proj_def`) — discoverability is equivalent to `(E i : proj(Σ.L(ℓ).eᵢ, d, Σ) ∩ [v_lo, v_hi) ≠ ∅)`, requiring forward (endset-to-V) and reverse (V-to-endset) projection to be well-defined.

  In compact form: `LP-COV ∧ LP-MON ∧ LP-SLOT ∧ LP-CROSS ∧ proj_def ⊨ LP-DISC`.

  *Well-definedness.* The biconditional itself holds *by definition*: the right-hand side `(E i, v : ... : Σ.M(d)(v) ∈ coverage(Σ.L(ℓ).eᵢ))` *is* the definition of `discoverable(ℓ, d, [v_lo, v_hi), Σ)`. There is no theorem to derive; what we owe is a demonstration that the definition is *well-formed* at every reachable state and that the *computation realizing it* — forward and reverse — terminates and is sound. The remainder of this section discharges that obligation.
  Forward (from source): The link's endsets are addressable by LP-MON (`ℓ` is in `dom(Σ.L)`) and stable by LP-IMM (the endset values are preserved). For each slot `i ∈ {1, ..., |Σ.L(ℓ)|}`, LP-SLOT ensures the slot index is valid and `coverage(Σ.L(ℓ).eᵢ)` is determined by LP-COV. The forward predicate `Σ.M(d)(v) ∈ coverage(eᵢ)` is well-defined at every Σ: `Σ.M(d)(v)` is read from the document's current arrangement, `coverage(eᵢ)` is read from the (permanent) endset. A bounded iteration `v ∈ [v_lo, v_hi) ∩ dom(Σ.M(d))` × `i ∈ {1, ..., |Σ.L(ℓ)|}` decides the predicate; both ranges are finite (by `dom(Σ.M(d))` finite and `|Σ.L(ℓ)|` finite per L3, ASN-0043).
  Reverse (from target): given a V-position `v` and a candidate I-address `Σ.M(d)(v) = a`, the search "which links discover `a`?" iterates over `dom(Σ.L)`; for each ℓ in the domain, for each slot i, the predicate `a ∈ coverage(Σ.L(ℓ).eᵢ)` is well-defined by LP-MON + LP-COV + LP-SLOT. The search terminates because `dom(Σ.L)` is finite at every reachable state (L-fin, ASN-0043).
  Per-document scoping: LP-CROSS ensures that the discoverability check is determined entirely by `Σ.M(d)`; no other document's state participates.
  The forward and reverse walks are two terminating decision procedures for the same definitional predicate; they agree on the value `discoverable(ℓ, d, [v_lo, v_hi), Σ)` because they are evaluating the same right-hand-side formula. The biconditional in the statement records this equivalence between the predicate's *name* (`discoverable`) and its *defining formula*.

  *Weakest-precondition reading.* For the postcondition `D := discoverable(ℓ, d, [v_lo, v_hi), Σ)`:
  - `wp(K.μ⁻ on d, D)` requires `(E i, v : v ∈ R_ret ∩ [v_lo, v_hi) : Σ.M(d)(v) ∈ coverage(eᵢ))` — the queried V-window must retain at least one coverage-mapping V-position.
  - `wp(K.μ⁺ on d, D)` is `D ∨ (some newly added V-position in [v_lo, v_hi) maps to some eᵢ's coverage)`.
  - `wp(K.μ~ on d, D)` is `(E i, v : π(v) ∈ [v_lo, v_hi) ∧ v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(eᵢ))` — the V-window must be unmapped from its pre-image under π.

Discovery is determined by I-address intersection alone. It is *blind* to:

- which document originated `ℓ` — there is no provenance check on `home(ℓ)` (L1a, ASN-0043);
- whether `ℓ`'s V-position is mapped in `d`'s link subspace — a link is visible through its coverage, not through its placement;
- whether the I-addresses in coverage are held by other documents — any intersection with `d`'s range suffices.

Partial overlap is sufficient. If `coverage(eᵢ) = {a₁, ..., a_k}` and the V-range query maps to only `{a₃}`, `ℓ` is discoverable: the intersection `{a₃}` is non-empty.

This is the basis of Nelson's "a link to one version is a link to all versions": any document whose arrangement maps to coverage addresses discovers the link, and versions inherit coverage addresses by virtue of transclusion.

## What the Link Holder Can Rely On

Synthesizing the guarantees from LP-IMM through LP-DISC, the link holder can rely on the following:

(a) *The endsets I specified are stored exactly as I specified them.* By LP-IMM, the value `Σ.L(ℓ)` is preserved forever after creation.

(b) *The coverage I specified — the set of I-addresses my endset names — is permanent.* By LP-COV.

(c) *The content at each currently-allocated address in my coverage is permanent.* By LP-CON. If the bytes were there when I created the link, they are there now, with the same value. Speculative-coverage addresses (in coverage but not yet allocated) carry no value claim at the current state, but acquire one — irrevocable — as soon as they are allocated.

(d) *The link's address is permanent.* By LP-MON.

(e) *My slot assignments — which endset is "source," "target," "type" — are permanent.* By LP-SLOT.

(f) *The link's type identity is permanent.* By LP-TYPE. Two links related by `same_type` remain so forever.

(g) *I can find the V-positions of my endsets in any document by projection.* By the definition of `proj`, this is always possible — there is no caching or staleness; every query computes from current state.

(h) *In any document whose arrangement maps to my coverage, my link is discoverable.* By LP-DISC, with no provenance restriction.

(i) *Edits to one document cannot affect my link's rendering in another document.* By LP-CROSS, projections are per-document.

(j) *Arrangement changes cannot modify my link's stored value.* By LP-FRAME (below), arrangement transitions name only `M` in their effects.

(k) *The link survives partial deletion as long as any address in coverage remains in any document's arrangement.* By LP-SURV applied per document.

## What the Link Holder Cannot Rely On — Non-Invariants with Witnesses

The displacement modes catalog what is *not* invariant. These are not failures — they are deliberate flexibilities of the design. Each non-invariant is paired with a concrete witness transition that violates it; without a witness, "not preserved" is empty.

**LP-NOV (V-positions are not stable).**

  *Statement.* There exist link `ℓ`, slot `i`, document `d`, and a pair of states `Σ → Σ'` such that:

    `proj(Σ.L(ℓ).eᵢ, d, Σ) ≠ proj(Σ.L(ℓ).eᵢ, d, Σ')`

  with the inequality holding *as sets of V-positions*, not as cardinalities (cardinality non-stability is the separate claim LP-NOC).

  *Witness transition (K.μ⁺ family).* Let `Σ.L(ℓ).e₁ = {(a, 0.1)}` for some I-address `a`, so `coverage(e₁) = {a}`. Suppose `Σ.M(d)(1.5) = a` and `1.5` is the only V-position in `d` mapping to `a`. Then `proj(e₁, d, Σ) = {1.5}`. Apply K.μ⁺ on `d` inserting one fresh byte at V-position 1.3 in the text subspace: the new arrangement allocates `b ∉ coverage(e₁)` at 1.3, and the within-subspace shift moves the V-position formerly at 1.5 to 1.6 (Σ'.M(d)(1.6) = a). Then `proj(e₁, d, Σ') = {1.6}`. The V-position changed: `{1.5} ≠ {1.6}` — LP-NOV holds.

  *Structural reason.* LP-NOV is a direct consequence of LP-REARR with non-identity π and of K.μ⁺ when the insertion point is not at the subspace end. The only transitions that preserve V-positions exactly are K.μ~ with identity π (a no-op rearrangement), K.μ⁺ at the subspace end with no within-subspace shift, and K.μ⁻ with `R_ret ⊇ proj(eᵢ, d, Σ)` and no shift. The general case displaces.

**LP-NOC (Cardinality is not stable).**

  *Statement.* There exist link `ℓ`, slot `i`, document `d`, and a pair of states `Σ → Σ'` such that:

    `|proj(Σ.L(ℓ).eᵢ, d, Σ)| ≠ |proj(Σ.L(ℓ).eᵢ, d, Σ')|`

  *Witness for shrinkage (K.μ⁻ family).* Let `coverage(Σ.L(ℓ).e₁) = {a, b}` with `a ≠ b`. Let `Σ.M(d)(1.4) = a` and `Σ.M(d)(1.5) = b`, so `proj(e₁, d, Σ) = {1.4, 1.5}` (cardinality 2). Apply K.μ⁻ on `d` with retention `R_ret = dom(Σ.M(d)) \ {1.5}`. Then `proj(e₁, d, Σ') = {1.4, 1.5} ∩ R_ret = {1.4}` (cardinality 1). Cardinality shrunk from 2 to 1: `2 ≠ 1`, LP-NOC witnessed.

  *Witness for growth (K.μ⁺ family with transclusion).* From the original state Σ, apply K.μ⁺ on `d` transcluding `a` at a new V-position 7.3 with `Σ'.M(d)(7.3) = a`. Then `proj(e₁, d, Σ') = {1.4, 1.5, 7.3}` (cardinality 3). Cardinality grew from 2 to 3: `2 ≠ 3`, LP-NOC witnessed bidirectionally.

  *Structural reason.* Cardinality is `|coverage(e) ∩ ran(Σ.M(d))|` plus an S5-sharing inflation if multiple V-positions map to the same coverage I-address. K.μ⁻ can only shrink `ran(Σ.M(d))`; K.μ⁺ can only grow it. Either family can move cardinality strictly; K.μ~ alone cannot (LP-REARR preserves cardinality).

**LP-NOD (Document membership is not stable).**

  *Statement.* There exists link `ℓ`, slot `i`, and a pair of states `Σ → Σ'` such that:

    `footprint(ℓ, i, Σ) ≠ footprint(ℓ, i, Σ')`

  (Recall the footprint definition: `footprint(ℓ, i, Σ) = {d ∈ Σ.E_doc : proj(Σ.L(ℓ).eᵢ, d, Σ) ≠ ∅}`.)

  *Witness for growth (K.μ⁺ on a new document).* Let `coverage(Σ.L(ℓ).e₁) = {a}`. Suppose `Σ.M(d₁)(1.3) = a` and `Σ.M(d₂)` does not map to `a` (`a ∉ ran(Σ.M(d₂))`). Then `footprint(ℓ, 1, Σ) = {d₁}`. Apply K.μ⁺ on `d₂` transcluding `a` at V-position 5.5: `Σ'.M(d₂)(5.5) = a`. Then `proj(e₁, d₂, Σ') = {5.5} ≠ ∅`, so `footprint(ℓ, 1, Σ') = {d₁, d₂}`. The footprint grew: `{d₁} ≠ {d₁, d₂}`, LP-NOD witnessed.

  *Witness for shrinkage (K.μ⁻ removing the last coverage I-address).* From the footprint state `{d₁, d₂}` above, apply K.μ⁻ on `d₂` with retention `R_ret = dom(Σ'.M(d₂)) \ {5.5}`. Then `proj(e₁, d₂, Σ'') = ∅`, so `footprint(ℓ, 1, Σ'') = {d₁}`. The footprint shrank back.

  *Structural reason.* The footprint is the indexed family `{d : ran(Σ.M(d)) ∩ coverage(eᵢ) ≠ ∅}`. Since `ran(Σ.M(d))` is mutable under K.μ⁺ and K.μ⁻ on `d`, any transition that adds or removes a coverage I-address from any document's range changes the footprint. The link is not "located" in a fixed set of documents — its presentation footprint follows the placement of its coverage I-addresses across the system.

Nothing the link holder specified about *where* the endpoints appear is preserved, because nothing about *where* was ever stored. The link stores *what* (coverage); the *where* is recomputed from current state.

## Frame Conditions

The arrangement transitions K.μ⁺, K.μ⁺_L, K.μ⁻, and K.μ~ all specify in their frame condition:

  `C' = C  ∧  L' = L  ∧  E' = E  ∧  R' = R  ∧  (A d' : d' ≠ d : M'(d') = M(d'))`

per ASN-0047. The link store `L` is explicitly framed: it is not modified by any arrangement transition.

**LP-FRAME (Link frame under arrangement transitions).** For any K.μ⁺ / K.μ⁺_L / K.μ⁻ / K.μ~ transition `Σ → Σ'`:

  `(A ℓ ∈ dom(Σ.L) :: Σ'.L(ℓ) = Σ.L(ℓ))`

In conjunction with LP-CROSS, this gives the full asymmetry of the displacement: the link itself is touched by *no* arrangement transition, the projection in the targeted document `d` may be displaced, and the projection in every other document `d'` is unchanged. The arrangement-layer transitions are precisely the ones that can move V-positions; they do so only in their target document, and they never reach into the link store.

Allocation transitions also leave projections of existing links unchanged at the atomic level. K.α adds to `C` with frame `(A d :: M'(d) = M(d))`; K.λ adds to `L` (a new link, not modifying existing entries) with the same arrangement frame; K.δ adds to `E` and creates new documents with `M'(e) = ∅` for new `e ∈ E_doc`; K.ρ modifies only `R`. None of these atomic transitions changes any existing `proj(e, d, Σ)`. Projections move only when arrangements move, and arrangements move only through the K.μ family.

## A Worked Example: Atomic Decomposition of INSERT and DELETEVSPAN

We exhibit a concrete example tracing a projection through a sequence of FEBE-level state transitions, with each FEBE operation decomposed into its constituent pure atoms. The example uses tumbler-decimal notation for V-positions where the leading "1." denotes the text subspace (`s_T = 1`).

*Initial state Σ₀.* Document `d` has an arrangement mapping the text subspace:

  `Σ₀.M(d)(1.1) = a₁,  Σ₀.M(d)(1.2) = a₂,  Σ₀.M(d)(1.3) = a₃,`
  `Σ₀.M(d)(1.4) = a₄,  Σ₀.M(d)(1.5) = a₅`

where `a₁, ..., a₅` are distinct I-addresses denoting the bytes "H", "E", "L", "L", "O".

A link ℓ exists with endset `Σ₀.L(ℓ).e₁ = {(a₂, 0.3)}` — coverage is the three-byte span starting at `a₂`, namely `{a₂, a₃, a₄}` (denoting "ELL"). By the projection definition:

  `proj(e₁, d, Σ₀) = {v ∈ dom(Σ₀.M(d)) : Σ₀.M(d)(v) ∈ {a₂, a₃, a₄}} = {1.2, 1.3, 1.4}`

The link's endpoint appears at V-positions 1.2, 1.3, 1.4 — three V-positions, contiguous. Cardinality 3.

*FEBE INSERT "XY" at V-position 1.3, decomposed as K.α ∘ K.μ~ ∘ K.μ⁺.* We trace through each atom.

**Atom 1 — K.α** allocates two fresh I-addresses `b₁, b₂` in `Σ.C`; by T9 (ForwardAllocation, ASN-0034), `b₁, b₂` are strictly greater than every prior I-address allocated under the relevant allocator, so `b₁, b₂ ∉ {a₁, ..., a₅}` and `b₁, b₂ ∉ coverage(e₁)`. No `M(d)` is touched. By LP-FRAME, `proj(e₁, d, Σ₀.⁺K.α) = proj(e₁, d, Σ₀) = {1.2, 1.3, 1.4}`.

**Atom 2 — K.μ~** on `d` relabels the pre-existing V-positions 1.3, 1.4, 1.5 forward by 0.2 (making room for the insertion). The relabel bijection `π` acts as identity on {1.1, 1.2} and as `v ↦ v + 0.2` on {1.3, 1.4, 1.5}. The intermediate arrangement Σ₀.⁺K.α.⁺K.μ~ satisfies:

  `M(d)(1.1) = a₁,  M(d)(1.2) = a₂,  M(d)(1.5) = a₃,  M(d)(1.6) = a₄,  M(d)(1.7) = a₅`

(V-positions 1.3 and 1.4 are not yet in the domain.) By LP-REARR:

  `proj(e₁, d, after K.μ~) = π(proj(e₁, d, Σ₀)) = π({1.2, 1.3, 1.4}) = {1.2, 1.5, 1.6}`

Cardinality preserved at 3; V-positions displaced from {1.2, 1.3, 1.4} to {1.2, 1.5, 1.6}.

**Atom 3 — K.μ⁺** on `d` adds two new V→I mappings `1.3 ↦ b₁` and `1.4 ↦ b₂` at V-positions disjoint from the relabeled domain. The post-state Σ₁ arrangement:

  `Σ₁.M(d)(1.1) = a₁,  Σ₁.M(d)(1.2) = a₂,  Σ₁.M(d)(1.3) = b₁,  Σ₁.M(d)(1.4) = b₂,`
  `Σ₁.M(d)(1.5) = a₃,  Σ₁.M(d)(1.6) = a₄,  Σ₁.M(d)(1.7) = a₅`

By LP-EXT-PURE:

  `proj(e₁, d, Σ₁) = proj(e₁, d, after K.μ~) ∪ {v_new ∈ {1.3, 1.4} : Σ₁.M(d)(v_new) ∈ coverage(e₁)}`
                    `= {1.2, 1.5, 1.6} ∪ ∅`
                    `= {1.2, 1.5, 1.6}` ✓

The growth term is empty because `b₁, b₂ ∉ coverage(e₁)` (T9). The composed displacement is exactly LP-EXT-COMP applied to the pair (K.μ~, K.μ⁺):

  `proj(e₁, d, Σ₁) = π(proj(e₁, d, Σ₀)) ∪ ∅ = {1.2, 1.5, 1.6}` ✓

LP-COV holds: `coverage(e₁)` is still `{a₂, a₃, a₄}`. LP-CON holds: `a₂, a₃, a₄ ∈ dom(Σ₁.C)` with the same byte values. LP-NOV is witnessed across Σ₀ → Σ₁: the V-position set changed from `{1.2, 1.3, 1.4}` to `{1.2, 1.5, 1.6}`. LP-NOC is *not* witnessed at this step: cardinality stayed at 3 because K.μ~ is bijective and the K.μ⁺ growth term was empty.

*FEBE DELETEVSPAN at V-span [1.5, 1.7), decomposed as K.μ⁻ ∘ K.μ~.* We trace through each atom.

**Atom 1 — K.μ⁻** on `d` with retention `R_ret = dom(Σ₁.M(d)) \ {1.5, 1.6} = {1.1, 1.2, 1.3, 1.4, 1.7}` realizes the pure restriction `Σ₁.M(d) ↾ R_ret`. The intermediate arrangement Σ₁.⁺K.μ⁻ satisfies:

  `M(d)(1.1) = a₁,  M(d)(1.2) = a₂,  M(d)(1.3) = b₁,  M(d)(1.4) = b₂,  M(d)(1.7) = a₅`

(V-position 1.7 retains its original label.) By LP-CONTR-PURE:

  `proj(e₁, d, after K.μ⁻) = proj(e₁, d, Σ₁) ∩ R_ret = {1.2, 1.5, 1.6} ∩ {1.1, 1.2, 1.3, 1.4, 1.7} = {1.2}`

Cardinality dropped from 3 to 1; the dropped V-positions 1.5 and 1.6 (which mapped to `a₃, a₄`) are no longer in the domain.

**Atom 2 — K.μ~** on `d` relabels the surviving V-position 1.7 backward by 0.2 to 1.5 (closing the gap). The relabel bijection `π'` acts as identity on {1.1, 1.2, 1.3, 1.4} and as `1.7 ↦ 1.5`. The post-state Σ₂ arrangement:

  `Σ₂.M(d)(1.1) = a₁,  Σ₂.M(d)(1.2) = a₂,  Σ₂.M(d)(1.3) = b₁,`
  `Σ₂.M(d)(1.4) = b₂,  Σ₂.M(d)(1.5) = a₅`

By LP-REARR:

  `proj(e₁, d, Σ₂) = π'(proj(e₁, d, after K.μ⁻)) = π'({1.2}) = {1.2}` ✓

The composed displacement is exactly LP-CONTR-COMP applied to the pair (K.μ⁻, K.μ~):

  `proj(e₁, d, Σ₂) = π'(proj(e₁, d, Σ₁) ∩ R_ret) = π'({1.2}) = {1.2}` ✓

LP-COV holds: `coverage(e₁)` is still `{a₂, a₃, a₄}`. LP-CON holds: `a₃ ∈ dom(Σ₂.C)` despite being absent from `ran(Σ₂.M(d))` — the I-address persists in the content store; only its V-mapping in `d` was removed. LP-NOC is witnessed across Σ₁ → Σ₂: cardinality dropped from 3 to 1. LP-SURV holds: `ran(Σ₂.M(d)) ∩ coverage(e₁) = {a₁, a₂, b₁, b₂, a₅} ∩ {a₂, a₃, a₄} = {a₂} ≠ ∅`, so `proj(e₁, d, Σ₂) ≠ ∅` — Nelson's "anything left at each end" reading holds with `a₂` as the witness.

The example verifies LP-EXT-PURE (atom 3 of INSERT), LP-CONTR-PURE (atom 1 of DELETEVSPAN), LP-REARR (atom 2 of INSERT and atom 2 of DELETEVSPAN), and their compositions LP-EXT-COMP (Σ₀ → Σ₁ overall) and LP-CONTR-COMP (Σ₁ → Σ₂ overall). LP-COV and LP-CON hold throughout. LP-NOV is witnessed at Σ₀ → Σ₁; LP-NOC is witnessed at Σ₁ → Σ₂. The link itself — the value `Σ.L(ℓ)` — is unchanged at all three states (LP-IMM, LP-FRAME).

## Boundary Cases

We work through cases that test the boundaries of the projection definition. The first six cases probe structural edge behaviors of the projection definition itself — degenerate inputs and the post-state structure under specific composed transitions (empty projection, empty endset, zero-width span, exact-coverage deletion, mid-coverage insertion, coverage cluster structure); the remaining cases test the interaction with versioning, ownership, and split coverage.

**Empty projection.** If `proj(Σ.L(ℓ).eᵢ, d, Σ) = ∅` for every `d`, the endset's coverage has no current V-position in any document. The link still exists (LP-MON); its coverage is still defined (LP-COV); the I-addresses in coverage still hold content if they were ever allocated (LP-CON). The link is *orphaned with respect to placement* but is not invalid. A subsequent K.μ⁺ transition placing any coverage address into some document's arrangement restores a non-empty projection in that document. The link is discoverable (LP-DISC) from no document during the orphan period; once any coverage address is placed, discovery from the receiving document becomes possible.

This is the strongest sense in which the link is decoupled from arrangements: it can be *fully absent from V-space* yet remain a well-defined link with a well-defined coverage and well-defined type.

**Empty endset.** Suppose `e = ∅` — an endset with no spans. Then `coverage(e) = (∪ (s, w) ∈ ∅ : ...) = ∅`, the empty union. By the projection definition:

  `proj(∅, d, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ ∅} = ∅`

for every `d ∈ Σ.E_doc` and every reachable state Σ. The projection is *vacuously defined* — total over its signature and constantly empty. The link object remains in `dom(Σ.L)` if it was admitted there; discoverability via this endset (LP-DISC for the slot containing `∅`) is identically false, since `(E v ∈ ... : Σ.M(d)(v) ∈ ∅)` is identically false. But discoverability via the link's *other* slots (the other directional endset, the type slot) is unaffected. The link does not vanish; only one of its endsets is empty-projecting. This is consistent with Nelson's "if anything is left at each end" reading — when *nothing* is at one end (because the endset itself names no I-addresses), the link has no semantic effect through that endset, but the link remains a well-defined object.

Whether ASN-0043 admits `∅` as a valid endset value is a constraint on the link store, not on the projection. The projection definition is total and answers `∅` whenever the input endset has empty coverage; no implementation pathology arises from this case at the abstract layer.

**Zero-width span.** Suppose a span `(s, 0)` with `s ∈ T` appears in `e`. Then:

  `coverage({(s, 0)}) = {t ∈ T : s ≤ t < s ⊕ 0} = {t : s ≤ t < s} = ∅`

(the half-open interval is empty when start equals end). The zero-width span contributes nothing to `coverage(e)`. By the projection definition, `proj(e, d, Σ)` is identical whether or not zero-width spans appear in `e` — they are *vanishing* contributors to coverage and therefore to projection. This is consistent with Nelson's design intent (spans denote content; a zero-width span denotes no content) and with Gregory's implementation evidence (udanax-green's `deletevspanpm` returns early on `iszerotumbler(&vspanptr->width)` — the implementation rejects zero-width operations, while the abstract projection is invariant under zero-width-span insertions into endsets).

The composite case — an endset whose every span has zero width — coincides with the empty-endset case: `coverage(e) = ∅`, `proj(e, d, Σ) = ∅` for all `d, Σ`.

**Coverage entirely in a single arrangement run vs. straddling multiple runs.** Let `coverage(e) = {a₁, ..., a_k}` with the I-addresses ordered as `a₁ < a₂ < ... < a_k` in tumbler order. Two sub-cases:

(i) *Single-run coverage placement.* Suppose `Σ.M(d)` maps V-positions `v₁ < v₂ < ... < v_k` to `a₁, ..., a_k` with `vⱼ = u + j·δ` for some constants `u, δ` — the I-addresses appear contiguously in V-space. Then `proj(e, d, Σ) = {v₁, ..., v_k}` is a single contiguous V-run. The link's endpoint renders as one continuous V-region.

(ii) *Multi-run coverage placement.* Suppose `Σ.M(d)` maps `a₁, ..., a_j` to V-positions in `[u, u + jδ)` and `a_{j+1}, ..., a_k` to V-positions in `[u', u' + (k-j)δ)` with `u' > u + jδ` — the I-addresses are split into two V-runs. Then `proj(e, d, Σ) = {v₁, ..., v_j} ∪ {v_{j+1}, ..., v_k}`, two non-contiguous V-clusters.

In both sub-cases the projection cardinality is `k` (assuming no S5 sharing). The projection definition does not distinguish single-run from multi-run; it returns the set of V-positions, leaving cluster structure to higher layers (rendering, retrieval). The number of V-runs equals the number of maximal V-contiguous segments in `proj(e, d, Σ)`; LP-NOV implies cluster structure is not stable across editing.

The straddling-versus-contained case generalizes: coverage may be split across `m` V-runs in `d` for `1 ≤ m ≤ k`; the projection is the union of `m` contiguous segments. LP-EXT-COMP can split a single run by inserting non-coverage content into its middle (see next case); LP-CONTR-COMP can merge two runs by deleting non-coverage content between them. The displacement claims do not distinguish single-cluster from multi-cluster projections in their statements; they hold structurally regardless.

**DELETE of the exact coverage range.** Suppose `Σ.M(d)` maps V-positions `[v_lo, v_hi)` to `coverage(eᵢ)` (so `proj(eᵢ, d, Σ) = [v_lo, v_hi)` as a contiguous V-range) and no other V-position in `d` maps to coverage. Apply the FEBE DELETEVSPAN — decomposed as K.μ⁻ ∘ K.μ~ — with retention `R_ret = dom(Σ.M(d)) \ [v_lo, v_hi)`. By LP-CONTR-PURE applied to the K.μ⁻ atom:

  `proj(eᵢ, d, after K.μ⁻) = proj(eᵢ, d, Σ) ∩ R_ret = [v_lo, v_hi) ∩ R_ret = ∅`

By LP-REARR applied to the subsequent K.μ~ atom (relabeling surviving V-positions backward), `proj(eᵢ, d, Σ') = π'(∅) = ∅`. The projection collapses to empty *in d* under either the pure or composed claim — the K.μ~ atom is the identity on the empty set.

The coverage I-addresses are unchanged in `dom(Σ.C)` (LP-CON); they are simply no longer in `ran(Σ.M(d))`. The link is now orphaned with respect to `d` but may still project non-trivially in other documents (LP-CROSS).

This is the *exact-coverage deletion* case, distinguished from *partial-coverage deletion* by the resulting projection cardinality:

- exact-coverage deletion: `R_ret ∩ proj(eᵢ, d, Σ) = ∅`, so `proj(eᵢ, d, Σ') = ∅`;
- partial-coverage deletion: `∅ ⊊ R_ret ∩ proj(eᵢ, d, Σ) ⊊ proj(eᵢ, d, Σ)`, so `∅ ⊊ proj(eᵢ, d, Σ') ⊊ proj(eᵢ, d, Σ)`.

Both fall under the same pair of claims LP-CONTR-PURE and LP-CONTR-COMP; the claims do not need to distinguish the two — the structural difference is in the resulting cardinality, which is exactly what the intersection `proj ∩ R_ret` reports. The exact case is the wp boundary at which `wp(K.μ⁻, R) = false` (R := projection non-empty in d): the retention removes the last coverage-mapping V-position. After exact deletion, LP-SURV holds vacuously *in d* (since the antecedent is now false), but it may still hold non-vacuously in other documents whose arrangements still map to coverage.

Gregory's implementation evidence confirms the count: at exact-coverage deletion, the implementation produces *zero* projection clusters (the spanning crum is `disown`ed and freed entirely); the projection set is empty.

**INSERT inside a coverage range.** Suppose `proj(eᵢ, d, Σ) = {v_a, v_{a+1}, v_{a+2}, v_{a+3}}` is a four-V-position contiguous run mapping to coverage I-addresses, occupying V-range `[v_a, v_a + 4δ)` for the V-step `δ`. Apply the FEBE INSERT mid-subspace — decomposed as K.α ∘ K.μ~ ∘ K.μ⁺ — at V-position `v_mid ∈ (v_a + δ, v_a + 3δ)` (strictly between v_{a+1} and v_{a+2}, say), inserting one fresh byte with `Σ'.M(d)(v_mid) = a_new ∉ coverage(eᵢ)` (typical case by T9). The K.μ~ atom shifts V-positions `v_{a+2}, v_{a+3}` forward by the insertion width `w` via the bijection `π` (identity on `{v_a, v_{a+1}}`, plus `w` on `{v_{a+2}, v_{a+3}}`). The K.μ⁺ atom adds the new V-position `v_mid` mapping to `a_new ∉ coverage`. By LP-EXT-COMP:

  `proj(eᵢ, d, Σ') = π(proj(eᵢ, d, Σ)) ∪ {v_new : Σ'.M(d)(v_new) ∈ coverage(eᵢ)}`
                   `= π({v_a, v_{a+1}, v_{a+2}, v_{a+3}}) ∪ ∅`
                   `= {v_a, v_{a+1}, v_{a+2} + w, v_{a+3} + w}`

The four V-positions remain but now form *two* contiguous clusters separated by the inserted V-position: `{v_a, v_{a+1}}` and `{v_{a+2} + w, v_{a+3} + w}`. The link's endpoint now appears at two non-contiguous V-positions in `d`. The link object, its coverage, and its projection cardinality are all preserved; only the cluster structure has split.

This is the projection-cluster-fragmentation case: a single contiguous V-run is split into two by a mid-range insertion of non-coverage content. From the link holder's perspective, the link's endpoint *fragments* its visual presentation in `d` — the same content is now displayed in two non-adjacent V-runs. The fragmentation cannot decrease the projection cardinality (LP-EXT-COMP is monotone in `π`, which is a bijection) but it can change the cluster count from 1 to 2 (and a sequence of mid-range insertions can fragment the cluster further).

Gregory's implementation evidence confirms: at mid-coverage INSERT, the implementation produces *two* projection clusters (the spanning crum is split at the insertion point; both halves remain in the POOM and both project independently); the projection set has the same cardinality but two cluster connected components.

**Insertion adjacent to an existing endset.** Suppose `proj(Σ.L(ℓ).eᵢ, d, Σ) = {v}` and a K.μ⁺ transition introduces a new V-position `v'` adjacent to `v` with `Σ'.M(d)(v') = a_new`. Whether the projection grows depends on a property of the endset's spans:

  `proj(Σ.L(ℓ).eᵢ, d, Σ') = proj(Σ.L(ℓ).eᵢ, d, Σ) ∪ ({v'} if a_new ∈ coverage(Σ.L(ℓ).eᵢ) else ∅)`

For an endset specified at link creation against then-existing content, K.α allocates fresh I-addresses strictly greater than any prior I-address within the allocator's domain (T9 ForwardAllocation, ASN-0034). If `coverage(Σ.L(ℓ).eᵢ)` is bounded above by the maximum I-address that the relevant allocator had produced at link-creation time, then `a_new ∉ coverage` and the projection is unchanged — the link did not expand to include the inserted content. This is the typical case Nelson describes: inserted content has a different I-address and is not referenced by the endset.

The general statement is more delicate. The link itself never changes; the projection in `d` includes the new V-position iff `a_new ∈ coverage`. There is no rule that "extends" coverage on insertion; the endset's spans are fixed at creation. Whether `a_new` happens to fall within coverage is a mathematical property of the spans, not a structural guarantee of the link.

**Cross-version visibility.** A version `v` of `d` arises by K.δ (with `k = 1`) creating a new document address, followed by K.μ⁺ transitions populating `M(v)`. If `v`'s arrangement transcludes content from `d` that was linked, the coverage I-addresses appear in `ran(M(v))`, and `proj(eᵢ, v, Σ)` is non-empty. The link is discoverable from `v` just as from `d`, with no provenance check (LP-DISC). Subsequent edits to `v` (contraction or rearrangement) displace the projection in `v` per LP-CONTR-PURE/LP-CONTR-COMP/LP-REARR, without affecting the projection in `d`. The link itself remains a single object with a single set of endsets, visible through both versions independently.

A link created against version `n` of a document is visible through version `n+1` to the extent that version `n+1` transcludes the coverage addresses. The link is not *bound* to version `n`; it is bound to coverage I-addresses, which may appear in any version's arrangement.

**Cross-owner editing.** Consider a link owned by user A (link's home document is owned by A) referencing content allocated by user B (in B's document). B's edits affect projections through B's documents but cannot modify the link's value. LP-FRAME guarantees that K.μ⁻ and K.μ~ on B's document do not touch `Σ.L`. A's link's coverage is unchanged by any of B's edits. The projection of A's link in B's document may displace under rearrangement (LP-REARR), shrink under contraction (LP-CONTR-PURE) or contraction-with-shift (LP-CONTR-COMP), or remain stable. The link remains A's property; the rendering in B's document follows B's current arrangement.

A could in principle remove the link from her own document's V-arrangement of the link subspace via K.μ⁻ on subspace `s_L`. This removes the link's V-position in A's home document but does not remove it from `dom(L)` (LP-MON) — link addresses are permanent, and the link's value, coverage, and discoverability are unaffected.

**Reverse-orphaned link.** A link removed from its home document's V-arrangement of the link subspace (via K.μ⁻ on subspace `s_L`) is no longer presented at any V-position in the home document — but it remains in `dom(L)` (LP-MON). Its coverage is unchanged. It remains discoverable from any document whose arrangement maps to any address in its coverage (LP-DISC). This is the "reverse-orphaned" case Gregory describes: the link has no V-position presentation but is fully alive at the projection and discovery layers.

**Split coverage across multiple documents.** If an endset's coverage `{a₁, ..., a_k}` is initially placed in a single document `d` (with `proj` returning `k` V-positions in `d`), and the system evolves so that `d`'s arrangement maps only `{a₁, ..., a_j}` while another document `d'` transcludes `{a_{j+1}, ..., a_k}`, then:

  `proj(e, d, Σ') = j V-positions in d` (the surviving subset)
  `proj(e, d', Σ') = (k − j) V-positions in d'` (the transcluded subset)

Both projections are non-empty (LP-SURV satisfied per document); the link is discoverable from both documents (LP-DISC); and the link itself is unchanged. This is the symmetric form of Nelson's "if a passage is later split across two documents, must both links survive" — for a single link with split coverage, the rendering naturally distributes across both documents, each independently presenting the portion of coverage it holds.

## What the Architecture Forecloses

Several would-be hazards are structurally impossible by virtue of the projection design:

(α) *V-position staleness.* Projections are recomputed from the current arrangement on every query. There is no cache of V-positions in the link to grow stale.

(β) *Cross-document corruption.* A change to `M(d)` cannot affect `proj(e, d', Σ)` for `d' ≠ d`. Projections are independent per document; edits cannot leak across documents at the projection layer.

(γ) *Coverage drift.* The coverage of an endset cannot change once stored. Coverage is a function of the endset; the endset is preserved by LP-IMM; therefore coverage is preserved by LP-COV. There is no mechanism — no operation in the K family — that can rewrite coverage.

(δ) *Link relabeling via editing.* Removing content from `M(d)` cannot alter the link's endsets, slots, or type. The link is reached only via the projection layer; editing affects only the arrangement layer.

(ε) *Lost cross-version links.* A new version's arrangement may inherit I-addresses from its source via transclusion; the link automatically projects through the new version with no special handling. The link's discoverability is determined by coverage intersection, not by document identity.

(ζ) *Forged links via address reuse.* I-addresses are never reused (T8 AllocationPermanence, ASN-0034). A new K.α produces a fresh address; no future allocation can hijack an existing link's coverage by reproducing an address it already references.

(η) *Direction reversal.* Slot ordering is preserved (LP-SLOT). The link's directional semantics — which endset is source, which is target, which is type — cannot be inverted by any state transition.

The link holder's reliance is precisely characterized: durable identity (I-addresses naming content), permanent coverage (the endset preserving the set of named addresses), permanent content (each address forever holding the same bytes), permanent slot structure, and dynamic projection (V-positions computed from current arrangement). What the reader sees in any document at any time is a fresh derivation from durable identity and current arrangement. Nothing more is stored; nothing more is needed.

## Claims Introduced

Twenty-three claims, organized as three foundational definitions, six still-point invariants, two operation-coverage claims, three pure-atom displacement modes, two composed displacement modes, one cross-document independence, two derived guarantees, three non-invariants, and one frame condition.

| Label | Statement | Status |
|-------|-----------|--------|
| `proj` | `proj : (Σ : State) → Endset → (d : Σ.E_doc) → ℘_fin(dom(Σ.M(d)))` (dependent), with `proj(e, d, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e)}`; undefined when `d ∉ Σ.E_doc` | introduced |
| `render` | `render(ℓ, d, Σ) = ⟨proj(Σ.L(ℓ).eᵢ, d, Σ) : i = 1..|Σ.L(ℓ)|⟩` | introduced |
| `footprint` | `footprint(ℓ, i, Σ) = {d ∈ Σ.E_doc : proj(Σ.L(ℓ).eᵢ, d, Σ) ≠ ∅}` | introduced |
| LP-IMM | `(A Σ → Σ', ℓ ∈ dom(Σ.L) :: Σ'.L(ℓ) = Σ.L(ℓ))` | introduced |
| LP-COV | `(A Σ → Σ', ℓ ∈ dom(Σ.L), i :: coverage(Σ'.L(ℓ).eᵢ) = coverage(Σ.L(ℓ).eᵢ))` | introduced |
| LP-CON | `(A Σ → Σ', a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))` — content allocation persistence (statement scoped to allocated coverage; speculative-coverage addresses gain a value only upon their eventual K.α allocation) | introduced |
| LP-MON | `(A Σ → Σ' :: dom(Σ.L) ⊆ dom(Σ'.L))` — link addresses permanent | introduced |
| LP-SLOT | Slot index of each endset is positional and permanent across state transitions | introduced |
| LP-TYPE | `(A Σ → Σ', ℓ ∈ dom(Σ.L) :: Σ'.L(ℓ).type = Σ.L(ℓ).type)` | introduced |
| LP-MAP | Of the seventeen FEBE commands, the eight arrangement-modifying commands (INSERT, APPEND, COPY/VCOPY, DELETEVSPAN, REARRANGE, MAKELINK, CREATENEWDOCUMENT, CREATENEWVERSION) decompose into pure atoms K.α, K.λ, K.δ, K.ρ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~; each atom induces LP-EXT-PURE, LP-CONTR-PURE, LP-REARR, or LP-FRAME on the projection | introduced |
| LP-FRAME-READ | The nine read-only FEBE commands (RETRIEVEV, RETRIEVEDOCVSPAN, RETRIEVEDOCVSPANSET, RETRIEVEENDSETS, FINDLINKSFROMTOTHREE, FINDNUMOFLINKSFROMTOTHREE, FINDNEXTNLINKSFROMTOTHREE, FINDDOCSCONTAINING, SHOWRELATIONOF2VERSIONS) modify no state component; `(A e, d, ℓ :: proj' = proj ∧ Σ'.L(ℓ) = Σ.L(ℓ))` | introduced |
| LP-REARR | Under pure K.μ~ on `d` with bijection `π`: `proj(e, d, Σ') = π(proj(e, d, Σ))` | introduced |
| LP-CONTR-PURE | Under pure K.μ⁻ on `d` with retention `R` and `Σ'.M(d) = Σ.M(d) ↾ R` (no relabeling): `proj(e, d, Σ') = proj(e, d, Σ) ∩ R` | introduced |
| LP-EXT-PURE | Under pure K.μ⁺/K.μ⁺_L on `d` adding mappings at V-positions disjoint from `dom(Σ.M(d))` (no relabeling): `proj(e, d, Σ') = proj(e, d, Σ) ∪ {v_new : Σ'.M(d)(v_new) ∈ coverage(e)}`; in particular `proj' ⊇ proj` | introduced |
| LP-CONTR-COMP | Under composition K.μ~ ∘ K.μ⁻ on `d` (retention `R_ret`, then bijection `π'` relabeling survivors): `proj(e, d, Σ'') = π'(proj(e, d, Σ) ∩ R_ret)` — derived consequence of LP-CONTR-PURE ∘ LP-REARR | introduced |
| LP-EXT-COMP | Under composition K.μ~ ∘ K.μ⁺ on `d` (bijection `π` relabeling pre-existing V-positions, then K.μ⁺ adding new mappings): `proj(e, d, Σ'') = π(proj(e, d, Σ)) ∪ {v_new : Σ''.M(d)(v_new) ∈ coverage(e)}` — derived consequence of LP-REARR ∘ LP-EXT-PURE | introduced |
| LP-CROSS | For any arrangement transition on `d` and any `d' ≠ d`: `proj(e, d', Σ') = proj(e, d', Σ)` | introduced |
| LP-SURV | `proj(e, d, Σ) ≠ ∅  ⟺  ran(Σ.M(d)) ∩ coverage(e) ≠ ∅`; derived from `proj_def` at a single state; lifted across transitions via LP-IMM ⇒ LP-COV ⇒ stability of coverage | introduced |
| LP-DISC | `ℓ` discoverable from `(d, [v_lo, v_hi))` iff some endset's coverage intersects the V-range's images in `M(d)`; the iff holds *by definition* (`discoverable` is defined by the right-hand side); well-formedness audited via LP-COV ∧ LP-MON ∧ LP-SLOT ∧ LP-CROSS ∧ `proj_def` | introduced |
| LP-NOV | V-positions in `proj(Σ.L(ℓ).eᵢ, d, Σ)` are not stable; witness: K.μ⁺ inserting non-coverage content into a non-empty subspace at a position with coverage-mapping V-positions downstream | introduced |
| LP-NOC | `|proj(Σ.L(ℓ).eᵢ, d, Σ)|` is not stable; witnesses: K.μ⁻ with retention dropping a coverage-mapping V-position (shrinkage); K.μ⁺ transcluding a coverage I-address at a new V-position (growth) | introduced |
| LP-NOD | `footprint(ℓ, i, Σ)` is not stable; witnesses: K.μ⁺ on a new document placing a coverage I-address (growth); K.μ⁻ removing the last coverage-mapping V-position in some document (shrinkage) | introduced |
| LP-FRAME | Arrangement transitions (K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~) do not modify `Σ.L`; allocation transitions (K.α, K.λ, K.δ, K.ρ) do not modify any existing `Σ.M(d)` | introduced |

## Open Questions

What order, if any, does `proj` impose on the V-positions it returns — should it be regarded as a set, an ordered set keyed by T1, or a sequence with externally-imposed order?

Under what conditions on a sequence of arrangement transitions is the projection of an endset invariant from start to end — what closed-form characterization of "compensating edits" exists?

What guarantees must hold for two states `Σ` and `Σ'` such that `render(ℓ, d, Σ) = render(ℓ, d, Σ')` for every `ℓ` and `d` — is rendering equivalence determined by something weaker than `Σ.M = Σ'.M`?

What guarantees does the system provide about the correspondence between a document's projection and its version's projection when the version was created by fork — must they coincide on the inherited content, and what discipline on K.μ⁺ during fork enforces this?

Under what conditions can the projection in `d` be empty while the projection in some `d'` is non-empty, and what does this say about the link's effective visibility partition across the document space?

What invariants govern the projection when an endset's coverage spans I-addresses across multiple subspaces — content-subspace addresses and link-subspace addresses both appearing in one endset's spans?

What guarantees does the system provide about projection composition — when one link's endset references the address of a second link, does projecting the second link's endsets through some document yield a meaningful transitive projection of the first?

What abstract characterization of "well-behaved endset specifications" — beyond the ownership-scope, span-precision, and query-precision considerations sketched in LP-CON — distinguishes endsets that intend forward-reference (covering future allocations as designed) from endsets whose forward-reference would be a specification accident?

What guarantees about projection consistency hold across the lifetime of a single FOLLOWLINK-style operation — does the projection observed by a reader reflect a single state, and what mechanism ensures this against concurrent state transitions?

What is the relationship between the projection's cardinality and the cardinality of `coverage(e)` — under what conditions is `|proj(e, d, Σ)| = |coverage(e) ∩ ran(Σ.M(d))|`, and when does S5 sharing inflate `|proj|` beyond this bound?
