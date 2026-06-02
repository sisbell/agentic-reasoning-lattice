# Review of ASN-0047

## REVISE

### Issue 1: Duplicated exposition of the per-state vs. composite-boundary distinction
**ASN-0047, *Extended reachable-state invariants* preamble and *Scoped coupling constraints***: The two-class temporal-scope distinction is stated in full in the bulleted preamble ("*Per-state invariants* hold at **every** reachable state... *Composite-boundary properties* hold only at *composite boundaries*..."), then restated in the *ValidComposite★* discussion ("Intermediate states need not satisfy all system invariants; only the final state is required to"), and gestured at a third time in the parenthetical under ExtendedReachableStateInvariants ("P4★ and P7a are per-state properties holding at boundaries; P4a is a trace property...").
**Problem**: Two passages say the same thing in different words; the reader re-derives the same Class (a)/(b) split each place. This is meta-prose around the matrix that does not advance the argument.
**Required**: State the distinction once (the preamble is the right home) and have the later sections reference it rather than re-explain it.

### Issue 2: Near-tautological elaboration in the K.μ⁺ definition
**ASN-0047, *Elementary transitions*, K.μ⁺**: "The two conjuncts together force new mappings at positions disjoint from dom(M(d)). For any v ∈ dom(M'(d)) \ dom(M(d)), v is a new position by construction. For any v ∈ dom(M(d)), the value-preservation clause pins M'(d)(v) = M(d)(v)... Hence dom(M'(d)) \ dom(M(d)) — the set of newly-mapped positions — is exactly the set of positions disjoint from dom(M(d))..."
**Problem**: This paragraph proves that "newly-mapped positions are the positions not already in the domain" — a restatement of the effect clause `dom(M'(d)) ⊃ dom(M(d))` plus value-preservation, with no new content. It is essay-length elaboration of a definitional consequence in a structural slot.
**Required**: Delete or compress to one clause; the effect/precondition pair already carries it.

### Issue 3: K.δ case (ii) dispatch is split across two sections that re-enumerate the same k-cases
**ASN-0047, K.δ definition case (ii) and *K.δ case (ii) discharge and parent-allocator activation***: The k ∈ {0,1,2} sub-case requirements, structural identities, freshness mechanism, and parent-allocator activation are partitioned across the definition (which forward-defers: "discharged in §*K.δ case (ii) discharge and parent-allocator activation*") and a later section that re-walks k = 0, 1, 2 from scratch.
**Problem**: The reader must hold both enumerations simultaneously; the later section re-states the three regimes the definition already introduced, matching the forward-reference-accretion pattern (relocated/duplicated case enumeration with cross-section deferral). It is not clear which location is authoritative for, e.g., the k = 1 spawn-admissibility conjuncts.
**Required**: Consolidate the per-k contract and its discharge into one location, or make the definition state only the contract and the discharge section reference (not re-list) the sub-cases.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link withdrawal
The ASN models link-subspace contraction by suffix removal only; interior withdrawal with survivor renumbering is correctly deferred (Open Questions). This is new operation territory, not a defect here.

### Topic 2: Type-only / one-sided links (empty endsets)
Whether K.λ should require `e₁ ∪ e₂ ≠ ∅` is raised in Open Questions; endset-emptiness semantics for discovery consumers belong to a future link-semantics ASN.

VERDICT: REVISE
