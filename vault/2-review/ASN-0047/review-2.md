# Review of ASN-0047

## REVISE

### Issue 1: K.μ⁺ frame omits C' = C, contradicting P5 proof
**ASN-0047, Elementary transitions / Destruction confinement**: K.μ⁺'s frame is stated as "E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R." C' = C is absent. P5's proof then claims: "K.μ⁺, K.μ⁻, K.μ~ have C, E, and R in their frames."
**Problem**: K.μ⁻ and K.μ~ both list C' = C in their frames. K.μ⁺ does not. K.μ⁺ does not modify C (it modifies only M(d)), so the omission appears to be an oversight rather than a deliberate allowance for co-occurring K.α — individual frame conditions describe individual transitions, and K.α's own effect on C is already captured in K.α's definition. The P5 proof as written appeals to a frame condition that does not appear in K.μ⁺'s specification.
**Required**: Add C' = C to K.μ⁺'s frame, making it consistent with K.μ⁻ and K.μ~ and making the P5 proof correct as written.

### Issue 2: P4 proof conflates elementary and composite transition analysis
**ASN-0047, Coupling and isolation**: "Inductive step. We verify that each elementary transition preserves Contains(Σ) ⊆ R... K.μ⁺: May add new pairs to Contains. J1 requires co-occurring K.ρ to add those pairs to R'. Preserved by J1."
**Problem**: The proof structure is case analysis on individual elementary transitions, checking that each one preserves Contains(Σ) ⊆ R. For five of the six transitions this works: the transition either doesn't change Contains or doesn't change R, so preservation is immediate from the individual frame. But K.μ⁺ alone does not preserve the invariant — it adds pairs to Contains while its frame holds R' = R. The proof handles this by invoking J1, but J1 is a coupling constraint on composite transitions ("must co-occur"), not a property of K.μ⁺ individually. The proof is silently switching from "each elementary transition preserves P4" to "each valid composite transition preserves P4" without acknowledging the shift or showing the composition. Concretely: K.μ⁺ adds {(a, d) : a ∈ ran(M'(d)) \ ran(M(d))} to Contains; co-occurring K.ρ adds those same pairs to R; therefore Contains(Σ') = Contains(Σ) ∪ Δ ⊆ R ∪ Δ = R'. This three-step argument is what the proof needs and does not state.
**Required**: Either restructure P4 as a proof over composite transitions (the natural unit at which J1 applies), or explicitly show the K.μ⁺ + K.ρ composition: state the intermediate effect of each, then verify the invariant on the composed result.

### Issue 3: R's definition claims historical fidelity that K.ρ's precondition does not enforce
**ASN-0047, The state model / Provenance recording**: "The pair (a, d) ∈ R records that document d has, at some point in the system's history, contained I-address a in its arrangement." K.ρ's precondition: "a ∈ dom(C) ∧ d ∈ E_doc."
**Problem**: J1 establishes a forward coupling — K.μ⁺ must trigger K.ρ — ensuring that every actual containment event is recorded. But no reverse coupling constrains K.ρ to occur only when K.μ⁺ provides the corresponding (a, d) pair. K.ρ's precondition (a ∈ dom(C) ∧ d ∈ E_doc) admits pairs where d has never contained a in any historical arrangement. The definition says R records historical containment; the model permits R to over-approximate it. The stale-entry discussion in P4 correctly observes that (a, d) ∈ R does not imply current containment, but the gap is sharper: (a, d) ∈ R need not imply *any* past containment. Gregory's evidence points the right way — "accumulates entries from every content addition" — suggesting the implementation constrains K.ρ more tightly than the model does.
**Required**: One of: (a) add a reverse coupling (K.ρ for (a, d) occurs only when K.μ⁺ in the same composite introduces a into ran(M'(d))), which with J1 gives a bidirectional coupling K.μ⁺ ↔ K.ρ; (b) add a faithfulness invariant `(A (a, d) ∈ R :: there exists a prior state Σₜ with a ∈ ran(Σₜ.M(d)))`; or (c) weaken R's definition to state that R is an upper bound on containment history ("(a, d) ∈ R implies d was eligible to contain a") and note the over-approximation explicitly.

## OUT_OF_SCOPE

### Topic 1: Subspace constraints on arrangement reordering
**Why out of scope**: K.μ~ permits arbitrary bijections on V-positions, including those that cross subspace boundaries (text vs. link). Whether valid reorderings must respect subspace structure is a V-space mechanics question, acknowledged in the ASN's open questions, and belongs in a future ASN on V-space invariants.

### Topic 2: Version lineage as state
**Why out of scope**: The ASN models fork (J4) as compound entity creation but does not include a version DAG in the state. The relationship between version lineage and arrangement transitions is a genuine future concern but not an error in the transition taxonomy.

### Topic 3: Structural invariants of V-positions across transitions
**Why out of scope**: ASN-0036's S8a (V-position well-formedness) and S8-depth (fixed depth per subspace) are not verified against K.μ⁺ or K.μ~. Since the ASN's scope is permanence and coupling — not the structural invariants of arrangements — and since these invariants would be verified when operations are specified, this is future work.

VERDICT: REVISE
