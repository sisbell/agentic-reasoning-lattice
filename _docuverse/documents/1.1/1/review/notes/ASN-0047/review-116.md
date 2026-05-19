# Review of ASN-0047

## REVISE

### Issue 1: C-fin missing from ExtendedReachableStateInvariants

**ASN-0047, Extended reachable-state invariants**: The Class (a) per-state invariant conjunct list enumerates `S2 ∧ S3★ ∧ ... ∧ S8-fin ∧ ... ∧ L-fin ∧ ...` but omits C-fin (ContentStoreFiniteness).

**Problem**: The K.α subsequent-emission case formula `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)` requires the indexed set to be finite for `max` to be well-defined. Finiteness of dom(C) is load-bearing for this operation but never named as a per-state invariant. ASN-0093 has C-fin as a foundation invariant, but the explicit list here is otherwise exhaustive (L-fin is included; S8-fin is included).

**Required**: Add C-fin to the per-state invariant conjunct in ExtendedReachableStateInvariants and to the verification matrix, with the discharge "extends dom(C) by one (finite + 1 = finite)" under K.α, frame elsewhere.

### Issue 2: L1c attribution misplaced

**ASN-0047, Properties Introduced, "Local extensions and strengthenings"**: "L1c (structural inc-chain) | Local weakening of ASN-0043's L1c: every `ℓ ∈ dom(L)` is reachable from a T4-valid document-level seed..."

**Problem**: ASN-0093 (foundation) already states L1c in exactly the structural-inc-chain form this ASN uses. The local L1c in ASN-0047 is verbatim ASN-0093's L1c, not a strengthening or weakening. Attributing the weakening to "ASN-0043's L1c" misrepresents the dependency chain — the relaxation happened at ASN-0093, not here.

**Required**: Move L1c into the "Inherited from foundation" table with attribution to ASN-0093, or rewrite the "Local weakening" description to acknowledge ASN-0093 as the originating weakening.

### Issue 3: K.δ case (ii) k = 0 frontier discharge — dense argument needs lemma extraction

**ASN-0047, Elementary transitions, K.δ "Rationale (k = 0 conjuncts)"**: The argument that `inc(t, 0) ∉ E` operationally identifies t as the frontier of its sub-allocator chain runs across one ~30-line dense paragraph chaining three premises (T10a per-`(t,0)` uniqueness, P1 monotonicity, T10a GlobalUniqueness).

**Problem**: This is a load-bearing closure — it converts an operational precondition into an allocator-theoretic identification — but is buried as discharge prose under K.δ. The argument is correct but readers must reconstruct (i) why T4b's `parent`/zeros stratification cannot identify the frontier (the document-allocator vs version-allocator length-equality case), (ii) why direct freshness sidesteps allocator-structural identification, (iii) why the precondition pair is operationally equivalent to "t is on the frontier". The proof of S4 (and the matrix entries naming "T10a GlobalUniqueness on parent allocator") leans on this equivalence without re-deriving it.

**Required**: Extract the frontier-equivalence as a named lemma (e.g., FrontierEquivalence) with explicit statement `inc(t, 0) ∉ E ⟺ t is the frontier of its sub-allocator's (t, 0)-branch`, the three load-bearing premises, and the counterexample to T4b-based identification. The K.δ discharge can then cite the lemma rather than re-derive in place.

### Issue 4: K.δ case (ii) k = 2 sub-case A induction structure implicit

**ASN-0047, K.δ case (ii) discharge and parent-allocator activation, sub-case A**: "Here the spawned allocator is `A_doc(t)`, and its parent allocator in T10a's tree is `A_account(parent(t))` — the account sub-allocator under t's node — which was itself activated by an earlier K.δ event of this same k = 2 form; `t ∈ dom(A_account(parent(t)))` follows from that earlier event by induction."

**Problem**: The induction is on prior K.δ events activating account sub-allocators, but the base case is not named. The base case is a K.δ case (ii) k = 2 with operand t = node (sub-case B), where A_account(t) is activated and the spawnPt discharge goes through NodeUniqueAllocation clause (c) rather than through a state-tracked allocator. Without explicit identification of the base case, the induction reads as circular ("sub-case A relies on a prior K.δ k=2 event") rather than as well-founded recursion bottoming out in sub-case B.

**Required**: State the induction explicitly: "Base: first K.δ case (ii) k=2 event with t = node (dispatched to sub-case B, discharged by NodeUniqueAllocation). Inductive step: K.δ case (ii) k=2 with t = account, t placed in dom(A_account(parent(t))) by a prior K.δ event (either sub-case A inductively, or sub-case B at the lineage's base)."

### Issue 5: K.μ~ existence-condition narrative — mixed case (dom_C empty, dom_L non-empty)

**ASN-0047, Decomposition of K.μ~**: "*The empty case* `dom_C(M(d)) = ∅` *is doubly excluded:* (a) the only bijection on `∅` is the empty function `∅ → ∅`, which IS the identity..., violating (iii); (b) when `dom_C(M(d)) = ∅ ∧ dom_L(M(d)) = ∅` — i.e., `dom(M(d)) = ∅` — the K.μ⁻ + K.μ⁺ decomposition is itself blocked..."

**Problem**: The "doubly excluded" framing covers the all-empty case where both (a) and (b) apply. The mixed case (`dom_C(M(d)) = ∅` but `dom_L(M(d)) ≠ ∅`) is excluded by (a) alone — and is the more interesting case, since a reader might intuit "K.μ~ should reorder the link subspace when content is empty". The mixed case is left implicit; readers must derive that link-subspace fixity forces π = id on dom_L, leaving the empty dom_C unable to supply a non-identity permutation.

**Required**: Add an explicit paragraph: "*Mixed case* (`dom_C(M(d)) = ∅` with `dom_L(M(d)) ≠ ∅`): excluded by (a) alone — π must be a bijection on `dom(M(d)) = dom_L(M(d))`; link-subspace fixity forces `π|_{dom_L} = id`; hence π = id, violating (iii). K.μ~ cannot reorder link-subspace V-positions even when content is empty."

### Issue 6: Composite-boundary verification matrix lacks J0/J1★/J1'★ inputs

**ASN-0047, Extended reachable-state invariants, Class (b) Composite-boundary verification matrix**: The matrix has three rows (P4★, P4a, P7a) with discharge mechanisms and transient-failure characterisations.

**Problem**: P7a's discharge entry reads "J0 + J1★ at boundary: J0 places `a ∈ ran(M'(d))` at content-subspace position; J1★ supplies `(a, d) ∈ R'`". But the proof body separately requires a chained derivation through S3★ + L14 to establish that J0's witness V-position has `subspace(v) = s_C` — without this chain, J0 alone does not place `a` "at content-subspace position". The matrix glosses over this chain, making P7a's discharge appear simpler than it is.

**Required**: Expand the P7a row to: "J0 supplies v ∈ dom(M'(d)) with M'(d)(v) = a; S3★ + L14 + S3★-aux force subspace(v) = s_C; J1★ then supplies (a, d) ∈ R'." This matches the proof body's actual structure.

VERDICT: REVISE
