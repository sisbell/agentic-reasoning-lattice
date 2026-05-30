# ASN-0084: Cut-Point Rearrangements

*2026-04-10*

This ASN layers a class of arrangement rearrangements over the Strand Model (ASN-0036). The arrangement function M(d) is mutated by transposing regions of V-positions delimited by cut points: three cuts define two adjacent regions that exchange places (the *pivot*); four cuts define two outer regions exchanging across a fixed middle (the *swap*). REARRANGE is confined to the text subspace (S = 1, depth 2); cross-subspace transposition is outside the scope of this ASN. The induced bijection π : dom(M(d)) → dom(M(d)) has a uniform displacement structure on each region, determined by region widths alone. The correspondence-run decomposition guaranteed by S8 (ASN-0036) transforms by splitting at cuts, classifying each run into a region, and reassembling with the per-region displacement. The proofs draw directly on ASN-0036 (Strand Model — correspondence runs S8, contiguity D-CTG, sequential positions D-SEQ) and ASN-0034 (Tumbler Algebra — ordinal shift OrdinalShift, shift composition TS3, lexicographic order T1).

**Dependency audit.** The inquiry declares `depends: {34, 36, 53}`. ASN-0034 and ASN-0036 are load-bearing throughout: every region/interval argument, displacement computation, and run-decomposition step below cites one or both (T1, OrdinalShift, TS2–TS5, TA5, and the NAT-* arithmetic axioms from ASN-0034; S0–S8, D-CTG, D-SEQ, D-MIN, and OrdShiftHom from ASN-0036). No property of ASN-0053 (Span Algebra) is invoked anywhere in the body. The region/interval reasoning that span algebra would otherwise supply — disjointness, coverage, split, and merge of spans (ASN-0053 SC, S1, S3, S4) — is instead grounded in ASN-0036's D-SEQ, which enumerates V_S(d) as the concrete sequential set {[S, 1], ..., [S, N]}; under this enumeration all interval reasoning reduces to elementary natural-number arithmetic over the ordinals, never to span-algebra claims about (start, width) pairs. ASN-0053 therefore has no use site and is flagged for removal from the inquiry's `depends:` set.


## State and Vocabulary

We work with the content store C : T ⇀ Val (Σ.C, ASN-0036) and the arrangement function M(d) : T ⇀ T for each document d (Σ.M(d), ASN-0036). The arrangement M(d) is the mutable layer; C is immutable (S0, ASN-0036).

For a V-position v with subspace(v) = v₁ and #v = m, the *ordinal* is ord(v) = [v₂, ..., vₘ] — the tumbler obtained by stripping the subspace identifier v₁ (the complement of ASN-0036's SubspaceProjection, which extracts v₁; ord itself is defined locally here, as the foundation exports no tail-projection).

We restrict to the text subspace (subspace identifier 1) throughout this ASN. ASN-0036's S8-depth establishes only the lower bound m_s ≥ 2 on each subspace's depth, and ValidFirstInsertionPosition (ASN-0036) leaves the per-subspace depth m_s operator-chosen at initialization (constrained only by m_s ≥ 2). This ASN imposes the additional scope restriction that the text subspace has been initialized at the *minimum* permitted depth m_1 = 2; documents with m_1 > 2 are outside the scope of this ASN. Under this depth-2 restriction, S8-depth gives that every V-position v ∈ V_1(d) satisfies #v = 2 (ordinal depth 1). The operations defined here apply only to the text subspace; outside this scope (link subspace, or any other subspace at any depth), neither the rearrangement postconditions nor the supporting lemmas of this ASN are claimed to apply. The text-subspace restriction is deliberate: REARRANGE acts on the text region of a document and is not defined as a cross-subspace operation. CS3 and CS4 below jointly enforce this scope: CS3 requires subspace(cᵢ) = 1 for all cuts, and CS4 requires #cᵢ = 2. For parametric uniformity with ASN-0036's V_S(d), [S, k] notation, we use S = 1 throughout and read every appearance of S in this ASN as the text-subspace identifier 1. By D-SEQ (ASN-0036), which characterizes V_1(d) as a sequential range without gaps, V_S(d) = V_1(d) = {[S, k] : 1 ≤ k ≤ N} for some N ≥ 0, and each ord(v) is a singleton tumbler [k] with k ∈ ℕ⁺.

**Identification of singleton tumblers with natural numbers.** At depth 2, we identify the singleton tumbler [k] with the natural number k throughout the displacement and width arithmetic. The identification is licensed as follows. The set of singleton tumblers {[k] : k ∈ ℕ⁺} is in bijection with ℕ⁺ by the map [k] ↔ k (a singleton tumbler is determined by its single component). Under this bijection: T1's strict ordering on tumblers (ASN-0034) restricted to singletons coincides with the standard `<` on ℕ⁺ (lexicographic order on a single component reduces to comparison of that component); for j ≥ 1, OrdinalShift (ASN-0034) gives `shift([k], j) = [k + j]`, with `k + j ∈ ℕ⁺` by addition closure (NAT-closure, ASN-0034); the case j = 0 is covered by the identity convention introduced below (`shift([k], 0) := [k]`), which extends OrdinalShift's domain from ℕ⁺ to ℕ. **Truncated subtraction.** We define `m − n` (partial, m ≥ n) *locally in this ASN* — it is not a foundation export — as the unique j ∈ ℕ with [n] ≤ [m] and `shift-or-identity([n], j) = [m]`: OrdinalShift gives j ≥ 1 when m > n, and the identity convention gives j = 0 when m = n; existence and uniqueness of j are OrdinalShift's surjectivity onto {[k] : k ≥ n} and TS5 (ShiftAmountMonotonicity, ASN-0034) injectivity in the shift amount. By construction the right-inverse identity `n + (m − n) = m` holds (it is the defining equation `shift([n], m − n) = [m]`). Cancellation of ℕ-addition, where used below, is likewise discharged through the identification: `a + c = b + c ⟹ a = b` by TS2 (ShiftInjectivity, ASN-0034) and `c + a = c + b ⟹ a = b` by TS5 (ShiftAmountMonotonicity, ASN-0034). The width of an interval |[c, c')| = ord(c') − ord(c) (this truncated subtraction is total here because c < c' under T1, hence ord(c) < ord(c'), hence ord(c') ≥ ord(c)) yields a natural number. We use this identification implicitly: expressions like `ord(c₀) + j`, `ord(c₁) = ord(c₀) + w_α`, and `w_β = ord(c₂) − ord(c₁)` are read as natural-number arithmetic over the identified domain.

We recall D-CTG (VContiguity, ASN-0036): within each subspace, V-positions form a contiguous ordinal range with no gaps.

**Definition — ArrangementRearrangement.** An *arrangement rearrangement* is a state transition Σ → Σ' in which dom(M'(d)) = dom(M(d)), C' = C (S0, ASN-0036), M'(d') = M(d') for all d' ≠ d, and there exists a bijection π : dom(M(d)) → dom(M'(d)) such that M'(d)(π(v)) = M(d)(v) for all v ∈ dom(M(d)).

We derive that the I-address range is invariant and that multiplicities are preserved. Since π is a bijection from dom(M(d)) to dom(M'(d)) = dom(M(d)), every u ∈ dom(M'(d)) has the form u = π(v) for exactly one v ∈ dom(M(d)). Therefore: ran(M'(d)) = {M'(d)(u) : u ∈ dom(M'(d))} = {M'(d)(π(v)) : v ∈ dom(M(d))} = {M(d)(v) : v ∈ dom(M(d))} = ran(M(d)). The second equality uses surjectivity of π; the third uses the defining property M'(d)(π(v)) = M(d)(v). The multiset of I-addresses is also preserved: since π is a bijection, for each I-address a, the preimage {v : M(d)(v) = a} is in bijection (via π) with {π(v) : M(d)(v) = a}; we now show this latter set equals {u : M'(d)(u) = a} by establishing both inclusions. *Forward inclusion ({π(v) : M(d)(v) = a} ⊆ {u : M'(d)(u) = a}):* for v with M(d)(v) = a, the defining property M'(d)(π(v)) = M(d)(v) = a places π(v) in {u : M'(d)(u) = a}. *Backward inclusion ({u : M'(d)(u) = a} ⊆ {π(v) : M(d)(v) = a}):* for u with M'(d)(u) = a, surjectivity of π gives u = π(v) for some v ∈ dom(M(d)), and the defining property gives M(d)(v) = M'(d)(π(v)) = M'(d)(u) = a, so v lies in {v : M(d)(v) = a} and hence u = π(v) lies in {π(v) : M(d)(v) = a}. Both inclusions follow from the defining property M'(d)(π(v)) = M(d)(v) combined with bijectivity of π. The multiplicity of a is therefore identical in M(d) and M'(d).

**R-RI — RearrangementReferentialIntegrity (LEMMA).**

*Preconditions:* M(d) is well-defined; M'(d) results from an arrangement rearrangement of M(d) (dom(M'(d)) = dom(M(d)), C' = C, M'(d')= M(d') for d' ≠ d, and there exists a bijection π with M'(d)(π(v)) = M(d)(v)).

*Depends on:* ASN-0036 S3 (referential integrity of the pre-state), C' = C from the rearrangement definition, and the I-address range invariance ran(M'(d)) = ran(M(d)) derived above.

*Postcondition:* ran(M'(d)) ⊆ dom(C').

*Proof.* By the I-address range invariance shown above, ran(M'(d)) = ran(M(d)). By S3 of the pre-state, ran(M(d)) ⊆ dom(C). By C' = C, dom(C) = dom(C'). Chaining: ran(M'(d)) = ran(M(d)) ⊆ dom(C) = dom(C'). ∎

**Invariant preservation.** The following ASN-0036 invariants depend only on `dom(M(d))` and are preserved because `dom(M'(d)) = dom(M(d))`: D-CTG, D-CTG-depth (vacuous under the depth-2 scope of this ASN), D-MIN, D-SEQ, S8-fin, S8a, S8-depth. S2 (arrangement functionality) holds because each u ∈ dom(M'(d)) has u = π(v) for exactly one v (bijectivity), so M'(d)(u) = M(d)(v) is uniquely determined. S3 (referential integrity) is precisely the postcondition of R-RI above — ran(M'(d)) ⊆ dom(C') — so R-RI is the S3-preservation step of this invariant audit. **C-transport.** C' = C (the rearrangement definition), and the two-stream separation of the ASN-0036 state model — Σ.C and Σ.M(d) are distinct components, so no mutation of Σ.M(d) can alter Σ.C — together with S0 (content immutability) make "Σ.C is unchanged" immediate; the only mutation is to Σ.M(d). Hence every invariant stated on Σ.C alone carries over by identity: S0 (content immutability), S1 (store monotonicity), S4 (origin-based identity), S7a (document-scoped allocation), S7b (element-level I-addresses — which by zeros(a) = 3 asserts the element field is present), and S7d (document allocation discipline). **S5-multiplicity.** S5 (unrestricted sharing) is a permission rather than an obligation; the multiset-of-I-addresses preservation derived above — each I-address has identical multiplicity in M(d) and M'(d) by bijectivity of π — preserves any pre-existing sharing pattern. Every ASN-0036 invariant except the two S8 clauses (uniqueness of the containing run, and consistency under M'(d)) is therefore maintained by an arrangement rearrangement; preservation of S8 is established constructively in R-SP via R-BLK.

Any bijection qualifies; a rearrangement determined by cut points is one where the regions to exchange are identified by a tuple of cut positions. The properties in this ASN characterize this specific class of permutations.

Notation: at depth 2, V-positions have the form [S, p]. We write `c₀ + j` for the V-position [S, ord(c₀) + j] — that is, ordinal shift via OrdinalShift (ASN-0034): `c₀ + j = shift(c₀, j)`, consistent with the correspondence-run convention of ASN-0036. By convention, `c₀ + 0 = c₀` (identity). This extends OrdinalShift's domain from ℕ⁺ (the foundation's domain) to ℕ.

**Extended Associativity.** For all j, k ∈ ℕ, `(c + j) + k = c + (j + k)`: the j, k ≥ 1 case is TS3 (ShiftComposition, ASN-0034), `shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)`, and the cases with j = 0 or k = 0 hold by the identity convention. We cite this identity below as *Extended Associativity*. The same identity convention extends TS2 (ShiftInjectivity) and OrdShiftHom (b) — `subspace(shift(v, n)) = subspace(v)` (ASN-0036) — to n = 0, since shift(v, 0) = v; TS5 (ShiftAmountMonotonicity) extends to a zero amount via TS4 (StrictIncrease), since shift(v, 0) = v differs from shift(v, n) > v for n ≥ 1. TS4 itself requires n ≥ 1: `shift(v, n) > v` fails at n = 0 under T1 irreflexivity.


## Cut Points and the Region Partition

A *cut sequence* specifies the boundaries of regions to transpose. We formalize this as a tuple of tumblers within a single subspace. The cut positions are tumblers satisfying CS1–CS4 below; the last cut c_{n−1} serves as an exclusive upper bound and need not belong to V_S(d).

**Definition — CutSequence.** A *cut sequence* for document d in subspace S is a tuple K = (c₀, c₁, ..., c_{n−1}) of tumblers satisfying:

(CS1) n ∈ {3, 4} — exactly three or four cuts.

(CS2) c₀ < c₁ < ... < c_{n−1} under T1 (ASN-0034) — strictly ordered.

(CS3) subspace(cᵢ) = S = 1 for all i — all cuts in the text subspace.

(CS4) #cᵢ = 2 for all i — depth-2 positions.

The cut positions partition the V-positions of the affected range into regions. For n = 3 (the *pivot*), the cuts define two adjacent regions. For n = 4 (the *swap*), the cuts define two outer regions separated by a middle region.

**Definition — RegionPartition.** Given a cut sequence K for document d in subspace S with V_S(d) ≠ ∅:

For n = 3, the *affected range* A = {v ∈ V_S(d) : c₀ ≤ v < c₂} is partitioned:

```
α = {v ∈ V_S(d) : c₀ ≤ v < c₁}     — first region
β = {v ∈ V_S(d) : c₁ ≤ v < c₂}     — second region
```

For n = 4, the *affected range* A = {v ∈ V_S(d) : c₀ ≤ v < c₃} is partitioned:

```
α = {v ∈ V_S(d) : c₀ ≤ v < c₁}     — first region
μ = {v ∈ V_S(d) : c₁ ≤ v < c₂}     — middle region
β = {v ∈ V_S(d) : c₂ ≤ v < c₃}     — second region
```

Pairwise disjointness follows from the strict ordering of cut points and the trichotomy of T1: for any two distinct inter-cut intervals [c_i, c_{i+1}) and [c_j, c_{j+1}) with i < j, every v ∈ [c_i, c_{i+1}) satisfies v < c_{i+1} ≤ c_j (by CS2), so v ∉ [c_j, c_{j+1}) — the intervals are disjoint.

*Exhaustiveness.* For any v ∈ A, we show v lies in exactly one inter-cut interval by T1 trichotomy. For n = 3, A = {v ∈ V_S(d) : c₀ ≤ v < c₂}. T1 trichotomy on (v, c₁) yields three sub-cases: (i) v < c₁ — combined with c₀ ≤ v gives v ∈ [c₀, c₁) = α; (ii) v = c₁ — then v = c₁ < c₂ gives v ∈ [c₁, c₂) = β; (iii) v > c₁ — combined with v < c₂ gives v ∈ [c₁, c₂) = β. Each sub-case places v in exactly one region; disjointness above rules out double-counting. For n = 4, A = {v ∈ V_S(d) : c₀ ≤ v < c₃}. T1 trichotomy on (v, c₁) and (v, c₂) yields five admissible sub-cases (the c_0 ≤ v < c_3 hypothesis rules out v < c_0 and v ≥ c_3): (i) v < c₁ — then c₀ ≤ v < c₁ gives v ∈ α; (ii) v = c₁ — then v = c₁ < c₂ gives v ∈ [c₁, c₂) = μ; (iii) c₁ < v < c₂ — gives v ∈ μ; (iv) v = c₂ — then v = c₂ < c₃ gives v ∈ [c₂, c₃) = β; (v) c₂ < v < c₃ — gives v ∈ β. Each sub-case places v in exactly one region. Each region is a set of consecutive V-positions (by D-CTG, ASN-0036, restricted to the interval between its bounding cuts).

We write w_α = |α|, w_β = |β|, w_μ = |μ| for the region widths.

*Width-ordinal identities.* Under R-PRE, by R-PRE(iv) and D-SEQ (ASN-0036), the region widths are computable from the cut-point ordinals: w_α = ord(c₁) − ord(c₀); w_β = ord(c₂) − ord(c₁) for n = 3 and ord(c₃) − ord(c₂) for n = 4; w_μ = ord(c₂) − ord(c₁) for n = 4. By CS2 and T1, c_i < c_{i+1}, and under the singleton-tumbler identification of singleton tumblers with natural numbers (introduced above) this strict ordering coincides with ord(c_i) < ord(c_{i+1}) ∈ ℕ⁺. Hence ord(c_{i+1}) ≥ ord(c_i) + 1 > ord(c_i), discharging the m ≥ n precondition of the truncated subtraction (defined above) for each difference; each width is therefore a well-defined positive natural number (≥ 1).


## Rearrangement Postconditions

The following precondition and postcondition clauses define the rearrangement operation. They are the assumed operational context for the properties introduced in this ASN.

**R-PRE — RearrangePrecondition.**

(i) M(d) is well-defined (the document's arrangement exists).

(ii) V_S(d) ≠ ∅ (the subspace is non-empty — one cannot rearrange nothing).

(iii) The cut sequence K = (c₀, ..., c_{n−1}) satisfies CS1–CS4.

(iv) The affected range lies entirely within the current arrangement:

`(A v : subspace(v) = S ∧ #v = 2 ∧ c₀ ≤ v < c_{n−1} : v ∈ V_S(d))`

Clause (iv) ensures that the affected range is covered: no gap exists within [c₀, c_{n−1}). Combined with D-CTG, this says the entire inter-cut range consists of valid V-positions in V_S(d). Region non-degeneracy (w_α ≥ 1, w_β ≥ 1 in both forms, and w_μ ≥ 1 when n = 4) is *derived* from (iii) and (iv) rather than imposed as a separate precondition; the derivation is recorded as the "Width positivity" consequence below.

**Consequences of R-PRE.** *Subspace confinement.* All cuts lie in subspace S by CS3, and every V-position in the affected range [c₀, c_{n−1}) ∩ V_S(d) has subspace S by membership in V_S(d). The shifted positions `c₀ + j`, `c₁ + j`, `c₂ + j` named in R-P1, R-P2, R-S1, R-S2, R-S3 retain subspace S by case analysis on j: when j = 0, `c_i + 0 = c_i` by the identity convention, so subspace(c_i + 0) = subspace(c_i) = S directly by CS3; when j ≥ 1, OrdShiftHom (b) of ASN-0036 gives `subspace(shift(v, n)) = subspace(v)`, so subspace(c_i + j) = subspace(c_i) = S, again by CS3. The rearrangement constructions in this ASN (PivotPostcondition, SwapPostcondition) only assign new I-addresses to V-positions in V_S(d) and leave all other positions fixed (R-FRAME-P, R-FRAME-S), so no position outside subspace S is ever produced. This is a derived consequence of CS3, CS4, the identity convention, and OrdShiftHom (b) (ASN-0036), not a separate verification obligation.

*Width positivity.* Under R-PRE(iii) and R-PRE(iv), all region widths are positive: w_α ≥ 1 and w_β ≥ 1 in both forms, and additionally w_μ ≥ 1 when n = 4. The derivation has two steps for each adjacent cut pair (c_i, c_{i+1}). *Step 1 (cut-ordinal inequality from R-PRE(iii)).* Under CS3 and CS4, the singleton-tumbler identification reduces CS2's strict tumbler ordering c_i < c_{i+1} to ord(c_i) < ord(c_{i+1}), so ord(c_{i+1}) − ord(c_i) ≥ 1 by the truncated subtraction defined above (whose right-inverse identity, grounded in OrdinalShift, gives ord(c_i) + (ord(c_{i+1}) − ord(c_i)) = ord(c_{i+1}) > ord(c_i)). *Step 2 (region width = count of V-positions, via R-PRE(iv) and D-SEQ).* D-SEQ (ASN-0036) gives V_S(d) = {[S, k] : 1 ≤ k ≤ N} for some N, and R-PRE(iv) places every depth-2 subspace-S position with ordinal in [ord(c_i), ord(c_{i+1})) into V_S(d); the count of V-positions in [c_i, c_{i+1}) therefore equals ord(c_{i+1}) − ord(c_i) ≥ 1. *Concrete witnesses.* For each adjacent cut pair (c_i, c_{i+1}), the position c_i itself witnesses [c_i, c_{i+1}) ∩ V_S(d) ≠ ∅: by CS3, subspace(c_i) = S; by CS4, #c_i = 2; CS2 gives c₀ ≤ c_i < c_{n−1} (for i ≤ n − 2), placing c_i in [c₀, c_{n−1}) and hence in V_S(d) by R-PRE(iv); and c_i ∈ [c_i, c_{i+1}) by CS2's c_i < c_{i+1}. Instantiating at i = 0 yields w_α ≥ 1; at i = 1 (n = 4) yields w_μ ≥ 1; at i = n − 2 yields w_β ≥ 1.

*Empty-exterior boundary cases.* R-EXT in both PivotPostcondition and SwapPostcondition quantifies over {v ∈ V_S(d) : v < c₀ or v ≥ c_{n−1}}, and either subset may be empty for boundary configurations of the cut sequence. When ord(c₀) = 1, no V-position satisfies v < c₀ (V-position ordinals are ≥ 1 by S8a, ASN-0036), so the left-exterior subset is empty and R-EXT is vacuously satisfied on the left. When V_S(d) = {[S, 1], ..., [S, N]} and ord(c_{n−1}) = N + 1 (i.e., c_{n−1} sits one past the last V-position), no V-position satisfies v ≥ c_{n−1}, so the right-exterior subset is empty and R-EXT is vacuously satisfied on the right; R-PRE(iv) is unaffected because it constrains only [c₀, c_{n−1}), which excludes c_{n−1} itself. Both boundary configurations are admissible: R-PRE(iv) covers the entire affected range, R-EXT degenerates to a vacuous quantification on the empty side, and the well-definedness arguments (R-PIV, R-SWP) — which partition V_S(d) into the affected range and the exterior — proceed unchanged when one exterior subset is empty.


### 3-Cut Pivot Postcondition

Three cuts produce two adjacent regions that exchange places. The operation is: place β's content where α was, then place α's content immediately after.

**Definition — PivotPostcondition.** Given a 3-cut sequence K = (c₀, c₁, c₂) satisfying R-PRE, the *pivot* produces arrangement M'(d) defined by:

(R-EXT) For v ∈ V_S(d) with v < c₀ or v ≥ c₂:

`M'(d)(v) = M(d)(v)`

(R-P1) For 0 ≤ j < w_β:

`M'(d)(c₀ + j) = M(d)(c₁ + j)`

(R-P2) For 0 ≤ j < w_α:

`M'(d)(c₀ + w_β + j) = M(d)(c₀ + j)`

The domain is dom(M'(d)) = dom(M(d)).

(R-FRAME-P) Frame conditions:

(a) For v ∈ dom(M(d)) with subspace(v) ≠ S: M'(d)(v) = M(d)(v).

(b) For all d' ≠ d: M'(d') = M(d').

(c) C' = C (S0, ASN-0036).

In words: the first w_β positions of the affected range receive the content that was in β (clause R-P1). The next w_α positions receive the content that was in α (clause R-P2). Everything outside the affected range is unchanged (clause R-EXT). Positions in other subspaces, other documents, and the content store are all preserved.


### 4-Cut Swap Postcondition

Four cuts produce two outer regions separated by a middle region. The semantics is a direct extension of the pivot: place β's content where α was, place μ's content immediately after, place α's content last.

**Definition — SwapPostcondition.** Given a 4-cut sequence K = (c₀, c₁, c₂, c₃) satisfying R-PRE, the *swap* produces M'(d) defined by:

(R-EXT) For v ∈ V_S(d) with v < c₀ or v ≥ c₃:

`M'(d)(v) = M(d)(v)`

(R-S1) For 0 ≤ j < w_β:

`M'(d)(c₀ + j) = M(d)(c₂ + j)`

(R-S2) For 0 ≤ j < w_μ:

`M'(d)(c₀ + w_β + j) = M(d)(c₁ + j)`

(R-S3) For 0 ≤ j < w_α:

`M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j)`

The domain is dom(M'(d)) = dom(M(d)).

(R-FRAME-S) Frame conditions:

(a) For v ∈ dom(M(d)) with subspace(v) ≠ S: M'(d)(v) = M(d)(v).

(b) For all d' ≠ d: M'(d') = M(d').

(c) C' = C (S0, ASN-0036).

The arrangement is: region β content starting at c₀ (clause R-S1), then middle content (clause R-S2), then region α content (clause R-S3). Everything outside [c₀, c₃) is unchanged (clause R-EXT). Positions in other subspaces, other documents, and the content store are all preserved.

**Operation — REARRANGE_K.** REARRANGE_K(Σ, d) is the state transition Σ → Σ' that produces Σ' satisfying PivotPostcondition (when n = 3) or SwapPostcondition (when n = 4) together with the corresponding frame conditions R-FRAME-P (n = 3) or R-FRAME-S (n = 4). The two cases of n are mutually exclusive (CS1) and exhaustive over admissible cut sequences, so REARRANGE_K is a single operation whose postcondition specializes by the cut count. *Partiality.* REARRANGE_K is a partial operation on the state space: it is defined exactly on those (Σ, d) for which R-PRE(K) holds against Σ.M(d); on inputs that violate R-PRE(K), REARRANGE_K is undefined, and this ASN makes no commitment about the resulting state — neither that the operation aborts, nor that it produces some particular Σ', nor that any postcondition is satisfied. Out-of-contract behaviour is the caller's obligation to avoid via R-PRE(K), not the specification's to characterize.

REARRANGE_K has precondition R-PRE(K) and runtime signature (Σ, d) ↦ Σ'. The intra-document arrangement Σ.M(d) is the only mutated component: Σ.C, all other documents' arrangements Σ.M(d') for d' ≠ d, and the within-d non-S subspace portion of Σ.M(d) are preserved by the frame conditions; dom(M'(d)) = dom(M(d)) is asserted by the postconditions. This is the operation referent invoked by `wp(REARRANGE_K, Q)` in R-SP below.

**Reduction of compound shifts (R-P2, R-S2, R-S3).** The destination expressions `c₀ + w_β + j` (R-P2 and R-S2) and `c₀ + w_β + w_μ + j` (R-S3) are read as iterated ordinal shifts that reduce to single-step shifts via Extended Associativity (above). Explicitly, for any j ∈ ℕ:

- `c₀ + w_β + j = (c₀ + w_β) + j` (R-P2 and R-S2), by Extended Associativity with the outer pair (w_β, j) ∈ ℕ × ℕ. The intermediate position `c₀ + w_β` has subspace S by OrdShiftHom (b), so the subsequent shift by j is again a valid OrdinalShift application on a subspace-S V-position.
- `c₀ + w_β + w_μ + j = ((c₀ + w_β) + w_μ) + j` (R-S3), by two applications of Extended Associativity: first the outer pair (w_μ, j) ∈ ℕ × ℕ reduces `(c₀ + w_β) + (w_μ + j)` to `((c₀ + w_β) + w_μ) + j`, then the inner pair (w_β, w_μ) ∈ ℕ × ℕ underlies the identification `c₀ + (w_β + w_μ) = (c₀ + w_β) + w_μ`. The combined identity `c₀ + w_β + w_μ + j = ((c₀ + w_β) + w_μ) + j` is what the well-definedness arguments of R-PIV and R-SWP consume when computing the ordinal range covered by each clause.

The identity convention covers the j = 0 case of each step.

We must verify that the clauses cover [c₀, c₃) without overlap. The total width is w_β + w_μ + w_α. We need this to equal |[c₀, c₃)| = w_α + w_μ + w_β. Trivially: w_β + w_μ + w_α = w_α + w_μ + w_β. The three clause ranges are [c₀, c₀ + w_β), [c₀ + w_β, c₀ + w_β + w_μ), [c₀ + w_β + w_μ, c₀ + w_β + w_μ + w_α). By commutativity of natural-number addition, the last position is c₀ + (w_β + w_μ + w_α) = c₀ + (w_α + w_μ + w_β). And c₀ + (w_α + w_μ + w_β) has ordinal ord(c₀) + w_α + w_μ + w_β = ord(c₃), so the three ranges tile [c₀, c₃) exactly.


## Non-S Subspace Invariance

REARRANGE_K affects only the subspace-S portion of M(d); positions in any other subspace pass through unchanged. We collect the consequences of this structural fact into one lemma.

**R-NS — NonSubspaceInvariance (LEMMA).** Let π be the cut-point-induced bijection on dom(M(d)) (R-PPERM for n = 3, R-SPERM for n = 4), and let B be a correspondence-run partition of M(d). The following hold jointly:

*(NS-π) Pointwise identity on non-S.* For every v ∈ dom(M(d)) with subspace(v) ≠ S: π(v) = v and M'(d)(v) = M(d)(v).

*(NS-run) Non-S runs carry verbatim into B'.* For every run b = (v_b, a_b, n_b) ∈ B with subspace(v_b) = S' ≠ S, the same triple (v_b, a_b, n_b) appears unchanged in B' = R-BLK(B), with the post-state S8-cons consistency M'(d)(v_b + k) = a_b + k for 0 ≤ k < n_b inherited verbatim from the pre-state S8-cons consistency of b under M(d).

*(NS-inv) ASN-0036 invariants on non-S positions transport trivially.* Every ASN-0036 invariant evaluated at a V-position v with subspace(v) ≠ S — or at a run whose V-extent lies in some subspace S' ≠ S — that depends only on dom(M restricted to non-S positions) and on M restricted to non-S positions is preserved unchanged on M'(d).

*Proof.*

*(NS-π).* For v ∈ dom(M(d)) with subspace(v) ≠ S, the frame condition R-FRAME-P(a) (n = 3) or R-FRAME-S(a) (n = 4) gives M'(d)(v) = M(d)(v) directly. The non-S clause of the bijection definition (the first clause of R-PPERM's piecewise definition, mirrored as the first clause of R-SPERM's) stipulates π(v) = v on this domain; combined with the frame condition, this stipulation is consistent with the rearrangement defining equation M'(d)(π(v)) = M(d)(v) — substituting π(v) = v yields M'(d)(v) = M(d)(v), already supplied by the frame condition. Hence π fixes every non-S V-position pointwise, and M'(d) agrees with M(d) on every such position. The argument uses only (a) the frame clause of the operation's contract and (b) the first-line stipulation of the bijection definition; no subspace-S content of R-PPERM or R-SPERM is invoked.

*(NS-run).* Let b = (v_b, a_b, n_b) ∈ B with subspace(v_b) = S' ≠ S. *V-extent confinement.* By OrdShiftHom (b) of ASN-0036, subspace(shift(v_b, k)) = subspace(v_b) = S' for every 1 ≤ k < n_b; the identity convention gives subspace(v_b + 0) = subspace(v_b) = S'. Hence every V-position v_b + k of b satisfies subspace(v_b + k) = S' ≠ S, so V(b) ⊆ dom(M(d)) \ V_S(d). *Cut separation.* By CS3, every cut position cᵢ has subspace(cᵢ) = S; since S' ≠ S, cᵢ ∉ V(b). Hence Phase 1 of R-BLK never splits b — no cut position falls in V(b), so neither the interior-of-a-run nor the boundary-of-a-run sub-case fires for b at any step. *Phases 2 and 3.* Phase 2 classifies b into the dedicated non-S region (V-extent in a subspace other than S). Phase 3 applies displacement zero to non-S runs (the non-S clause of Phase 3 explicitly preserves V-start, I-start, and width — equivalently, π acts as the identity on V(b) by (NS-π)). The resulting B' contains the triple (v_b, a_b, n_b) unchanged. *Post-state S8-cons consistency.* For 0 ≤ k < n_b: M'(d)(v_b + k) = M(d)(v_b + k) (by (NS-π) applied at v_b + k, which has subspace ≠ S as established above) = a_b + k (by S8-cons of b under M(d), supplied by B). Hence (v_b, a_b, n_b) ∈ B' satisfies S8-cons under M'(d).

*(NS-inv).* Two structural facts feed the transport. *(a) dom(M'(d)) = dom(M(d))*, asserted by the rearrangement postconditions (R-EXT plus the R-P1/R-P2 or R-S1/R-S2/R-S3 image equalities cover V_S(d); R-FRAME-P(a)/R-FRAME-S(a) covers the rest). *(b)* M'(d) and M(d) agree pointwise on dom(M(d)) \ V_S(d), by (NS-π). Any ASN-0036 invariant whose evaluation at a non-S V-position depends only on (i) which non-S V-positions are in dom and (ii) the values of M restricted to non-S V-positions is therefore preserved unchanged. *Catalogue (non-S-applicable invariants).* S8a (VPositionWellFormedness) — applicable at any V-position regardless of subspace, requiring positive ordinal — depends only on (i) and is preserved by (a) at every non-S V-position. The per-subspace clauses of S8-fin and S8-depth applicable to non-S subspaces S' ≠ S (each constraining only dom restricted to a single subspace) likewise depend only on (i) and are preserved by (a). S2 (arrangement functionality) at non-S positions depends on (i) and the agreement of M and M', preserved by (a) and (b). *Out of scope for (NS-inv).* D-CTG, D-CTG-depth, D-MIN, D-SEQ are stated about V_S(d) specifically (subspace S = 1: contiguous depth structure of V_S(d), the minimum-depth text subspace, sequential ordinal labelling V_S(d) = {[S, 1], ..., [S, N]}), so they have no non-S evaluation and are not (NS-inv) consumers; their preservation under REARRANGE_K is discharged at the global dom-preservation step in R-SP (dom(M'(d)) = dom(M(d))), not via the non-S agreement above. S3 contributions from non-S V-positions reduce to {M'(d)(v) : subspace(v) ≠ S} = {M(d)(v) : subspace(v) ≠ S} by (b), so the ran(M'(d)) ⊆ dom(C') containment on the non-S portion follows from the pre-state's analogous containment on the non-S portion (with C' = C by R-FRAME-P(c)/R-FRAME-S(c)). S8-uniq on non-S runs reduces to the pre-state's uniqueness-of-containing-run on non-S V-positions via (NS-run): the carried-over runs are pairwise disjoint and cover dom(M(d)) \ V_S(d) by the pre-state partition property, and (NS-run) preserves this verbatim into B'. S8-cons on non-S runs is the consistency clause established in (NS-run). The content-store invariants (S0, S1, S4, S5, S7a, S7b, S7d) are independent of M and so independent of the non-S/subspace-S distinction; they appear here only for completeness — REARRANGE_K preserves them by C' = C. ∎


## Postcondition Well-Definedness

**R-PIV — PivotWellDefined (LEMMA, supporting).** The pivot postcondition defines a total function on dom(M(d)) (each position is assigned exactly one I-address).

*Proof.* We must show: (a) every v ∈ dom(M(d)) falls under exactly one clause, and (b) the right-hand sides are well-defined.

For v ∈ dom(M(d)) with subspace(v) ≠ S: R-NS(NS-π) (equivalently R-FRAME-P(a)) assigns M'(d)(v) = M(d)(v), and no other clause applies (R-EXT, R-P1, R-P2 operate only on subspace S positions).

It remains to show that every v ∈ V_S(d) falls under exactly one of R-EXT, R-P1, R-P2.

For (a): the positions addressed by R-EXT are those outside [c₀, c₂). The positions addressed by R-P1 are {c₀ + j : 0 ≤ j < w_β}. At depth 2, c₀ = [S, p] and c₀ + j = [S, p + j], so these positions have ordinals p, p + 1, ..., p + w_β − 1. By R-PRE(iv), all V-positions with subspace S, depth 2, and ordinal in [p, p + w_α + w_β) lie in V_S(d), so the R-P1 positions are distinct elements of V_S(d). The positions addressed by R-P2 are {c₀ + w_β + j : 0 ≤ j < w_α} = {[S, p + w_β + j] : 0 ≤ j < w_α}, with ordinals p + w_β, ..., p + w_β + w_α − 1. By associativity of ordinal addition, c₀ + (w_β + j) = (c₀ + w_β) + j, so these are well-defined.

The R-P1 ordinal range is [p, p + w_β). The R-P2 ordinal range is [p + w_β, p + w_β + w_α). Both ranges are non-empty (since w_β ≥ 1 and w_α ≥ 1 by Width positivity), and they are disjoint because [p, p + w_β) ∩ [p + w_β, p + w_β + w_α) = ∅ — the half-open intervals meet at the shared endpoint p + w_β, which is included only in the second range. Their union is [p, p + w_β + w_α) = [p, p + w_α + w_β). And p + w_α + w_β is the ordinal of c₂ (since |[c₀, c₂)| = w_α + w_β, and by R-PRE(iv) the ordinals in [c₀, c₂) lie consecutively in V_S(d)). So the union of R-P1 and R-P2 covers exactly [c₀, c₂) ∩ V_S(d). Together with R-EXT (covering V_S(d) \ [c₀, c₂)), every position is covered exactly once.

For (b): the right-hand sides reference M(d)(c₁ + j) for j < w_β and M(d)(c₀ + j) for j < w_α. By R-PRE(iv), all positions in [c₀, c₂) are in V_S(d) ⊆ dom(M(d)). The positions c₁ + j for j < w_β have ordinals in [ord(c₁), ord(c₂)) = the ordinals of β. The positions c₀ + j for j < w_α have ordinals in [ord(c₀), ord(c₁)) = the ordinals of α. Both sets are subsets of [c₀, c₂) ∩ V_S(d) ⊆ dom(M(d)). ∎


**R-SWP — SwapWellDefined (LEMMA, supporting).** The swap postcondition defines a total function on dom(M(d)).

*Proof.* We must show: (a) every v ∈ dom(M(d)) falls under exactly one clause, and (b) the right-hand sides are well-defined.

For v ∈ dom(M(d)) with subspace(v) ≠ S: R-NS(NS-π) (equivalently R-FRAME-S(a)) assigns M'(d)(v) = M(d)(v), and no other clause applies.

It remains to show that every v ∈ V_S(d) falls under exactly one of R-EXT, R-S1, R-S2, R-S3.

For (a): let p = ord(c₀). The positions addressed by each clause have the following ordinal ranges:

- R-EXT: ordinals outside [p, p + w_α + w_μ + w_β), i.e., ord(v) < p or ord(v) ≥ p + w_α + w_μ + w_β.
- R-S1: {c₀ + j : 0 ≤ j < w_β}, ordinals [p, p + w_β).
- R-S2: {c₀ + w_β + j : 0 ≤ j < w_μ}, ordinals [p + w_β, p + w_β + w_μ). By associativity, c₀ + (w_β + j) = (c₀ + w_β) + j, so these are well-defined.
- R-S3: {c₀ + w_β + w_μ + j : 0 ≤ j < w_α}, ordinals [p + w_β + w_μ, p + w_β + w_μ + w_α). Similarly well-defined by associativity.

Pairwise disjointness: the four ordinal ranges are [p, p + w_β), [p + w_β, p + w_β + w_μ), [p + w_β + w_μ, p + w_β + w_μ + w_α), and the exterior. Since w_α ≥ 1, w_β ≥ 1, and w_μ ≥ 1 by Width positivity (n = 4 case), the half-open intervals are non-empty and their left endpoints are strictly increasing: p < p + w_β < p + w_β + w_μ < p + w_β + w_μ + w_α. Hence no two intervals overlap, and none overlaps with the exterior.

Exhaustiveness: the union of R-S1, R-S2, R-S3 covers ordinals [p, p + w_β + w_μ + w_α). And p + w_β + w_μ + w_α = p + w_α + w_μ + w_β = ord(c₃) (since |[c₀, c₃)| = w_α + w_μ + w_β and by R-PRE(iv) the ordinals in [c₀, c₃) lie consecutively in V_S(d)). So the union of all four clauses covers V_S(d).

For (b): the right-hand sides reference M(d)(c₂ + j) for j < w_β (ordinals of β), M(d)(c₁ + j) for j < w_μ (ordinals of μ), and M(d)(c₀ + j) for j < w_α (ordinals of α). All three sets are subsets of [c₀, c₃) ∩ V_S(d) ⊆ dom(M(d)) by R-PRE(iv). ∎


## The 3-Cut Pivot Permutation

**R-PPERM — PivotPermutation (LEMMA).** The *cut-point-induced bijection* π : dom(M(d)) → dom(M'(d)) satisfying M'(d)(π(v)) = M(d)(v) is the specific bijection determined by the cut sequence K and the region partition. *Uniqueness scope.* When the pre-state arrangement M(d) is injective on V_S(d) (every I-address appears at most once as a value of M(d)), π is the unique bijection satisfying M'(d)(π(v)) = M(d)(v) on V_S(d). When M(d) has repeated I-addresses (S5, ASN-0036 — unrestricted sharing), bijections that permute positions within each fibre {v : M(d)(v) = a} all satisfy the defining equation; π is then unique only up to that equivalence class of fibre-permutations. The cut-point-induced choice singled out here is the canonical representative whose action is determined purely by the cut sequence and the regions α and β, independent of the I-address fibre structure. The formula is:

```
         ⎧ v                   if subspace(v) ≠ S                  (non-S)
         ⎪ v                   if v ∈ V_S(d) and (v < c₀ or v ≥ c₂)  (subspace-S exterior)
π(v) =  ⎨ c₀ + w_β + j        if v = c₀ + j, 0 ≤ j < w_α              (α → end)
         ⎩ c₀ + j              if v = c₁ + j, 0 ≤ j < w_β              (β → start)
```

The non-S branch records, in the piecewise definition itself, that π is the identity on positions with subspace(v) ≠ S — exactly the (NS-π) clause of R-NS, which the proof below cites once at the non-S case. The subspace-S exterior, α, and β branches partition V_S(d), so the four-case piecewise definition is total on dom(M(d)).

*Proof.* We verify M'(d)(π(v)) = M(d)(v) in each case. For v ∈ dom(M(d)) with subspace(v) ≠ S: π(v) = v and M'(d)(v) = M(d)(v), both by R-NS(NS-π). For v ∈ V_S(d) with v < c₀ or v ≥ c₂: π(v) = v, and M'(d)(v) = M(d)(v) by R-EXT. For v = c₀ + j in α: π(v) = c₀ + w_β + j, and M'(d)(c₀ + w_β + j) = M(d)(c₀ + j) = M(d)(v) by R-P2. For v = c₁ + j in β: π(v) = c₀ + j, and M'(d)(c₀ + j) = M(d)(c₁ + j) = M(d)(v) by R-P1.

Injectivity: within each case, the mapping is injective (the exterior is the identity; the α case maps distinct j to distinct c₀ + w_β + j; the β case maps distinct j to distinct c₀ + j). Across cases: the four image sets — {v ∈ dom(M(d)) : subspace(v) ≠ S}, V_S(d) \ [c₀, c₂), {c₀ + w_β + j : 0 ≤ j < w_α}, {c₀ + j : 0 ≤ j < w_β} — are pairwise disjoint (the first is disjoint from the rest by subspace separation; the remaining three are pairwise disjoint as shown in R-PIV). Surjectivity: π is an injection from dom(M(d)) into itself, and dom(M(d)) is finite (S8-fin of ASN-0036); on a finite set, every self-injection is a bijection, so π is surjective. ∎

The pivot postcondition preserves dom(M(d)) (R-PIV), preserves C (R-FRAME-P(c)), and admits the bijection π satisfying M'(d)(π(v)) = M(d)(v) (R-PPERM); it therefore constitutes an arrangement rearrangement, and the invariant preservation established above applies.


## The 4-Cut Swap Permutation

**R-SPERM — SwapPermutation (LEMMA).** The *cut-point-induced bijection* π satisfying M'(d)(π(v)) = M(d)(v) is the specific bijection determined by the 4-cut sequence K and the regions α, μ, β. As in R-PPERM, π is the unique such bijection when M(d) is injective on V_S(d); otherwise (under S5 sharing) it is the canonical representative whose action depends only on the cut sequence and region widths, not on the I-address fibre structure. The formula is:

```
         ⎧ v                        if subspace(v) ≠ S                     (non-S)
         ⎪ v                        if v ∈ V_S(d) and (v < c₀ or v ≥ c₃)     (subspace-S exterior)
         ⎪ c₀ + w_β + w_μ + j       if v = c₀ + j, 0 ≤ j < w_α                (α → end)
π(v) =  ⎨ c₀ + w_β + j             if v = c₁ + j, 0 ≤ j < w_μ                (μ → middle)
         ⎩ c₀ + j                   if v = c₂ + j, 0 ≤ j < w_β                (β → start)
```

The non-S branch records, in the piecewise definition itself, that π is the identity on positions with subspace(v) ≠ S — exactly the (NS-π) clause of R-NS, which the proof below cites once at the non-S case. The subspace-S exterior, α, μ, and β branches partition V_S(d), so the five-case piecewise definition is total on dom(M(d)).

*Proof.* We verify M'(d)(π(v)) = M(d)(v) in each case.

For v ∈ dom(M(d)) with subspace(v) ≠ S: π(v) = v and M'(d)(v) = M(d)(v), both by R-NS(NS-π).

For v ∈ V_S(d) with v < c₀ or v ≥ c₃: π(v) = v, and M'(d)(v) = M(d)(v) by R-EXT.

For v = c₀ + j in α (0 ≤ j < w_α): π(v) = c₀ + w_β + w_μ + j, and M'(d)(c₀ + w_β + w_μ + j) = M(d)(c₀ + j) = M(d)(v) by R-S3.

For v = c₁ + j in μ (0 ≤ j < w_μ): π(v) = c₀ + w_β + j, and M'(d)(c₀ + w_β + j) = M(d)(c₁ + j) = M(d)(v) by R-S2.

For v = c₂ + j in β (0 ≤ j < w_β): π(v) = c₀ + j, and M'(d)(c₀ + j) = M(d)(c₂ + j) = M(d)(v) by R-S1.

Injectivity: within each case, the mapping is injective (the exterior is the identity; the α case maps distinct j to distinct c₀ + w_β + w_μ + j; the μ case maps distinct j to distinct c₀ + w_β + j; the β case maps distinct j to distinct c₀ + j). Across cases: the five image sets — {v ∈ dom(M(d)) : subspace(v) ≠ S}, V_S(d) \ [c₀, c₃), {c₀ + w_β + w_μ + j : 0 ≤ j < w_α}, {c₀ + w_β + j : 0 ≤ j < w_μ}, {c₀ + j : 0 ≤ j < w_β} — are pairwise disjoint (the first is disjoint from the rest by subspace separation; the remaining four are pairwise disjoint as shown in R-SWP). Surjectivity: π is an injection from dom(M(d)) into itself, and dom(M(d)) is finite (S8-fin of ASN-0036); on a finite set, every self-injection is a bijection, so π is surjective. ∎

The swap postcondition preserves dom(M(d)) (R-SWP), preserves C (R-FRAME-S(c)), and admits the bijection π satisfying M'(d)(π(v)) = M(d)(v) (R-SPERM); it therefore constitutes an arrangement rearrangement, and the invariant preservation established above applies.

We observe the structural relationship between the two forms: the 4-cut postcondition formulas (R-S1, R-S2, R-S3) reduce to the 3-cut formulas (R-P1, R-P2) when w_μ is set to zero in the expressions — R-S2 vanishes, and R-S3 becomes R-P2. However, the preconditions prevent this degenerate case from arising: CS2 requires c₁ < c₂, so w_μ ≥ 1. The two forms are distinct primitives. The 3-cut pivot transposes two *adjacent* regions; the 4-cut swap transposes two regions separated by at least one middle position.


## Sufficient Precondition

**R-SP — RearrangeSufficientPrecondition (LEMMA).** *Scope.* The lemma establishes sufficiency only (one direction, ⇐): the conjunction below is sufficient for the post-state predicate, not the weakest precondition. The necessity sketches below isolate three load-bearing conjuncts (R-PRE(i), R-PRE(iii), R-PRE(iv)) without claiming exhaustiveness. The proof uses R-BLK (RunDecompositionTransformation), whose output supplies the S8 witness B', and R-COMM (PermutationShiftCommutativity), the within-region shift-commutativity of π.

Let Q be the post-condition

> *M'(d) satisfies every ASN-0036 invariant carried by an arrangement transition — S0, S1, S2, S3, S4, S5, S7 (StructuralAttribution, ≡ S7a ∧ S7b ∧ S7d), S7a, S7b, S7d, D-CTG, D-CTG-depth, D-MIN, D-SEQ, S8a (VPositionWellFormedness), S8-fin, S8-depth, and S8 (CorrespondenceRunPartition) with its clauses S8-uniq (uniqueness of containing run) and S8-cons (consistency under M'(d)) — with the constructive witness B' = R-BLK(B) discharging the S8 existence clause: a correspondence-run partition of dom(M'(d)) under M'(d) obtained from the pre-state partition B of dom(M(d)) via Phases 1–3 on the V_S(d) portion (the runs in dom(M(d)) \ V_S(d), preserved pointwise by R-FRAME-P(a)/R-FRAME-S(a), carry over unchanged into B').*

Then

`wp(REARRANGE_K, Q) ⇐ R-PRE(K) ∧ ASN-0036-invariants(Σ, d) ∧ (B is a correspondence-run partition of dom(M(d)) under M(d))`

i.e., R-PRE on the cut sequence K, the full ASN-0036 invariant suite on the pre-state, and a designated pre-state partition B together suffice to establish the invariant suite on the post-state with B' as the constructive partition witness.

*Q is non-trivial.* Singleton-run partitions establish S8 existence on any finite arrangement (each (v, M'(d)(v), 1) satisfies S8-cons trivially at the lone offset k = 0), so "M'(d) admits *some* correspondence-run partition" alone is satisfied by *any* M'(d) and discriminates no rearrangements. Q strengthens this in two directions: (i) it requires the partition witness to be the *specific* output of R-BLK applied to B — a partition whose V-extents and I-starts are determined by Phases 1–3 from the pre-state partition, not an arbitrary post-hoc partition; and (ii) it requires the full ASN-0036 invariant conjunction on M'(d), which constrains the rearrangement globally (S2 functionality, S3 referential integrity, the dom-only invariants D-CTG/D-CTG-depth/D-MIN/D-SEQ/S8a/S8-fin/S8-depth, the content-store invariants S0/S1/S4/S5/S7a/S7b/S7d) rather than through S8 existence alone.

*Proof.* We discharge Q clause-by-clause, leaning on the prior derivations.

*S0, S1, S4, S7 (StructuralAttribution) with its sub-clauses S7a, S7b, S7d (content store invariants).* Each is stated on Σ.C alone and transports by identity via C-transport (Invariant preservation). S7 reduces to the conjunction S7a ∧ S7b ∧ S7d on Σ.C, so its preservation follows from that of its sub-clauses.

*S2 (arrangement functionality).* Each u ∈ dom(M'(d)) has u = π(v) for exactly one v by bijectivity of π (R-PPERM or R-SPERM), so M'(d)(u) = M(d)(v) is uniquely determined.

*S3 (referential integrity).* R-RI gives ran(M'(d)) ⊆ dom(C').

*S5 (unrestricted sharing).* The multiset-of-I-addresses preservation derived in the *Invariant preservation* paragraph above (each I-address has identical multiplicity in M(d) and M'(d) by bijectivity of π) preserves any pre-existing sharing pattern, and S5 imposes no positive constraint to violate.

*D-CTG, D-CTG-depth, D-MIN, D-SEQ, S8a (VPositionWellFormedness), S8-fin, S8-depth.* Each is a property of dom(M(d)) (V-positions, their counts, their subspace and depth, their ordinal arrangement), and dom(M'(d)) = dom(M(d)) from the rearrangement definition, so each carries over verbatim. D-CTG-depth is vacuous under this ASN's m_1 = 2 scope (text subspace at minimum depth).

*S8-uniq, S8-cons via B' = R-BLK(B).* R-BLK constructs B' from B via Phases 1–3 under R-PRE; we verify both S8-uniq and S8-cons on the construction. The verification handles V-positions in V_S(d) (the subspace REARRANGE acts on) and V-positions in subspaces other than S separately.

- *S8-uniq (uniqueness of containing run).* *Subspace-S case.* π is a bijection on V_S(d) (R-PPERM/R-SPERM restricted to V_S(d)). Phase 1 produces a partition of V_S(d) (each split preserves coverage and disjointness, by Split's V-extent decomposition); Phase 2 attaches a region label to each run without altering V-extents; Phase 3 applies π to V-starts only, preserving widths. For each reassembled run (π(v_j), a_j, n_j), its V-extent {π(v_j) + k : 0 ≤ k < n_j} coincides with the π-image of the original V-extent π(V(v_j, a_j, n_j)) = {π(v_j + k) : 0 ≤ k < n_j} by R-COMM (the same-region precondition discharged by Phase 1, which ensures each pre-reassembly run lies entirely within one region; thus π(v_j + k) = π(v_j) + k for 0 ≤ k < n_j). The image of a partition of V_S(d) under a bijection is again a partition of V_S(d) (disjointness from injectivity; coverage from surjectivity); combined with the V-extent identification just established via R-COMM, the V-extents of the reassembled runs are pairwise disjoint and cover V_S(d). Hence for each v ∈ V_S(d), exactly one such run contains v. *Non-S-subspace case.* Discharged by R-NS(NS-run) and (NS-inv): non-S runs in B carry verbatim into B', and the pre-state S8-uniq uniqueness on dom(M(d)) \ V_S(d) transports unchanged to M'(d). Combining both cases, the V-extents of B' partition dom(M'(d)) = dom(M(d)), discharging the E! quantification of S8-uniq on M'(d).
- *S8-cons (consistency under M'(d)).* *Subspace-S case.* For each reassembled run (π(v_j), a_j, n_j) ∈ B' arising from a subspace-S pre-run and 0 ≤ k < n_j: M'(d)(π(v_j) + k) = M'(d)(π(v_j + k)) (by R-COMM, valid because v_j and v_j + k lie in the same region after Phase 1) = M(d)(v_j + k) (by the defining property of π, given by R-PPERM or R-SPERM) = a_j + k (by S8-cons of the original run (v_j, a_j, n_j), supplied by B). Each equality discharges its precondition from R-PRE or from the pre-state S8 hypothesis. *Non-S-subspace case.* Discharged by R-NS(NS-run), whose post-state S8-cons consistency clause supplies M'(d)(v_j + k) = a_j + k for 0 ≤ k < n_j on every carried-over non-S run.

This completes the discharge of Q under the stated precondition. ∎

*Remark.* The sufficiency derivation makes explicit that R-BLK is the constructive witness for S8 on the post-state; R-PRE supplies cut-coverage (so Phase 1 is well-defined) and non-empty regions (so Phases 2–3 do not degenerate); pre-state S8 supplies the initial partition B that Phases 1 and 3 transform; pre-state ASN-0036 invariants supply the foundation S0–S3, S7, D-CTG, D-MIN, S8-fin, S8-depth that the post-state inherits via the transport arguments above. A stronger post-condition — that B' is the *canonical* (maximal) partition of M'(d) — is not derivable from R-PRE alone, and this gap is the source of post-rearrangement merges (R-BLK).

*Necessity sketch (R-PRE(iv) coverage).* We exhibit one concrete pre-state demonstrating that R-PRE(iv) is not gratuitous: dropping the coverage conjunct admits a configuration on which Q fails *even when the pre-state satisfies every ASN-0036 invariant*. The counterexample isolates R-PRE(iv) as a constraint on the cut sequence relative to V_S(d), distinct from the structural invariants D-CTG and D-SEQ that the foundation already supplies. *Pre-state.* Let V_S(d) = {[1, 1], [1, 2], [1, 3], [1, 4], [1, 5]} — a sequential V-position set satisfying D-CTG (no gaps), D-SEQ (contiguous ordinals starting at 1), and S8a (positive ordinals at depth 2) of ASN-0036. Take any arrangement M(d) defined on these five positions (the specific I-addresses are irrelevant to the analysis below); the pre-state run partition B exists and is valid by S8. Take the 3-cut sequence K = ([1, 2], [1, 4], [1, 100]) — satisfying CS1 (n = 3), CS2 ([1, 2] < [1, 4] < [1, 100] under T1's strict ordering on tumblers), CS3 (all subspace 1), and CS4 (all depth 2). *R-PRE(i)–(iii) hold; (iv) fails.* Clauses (i) and (ii) are immediate. Clause (iii) is just CS1–CS4, verified above. With w_α = ord(c₁) − ord(c₀) = 4 − 2 = 2 and w_β = ord(c₂) − ord(c₁) = 100 − 4 = 96 (each width derived from the cut ordinals alone), both are ≥ 1, but this is irrelevant to the analysis below — the failure does not depend on width arithmetic. The affected range [c₀, c_{n−1}) at depth 2 in subspace 1 covers ordinals {2, 3, ..., 99}, and positions [1, 6], [1, 7], ..., [1, 99] are absent from V_S(d) (which extends only to [1, 5]); the universal "(A v : subspace(v) = 1 ∧ #v = 2 ∧ c₀ ≤ v < c₂ : v ∈ V_S(d))" of R-PRE(iv) is therefore falsified at any such witness — e.g., at v = [1, 6]. *Q fails.* R-P1 with j = 2 demands M'(d)(c₀ + 2) = M(d)(c₁ + 2), i.e., M'(d)([1, 4]) = M(d)([1, 6]). The left-hand side is well-typed ([1, 4] ∈ V_S(d) ⊆ dom(M(d)) = dom(M'(d))), but [1, 6] ∉ dom(M(d)), so the right-hand side is undefined and the postcondition equation cannot be satisfied for any candidate M'(d). Equivalently, the well-definedness step (b) of R-PIV fails: R-P1's reference to M(d)(c₁ + j) for 0 ≤ j < w_β requires the source position to lie in dom(M(d)), and at j = 2 the source is [1, 6] ∉ dom(M(d)). The failure compounds at j = 3, 4, ..., 95 — both as missing source references (M(d)([1, 7]), ..., M(d)([1, 99])) and, beyond j = 3, as missing destination V-positions (M'(d)([1, 6]), ..., M'(d)([1, 97]) lie outside dom(M'(d)) = dom(M(d))) — but a single witness at j = 2 already refutes Q. The R-BLK partition witness clause of Q inherits the failure: Phases 1–2 still complete (c₀ and c₁ classify against B by the interior/boundary dispatch on V_S(d); c₂ = [1, 100] falls outside ⋃_k V(b_k) and is admitted by the "Outside ⋃_k V(b_k)" clause as the last cut), but Phase 3 has no valid M'(d) to reassemble against, since M'(d) is the very object whose well-definedness R-P1 just disqualified. *Why R-PRE(iv) is structural.* No ASN-0036 invariant is violated by the pre-state above; the only failure is R-PRE(iv). This isolates R-PRE(iv) as a constraint *on the cut sequence relative to V_S(d)* — specifically bounding c_{n−1} ≤ [S, N + 1] where N = max{ord(v) : v ∈ V_S(d)} (under the D-SEQ characterization V_S(d) = {[S, 1], ..., [S, N]}), and analogously bounding each non-last cut into V_S(d) by CS2 — rather than as a redundant restatement of D-CTG or D-SEQ. *Conclusion.* R-PRE(iv) is load-bearing: even with a well-formed pre-state arrangement, dropping it admits cut sequences on which R-P1 (and hence Q) cannot be satisfied.

*Well-typedness argument (R-PRE(iii) — CS3).* CS3 — the same-subspace clause of R-PRE(iii) — is a *well-typedness guard* on the postcondition: dropping it leaves the region widths and the β-extent untyped, so Q has no well-formed instance to evaluate. *Pre-state.* Let V_S(d) = {[1, 1], ..., [1, 5]} as before, and additionally suppose subspace 2 contains [2, 1] ∈ dom(M(d)) (S5 admits multi-subspace domains; the pre-state ASN-0036 invariants hold across both subspaces). Take the 3-cut sequence K = ([1, 2], [1, 5], [2, 1]). CS1 (n = 3), CS2 ([1, 2] < [1, 5] < [2, 1] under T1, the subspace coordinate 1 < 2 dominating at the last cut), and CS4 (all depth 2) hold; CS3 is *violated* — c₂ = [2, 1] is in subspace 2 while c₀, c₁ are in subspace 1. R-PRE(iv), which quantifies over *the* subspace S of the cuts, presupposes CS3 and is vacuous in its absence, so CS3 is the unique load-bearing failure. *Q is ill-typed.* Region β — the V-positions at depth 2 in subspace S with ordinal in [ord(c₁), ord(c₂)) — has no well-typed extent when its bounding cuts straddle subspaces: the cross-subspace interval [c₁, c₂) under T1 does not correspond to a region width in either subspace, so the iteration bound w_β in R-P1's reference M(d)(c₁ + j) is undefined and the rearrangement equation has no well-typed instances. The frame condition compounds this: R-FRAME-P(a) demands M'(d)([2, 1]) = M(d)([2, 1]) (treating subspace 2 as inert frame), yet c₂ = [2, 1] is simultaneously named as an arithmetic cut endpoint — a type-level mismatch. *Why CS3 is load-bearing.* No ASN-0036 invariant is violated by the pre-state; CS3 alone isolates the cut sequence to a single subspace so that the region widths w_α, w_β are well-typed and R-FRAME-P/S(a) is consistent with the cut-induced region partition.

*Remaining conjuncts (R-PRE(i), R-PRE(ii)).* R-PRE(i) — M(d) is well-defined — gates the source-side references M(d)(c_i + j) on the right-hand sides of R-P1/R-P2/R-S1/R-S2/R-S3; with M(d) undefined, no postcondition equation can be evaluated. R-PRE(ii) — V_S(d) ≠ ∅ — gates the existence of any cut position in subspace S (cuts have subspace S by CS3 and depth 2 by CS4, so under D-SEQ they are drawn from V_S(d) ∪ {[S, N + 1]}; with V_S(d) = ∅ the cut sequence cannot be formed at all). Both are guards on the well-typedness of the postcondition rather than on the body of the rearrangement, and we omit detailed counterexample constructions for them — the failure mode in each case is immediate from the postcondition definition rather than from a derived contradiction with the ASN-0036 invariants.

The arguments above establish the qualitative claim that R-PRE is non-redundant at its three load-bearing conjuncts (R-PRE(i), R-PRE(iii), R-PRE(iv)), with two distinct modes of indispensability: R-PRE(iv) is a *semantic* precondition (its negation admits a well-typed instance of Q that no M'(d) can satisfy), while R-PRE(i) and R-PRE(iii) are *well-typedness guards* (their negation makes Q unevaluable rather than unsatisfiable). A full necessity proof — characterizing the weakest precondition exhaustively, with the well-typedness/semantic distinction made formal — is left as the open question recorded above.


## Displacement Analysis

The permutations R-PPERM and R-SPERM can be characterized by ordinal displacements — how far each position moves within its subspace. These displacements illuminate the structure and connect to the correspondence-run decomposition transformation.

**Definition — PermutationDisplacement.** For a position v ∈ dom(M(d)), define Δ(v) as a signed magnitude `(σ, n) ∈ {+, −, 0} × ℕ` capturing the ordinal shift induced by π. The carrier is a pair to avoid relying on a signed integer type that the foundation does not provide; the truncated subtraction defined above suffices once direction is recorded by σ and the operands are restricted to a domain on which it is well-typed. The cases are:

```
Δ(v) = (0, 0)                               if subspace(v) ≠ S                                (non-S convention)
Δ(v) = (0, 0)                               if v ∈ V_S(d) and π(v) = v                       (S-exterior / fixed)
Δ(v) = (+, ord(π(v)) − ord(v))              if v ∈ V_S(d) and ord(π(v)) > ord(v)             (S, forward shift)
Δ(v) = (−, ord(v) − ord(π(v)))              if v ∈ V_S(d) and ord(π(v)) < ord(v)             (S, backward shift)
```

The explicit `v ∈ V_S(d)` guard on the (+) and (−) branches is the domain condition that keeps the truncated subtraction (defined above) well-typed: on V_S(d), depth-2 ordinals are singleton tumblers (identified with positive naturals under the singleton-tumbler identification introduced above), so the strict T1 ordering `ord(π(v)) > ord(v)` or `ord(π(v)) < ord(v)` reduces to strict ordering on positive naturals, and the corresponding `ord(π(v)) − ord(v)` and `ord(v) − ord(π(v))` are truncated-subtraction applications on naturals (its defined domain). The non-S convention `Δ(v) = (0, 0)` on `subspace(v) ≠ S` is consistent with the (S-exterior / fixed) clause because R-PPERM and R-SPERM both fix every non-S position (R-NS(NS-π)). We write `+n` for `(+, n)`, `−n` for `(−, n)`, and `0` for `(0, 0)` when no ambiguity arises.

*Canonical form.* The only values produced by the case analysis are (0, 0), (+, n) with n ≥ 1, and (−, n) with n ≥ 1. The (+) branch fires only when ord(π(v)) > ord(v), so n = ord(π(v)) − ord(v) ≥ 1; the (−) branch fires only when ord(v) > ord(π(v)), so n = ord(v) − ord(π(v)) ≥ 1; the (0, 0) branch fires when subspace(v) ≠ S or when π(v) = v. We say Δ(v₁) = Δ(v₂) when their canonical forms are componentwise equal (same σ and same n); the canonical-form restriction makes equality unambiguous (no two distinct case-analysis outputs share a carrier representation).

*Exhaustiveness and mutual exclusivity.* For non-S positions (subspace(v) ≠ S), the non-S clause fires uniquely; the (S-exterior / fixed) and (+)/(−) clauses are excluded by their `v ∈ V_S(d)` guard. For V_S(d) positions, ord is a single-component tumbler, so T1 trichotomy on (ord(π(v)), ord(v)) yields exactly one of ord(π(v)) = ord(v), ord(π(v)) > ord(v), or ord(π(v)) < ord(v) — discharging exactly one of the three V_S(d) clauses and excluding the other two. The four clauses are therefore exhaustive and mutually exclusive across dom(M(d)). (R-PPERM/R-SPERM additionally guarantee that for non-S v, π(v) = v, so the value Δ(v) = (0, 0) supplied by the non-S clause agrees with what the (S-exterior / fixed) clause would yield if its guard were relaxed; the two clauses agree on their overlap and the definition is consistent.)

We do *not* define addition, multiplication, or an ordering on the signed-magnitude carrier in this ASN; Δ-values are compared only by equality, never by summation or comparison.

On the exterior, π(v) = v, so Δ(v) = 0.

For the 3-cut pivot, from R-PPERM:

```
Δ(v) = +w_β      if v ∈ α     (shifts forward by width of β)
Δ(v) = −w_α      if v ∈ β     (shifts backward by width of α)
Δ(v) = 0         otherwise
```

For the 4-cut swap, from R-SPERM:

```
Δ(v) = +(w_β + w_μ)        if v ∈ α   (shifts forward past middle and β)
Δ(v) on μ                              if v ∈ μ   (determined by case analysis on w_β vs w_α; see formal cases below)
Δ(v) = −(w_α + w_μ)        if v ∈ β   (shifts backward past middle and α)
Δ(v) = 0                   otherwise
```

The μ case splits on the comparison of w_β and w_α (both ∈ ℕ⁺): when w_β > w_α, Δ(v) = +(w_β − w_α); when w_β < w_α, Δ(v) = −(w_α − w_β); when w_β = w_α, Δ(v) = 0. Each branch invokes the truncated subtraction on its defined domain.

The displacement formulation makes it clear that every position in the affected range shifts by a value determined solely by the region widths — the displacement does not depend on the position's location within its region. All positions in α shift by the same amount; all positions in β shift by the same amount. We state this formally:

**R-DISP — DisplacementUniformity (LEMMA).** Let C be a cut sequence satisfying R-PRE, and let π be the permutation from R-PPERM (3-cut) or R-SPERM (4-cut). For all v₁, v₂ in the same region — where the regions partition dom(M(d)) into the non-S domain {v ∈ dom(M(d)) : subspace(v) ≠ S}, the subspace-S exterior {v ∈ V_S(d) : v < c₀ or v ≥ c_{n−1}}, α, β, and (for 4-cut) μ:

`Δ(v₁) = Δ(v₂)`

with the common value given by: Δ = 0 on the non-S domain (π is the identity off V_S(d) by R-PPERM/R-SPERM); for 3-cut, Δ = +w_β on α, Δ = −w_α on β, Δ = 0 on the subspace-S exterior; for 4-cut, Δ = +(w_β + w_μ) on α, Δ = −(w_α + w_μ) on β, Δ = 0 on the subspace-S exterior, and on μ the three sub-cases are Δ = +(w_β − w_α) when w_β > w_α, Δ = −(w_α − w_β) when w_β < w_α, and Δ = 0 when w_β = w_α.

*Proof.* The result follows from the explicit R-PPERM and R-SPERM formulas, in which the offset j within a region cancels. We show each region; each case identifies the sign of ord(π(v)) − ord(v) before applying the truncated subtraction on its defined domain.

*Non-S domain (both forms):* For v ∈ dom(M(d)) with subspace(v) ≠ S, Δ(v) = 0 directly by the non-S clause of the definition. (R-NS(NS-π) additionally gives π(v) = v, which is consistent with — but not required for — the value.)

*Subspace-S exterior (both forms):* v ∈ V_S(d) and π(v) = v, so the (S-exterior / fixed) clause applies and Δ(v) = 0.

*3-cut α:* For v = c₀ + j with 0 ≤ j < w_α: π(v) = c₀ + w_β + j, so ord(π(v)) = ord(c₀) + w_β + j and ord(v) = ord(c₀) + j. Since w_β ≥ 1, ord(π(v)) > ord(v); the (+) branch applies, giving Δ(v) = +((ord(c₀) + w_β + j) − (ord(c₀) + j)) = +w_β.

*3-cut β:* For v = c₁ + j with 0 ≤ j < w_β: π(v) = c₀ + j, so ord(π(v)) = ord(c₀) + j and ord(v) = ord(c₁) + j = ord(c₀) + w_α + j. Since w_α ≥ 1, ord(v) > ord(π(v)); the (−) branch applies, giving Δ(v) = −((ord(c₀) + w_α + j) − (ord(c₀) + j)) = −w_α.

*4-cut α:* For v = c₀ + j with 0 ≤ j < w_α: π(v) = c₀ + w_β + w_μ + j, so ord(π(v)) = ord(c₀) + w_β + w_μ + j and ord(v) = ord(c₀) + j. Since w_β + w_μ ≥ 2, ord(π(v)) > ord(v); the (+) branch applies, giving Δ(v) = +(w_β + w_μ).

*4-cut μ:* For v = c₁ + j with 0 ≤ j < w_μ: π(v) = c₀ + w_β + j, so ord(π(v)) = ord(c₀) + w_β + j and ord(v) = ord(c₁) + j = ord(c₀) + w_α + j. The comparison of ord(π(v)) and ord(v) reduces to the comparison of w_β and w_α. When w_β > w_α: (+) branch, Δ(v) = +(w_β − w_α). When w_β < w_α: (−) branch, Δ(v) = −(w_α − w_β). When w_β = w_α: ord(π(v)) = ord(v), Δ(v) = 0. In all three sub-cases, j cancels.

*4-cut β:* For v = c₂ + j with 0 ≤ j < w_β: π(v) = c₀ + j, so ord(π(v)) = ord(c₀) + j and ord(v) = ord(c₂) + j = ord(c₀) + w_α + w_μ + j. Since w_α + w_μ ≥ 2, ord(v) > ord(π(v)); the (−) branch applies, giving Δ(v) = −(w_α + w_μ).

In every case, j cancels and the common value depends only on region widths. ∎


## Correspondence-Run Decomposition Transformation

We recall from S8 (CorrespondenceRunPartition, ASN-0036) that for every v ∈ dom(M(d)) there exists a unique correspondence run (v_s, a_s, n) with v ∈ {v_s + k : 0 ≤ k < n} and M(d)(v_s + k) = a_s + k for all 0 ≤ k < n. Equivalently, S8 yields a finite partition of dom(M(d)) into correspondence runs. We layer three new operations (Split, Merge, and a canonical decomposition) over the foundation's runs. Throughout this section, when we say *run* we mean a correspondence run (v, a, n) with n ≥ 1, and write V(v, a, n) = {v + k : 0 ≤ k < n} for its V-extent. To avoid colliding with the foundation's own clause lettering (where S8's postconditions are (a) lockstep consistency, (b) well-defined label, (c) unique decomposition), we name two local labels: *S8-uniq* for the uniqueness-of-containing-run guarantee (the foundation's clause (c), restated per-position) and *S8-cons* for the consistency clause M(d)(v + k) = a + k (the foundation's clause (a)).

**Split.** Given a run b = (v, a, n) under some arrangement A and an interior offset c with 1 ≤ c < n, the *split* at c produces two runs: (v, a, c) and (v + c, a + c, n − c). Their V-extents (ordinal ranges [ord(v), ord(v) + c) and [ord(v) + c, ord(v) + n)) are disjoint and partition b's V-extent.

Both pieces inherit S8-cons (consistency under A). For the first piece (v, a, c), we need A(v + k) = a + k for 0 ≤ k < c; this holds by restricting the original S8-cons to the subrange k < c < n. For the second piece (v + c, a + c, n − c), we need A((v + c) + k) = (a + c) + k for 0 ≤ k < n − c. When k ≥ 1, associativity (TS3) gives (v + c) + k = v + (c + k); when k = 0, (v + c) + 0 = v + c by the identity convention. In both cases, c + k < n, so the original S8-cons yields A(v + (c + k)) = a + (c + k). The same associativity/identity argument gives (a + c) + k = a + (c + k), completing the derivation: A((v + c) + k) = a + (c + k) = (a + c) + k. The proof is arrangement-parametric: it uses only S8-cons of the original run and TS3, with no property specific to a particular arrangement.

**Merge.** Two runs (v₁, a₁, n₁) and (v₂, a₂, n₂) under arrangement A are *mergeable* when v₂ = v₁ + n₁ (V-adjacent) and a₂ = a₁ + n₁ (I-adjacent). The merged run is (v₁, a₁, n₁ + n₂). We verify S8-cons for the merged run — that A(v₁ + k) = a₁ + k for 0 ≤ k < n₁ + n₂ — by two cases. For 0 ≤ k < n₁: this is S8-cons of the first run directly. For n₁ ≤ k < n₁ + n₂: write k = n₁ + k' with 0 ≤ k' < n₂. When k' ≥ 1, TS3 gives v₁ + k = v₁ + (n₁ + k') = (v₁ + n₁) + k' = v₂ + k'; when k' = 0, v₁ + n₁ = v₂ by the adjacency condition. By S8-cons of the second run, A(v₂ + k') = a₂ + k'. The same associativity/identity argument gives a₁ + k = a₁ + (n₁ + k') = (a₁ + n₁) + k' = a₂ + k', so A(v₁ + k) = a₂ + k' = a₁ + k. As with Split, this proof is arrangement-parametric: it depends only on S8-cons of the two constituents and TS3. In particular, when R-BLK applies Merge to the post-rearrangement arrangement M'(d), the verification holds because the reassembled runs already satisfy S8-cons for M'(d) (established in Phase 3).

**Canonical decomposition.** The *canonical run decomposition* of M(d) is the partition of dom(M(d)) into *maximal* runs — runs that cannot be extended by merging with a V-adjacent, I-adjacent neighbor. Existence and uniqueness of this maximal-run partition are established by the foundation, not here: S8 (CorrespondenceRunPartition, ASN-0036) states directly that the maximal runs partition dom(Σ.M(d)) and that the maximal-run decomposition is unique. We do not re-establish those two facts. What R-BLK additionally requires — and what S8 does not address — is the connection between that S8-unique partition and the *exhaustive-Merge process* built from the Split and Merge operations introduced in this ASN: that the process terminates and is confluent, reaching the S8 partition regardless of merge order. Steps (a)–(d) below supply this operational connection over the new operations; wherever maximal-partition uniqueness itself is invoked (notably the conclusion of step (b) and its uses), it is the uniqueness already exported by S8 (ASN-0036).

*Scope of this analysis.* We analyze the maximal runs whose V-positions lie in V_S(d) — the runs that REARRANGE can possibly affect. Runs whose V-positions lie in subspaces other than S are preserved pointwise by R-FRAME-P(a) / R-FRAME-S(a) and play no role in the analysis below; references to "v ∈ dom(M(d))" in steps (a)–(d) are read under the additional restriction subspace(v) = S, equivalently v ∈ V_S(d). The argument we give is *agnostic* to whether dom(M(d)) contains positions in other subspaces.
 
*Existence of a maximum (helper lemma).* For any non-empty S ⊆ {0, 1, ..., B} ⊆ ℕ with B ∈ ℕ, max(S) exists. *Proof.* Let U = {u ∈ ℕ : (A s ∈ S : s ≤ u)} be the set of upper bounds of S in ℕ. Every s ∈ S satisfies s ≤ B, so B ∈ U and U is non-empty; by NAT-wellorder (ASN-0034) U has a least element m = min(U). We show m ∈ S, whence m = max(S). Suppose for contradiction m ∉ S. Fix any s₀ ∈ S (S non-empty); since m ∈ U we have s₀ ≤ m, and s₀ ≠ m because s₀ ∈ S while m ∉ S, so s₀ < m by NAT-order trichotomy (ASN-0034). Hence m ≥ 1 (as 0 ≤ s₀ < m). Let m − 1 denote the predecessor of m — the unique j ∈ ℕ with shift([j], 1) = [m] under the singleton-tumbler identification (it exists because m ≥ 1; it is the truncated subtraction defined above). By construction (m − 1) + 1 = m, and m − 1 < m by TS4 (ShiftStrictIncrease, ASN-0034). For every s ∈ S the same trichotomy argument gives s < m, hence s + 1 ≤ m = (m − 1) + 1 by NAT-discrete (ASN-0034). Under the singleton identification, s + 1 ≤ (m − 1) + 1 reads shift([s], 1) ≤ shift([m − 1], 1); were s > m − 1, TS1 (ShiftOrderPreservation, ASN-0034) would give shift([m − 1], 1) < shift([s], 1), contradicting the inequality — so s ≤ m − 1 by T1 trichotomy. Thus m − 1 is an upper bound of S with m − 1 < m, contradicting the minimality of m in U. Therefore m ∈ S, and max(S) = m exists. We invoke this lemma once each below for f(v) and r(v); both invocations supply the bound B explicitly.
 
*(a) The maximal run containing any v ∈ V_S(d) is uniquely determined.* Fix v ∈ V_S(d). Define the *forward extent* f(v) = max{k ≥ 0 : (A j : 0 ≤ j ≤ k : v + j ∈ V_S(d) ∧ M(d)(v + j) = M(d)(v) + j)}. The defining set is non-empty (k = 0 works: v + 0 = v by the identity convention, v ∈ V_S(d) by assumption, and M(d)(v) = M(d)(v) + 0 by the identity convention again). By D-SEQ (ASN-0036), V_S(d) = {[S, 1], ..., [S, N]} for some N ∈ ℕ (the maximum ordinal in V_S(d), finite by S8-fin). Any k in the defining set satisfies v + k ∈ V_S(d), so ord(v + k) = ord(v) + k ≤ N (TS3 plus the identity convention), giving k ≤ N − ord(v). The defining set is therefore a non-empty subset of {0, 1, ..., N − ord(v)} ⊆ ℕ, bounded above by N − ord(v); existence of a maximum follows from the helper lemma above with B = N − ord(v). Define the *backward extent* r(v) = max{k ≥ 0 : [S, ord(v) − k] ∈ V_S(d) ∧ (A i : 0 ≤ i ≤ k : M(d)([S, ord(v) − k + i]) = shift(M(d)([S, ord(v) − k]), i))}, where the identity convention covers i = 0 and OrdinalShift applies for i ≥ 1. The defining set is non-empty (k = 0 works: [S, ord(v)] = v ∈ V_S(d), and the inner conjunct is vacuous/identity at i = 0). Any k in the defining set satisfies [S, ord(v) − k] ∈ V_S(d), so ord(v) − k ≥ 1 (S8a, ASN-0036), giving k ≤ ord(v) − 1. The defining set is therefore a non-empty subset of {0, 1, ..., ord(v) − 1} ⊆ ℕ, bounded above by ord(v) − 1; existence of a maximum again follows from the helper lemma with B = ord(v) − 1. The membership requirement [S, ord(v) − k] ∈ V_S(d) demands ord(v) − k ≥ 1 (since V-positions have positive ordinals by S8a) and is checked at the tentative start; for each intermediate offset i with 0 ≤ i ≤ k, the position [S, ord(v) − k + i] lies in V_S(d) automatically. To see this, note v ∈ V_S(d) gives ord(v) ∈ {1, ..., N} where V_S(d) = {[S, j] : 1 ≤ j ≤ N} by D-SEQ (ASN-0036), and [S, ord(v) − k] ∈ V_S(d) gives ord(v) − k ≥ 1; the intermediate ordinals ord(v) − k + i lie in [ord(v) − k, ord(v)] ⊆ [1, N], so [S, ord(v) − k + i] ∈ V_S(d). The inner consistency conjunct in r(v) is therefore well-formed at every offset. This formulation checks S8-cons forward from the tentative run start [S, ord(v) − k], avoiding subtraction on I-addresses. Both f(v) and r(v) are determined by M(d) and v alone — M(d) is a function (S2), so for each candidate position the correspondence either holds or does not, with no ambiguity. Writing v_s = [S, ord(v) − r(v)] for the start position, the maximal run containing v is (v_s, M(d)(v_s), r(v) + 1 + f(v)), and it is uniquely determined by the values of r(v) and f(v).

*Maximality of the constructed run.* The run (v_s, M(d)(v_s), r(v) + 1 + f(v)) is maximal in the canonical-partition sense — no V-adjacent, I-adjacent extension is admissible. *Forward extension impossible:* extending the run to length r(v) + 2 + f(v) would require a forward offset f(v) + 1 with v + (f(v) + 1) ∈ V_S(d) and M(d)(v + (f(v) + 1)) = M(d)(v) + (f(v) + 1), so f(v) + 1 would lie in the defining set of f(v); but f(v) was chosen as the maximum of that set (helper lemma), so f(v) + 1 ≤ f(v), contradiction. *Backward extension impossible:* extending the run by one position to the left would require a backward offset r(v) + 1 with [S, ord(v) − r(v) − 1] ∈ V_S(d) and the inner forward-consistency conjunct holding from this new start, so r(v) + 1 would lie in the defining set of r(v); but r(v) was chosen as the maximum of that set, so r(v) + 1 ≤ r(v), contradiction. Hence no strict extension of the run exists, and the run is maximal. This maximality conclusion is the property that the merge-order argument (c) depends on.

*(b) Two maximal runs sharing a V-position are identical.* This is exactly S8's uniqueness of the maximal-run decomposition (ASN-0036): the maximal runs partition dom(Σ.M(d)), so distinct maximal runs have disjoint V-extents and cannot share a V-position. We do not re-derive it. What the merge-order argument (c) below consumes is only that every terminal partition of the exhaustive-Merge process consists of maximal runs (established in (c)), after which S8 closes uniqueness.

*(c) Merge-order independence.* Start from any partition of V_S(d) into runs (existence guaranteed by S8, restricted to subspace S; runs in other subspaces are unaffected). The exhaustive merge process repeatedly finds a mergeable pair and merges them, reducing the run count by one. Termination: V_S(d) is finite (S8-fin), so the initial run count is finite, and each merge strictly reduces it, so the process terminates.
 
*Partition invariant maintained through merges.* At each step of the merge process, the current collection is a partition of V_S(d) into valid runs (pairwise-disjoint V-extents covering V_S(d), with each run satisfying S8-cons under M(d)). Initially this holds by S8. Each merge step replaces two runs b₁ = (v₁, a₁, n₁) and b₂ = (v₂, a₂, n₂) — satisfying v₂ = v₁ + n₁ and a₂ = a₁ + n₁ — with the single run b₁₂ = (v₁, a₁, n₁ + n₂). The merged run b₁₂ is valid by the Merge lemma. Its V-extent equals V(b₁) ∪ V(b₂) (a contiguous range by V-adjacency), so coverage is preserved; disjointness from every other run b' in the collection is inherited because V(b₁) and V(b₂) were each already disjoint from V(b') by the prior partition property. Hence the post-merge collection is again a partition of V_S(d) into valid runs, and the disjointness arguments invoked below apply at every stage of the merge process.
 
At termination, no mergeable pair remains — we show every run is maximal by establishing that any non-maximal run has a V-adjacent, I-adjacent partition neighbor.

*Strict extension (definition).* A *strict extension* of run b = (v_b, a_b, n_b) is a valid correspondence run b* = (v_s*, a_s*, n_s*) under M(d) — meaning v_s* ∈ V_S(d), n_s* ≥ 1, every v_s* + k for 0 ≤ k < n_s* lies in V_S(d), and M(d)(v_s* + k) = a_s* + k — with V(b*) ⊋ V(b) (V-extent strict containment). A run b is *maximal* iff no strict extension of b exists. We use "strict extension" exclusively in this sense below.
 
Suppose, toward contradiction, that some run b = (v_b, a_b, n_b) in the terminal partition is non-maximal. By the definition of maximality, b admits a strict extension as a valid correspondence run — either *forward* (a length n_b' > n_b run sharing V-start v_b, witnessing v_b + n_b ∈ V_S(d) with M(d)(v_b + n_b) = a_b + n_b) or *backward* (a run with V-start v_s such that ord(v_s) < ord(v_b), witnessing [S, ord(v_b) − 1] ∈ V_S(d) with shift(M(d)([S, ord(v_b) − 1]), 1) = a_b).

*Exhaustiveness of the forward/backward dichotomy.* Any valid correspondence run b* = (v_s*, a_s*, n_s*) whose V-extent V(b*) = [ord(v_s*), ord(v_s*) + n_s*) strictly contains V(b) = [ord(v_b), ord(v_b) + n_b) — the definition of "strict extension" — must satisfy ord(v_s*) ≤ ord(v_b) and ord(v_s*) + n_s* ≥ ord(v_b) + n_b, with at least one inequality strict. If ord(v_s*) < ord(v_b), b* is a backward extension (and its consistency at offset ord(v_b) − ord(v_s*) − 1, applied to its predecessor at [S, ord(v_b) − 1], witnesses shift(M(d)([S, ord(v_b) − 1]), 1) = a_b via S8-cons). Otherwise ord(v_s*) = ord(v_b), so v_s* = v_b (by S8a and D-SEQ, ord uniquely identifies V-positions within V_S(d) under the singleton-tumbler identification); the strict-containment requirement then forces n_s* > n_b, and S8-cons of b* at offset n_b witnesses v_b + n_b ∈ V_S(d) and M(d)(v_b + n_b) = a_b + n_b — a forward extension. The two cases are exhaustive and disjoint. We dispatch on the two directions and derive a contradiction in each.

*Forward extension.* Suppose v_b + n_b ∈ V_S(d) and M(d)(v_b + n_b) = a_b + n_b (witnessed by some forward extension b' = (v_b, a_b, n_b') with n_b' > n_b, whose S8-cons at offset n_b supplies this membership and I-address). The singleton b'' = (v_b + n_b, a_b + n_b, 1) is a valid length-1 run (S8-cons holds trivially at offset 0), V-adjacent to b (its V-start equals v_b + n_b) and I-adjacent to b (its I-start equals a_b + n_b).

Now let c = (v_c, a_c, n_c) be the (unique) partition run with v_b + n_b ∈ V(c); existence follows because the partition (of V_S(d)) covers v_b + n_b ∈ V_S(d). We show v_c = v_b + n_b. Since v_b + n_b ∈ V(c), we have v_b + n_b = v_c + k_c for some 0 ≤ k_c < n_c. Suppose for contradiction that k_c ≥ 1, i.e., ord(v_c) < ord(v_b + n_b) = ord(v_b) + n_b. Then by S8-uniq applied to c, the position v_c + (k_c − 1) = v_b + (n_b − 1) lies in V(c); but v_b + (n_b − 1) also lies in V(b) (offset n_b − 1 < n_b). Partition disjointness — distinct partition runs have disjoint V-extents (maintained as a partition invariant through merges, established above) — forces b = c. Under b = c, we have v_c = v_b and n_c = n_b, so v_b + n_b = v_c + k_c = v_b + k_c, and TS5 gives n_b = k_c (using n_b ≥ 1 from S8 and k_c ≥ 1 from the contradiction assumption: the contrapositive of TS5 (ShiftAmountMonotonicity, ASN-0034) on a common base v_b extracts equality of shift amounts from equality of shift outputs); but k_c < n_c = n_b gives n_b < n_b, contradiction. Hence k_c = 0 and v_c = v_b + n_b. Finally, S8-cons of c at offset 0 gives a_c = M(d)(v_c) = M(d)(v_b + n_b) = a_b + n_b. Thus c has V-start v_b + n_b (V-adjacent to b) and I-start a_b + n_b (I-adjacent to b), so (b, c) is a mergeable pair — contradicting the assumption that no mergeable pair remains.

*Backward extension.* Suppose [S, ord(v_b) − 1] ∈ V_S(d) and shift(M(d)([S, ord(v_b) − 1]), 1) = a_b. Let c = (v_c, a_c, n_c) be the (unique) partition run with [S, ord(v_b) − 1] ∈ V(c); existence follows from partition coverage of V_S(d). Write [S, ord(v_b) − 1] = v_c + k_c for some 0 ≤ k_c < n_c, so ord(v_c) + k_c = ord(v_b) − 1 and hence v_c + (k_c + 1) = v_b. We show n_c = k_c + 1 (V-adjacency v_c + n_c = v_b). Suppose for contradiction that n_c > k_c + 1; then v_c + (k_c + 1) = v_b lies in V(c) by S8-uniq. But v_b also lies in V(b) (offset 0). Partition disjointness forces b = c, contradicting ord(v_c) ≤ ord(v_b) − 1 < ord(v_b). Hence n_c = k_c + 1. For I-adjacency a_c + n_c = a_b: S8-cons of c at offset k_c gives M(d)([S, ord(v_b) − 1]) = a_c + k_c, so shift(a_c + k_c, 1) = a_b. By TS3 (when k_c ≥ 1) or the identity convention (when k_c = 0), shift(a_c + k_c, 1) = a_c + (k_c + 1) = a_c + n_c. Therefore a_c + n_c = a_b, and (c, b) is a mergeable pair — contradicting the assumption that no mergeable pair remains.

In both directional cases we derive a contradiction. Therefore every run in the terminal partition is maximal.

By S8's uniqueness of the maximal-run decomposition (ASN-0036), the partition into maximal runs is unique, so every termination state is the same partition regardless of merge order.

*(d) Maximal runs admit no merge.* Two maximal runs cannot be simultaneously V-adjacent and I-adjacent: if b₁ = (v₁, a₁, n₁) and b₂ = (v₂, a₂, n₂) satisfy v₂ = v₁ + n₁ and a₂ = a₁ + n₁, then (v₁, a₁, n₁ + n₂) is a valid run (by Merge) whose V-extent strictly contains V(b₁), contradicting b₁'s maximality. This is precisely the condition checked in (c) — at termination, no such pair exists, confirming that the exhaustive merge reaches the maximal-run partition.

**R-COMM — PermutationShiftCommutativity (LEMMA).** Let π be a cut-point permutation (R-PPERM or R-SPERM) for a cut sequence K satisfying R-PRE. For any V-position v ∈ dom(M(d)) and offset k ≥ 0 such that v + k ∈ dom(M(d)) and v, v + k lie in the same region — where the regions are the non-S subspace ({v ∈ dom(M(d)) : subspace(v) ≠ S}), the subspace-S exterior, α, μ, or β:

`π(v + k) = π(v) + k`

In words: the cut-point permutation commutes with ordinal shift within each region. Every position in a region receives the same ordinal displacement, so shifting within the region before or after applying π yields the same result.

*Proof.* We verify each region case using the explicit R-PPERM and R-SPERM formulas, with associativity of natural-number addition at the ordinal level as the sole algebraic tool. In each subspace-S case, the same-region hypothesis bounds the shifted offset j' + k inside the region's width, justifying application of the corresponding R-PPERM or R-SPERM branch.

*Non-S subspace (both forms):* For v with subspace(v) ≠ S, the same-region hypothesis places v + k in the non-S subspace as well — by OrdShiftHom (b) of ASN-0036, subspace(v + k) = subspace(v) ≠ S, so v + k automatically inherits the non-S region. By R-NS(NS-π) applied at v and at v + k, π(v) = v and π(v + k) = v + k, so π(v + k) = v + k = π(v) + k.

*Subspace-S exterior (both forms):* π(v + k) = v + k = π(v) + k, since π is the identity on the exterior.

*3-cut α:* v = c₀ + j' for some 0 ≤ j' < w_α. The same-region hypothesis "v + k ∈ α" places v + k = c₀ + (j' + k) with 0 ≤ j' + k < w_α (because α is defined as {c₀ + i : 0 ≤ i < w_α}, and the bijection between α's positions and offsets in [0, w_α) is supplied by the singleton-tumbler identification of V-positions with their ordinals). This bound discharges R-PPERM's α-branch precondition, yielding π(v + k) = c₀ + w_β + (j' + k). Also π(v) + k = (c₀ + w_β + j') + k = c₀ + w_β + (j' + k) by associativity (Extended Associativity, recorded in the OrdinalShift consumers list).

*3-cut β:* v = c₁ + j' for some 0 ≤ j' < w_β. The same-region hypothesis "v + k ∈ β" gives 0 ≤ j' + k < w_β, discharging R-PPERM's β-branch precondition. Then v + k = c₁ + (j' + k), and by R-PPERM: π(v + k) = c₀ + (j' + k). Also π(v) + k = (c₀ + j') + k = c₀ + (j' + k) by associativity.

*4-cut α:* v = c₀ + j' for some 0 ≤ j' < w_α. The same-region hypothesis "v + k ∈ α" gives 0 ≤ j' + k < w_α, discharging R-SPERM's α-branch precondition. Then v + k = c₀ + (j' + k), and by R-SPERM: π(v + k) = c₀ + w_β + w_μ + (j' + k). Also π(v) + k = (c₀ + w_β + w_μ + j') + k = c₀ + w_β + w_μ + (j' + k) by associativity.

*4-cut μ:* v = c₁ + j' for some 0 ≤ j' < w_μ. The same-region hypothesis "v + k ∈ μ" gives 0 ≤ j' + k < w_μ, discharging R-SPERM's μ-branch precondition. Then v + k = c₁ + (j' + k), and by R-SPERM: π(v + k) = c₀ + w_β + (j' + k). Also π(v) + k = (c₀ + w_β + j') + k = c₀ + w_β + (j' + k) by associativity.

*4-cut β:* v = c₂ + j' for some 0 ≤ j' < w_β. The same-region hypothesis "v + k ∈ β" gives 0 ≤ j' + k < w_β, discharging R-SPERM's β-branch precondition. Then v + k = c₂ + (j' + k), and by R-SPERM: π(v + k) = c₀ + (j' + k). Also π(v) + k = (c₀ + j') + k = c₀ + (j' + k) by associativity. ∎

**R-BLK — RunDecompositionTransformation (LEMMA).** R-BLK names both the lemma below and the constructive transformation (B, C, M(d), M'(d)) ↦ B' it specifies; R-SP invokes the latter via R-BLK(B). Let B = {b₁, ..., bₘ} be a run partition of M(d) (per S8) — including runs whose V-extents lie in V_S(d) and runs whose V-extents lie in subspaces other than S. Let the cut sequence K have cut positions c₀, ..., c_{n−1}. The rearranged arrangement M'(d) admits a run partition B' obtained by:

*Scope note on non-S runs.* The non-S behaviour through all three Phases is supplied by R-NS(NS-run): for any run b ∈ B with V-extent in some subspace S' ≠ S, Phase 1 performs no split (cuts have subspace S by CS3, disjoint from S'), Phase 2 classifies b into the dedicated non-S region, and Phase 3 carries the triple (v_b, a_b, n_b) through unchanged into B'. The Phase clauses below state explicitly where this dispatch fires, but the substantive verification — V-extent confinement to S' by OrdShiftHom (b) of ASN-0036, post-state S8-cons consistency under M'(d) via R-NS(NS-π), and pairwise disjointness from subspace-S runs by T10 of ASN-0034 — is recorded once in R-NS and not repeated.

*Phase 1: Split.* Process cut positions in index order (c₀, c₁, ..., c_{n−1}), maintaining the partition as it is progressively refined. For each cut position cᵢ, classify by whether cᵢ falls within some run's V-extent:

- *Interior of a run:* if cᵢ ∈ V(bₖ) for some bₖ = (vₖ, aₖ, nₖ) with cᵢ ≠ vₖ, split bₖ at the offset c = ord(cᵢ) − ord(vₖ), producing (vₖ, aₖ, c) and (vₖ + c, aₖ + c, nₖ − c). The two new runs partition the V-extent of the original.
- *Boundary of a run:* if cᵢ ∈ V(bₖ) and cᵢ = vₖ, no split is needed — the cut already coincides with a run boundary.
- *Outside ⋃_k V(bₖ):* no split is performed. This occurs only for the last cut c_{n−1} when c_{n−1} ∉ V_S(d). The case is justified by three steps. *(1) Every cᵢ with 0 ≤ i ≤ n − 2 lies in [c₀, c_{n−1}).* By CS2, c₀ < c₁ < ... < c_{n−1}, so for each i with 0 ≤ i ≤ n − 2 we have c₀ ≤ cᵢ < c_{n−1}, placing cᵢ in [c₀, c_{n−1}). *(2) Each such cᵢ lies in V_S(d).* By CS3, subspace(cᵢ) = S; by CS4, #cᵢ = 2 (depth-2 in subspace S). Combined with c₀ ≤ cᵢ < c_{n−1}, R-PRE(iv) — which quantifies over every position with subspace S, depth 2, and ordinal in [c₀, c_{n−1}) — places cᵢ in V_S(d). *(3) Each such cᵢ lies in some V(bₖ).* By hypothesis, B is a run partition of M(d) (per S8), and S8 (ASN-0036) guarantees its runs cover every V-position in dom(M(d)) ⊇ V_S(d). Hence each cᵢ ∈ V_S(d) lies in V(bₖ) for some k. Combining (1)–(3): c₀, ..., c_{n−2} all lie in V_S(d) ⊆ ⋃_k V(b_k); only c_{n−1}, which serves as an exclusive upper bound for R-PRE(iv) and so is exempt from the iv-coverage clause, may fall outside V_S(d). Under the text-subspace scope (S = 1), V_S(d) is sequential by D-SEQ — V_S(d) = {[S, 1], ..., [S, N]} — so c_{n−1} ∉ V_S(d) is equivalent to ord(c_{n−1}) > N, i.e., c_{n−1} > max(V_S(d)); we use both phrasings interchangeably below. In this case, c_{n−1} ∉ dom(M(d)), so the right-exterior region {v ∈ V_S(d) : v ≥ c_{n−1}} is empty (no V-position has ord ≥ ord(c_{n−1}) > N), and no run can possibly straddle c_{n−1}.

*Interaction between successive cuts.* Phase 1 processes cuts in index order against the *current* (already-refined) partition rather than against the original B, so we must verify that the interior/boundary/outside dispatch remains coherent when a later cut c_j (j > i) is classified after an earlier cut cᵢ has already split some bₖ ∈ B. We dispatch by where c_j lies relative to the original V(bₖ), distinguishing two cases that together exhaust the Phase 1 outcomes for c_j. *Case A — c_j ∉ V(bₖ) originally.* Then c_j either lies in some other original run b_{k'} with k' ≠ k (and the Phase 1 dispatch handles it against b_{k'} by the interior/boundary/outside classification applied to b_{k'}, independently of bₖ's split), or lies outside ⋃_k V(b_k) entirely (in which case the "Outside" sub-case fires, which by the justification in the bullet above can occur only for c_{n−1}). Either way, the step-i split of bₖ is irrelevant to the step-j dispatch. *Case B — c_j ∈ V(bₖ) originally.* We show that c_j then falls in the right piece of bₖ's split, never in the left piece. The step-i split at offset c = ord(cᵢ) − ord(vₖ) produced a left piece (vₖ, aₖ, c) with V-extent [ord(vₖ), ord(vₖ) + c) and a right piece starting at vₖ + c with ord(vₖ + c) = ord(vₖ) + c = ord(cᵢ). At step j > i, CS2 gives ord(c_j) > ord(cᵢ) = ord(vₖ) + c, so c_j cannot lie in the left piece's V-extent [ord(vₖ), ord(vₖ) + c). Combined with the case hypothesis c_j ∈ V(bₖ) — i.e., ord(c_j) < ord(vₖ) + nₖ — this places c_j in the right piece's V-extent [ord(vₖ) + c, ord(vₖ) + nₖ). The Phase 1 dispatch for c_j against the right piece then applies the interior/boundary classification to determine whether to split the right piece further. The case split (A vs. B) exhausts every Phase 1 outcome at step j: under partition disjointness (maintained as a Phase 1 invariant — each split replaces one run by two disjoint runs whose union equals the original V-extent), c_j belongs to at most one original run, and Case A subsumes both "different original run" and "outside all original runs" sub-cases. The process is well-defined because S8-uniq/S8-cons are maintained after each split (uniqueness of containing run carries over from the partition property, consistency by the Split lemma). After all cuts are processed, no run straddles any cut position c_i for 0 ≤ i ≤ n − 1 (equivalently, no c_i is strictly interior to the V-extent of any run in the resulting partition).

*Phase 2: Classify.* Each run in the post-split partition lies entirely within one region — non-S (V-extent in some subspace S' ≠ S), exterior left, α, μ if 4-cut, β, or exterior right — because no run crosses a cut boundary (subspace-S runs are split at S-subspace cuts, and non-S runs are entirely contained in their subspace by OrdShiftHom (b) of ASN-0036 as cited in the Scope note). When c_{n−1} > max(V_S(d)), the exterior-right region is empty and no run is classified there; the non-S region is empty when dom(M(d)) ⊆ V_S(d), and either condition may hold independently. The classification by Phase 1 of the remaining cuts together with the subspace separation of non-S runs covers all runs.

*Phase 3: Reassemble.* Apply the permutation π to each run's V-start. Each run (vₖ, aₖ, nₖ) in the post-split, post-classify partition becomes (π(vₖ), aₖ, nₖ): the V-start is replaced by π(vₖ); the I-start aₖ and width nₖ are preserved verbatim. Per region:

- Non-S runs: π(vₖ) = vₖ by R-NS(NS-π); the triple (vₖ, aₖ, nₖ) carries through unchanged, as also recorded by R-NS(NS-run).
- Exterior runs: π(vₖ) = vₖ by the subspace-S exterior clause of R-PPERM/R-SPERM; the triple carries through unchanged.
- α runs: π(vₖ) is computed by the α-branch of R-PPERM (3-cut) or R-SPERM (4-cut).
- β runs: π(vₖ) is computed by the β-branch of R-PPERM (3-cut) or R-SPERM (4-cut).
- μ runs (4-cut only): π(vₖ) is computed by the μ-branch of R-SPERM.

The I-start and width of each run are preserved because the rearrangement modifies no I-addresses (M'(d) and M(d) share the same value set, only repositioned) and because, by R-COMM, π commutes with ordinal shift within each region — so the consecutive V-positions vₖ, vₖ + 1, ..., vₖ + (nₖ − 1) of a run map to consecutive V-positions π(vₖ), π(vₖ) + 1, ..., π(vₖ) + (nₖ − 1), keeping the width intact.

*Per-region displacement (commentary).* Phase 3 is formulated entirely in terms of π; the displacement Δ plays no operational role. R-DISP records the ordinal-level magnitudes for each region — Δ is constant on each region, taking values 0 on the non-S and exterior regions, +w_β (3-cut) or +(w_β + w_μ) (4-cut) on α, −w_α (3-cut) or −(w_α + w_μ) (4-cut) on β, and (for 4-cut) +(w_β − w_α), −(w_α − w_β), or 0 on μ per the three sub-cases of the comparison of w_β and w_α. These magnitudes are *descriptive*: R-DISP is consumed below only as an equality predicate ("two positions in the same region have equal Δ") and never via arithmetic on the signed-magnitude carrier, which supports no addition, summation, or comparison in this ASN. The worked examples display Δ-values as a numerical cross-check that per-region uniformity holds, not as an operational replacement for π.

*Contiguity of reassembled runs.* Within each region, π applies a uniform ordinal displacement. After Phase 1, every run lies entirely in a single region, so for each run (vⱼ, aⱼ, nⱼ) and 0 ≤ k < nⱼ, positions vⱼ and vⱼ + k are in the same region: for subspace-S runs this is by Phase 1's split-at-cuts construction; for non-S runs this is the V-extent confinement clause of R-NS(NS-run). By R-COMM applied with the same-region precondition discharged (π(vⱼ + k) = π(vⱼ) + k), consecutive V-positions in the original run map to consecutive V-positions, so each reassembled run (π(vⱼ), aⱼ, nⱼ) occupies a contiguous V-position range and is therefore a valid run. For non-S runs π is the identity (R-NS(NS-π)) and the run passes through unchanged (R-NS(NS-run)) — contiguity is immediate.

The resulting runs satisfy S8-cons (consistency under M'(d)). *Subspace-S runs:* for each reassembled run (π(vⱼ), aⱼ, nⱼ) and 0 ≤ k < nⱼ: M'(d)(π(vⱼ) + k) = M'(d)(π(vⱼ + k)) = M(d)(vⱼ + k) = aⱼ + k. The second equality uses the permutation defining property M'(d)(π(v)) = M(d)(v); the first uses R-COMM. *Non-S runs:* discharged by R-NS(NS-run), whose post-state S8-cons clause supplies M'(d)(vⱼ + k) = aⱼ + k for 0 ≤ k < nⱼ directly.

Uniqueness of the containing run (S8-uniq) for M'(d): π is a bijection on dom(M(d)) = dom(M'(d)), and π restricts to the identity on the non-S part of dom(M(d)) (R-NS(NS-π)) and to a bijection on V_S(d) (R-PPERM/R-SPERM). The V-extents of the reassembled subspace-S runs are pairwise disjoint and cover V_S(d) (from the partition property of the pre-reassembly subspace-S partition and bijectivity of π|_{V_S(d)}); the V-extents of the carried-over non-S runs are pairwise disjoint and cover dom(M(d)) \ V_S(d) (inherited from the pre-state partition, via R-NS(NS-run)). Pairwise disjointness across the two groups holds because subspace-S and non-S V-extents lie in distinct subspaces (T10 of ASN-0034: non-nesting prefixes generate disjoint subtrees). Together these yield the E! quantification of S8-uniq on dom(M'(d)).

The partition B' is valid but not necessarily maximal: B' may contain V-adjacent, I-adjacent pairs of runs that satisfy the merge condition. The maximal partition of M'(d) is recovered by applying the exhaustive-merge process to B' — which terminates and produces a unique maximal partition by the canonical-decomposition argument (steps (a)–(d) above), applied with M'(d) in place of M(d). This ASN does not characterize *which* pre-state run pairs produce post-state mergeability; doing so would require a separate analysis tying region assignment under R-BLK Phase 2 to I-address arithmetic from the pre-state, beyond R-BLK's scope. The 4-cut worked example below exhibits a concrete instance (B and H merging into a width-3 run).


## Worked Example: 3-Cut Pivot on a 5-Position Document

We trace a concrete 3-cut pivot to verify the postconditions against explicit values. Let document d have subspace S = 1 with V_S(d) = {[1,1], [1,2], [1,3], [1,4], [1,5]}, and let the arrangement be:

```
M(d)([1,1]) = 3.0.1.0.1.0.1.1    (I-address A)
M(d)([1,2]) = 3.0.1.0.1.0.1.2    (I-address B)
M(d)([1,3]) = 3.0.1.0.1.0.1.3    (I-address C)
M(d)([1,4]) = 5.0.2.0.1.0.1.1    (I-address D)
M(d)([1,5]) = 5.0.2.0.1.0.1.2    (I-address E)
```

Content A–C originates from document 3.0.1.0.1 (origin 3.0.1.0.1); D–E from document 5.0.2.0.1 (origin 5.0.2.0.1). The canonical run partition has two runs: b₁ = ([1,1], 3.0.1.0.1.0.1.1, 3) and b₂ = ([1,4], 5.0.2.0.1.0.1.1, 2).

We apply a 3-cut pivot with K = ([1,2], [1,4], [1,5]): c₀ = [1,2], c₁ = [1,4], c₂ = [1,5]. The affected range is [c₀, c₂) = {[1,2], [1,3], [1,4]}. Region α = {[1,2], [1,3]} (w_α = 2), region β = {[1,4]} (w_β = 1).

**R-PRE verification.** (i) M(d) well-defined. (ii) V_S(d) ≠ ∅. (iii) CS1: n = 3; CS2: [1,2] < [1,4] < [1,5]; CS3: all subspace 1; CS4: all depth 2. (iv) All positions in [[1,2], [1,5)) are in V_S(d). Width positivity: w_α = 2 ≥ 1, w_β = 1 ≥ 1 (consequence). ✓

**Applying the postconditions.** We compute M'(d) position by position:

R-EXT: M'(d)([1,1]) = M(d)([1,1]) = A. M'(d)([1,5]) = M(d)([1,5]) = E.

R-P1 (j = 0): M'(d)(c₀ + 0) = M'(d)([1,2]) = M(d)(c₁ + 0) = M(d)([1,4]) = D.

R-P2 (j = 0): M'(d)(c₀ + 1 + 0) = M'(d)([1,3]) = M(d)(c₀ + 0) = M(d)([1,2]) = B.

R-P2 (j = 1): M'(d)(c₀ + 1 + 1) = M'(d)([1,4]) = M(d)(c₀ + 1) = M(d)([1,3]) = C.

**Result:**

```
M'(d)([1,1]) = A     (exterior, unchanged)
M'(d)([1,2]) = D     (was β, now at start of affected range)
M'(d)([1,3]) = B     (was α position 1, shifted forward by w_β = 1)
M'(d)([1,4]) = C     (was α position 2, shifted forward by w_β = 1)
M'(d)([1,5]) = E     (exterior, unchanged)
```

**R-PPERM verification.** The permutation π: π([1,1]) = [1,1] (exterior), π([1,2]) = [1,3] (α: c₀ + 0 → c₀ + w_β + 0 = [1,3]), π([1,3]) = [1,4] (α: c₀ + 1 → c₀ + w_β + 1 = [1,4]), π([1,4]) = [1,2] (β: c₁ + 0 → c₀ + 0 = [1,2]), π([1,5]) = [1,5] (exterior). We check: M'(d)(π([1,2])) = M'(d)([1,3]) = B = M(d)([1,2]) ✓. M'(d)(π([1,4])) = M'(d)([1,2]) = D = M(d)([1,4]) ✓.

**R-RI verification.** ran(M'(d)) = {A, D, B, C, E} = ran(M(d)) (the same five I-addresses, only their V-position assignments rearranged). Since ran(M(d)) ⊆ dom(C) by S3 of the pre-state and C' = C, ran(M'(d)) ⊆ dom(C'). ✓

**Displacement verification.** Reading Δ as a signed magnitude: Δ([1,1]) = 0 (exterior left, unchanged). Δ([1,2]) = +(3 − 2) = +1 = +w_β = +1 (α-branch, j = 0). Δ([1,3]) = +(4 − 3) = +1 = +w_β (α-branch, j = 1). Δ([1,4]) = −(4 − 2) = −2 = −w_α (β-branch, j = 0). Δ([1,5]) = 0 (exterior right). The α-region displacement is uniformly +1, the β-region displacement is uniformly −2, and the two exterior positions are fixed — confirming R-DISP for this example.

**Run decomposition via R-BLK.** *Phase 1 (Split):* c₀ = [1,2] is interior to b₁ = ([1,1], A, 3) at offset ord(c₀) − ord(b₁.v) = 2 − 1 = 1; split b₁ into ([1,1], A, 1) and ([1,2], B, 2). c₁ = [1,4] coincides with b₂'s V-start ([1,4]), so no split is performed at c₁ (boundary case). c₂ = [1,5] is interior to b₂ = ([1,4], D, 2) at offset ord(c₂) − ord(b₂.v) = 5 − 4 = 1; split b₂ into ([1,4], D, 1) and ([1,5], E, 1), separating the β-content D from the exterior-right content E. Post-split partition: {([1,1], A, 1), ([1,2], B, 2), ([1,4], D, 1), ([1,5], E, 1)}.

*Phase 2 (Classify):* Each post-split run lies entirely within one region. ([1,1], A, 1) has V-extent {[1,1]} with ord = 1 < ord(c₀) = 2, so it lies in the *exterior left* region. ([1,2], B, 2) has V-extent {[1,2], [1,3]} with ordinals in [ord(c₀), ord(c₁)) = [2, 4), so it lies in *α*. ([1,4], D, 1) has V-extent {[1,4]} with ordinal in [ord(c₁), ord(c₂)) = [4, 5), so it lies in *β*. ([1,5], E, 1) has V-extent {[1,5]} with ord = 5 ≥ ord(c₂) = 5, so it lies in the *exterior right* region. No run is classified into the non-S region because every V-position in this example has subspace 1 = S; the non-S region is empty here.

*Phase 3 (Reassemble):* Apply each run's region displacement to its V-start. Region displacements are Δ_exterior-left = 0, Δ_α = +w_β = +1, Δ_β = −w_α = −2, Δ_exterior-right = 0 (per R-DISP for the 3-cut pivot).

- ([1,1], A, 1) → ([1,1], A, 1) (exterior left, Δ = 0, V-start unchanged).
- ([1,2], B, 2) → ([1,3], B, 2) (α, Δ = +1; V-start shifted from [1,2] to [1,3], width and I-start preserved).
- ([1,4], D, 1) → ([1,2], D, 1) (β, Δ = −2; V-start shifted from [1,4] to [1,2], width and I-start preserved).
- ([1,5], E, 1) → ([1,5], E, 1) (exterior right, Δ = 0, V-start unchanged).

Sorted by V-start: {([1,1], A, 1), ([1,2], D, 1), ([1,3], B, 2), ([1,5], E, 1)}. *S8-cons verification on reassembled runs:* ([1,3], B, 2): M'(d)([1,3]) = B, M'(d)([1,4]) = C = B + 1 ✓. The width-1 runs ([1,1], A, 1), ([1,2], D, 1), ([1,5], E, 1) satisfy S8-cons trivially at their lone offset k = 0.

*Merge check:* No V-adjacent, I-adjacent pair. ([1,1], A, 1) and ([1,2], D, 1) are V-adjacent (1 + 1 = 2) but not I-adjacent (origin(A) = 3.0.1.0.1 ≠ origin(D) = 5.0.2.0.1, so A + 1 ≠ D). ([1,2], D, 1) and ([1,3], B, 2) are V-adjacent (2 + 1 = 3) but not I-adjacent (origin(D) ≠ origin(B), so D + 1 ≠ B). ([1,3], B, 2) and ([1,5], E, 1) are not V-adjacent (3 + 2 = 5 ✓ for V-adjacency, but check I-adjacency: B + 2 = 3.0.1.0.1.0.1.4 ≠ E = 5.0.2.0.1.0.1.2, different origins).

**Canonical partition:** {([1,1], A, 1), ([1,2], D, 1), ([1,3], B, 2), ([1,5], E, 1)}. The rearrangement preserved one run's interior structure ([1,3], B, 2) — B and C remained adjacent — while isolating A from B/C and pulling D into the position between A and B. No new merges arose because the pre-state I-address origins differ across the boundaries created by the pivot.


## Worked Example: 4-Cut Swap on an 8-Position Document

We trace a 4-cut swap with unequal region widths. Let document d have subspace S = 1 with V_S(d) = {[1,1], ..., [1,8]}, and let the arrangement be:

```
M(d)([1,1]) = 3.0.1.0.1.0.1.1    (I-address A)
M(d)([1,2]) = 3.0.1.0.1.0.1.2    (I-address B)
M(d)([1,3]) = 3.0.1.0.1.0.1.3    (I-address C)
M(d)([1,4]) = 7.0.1.0.1.0.1.1    (I-address D)
M(d)([1,5]) = 5.0.2.0.1.0.1.1    (I-address E)
M(d)([1,6]) = 5.0.2.0.1.0.1.2    (I-address F)
M(d)([1,7]) = 5.0.2.0.1.0.1.3    (I-address G)
M(d)([1,8]) = 3.0.1.0.1.0.1.4    (I-address H)
```

Content A–C originates from document 3.0.1.0.1; D from document 7.0.1.0.1; E–G from document 5.0.2.0.1; H from document 3.0.1.0.1. The canonical run partition has four runs: b₁ = ([1,1], A, 3), b₂ = ([1,4], D, 1), b₃ = ([1,5], E, 3), b₄ = ([1,8], H, 1).

We apply a 4-cut swap with K = ([1,2], [1,4], [1,5], [1,8]): c₀ = [1,2], c₁ = [1,4], c₂ = [1,5], c₃ = [1,8]. The affected range is [c₀, c₃) = {[1,2], ..., [1,7]}. Region α = {[1,2], [1,3]} (w_α = 2), middle μ = {[1,4]} (w_μ = 1), region β = {[1,5], [1,6], [1,7]} (w_β = 3). Since w_α = 2 ≠ w_β = 3, the middle displacement w_β − w_α = 1 is nonzero.

**R-PRE verification.** (i) M(d) well-defined. (ii) V_S(d) ≠ ∅. (iii) CS1: n = 4; CS2: [1,2] < [1,4] < [1,5] < [1,8]; CS3: all subspace 1; CS4: all depth 2. (iv) All positions in [[1,2], [1,8)) are in V_S(d). Width positivity: w_α = 2 ≥ 1, w_β = 3 ≥ 1, w_μ = 1 ≥ 1 (consequence). ✓

**Applying the postconditions.** We compute M'(d) position by position:

R-EXT: M'(d)([1,1]) = M(d)([1,1]) = A. M'(d)([1,8]) = M(d)([1,8]) = H.

R-S1 (j = 0): M'(d)(c₀ + 0) = M'(d)([1,2]) = M(d)(c₂ + 0) = M(d)([1,5]) = E.

R-S1 (j = 1): M'(d)(c₀ + 1) = M'(d)([1,3]) = M(d)(c₂ + 1) = M(d)([1,6]) = F.

R-S1 (j = 2): M'(d)(c₀ + 2) = M'(d)([1,4]) = M(d)(c₂ + 2) = M(d)([1,7]) = G.

R-S2 (j = 0): M'(d)(c₀ + 3 + 0) = M'(d)([1,5]) = M(d)(c₁ + 0) = M(d)([1,4]) = D.

R-S3 (j = 0): M'(d)(c₀ + 3 + 1 + 0) = M'(d)([1,6]) = M(d)(c₀ + 0) = M(d)([1,2]) = B.

R-S3 (j = 1): M'(d)(c₀ + 3 + 1 + 1) = M'(d)([1,7]) = M(d)(c₀ + 1) = M(d)([1,3]) = C.

**Result:**

```
M'(d)([1,1]) = A     (exterior, unchanged)
M'(d)([1,2]) = E     (from β via R-S1)
M'(d)([1,3]) = F     (from β via R-S1)
M'(d)([1,4]) = G     (from β via R-S1)
M'(d)([1,5]) = D     (from μ via R-S2)
M'(d)([1,6]) = B     (from α via R-S3)
M'(d)([1,7]) = C     (from α via R-S3)
M'(d)([1,8]) = H     (exterior, unchanged)
```

The three swap clauses tile [c₀, c₃) = [[1,2], [1,8]) exactly: R-S1 covers ordinals 2–4 (w_β = 3 positions), R-S2 covers ordinal 5 (w_μ = 1 position), R-S3 covers ordinals 6–7 (w_α = 2 positions). Total: 3 + 1 + 2 = 6 = |[c₀, c₃)|. ✓

**R-SPERM verification.** The permutation π:

- π([1,1]) = [1,1] (exterior).
- π([1,2]) = c₀ + w_β + w_μ + 0 = [1,6] (α: j = 0). Check: M'(d)([1,6]) = B = M(d)([1,2]) ✓.
- π([1,3]) = c₀ + w_β + w_μ + 1 = [1,7] (α: j = 1). Check: M'(d)([1,7]) = C = M(d)([1,3]) ✓.
- π([1,4]) = c₀ + w_β + 0 = [1,5] (μ: j = 0). Check: M'(d)([1,5]) = D = M(d)([1,4]) ✓.
- π([1,5]) = c₀ + 0 = [1,2] (β: j = 0). Check: M'(d)([1,2]) = E = M(d)([1,5]) ✓.
- π([1,6]) = c₀ + 1 = [1,3] (β: j = 1). Check: M'(d)([1,3]) = F = M(d)([1,6]) ✓.
- π([1,7]) = c₀ + 2 = [1,4] (β: j = 2). Check: M'(d)([1,4]) = G = M(d)([1,7]) ✓.
- π([1,8]) = [1,8] (exterior).

**R-RI verification.** ran(M'(d)) = {A, B, C, D, E, F, G, H} = ran(M(d)) (the same eight I-addresses, only their V-position assignments rearranged). Since ran(M(d)) ⊆ dom(C) by S3 of the pre-state and C' = C, ran(M'(d)) ⊆ dom(C'). ✓

**Displacement verification.** Reading Δ as a signed magnitude: Δ([1,2]) = +(6 − 2) = +4 = +(w_β + w_μ) ✓. Δ([1,3]) = +(7 − 3) = +4 ✓. Δ([1,4]) = +(5 − 4) = +1 = +(w_β − w_α), the μ-branch with w_β > w_α ✓. Δ([1,5]) = −(5 − 2) = −3 = −(w_α + w_μ) ✓. Δ([1,6]) = −(6 − 3) = −3 ✓. Δ([1,7]) = −(7 − 4) = −3 ✓. The middle-region displacement is +1, confirming the asymmetric structure when w_α ≠ w_β.

**Run decomposition via R-BLK.** *Phase 1 (Split):* c₀ = [1,2] is interior to b₁ = ([1,1], A, 3) at offset 1. Split: ([1,1], A, 1) and ([1,2], B, 2). The remaining cuts c₁ = [1,4], c₂ = [1,5], c₃ = [1,8] coincide with run boundaries (c₁ = b₂'s start, c₂ = b₃'s start, c₃ = b₄'s start), so no further splits. Post-split partition: {([1,1], A, 1), ([1,2], B, 2), ([1,4], D, 1), ([1,5], E, 3), ([1,8], H, 1)}.

*Phase 2 (Classify):* ([1,1], A, 1) → exterior left. ([1,2], B, 2) → α. ([1,4], D, 1) → μ. ([1,5], E, 3) → β. ([1,8], H, 1) → exterior right.

*Phase 3 (Reassemble):* Apply region displacements:

- ([1,1], A, 1) → ([1,1], A, 1) (exterior, Δ = 0)
- ([1,2], B, 2) → ([1,6], B, 2) (α, Δ = +4)
- ([1,4], D, 1) → ([1,5], D, 1) (μ, Δ = +1)
- ([1,5], E, 3) → ([1,2], E, 3) (β, Δ = −3)
- ([1,8], H, 1) → ([1,8], H, 1) (exterior, Δ = 0)

Sorted by V-start: {([1,1], A, 1), ([1,2], E, 3), ([1,5], D, 1), ([1,6], B, 2), ([1,8], H, 1)}. Checking S8-cons: for run ([1,2], E, 3), M'(d)([1,2]) = E, M'(d)([1,3]) = F = E + 1, M'(d)([1,4]) = G = E + 2 ✓.

*Merge check:* ([1,6], B, 2) and ([1,8], H, 1) are V-adjacent (6 + 2 = 8) and I-adjacent (B + 2 = 3.0.1.0.1.0.1.4 = H). Merge: ([1,6], B, 3). No other pair satisfies both conditions — ([1,1], A, 1) and ([1,2], E, 3) differ in origin; ([1,2], E, 3) and ([1,5], D, 1) differ in origin; ([1,5], D, 1) and ([1,6], B, 2) differ in origin.

**Canonical partition:** {([1,1], A, 1), ([1,2], E, 3), ([1,5], D, 1), ([1,6], B, 3)}. The rearrangement brought B, C (formerly at [1,2]–[1,3]) adjacent to H (at [1,8]), and since B + 2 = H, they merge into a single run of width 3. Meanwhile A, formerly part of a width-3 run with B and C, is now isolated.


## Worked Example: 4-Cut Swap with Equal Region Widths (w_α = w_β)

The two preceding examples leave the μ-displacement sub-case w_α = w_β untraced. We trace a 4-cut swap with w_α = w_β to verify the Δ_μ = 0 branch — μ is fixed pointwise by π, even though the surrounding α and β regions exchange places. Let document d have subspace S = 1 with V_S(d) = {[1,1], ..., [1,7]}, and let the arrangement be:

```
M(d)([1,1]) = 3.0.1.0.1.0.1.1    (I-address A)
M(d)([1,2]) = 3.0.1.0.1.0.1.2    (I-address B)
M(d)([1,3]) = 3.0.1.0.1.0.1.3    (I-address C)
M(d)([1,4]) = 7.0.1.0.1.0.1.1    (I-address D)
M(d)([1,5]) = 5.0.2.0.1.0.1.1    (I-address E)
M(d)([1,6]) = 5.0.2.0.1.0.1.2    (I-address F)
M(d)([1,7]) = 9.0.1.0.1.0.1.1    (I-address G)
```

Content A–C originates from document 3.0.1.0.1; D from 7.0.1.0.1; E–F from 5.0.2.0.1; G from 9.0.1.0.1. The canonical run partition has four runs: b₁ = ([1,1], A, 3), b₂ = ([1,4], D, 1), b₃ = ([1,5], E, 2), b₄ = ([1,7], G, 1).

We apply a 4-cut swap with K = ([1,2], [1,4], [1,5], [1,7]): c₀ = [1,2], c₁ = [1,4], c₂ = [1,5], c₃ = [1,7]. The affected range is [c₀, c₃) = {[1,2], ..., [1,6]}. Region α = {[1,2], [1,3]} (w_α = 2), middle μ = {[1,4]} (w_μ = 1), region β = {[1,5], [1,6]} (w_β = 2). Since w_α = w_β = 2, the μ-branch displacement w_β − w_α vanishes and the Δ_μ = 0 sub-case applies.

**R-PRE verification.** (i) M(d) well-defined. (ii) V_S(d) ≠ ∅. (iii) CS1: n = 4; CS2: [1,2] < [1,4] < [1,5] < [1,7]; CS3: all subspace 1; CS4: all depth 2. (iv) All positions in [[1,2], [1,7)) are in V_S(d). Width positivity: w_α = 2 ≥ 1, w_β = 2 ≥ 1, w_μ = 1 ≥ 1 (consequence). ✓

**Applying the postconditions.** We compute M'(d) position by position:

R-EXT: M'(d)([1,1]) = M(d)([1,1]) = A. M'(d)([1,7]) = M(d)([1,7]) = G.

R-S1 (j = 0): M'(d)(c₀ + 0) = M'(d)([1,2]) = M(d)(c₂ + 0) = M(d)([1,5]) = E.

R-S1 (j = 1): M'(d)(c₀ + 1) = M'(d)([1,3]) = M(d)(c₂ + 1) = M(d)([1,6]) = F.

R-S2 (j = 0): M'(d)(c₀ + w_β + 0) = M'(d)([1,4]) = M(d)(c₁ + 0) = M(d)([1,4]) = D.

R-S3 (j = 0): M'(d)(c₀ + w_β + w_μ + 0) = M'(d)([1,5]) = M(d)(c₀ + 0) = M(d)([1,2]) = B.

R-S3 (j = 1): M'(d)(c₀ + w_β + w_μ + 1) = M'(d)([1,6]) = M(d)(c₀ + 1) = M(d)([1,3]) = C.

**Result:**

```
M'(d)([1,1]) = A     (exterior, unchanged)
M'(d)([1,2]) = E     (from β via R-S1)
M'(d)([1,3]) = F     (from β via R-S1)
M'(d)([1,4]) = D     (from μ via R-S2 — *fixed in place* by Δ_μ = 0)
M'(d)([1,5]) = B     (from α via R-S3)
M'(d)([1,6]) = C     (from α via R-S3)
M'(d)([1,7]) = G     (exterior, unchanged)
```

The R-S2 clause exhibits the structural property of the w_α = w_β branch: M'(d)([1,4]) = M(d)([1,4]) = D, because the destination ord c₀ + w_β = 4 coincides with the source ord c₁ = 4 when w_β = w_α. R-S2 is *not* vacuous — it still asserts the equation M'(d)([1,4]) = M(d)([1,4]) — but it discharges to a fixed-point identity at every offset j < w_μ. The three swap clauses tile [c₀, c₃) = [[1,2], [1,7)) exactly: R-S1 covers ordinals 2–3 (w_β = 2 positions), R-S2 covers ordinal 4 (w_μ = 1 position), R-S3 covers ordinals 5–6 (w_α = 2 positions). Total: 2 + 1 + 2 = 5 = |[c₀, c₃)|. ✓

**R-SPERM verification.** The permutation π:

- π([1,1]) = [1,1] (exterior).
- π([1,2]) = c₀ + w_β + w_μ + 0 = [1,5] (α: j = 0). Check: M'(d)([1,5]) = B = M(d)([1,2]) ✓.
- π([1,3]) = c₀ + w_β + w_μ + 1 = [1,6] (α: j = 1). Check: M'(d)([1,6]) = C = M(d)([1,3]) ✓.
- π([1,4]) = c₀ + w_β + 0 = [1,4] (μ: j = 0). Check: M'(d)([1,4]) = D = M(d)([1,4]) ✓.
- π([1,5]) = c₀ + 0 = [1,2] (β: j = 0). Check: M'(d)([1,2]) = E = M(d)([1,5]) ✓.
- π([1,6]) = c₀ + 1 = [1,3] (β: j = 1). Check: M'(d)([1,3]) = F = M(d)([1,6]) ✓.
- π([1,7]) = [1,7] (exterior).

Note π([1,4]) = [1,4]: μ is the single position fixed by π via the μ-branch (as distinct from the exterior, which is fixed via R-FRAME-S(a)). The rearrangement is still a genuine swap — α and β positions move — but the middle region holds in place pointwise.

**R-RI verification.** ran(M'(d)) = {A, B, C, D, E, F, G} = ran(M(d)). Since ran(M(d)) ⊆ dom(C) by S3 of the pre-state and C' = C, ran(M'(d)) ⊆ dom(C'). ✓

**Displacement verification.** Reading Δ as a signed magnitude: Δ([1,2]) = +(5 − 2) = +3 = +(w_β + w_μ) ✓. Δ([1,3]) = +(6 − 3) = +3 ✓. Δ([1,4]) = 0 — the μ-branch with w_β = w_α ✓. Δ([1,5]) = −(5 − 2) = −3 = −(w_α + w_μ) ✓. Δ([1,6]) = −(6 − 3) = −3 ✓. The middle-region displacement vanishes, confirming the structural symmetry of the Δ_μ = 0 sub-case.

**Run decomposition via R-BLK.** *Phase 1 (Split):* c₀ = [1,2] is interior to b₁ = ([1,1], A, 3) at offset 1. Split: ([1,1], A, 1) and ([1,2], B, 2). The remaining cuts c₁ = [1,4], c₂ = [1,5], c₃ = [1,7] coincide with run boundaries (c₁ = b₂'s start, c₂ = b₃'s start, c₃ = b₄'s start), so no further splits. Post-split partition: {([1,1], A, 1), ([1,2], B, 2), ([1,4], D, 1), ([1,5], E, 2), ([1,7], G, 1)}.

*Phase 2 (Classify):* ([1,1], A, 1) → exterior left. ([1,2], B, 2) → α. ([1,4], D, 1) → μ. ([1,5], E, 2) → β. ([1,7], G, 1) → exterior right.

*Phase 3 (Reassemble):* Apply region displacements (α: Δ = +3, μ: Δ = 0, β: Δ = −3, exteriors: Δ = 0):

- ([1,1], A, 1) → ([1,1], A, 1) (exterior)
- ([1,2], B, 2) → ([1,5], B, 2) (α, V-start shifted +3)
- ([1,4], D, 1) → ([1,4], D, 1) (μ, V-start unchanged — Δ = 0)
- ([1,5], E, 2) → ([1,2], E, 2) (β, V-start shifted −3)
- ([1,7], G, 1) → ([1,7], G, 1) (exterior)

Sorted by V-start: {([1,1], A, 1), ([1,2], E, 2), ([1,4], D, 1), ([1,5], B, 2), ([1,7], G, 1)}. The μ-run ([1,4], D, 1) carries through Phase 3 untouched because its assigned displacement is zero; the α- and β-runs exchange positions across this fixed centre.

*S8-cons verification on reassembled runs:* ([1,2], E, 2): M'(d)([1,2]) = E, M'(d)([1,3]) = F = E + 1 ✓. ([1,5], B, 2): M'(d)([1,5]) = B, M'(d)([1,6]) = C = B + 1 ✓. The width-1 runs ([1,1], A, 1), ([1,4], D, 1), ([1,7], G, 1) satisfy S8-cons trivially at the lone offset k = 0.

*Merge check:* No V-adjacent, I-adjacent pair: ([1,1], A, 1) and ([1,2], E, 2) differ in origin (3.0.1.0.1 vs 5.0.2.0.1); ([1,2], E, 2) and ([1,4], D, 1) differ in origin (5.0.2.0.1 vs 7.0.1.0.1); ([1,4], D, 1) and ([1,5], B, 2) differ in origin (7.0.1.0.1 vs 3.0.1.0.1); ([1,5], B, 2) and ([1,7], G, 1) differ in origin (3.0.1.0.1 vs 9.0.1.0.1).

**Canonical partition:** {([1,1], A, 1), ([1,2], E, 2), ([1,4], D, 1), ([1,5], B, 2), ([1,7], G, 1)}. The rearrangement exchanges the α- and β-runs across a fixed μ-run; the canonical partition is reached without further merges because each region's I-address origin differs from its neighbours'. The example confirms the Δ_μ = 0 sub-case: the μ-run is structurally invariant under R-BLK's Phase 3 reassembly when w_α = w_β.


## Worked Example: 4-Cut Swap with w_β < w_α (Negative Δ_μ Sub-Case)

The preceding 4-cut examples exercise the Δ_μ branches in the w_β > w_α case (the 8-position swap with w_α = 2, w_β = 3) and the w_β = w_α case (the equal-widths swap with w_α = w_β = 2). The third μ-branch sub-case — w_β < w_α, in which the μ-region shifts *backward* by w_α − w_β — has so far gone untraced. We exhibit it here with w_α = 3, w_β = 1, w_μ = 2. The asymmetry w_α > w_β reverses the direction of Δ_μ: the middle region moves earlier in the V-position ordering, into the slot vacated by the (now-narrower) β-region, while α stretches across the right end of the affected range.

Let document d have subspace S = 1 with V_S(d) = {[1,1], ..., [1,8]}, and let the arrangement be:

```
M(d)([1,1]) = 3.0.1.0.1.0.1.1    (I-address A)
M(d)([1,2]) = 3.0.1.0.1.0.1.2    (I-address B)
M(d)([1,3]) = 3.0.1.0.1.0.1.3    (I-address C)
M(d)([1,4]) = 3.0.1.0.1.0.1.4    (I-address D)
M(d)([1,5]) = 5.0.2.0.1.0.1.1    (I-address E)
M(d)([1,6]) = 5.0.2.0.1.0.1.2    (I-address F)
M(d)([1,7]) = 7.0.1.0.1.0.1.1    (I-address G)
M(d)([1,8]) = 9.0.1.0.1.0.1.1    (I-address H)
```

Content A–D originates from document 3.0.1.0.1; E–F from 5.0.2.0.1; G from 7.0.1.0.1; H from 9.0.1.0.1. The canonical run partition has four runs: b₁ = ([1,1], A, 4), b₂ = ([1,5], E, 2), b₃ = ([1,7], G, 1), b₄ = ([1,8], H, 1).

We apply a 4-cut swap with K = ([1,2], [1,5], [1,7], [1,8]): c₀ = [1,2], c₁ = [1,5], c₂ = [1,7], c₃ = [1,8]. The affected range is [c₀, c₃) = {[1,2], ..., [1,7]}. Region α = {[1,2], [1,3], [1,4]} (w_α = 3), middle μ = {[1,5], [1,6]} (w_μ = 2), region β = {[1,7]} (w_β = 1). Since w_β = 1 < w_α = 3, the μ-branch invokes Δ_μ = −(w_α − w_β) = −2, the negative sub-case.

**R-PRE verification.** (i) M(d) well-defined. (ii) V_S(d) ≠ ∅. (iii) CS1: n = 4; CS2: [1,2] < [1,5] < [1,7] < [1,8]; CS3: all subspace 1; CS4: all depth 2. (iv) All positions in [[1,2], [1,8)) are in V_S(d). Width positivity: w_α = 3 ≥ 1, w_β = 1 ≥ 1, w_μ = 2 ≥ 1 (consequence). ✓

**Applying the postconditions.** We compute M'(d) position by position:

R-EXT: M'(d)([1,1]) = M(d)([1,1]) = A. M'(d)([1,8]) = M(d)([1,8]) = H.

R-S1 (j = 0): M'(d)(c₀ + 0) = M'(d)([1,2]) = M(d)(c₂ + 0) = M(d)([1,7]) = G.

R-S2 (j = 0): M'(d)(c₀ + w_β + 0) = M'(d)([1,3]) = M(d)(c₁ + 0) = M(d)([1,5]) = E.

R-S2 (j = 1): M'(d)(c₀ + w_β + 1) = M'(d)([1,4]) = M(d)(c₁ + 1) = M(d)([1,6]) = F.

R-S3 (j = 0): M'(d)(c₀ + w_β + w_μ + 0) = M'(d)([1,5]) = M(d)(c₀ + 0) = M(d)([1,2]) = B.

R-S3 (j = 1): M'(d)(c₀ + w_β + w_μ + 1) = M'(d)([1,6]) = M(d)(c₀ + 1) = M(d)([1,3]) = C.

R-S3 (j = 2): M'(d)(c₀ + w_β + w_μ + 2) = M'(d)([1,7]) = M(d)(c₀ + 2) = M(d)([1,4]) = D.

**Result:**

```
M'(d)([1,1]) = A     (exterior, unchanged)
M'(d)([1,2]) = G     (from β via R-S1)
M'(d)([1,3]) = E     (from μ via R-S2)
M'(d)([1,4]) = F     (from μ via R-S2)
M'(d)([1,5]) = B     (from α via R-S3)
M'(d)([1,6]) = C     (from α via R-S3)
M'(d)([1,7]) = D     (from α via R-S3)
M'(d)([1,8]) = H     (exterior, unchanged)
```

The three swap clauses tile [c₀, c₃) = [[1,2], [1,8)) exactly: R-S1 covers ordinal 2 (w_β = 1 position), R-S2 covers ordinals 3–4 (w_μ = 2 positions), R-S3 covers ordinals 5–7 (w_α = 3 positions). Total: 1 + 2 + 3 = 6 = |[c₀, c₃)|. ✓

**R-SPERM verification.** The permutation π:

- π([1,1]) = [1,1] (exterior).
- π([1,2]) = c₀ + w_β + w_μ + 0 = [1,5] (α: j = 0). Check: M'(d)([1,5]) = B = M(d)([1,2]) ✓.
- π([1,3]) = c₀ + w_β + w_μ + 1 = [1,6] (α: j = 1). Check: M'(d)([1,6]) = C = M(d)([1,3]) ✓.
- π([1,4]) = c₀ + w_β + w_μ + 2 = [1,7] (α: j = 2). Check: M'(d)([1,7]) = D = M(d)([1,4]) ✓.
- π([1,5]) = c₀ + w_β + 0 = [1,3] (μ: j = 0). Check: M'(d)([1,3]) = E = M(d)([1,5]) ✓.
- π([1,6]) = c₀ + w_β + 1 = [1,4] (μ: j = 1). Check: M'(d)([1,4]) = F = M(d)([1,6]) ✓.
- π([1,7]) = c₀ + 0 = [1,2] (β: j = 0). Check: M'(d)([1,2]) = G = M(d)([1,7]) ✓.
- π([1,8]) = [1,8] (exterior).

The μ-region positions [1,5] and [1,6] map *backward* to [1,3] and [1,4] respectively — a uniform shift of −2, equal to −(w_α − w_β) = −(3 − 1) per R-DISP's μ-branch with w_β < w_α.

**R-RI verification.** ran(M'(d)) = {A, B, C, D, E, F, G, H} = ran(M(d)). Since ran(M(d)) ⊆ dom(C) by S3 of the pre-state and C' = C, ran(M'(d)) ⊆ dom(C'). ✓

**Displacement verification.** Reading Δ as a signed magnitude: Δ([1,2]) = +(5 − 2) = +3 = +(w_β + w_μ) ✓. Δ([1,3]) = +(6 − 3) = +3 ✓. Δ([1,4]) = +(7 − 4) = +3 ✓. Δ([1,5]) = −(5 − 3) = −2 = −(w_α − w_β), the μ-branch with w_β < w_α ✓. Δ([1,6]) = −(6 − 4) = −2 ✓. Δ([1,7]) = −(7 − 2) = −5 = −(w_α + w_μ) ✓. The middle-region displacement is uniformly −2, confirming the negative Δ_μ sub-case and matching R-DISP's prediction at every offset.

**Run decomposition via R-BLK.** *Phase 1 (Split):* c₀ = [1,2] is interior to b₁ = ([1,1], A, 4) at offset 1. Split: ([1,1], A, 1) and ([1,2], B, 3). The remaining cuts c₁ = [1,5], c₂ = [1,7], c₃ = [1,8] coincide with run boundaries (c₁ = b₂'s start, c₂ = b₃'s start, c₃ = b₄'s start), so no further splits. Post-split partition: {([1,1], A, 1), ([1,2], B, 3), ([1,5], E, 2), ([1,7], G, 1), ([1,8], H, 1)}.

*Phase 2 (Classify):* ([1,1], A, 1) → exterior left. ([1,2], B, 3) → α (ordinals 2, 3, 4 ∈ [ord(c₀), ord(c₁)) = [2, 5)). ([1,5], E, 2) → μ (ordinals 5, 6 ∈ [ord(c₁), ord(c₂)) = [5, 7)). ([1,7], G, 1) → β (ordinal 7 ∈ [ord(c₂), ord(c₃)) = [7, 8)). ([1,8], H, 1) → exterior right.

*Phase 3 (Reassemble):* Apply region displacements (α: Δ = +3, μ: Δ = −2, β: Δ = −5, exteriors: Δ = 0):

- ([1,1], A, 1) → ([1,1], A, 1) (exterior)
- ([1,2], B, 3) → ([1,5], B, 3) (α, V-start shifted +3)
- ([1,5], E, 2) → ([1,3], E, 2) (μ, V-start shifted −2 — the negative Δ_μ sub-case in action)
- ([1,7], G, 1) → ([1,2], G, 1) (β, V-start shifted −5)
- ([1,8], H, 1) → ([1,8], H, 1) (exterior)

Sorted by V-start: {([1,1], A, 1), ([1,2], G, 1), ([1,3], E, 2), ([1,5], B, 3), ([1,8], H, 1)}.

*S8-cons verification on reassembled runs:* ([1,3], E, 2): M'(d)([1,3]) = E, M'(d)([1,4]) = F = E + 1 ✓. ([1,5], B, 3): M'(d)([1,5]) = B, M'(d)([1,6]) = C = B + 1, M'(d)([1,7]) = D = B + 2 ✓. The width-1 runs satisfy S8-cons trivially.

*Merge check:* ([1,1], A, 1) and ([1,2], G, 1) are V-adjacent (1 + 1 = 2) but not I-adjacent (origin(A) = 3.0.1.0.1 ≠ origin(G) = 7.0.1.0.1, so A + 1 ≠ G). ([1,2], G, 1) and ([1,3], E, 2) are V-adjacent (2 + 1 = 3) but differ in origin (G vs E). ([1,3], E, 2) and ([1,5], B, 3) are V-adjacent (3 + 2 = 5) but differ in origin (E vs B). ([1,5], B, 3) and ([1,8], H, 1) are V-adjacent (5 + 3 = 8); checking I-adjacency: B + 3 = 3.0.1.0.1.0.1.5 ≠ H = 9.0.1.0.1.0.1.1. No mergeable pair.

**Canonical partition:** {([1,1], A, 1), ([1,2], G, 1), ([1,3], E, 2), ([1,5], B, 3), ([1,8], H, 1)}. The rearrangement extracts G into the slot vacated by α's leftward content (originally B at [1,2]), places the μ-content (E, F) one step earlier in the V-ordering (Δ_μ = −2), and pushes B, C, D to the right end of the affected range. The example confirms the negative Δ_μ sub-case: the μ-region moves earlier when the narrower β cannot accommodate α's full width, with the displacement magnitude w_α − w_β exposed cleanly in both the explicit π formula and the post-reassembly V-start of the μ-run.


## Worked Example: 3-Cut Pivot at the Boundary (Minimum V_S(d), Empty Right Exterior)

The four preceding examples illustrate typical configurations with non-trivial exteriors and multiple-position runs. We now exhibit the *boundary* configuration: a 3-cut pivot on the minimum-size V_S(d) admitting a 3-cut sequence, with the rightmost cut placed strictly above max(V_S(d)) so the right exterior is empty. This case exercises three structural edges simultaneously — the minimum w_α = w_β = 1 (Phase 2 classifies a single position into each region), V_S(d) size 2 (the smallest V_S(d) for which a 3-cut sequence with non-degenerate regions exists), and the "Outside ⋃_k V(b_k)" sub-case of Phase 1 (where the last cut falls outside dom(M(d)) and triggers the empty-right-exterior trace recorded in R-BLK).

Let document d have subspace S = 1 with V_S(d) = {[1,1], [1,2]} (so N = max{ord(v) : v ∈ V_S(d)} = 2), and let the arrangement be:

```
M(d)([1,1]) = 3.0.1.0.1.0.1.1    (I-address A)
M(d)([1,2]) = 5.0.2.0.1.0.1.1    (I-address B)
```

Content A originates from document 3.0.1.0.1; B from document 5.0.2.0.1. The canonical run partition has two width-1 runs: b₁ = ([1,1], A, 1) and b₂ = ([1,2], B, 1) — distinct origins prevent any merge in the pre-state.

We apply a 3-cut pivot with K = ([1,1], [1,2], [1,3]): c₀ = [1,1], c₁ = [1,2], c₂ = [1,3] = [S, N + 1]. The affected range [c₀, c₂) at depth 2 in subspace 1 covers ordinals {1, 2}; under D-SEQ (V_S(d) = {[1,1], [1,2]}), this is exactly V_S(d). Region α = {[1,1]} (w_α = 1), region β = {[1,2]} (w_β = 1). Both exteriors are *empty*: the left exterior {v ∈ V_S(d) : v < c₀} is empty because ord(c₀) = 1 = min{ord(v) : v ∈ V_S(d)}; the right exterior {v ∈ V_S(d) : v ≥ c₂} is empty because ord(c₂) = 3 > N = 2.

**R-PRE verification.** (i) M(d) well-defined. (ii) V_S(d) = {[1,1], [1,2]} ≠ ∅. (iii) CS1: n = 3; CS2: [1,1] < [1,2] < [1,3]; CS3: all subspace 1; CS4: all depth 2. (iv) The positions with subspace 1, depth 2, and ordinal in [1, 3) are exactly [1,1] and [1,2], both in V_S(d); the bound v < c₂ is exclusive, so c₂ = [1,3] is not required to be in V_S(d) — and indeed it is not. Width positivity: w_α = 1 ≥ 1, w_β = 1 ≥ 1 (consequence). ✓

**Applying the postconditions.** Both exteriors are empty, so R-EXT contributes no equations; the entire V_S(d) is covered by R-P1 and R-P2.

R-P1 (j = 0): M'(d)(c₀ + 0) = M'(d)([1,1]) = M(d)(c₁ + 0) = M(d)([1,2]) = B.

R-P2 (j = 0): M'(d)(c₀ + 1 + 0) = M'(d)([1,2]) = M(d)(c₀ + 0) = M(d)([1,1]) = A.

**Result:**

```
M'(d)([1,1]) = B     (was β at c₁, pivoted to c₀)
M'(d)([1,2]) = A     (was α at c₀, pivoted past β to c₀ + w_β)
```

The pivot reduces to a transposition of the two V-positions. No position is fixed by π (a *pure* swap with no exterior anchor).

**R-PPERM verification.** The permutation π: π([1,1]) = c₀ + w_β + 0 = [1,2] (α: j = 0). π([1,2]) = c₀ + 0 = [1,1] (β: j = 0). Bijectivity: π is an involution ((π ∘ π)([1,1]) = π([1,2]) = [1,1], symmetrically for [1,2]). Check: M'(d)(π([1,1])) = M'(d)([1,2]) = A = M(d)([1,1]) ✓. M'(d)(π([1,2])) = M'(d)([1,1]) = B = M(d)([1,2]) ✓.

**R-RI verification.** ran(M'(d)) = {B, A} = {A, B} = ran(M(d)) ⊆ dom(C) = dom(C'). ✓

**Displacement verification.** Δ([1,1]) = +(2 − 1) = +1 = +w_β (α-branch, j = 0). Δ([1,2]) = −(2 − 1) = −1 = −w_α (β-branch, j = 0). Δ is uniformly +1 on α and uniformly −1 on β, confirming R-DISP at minimum width. No position receives Δ = 0 — both exterior regions are empty, so the (0, 0) branch fires nowhere on V_S(d).

**Run decomposition via R-BLK.** *Phase 1 (Split):* c₀ = [1,1] coincides with b₁'s V-start ([1,1]) — boundary case, no split. c₁ = [1,2] coincides with b₂'s V-start ([1,2]) — boundary case, no split. c₂ = [1,3] = [S, N + 1] falls *outside* ⋃_k V(b_k): every run b_k in the partition of V_S(d) has V-extent V(b_k) ⊆ V_S(d) = {[1,1], [1,2]}, so max{ord(v) : v ∈ V(b_k)} ≤ 2 < 3 = ord(c₂), hence c₂ ∉ V(b_k) for every k. This is the *empty right exterior* sub-case described in Phase 1 ("Outside ⋃_k V(b_k)"); no split occurs at c₂, no run is bisected by c₂, and the right-exterior region {v ∈ V_S(d) : v ≥ c₂} contains zero V-positions. Post-split partition: {([1,1], A, 1), ([1,2], B, 1)} — identical to the pre-state partition, since every cut fell at a run boundary or outside V_S(d).

*Phase 2 (Classify):* ([1,1], A, 1) has V-extent {[1,1]} with ord = 1 in [ord(c₀), ord(c₁)) = [1, 2), so it lies in *α*. ([1,2], B, 1) has V-extent {[1,2]} with ord = 2 in [ord(c₁), ord(c₂)) = [2, 3), so it lies in *β*. No run is classified into the left exterior (empty) or the right exterior (empty). The non-S region is also empty (every V-position has subspace 1 = S). Every run is classified into α or β.

*Phase 3 (Reassemble):* Apply π to each run's V-start.

- ([1,1], A, 1) → (π([1,1]), A, 1) = ([1,2], A, 1) (α-branch of R-PPERM with j = 0 gives π([1,1]) = c₀ + w_β + 0 = [1,2]).
- ([1,2], B, 1) → (π([1,2]), B, 1) = ([1,1], B, 1) (β-branch of R-PPERM with j = 0 gives π([1,2]) = c₀ + 0 = [1,1]).

Sorted by V-start: {([1,1], B, 1), ([1,2], A, 1)}. *S8-cons verification:* both runs are width 1, so S8-cons holds trivially at the lone offset k = 0 (M'(d)([1,1]) = B = B + 0; M'(d)([1,2]) = A = A + 0).

*Merge check:* ([1,1], B, 1) and ([1,2], A, 1) are V-adjacent (1 + 1 = 2) but not I-adjacent (origin(B) = 5.0.2.0.1 ≠ origin(A) = 3.0.1.0.1, so B + 1 ≠ A). No mergeable pair.

**Canonical partition:** {([1,1], B, 1), ([1,2], A, 1)}. The rearrangement exchanges the two positions across the cut sequence; both runs remain width-1, no merges arise, and the canonical decomposition of M'(d) coincides with the post-Phase-3 partition. The example confirms three structural edges of R-BLK simultaneously: (a) the minimum w_α = w_β = 1 still admits valid Phase-2 classification (α and β each receive exactly one run); (b) the empty-right-exterior dispatch in Phase 1 fires correctly at c₂ = [S, N + 1] (the "Outside ⋃_k V(b_k)" sub-case), with no run bisected and no right-exterior classification; (c) Phase 3 reassembles via π alone at minimum size, with the I-start and width of each run preserved verbatim and the V-starts transposed by the explicit R-PPERM formulas.


## Properties Introduced

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| CutSequence | DEF | Tuple (c₀, ..., c_{n−1}) with n ∈ {3,4}, strictly ordered, same subspace, depth 2 (CS1–CS4) | introduced |
| RegionPartition | DEF | Partition of affected range into regions α, β (3-cut) or α, μ, β (4-cut) by cut positions | introduced |
| R-PRE | DEF | Precondition: M(d) exists, V_S(d) non-empty, cuts satisfy CS1–CS4, affected range covered, every region non-empty (w_α, w_β ≥ 1 in both forms; w_μ ≥ 1 when n = 4) | introduced |
| PivotPostcondition | DEF | 3-cut rearrangement: β content placed at c₀, then α content, exterior unchanged (R-EXT, R-P1, R-P2) | introduced |
| SwapPostcondition | DEF | 4-cut rearrangement: β at c₀, then μ, then α, exterior unchanged (R-EXT, R-S1, R-S2, R-S3) | introduced |
| REARRANGE_K | OPERATION | State transition Σ → Σ' parameterized by cut sequence K and document d; precondition R-PRE(K); postcondition PivotPostcondition (n=3) or SwapPostcondition (n=4) plus frame conditions R-FRAME-P or R-FRAME-S | introduced |
| ArrangementRearrangement | DEF | State transition with dom(M'(d)) = dom(M(d)), C' = C, M'(d') = M(d') for d' ≠ d, and bijection π with M'(d)(π(v)) = M(d)(v) | introduced |
| PermutationDisplacement | DEF | Signed magnitude Δ(v) ∈ {+, −, 0} × ℕ recording the ordinal shift from v to π(v); (+)/(−) branches restricted to v ∈ V_S(d) so the truncated subtraction operates on single-component depth-2 ordinals, non-S positions fixed to (0, 0) by convention | introduced |
| R-DISP | LEMMA | For all v₁, v₂ in the same region, Δ(v₁) = Δ(v₂); common value determined by region widths alone | introduced |
| Split | DEF | Correspondence run (v, a, n) at interior offset c yields (v, a, c) and (v + c, a + c, n − c) | introduced |
| Merge | DEF | V-adjacent and I-adjacent correspondence runs (v₁, a₁, n₁), (v₂, a₂, n₂) combine to (v₁, a₁, n₁ + n₂) | introduced |
| CanonicalRunDecomposition | DEF | Unique partition of dom(M(d)) into maximal correspondence runs — no two V-adjacent, I-adjacent runs remain unmerged | introduced |
| R-PIV | LEMMA | Pivot postcondition is a total function on dom(M(d)) | supporting |
| R-SWP | LEMMA | Swap postcondition is a total function on dom(M(d)) | supporting |
| R-PPERM | LEMMA | Bijection π for 3-cut pivot: α shifts forward by w_β, β shifts backward by w_α | introduced |
| R-SPERM | LEMMA | Bijection π for 4-cut swap: α shifts forward by w_β + w_μ, μ shifts by w_β − w_α, β shifts backward by w_α + w_μ | introduced |
| R-FRAME-P | FRAME | Pivot: other subspaces, other documents, and content store are preserved | introduced |
| R-FRAME-S | FRAME | Swap: other subspaces, other documents, and content store are preserved | introduced |
| R-NS | LEMMA | REARRANGE_K is the identity on dom(M(d)) \ V_S(d): π fixes non-S positions pointwise (NS-π), non-S runs carry verbatim into B' (NS-run), and ASN-0036 invariants on non-S positions transport trivially (NS-inv) | introduced |
| R-RI | LEMMA | Rearrangement preserves S3 (referential integrity): ran(M'(d)) = ran(M(d)) ⊆ dom(C) = dom(C') | introduced |
| R-COMM | LEMMA | π(v + k) = π(v) + k when v and v + k lie in the same region: cut-point permutation commutes with ordinal shift | introduced |
| R-BLK | LEMMA | Run partition transforms by split-at-cuts then displace-per-region, preserving S8-uniq/S8-cons under M'(d) | introduced |
| R-SP | LEMMA | R-PRE(K) ∧ pre-state ASN-0036 invariants ∧ pre-state run partition B is sufficient for REARRANGE_K to establish ASN-0036 invariants on M'(d) with B' = R-BLK(B) as the constructive S8 witness (sufficiency only; necessity not claimed) | introduced |


## Open Questions

Does the 4-cut swap definition generalize to k-cut rearrangements for k > 4, and if so, what is the natural class of permutations that "rearrangement by cut points" can express?

What must a well-formed editing sequence guarantee about the composition of multiple rearrangements — is the composition of two rearrangements always expressible as a single rearrangement, or can sequences of rearrangements produce arrangements unreachable by any single operation?

Under what conditions can a rearrangement cause the number of correspondence runs in the canonical partition to increase, and is there an upper bound on the increase relative to the number of cut points?

What constraints, if any, must cut points satisfy relative to the run boundaries of the canonical partition, or are arbitrary cut positions within the V-span always valid?
