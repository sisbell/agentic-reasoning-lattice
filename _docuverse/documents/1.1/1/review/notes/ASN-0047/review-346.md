# Review of ASN-0047

## REVISE

### Issue 1: Contradictory membership of S8-fin in "the arrangement-shape invariant package"
**ASN-0047, *Decomposition of K.μ~* (admissibility clause (i)) vs. *Extended reachable-state invariants* (Class (a), "K.μ~ discharge for the arrangement-shape invariants")**:

Clause (i) of K.μ~ admissibility states: "the induced post-state `M'(d)` would satisfy the arrangement-*shape* invariant package on `M'(d)` — **S8a, S8-depth, S8-fin, D-CTG★, D-MIN★**, from which the derived D-SEQ★ follows."

The Class (a) discharge then states: "The shape stipulations (S8a, S8-depth, D-CTG★, D-MIN★) are stipulated on `M'(d)` by K.μ~ admissibility (i)... Two members carry a rider beyond that decomposition. **S8-fin(Σ') — bundled in the matrix with S8a/S8-depth but not part of the shape package** — is discharged independently of admissibility (i)..."

**Problem**: The same term ("arrangement-shape invariant package" / "shape package") is given two contradictory memberships for S8-fin: clause (i) includes it; the discharge explicitly excludes it ("not part of the shape package"). This is not a navigational nicety — it is load-bearing, because the discharge's argument depends on S8-fin *not* being stipulated by clause (i) (finiteness is an operational consequence of K.μ⁻ restricting a finite domain and K.μ⁺ adding finitely many positions, not a property of the admissible *V-position domain shape*). The D-SEQ★ derivation, in turn, consumes S8-fin, so a reader following clause (i) literally would treat S8-fin as a stipulated shape constraint and the discharge as redundant.

**Required**: Remove S8-fin from clause (i)'s package list (leaving S8a, S8-depth, D-CTG★, D-MIN★, with D-SEQ★ derived), so the single source of S8-fin(Σ') is the independent operational discharge already given. The two passages will then agree.

### Issue 2: Meta-framing in the P4a definition slot
**ASN-0047, *Coupling and isolation* (P4a definition box)**: "P4a is a composite-boundary property (temporal scope per the *Extended reachable-state invariants* preamble). What is specific to P4a — and made formal here — is that its witness need not inhabit the *current* arrangement: we give its witnessing domain below."

**Problem**: These two opening sentences announce what is special about the claim and defer its delivery ("we give its witnessing domain below") within the same short box, rather than advancing the definition. A precise reader skips them to reach the actual `valid transition trace` definition a few lines down. This is the "defensive/meta-commentary in a structural slot" pattern the anti-bloat classifier targets — the witnessing-domain content arrives immediately after, so the announcement carries no information.

**Required**: Drop the meta-framing and lead with the trace definition and the formal P4a statement; the witnessing-domain point is made by the existential `(E Σ_k ∈ {Σ₀, ..., Σ_n} : ...)` itself.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link contraction
The ASN models link-subspace contraction by suffix removal only (K.μ⁻), and explicitly defers interior withdrawal with compaction/renumbering to a future ASN (its own open question). Correctly scoped out — DELETEVSPAN mechanics are named-operation territory.

### Topic 2: Concurrency / serialization of allocation
Whether concurrent allocations under one home document need serialization is raised as an open question and left to a future ASN; operation atomicity/concurrency is out of scope.

VERDICT: REVISE
