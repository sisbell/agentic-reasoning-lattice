Reading through the foundation statements, then the ASN claims, then the D-CTG-depth proof structure.

The foundation layer is internally consistent: NAT-carrier → NAT-zero/NAT-order/NAT-closure → NAT-addcompat/NAT-discrete/NAT-wellorder/NAT-card → T0 → T1/T3/T4 → T0(a). The companion-relation definitions in NAT-order, the ≤-transitivity consequence, the no-interval form in NAT-discrete, and the strictly-increasing-enumeration characterisation in NAT-card all check out.

The design posits D-CTG, S8a, S8-fin, and subspace are structurally sound — each cites only what their formal statement actually consumes. V-sub's definition is a clean restriction of Σ.M(d) by the subspace projection. Σ.M(d) is an unresolved dependency from outside this ASN; its minimality here is intentional.

D-CTG-depth's proof logic is mostly sound. The NAT-wellorder invocation to extract the first interior disagreement j, the T1-witness pinning argument (k = j by bracketing k ≥ j and k ≤ j), the w construction, the u < w branch via T1(i) at witness j+1, the w < x branch via T1(i) at witness j (with j < m derived from NAT-addcompat plus transitivity), the D-CTG invocation requiring w ∈ T (met by T0 comprehension), the zeros(w) = 0 discharge through S8a positivity and NAT-card's empty-set characterisation, and the infinite-sequence extraction via T0(a) iterating bounds — all walk correctly. Three issues remain.

---

### S8-depth Formal Contract missing Axiom entry
**Class**: REVISE
**Foundation**: D-CTG (VContiguity), S8a (ArrangementDomainRestriction), S8-fin (FiniteArrangement) — all three analogous posits carry an explicit Axiom entry with "For every reachable state Σ and every document d" before the formal statement
**ASN**: S8-depth Formal Contract section — the section contains only a Depends list; the formal posit `(A d, u, w : u ∈ dom(Σ.M(d)) ∧ w ∈ dom(Σ.M(d)) ∧ subspace(u) = subspace(w) : #u = #w)` appears in the narrative prose, not in a structured Axiom field
**Issue**: S8-depth is a protocol posit on the same footing as D-CTG, S8a, and S8-fin, all of which place their formal statement in an Axiom entry that opens with "For every reachable state Σ and every document d." S8-depth's Formal Contract omits this entry entirely. The formal statement as given in the prose has Σ as a free variable — the reachable-state quantification that is explicit in every peer posit is absent from the contract section that downstream consumers and formalization tools read as authoritative. A consumer reading only the Formal Contract finds the Depends list but no formal statement to bind.
**What needs resolving**: Add an Axiom entry to S8-depth's Formal Contract that begins "For every reachable state Σ and every document d" and reproduces the formal statement `(A d, u, w : u ∈ dom(Σ.M(d)) ∧ w ∈ dom(Σ.M(d)) ∧ subspace(u) = subspace(w) : #u = #w)` in the same structural position that D-CTG, S8a, and S8-fin use for their posits.

---

### NAT-discrete citation vestigial in D-CTG-depth
**Class**: REVISE
**Foundation**: NAT-discrete (NatDiscreteness) — axiom: `m < n ⟹ m + 1 ≤ n`; NAT-addcompat (NatAdditionOrderAndSuccessor) — axiom: `n < n + 1`
**ASN**: D-CTG-depth Depends list entry for NAT-discrete: *"supplies the discreteness of ℕ, the axiom `j < m ⟹ j + 1 ≤ m`, the forward direction of the equivalence between the additive interior bound `j + 1 ≤ m` and the strict comparison `j < m` on ℕ"*
**Issue**: The Depends entry itself correctly attributes the backward direction `j + 1 ≤ m ⟹ j < m` to NAT-addcompat (`j < j + 1` at `n := j`, chained with transitivity). That backward direction is what the w < x branch consumes. The w > u branch uses `j + 1 ≤ m` directly from the interior-range premise. No proof step goes from `j < m` to `j + 1 ≤ m` — the interior range supplies `j + 1 ≤ m` as a direct premise; there is no point where the proof first derives `j < m` and then needs to recover `j + 1 ≤ m`. The forward direction of NAT-discrete is not consumed anywhere, making the citation vestigial.
**What needs resolving**: Either identify the specific proof step that consumes NAT-discrete's forward direction `j < m ⟹ j + 1 ≤ m` and make it explicit in the proof body, or remove NAT-discrete from D-CTG-depth's Depends list if no such step exists.

---

### D-CTG-depth proof only closes the u < x case; postcondition is universal
**Class**: REVISE
**Foundation**: T1 (LexicographicOrder) — Postcondition (b): exactly-one trichotomy on T
**ASN**: D-CTG-depth proof body: *"Suppose for contradiction that V_1(d) contains two positions u and x with u < x (both depth m) that disagree somewhere in the interior range"*; Postcondition: `(A u, x : u ∈ V_1(d) ∧ x ∈ V_1(d) : (A i : 2 ≤ i ∧ i + 1 ≤ m : u_i = x_i))`
**Issue**: The contradiction is set up specifically for u < x. Negating the postcondition yields: there exist u, x ∈ V_1(d) with an interior disagreement. T1's trichotomy on T gives exactly three cases for any such pair: u < x, u = x, or x < u. The u = x case is trivially consistent with agreement. The u < x case is closed by the proof. The x < u case is not addressed — the proof neither invokes "WLOG u < x" (citing T1's trichotomy and symmetry of the disagreement predicate to collapse both ordered cases into one), nor runs the symmetric argument with u and x relabeled. The final claim "therefore no two positions in V_1(d) can disagree at any component j" asserts more than has been established: only that no pair with u < x can disagree; the pair with u > x is left open.
**What needs resolving**: Either add an explicit WLOG sentence that invokes T1's trichotomy on T to collapse the x < u case into the u < x case by relabeling (and notes that the disagreement predicate and the construction are symmetric under this relabeling), or close the x < u case explicitly with the symmetric sub-argument.

VERDICT: REVISE