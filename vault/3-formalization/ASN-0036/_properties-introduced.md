## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.C | Content store: `T ⇀ Val`, mapping I-addresses to content values | introduced |
| Σ.M(d) | Arrangement for document `d`: `T ⇀ T`, mapping V-positions to I-addresses | introduced |
| S0 | Content immutability: `a ∈ dom(C) ⟹ a ∈ dom(C') ∧ C'(a) = C(a)` for all transitions | design requirement; motivated by NoDeallocation (ASN-0034) |
| S1 | Store monotonicity: `dom(C) ⊆ dom(C')` for all transitions | from S0 |
| S2 | Arrangement functionality: `M(d)` is a function — each V-position maps to exactly one I-address | axiom |
| S3 | Referential integrity: `(A d, v : v ∈ dom(M(d)) : M(d)(v) ∈ dom(C))` | design; uses NoDeallocation (ASN-0034) |
| AX-2 | Allocation-mediated entry: content-creation transitions are T10a-conforming allocation events; corollary: `dom(Σ.C) ⊆ allocated(s)` | axiom |
| AX-3 | Infinite type domains: `Doc` and `VPos(S)` are countably infinite — carrier sets for the state model | axiom |
| S4 | Origin-based identity: distinct allocations produce distinct I-addresses regardless of value equality | from GlobalUniqueness, T3, AX-2 (ASN-0034) |
| S5 | Unrestricted sharing: S0–S3 do not entail any finite bound on sharing multiplicity | consistent with S0, S1, S2, S3 |
| S6 | Persistence independence: named restatement of S1 — labels the anti-GC commitment | restatement of S1 |
| S7a | Document-scoped allocation: every I-address is allocated under the originating document's prefix | design; uses Prefix, T4, T4c (ASN-0034) |
| S7b | Element-level I-addresses: `(A a ∈ dom(C) :: zeros(a) = 3)` | design; uses T4 (ASN-0034) |
| S7c | Element-field depth: `(A a ∈ dom(C) :: #fields(a).element ≥ 2)` — subspace identifier and content ordinal occupy distinct components | design; uses S7b, T4, TA7a (ASN-0034) |
| S7 | Structural attribution: `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)` — full document prefix | from S7a, S7b, S0, S4, T4, T3, GlobalUniqueness (ASN-0034) |
| S7e | Origin discriminates documents: for `a₁, a₂` under distinct documents (D-DOC), `origin(a₁) ≠ origin(a₂)` | from S7d, D-DOC, GlobalUniqueness (ASN-0034), origin(a) |
| S8-fin | Finite arrangement: `dom(M(d))` is finite for every document `d` | design requirement |
| S8a | V-position well-formedness: `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1)` — standalone constraint on V-position components; `v₁ ≥ 1` is a consequence of `zeros(v) = 0`, stated for S8's partition proof | design requirement |
| S8-depth | Fixed-depth V-positions: `(A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)` | design; uses OrdinalShift, TumblerAdd (ASN-0034) |
| S8 | Span decomposition: `dom(M(d))` decomposes into finitely many correspondence runs `(vⱼ, aⱼ, nⱼ)` with `M(d)(vⱼ + k) = aⱼ + k` for `0 ≤ k < nⱼ` | theorem from S8-fin, S2, S8a, S8-depth, T1, T3, T5, T10, TA5 (ASN-0034) |
| E₁(a) | Element subspace projection: E₁(a) = fields(a).element₁ for a with zeros(a) = 3 | introduced |
| ord(v) | Ordinal extraction: ord(v) = [v₂, ..., vₘ]; when v satisfies S8a, ord(v) ∈ S | introduced |
| vpos(S, o) | V-position reconstruction: vpos(S, o) = [S, o₁, ..., oₖ]; inverse of ord for any o ∈ T; satisfies S8a when S ≥ 1 and all oᵢ > 0 | introduced |
| w_ord | Ordinal displacement projection: w_ord = [w₂, ..., wₘ] for displacement w with w₁ = 0 | introduced |
| OrdAddHom | (a) ord(v ⊕ w) = ord(v) ⊕ w_ord; (b) subspace(v ⊕ w) = subspace(v); (c) v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord) | lemma from ord, w_ord, TumblerAdd, TA0 (ASN-0034) |
| OrdAddS8a | v ⊕ w satisfies S8a ⟺ all tail components of w after the action point are positive; equivalently ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a | lemma from OrdAddHom, S8a, TumblerAdd (ASN-0034) |
| OrdShiftHom | ord(shift(v, n)) = shift(ord(v), n); shift(v, n) unconditionally satisfies S8a when v does | corollary from OrdAddHom, OrdAddS8a, OrdinalShift, OrdinalDisplacement (ASN-0034) |
| D-CTG | V-position contiguity: within each subspace, V-positions form a contiguous ordinal range with no gaps — design constraint on well-formed document states | design; uses T0(a), T1, T3 (ASN-0034) |
| D-MIN | V-position minimum: min_S(d) = min(V_S(d)), the T1-least element of V_S(d) — pure definition, membership trivial | definition |
| AX-6 | Minimum presence: V_S(d) ≠ ∅ ⟹ [S, 1, …, 1] ∈ V_S(d) — design constraint on operations | design requirement |
| D-MIN-VAL | Minimum position value: min_S(d) = [S, 1, …, 1] — characterizes the value of the minimum | from D-MIN, AX-6, S8a, T1, T3 (ASN-0034) |
| D-CTG-depth | Shared prefix reduction: at depth m ≥ 3, contiguity reduces to the last component (all positions share components 2 through m − 1) | corollary of D-CTG, S8-fin, S8-depth, T0(a), T1, T3 (ASN-0034) |
| D-SEQ | Sequential positions (m ≥ 2): non-empty V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n} for some n ≥ 1 | from D-CTG, D-CTG-depth, D-MIN, D-MIN-VAL, AX-6, S8-fin, S8-depth, T1 (ASN-0034) |
| ValidInsertionPosition | given depth m ≥ 2: if V_S(d) ≠ ∅, m equals common depth and v = min(V_S(d)) or v = shift(min(V_S(d)), j) with 1 ≤ j ≤ N; if V_S(d) = ∅, v = [S, 1, ..., 1] of depth m | introduced |
| S9 | Two-stream separation: arrangement changes cannot alter stored content | theorem from S0 |
