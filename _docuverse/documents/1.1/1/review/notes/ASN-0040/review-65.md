# Review of ASN-0040

## REVISE

### Issue 1: The "S2 exception" is deferred to from four separate sites
**ASN-0040, S2 discussion / B6 intro / B6 necessity proof / B6 postcondition (b)**: The same fact — that condition (i) is retained at the d=1 trailing-zero case for injectivity rather than for T4 — appears in four places:
- S2 prose: "Admitting ([1, 0], 1) would give two distinct namespaces sharing their entire stream, so B6(i) excludes such parents to keep the namespace map injective — the one point where (i) is retained beyond what T4 alone forces."
- B6 statement: "Condition (i) is necessary for T4 except at the d = 1 trailing-zero case (S2), where it is retained to keep the namespace map injective."
- B6 necessity sub-case (b): "The load-bearing case for T4-necessity is d = 2 (the d = 1 case is the S2 exception)."
- B6 postcondition (b): "with one exception: the d = 1 trailing-zero case (the S2 exception)."

**Problem**: This is exactly the forward-reference accretion pattern the `review-mode.anti-bloat` classifier targets — multiple paragraphs in different sections deferring to the same point. The precise reader must reassemble one claim from four scattered restatements.
**Required**: State the injectivity motivation once (at S2, where it is derived) and let B6 cite it by label without re-narrating it three more times.

### Issue 2: B8 is labeled "Global Uniqueness" but proves only co-reachable uniqueness
**ASN-0040, B8**: "B8 (Global Uniqueness). Distinct *co-reachable* baptismal acts produce distinct addresses... B8 establishes uniqueness only along a single transition path; cross-branch uniqueness... is unaddressed."
**Problem**: The label "Global Uniqueness" overclaims. The foundation's `GlobalUniqueness` (ASN-0034) is unconditional across all allocation events; reusing that name for a strictly weaker, path-scoped result invites the reader to assume the stronger guarantee. The scoping is *correct* (two incomparable branches can deterministically compute the same `c₁`, so unconditional uniqueness is false here) — but the name contradicts the proven content.
**Required**: Rename to reflect the actual scope (e.g., "Co-reachable Uniqueness" / "Single-Path Uniqueness") so the label and the postcondition agree.

### Issue 3: B6 condition-(iii) subsumption explained twice
**ASN-0040, B6 statement and B6 necessity proof**: The statement says "(at d = 1 it reduces to zeros(p) ≤ 3 and is subsumed by condition (i))"; the necessity proof repeats "At d = 1, condition (iii) reduces to zeros(p) ≤ 3, which is already implied by condition (i)... there it adds nothing and is subsumed by (i) rather than independent."
**Problem**: The postcondition (b) then asserts "(i), (ii), (iii) are jointly necessary... violating any single one forces a T4 violation," which is loose: at d=1 you cannot violate (iii) while satisfying (i), so the per-condition necessity holds only at d=2 for (iii). The body says this twice but the postcondition still phrases it as uniform single-condition necessity.
**Required**: State the subsumption once, and tighten postcondition (b) to "each condition is necessary at the depth where it binds (iii independently only at d=2)."

### Issue 4: B3 fourth-quadrant sentence enumerates a case the requirement already excludes
**ASN-0040, B3**: "The fourth quadrant — t ∉ s.B ∧ Occupied(t, s) — is precisely the negation of the requirement, hence forbidden."
**Problem**: This sentence imagines and then forbids the exact configuration the stated implication `Occupied(t,s) ⟹ t ∈ s.B` already excludes by definition. It advances no reasoning beyond restating the requirement's contrapositive — meta-prose in a structural slot.
**Required**: Delete; the three permitted quadrants plus the implication are self-sufficient.

### Issue 5: B9 trace Steps 6–7 are near-verbatim repetitions of Step 5
**ASN-0040, "B9 unbounded extent exhibited"**: Steps 6 and 7 repeat Step 5's structure essentially unchanged ("By B2, c_{hwm+1} = c₄. B1: children = {c₁, c₂, c₃, c₄}, contiguous prefix of length 4." / "...= c₅... length 5").
**Problem**: One iteration of `inc(·,0)` already demonstrates the pattern; three identical steps to climb from m=2 to M=5 add length without adding evidence. A concrete example is welcome (and Steps 1–5 earn it), but the tail iterations are padding.
**Required**: Collapse Steps 6–7 into a single "and so on for M−m further steps" remark after Step 5.

## OUT_OF_SCOPE

### Topic 1: Cross-branch (non-co-reachable) address uniqueness
**Why out of scope**: B8 correctly scopes itself to co-reachable acts and the ASN flags cross-branch uniqueness as unaddressed. Two incomparable reachability branches computing the same deterministic `next` is a replication/coordination concern, matching the deferred BEBE/cross-replica open question — new territory, not a defect here.

### Topic 2: Alignment of foundation `allocated(s)` with `s.B`
**Why out of scope**: The relationship `allocated(s) ⊆ s.B` and the activation discipline aligning allocator-extension transitions with baptismal operations is named as an open question and depends on machinery (allocator activation, genesis coverage) outside this note's growth-law mandate.

VERDICT: REVISE
