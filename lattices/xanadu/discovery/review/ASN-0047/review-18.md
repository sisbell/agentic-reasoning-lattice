# Review of ASN-0047

## REVISE

### Issue 1: Reachable-state invariants theorem lacks pre-state conditioning

**ASN-0047, Valid composite / Reachable-state invariants**: "Every valid composite transition produces a final state Σ' satisfying P6, P7, P8, S2, S3, S8a, S8-depth, S8-fin, and Contains(Σ') ⊆ R'."

**Problem**: The theorem statement is unconditional, but every one of its derivations uses an inductive hypothesis — the pre-state must already satisfy the invariants. The P4 proof explicitly says "assuming it holds before the transition." P6 uses P0 and P1 on existing entries (requiring P6 at the pre-state). P7 uses P0 and P2 similarly. The statement as written is false for arbitrary starting states: begin from a state where Contains(Σ) ⊄ R, apply a no-op valid composite (empty sequence), and the post-state still violates Contains(Σ') ⊆ R'.

**Required**: Either (a) state the theorem as an invariance result over reachable states — "Starting from Σ₀, all reachable states satisfy..." with explicit base-case verification and inductive-step structure, or (b) add the pre-state assumption: "For any state Σ satisfying P4, P6, P7, P8, S2–S8-fin, every valid composite Σ → Σ' produces Σ' satisfying the same." The title says "Reachable-state" but the formal statement does not restrict to reachable states.

### Issue 2: Valid composite condition (3a) is redundant and confusingly labeled

**ASN-0047, Valid composite definition**: "(3a) Transition constraints: the composite Σ → Σ' satisfies P0, P1, P2."

**Problem**: P0, P1, and P2 are derivable from condition (1) alone. Each elementary transition's frame ensures: K.α extends C preserving existing entries (all others hold C' = C); K.δ extends E (all others hold E' = E); K.ρ extends R (all others hold R' = R). By transitivity over any finite sequence, P0, P1, P2 hold for every composite satisfying (1). No composite can satisfy (1) and violate (3a). Additionally, the label "(3a)" implies a sibling "(3b)" that does not exist, suggesting an incomplete definition.

**Required**: Either (a) remove (3a) and add a lemma deriving P0/P1/P2 from the elementary transition definitions, or (b) relabel as (3) and note explicitly that it is a consequence of (1), stated for reference. Either way, address the orphaned "a" suffix.

### Issue 3: Contains(Σ) absent from Properties Introduced table

**ASN-0047, Properties Introduced table**

**Problem**: Contains(Σ) = {(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))} is a named definition with its own bold label, used in the valid composite definition, the reachable-state invariants theorem, P4, J1's wp derivation, J2's isolation argument, and the worked example. It is not listed in the Properties Introduced table, which does list comparable definitions (parent(e), Σ₀, Valid composite).

**Required**: Add Contains(Σ) to the table with its definition and role.

## OUT_OF_SCOPE

### Topic 1: Node address allocation without ownership domain
**Why out of scope**: K.δ for root nodes (IsNode(e)) has no parent and therefore no ownership domain for inc(·, k). How fresh node addresses are generated while maintaining GlobalUniqueness is an allocation/authority question outside this ASN's transition taxonomy.

### Topic 2: Cross-subspace reordering constraints
**Why out of scope**: K.μ~'s bijection π can map V-positions across subspace boundaries (e.g., text subspace → link subspace). The ASN correctly flags this as an open question. Subspace semantics belong to a future ASN on document structure.

VERDICT: REVISE
