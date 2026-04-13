# Cross-cutting Review — ASN-0036 (cycle 2)

*2026-04-12 18:18*

I've read the full ASN-0036 against its foundation statements, tracing every citation, precondition chain, and definition across all properties. Here are three new findings.

---

### S8 proof applies TA5 properties (defined for `inc`) to `shift` results via an unstated equivalence

**Foundation**: TA5 (HierarchicalIncrement) — defines `inc(t, k)` and its properties (a)–(d). OrdinalShift (ShiftDefinition) — defines `shift(v, n) = v ⊕ δ(n, m)` via TumblerAdd. TS4 (ShiftStrictIncrease) — `shift(v, n) > v`.

**ASN**: S8 (Finite span decomposition), uniqueness proof: "By S8a, `zeros(v) = 0`, so every component of `v` is nonzero and `sig(v) = … = m`. By TA5(c), `v + 1 = inc(v, 0)` satisfies `#(v + 1) = m` and differs from `v` only at position `m`." And cross-subspace at m ≥ 2: "since `sig(v) = m ≥ 2`, TA5(b) gives `(v + 1)ᵢ = vᵢ` for all `i < sig(v)`."

**Issue**: S8-depth defines `v + 1 = shift(v, 1) = v ⊕ δ(1, #v)` (via TumblerAdd), while `inc(v, 0)` is a separate operation defined by TA5 (direct component modification at `sig(v)`). The proof asserts `v + 1 = inc(v, 0)` and then applies TA5(a), TA5(b), TA5(c) — all properties of `inc` — to characterize `shift` results. For S8a-satisfying tumblers these operations coincide (both advance the last component by 1), but this equivalence is never stated or derived. Every TA5 fact the proof cites has a direct counterpart in the shift/TumblerAdd framework: TS4 gives `shift(v, 1) > v`, OrdinalShift's postcondition gives `#shift(v, 1) = #v`, and TumblerAdd's copy rule gives `shift(v, 1)ᵢ = vᵢ` for `i < m`. The bridge is both unstated and unnecessary — the proof introduces a dependency on an unproven lemma when the required facts are directly available from shift's own properties.

**What needs resolving**: Either establish that `shift(v, 1) = inc(v, 0)` for S8a-satisfying tumblers as an explicit lemma (bridging TumblerAdd and TA5), or rewrite S8's proof to cite TumblerAdd/OrdinalShift/TS4 directly rather than routing through TA5.

---

### S3 formal contract claims derivability from S1, but proof requires an unstated operation-level constraint

**Foundation**: S0 (Content immutability), S1 (Store monotonicity) — `dom(Σ.C) ⊆ dom(Σ'.C)`.

**ASN**: S3 (Referential integrity), formal contract: "*Preconditions:* S1 (store monotonicity) holds for the system. *Invariant:* `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))` for every reachable state Σ." Proof, exhaustiveness: "An operation mapping to an address in neither set … would yield `a ∉ dom(Σ'.C)`, violating the invariant. Such an operation is excluded by S3's status as a design requirement."

**Issue**: S3's formal contract presents it as an invariant with S1 as its sole precondition, implying S3 is derivable from S1. It is not. A system satisfying S0 and S1 can violate S3: start from Σ₀ with empty content store and arrangements; perform a transition that adds `M(d)(v) = a` where `a` is never allocated; S0 holds vacuously (no existing content to preserve), S1 holds (dom(C) doesn't shrink), but `a ∉ dom(Σ'.C)`, violating S3. The proof acknowledges this by invoking "S3's status as a design requirement" to exclude the non-conforming fourth case — making the argument self-referential. S3 has the same logical status as D-CTG: a design constraint on operations with per-operation verification obligations. D-CTG is correctly classified as an axiom; S3 is misclassified as an invariant derivable from S1. S8-fin, which has the same inductive structure, avoids this by listing no preconditions — it doesn't claim derivability from another property.

**What needs resolving**: S3's formal contract must either (a) classify S3 as an axiom/design requirement with per-operation verification obligations (parallel to D-CTG), or (b) add the operation-level constraint — that every transition mapping `v` to `a` satisfies `a ∈ dom(Σ'.C)` — as an explicit precondition alongside S1.

---

### D-MIN postcondition depends on m ≥ 2 (S8-vdepth) without declaring it

**Foundation**: S8-vdepth (MinimalVPositionDepth) — `(A d, v : v ∈ dom(Σ.M(d)) : #v ≥ 2)`.

**ASN**: D-MIN (VMinimumPosition), formal contract: "*Postconditions:* Combined with D-CTG and S8-fin, `V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}` for some finite n ≥ 1." The inline derivation: "By D-CTG combined with S8-fin and S8-depth (when m ≥ 3) or trivially (when m = 2, there is only one post-subspace component)…"

**Issue**: The characterization `V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}` uses a notation where `S` occupies position 1 and `k` occupies position `m`. This requires `m ≥ 2` — at `m = 1`, positions 1 and `m` coincide, `S` and `k` occupy the same component, and the notation is ill-formed (D-SEQ explicitly acknowledges this: "at m = 1 the tuple `[S, 1, …, 1, k]` collapses to a single component"). The inline derivation handles `m = 2` and `m ≥ 3` but silently excludes `m = 1`, relying on a bound that comes from S8-vdepth. D-MIN's formal contract lists `S8-depth` and `S8a` as preconditions and "D-CTG and S8-fin" as combining properties for the postcondition, but does not list S8-vdepth. D-SEQ, which formalizes the same characterization, correctly cites S8-vdepth for `m ≥ 2` in its preconditions — but D-MIN's postcondition derives the result independently without inheriting that dependency.

**What needs resolving**: D-MIN's postcondition must declare its dependency on S8-vdepth (for the `m ≥ 2` lower bound), either by adding S8-vdepth to the "Combined with" list or by noting `m ≥ 2` as a precondition of the postcondition's derivation.
