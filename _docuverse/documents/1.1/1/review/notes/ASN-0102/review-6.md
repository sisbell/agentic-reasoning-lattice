# Review of ASN-0102

## REVISE

### Issue 1: P6 preservation rationale cites the wrong frame component
**ASN-0102, X14 (final paragraph)**: "The per-state Class (a) conjuncts touching the link store, entity set, and node lineage — L0, L1, … , **P6**, P8, NodeLineage — are preserved because COPY's frame leaves `Σ.L` and `Σ.E` untouched … so every clause quantifying over `dom(Σ.L)`, `E`, or link-subspace positions holds at `Σ'` exactly as at `Σ`."

**Problem**: P6 (ExistentialCoherence, ASN-0047) is `(A a ∈ dom(C) :: origin(a) ∈ E_doc)` — it quantifies over `dom(C)`, **not** over `dom(Σ.L)`, `E`, or link-subspace positions. The stated justification ("frame leaves `Σ.L` and `Σ.E` untouched") does not cover P6's quantification. P6 is in fact preserved, but for a different reason than the one given.
**Required**: Move P6 out of the link/entity group and discharge it explicitly: `dom(C)` is unchanged (X1) and `E` is unchanged (`Σ'.E = Σ.E`), so `(A a ∈ dom(C) :: origin(a) ∈ E_doc)` carries forward intact. (P8 and NodeLineage are correctly grouped, since they genuinely quantify over `E`.)

### Issue 2: X8 within-reference non-coalescence is asserted, not derived
**ASN-0102, X8**: "Within a single reference, consecutive runs are the maximal runs of that reference (C1a, M12), hence pairwise non-I-adjacent **by definition of maximality**; they never coalesce."

**Problem**: "By definition of maximality" is a property of a *single* run (it cannot be right-extended). Concluding that two *distinct* consecutive runs are non-I-adjacent requires an intermediate step that is omitted: the runs must first be shown V-adjacent (so that maximality's no-right-extension condition `f(vⱼ+nⱼ) ≠ aⱼ+nⱼ` actually bears on the next run's I-start). This is "X follows from Y" stated as a one-liner where a two-step argument is needed.
**Required**: Show the chain explicitly — the reference span `⟦σ⟧` is contiguous and fully populated (content-reference well-formedness + C0a), so `dom(f)` is V-contiguous and consecutive maximal runs are V-adjacent (`vⱼ₊₁ = vⱼ + nⱼ`); then maximality (run `j` cannot be right-extended) gives `aⱼ₊₁ ≠ aⱼ + nⱼ`, i.e. non-I-adjacency, so M7's merge condition fails.

### Issue 3: X14 New/Old distinction introduced as a dangling paragraph
**ASN-0102, X14**: between the *J0* bullet and the *J1★* bullet, an unbulleted paragraph ("We must distinguish *newly mapped at a position* from *new to the range*. Write the copied address set `A` … `New` … `Old` …") appears.

**Problem**: The `New`/`Old` split is the setup for the J1★ and J1'★ discharges, but it is wedged after the (vacuous) J0 bullet with no structural marker, reading as if it belonged to J0. A reviewer cannot tell at a glance which obligation it serves.
**Required**: Promote it to its own labelled lead-in before the J1★/J1'★ bullets, or fold the definitions of `New`/`Old` into the J1★ bullet where they are first used.

## OUT_OF_SCOPE

### Topic 1: Re-displacement and continued discoverability of copied origin
The four Open Questions (later displacement of copied content, onward referencing of by-reference content, time-varying resolution, identity when the allocating document is unreachable) are correctly posed as future work and are not claimed here. No flag — recorded only to confirm they were read and judged out of scope, not omissions.

VERDICT: REVISE
