I walked the foundation exports, then read ASN-0036 as a system: the two-stream invariants (S0–S8), the text-subspace contiguity chain (V-sub → D-CTG → D-CTG-depth → D-MIN → D-SEQ), the shift-homomorphism bridge (OrdShiftHom), the structural-attribution stack (S7/S7a/S7b/S7d), and the insertion-position predicates.

The core mathematics holds. D-CTG-depth's two-part argument (shared-prefix contradiction via T0(a)/S8-fin, then the betweenness reduction) is sound, including the load-bearing shared-prefix conjunct. D-SEQ's four-step assembly correctly composes contiguity with finiteness, with the m=2 / m≥3 split handled. S7's `origin(a)` well-definedness — T4-validity from S7a+T10a.4, the `zeros(origin(a)) = 2` computation, the two-separator distinctness/non-adjacency, document-level placement, and cross-document uniqueness via S7d→GlobalUniqueness — checks out. S8's `succ` partition (injective + acyclic + finite ⟹ disjoint paths), the i=0/i≥1 TS3 split, and the depth handling are correct; I confirmed the previously-declined S8 depth-step is now routed through `shift`'s frame (OrdShiftHom/TA0), not S8-depth, so I did not re-raise it. Precondition chains for OrdShiftHom (m≥2, n≥1) are met at every call site.

The findings below are one real grounding gap that crosses claim boundaries, plus presentation issues that the precise reader has to work around.

### ValidInsertionPosition leaves N = |V_1(d)| ungrounded
**Class**: REVISE
**Foundation**: NAT-card (NatFiniteSetCardinality) — its `|·|` is posited only for subsets of an initial segment `{j ∈ ℕ : 1 ≤ j ≤ n}`; D-SEQ (SequentialPositions, this ASN); S8-fin (FiniteArrangement, this ASN)
**ASN**: ValidInsertionPosition — "Setting `N = |V_1(d)|`, the predicate holds iff `v = min(V_1(d))` or `v = shift(min(V_1(d)), j)` for some `j ∈ {1, ..., N}`." Its Depends lists only S8-depth, S8a, D-MIN, OrdinalShift, OrdShiftHom, T3, NAT-order — no S8-fin, no D-SEQ, no NAT-card.
**Issue**: `N = |V_1(d)|` is load-bearing: it bounds the index set `{1,…,N}` and fixes the "exactly `N+1` pairwise-distinct positions" postcondition. For `N ∈ ℕ` the claim needs (i) `V_1(d)` finite (S8-fin) and (ii) a cardinality grounding. NAT-card — the only cardinality primitive — is scoped to subsets of `{1,…,n}`; `V_1(d)` is a set of tumblers, not such a subset, so NAT-card does not apply to it directly (contrast S8a, which carefully notes its index set *is* a `{1,…,#t}`-subset before invoking NAT-card). The clean grounding is D-SEQ, which gives `V_1(d) = {[1,…,1,k] : 1 ≤ k ≤ n}` and hence the bijection `[1,…,1,k] ↦ k` onto `{1,…,n}`, so `|V_1(d)| = n` — but D-SEQ is not cited. The chain establishing `N ∈ ℕ` is broken.
**What needs resolving**: ground `N = |V_1(d)|` as a natural — cite D-SEQ (which supplies the sequential form `V_1(d) ≅ {1,…,n}`, grounding both finiteness and `|V_1(d)| = n` via NAT-card), or equivalently define `N` as D-SEQ's `n`; add the missing dependency edge(s).

### S5's sharing-multiplicity uses the same ungrounded |·|
**Class**: OBSERVE
**Foundation**: NAT-card (NatFiniteSetCardinality) — scoped to `{1..n}`-subsets
**ASN**: S5 — postcondition `|{(d, v) : v ∈ dom(Σ.M(d)) ∧ Σ.M(d)(v) = a}| > N` and proof "the sharing multiplicity of `a` in `Σ_N` is `|{(d, v) : ...}| = N + 1`". Depends: S0, S1, S2, S3, T3 — no NAT-card.
**Issue**: same root as the ValidInsertionPosition finding — `|·|` is applied to a set of `(d,v)` pairs, not an initial-segment subset, so NAT-card does not directly ground it. Milder here because the construction exhibits `N+1` explicitly indexed distinct pairs (`i ↦ (dᵢ, v)` / `k ↦ (d, vₖ)`), so the value is grounded by that injection — but the injection-to-cardinality step is not cited.
**What needs resolving**: ground the multiplicity by citing NAT-card via the explicit indexing bijection `{1,…,N+1} →` the constructed family, or state the injection `{1,…,N+1} ↪ {(d,v):…}` that forces `|·| > N`.

### S7 re-derives the separator arithmetic four times over
**Class**: OBSERVE
**Foundation**: NAT-addassoc, NAT-addcompat, NAT-sub, NAT-order — the chain showing the two zero separators of `origin(a)` are distinct and non-adjacent
**ASN**: S7 — the derivation that `#N(a)+1 < ((#N(a)+1)+#U(a))+1` with difference `#U(a)+1 ≥ 2` appears in full in the Well-definedness proof, then verbatim again in the Postconditions ("distinct because the second strictly exceeds the first: from the additive form … NAT-addcompat's strict successor gives … their difference is `#U(a) + 1 ≥ 2`"), then again spread across the NAT-order, NAT-addcompat, NAT-addassoc, and NAT-sub entries of Depends.
**Issue**: the identical arithmetic is stated four times; the Depends entries in particular are full re-derivations (use-site inventories), not dependency descriptions. This is exactly the sprawl that degrades review capability — verifying the claim means reconciling four copies of one fact.
**What needs resolving**: derive separator distinctness/non-adjacency once in the proof; have Postconditions assert the result (origin(a) T4-valid, document-level) and have each Depends entry name its role in one line rather than re-running the derivation.

### Citation-justification meta-prose in S7d and S7 dependency slots
**Class**: OBSERVE
**Foundation**: n/a (Depends-slot prose)
**ASN**: S7d's T4 entry — "T10a's discipline preserves T4-validity but does not itself define `zeros`; the direct appearance of `zeros` in S7d's statement therefore requires this first-order citation, as in S7b and S7…"; S7's Σ.C entry — "Σ.C is reachable transitively through S7a and S7b … but S7's direct use of the symbol … is what obliges the direct citation, so that the dependency specification is self-contained."
**Issue**: this prose explains *why a citation is made* (citation hygiene, self-containment) rather than *what the dependency supplies* — the reviser-drift pattern the review brief calls out as compounding across cycles. It is noise in a structural slot.
**What needs resolving**: trim each entry to the content it provides (T4 supplies `zeros`; Σ.C supplies the content store and `dom(Σ.C)`); drop the "therefore requires this first-order citation" / "obliges the direct citation, so that the dependency specification is self-contained" justifications.

VERDICT: REVISE