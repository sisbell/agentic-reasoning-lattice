# Review of ASN-0126

The mathematics here is sound. I checked the proofs of P1–P6, the projection-bridge transfer (B1/B2), the wp derivation, and the worked illustration's address arithmetic, and they hold:

- **Worked illustration verified.** With `d = 1.1.0.1.0.1`, the chain `ℓ₁=…2.1, ℓ₂=…2.2`, `a_R = inc(ℓ₂,0) = …2.3`, `a = inc(a_R,0) = …2.4 = g`, and `coverage(G_rng) = […2.4, …2.7)` are all correct; `a_R ∉ coverage(G_rng)` (so the retractor lands active) and `g ∈ coverage(G_rng)` (so the citation is born nullified) both check out. This is exactly the C3-failure witness the wp section promises, and it is the kind of concrete verification the standard demands.
- **The relaxation is handled honestly.** The framework drops ASN-0086's unit-depth discipline (Binary counts spans, not unit-depth), so it correctly uses the *full* wp Case 2 with C3 live rather than the disciplined simplification, and never transfers a layer-reachable-only result through B2.

So my findings are presentational — which is what this note's `anti-bloat` classifier asks for.

## REVISE

### Issue 1: Forward-reference, ordering, and use-site meta-prose
Several sentences justify *where* a claim sits or *that it will be used later* rather than advancing the claim. A reader following the argument must skip them:

- **C0 (The registry)**: "Constraining only the initial registry suffices, because the registry never drifts — Registry permanence (P1) below freezes it at every later state." — forward-references P1 to justify C0's scope.
- **The registry**: "the gate below reads that shape; so we fix the registry's structure now, before any step gates on it." — document-ordering justification.
- **The shape-gated emit**: "we give that re-expression once the projection bridge is in hand (Retraction as an attributed Binary)." — ordering justification on a deferral.
- **The projection bridge**: "The bridge has two consequences, cited throughout the sequel." — announces downstream use; B1 and B2 stand on their own.
- **Registry permanence** (before P4): "These two facts — verdict-stability and definedness-coincidence — are exactly what this note's fourth property records." — self-referential bridge to the next named property.

**Problem**: These are exactly the document-ordering and downstream-consumer patterns the classifier flags. None changes what is being claimed.
**Required**: State each claim directly; delete the clauses that only justify ordering or announce later citation (e.g., "The bridge has two consequences." then B1, B2).

### Issue 2: P2 (ShapeStability) re-records an already-derived fact and is cited by nothing
**ASN-0126, Registry permanence, P2**: "The claim has two conjuncts… *Coverage-class well-definedness* (← C0). That `shape(·)` is a function of `[K]`… was derived above (The registry)… This conjunct rests on that derivation — on C0, not P1."

**Problem**: P2's second conjunct is the result already derived in *The registry*; P2 itself acknowledges it adds no derivation. Meanwhile the property the sequel actually consumes is P4 — and P4's proof reaches back to P1 directly ("shape(K) is registry-determined and the registry is invariant"), not to P2. P6 likewise cites P1, L12, P4, never P2. So P2 bundles one new fact (state-stability, the P1 instance for `shape`) with one re-recorded fact (well-definedness, from C0), under a name ("ShapeStability") that describes only the first, and is itself load-bearing for nothing downstream.
**Required**: Either trim P2 to its state-stability content (and let the well-definedness stay where it was derived), or — if P2 is intended as a standalone consumer-facing guarantee — name a downstream consumer and present both halves as bare citations (← P1, ← C0) so it reads as consolidation, not re-derivation.

## OUT_OF_SCOPE

### Topic 1: How types enter the immutable registry
P1 freezes the registry at `Σ_init`, so every type an app will ever emit must already key `Σ_init.registry`; a substrate with `Σ_init.registry = ∅` can never extend `dom(Σ.L)` (every `K.λ_sh` needs precondition (i)). The mechanism by which app declarations populate `Σ_init.registry`, and whether any dynamic/staged registration is possible, is genuinely new territory — open question 4 already sits adjacent to it.
**Why out of scope**: Initialization and declaration semantics are a successor concern; the immutability of the registry within the state space is the deliberate subject of *this* note, and it is proven correctly.

VERDICT: REVISE
