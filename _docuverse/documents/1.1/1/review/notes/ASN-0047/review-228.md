# Review of ASN-0047

## REVISE

### Issue 1: S3★ listed as both an admissibility hypothesis and a derived consequence for K.μ~

**ASN-0047, *Decomposition of K.μ~*, admissibility clause (i) vs. Step (B)**: Clause (i) states π is admissible iff "the induced post-state M'(d) would satisfy the arrangement-shape invariant package on M'(d) — S8a, S8-depth, S8-fin, D-CTG★, D-MIN★, S3★, and S3★-aux". Step (B) then claims the decomposition "establishes `S3★(Σ')` at the post-state `Σ' = (C, L, E, M', R)` from the two Class (a) cells", and the verification matrix discharges the S3★/K.μ~ cell via "elementary decomposition K.μ⁻+K.μ⁺".

**Problem**: S3★ occupies two incompatible logical roles. If clause (i) *filters* on S3★(Σ'), then every realisable π satisfies it by definition and Step (B) is circular/redundant. If Step (B) genuinely *derives* S3★(Σ') from the decomposition structure, then S3★ does not belong in the clause-(i) hypothesis set. The ASN itself draws this exact distinction elsewhere — "the remaining per-state arrangement invariants on M'(d) — CL-OWN, CL-UNIQ, S2, and S8★ — are *not* admissibility hypotheses but derived consequences" — but inconsistently leaves S3★ in the hypothesis group while proving it as a consequence.

**Required**: Decide S3★'s status. Given Step (B) proves S3★(Σ') from the K.μ⁻ restriction + K.μ⁺ amendment cells, move S3★ into the derived group alongside CL-OWN/CL-UNIQ/S2/S8★ and remove it from clause (i). Keep only the genuinely-filtered shape invariants (S8a, S8-depth, S8-fin, D-CTG★, D-MIN★, S3★-aux) in (i).

### Issue 2: Body asserts empty-endset consumer semantics that the matching Open Question marks as undecided, and references an undefined term

**ASN-0047, *Link store and extended system state*, "Semantics of empty endsets at slots 1 and 2"**: "both empty is admissible as a type-only marker. Endset-iterating consumers (L8's `same_type`, discovery-set unions) treat an empty endset as contributing ∅ by the natural inductive form."

**Problem**: (a) The Open Question "Should K.λ require `e₁ ∪ e₂ ≠ ∅` ... do one-sided links ... carry distinguishable semantics in endset-iterating consumers like L8's same_type and the discovery-set unions?" presents this very semantics as unresolved. The body asserts as settled ("treat an empty endset as contributing ∅") precisely what the Open Question defers. (b) "discovery-set unions" is undefined anywhere in this ASN — there is no discovery operation or discovery-set in the state model — so the asserted consumer behavior has no referent here.

**Required**: Either remove the consumer-semantics sentence (the OQ already owns the question), or downgrade it to "L3 admits both-empty type-only markers; the semantics of empty endsets for endset-iterating consumers is left to a future ASN." Drop the undefined "discovery-set unions" reference.

### Issue 3: Dead derivation of a fact already fixed by axiom

**ASN-0047, *Link store and extended system state***: "We note that `s_C ≥ 1` follows from S7b and T4: content I-addresses are element-level by S7b (`zeros(a) = 3`), and T4 requires every element-field component to be strictly positive, so `subspace_I(a) = s_C > 0`. The same derivation gives `s_L ≥ 1`..."

**Problem**: SubspaceConventionAxiom, stated two paragraphs earlier, fixes `s_C = 1 ∧ s_L = 2`. Given that axiom, `s_C ≥ 1` and `s_L ≥ 1` are trivially true and need no derivation. This paragraph re-derives via S7b + T4 a fact the adopted axiom already pins, advancing no reasoning — the kind of accreted prose the precise reader must skip past.

**Required**: Delete the paragraph. If the intent is to record that positivity holds independently of the chosen identifier values, say so in one clause and cite it where positivity is actually consumed, rather than as a standalone derivation of `≥ 1`.

### Issue 4: K.δ k=0 fork sub-case carries an unstated precondition

**ASN-0047, *Coupling and isolation*, J4 / Definition (Fork), clause (i)**: "either k = 1 with t = d_src ... or k = 0 with t = prev_version the current frontier of `A_v(d_src)`, producing the next version d_new = inc(prev_version, 0)". The fork *precondition* is stated only as "d_src ∈ E_doc ∧ V_{s_C}(d_src) ≠ ∅".

**Problem**: The k = 0 sub-case requires `A_v(d_src)` to already be active (a first version must already exist, supplying "the current frontier"). This requirement is implicit in the phrase "current frontier of A_v(d_src)" but is absent from the explicitly stated fork precondition. A reader checking fork applicability against the precondition alone cannot tell that k = 0 forks demand a pre-existing version chain, while k = 1 forks demand its absence.

**Required**: State the per-sub-case activation condition in the fork precondition — k = 1 fires when `A_v(d_src)` has no prior emission; k = 0 fires when `A_v(d_src)` already has a frontier — or cite FrontierEquivalence as the discharge for the k = 0 frontier existence.

## OUT_OF_SCOPE

None. The Open Questions appropriately defer link-inheritance-under-fork, transitive-transclusion provenance, concurrency, and link-withdrawal mechanisms to future ASNs.

VERDICT: REVISE
