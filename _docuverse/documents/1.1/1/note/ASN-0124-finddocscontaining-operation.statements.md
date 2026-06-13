# ASN-0124 Claim Statements

*Source: ASN-0124-finddocscontaining-operation.md (revised 2026-06-12) — Extracted: 2026-06-12*

## Definition — ContentImage

**FD-IMGC (ContentImage).** *For `d ∈ dom(Σ.M)` and `W ⊆ T`:*

> `image_C(W, d, Σ) ≡ {Σ.M(d)(v) : v ∈ W ∩ dom(Σ.M(d)) ∧ subspace(v) = s_C}`,

*undefined for `d ∉ dom(Σ.M)`; and the restriction is exactly intersection with the content store:*

> `image_C(W, d, Σ) = image(W, d, Σ) ∩ dom(Σ.C)`.

---

## Definition — ContentRange

**FD-RAN (ContentRange).** *For `d ∈ dom(Σ.M)`:*

> `ran_C(d, Σ) ≡ image_C(T, d, Σ) = {Σ.M(d)(v) : v ∈ V_{s_C}(d)}`,

*and the alignment with the foundation's containment relation is definitional: `a ∈ ran_C(d, Σ) ⟺ (a, d) ∈ Contains_C(Σ)` — unfolding both sides yields the same existential over content-subspace positions (with `d ∈ E_doc = dom(Σ.M)` supplied by the comprehension's guard). `ran_C(d, Σ)` is finite (`dom(Σ.M(d))` is finite, S8-fin) and `ran_C(d, Σ) ⊆ dom(Σ.C)` (FD-IMGC at `W = T`).*

---

## Definition — VSpecSet

**FD-Q (VSpecSet).** *A vspec-set at Σ is a finite set `Q = {(d₁, W₁), …, (d_p, W_p)}` of pairs with each `d_j ∈ dom(Σ.M)` and each `W_j ⊆ T` a V-region. The pairs may name the same document more than once, and may name different documents — the queried material may span the docuverse.*

---

## Definition — Resolution

**FD-RES (Resolution).** *The resolution of a vspec-set is the union of its content images:*

> `resolve(Q, Σ) ≡ (∪ (d, W) : (d, W) ∈ Q : image_C(W, d, Σ))`.

*Postconditions: (a) groundedness — `resolve(Q, Σ) ⊆ dom(Σ.C)` (FD-IMGC); the resolution phase cannot inject an unallocated or link-store address into the query, whatever region the asker names. (b) finiteness — a finite union of finite sets (S8-fin). (c) flattening — the pair structure of `Q` is discarded: the value is a bare I-address set, and nothing downstream can recover which named region contributed which address.*

---

## FD-ASKER — AskerIndependence (LEMMA, lemma)

**FD-ASKER (AskerIndependence).** *Vspec-sets with equal resolutions get equal answers: `resolve(Q₁, Σ) = resolve(Q₂, Σ) ⟹ finddocs_V(Q₁, Σ) = finddocs_V(Q₂, Σ)` (immediate once FD-V below is seen to be a function of the resolved set). In particular, naming material through a transcluder and naming it through its origin are the same query: if `Σ.M(d_t)(v) = a = Σ.M(d_o)(u)` with `subspace(v) = subspace(u) = s_C`, then `resolve({(d_t, {v})}, Σ) = {a} = resolve({(d_o, {u})}, Σ)`. The asker's starting document is consumed entirely at resolution; the search itself never sees it.*

---

## Definition — ContainmentComprehension

**FD-FIND (ContainmentComprehension).** *For any `I ⊆ T` and state Σ:*

> `finddocs(I, Σ) ≡ {d ∈ dom(Σ.M) : ran_C(d, Σ) ∩ I ≠ ∅}`.

*Degenerate cases: `finddocs(∅, Σ) = ∅` (no intersection can be non-empty); a freshly registered document (`dom(Σ.M(d)) = ∅`, the K.δ Document post-state) has `ran_C(d, Σ) = ∅` and is never a member.*

---

## Definition — TheOperation

**FD-V (TheOperation).** *FINDDOCSCONTAINING is the two-phase composite:*

> `finddocs_V(Q, Σ) ≡ finddocs(resolve(Q, Σ), Σ)`,

*defined whenever every document named in `Q` is registered. By FD-RES(b) and L-fin-style finiteness of the stratum — `dom(Σ.M)` is finite at every reachable state, since `E` grows by one entity per K.δ from the finite `E₀` — the result is a finite set of bare document identities: the codomain is `𝒫(E_doc)`, each member a T4-valid document tumbler (`zeros = 2`, M0). Nothing else is returned: no pairing with the matched material, no positions within the member, no multiplicity. Membership is idempotent — a document matching through a hundred positions and a document matching through one are the same kind of member.*

---

## FD-COMPLETE — DocuverseCompleteness (INV, predicate)

**FD-COMPLETE (DocuverseCompleteness).** *`(A d : d ∈ dom(Σ.M) ∧ ran_C(d, Σ) ∩ I ≠ ∅ : d ∈ finddocs(I, Σ))` — no document anywhere whose current arrangement meets the material may be omitted. The quantifier ranges over the entire document stratum `dom(Σ.M) = E_doc` at Σ — every version of every document under every node and account (each version is its own document entity); nodes (`zeros = 0`) and accounts (`zeros = 1`) are themselves entities but not documents, so they lie outside the range and can never be returned (matching FD-V's codomain `𝒫(E_doc)`). The signature `finddocs(I, Σ)` admits no locality, authorship, or asker parameter, so no sub-docuverse restriction is even expressible — completeness is global by construction, relative to the one unified state.*

---

## FD-SOUND — PresentWitnessSoundness (INV, predicate)

**FD-SOUND (PresentWitnessSoundness).** *`(A d : d ∈ finddocs(I, Σ) : (E v, a :: v ∈ dom(Σ.M(d)) ∧ subspace(v) = s_C ∧ Σ.M(d)(v) = a ∧ a ∈ I))` — every member carries a present witness pair `(v, a)`: a live position currently mapped onto queried material. No document is admitted on the basis of content it once held and has since contracted away, on value resemblance, or on provenance records.*

---

## FD-GROUND — GhostAddressInertness (LEMMA, lemma)

**FD-GROUND (GhostAddressInertness).** *`finddocs(I, Σ) = finddocs(I ∩ dom(Σ.C), Σ)`.*

*Derivation. `ran_C(d, Σ) ⊆ dom(Σ.C)` (FD-RAN), so `ran_C(d, Σ) ∩ I = ran_C(d, Σ) ∩ (I ∩ dom(Σ.C))` for every `d`; the membership predicate is unchanged. Addresses never allocated, and link-store addresses, contribute nothing — a query cannot be poisoned by naming them. (When the I-argument arrives through FD-RES this is moot — resolution is grounded — but the primitive is total over `𝒫(T)` and safe there.)*

---

## FD-PART — AnyPortionSufficiency (LEMMA, lemma)

**FD-PART (AnyPortionSufficiency).** *A single shared address suffices and is all that is ever required: for `a ∈ I` and `d ∈ dom(Σ.M)`, `a ∈ ran_C(d, Σ) ⟹ d ∈ finddocs(I, Σ)`; and membership never demands coverage — no clause of FD-FIND requires `I ⊆ ran_C(d, Σ)`, so a document arranging exactly one address of a thousand-address query is as much a member as one arranging them all.*

*Derivation. The first half is the comprehension read at the witness `a`. For the second half it suffices that the predicate is an intersection-non-emptiness test, which is monotone in evidence: one witness closes it.*

---

## FD-UDIST — UnionDistributivity (LEMMA, lemma)

**FD-UDIST (UnionDistributivity).** *For all `I₁, I₂ ⊆ T` — no disjointness required:*

> `finddocs(I₁ ∪ I₂, Σ) = finddocs(I₁, Σ) ∪ finddocs(I₂, Σ)`.

*Derivation. `ran_C(d, Σ) ∩ (I₁ ∪ I₂) = (ran_C(d, Σ) ∩ I₁) ∪ (ran_C(d, Σ) ∩ I₂)`, and a union is non-empty iff a part is; set-builder over the disjunction splits the comprehension. With FD-RES this gives the per-region decomposition of the operation itself: `finddocs_V(Q, Σ) = (∪ (d, W) ∈ Q : finddocs(image_C(W, d, Σ), Σ))`.*

---

## FD-IMONO — MonotonicityInMaterial (LEMMA, lemma)

**FD-IMONO (MonotonicityInMaterial — corollary).** *`I' ⊆ I ⟹ finddocs(I', Σ) ⊆ finddocs(I, Σ)`, by FD-UDIST at `I = I' ∪ (I ∖ I')`.*

---

## FD-LOCAL — PerDocumentLocality (LEMMA, lemma)

**FD-LOCAL (PerDocumentLocality).** *Write `χ(d, I, Σ) ≡ ran_C(d, Σ) ∩ I ≠ ∅` for the membership criterion. χ is a function of `I` and `Σ.M(d)` alone: unfolding FD-RAN, it is built from `dom(Σ.M(d))`, the tumbler projection `subspace(·)`, the values `Σ.M(d)(·)`, and `I` — no other document's arrangement, no `Σ.C` value, no `Σ.L`, no `Σ.R`, no allocation history occurs in it. Two corollaries: (i)* cross-document independence *— any transition with `Σ'.M(d) = Σ.M(d)` leaves `d`'s membership unchanged, in both directions; (ii)* non-impedance *— enlarging the docuverse (new documents, new content, new links, new provenance — all framing `d`'s arrangement, hence inert by (i)) can never remove `d`.*

---

## FD-SELF — SelfInclusion (LEMMA, lemma)

**FD-SELF (SelfInclusion).** *Every naming document with a non-trivial region is a member of its own query's answer: for `(d, W) ∈ Q` with `image_C(W, d, Σ) ≠ ∅`, `d ∈ finddocs_V(Q, Σ)`. For the single-region query the statement is a biconditional, and self-membership is equivalent to the answer being non-empty at all:*

> `d ∈ finddocs_V({(d, W)}, Σ) ⟺ image_C(W, d, Σ) ≠ ∅`, *and* `image_C(W, d, Σ) = ∅ ⟹ finddocs_V({(d, W)}, Σ) = ∅`.

*Derivation. Take `a ∈ image_C(W, d, Σ)`, witnessed by position `v`. Then `a ∈ resolve(Q, Σ)` (FD-RES), and the same `v` witnesses `a ∈ ran_C(d, Σ)` since `image_C(W, d, Σ) ⊆ image_C(T, d, Σ) = ran_C(d, Σ)` — sub-regions image into the full range. So `χ(d, resolve(Q, Σ), Σ)` holds and `d` is a member (FD-PART). For the biconditional's other direction: if the image is empty, the singleton query's resolution is empty and `finddocs(∅, Σ) = ∅` (FD-FIND) — nobody is a member, `d` included.*

---

## FD-NEUT — OriginNeutrality (LEMMA, lemma)

**FD-NEUT (OriginNeutrality).** *(a) — frame observation — the membership criterion χ contains no occurrence of `origin(·)`, of `Σ.R`, or of any allocation-event datum: the document that allocated a queried address is tested by exactly the same predicate as every other document. (b) Consequently the origin appears precisely when it qualifies: for `a ∈ I`, `origin(a) ∈ finddocs(I, Σ)` iff `origin(a) ∈ dom(Σ.M)` and `ran_C(origin(a), Σ) ∩ I ≠ ∅` — in particular, whenever the origin still arranges `a` itself. (c) And the origin can fail to qualify: there are reachable states in which `origin(a) ∉ finddocs({a}, Σ)` while transcluders of `a` are members.*

*Construction for (c). Take any reachable Σ₀′ with two registered documents `d₁, d₂` (K.δ scaffolding per ASN-0047). Run the valid insertion composite on `d₁` — K.α allocating fresh `a` on `d₁`'s content chain `A_C(d₁)` (so `origin(a) = d₁`, ASN-0093/S7), K.μ⁺ arranging `v ↦ a`, K.ρ recording `(a, d₁)` (J0, J1★ discharged) — then the transclusion composite into `d₂` — K.μ⁺ arranging `u ↦ a` (precondition `a ∈ dom(C)` holds), K.ρ recording `(a, d₂)` (J1★) — then the contraction K.μ⁻ on `d₁` retaining nothing of its content subspace (`n'_{s_C} = 0`; valid and self-sufficient, J2). At the resulting boundary: `a ∈ dom(C)` still (P0 — the contraction's frame is `C' = C`; the material itself cannot be destroyed), `ran_C(d₁) ∌ a`, `ran_C(d₂) ∋ a`, so `finddocs({a}) = {d₂}`.*

---

## FD-IDENT — AddressIdentityKeying (LEMMA, lemma)

**FD-IDENT (AddressIdentityKeying).** *(a)* Value-blindness. *`finddocs` is a function of `(I, Σ.M)`: by FD-LOCAL aggregated over `d`, no stored value `Σ.C(·)` is ever read — the definition of `image_C` filters by subspace, not by consulting `C`, and the criterion compares addresses, never bytes. Two states agreeing on `M` give identical answers for every `I`, whatever their content stores hold. (b)* Coincidence exclusion. *Independently created material is unrelated however its values compare: if `a₁ ≠ a₂` with `Σ.C(a₁) = Σ.C(a₂)` — distinct allocation events necessarily yield distinct addresses regardless of value, S4 (ASN-0036) — then a document arranging only `a₂` satisfies `ran_C(d, Σ) ∩ {a₁} = ∅` and is excluded from `finddocs({a₁}, Σ)`. (c)* Provenance kinship is not sufficient. *Sharing an origin does not match: for `a' = inc(a, 0)` a sibling emission on the same content chain (`origin(a') = origin(a)`, `a' ≠ a` by ChainEnumerationInjectivity, ASN-0093), a document arranging only `a'` is excluded from `finddocs({a}, Σ)`.*

---

## FD-CHAIN — FlatChainReach (LEMMA, lemma)

**FD-CHAIN (FlatChainReach).** *Fix `a ∈ dom(Σ.C)`. (a)* Propagation. *A transclusion composite from `d_i` to `d_{i+1}` whose copied region's content image contains `a` — the new mappings of the K.μ⁺ on `d_{i+1}` include some `u ↦ a`, the address read off `d_i`'s arrangement by FD-IMGC — yields `a ∈ ran_C(d_{i+1}, ·)` at its boundary. Since the image read from `d_i` consists of the very addresses `d_i` arranges, the address arriving in `d_{i+1}` is* the same `a` *that arrived in `d_i` — depth of copying never mints a new identity. (b)* Flat evaluation. *At any state Σ, `finddocs({a}, Σ) = {d ∈ dom(Σ.M) : a ∈ ran_C(d, Σ)}` collects the entire current sharing set of `a` in one comprehension: the criterion mentions no path, no copy event, no `Σ.R`, no other document (FD-LOCAL) — so a chain `d₀ → d₁ → ⋯ → d_n` of transclusion composites, each propagating `a`, leaves all of `d₀, …, d_n` simultaneous members, found without any iterative chain-following, and so found for every `I ∋ a` (FD-IMONO). (c)* Severance immunity. *Membership of the chain's ends does not depend on its middle: if `d_mid` later contracts `a` away, every other document's membership is untouched (FD-LOCAL(i)), so the ends remain co-listed without the middle.*

---

## FD-VERS — ForkMembershipDuplication (LEMMA, lemma)

**FD-VERS (ForkMembershipDuplication).** *Let `Σ →* Σ'` be a J4 fork composite (ASN-0047) with content source operand `d_op` and fresh version `d_new`. Then for every `I`:*

> `finddocs(I, Σ') = finddocs(I, Σ) ∪ ({d_new} if d_op ∈ finddocs(I, Σ) else ∅)`,

*and in particular `d_new ∈ finddocs(I, Σ') ⟺ d_op ∈ finddocs(I, Σ')`.*

*Derivation. J4's derived consequence gives `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)})`, and the transcription map φ lands in `V_{s_C}(d_new)`, so `ran_C(d_new, Σ') = ran_C(d_op, Σ)`. The fork's steps frame every existing arrangement — `d_op`'s included — so `ran_C(d, Σ') = ran_C(d, Σ)` for all prior `d`, and every prior membership is unchanged (FD-LOCAL); the only candidate change is the fresh `d_new`, whose criterion evaluates to `d_op`'s.*

---

## FD-COOC — CooccurrenceByComposition (LEMMA, lemma)

**FD-COOC (CooccurrenceByComposition).** *For fragments `I₁, …, I_k` (each, say, a fragment's resolution), define a document's incidence `inc(d) = {j : ran_C(d, Σ) ∩ I_j ≠ ∅}`. Then: the union query yields the documents touching* any *fragment, `finddocs(∪_j I_j, Σ) = {d : inc(d) ≠ ∅}` (FD-UDIST); the intersection of the per-fragment queries yields the* recombiners *— the documents drawing together all the scattered pieces — `∩_j finddocs(I_j, Σ) = {d : inc(d) = {1, …, k}}`; and full containment at address grain is the finest such composition: for `I ≠ ∅`, `{d : I ⊆ ran_C(d, Σ)} = ∩_{a ∈ I} finddocs({a}, Σ)`. The guard is the one boundary the identity needs: at `I = ∅` the left side is all of `dom(Σ.M)` — every document vacuously contains all of nothing — while an intersection over an empty index set is undefined until a universe is declared; read within the universe `dom(Σ.M)`, the empty intersection is `dom(Σ.M)` and the identity extends to `I = ∅` as well.*

---

## FD-LOSSY — MergedResultUnderdetermination (LEMMA, lemma)

**FD-LOSSY (MergedResultUnderdetermination).** *The single merged answer under-determines the incidence pattern: there are reachable states `Σ¹, Σ²` and fragments `I₁, I₂` with `finddocs(I₁ ∪ I₂, Σ¹) = finddocs(I₁ ∪ I₂, Σ²)` but different incidences.*

*Construction. Register a single document `d` (K.δ scaffolding per ASN-0047; `dom(M) = {d}` at every state below). Let `a₁ = [d.0.s_C.1]` and `a₂ = inc(a₁, 0)` be the first two emissions of `d`'s content chain `A_C(d)` (FirstEmission; distinct by ChainEnumerationInjectivity, ASN-0093), and fix the fragments `I₁ = {a₁}`, `I₂ = {a₂}`. For `Σ¹`, run one valid insertion composite on `d`: K.α allocating `a₁`, K.μ⁺ arranging `[1,1] ↦ a₁`, K.ρ recording `(a₁, d)`. At this boundary `ran_C(d, Σ¹) = {a₁}`, and `a₂ ∉ dom(Σ¹.C)`: so `finddocs(I₁ ∪ I₂, Σ¹) = {d}` and `inc(d) = {1}` at `Σ¹`. For `Σ²`, continue with: K.α allocating `a₂`, K.μ⁻ on `d` at `n'_{s_C} = 0`, K.μ⁺ arranging `[1,1] ↦ a₂`, K.ρ recording `(a₂, d)`. At this boundary `ran_C(d, Σ²) = {a₂}`, so `finddocs(I₁ ∪ I₂, Σ²) = {d}` and `inc(d) = {2}` at `Σ²`. The two answers are equal as sets — `{d} = {d}` — while the incidence is `{1}` at `Σ¹` and `{2}` at `Σ²`.*

---

## FD-CONVEX — SingleSpanConvexityForcing (LEMMA, lemma)

**FD-CONVEX (SingleSpanConvexityForcing).** *A single contiguous V-span cannot name scattered fragments exactly. Let `σ` be a V-span over `d`'s content positions (T12) with `u, q ∈ ⟦σ⟧ ∩ V_{s_C}(d)`, `u < q`. Then every intervening content position is dragged in: for `v ∈ V_{s_C}(d)` with `u < v < q` — and every same-depth position strictly between two members of `V_{s_C}(d)` is itself a member, by the canonical gap-free form D-SEQ★ — span denotations are order-convex (T12(c)), so `v ∈ ⟦σ⟧`, whence `Σ.M(d)(v) ∈ image_C(⟦σ⟧, d, Σ) ⊆ resolve`. By FD-PART, every document sharing* only the connective material *is admitted. The two-region vspec-set `{(d, W₁), (d, W₂)}` with `u ∈ W₁`, `q ∈ W₂`, `v ∉ W₁ ∪ W₂` resolves to `image_C(W₁, d, Σ) ∪ image_C(W₂, d, Σ)` — exactly the fragments' material — and excludes the connective-only documents whenever the connective image is disjoint from the fragment images (guaranteed when `Σ.M(d)` is injective on the span).*

---

## FD-FRAME — NonArrangementInertness (LEMMA, lemma)

**FD-FRAME (NonArrangementInertness).** *Every transition that fixes the content-subspace arrangement family fixes the answer: for every `I`,* K.α, K.λ, K.ρ *(arrangement frames `M' = M`),* K.δ *(Node/Account cases frame `M`; the Document case adds `d_new` with `M'(d_new) = ∅`, never a member, others framed), and* K.μ⁺_L *(adds only `s_L`-positions to one document, so `V_{s_C}(d)` and its images are unchanged) all satisfy `finddocs(I, Σ') = finddocs(I, Σ)`. Derivation: in each case `χ(d, I, ·)` is unchanged for every `d` (FD-LOCAL), and the comprehension's domain either is unchanged or gains only non-members.*

---

## FD-STEP — ArrangementStepCharacterization (LEMMA, lemma)

**FD-STEP (ArrangementStepCharacterization).** *The only movers are the content-subspace arrangement transitions, and each moves the answer in exactly one place:*

- *K.μ⁺ on `d` (content extension, new images `N = {Σ'.M(d)(v) : v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d))}`): `ran_C(d, Σ') = ran_C(d, Σ) ∪ N` (extension frame: prior positions agree, new positions are content-subspace by the amended precondition), all other documents framed, so*

  > `finddocs(I, Σ') = finddocs(I, Σ) ∪ ({d} if N ∩ I ≠ ∅ else ∅)`

- *K.μ⁻ on `d` (contraction with retention set `Ret`): writing `ran_Ret ≡ {Σ.M(d)(v) : v ∈ Ret ∧ subspace(v) = s_C}` — a pre-state quantity — the retained-domain agreement gives `ran_C(d, Σ') = ran_Ret ⊆ ran_C(d, Σ)`, others framed, so*

  > `finddocs(I, Σ') = (finddocs(I, Σ) ∖ {d}) ∪ ({d} if ran_Ret ∩ I ≠ ∅ else ∅)`

- *K.μ~ on `d` (reorder with witnessing bijection π): the domain is fixed (K.μ~-FIX), π is subspace-preserving, and the bijection equation `Σ'.M(d)(π(v)) = Σ.M(d)(v)` makes the content images a reindexed copy: `ran_C(d, Σ') = ran_C(d, Σ)`, so*

  > `finddocs(I, Σ') = finddocs(I, Σ)`

---

## FD-CWP — ContractionSurvivalWP (LEMMA, lemma)

**FD-CWP (ContractionSurvivalWP).** *Fix a K.μ⁻ on `d` with retention set `Ret` (per-subspace initial segments, ASN-0047; `Ret ⊆ dom(Σ.M(d))` by D-SEQ★). The weakest precondition on the pre-state under which the edited document survives in the answer is its own enabling condition plus a retained witness:*

> `wp(K.μ⁻[d, Ret], d ∈ finddocs(I, ·)) ≡ enabled(K.μ⁻[d, Ret]) ∧ (E v : v ∈ Ret ∧ subspace(v) = s_C : Σ.M(d)(v) ∈ I)`,

*the existential being exactly `ran_Ret ∩ I ≠ ∅`, a function of `(Σ, Ret)` evaluable before the step. The whole answer is preserved iff survival is owed only where it was held: `finddocs(I, Σ') = finddocs(I, Σ) ⟺ (d ∈ finddocs(I, Σ) ⟹ ran_Ret ∩ I ≠ ∅)` — contraction can never create membership (FD-STEP), so the edited document is the only contingency. Boundary case `Ret = ∅` (full clearance): the existential is false, so the document drops iff it was a member.*

---

## FD-FRESH — InsertionInvariance (LEMMA, lemma)

**FD-FRESH (InsertionInvariance).** *The in-vocabulary insertion composite on `d` at position `p` of an `N`-position content segment, with `n ≥ 1` fresh units, is:* K.α *iterated `n` times, allocating fresh `A_new = {a'₁, …, a'ₙ}` along `d`'s content chain `A_C(d)`; the full content clear* K.μ⁻ *on `d` at `n'_{s_C} = 0`, link subspace retained (omitted when `V_{s_C}(d) = ∅` — the first-insertion case); one rebuild* K.μ⁺ *re-populating the canonical segment of length `N + n` — position `k` takes `d`'s old `k`-th image for `1 ≤ k < p`, takes `a'_{k−p+1}` for `p ≤ k < p + n`, and takes `d`'s old `(k − n)`-th image for `p + n ≤ k ≤ N + n`; and* K.ρ *recording `(a', d)` for each `a' ∈ A_new`. The net effect, initial-to-final, is ASN-0082's gap-shift contract realized: positions `≥ p` re-mapped at `shift(v, n)` carrying their old images (I3), the left region's mappings unchanged (I3-L), the vacated gap holding `A_new`, the post-domain exactly the canonical segment (I3-V, I3-CS). Then for every `I` fixed at the pre-state with `I ⊆ dom(Σ.C)`:*

> `finddocs(I, Σ_post) = finddocs(I, Σ_pre)`.

*Derivation, step by step from FD-FRAME and FD-STEP. The K.α steps: FD-FRAME — no motion. The clear: FD-STEP's contraction clause at `ran_Ret = ∅` (no content position retained) — `d` drops iff it was a member, every other document framed (FD-LOCAL). The rebuild: FD-STEP's growth clause with new-image set `N_step = ran_C(d, Σ_pre) ∪ A_new`; K.α's freshness gives `A_new ∩ dom(Σ_pre.C) = ∅ ⊇ A_new ∩ I`, so `N_step ∩ I ≠ ∅ ⟺ ran_C(d, Σ_pre) ∩ I ≠ ∅` — `d` re-enters exactly iff it dropped. The K.ρ steps: FD-FRAME. Net: identity.*

---

## FD-NONMONO — LiveNonMonotonicity (LEMMA, lemma)

**FD-NONMONO (LiveNonMonotonicity).** *Across `Σ →* Σ'` neither inclusion holds in general: the transclusion step grows the answer (FD-STEP, K.μ⁺ with `N ∩ I ≠ ∅` — realized in the FD-CHAIN propagation), and the contraction step shrinks it (FD-CWP's failing branch — realized in the FD-NEUT(c) construction). For the two-phase operation there is one further motion: the* resolution *itself is present-tense — editing a* named *document moves `resolve(Q, ·)` even while every containment fact is fixed (D-PRES, ASN-0127). The motion enters through the pointing, not through the containing.*

---

## FD-VDYN — TwoPhasePerTransitionDynamics (LEMMA, lemma)

**FD-VDYN (TwoPhasePerTransitionDynamics).** *Fix a vspec-set `Q` with every named document registered at Σ — so `finddocs_V(Q, ·)` is defined at both ends of any transition, `dom(M)` being monotone (M1) — call `d` named when `(d, W) ∈ Q` for some `W`, and across a transition `Σ → Σ'` write `I = resolve(Q, Σ)`, `I' = resolve(Q, Σ')`. FD-IMGC's defining comprehension consults only `W` and the content-subspace restriction of `Σ.M(d)`, so the resolution moves only when some named document's content-subspace arrangement moves. Four cases exhaust the vocabulary.*

*(a) No named content motion — K.α, K.λ, K.ρ, K.δ anywhere; K.μ⁺_L anywhere (it adds only `s_L`-positions, which `image_C` filters out); K.μ⁺, K.μ⁻, K.μ~ on unnamed documents. Then `I' = I` and the two-phase answer moves exactly as the fixed-`I` answer moves, `finddocs_V(Q, Σ') = finddocs(I, Σ')`, governed by FD-FRAME and FD-STEP.*

*(b) Extension of a named document — K.μ⁺ on named `d_q`: monotone growth,*

> `finddocs_V(Q, Σ) ⊆ finddocs_V(Q, Σ')`.

*Derivation. `image_C(W, d_q, Σ) ⊆ image_C(W, d_q, Σ')` for every `W` — F-IMG-MONO (ASN-0127) restricted through FD-IMGC — and every other named arrangement is framed, so `I ⊆ I'`. Then `finddocs(I, Σ) ⊆ finddocs(I, Σ')` by FD-STEP's growth clause, and `finddocs(I, Σ') ⊆ finddocs(I', Σ')` by FD-IMONO.*

*(c) Contraction of a named document — K.μ⁻ on named `d_q`: monotone shrinkage,*

> `finddocs_V(Q, Σ') ⊆ finddocs_V(Q, Σ)`.

*Derivation. `image_C(W, d_q, Σ') ⊆ image_C(W, d_q, Σ)` — F-IMG-CONTR through FD-IMGC — others framed, so `I' ⊆ I`. Then `finddocs(I', Σ') ⊆ finddocs(I, Σ')` by FD-IMONO, and `finddocs(I, Σ') ⊆ finddocs(I, Σ)` by FD-STEP's shrinkage clause.*

*(d) Reorder of a named document — K.μ~ on named `d_q` with witnessing bijection π: the genuinely two-phase case. Every fixed-`I` answer is invariant (FD-STEP, reorder clause), so all motion is resolution motion:*

> `finddocs_V(Q, Σ') = finddocs(I', Σ') = finddocs(I', Σ)`, *with* `image_C(W, d_q, Σ') = image_C(π⁻¹(W), d_q, Σ)`

*— the second equality by FD-STEP at the fixed set `I'`; the swing law from domain fixity (K.μ~-FIX), subspace preservation, and the bijection equation `Σ'.M(d_q)(π(v)) = Σ.M(d_q)(v)`, i.e. F-IMG-SWING restricted through FD-IMGC. Stability condition: if π fixes every named region setwise on the content positions — `π⁻¹(W) ∩ V_{s_C}(d_q) = W ∩ V_{s_C}(d_q)` for each `(d_q, W) ∈ Q` — then `I' = I` and the answer is unchanged.*

---

## Definition — ProvenanceQuery

**FD-HIST (ProvenanceQuery).** *`finddocs_R(I, Σ) ≡ {d ∈ dom(Σ.M) : (E a : a ∈ I : (a, d) ∈ Σ.R)}`.*

---

## FD-RMONO — HistoricalMonotonicity (LEMMA, lemma)

**FD-RMONO (HistoricalMonotonicity).** *Across `Σ →* Σ'`: `finddocs_R(I, Σ) ⊆ finddocs_R(I, Σ')`. Derivation: `R ⊆ R'` per transition (P2), `dom(M) ⊆ dom(M')` (M1), both lifted over the finite decomposition of `→*` (SequentialTransitionAxiom); the criterion reads only these monotone components.*

---

## FD-SUPER — LiveBoundedByHistorical (LEMMA, lemma)

**FD-SUPER (LiveBoundedByHistorical).** *At every composite boundary Σ: `finddocs(I, Σ) ⊆ finddocs_R(I, Σ)`. Derivation: a member's present witness (FD-SOUND) is a pair `(a, d) ∈ Contains_C(Σ)` with `a ∈ I` (FD-RAN alignment), and P4★ places it in `Σ.R`.*

---

## FD-WITNESS — EverContainedEqualsOnceLive (LEMMA, lemma)

**FD-WITNESS (EverContainedEqualsOnceLive).** *For every valid trace `Σ₀ →* Σ₁ →* ⋯ →* Σ_n = Σ` (each `Σ_k` a composite boundary):*

> `finddocs_R(I, Σ) = (∪ k : 0 ≤ k ≤ n : finddocs(I, Σ_k))`.

*Derivation. (⊆) For `d ∈ finddocs_R(I, Σ)` take `a ∈ I` with `(a, d) ∈ Σ.R`; P4a yields a trace state `Σ_k` and a position `v ∈ dom(M_k(d))` with `subspace(v) = s_C ∧ M_k(d)(v) = a` — that is, `a ∈ ran_C(d, Σ_k)`, so `d ∈ finddocs({a}, Σ_k) ⊆ finddocs(I, Σ_k)` (FD-IMONO). (⊇) For `d ∈ finddocs(I, Σ_k)`, its witness pair lies in `Contains_C(Σ_k) ⊆ Σ_k.R` (P4★ at the boundary `Σ_k`) `⊆ Σ.R` (P2 along the suffix), and `d ∈ dom(Σ.M)` by M1.*

---

## Definition — GhostCharacterization

**FD-GHOST (GhostCharacterization).** *Define `ghosts(I, Σ) ≡ finddocs_R(I, Σ) ∖ finddocs(I, Σ)`. By FD-WITNESS (the `k = n` term contributing nothing to the difference): `ghosts(I, Σ) = (∪ k : 0 ≤ k < n : finddocs(I, Σ_k)) ∖ finddocs(I, Σ)` — exactly the documents that contained queried material at some past boundary and contain none of it now.*

---

## FD-COINC — CoincidenceOnNonShrinkingHistories (LEMMA, lemma)

**FD-COINC (CoincidenceOnNonShrinkingHistories).** *Call a valid trace* range-non-decreasing *when every composite preserves or grows every content range: `(A k, d : 0 ≤ k < n ∧ d ∈ dom(Σ_k.M) : ran_C(d, Σ_k) ⊆ ran_C(d, Σ_{k+1}))` — sufficient syntactic condition: no composite of the trace contains a K.μ⁻ step (then every atomic step frames or extends arrangements, FD-FRAME/FD-STEP; note a reorder's decomposition contains K.μ⁻, though its net effect satisfies the semantic hypothesis anyway). Along such a trace the two queries coincide at the endpoint: `finddocs_R(I, Σ) = finddocs(I, Σ)`. Derivation: (⊇) FD-SUPER. (⊆) FD-WITNESS gives liveness at some `Σ_k`; the chained range inclusions carry the witness `a ∈ ran_C(d, Σ_k) ⊆ ⋯ ⊆ ran_C(d, Σ)`.*
