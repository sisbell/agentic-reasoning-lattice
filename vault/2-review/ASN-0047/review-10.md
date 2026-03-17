# Review of ASN-0047

## REVISE

### Issue 1: No formal definition of valid composite transition
**ASN-0047, Coupling and isolation**: "A *composite transition* is an ordered sequence of elementary transitions whose intermediate states need not satisfy all system invariants; the invariants are required to hold at the final state."
**Problem**: The ASN introduces three distinct categories of constraint — elementary preconditions (checked at intermediate states), coupling constraints (J0, J1, J1'), and state invariants (P0–P8, S2, S3, S8a, S8-depth, S8-fin, Contains(Σ) ⊆ R) — but never collects them into a single formal definition of "valid composite transition." J0 is an "axiom," J1 is "derived by wp," J1' is a "design constraint," and the invariants are spread across ASN-0036 and this ASN. The reader must reconstruct the validity conditions from scattered paragraphs.
**Required**: A definition block that states: a composite transition Σ → Σ' is valid iff (1) it is a finite sequence of elementary transitions where each step's preconditions hold at its intermediate state, (2) coupling constraints J0, J1, J1' are satisfied for the composite, and (3) the final state Σ' satisfies all state invariants. This definition is load-bearing — future ASNs that introduce named operations will compose elementary transitions and need a precise notion of what compositions are legal.

### Issue 2: J4 formal statement is a special case of J1, structural claim not formalized
**ASN-0047, J4**: The formal statement quantifies over freshly created documents whose arrangements draw from a source, and concludes provenance is recorded for each I-address.
**Problem**: Apply the convention M(d) = ∅ for d ∈ E'\_doc \ E\_doc to J1: for d\_new freshly created, ran(M'(d\_new)) \ ran(M(d\_new)) = ran(M'(d\_new)) \ ∅ = ran(M'(d\_new)). J1 directly gives (a, d\_new) ∈ R' for every a in this set. J4's formal conclusion is exactly J1 applied to the fresh-document case — it adds no new constraint. Meanwhile, the actual structural claim — fork decomposes into K.δ + K.μ⁺ + K.ρ with C' = C (no new content enters the content store) — appears only in prose and is never formalized.
**Required**: Either (a) strengthen J4's formal statement to include the structural claim (e.g., formalize that dom(C') = dom(C) for the fork portion), or (b) explicitly acknowledge that the provenance conclusion is derived from J1 and reframe J4 as a structural description of a common composite pattern.

### Issue 3: Fork of empty source document — missing boundary case
**ASN-0047, K.δ**: "Forking is compound: K.δ followed by arrangement extension and provenance recording (J4 below)."
**Problem**: K.μ⁺ requires dom(M'(d)) ⊃ dom(M(d)) — strict domain extension. When the source document's arrangement is empty (ran(M(d\_src)) = ∅), there are no I-addresses to copy, and K.μ⁺ cannot produce a strict superset of ∅ without inventing mappings that aren't from the source. The fork reduces to K.δ alone: ex nihilo creation and fork-of-empty are structurally identical. The prose states fork = K.δ + K.μ⁺ + K.ρ as a universal characterization without noting this degenerate case. J4's formal statement handles it vacuously (ran(M'(d\_new)) = ∅ makes the conclusion vacuously true), but the prose is inaccurate.
**Required**: Qualify the description: "When the source arrangement is non-empty, forking is compound: K.δ followed by K.μ⁺ and K.ρ. When the source arrangement is empty, fork reduces to K.δ alone — structurally identical to ex nihilo creation."

### Issue 4: K.μ~ is decomposable; "no fourth mode" overstates independence
**ASN-0047, Elementary transitions**: "Any modification to a finite partial function decomposes into entry additions (K.μ⁺), entry removals (K.μ⁻), and value-preserving re-indexing (K.μ~); there is no fourth mode."
**Problem**: K.μ~ itself decomposes into K.μ⁻ (remove all mappings) followed by K.μ⁺ (add all at new positions). The coupling analysis goes through: after K.μ⁻, ran(M\_inter(d)) = ∅. K.μ⁺ then reintroduces the same I-addresses. J1 requires (a, d) ∈ R' for each a ∈ ran(M'(d)) \ ran(M\_inter(d)) = ran(M(d)). These pairs are already in R from prior containment; P2 preserves them. No new K.ρ is needed. So K.μ~ is not an independent primitive — two modes (addition, removal) suffice for all partial-function mutations. The "no fourth mode" claim implies three independent modes when there are two.
**Required**: Acknowledge the decomposability: "K.μ~ decomposes into K.μ⁻ followed by K.μ⁺, with coupling satisfied by existing provenance entries (P2). We retain it as a distinct elementary transition because its isolation property (J3) and semantic clarity — reordering as a single atomic concept — justify separate treatment." Adjust the completeness argument from "three modes, no fourth" to "two independent modes (addition, removal); K.μ~ is a named special case."

## OUT_OF_SCOPE

### Topic 1: Subspace-respecting reordering
**Why out of scope**: The ASN explicitly lists this as an open question: "Must arrangement reordering respect subspace boundaries within a document?" K.μ~'s precondition requires S8a and S8-depth in the result but does not prevent cross-subspace V-position reassignment. This is a design decision for a future ASN on arrangement structure, not an error in the transition taxonomy.

### Topic 2: Node allocation mechanism
**Why out of scope**: K.δ for root nodes (IsNode(e)) requires no parent. The allocation mechanism for fresh node addresses is unspecified — unlike non-root entities which use inc(·, k) within a parent's ownership domain. This belongs to system bootstrap and administration, not to the abstract state transition model.

VERDICT: REVISE
