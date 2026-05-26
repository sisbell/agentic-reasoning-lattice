# ASN-0091: REARRANGE Operation
*2026-05-26*

We seek a precise account of rearrangement — the operation by which segments of a document's content stream are reordered without altering the content itself. The naive picture — that moving text "creates new positions" and "destroys old ones" — implies catastrophic consequences: every link attached to the moved content would break, every cross-document transclusion would dangle, and the historical record of what was contained where would dissolve. None of these failures may occur. Our task is to derive precisely why, and to identify what does change and what cannot.

Our starting commitment is the separation of two streams. The content store `Σ.C : T ⇀ Val` is permanent and append-only: once an address `a` enters `dom(Σ.C)`, it remains there bound forever to its initial value (foundation invariant C0/S0). The arrangement `Σ.M(d) : T ⇀ T` for each document `d ∈ dom(Σ.M)` is a partial function from V-positions to I-addresses recording how the document currently presents its contents in linear order. The arrangement is mutable; the content store is not. The link store `Σ.L : T ⇀ EndsetSequence` is also append-only and immutable on existing keys (foundation invariant L12). Rearrangement, by its name, can affect only the arrangement — the entire question is what this restriction lets us prove.

## REARRANGE as Vstream-Only Operation

Let us define the class of transitions REARRANGE belongs to. A transition `Σ → Σ'` is *Vstream-only on `d`* when
```
dom(Σ'.M(d)) = dom(Σ.M(d))                                                              (RA-dom)
```
and there exists a bijection
```
π : dom(Σ.M(d)) → dom(Σ.M(d))
```
satisfying
```
(A v : v ∈ dom(Σ.M(d)) : Σ'.M(d)(π(v)) = Σ.M(d)(v))                                    (RA-π)
```
together with the frame conditions
```
Σ'.C = Σ.C  ∧  Σ'.L = Σ.L  ∧  Σ'.E = Σ.E  ∧  Σ'.R = Σ.R                                 (RA-frame)
  ∧  dom(Σ'.M) = dom(Σ.M)
  ∧  (A d' ∈ dom(Σ.M) : d' ≠ d : Σ'.M(d') = Σ.M(d'))
```

The bijection π is the *rearrangement permutation*. RA-dom pins the post-state arrangement's support to the same V-positions; without it, RA-π alone would only entail `dom(Σ'.M(d)) ⊇ dom(Σ.M(d))` (since RA-π asserts each `π(v)` is defined in `Σ'.M(d)`), leaving open the possibility of additional populated V-positions in the post-state. The defining equation RA-π then says that for every V-position `v` populated in `Σ.M(d)`, the same I-address `Σ.M(d)(v)` lives in `Σ'.M(d)` — but at the V-position `π(v)`. The (V, I) pairs are permuted; no pair is created, destroyed, or modified. RA-frame fixes every state component apart from `Σ.M(d)` itself — the content store `C`, link store `L`, entity set `E`, and provenance relation `R` are all preserved, the document registry `dom(M)` is preserved, and the arrangements of every other registered document are preserved. The abstract class is genuinely "Vstream-only on d." The `dom(Σ'.M) = dom(Σ.M)` clause discharges, in particular, the implicit precondition needed for downstream lemmas to evaluate state-relative predicates at Σ' (RE-disc applies LP12 at Σ', which requires `d ∈ dom(Σ'.M)`; RE-trans's home-document clause requires `origin(a) ∈ dom(Σ'.M)`). The bijection π is not in general unique: when `Σ.M(d)` has shared I-addresses (allowed by foundation S5/UnrestrictedSharing — the same I-address at multiple V-positions), any permutation π of `dom(Σ.M(d))` that fixes the partition into pre-images `{π⁻¹(a) := {v : Σ.M(d)(v) = a}}_a` while otherwise permuting freely within each pre-image satisfies RA-π. Every RE-* claim derived from RA-π below is parameterised by the specific π witnessing the transition; RE-proj in particular states `project(e, d, Σ') = π(project(e, d, Σ))` for whichever π witnesses Σ → Σ', not for an arbitrary bijection.

The abstract class admits the degenerate identity case π = id, in which RA-π collapses to `Σ'.M(d)(v) = Σ.M(d)(v)` and RA-frame forces `Σ' = Σ`. Every claim derived below holds uniformly across the identity and non-identity cases — under π = id all RE-* claims reduce to identities of Σ with itself. REARRANGE_K excludes this degenerate case via ASN-0084's K.μ~ admissibility clause (ii) alone (`π ≠ id`); the existence precondition `|dom_C(M(d))| ≥ 2` plays an independent role — it is what ensures that non-identity permutations on `V_S(d)` exist at all (a singleton domain admits only the identity as a self-bijection) — but it does not by itself exclude `π = id` on a domain of size ≥ 2 (the identity exists on every non-empty set). The two conditions together make REARRANGE_K realize a strictly non-trivial subset of the abstract class: clause (ii) excludes the identity, and `|dom_C(M(d))| ≥ 2` ensures the non-identity alternative is non-empty.

REARRANGE_K (the cut-sequence operation of ASN-0084) realizes this class. ASN-0084's R-PPERM and R-SPERM construct π explicitly for 3-cut pivot and 4-cut swap respectively. ASN-0047's K.μ~-FIX (DomainFixity) discharges RA-dom: `dom(Σ'.M(d)) = dom(Σ.M(d))` follows from π's bijectivity together with ASN-0047's D-SEQ★ at both endpoints (per-subspace V-position enumeration matches across the transition). REARRANGE_K is the concrete realization of ASN-0047's K.μ~ operation, whose frame supplies RA-frame in full. K.μ~'s ASN-0047 frame reads `C' = C; E' = E; R' = R; L' = L; (A d' : d' ≠ d : M'(d') = M(d'))`, which matches each RA-frame conjunct exactly — notably `L' = L` (the source of the link-store invariance derived below, RE-L), `E' = E`, and `R' = R` (the source of RE-R). ASN-0084's R-FRAME-P/S, by contrast, supply only the within-document, within-subspace clauses at the cut-sequence level (clause (a): non-S V-positions preserved; clause (b): other documents' arrangements preserved; clause (c): `C' = C`); link-store, entity-set, and provenance preservation enter the picture through K.μ~ at the ASN-0047 layer, not through R-FRAME-P/S. The cut sequence further restricts the bijection — π acts as identity on V-positions outside the affected range `[c₀, c_{n−1})` and on V-positions in subspaces other than the cut subspace S. Most of the abstract claims below are derivable from RA-dom, RA-π, and RA-frame alone, independent of how π was generated; the exception is RE-sub (subspace frame), which requires the cut-subspace restriction supplied by ASN-0084's R-FRAME-P/S(a) and is therefore REARRANGE_K-specific.

The cut subspace is fixed at S = s_C by ASN-0084's CS3, so REARRANGE_K rearranges the content subspace alone. We will examine the consequences for the link subspace as a separate frame property below.

## What the Content Store Sees: Nothing

The first consequence of RA-frame is immediate. **Content-Store Invariance**:
```
Σ'.C = Σ.C                                                                              (RE-C)
```
No content is allocated, freed, or modified by rearrangement. Every I-address in `dom(Σ.C)` retains its bound value; no new I-address enters `dom(Σ.C)`; the function `Σ.C` is literally unchanged. This is the architectural reason rearrangement cannot disturb content identity: the layer where identity lives is untouched.

The same observation applies symmetrically to the link store via RA-frame. We will exploit this when reasoning about links below.

## Domain Stability and Range Invariance

RA-dom asserts `dom(Σ'.M(d)) = dom(Σ.M(d))` directly. Every V-position that was populated in d remains populated; every V-position that was unpopulated remains unpopulated. (For REARRANGE_K specifically, this equality is not axiomatic but lemma-derived — ASN-0047's K.μ~-FIX establishes it from π's bijectivity together with ASN-0047's D-SEQ★.)

**Domain Stability**:
```
dom(Σ'.M(d)) = dom(Σ.M(d))                                                              (RE-dom)
```

This distinguishes rearrangement from contraction (which removes V-positions) and from extension (which adds them). Rearrangement is the unique transition class that touches the arrangement's *structure* without changing its *support*.

The bijection further makes the range — viewed as a set or as a multiset — a permutation of itself. Compute:
```
ran(Σ'.M(d)) = {Σ'.M(d)(v') : v' ∈ dom(Σ'.M(d))}
             = {Σ'.M(d)(π(v)) : v ∈ dom(Σ.M(d))}        [π bijects dom onto itself]
             = {Σ.M(d)(v) : v ∈ dom(Σ.M(d))}             [RA-π]
             = ran(Σ.M(d))
```

**Range Invariance**:
```
ran(Σ'.M(d)) = ran(Σ.M(d))                                                              (RE-ran)
```

Lifting to multisets: for each I-address `a`, define `μ_a(M) = |{v : v ∈ dom(M) ∧ M(v) = a}|`. By injectivity of π on a finite set (dom(M(d)) is finite by S8-fin):
```
μ_a(Σ'.M(d)) = |{v' : v' ∈ dom(Σ'.M(d)) ∧ Σ'.M(d)(v') = a}|
             = |{π(v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|       [substitute v' = π(v)]
             = |{v : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}|           [π injective]
             = μ_a(Σ.M(d))
```

**Per-Address Multiplicity Invariance**:
```
(A a ∈ T :: μ_a(Σ'.M(d)) = μ_a(Σ.M(d)))                                                (RE-μ)
```

Together, RE-ran and RE-μ are the formal content of Nelson's "the document afterward contains exactly the same set of content as before — no additions, no losses, no duplications." Range invariance says the set is identical. Multiplicity invariance says each I-address appears the same number of times. The arrangement is a permutation, not a transformation.

## Where Position Lives After Rearrangement

Every (V, I) pair in the pre-state has an image (V, I) pair in the post-state: the pre-state pair `(v, M(d)(v))` corresponds to the post-state pair `(π(v), M(d)(v))`. The I-address is the same; the V-position has moved. This is the precise sense in which "every byte retains its identity": the byte associated with I-address `M(d)(v)` is still in d, now at V-position `π(v)`.

Conversely, for each post-state V-position `v'`, the pre-image `π⁻¹(v')` is the V-position that previously held the I-address now at `v'`. The map π⁻¹ recovers, for each post-state V-position, the V-position it migrated from.

What changed is not which I-addresses are in d, nor which V-positions are populated, but which V-position holds which I-address. The bijection π is the entire content of the rearrangement.

## Links Persist; Their Coverage Cannot Move

The link store is fixed by RA-frame:
```
dom(Σ'.L) = dom(Σ.L)  ∧  (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a))                          (RE-L)
```

Every link persists across rearrangement with its full endset sequence intact. No link is added, removed, or modified.

Coverage of an endset is a function of the endset's span representation alone — it consults no state component beyond the endset itself (per the definition in ASN-0098). Since the endset is preserved verbatim, its coverage is preserved:
```
(A a ∈ dom(Σ.L), i : 1 ≤ i ≤ |Σ.L(a)| :: coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ))   (RE-cov)
```

This is the formal precipitate of Nelson's "links between bytes can survive rearrangements." A link's reference structure is keyed to I-addresses (via spans on the I-address space). The I-addresses are unchanged. So the reference structure is unchanged.

## Discoverability Is Preserved

A link is *discoverable from* document `d` at state `Σ` when some endset's coverage intersects the document's I-address range — when there exists a slot `i` with `coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅` (the characterisation supplied by foundation lemma LP12 of ASN-0098). Combining RE-cov and RE-ran:
```
discoverable_from(a, d, Σ')
  ⟺ (E i :: coverage(Σ'.L(a).eᵢ) ∩ ran(Σ'.M(d)) ≠ ∅)
  ⟺ (E i :: coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅)
  ⟺ discoverable_from(a, d, Σ)
```

**Discoverability Invariance**:
```
(A a ∈ dom(Σ.L), d ∈ dom(Σ.M) :: discoverable_from(a, d, Σ') ⟺ discoverable_from(a, d, Σ))    (RE-disc)
```

The set of links that can be found from d is exactly the same before and after rearrangement. This is the strong sense of link survivability: not merely that links persist as objects, but that their *relationships* to documents — the answer to "is this link reachable from here?" — are unchanged.

## Projection Transports Along π

Where a link's coverage strikes the arrangement is the set `project(e, d, Σ) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(e)}`. The bijection π carries this set faithfully to the post-state. For each `v ∈ project(e, d, Σ)`, the V-position `π(v)` holds the same I-address (RA-π), and that address remains in coverage (RE-cov), so `π(v) ∈ project(e, d, Σ')`. For the reverse inclusion, take any `v' ∈ project(e, d, Σ')` and set `v := π⁻¹(v')`, which exists because π is a bijection (the inverse is licensed by bijectivity alone, independent of any cardinality assumption on the domain). Then `v ∈ dom(Σ.M(d))` (RA-dom carries π's domain to dom(Σ.M(d))), and `Σ.M(d)(v) = Σ'.M(d)(π(v)) = Σ'.M(d)(v') ∈ coverage(e)` by RA-π together with RE-cov, so `v ∈ project(e, d, Σ)` and `v' = π(v) ∈ π(project(e, d, Σ))`. Therefore
```
project(e, d, Σ') = π(project(e, d, Σ))                                                 (RE-proj)
```

A reader who follows the link arrives at the same I-address it always identified — but its V-position in d's current arrangement may have changed. This is Nelson's "arrive at the same content, regardless of its new position": the link follows content identity, not arrangement.

## Run Decomposition Is Not Invariant

Up to now every property has been preserved. The bijection's effect lies elsewhere: the *structure* of the (V, I) mapping — the way contiguous V-intervals correspond to contiguous I-intervals — can change.

A maximal run in `M(d)` is a triple `(v, a, n)` with `M(d)(v + k) = a + k` for `0 ≤ k < n`, maximal in the sense that it cannot be extended at either end. The canonical maximal-run decomposition is unique (per the foundation's bundle algebra in ASN-0058). Its cardinality measures how "structured" the arrangement is — fewer runs means longer contiguous mappings.

Rearrangement can fragment runs. Take a maximal run `(v, a, n)` with `n ≥ 2` in `Σ.M(d)`, and suppose π displaces position `v` to a location not adjacent to π(v + 1). Then the post-state arrangement no longer has a contiguous V-interval mapping to the I-interval `[a, a + n)`. The single pre-state run resolves into multiple post-state runs.

> **Fragmentation Possibility.** There exist rearrangements `Σ → Σ'` such that the cardinality of the canonical maximal-run decomposition of `Σ'.M(d)` is strictly greater than that of `Σ.M(d)`. (RE-frag)

**Direct witness (fragmentation).** Take pre-state `Σ.M(d)` with V-positions `[1, 1], [1, 2], [1, 3]` mapping to a single maximal run `([1, 1], a, 3)` — that is, `Σ.M(d)([1, k]) = a + (k − 1)` for `k ∈ {1, 2, 3}`. Pre-state run cardinality: 1.

Apply REARRANGE_K with cut sequence `(c₀, c₁, c₂) = ([1, 1], [1, 2], [1, 4])`, a 3-cut pivot with `w_α = ord(c₁) − ord(c₀) = 1` and `w_β = ord(c₂) − ord(c₁) = 2`. R-PRE(iv) is discharged because every depth-2 position `v` with `[1, 1] ≤ v < [1, 4]` — namely `[1, 1], [1, 2], [1, 3]` — lies in `V_S(d)`. By ASN-0084's R-P1 (`Σ'.M(d)(c₀ + j) = Σ.M(d)(c₁ + j)` for `0 ≤ j < w_β`): `Σ'.M(d)([1, 1]) = Σ.M(d)([1, 2]) = a + 1` and `Σ'.M(d)([1, 2]) = Σ.M(d)([1, 3]) = a + 2`. By R-P2 (`Σ'.M(d)(c₀ + w_β + j) = Σ.M(d)(c₀ + j)` for `0 ≤ j < w_α`): `Σ'.M(d)([1, 3]) = Σ.M(d)([1, 1]) = a`.

Post-state arrangement: `[1, 1] ↦ a + 1`, `[1, 2] ↦ a + 2`, `[1, 3] ↦ a`. The maximal runs of `Σ'.M(d)` are `([1, 1], a + 1, 2)` (since `(a + 1) + 1 = a + 2 = Σ'.M(d)([1, 2])`, but `(a + 2) + 1 ≠ a = Σ'.M(d)([1, 3])`) and `([1, 3], a, 1)` (no extension possible). Post-state run cardinality: 2 — strictly greater than the pre-state cardinality 1.

A consequence for endset projection: if a pre-state contiguous V-interval `[v, v + n)` is in `project(e, d, Σ)`, the post-state image `π([v, v + n))` may consist of multiple disjoint V-intervals. The set is preserved (RE-proj), but its geometry — its decomposition into contiguous V-runs — is not. This is the formal account of Nelson's "the endset becomes a discontiguous set of bytes" when a linked span is split.

**Reverse witness (coalescence).** Take pre-state `Σ.M(d)` with V-positions `[1, 1] ↦ a + 1`, `[1, 2] ↦ c`, `[1, 3] ↦ a`, where `a + 1` and `a` are consecutive content addresses (both produced by the same sub-allocator chain) but `c` is unrelated to either. The pre-state maximal runs are `([1, 1], a + 1, 1)`, `([1, 2], c, 1)`, `([1, 3], a, 1)` — three singletons, since `(a + 1) + 1 = a + 2 ≠ c` and `c + 1 ≠ a`. Pre-state run cardinality: 3.

Apply REARRANGE_K with cut sequence `([1, 1], [1, 3], [1, 4])`, a 3-cut pivot with `w_α = 2` and `w_β = 1`. R-PRE(iv) is discharged as above. By R-P1 (`0 ≤ j < 1`): `Σ'.M(d)([1, 1]) = Σ.M(d)([1, 3]) = a`. By R-P2 (`0 ≤ j < 2`): `Σ'.M(d)([1, 2]) = Σ.M(d)([1, 1]) = a + 1` and `Σ'.M(d)([1, 3]) = Σ.M(d)([1, 2]) = c`.

Post-state arrangement: `[1, 1] ↦ a`, `[1, 2] ↦ a + 1`, `[1, 3] ↦ c`. The maximal runs are `([1, 1], a, 2)` (since `a + 1 = Σ'.M(d)([1, 2])`) and `([1, 3], c, 1)`. Post-state run cardinality: 2 — strictly less than the pre-state cardinality 3.

Run-decomposition cardinality is neither monotone nor invariant under rearrangement — it tracks the *visible structure* of the arrangement, which is exactly what rearrangement reshapes.

## Cross-Document Independence

Among d's siblings, nothing happens. RA-frame guarantees `Σ'.M(d') = Σ.M(d')` for every `d' ≠ d`:
```
(A d' ∈ dom(Σ.M) : d' ≠ d :: Σ'.M(d') = Σ.M(d'))                                       (RE-other)
```

This is the formal precipitate of Nelson's "REARRANGE is document-scoped — the cuts are V-addresses within the target document." Rearrangement cannot move content between documents, cannot deplete or extend any other document's arrangement, and cannot affect any projection evaluated against any other document. The operation's scope is fully named by the document parameter `d`.

## Cross-Document Transclusion Preserved

When `a ∈ ran(Σ.M(d))` with `origin(a) ≠ d`, the I-address `a` is foreign content displayed in d — a transclusion from d's perspective. The transclusion relationship has three components: (a) `a` is in d's arrangement; (b) `a`'s home document `origin(a)` is present and undisturbed; (c) the origin function — which document allocated `a` — is unchanged.

By RE-ran, the *set* of foreign addresses `{a ∈ ran(Σ.M(d)) : origin(a) ≠ d}` is preserved; by RE-μ, each such address appears in d's arrangement with the same multiplicity at Σ' as at Σ — so the multiset of foreign addresses is preserved. By RE-other applied to `d' = origin(a)`, the source arrangement is unchanged. By RE-C, the address `a` remains in `dom(Σ'.C)` with its original value. Origin itself is a function of the address (per S7 of ASN-0036) — not of state — so it is invariant unconditionally.

> **Transclusion Preservation.** For every transclusion relationship at Σ — every pair (a, d) with `a ∈ ran(Σ.M(d))` and `origin(a) ≠ d` — the same relationship holds at Σ', with the same multiplicity, and the home document `origin(a)`'s arrangement is unchanged. (RE-trans)

Even when REARRANGE fragments d's view of the transcluded span (RE-frag), each piece independently carries its foreign origin. Splitting at a cut point does not turn one transclusion into two distinct relationships; it produces two contiguous V-intervals that *jointly* refer to the same span at the source. The transcluding document still finds its borrowed content; the home document is undisturbed; and the function answering "where did this byte come from?" is invariant.

## Subspace Frame (REARRANGE_K-specific)

RE-sub is the one consequence in this ASN that does not flow from the abstract class alone. The abstract bijection RA-π acts on `dom(Σ.M(d))` without constraint and could, in principle, move V-positions across subspaces; only the cut-sequence structure pins π down to the cut subspace S.

ASN-0084's R-FRAME-P/S(a) restricts the cut sequence's effect to the content subspace S = s_C. V-positions in any other subspace are untouched:
```
(A v : v ∈ dom(Σ.M(d)) ∧ subspace(v) ≠ S :: Σ'.M(d)(v) = Σ.M(d)(v))                     (RE-sub)
```

When the cut subspace is the content subspace, the link subspace is wholly preserved — both its set of populated V-positions and its V→I mapping. Rearrangement of content does not perturb the link arrangement.

This is structurally necessary. If REARRANGE could carry content-subspace V-positions into link-subspace V-positions or vice versa, the typed referential integrity invariant (foundation S3★: content-subspace V-positions map to `dom(C)`, link-subspace V-positions map to `dom(L)`) would be violable by rearrangement. The subspace restriction is what makes typed referential integrity stable under arrangement permutations — and that restriction is supplied at the cut-sequence layer, not at the abstract Vstream-only layer.

## Origin and Provenance Invariance

The function `origin(a) = N(a).0.U(a).0.D(a)` (S7 of ASN-0036) projects an I-address to the document-level prefix encoding its allocator. Origin consults only the address `a`. It is a structural projection on T, independent of any state component. Therefore origin is invariant across every state transition, including REARRANGE:
```
(A a ∈ T :: origin(a) at Σ' = origin(a) at Σ)                                           (RE-origin)
```

(More precisely: origin is a function on tumblers, not state, so it has no temporal dimension at all. RE-origin records the fact that REARRANGE consumes no degree of freedom that origin depends on.)

The provenance relation `Σ.R ⊆ T × E_doc` records which documents have, at some point in their history, contained which I-addresses. RA-frame includes `Σ'.R = Σ.R` directly, so:
```
Σ'.R = Σ.R                                                                              (RE-R)
```

The historical record is intact across rearrangement. The bytes that have ever lived in d are exactly the bytes that live in d after the rearrangement (since REARRANGE adds and removes nothing — RE-ran), and the records of their past containments in other documents are unchanged. For REARRANGE_K specifically, the same conclusion is independently supplied by ASN-0047's J3 (Reordering Isolation), which places R in K.μ~'s frame — confirming that K.μ~ realizes the abstract class's R-preservation property.

## What Rearrangement Is Not

We collect the negations. Rearrangement does not:

- modify the content store (RE-C);
- modify the link store (RE-L);
- change which V-positions are populated (RE-dom);
- change the multiset of I-addresses in d (RE-ran, RE-μ);
- change link coverage (RE-cov);
- change link discoverability from any document (RE-disc);
- change the set of V-positions where any link projects onto d (RE-proj transports a set along π, preserving its cardinality and content-identity);
- modify any other document's arrangement (RE-other);
- modify V-positions in subspaces other than the cut subspace (RE-sub);
- change origin of any I-address (RE-origin);
- modify the provenance relation (RE-R).

What rearrangement does is exactly one thing: it permutes which V-positions hold which I-addresses, via a bijection π that exhausts d's V-stream domain. Everything else follows — including the cost (run-decomposition cardinality can grow under fragmentation) and the guarantees (link survivability, transclusion preservation, content permanence).

## Worked Example

We trace a small concrete state through a single REARRANGE_K invocation and verify each RE-* claim at the level of actual values.

*Setup.* Fix documents `d = [1, 0, 1, 0, 1]` and `d' = [1, 0, 1, 0, 2]`, both T4-valid with `zeros(·) = 2`. By the sub-allocator chain discipline (ASN-0093), let `b₁ := [d.0.1.1] = [1, 0, 1, 0, 1, 0, 1, 1]` be the first emission of `A_C(d)`, and let `a₁ := [d'.0.1.1] = [1, 0, 1, 0, 2, 0, 1, 1]` and `a₂ := inc(a₁, 0) = [1, 0, 1, 0, 2, 0, 1, 2]` be the first two emissions of `A_C(d')`, so `a₂ = a₁ + 1` within the chain. Let `a_link := [d.0.2.1]` be the first emission of `A_L(d)`.

*Pre-state.* `Σ.C` contains `b₁, a₁, a₂` (and possibly more); `Σ.L` contains `a_link` with endset sequence `(e₁, e₂, e₃)`, where `e₁ = ⟨(b₁, δ(1, 8))⟩` is a canonical single-span endset with `coverage(e₁) = {t ∈ T : b₁ ≤ t < b₁ ⊕ δ(1, 8)}` (the tumbler interval under T1), and `e₃` is the non-empty type endset. Note that the interval contains many tumblers that are not I-addresses (e.g., longer tumblers extending `b₁` at lower hierarchical levels lie between `b₁` and `b₁ ⊕ δ(1, 8)` by T1 case (ii) and case (i)); what we need below is the intersection of `coverage(e₁)` with the address stores. By LP-Fin Corollary (ASN-0098), `coverage(e₁) ∩ (dom(Σ.C) ∪ dom(Σ.L)) = {b₁}` — the single first emission of `A_C(d)` is the only F-candidate the canonical span admits in the interval. In particular this intersection is disjoint from `{a₁, a₂}` (since `a₁, a₂` agree with `b₁` only on positions 1–4 and diverge at position 5, placing them outside the interval). `Σ.M(d)` populates both subspaces at their respective common depths — the content subspace at depth 2 with three positions, and the link subspace at depth 2 with one populated V-position pointing at the link in `dom(Σ.L)`:
```
Σ.M(d) = { [1, 1] ↦ a₁,    [1, 2] ↦ a₂,    [1, 3] ↦ b₁,    [2, 1] ↦ a_link }
```
The link-subspace entry `[2, 1] ↦ a_link` is well-typed under S3★: a link-subspace V-position whose image lies in `dom(Σ.L)`. `Σ.M(d')` populates its own content subspace (concrete details immaterial here), and `Σ.M(d''')` for any other `d''' ∈ dom(Σ.M)` is whatever it is.

*Operation.* Apply REARRANGE_K to `d` with cut sequence `(c₀, c₁, c₂) = ([1, 1], [1, 2], [1, 4])`, a 3-cut pivot with cut subspace S = s_C, `w_α = 1`, `w_β = 2`. The permutation π (R-PPERM, ASN-0084) acts on content-subspace V-positions as `π([1, 1]) = c₀ + w_β = [1, 3]` (α-region: c₀ + j ↦ c₀ + w_β + j), `π([1, 2]) = c₀ = [1, 1]` (β-region: c₁ + j ↦ c₀ + j with j = 0), `π([1, 3]) = c₀ + 1 = [1, 2]` (β-region with j = 1); on non-S V-positions π acts as identity (R-PPERM, non-S branch), so `π([2, 1]) = [2, 1]`.

*Post-state.* By R-P1 and R-P2 for content-subspace positions, and R-FRAME-P(a) for the link-subspace position:
```
Σ'.M(d) = { [1, 1] ↦ a₂,    [1, 2] ↦ b₁,    [1, 3] ↦ a₁,    [2, 1] ↦ a_link }
```

*Verification.* For each derived claim, we exhibit the concrete witness:

- **RE-C.** `Σ'.C = Σ.C` by RA-frame (no content allocation, no content modification).
- **RE-L.** `dom(Σ'.L) = dom(Σ.L) = {a_link}` and `Σ'.L(a_link) = Σ.L(a_link) = (e₁, e₂, e₃)` by RA-frame.
- **RE-dom.** `dom(Σ'.M(d)) = {[1, 1], [1, 2], [1, 3], [2, 1]} = dom(Σ.M(d))` by direct inspection.
- **RE-ran.** `ran(Σ'.M(d)) = {a₂, b₁, a₁, a_link} = {a₁, a₂, b₁, a_link} = ran(Σ.M(d))` as sets.
- **RE-μ.** `μ_{a₁}(Σ.M(d)) = μ_{a₂}(Σ.M(d)) = μ_{b₁}(Σ.M(d)) = μ_{a_link}(Σ.M(d)) = 1`, and identically for `Σ'.M(d)`; multiplicities of all other I-addresses are zero in both.
- **RE-cov.** `coverage(Σ'.L(a_link).eᵢ) = coverage(Σ.L(a_link).eᵢ)` for `i ∈ {1, 2, 3}`, since the endset sequence itself is preserved (RE-L) and coverage depends only on the endset.
- **RE-disc.** `coverage(e₁) ∩ ran(Σ.M(d)) ⊇ {b₁} ≠ ∅`, so `discoverable_from(a_link, d, Σ)` holds (LP12, ASN-0098). The same intersection `coverage(e₁) ∩ ran(Σ'.M(d)) ⊇ {b₁} ≠ ∅` holds at the post-state, so `discoverable_from(a_link, d, Σ')` holds too. The biconditional is satisfied.
- **RE-proj.** `project(e₁, d, Σ) = {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ coverage(e₁)} = {[1, 3]}` (only `b₁`'s V-position; `[2, 1] ↦ a_link` is excluded since `a_link ∉ coverage(e₁)` — `a_link = [d.0.2.1]` agrees with `b₁ = [d.0.1.1]` on positions 1–6 but has component `2` at position 7 while `b₁` has component `1`, so by T1 case (i) at position 7 `b₁ < a_link` and `b₁ ⊕ δ(1, 8) < a_link`, placing `a_link` strictly above the interval). `project(e₁, d, Σ') = {[1, 2]}` (where `b₁` lives now). The image `π({[1, 3]}) = {[1, 2]}` matches.
- **RE-frag.** Pre-state runs on the content subspace: `([1, 1], a₁, 2)` (since `a₂ = a₁ + 1`) and `([1, 3], b₁, 1)` — cardinality 2. Post-state runs on the content subspace: `([1, 1], a₂, 1)`, `([1, 2], b₁, 1)`, `([1, 3], a₁, 1)` — cardinality 3, since no two consecutive post-state I-addresses extend each other (`a₂ + 1 ≠ b₁`; `b₁ + 1 ≠ a₁`). The link-subspace run `([2, 1], a_link, 1)` is shared between both states. The content-subspace cardinality strictly increased — a fragmentation witness arising from a transclusion-bearing arrangement.
- **RE-other.** `Σ'.M(d') = Σ.M(d')` by RA-frame; the foreign document's arrangement is untouched.
- **RE-trans.** Both `a₁` and `a₂` have `origin(·) = d' ≠ d`, so each is a transclusion in `d`. `{a₁, a₂} ⊆ ran(Σ.M(d))` and `{a₁, a₂} ⊆ ran(Σ'.M(d))`. `origin(a₁) = origin(a₂) = d'` is unchanged (RE-origin). `Σ'.M(d') = Σ.M(d')` by RE-other.
- **RE-sub.** The link-subspace position `[2, 1] ∈ dom(Σ.M(d))` has `subspace([2, 1]) = 2 ≠ s_C = S`. By RE-sub, `Σ'.M(d)([2, 1]) = Σ.M(d)([2, 1]) = a_link`, matching the post-state arrangement exhibited above. The cut-subspace restriction is exercised concretely: REARRANGE_K's content-subspace cuts leave the link-subspace entry verbatim, despite the bijection π acting non-trivially on content-subspace V-positions.
- **RE-origin.** `origin(a₁) = origin(a₂) = d'` (extracted from positions 1–5 of `a₁` and `a₂`); `origin(b₁) = d` (extracted from positions 1–5 of `b₁`). Origin is a structural projection on the address; it does not depend on state and is unchanged.
- **RE-R.** `Σ'.R = Σ.R` by RA-frame directly; equivalently, by ASN-0047's J3 (Reordering Isolation) through K.μ~'s frame.

Every derived claim holds at the concrete level; no two derived claims conflict at any point of the trace.

## Composition Across Multi-Step REARRANGE Sequences

Each RE-* claim is stated as a single-step property of `Σ → Σ'`. Write `Σ →_R Σ'` to denote a single REARRANGE step — a transition satisfying RA-dom, RA-π, and RA-frame for some document `d` (equivalently, an abstract Vstream-only transition; REARRANGE_K is one realisation). For a finite sequence of REARRANGE-only transitions `Σ₀ →_R Σ₁ →_R ⋯ →_R Σ_n`, the single-step claims compose by trivial induction. Equalities chain transitively, yielding the multi-step (★) forms:

- **RE-C★, RE-L★, RE-dom★, RE-ran★, RE-other★, RE-sub★, RE-R★:** equalities `X(Σ₀) = X(Σ_n)` follow by chaining `X(Σᵢ) = X(Σᵢ₊₁)` across the n steps.
- **RE-μ★:** `μ_a(Σ_n.M(d)) = μ_a(Σ₀.M(d))` for every I-address `a` and every document `d`.
- **RE-cov★:** `coverage(Σ_n.L(a).eᵢ) = coverage(Σ₀.L(a).eᵢ)` for every link `a` and slot `i`.
- **RE-disc★:** `discoverable_from(a, d, Σ_n) ⟺ discoverable_from(a, d, Σ₀)` for every link `a` and document `d` — biconditionals compose.
- **RE-proj★:** `project(e, d, Σ_n) = (π̂_n ∘ ⋯ ∘ π̂_1)(project(e, d, Σ_0))`, where for each step `Σ_{i−1} →_R Σ_i` targeting document `dᵢ` with rearrangement permutation `π_i` on `dom(Σ_{i−1}.M(dᵢ))`, `π̂_i := π_i` when `dᵢ = d` and `π̂_i := id_{dom(Σ_{i−1}.M(d))}` otherwise (in which case RE-other applied at step i gives `Σ_i.M(d) = Σ_{i−1}.M(d)`, so the identity is well-typed and the projection is unchanged). For sequences in which every step targets the same document `d`, `π̂_i = π_i` throughout, and the formula reduces to `project(e, d, Σ_n) = (π_n ∘ ⋯ ∘ π_1)(project(e, d, Σ_0))`.
- **RE-frag★:** no per-step monotonicity is available — each step in the sequence may independently increase or decrease run-decomposition cardinality, as the single-step fragmentation and coalescence witnesses above demonstrate. The claim is the negation of any uniform per-step direction; we do not assert anything stronger about the net cardinality change `|runs(Σ_n.M(d))| − |runs(Σ₀.M(d))|` across the full sequence.
- **RE-trans★:** the single-step RE-trans makes three assertions: (i) the (a, d) transclusion relationship persists across the step; (ii) the multiplicity at d is preserved; (iii) `origin(a)`'s arrangement is unchanged by the step. The multi-step ★ form straightforwardly composes (i) and (ii) — at every intermediate state `Σᵢ`, the transclusion `(a, d)` from `Σ₀` is present with the same multiplicity, and chaining n single-step instances yields the same conclusion at `Σ_n`. Conclusion (iii), however, does *not* compose unconditionally: if some intermediate step `Σⱼ →_R Σⱼ₊₁` targets `origin(a)`, then that step reorders `origin(a)`'s arrangement, so the home-document arrangement at `Σ_n` need not equal the one at `Σ₀`. The multi-step claim therefore restricts (iii) to sequences where no step targets `origin(a)`: under that restriction, `Σ_n.M(origin(a)) = Σ₀.M(origin(a))` follows by chaining RE-other across each step (each step targets some `dᵢ ≠ origin(a)`, so RE-other applies). When at least one step targets `origin(a)`, the unrestricted ★ form delivers only (i) + (ii) for the transclusion at d — the home-document arrangement may have undergone its own permutation in the interim, though the transclusion relationship at d remains intact because each rearrangement at `origin(a)` itself preserves `origin(a)`'s range (RE-ran applied at the step targeting `origin(a)`), so `a` remains in `ran(Σⱼ.M(origin(a)))` for every j.
- **RE-origin★:** origin is state-independent, so trivially invariant across any sequence.

For mixed sequences that interleave REARRANGE with other transitions (K.α, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.δ, K.σ, K.ρ), the per-operation lemmas of foundation ASN-0098 govern each non-REARRANGE step. The REARRANGE steps in such a mixed sequence are themselves governed by ASN-0098's LP-Comp (case-analysis over K.μ~) at the projection layer, with the abstract RE-* claims of this ASN delivering the full collection of consequences at each REARRANGE step. The closure properties above apply only to pure REARRANGE sub-sequences; properties tied to coverage or arrangement state (RE-cov, RE-disc, RE-proj) require care across mixed sequences, since intervening K.α/K.λ/K.μ⁻/K.μ⁺ steps can shift coverage relationships even though they leave individual endsets verbatim (LP3, ASN-0098).

## Claims Introduced

The *Provenance* column records which premises a claim depends on: **abstract** = derivable from RA-dom, RA-π, and RA-frame alone (the abstract Vstream-only class); **REARRANGE_K** = requires the cut-sequence specifics supplied by ASN-0084's R-FRAME-P/S; **structural** = state-independent (holds without reference to any state transition).

| Label | Statement | Provenance | Status |
|-------|-----------|-----------|--------|
| RA-dom | Rearrangement domain stability: dom(Σ'.M(d)) = dom(Σ.M(d)) | abstract (definition) | introduced |
| RA-π | Rearrangement equation: π : dom(M(d)) → dom(M(d)) is a bijection with M'(d)(π(v)) = M(d)(v) for every v ∈ dom(M(d)) | abstract (definition) | introduced |
| RA-frame | Rearrangement frame: Σ'.C = Σ.C, Σ'.L = Σ.L, Σ'.E = Σ.E, Σ'.R = Σ.R, dom(Σ'.M) = dom(Σ.M), and Σ'.M(d') = Σ.M(d') for every d' ∈ dom(Σ.M) with d' ≠ d | abstract (definition) | introduced |
| RE-C | Content-store invariance: Σ'.C = Σ.C under REARRANGE | abstract (from RA-frame) | introduced |
| RE-dom | Domain stability: dom(Σ'.M(d)) = dom(Σ.M(d)) | abstract (from RA-dom) | introduced |
| RE-ran | Range invariance: ran(Σ'.M(d)) = ran(Σ.M(d)) | abstract (from RA-π) | introduced |
| RE-μ | Per-address multiplicity invariance: μ_a(Σ'.M(d)) = μ_a(Σ.M(d)) for every I-address a | abstract (from RA-π) | introduced |
| RE-L | Link store invariance: dom(Σ'.L) = dom(Σ.L) and Σ'.L(a) = Σ.L(a) for every a ∈ dom(Σ.L) | abstract (from RA-frame) | introduced |
| RE-cov | Coverage invariance: coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ) for every link a and slot i | abstract (from RE-L) | introduced |
| RE-disc | Discoverability invariance: discoverable_from(a, d, Σ') ⟺ discoverable_from(a, d, Σ) for every link a and document d | abstract (from RE-cov + RE-ran via LP12) | introduced |
| RE-proj | Projection transport: project(e, d, Σ') = π(project(e, d, Σ)) for every endset e | abstract (from RA-π + RE-cov) | introduced |
| RE-frag | Fragmentation possibility: there exist REARRANGE instances where the maximal-run-decomposition cardinality of M(d) strictly increases | abstract (existential; witnesses are REARRANGE_K) | introduced |
| RE-other | Other-document invariance: Σ'.M(d') = Σ.M(d') for every d' ≠ d | abstract (from RA-frame) | introduced |
| RE-trans | Transclusion preservation: for every (a, d) with a ∈ ran(Σ.M(d)) and origin(a) ≠ d, the transclusion relationship and its multiplicity persist at Σ', and origin(a)'s arrangement is unchanged | abstract (from RE-ran + RE-μ + RE-other + RE-C + RE-origin) | introduced |
| RE-sub | Subspace frame: for every v ∈ dom(M(d)) with subspace(v) ≠ S, Σ'.M(d)(v) = Σ.M(d)(v) | REARRANGE_K (from R-FRAME-P/S(a)) | introduced |
| RE-origin | Origin invariance: origin(a) is unchanged across REARRANGE for every a | structural (state-independent) | introduced |
| RE-R | Provenance invariance: Σ'.R = Σ.R under REARRANGE | abstract (from RA-frame; equivalently, J3 for REARRANGE_K) | introduced |

## Open Questions

What guarantees must rearrangement preserve about cross-document transclusion when a cut splits a span transcluded from the same source document into two non-contiguous pieces?
What semantics, if any, should rearrangement carry on the link subspace, and what invariants would such an operation be required to preserve?
Under what conditions are two distinct rearrangement transitions observationally equivalent at the level of link discoverability rather than at the level of arrangement equality?
What upper bound, if any, can be placed on the increase in maximal-run-decomposition cardinality from a single rearrangement invocation?
Can every bijection of dom(M(d)) that preserves the arrangement well-formedness invariants be realized by a finite composition of cut-sequence rearrangements?
