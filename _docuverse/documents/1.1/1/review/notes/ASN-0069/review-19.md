# Review of ASN-0069

## REVISE

### Issue 1: Worked example omits the empty-source case

**ASN-0069, "Worked Example"**: The example fixes `M(d_src)` with three content positions `[s_C, 1] ↦ a₁, [s_C, 2] ↦ a₂, [s_C, 3] ↦ a₃` and one link position, then demonstrates V1–V12 against this populated state.

**Problem**: V7 is a *normative* behavior of the operation — it commits to producing an empty fork (K.δ-alone composite, no K.μ⁺, no K.ρ) when `V_{s_C}(d_src) = ∅`, and rejects rejection as inadmissible. The worked example never exhibits this boundary case. The ASN takes the trouble to argue V7 must be admitted (citing CREATENEWDOCUMENT-produced empty documents and V11 chain coherence), but never instantiates it. A reader checking V7 against a specific scenario — fork of an empty `d_src`, fork of a fork of an empty source, fork where `V_{s_C}(d_src) = ∅` but `V_{s_L}(d_src) ≠ ∅` (so the source has only links) — finds nothing.

**Required**: Add a short empty-source vignette to the worked example demonstrating: (i) `M'(d_new) = ∅` after the K.δ-alone composite; (ii) `R' = R` (no provenance pairs added); (iii) V12 holds vacuously over `ran(M'(d_new)) = ∅`; (iv) the link-only sub-case (source with `V_{s_L}(d_src) ≠ ∅, V_{s_C}(d_src) = ∅`) confirms the fork's link subspace is still empty (V6) and the source's links remain intact (V5).

## OUT_OF_SCOPE

### Topic 1: Concurrent modification semantics
**Why out of scope**: The first open question ("guarantee when a fork is invoked while the source's arrangement is being concurrently modified") is appropriately deferred. ASN-0047's SequentialTransitionAxiom forces total ordering; concurrency control beyond that is a future operations concern.

### Topic 2: Snapshot vs. living fork distinction
**Why out of scope**: Distinguishing snapshot forks from "living" forks (whose inherited positions track the source's evolving arrangement) is a different operation than the one derived here. V4b fixes literal-inheritance snapshot semantics; admitting a living-fork variant would require new operations, not changes to V0.

### Topic 3: Version-space coherence over the set of all forks
**Why out of scope**: This is version DAG structure — explicitly listed as out of scope.

VERDICT: REVISE
