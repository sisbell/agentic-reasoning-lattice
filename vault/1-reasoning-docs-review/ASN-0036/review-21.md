## Foundation Consistency Check: ASN-0036

### 1. Stale Labels

(none)

### 2. Local Redefinitions

(none)

### 3. Structural Drift

(none)

### 4. Missing Dependencies

(none) — Every cited property (T2, T3, T4, T5, T8, T9, T10, T10a, TA5(c), TA7a, OrdinalShift, and the ordinal-displacement arithmetic) belongs to ASN-0034, which is the only declared dependency.

### 5. Exhaustiveness Gaps

(none)

### 6. Registry Mismatches

**Finding 1 — D-CTG-depth: T0(a) used in proof but absent from dependency list.**

The properties table records D-CTG-depth as:

> `corollary from D-CTG, S8-fin, S8-depth`

The body proof of D-CTG-depth explicitly cites T0(a) (UnboundedComponentValues) to complete the contradiction:

> "By T0(a), unboundedly many values of n exist, yielding infinitely many distinct positions in V_S(d) — contradicting S8-fin."

T0(a) is load-bearing here: the construction produces a position `w` whose (j+1)-th component takes any value `n > (v₁)_{j+1}`, and T0(a) is what guarantees unboundedly many such `n` exist. Without it the argument obtains only finitely many positions. T0(a) should appear in the dependency list.

---

**Finding 2 — D-SEQ: body cites D-CTG-depth directly; table skips it and lists D-CTG instead.**

The properties table records D-SEQ as:

> `corollary from D-CTG, D-MIN, S8-fin, S8-depth`

The body proof of D-SEQ opens by invoking the intermediate corollary explicitly:

> "By D-CTG-depth (when m ≥ 3) or trivially (when m = 2, there is only one post-subspace component), all positions in V_S(d) share components 2 through m − 1."

The table skips D-CTG-depth and instead lists its own source (D-CTG) as a direct dependency of D-SEQ. Since D-CTG-depth is a named result that the proof cites by name, it should appear in the D-SEQ dependency list; D-CTG should appear as a dependency of D-CTG-depth (where it already does), not as a substitute citation here.

---

`RESULT: 2 FINDINGS`
