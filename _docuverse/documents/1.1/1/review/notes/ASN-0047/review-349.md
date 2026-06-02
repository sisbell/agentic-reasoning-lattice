# Review of ASN-0047

I read the full transition model, checked the per-elementary verification matrix and its prose, the K.μ~ decomposition (admissibility (i)–(v), K.μ~-FIX, K.μ~-RANGE, necessity/sufficiency), the J4 fork variants, and the seven worked examples. The core induction is sound: the per-state/composite-boundary split is well-motivated, FrontierEquivalence/ActivatedEmission/K.δ-case-(ii) are non-circular (proper induction on prior-state ActivatedEmission), and the φ-bijection fork characterization (order + multiplicity) with derived range-equality is correctly exercised by the duplicate-source example. I found no proof-level gap. Two issues remain, both presentation.

## REVISE

### Issue 1: Stale section cross-reference in the inductive base case
**ASN-0047, *Extended reachable-state invariants*, Base paragraph**: "The extended initial state Σ₀ satisfies every per-state invariant (verified in the Link store and extended system state section — L₀ = ∅ satisfies link invariants vacuously...)."

**Problem**: There is no section titled "Link store and extended system state." The actual base-case verification (link invariants vacuous, S3★ reducing to S3, P4★ reducing to the unscoped bound, D-CTG★/D-MIN★ vacuous) is the **Initial state invariant verification** block under *The state model*. The pointer is a stale name left from an earlier structure, and the base case is the load-bearing anchor of both inductions — a reader sent to a non-existent section cannot confirm it.

**Required**: Repoint the reference to *The state model* / "Initial state invariant verification."

### Issue 2: Forward-reference accretion — k=2 spawn discharge deferred from a precondition slot
**ASN-0047, *Elementary transitions*, K.δ case (ii) k=2 precondition**: "(Which sub-allocator this k = 2 spawn activates, and the sourcing of its spawnPt-membership premise, are identified once in ParentAllocatorDispatch and applied in *K.δ case (ii) discharge*; only the zeros/parent identities above are needed at the precondition.)"

**Problem**: This is a navigational note in a structural slot (the precondition definition) that defers a single argument to two downstream locations and tells the reader which parts are *not* needed here. It is the "multiple paragraphs defer to the same downstream location" / "deferred to Y" pattern: the precondition states the zeros/parent identities it actually uses, so the parenthetical advances no claim — it only manages the reader's expectation about where the rest lives. The k=2 discharge already has a dedicated section and a dedicated sub-lemma (ParentAllocatorDispatch); the precondition does not also need to forecast them.

**Required**: Delete the parenthetical. The precondition should state only the conjuncts it discharges (zeros bound, parent identity, spawn admissibility, freshness via ChildSpawnFreshness); the activation/spawnPt machinery is reached through the normal section flow without an inline forecast.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link/content withdrawal
**Why out of scope**: K.μ⁻'s suffix-only contraction (interior removal requires the K.μ⁻+K.μ⁺ replacement composite) is faithful to the gap-free POOM for suffix deletes; modeling the implementation's compact-and-renumber `DELETEVSPAN` is named operation territory and is already logged in Open Questions, not a defect here.

VERDICT: REVISE
