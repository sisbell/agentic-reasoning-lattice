# Review of ASN-0126

I checked the mathematics first. The core results are sound: the gate guarantee (P3/P6), registry invariance (P1→P2→P4), the projection bridge (ProjectionBridge/B1/B2), gate realizability (P5), and the retraction R-Scope transfer all hold under scrutiny. I verified the address arithmetic in the worked illustration end-to-end (`ℓ₁=…2.1`, `ℓ₂=…2.2`, `a_R=inc(ℓ₂,0)=…2.3`, `g=inc(a_R,0)=…2.4` landing on the lower endpoint of `coverage(G_rng)=[…2.4,…2.7)`, hence born-nullified) and the ghost-root over-nullification example (`a=1.1.0.1.0.1.0.2`, `zeros=3`, `#E=1`, so `a∉dom(Σ.L)` and `a≠a_emit`, P-tgt failing on both disjuncts). RegisteredAdmissible's `coverage(K)=coverage(K_j)≠∅ ⟹ K≠∅` transfer is correct. No correctness defects, no proof-by-checkmark, no missing-case hand-waves, and references stay inside the two foundations.

What remains is residual meta-prose — the pattern this note's classifier exists to catch.

## REVISE

### Issue 1: Justificatory clause embedded in the well-formedness definition

**ASN-0126, The registry**: "A registry is well-formed when shape values lie in `{Unary, Binary, Multi}` and — the condition the shape function's well-definedness actually rests on — *coverage-class keys are unique*: no two entries have `~`-equal keys."

**Problem**: The em-dash clause "the condition the shape function's well-definedness actually rests on" explains *why* the uniqueness clause is included rather than stating the condition. The well-definedness it previews is then asserted outright in the very next sentence ("so `shape(K)` depends only on `[K]`, defined exactly on the registered coverage classes"). The reader must parse a forward-justification mid-definition to reach the two actual conditions, and that justification is redundant with the sentence immediately following.

**Required**: State the two well-formedness conditions plainly ("shape values lie in `{Unary, Binary, Multi}` and coverage-class keys are unique: no two entries have `~`-equal keys"). The `shape(K)` sentence already carries the well-definedness consequence.

### Issue 2: Significance/dependency clauses that don't advance the local argument

**ASN-0126, Reachable conformance**: "This is the state-level closure of P3's single-step half — the guarantee a consuming app relies on."

**ASN-0126, Weakest precondition of the shape-gated emit**: "…governs only well-formedness — it *enables* the emit, is what P3 rests on, and deposits the conforming tuple into the *audit* slice `L_K^{Σ'}` — whereas…"

**Problem**: "— the guarantee a consuming app relies on" and "is what P3 rests on" describe a claim's downstream importance / inter-claim dependency; neither advances the surrounding statement. Deleting them leaves complete sentences ("This is the state-level closure of P3's single-step half." / "…it enables the emit and deposits the conforming tuple into the audit slice `L_K^{Σ'}`…", the latter two being substantive descriptions of what the gate does). These are the kind of motivational asides that compound across cycles.

**Required**: Drop the two clauses; keep the surrounding sentences. (I did *not* flag RegisteredAdmissible's "since the emitted triple's type slot is `K`, not `K_j`" — that one names the genuine K-vs-K_j subtlety the lemma exists to discharge, so it earns its place.)

## OUT_OF_SCOPE

### Topic 1: Substrate-enforced single-tuple-scope for retraction

The note proves single-tuple-scope is an *app obligation* under the static gate, because `Sh-conf` consults no state-indexed address set and so cannot test R-Scope's P-tgt (target is a leaf link address or self-emit). This is the correct conclusion for a static gate — the ghost-root example shows the gate clearing while scope fails wholesale. A substrate that *enforced* leaf-targeting would need a state-dependent retraction discipline, a different design from this framework's static gate.

**Why out of scope**: Enforcing P-tgt requires reading `dom(Σ.L)` at emit time, which contradicts this note's static-gate thesis. It is new territory for a successor note, not a defect here; the note is right to surface it as an app obligation rather than silently leave the gap.

META: none — the note defines a state component (registry), an operation refinement (`K.λ_sh`), and reachable-state invariants (P1–P6) abstractly enough that any implementation would have to satisfy them; it is squarely in specification territory.

VERDICT: REVISE
