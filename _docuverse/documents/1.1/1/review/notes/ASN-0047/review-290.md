# Review of ASN-0047

I read the full transition model. The technical core — the five-component state, the seven elementary transitions, the J0/J1★/J1'★ couplings, P3 confinement, and the per-state/composite-boundary split — is sound, and the worked examples exercise the genuinely hard cases (interior replacement, k=0 fork edit-inheritance, link orphaning). My findings are one genuine coverage gap plus three presentational issues the `anti-bloat` classifier asks me to surface. I am not re-raising the previously-declined splitting/sprawl/matrix-expansion findings.

## REVISE

### Issue 1: C1c (and M1) inherited invariants are never accounted for
**ASN-0047, *Extended reachable-state invariants* + *Inherited from foundation* table**: The Class (a) per-state list and the inherited table both carry **L1c (LinkAllocatorConformance)** and verify its preservation in depth (the *L1c* prose reconstructs the structural inc-chain step by step). The content analogue **C1c (ContentAllocatorConformance)** — a foundation invariant of ASN-0093 with identical shape (`k₁ = 2`, per-step `kᵢ ∈ {0,1,2}`, length monotonicity) — appears in neither list and is never verified for K.α, even though K.α's definition asserts "`a` produced by `origin(a)`'s content sub-allocator." Likewise **M1 (ArrangementMonotonicity, ASN-0093)** is absent: since K.μ⁻ contracts individual `M(d)`, a reader must be told explicitly that M1 ranges over `dom(M) = E_doc` (which only grows) and not over `dom(M(d))`.

**Problem**: Asymmetric coverage. The reader who trusts L1c's careful treatment has no parallel assurance for C1c, and M1's compatibility with arrangement contraction is left implicit precisely where it is most likely to be doubted.

**Required**: Add a C1c row/paragraph to Class (a) mirroring the L1c discharge (first emission via SubAllocatorBundle, subsequent via TA5(c)), and add M1 to the inherited table with one line clarifying it constrains `dom(M)`, not `dom(M(d))`.

### Issue 2: The ~30-label per-state invariant list is enumerated verbatim three times
**ASN-0047, *Extended reachable-state invariants***: The full conjunction `S2 ∧ S3★ ∧ S3★-aux ∧ S4 ∧ … ∧ CL-OWN ∧ CL-UNIQ` is written out in the section preamble's bullet, again in the `ExtendedReachableStateInvariants` definition, and a third time in the "Class (a)" proof header. The composite-boundary triple `P4★ ∧ P4a ∧ P7a` is likewise repeated.

**Problem**: Three verbatim copies of a long label list is exactly the accretion the anti-bloat classifier targets — any future edit must keep three copies in sync, and the reader gains nothing from the repetition.

**Required**: State the per-state and composite-boundary partitions once (the `ExtendedReachableStateInvariants` definition is the natural home) and have the preamble and proof header reference it rather than re-list.

### Issue 3: Clause (v)'s independence construction restates what LRP already establishes
**ASN-0047, *Decomposition of K.μ~*, admissibility clause (v)**: The text proves clause (v) is independent of (i)–(iv) by constructing a within-`s_L` transposition, then in the same passage states "The full-clearance decomposition cannot realise such a re-seating: the link subspace is retained pointwise (LRP)… so every realisable π fixes the link subspace."

**Problem**: The constructed within-`s_L` permutation is a case the carrier (the full-clearance K.μ⁻+K.μ⁺ realisation) already excludes by LRP — the "imagines a case the carrier already excludes" pattern. The independence argument and the LRP "cannot realise" statement are two passes at the same point. Compounding the confusion, clause (v) is presented as an independent *admissibility hypothesis* (a precondition on π) when it is in fact forced by the chosen realisation; the later *Link V-position permanence* paragraph then walks back the apparent "links cannot be reordered" guarantee via withdraw-and-re-add.

**Required**: Collapse the two passes into one — either derive clause (v) from LRP (it is a consequence of the realisation, not a free design choice) or keep it as an independent clause but cut the duplicate "cannot realise" restatement. State once, at clause (v)'s introduction, that single-K.μ~ link fixity is a realisation artifact, not a lifetime guarantee, and drop the redundant re-explanation in *Link V-position permanence*.

### Issue 4: Rationale-over-statement prose around P4★ and J0
**ASN-0047, P4★ definition and J0**: P4★'s definition is followed by a paragraph arguing *why* the unscoped `Contains(Σ) ⊆ R` "cannot hold once any link-subspace mapping exists" (a P7-incompatibility essay). J0 carries the rationale "in Nelson's model content enters the docuverse only by being placed in a document, so there is no orphan content."

**Problem**: These explain why the property/axiom is needed rather than tightening what it says — the meta-prose pattern flagged for this classifier. The P4★ paragraph in particular re-derives a relationship (link pairs excluded by P7) that S3★/L14 already make structural.

**Required**: Reduce the P4★ rationale to a single clause noting the content-subspace scoping coexists with P7, and trim the J0 motivation to a one-line Nelson citation.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal with renumbering (DELETEVSPAN compaction)
**Why out of scope**: The penultimate Open Question correctly defers the renumbering-aware interior link-arrangement contraction to a future ASN. K.μ⁻'s suffix-only contraction is a faithful abstract choice here; the interior-compaction operation is named-operation territory (explicitly excluded by the Scope section), not a defect in this ASN.

META: not applicable — the ASN defines state, abstract transitions, and their invariants, and stays out of named-operation and implementation territory.

VERDICT: REVISE
