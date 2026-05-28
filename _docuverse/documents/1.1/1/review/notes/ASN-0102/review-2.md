# Review of ASN-0102

## REVISE

### Issue 1: Operation effect on state components L, E, R is unspecified

**ASN-0102, Definition of COPY**: The definition gives only `Σ'.C = Σ.C`, `(A d' : d' ≠ d : Σ'.M(d') = Σ.M(d'))`, and the target arrangement `Σ'.M(d)`.

**Problem**: The standing state is `Σ = (Σ.C, Σ.L, Σ.E, Σ.M, Σ.R)` (ASN-0047). The Definition never states the frame for `Σ.L`, `Σ.E`, or `Σ.R`. The wp(S3★) derivation later *asserts* "`dom(Σ'.L) = dom(Σ.L)` (COPY's frame leaves `Σ.L` untouched)" — but the Definition contains no such clause. An operation contract must pin every component of the post-state; a reader cannot verify L12 (link immutability) or P-invariants from an undeclared frame.

**Required**: State the complete frame in the Definition: `Σ'.L = Σ.L`, `Σ'.E = Σ.E`, and the effect on `Σ'.R` (see Issue 2).

### Issue 2: The coupling invariant J1★ is never discharged

**ASN-0102, X14**: "the content-containment relation `Contains_C(Σ')` records `(a_j + i, d)`."

**Problem**: `Contains_C(Σ')` is *derived* from `Σ'.M` and so is automatic, but the provenance relation `Σ.R` is a distinct state component. COPY extends the content-subspace range with `ran(Σ'.M(d)) ∖ ran(Σ.M(d))` (X3), and J1★ (ExtensionRecordsProvenanceContentSubspace, ASN-0047) requires `(a, d) ∈ R'` for exactly these newly-mapped content addresses. As a valid composite (ValidComposite★), COPY must satisfy J0, J1★, and J1'★ between pre- and post-state. The note never records provenance, never adds the required K.ρ effect, and never checks any coupling constraint. X14 conflates the derived `Contains_C` with the provenance obligation on `R`.

**Required**: Specify COPY's effect on `Σ.R` (record provenance for each copied content address) and discharge J0/J1★/J1'★ explicitly, or justify why COPY is exempt.

### Issue 3: COPY's transition status (elementary vs. composite) is left undeclared, undermining X15

**ASN-0102, X15**: "no intermediate state is observable in which the displacement has been applied but the copied region not yet laid down."

**Problem**: COPY *relabels* existing V-positions — every content-subspace position `u ≥ v` has its image moved to `u + W`. The foundation's K.μ⁺ (ArrangementExtension, ASN-0047) requires `M'(d)(v) = M(d)(v)` for all old positions, so COPY is **not** a single K.μ⁺ transition. The note neither names a new elementary transition nor presents COPY as a composite. If COPY is a composite of K.μ steps, then by ValidComposite★ intermediate states *do* exist between its atomic steps — directly contradicting X15's "no intermediate state observable." The appeal to SequentialTransitionAxiom only grants atomicity to *single* transitions, which COPY has not been shown to be.

**Required**: Declare whether COPY is one elementary transition (and add it to the transition vocabulary Σ with its own frame) or a composite (and weaken X15 to the composite-boundary guarantee). The coupling discharge in Issue 2 depends on this answer.

### Issue 4: X8's claim that distinct references carry distinct origins is false

**ASN-0102, X8**: "distinct content references carry distinct `homedoc`, so the first gate fails and a separate crum is emitted per reference (Q8). The constructed count and the green implementation's count thus agree at `k`."

**Problem**: Two content references may resolve to content sharing one origin — either both target the same source document, or both transclude from a common ancestor (so `d_1 ≠ d_2` yet `origin = d_0`). Then `homedoc` is equal, and if the boundary is also I-adjacent, `isanextensionnd`'s twin gates (`homedoc` equality ∧ I-adjacency) both pass and the implementation *would* coalesce, yielding fewer than `k` crums. This contradicts the note's own correct analysis two sentences earlier (canonical count `≤ k`, equality *iff* no inter-reference boundary is I-adjacent). The blanket "distinct references carry distinct homedoc" is unsupported.

**Required**: Drop the false premise; argue the constructed-count claim from the construction itself (one block per maximal run, V-adjacent lay-down), and state Gregory's agreement only for the case where no inter-reference boundary is I-adjacent.

### Issue 5: First Open Question appears already answered by X10/X15

**ASN-0102, Open Questions**: "What must a placement operation guarantee about the consistency of a self-transclusion when the target position lies strictly inside the source span?"

**Problem**: X10 and X15 already resolve this: `resolve_Σ(R)` is pinned to the pre-state by SequentialTransitionAxiom, so the source span is read as a frozen image *before* displacement opens the gap — precisely the target-inside-source case. Listing it as open, while X10 claims to handle "self-transclusion," is internally inconsistent.

**Required**: Either remove the question (resolved by X10/X15) or state the residual guarantee X10's atomicity argument does not cover.

## OUT_OF_SCOPE

### Topic 1: Position-management mechanics of the forward shift
**Why out of scope**: The displacement is shared with INSERT, which the scope list excludes. The note correctly defers it ("its position-management mechanics are not the subject of this note"). (Note: this exclusion does not cover COPY's own transition status — see Issue 3.)

### Topic 2: Later re-displacement, version correspondence, and onward-reference containment
**Why out of scope**: Open Questions 2–5 concern subsequent operations, version creation, and reachability of allocating documents — future-ASN territory, not defects here.

VERDICT: REVISE
