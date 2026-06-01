# Review of ASN-0047

This is a mature, largely sound ASN. The transition taxonomy, the per-state / composite-boundary split, the K.μ~ decomposition, and the worked examples hold up under checking. The operations are boundary-complete (K.μ⁻ guarded by `dom(M(d)) ≠ ∅`; K.μ⁺ first-insertion via ValidFirstInsertionPosition; K.μ~ guarded by the non-constant-content-subspace precondition, which correctly excludes the equal-valued-transclusion no-op). I found no correctness defect in the invariant-preservation arguments. The findings below are the forward-reference / deferral patterns the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Deferral chain (and a misdirected pointer) for the K.μ~ "full-clearance form" canonical statement
**ASN-0047, *Decomposition of K.μ~***: Step (A) says the decomposition is "in the full-clearance form whose canonical statement is given in §*Necessity and sufficiency of the precondition* below." The sufficiency proof in that subsection then says "the full-clearance form ... — stated in §*Decomposition of K.μ~* below — realises it." The canonical statement (`**Full-clearance form (canonical statement).**`) actually lives in the trailing `**Decomposition.**` paragraph of the *same* section.

**Problem**: Two load-bearing proof steps (Step (A) and the sufficiency proof) lean on a statement given only later, reached via a chain of forward pointers. Worse, Step (A)'s pointer is misdirected: it names §Necessity and sufficiency, but the canonical statement is in §Decomposition — §Necessity merely forwards again. The reader must chase Step (A) → §Necessity → §Decomposition to find what "full-clearance form" means, and "§*Decomposition of K.μ~* below" is a self-reference to the section the reader is already inside. This is the flagged "multiple paragraphs defer to a downstream location" pattern compounded into a chain.

**Required**: State the full-clearance form (`n'_{s_C} = 0`: clear the content subspace, retain link positions pointwise, rebuild content at fresh positions) once, at the head of the K.μ~ section before Step (A), and have Step (A), Step (B), and the sufficiency proof reference that single statement. Remove the intermediate forwarding pointer and the self-referential "§Decomposition of K.μ~ below."

### Issue 2: The primary allocation operations discharge their freshness obligation entirely by forward reference
**ASN-0047, *Elementary transitions* (K.α) and *Link allocation* (K.λ)**: K.α states "Freshness `a ∉ dom(C) ∪ dom(L)` ... is SubAllocFresh (lemma stated below, at *Allocator hierarchy under documents*)"; K.λ likewise defers `ℓ ∉ dom(L) ∪ dom(C)` to "SubAllocFresh at `x = L`."

**Problem**: Freshness is the load-bearing precondition of both allocation primitives (it is what makes S4, L11a, GlobalUniqueness, and the whole append-only discipline go through), yet at the point each operation is defined it is left as an unverified forward reference to a lemma two-to-three sections downstream (`SubAllocFresh`, itself built on `SubAllocatorBundle`). The reader cannot confirm the operation's core obligation without leaving the operation definition. This is the forward-pointer ordering pattern the anti-bloat pass targets — distinct from the operation's other preconditions, which are discharged in place.

**Required**: Either move the SubAllocFresh / SubAllocatorBundle machinery ahead of the elementary-transition definitions, or inline the one-line three-part freshness discharge (seed: SubAllocatorBundle.FirstEmission; frontier: GlobalUniqueness on the tracked chain; cross-subspace: SC-NEQ + T7) at K.α/K.λ so the operation's freshness obligation is self-contained at its point of statement.

## OUT_OF_SCOPE

### Topic 1: Forked-document arrangement correspondence to source
**Why out of scope**: The first Open Question (what invariants a fork's initial arrangement must satisfy relative to the source's current arrangement — identity, subset, run-structure preservation) is genuinely new territory. J4 establishes the fork composite and the range-containment `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}})` but deliberately leaves the correspondence-preservation question open; that belongs in a successor ASN, not this one.

### Topic 2: Link-withdrawal / tombstoning mechanism
**Why out of scope**: The Open Question on reconciling Nelson's tombstoning (LM 4/9) with D-CTG★/D-MIN★ (interior link withdrawal requiring a mechanism outside K.μ⁻'s suffix-truncation contract) is correctly identified as requiring a separate mechanism. The orphan-link state this ASN defines (K.λ without K.μ⁺_L) is the in-scope portion; status-flag/tombstone state is future work.

VERDICT: REVISE
