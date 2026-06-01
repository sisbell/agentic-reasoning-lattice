# Review of ASN-0047

## REVISE

### Issue 1: P4a's formal statement does not assert what its name and prose claim

**ASN-0047, P4a (Recorded-boundary witnessing — trace property)**: The prose fixes `Σ_k` as a specific state — "its *recording boundary* `Σ_k` (the least `k` with `(a, d) ∈ R_k`)" and "P4a asserts that at that recording boundary the entry had a *content-subspace* containment witness" — but the formal statement existentially rebinds the same symbol over the entire trace:

> `(A (a, d) ∈ R :: (E Σ_k ∈ {Σ₀, ..., Σ_n} : (E v ∈ dom(M_k(d)) : subspace(v) = s_C ∧ M_k(d)(v) = a)))`

**Problem**: The formula proves only "*some* trace state witnesses `a`," which is strictly weaker than "the *recording boundary* witnesses `a`." The matrix discharge confirms the weaker reading — it supplies `Σ'` (= `Σ_n`) as the witness for entries in `R' \ R`, not the least-index recording state. So the property named "Recorded-boundary witnessing" is never actually established at the recording boundary. The symbol `Σ_k` is overloaded: a fixed least-index state in prose, an unbound existential in the formula.

**Required**: Either (a) fix the formula to bind `Σ_k` as the least index (`Σ_k = ` the recording boundary) and prove the witness exists *there*, or (b) rename the property and rewrite the prose to claim only "some trace state witnesses," matching what J1'★ at `Σ'` actually delivers. As written, the proof obligation and the stated property diverge.

### Issue 2: NodeBaptism axiom box carries protocol rationale and a downstream-consumer inventory instead of axiom content

**ASN-0047, NodeBaptism (Axiom, boundary input)**: The box's load-bearing content is just (a) freshness `e ∉ Σ.E` and (b) lineage `n₀ ≼ e`. Surrounding this:

> "A node is a *ghost element* (Nelson, LM 4/23) ... the operation set provides no `inc`-rule producing a node. Bringing a node into existence is a network-provisioning act (Nelson's BEBE inter-server protocol, LM 4/70) performed at the boundary of the docuverse transition model rather than within it."

and a use-site inventory:

> "As a base for downstream allocation, a baptised node `t ∈ Σ.E_node` serves directly as the base of its account sub-allocator `A_account(t)`: the boundary fact `t ∈ Σ.E_node` is exactly the commitment discharging the spawnPt premise for the `k' = 2` step ..."

**Problem**: This is the flagged anti-bloat pattern — prose around an axiom explaining *why the axiom is needed* and *where it is consumed* rather than *what it says*. The ghost-element/BEBE framing is rationale; the spawnPt-discharge sentence is a downstream-consumer enumeration that belongs (and is already restated) in the K.δ k=2 dispatch table.

**Required**: Reduce the box to the axiom's commitments (a)/(b) plus the bootstrap fact `n₀ ∈ E₀`. Move the spawnPt-discharge role to the single site that uses it (K.δ k=2 dispatch), where it already appears.

### Issue 3: Duplicated summary of the K.δ spawnPt dispatch

**ASN-0047, K.δ case (ii) discharge**: The three-row spawnPt-premise table (account / non-bootstrap node / bootstrap node) is immediately followed by:

> "Across K.δ case (ii), the source of the spawnPt premise denotes the minting source at the moment of the K.δ event — a parent allocator that is either pre-activated (k = 0; k = 1 after first version) or activated by the K.δ event itself (k = 2 off an account; first k = 1 emission), or, when the operand is a node, the NodeBaptism boundary commitment in place of a parent allocator, as named explicitly in the k = 2 dispatch above."

**Problem**: This paragraph restates the table it follows ("two paragraphs say the same thing in different words"), closing with "as named explicitly ... above" — a deferral back to the content it duplicates.

**Required**: Delete the summary paragraph; the table is self-contained.

### Issue 4: Defensive "no check needed" prose in K.μ~ admissibility

**ASN-0047, Decomposition of K.μ~ (admissibility clause discussion)**: 

> "S8a at every `π(v)` is part of clause (i)'s post-state invariant package on M'(d); K.μ~-FIX gives `dom(M'(d)) = dom(M(d))`, so every `π(v) ∈ dom(M(d))` inherits S8a from the inductive hypothesis at Σ unconditionally — no separate per-`π(v)` check is needed."

**Problem**: This is a defensive justification asserting that an obligation *need not* be discharged — meta-prose that does not advance the argument. The matrix and the per-invariant prose already establish S8a preservation; the inline reassurance is the kind of accretion the anti-bloat classifier flags.

**Required**: Remove the sentence; if S8a-at-`π(v)` warrants mention, the verification-matrix S8a/K.μ~ cell is the single correct site.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal / tombstoning mechanism

**Why out of scope**: The tension between Nelson's tombstoning design (LM 4/9) and the suffix-only contraction forced by D-CTG★/D-MIN★ (interior link withdrawal requires withdrawing all later-allocated links) is correctly identified and deferred to an Open Question. A status-flag/tombstone mechanism is new state outside K.μ⁻'s presentational-removal contract and belongs in a future ASN, not this one.

VERDICT: REVISE
