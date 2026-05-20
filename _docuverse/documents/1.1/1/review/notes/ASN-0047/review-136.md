# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ dependency chain Step (A) implicit dependency on content-side subspace preservation
**ASN-0047, "Decomposition of K.μ~"**: "Step (A) — S3★(Σ') and admissibility clause (i). [...] *Does not consume:* subspace preservation under π, link-subspace fixity, CL-UNIQ."

**Problem**: Step (A) claims independence from subspace preservation (Step B). But the proof of Step (A.2) discharges S3★(Σ') by stating "the K.μ⁺ amendment forces every new V-position to subspace = s_C" while K.μ⁺ in the full-clearance form writes at positions `{π(v) : v ∈ V_{s_C}(d)}`. For the amendment to be satisfied on this set, π must map V_{s_C}(d) into V_{s_C} — i.e., π must preserve content-side subspace. If π violates this (mapping a content v to a link π(v)), the K.μ⁺ amendment fails and the realization cannot fire. Step (A) thus implicitly assumes content-side subspace preservation; Step (B) then derives the full bidirectional form. The chain's framing of (A) and (B) as having distinct, non-overlapping dependencies is logically muddled. The proof works because admissibility (i) + L14 forces subspace preservation directly — but the dependency-chain presentation hides this.

**Required**: Either restate Step (A)'s consumed conditions to include "content-side subspace preservation under π" explicitly, or restructure the chain to derive subspace preservation immediately from admissibility (i) + L14 as a single step, with Step (A) and Step (B) collapsed into derivations that share the admissibility hypothesis transparently.

### Issue 2: K.μ~ "preservation" framing in verification matrix is tautological for S3★
**ASN-0047, ExtendedReachableStateInvariants Class (a) matrix, S3★ row, K.μ~ column**: "preserved via K.μ⁻ restriction + K.μ⁺ amendment alone (link-subspace fixity is downstream, not prerequisite)"

**Problem**: S3★(Σ') is part of K.μ~'s admissibility clause (i) by definition — K.μ~ does not fire unless the post-state satisfies S3★. The matrix cell treats this as elementary preservation analogous to other transitions (K.α, K.δ, K.μ⁺) where the post-state property is genuinely derived from preconditions plus elementary effects. For K.μ~, the post-state S3★ is *stipulated* by admissibility rather than mechanically derived. The same applies to the S8a, S8-depth, D-CTG★, D-MIN★ rows under K.μ~ — all listed in admissibility (i). Calling these "preserved" conflates definitional stipulation with mechanical derivation, masking the actual structure: admissibility (i) selects which π's K.μ~ can realize, and the K.μ⁻ + K.μ⁺ realization mechanically produces the stipulated post-state.

**Required**: Mark admissibility-stipulated invariants explicitly in the K.μ~ column (e.g., "stipulated by admissibility (i)") and reserve "preserved via decomposition" for invariants whose preservation is genuinely derived from the elementary steps (S8★, S3★-aux, CL-OWN, CL-UNIQ, S4, etc.). Without this distinction, the matrix's uniform framing misrepresents the structure of the K.μ~ argument.

### Issue 3: Missing worked example for K.δ k=0
**ASN-0047, "Worked example" sections**: The ASN exercises K.δ case (i) (entity hierarchy), K.δ case (ii) k=2 (account and document descent), and K.δ case (ii) k=1 (fork). K.δ case (ii) k=0 is discussed in prose under "K.δ case (ii) discharge and parent-allocator activation" and "Allocator hierarchy under documents" but never traced through a concrete state transition.

**Problem**: K.δ k=0's freshness discharge is structurally distinct from k ∈ {1, 2}: it uses FrontierEquivalence (a derived lemma chaining TA5(c) + P1 + operational precondition), not the direct T10a per-`(t, k')` uniqueness axiom. The dispatch through T10a.6 (DomainDisjointness) against the operand's actual provenance (e.g., A_v(d₁) vs A_doc(parent(d₁))) is also unique to k=0. The matrix entry "T10a chain-advancement uniqueness at (t, 0) (derived form, via FrontierEquivalence)" carries weight that's only exercised in prose. Without a worked example, the FrontierEquivalence + T10a.6 dispatch route is harder to validate against concrete addresses.

**Required**: Add a worked example for K.δ k=0 — e.g., allocating a second sibling document under an existing account (operand t = first document under A, output `inc(t, 0)`) or a second version on an existing version chain (operand t = first version of d', output `inc(t, 0)`). The example should trace (a) FrontierEquivalence discharge of `inc(t, 0) ∉ E`, (b) T10a.6 dispatch identifying t's owning allocator, (c) verification of K.δ-ID.parent-0/1 and K.δ-ID.zeros-0/1 against concrete tumblers.

### Issue 4: Missing worked examples for two-step and three-step replacement composites
**ASN-0047, "Elementary transitions" Replacement enumeration**: The ASN catalogues three forms of content replacement — *two-step* (prior-provenance transcluded), *three-step* (first-time transcluded), *four-step* (fresh-content). Only the four-step form is exercised in "Worked example: interior content replacement."

**Problem**: The three forms differ substantively in their coupling discharge. The two-step form's substantive precondition `(a, d) ∈ R` (pre-state provenance from prior insertion-deletion cycle) is what distinguishes it from the three-step form; J1★ at the composite boundary is discharged by `(a, d) ∈ R ⊆ R'` via P2 rather than by a trailing K.ρ. The three-step form is the first-time cross-document transclusion case where `a ∈ dom(C)` already but `(a, d) ∉ R`; J1★ requires a K.ρ to record the freshly introduced provenance pair. These are conceptually different patterns and exercising only the four-step form leaves the prior-provenance constraint untested.

**Required**: Add either a worked example for the two-step or three-step form, or explicit verification traces showing how J1★ and J1'★ are discharged for each. In particular, the two-step's reliance on pre-state `(a, d) ∈ R` should be exercised against a concrete scenario where d previously contained a, was contracted, and then re-arranges a.

### Issue 5: K.δ-ID identities framed as new properties in the table rather than as derived consequences
**ASN-0047, "Properties Introduced" table, "New properties introduced by this ASN"**: K.δ-ID.zeros-0/1, K.δ-ID.zeros-2, K.δ-ID.parent-0/1, K.δ-ID.parent-2 are listed alongside genuinely novel structural commitments (Σ.E, Σ.R, the elementary transitions, J0/J1★/J1'★, etc.).

**Problem**: The K.δ-ID identities are derived consequences of TA5 (HierarchicalIncrement, ASN-0034) and T4b (UniqueParse, ASN-0034) — they are useful named handles for downstream citation, not new structural specifications. Placing them in the "New properties introduced by this ASN" table conflates derivational shortcuts with primitive specifications. The table loses precision when downstream readers cannot distinguish primitive commitments (which must be evaluated for soundness) from derived shortcuts (which are evaluated against their derivation chain).

**Required**: Move K.δ-ID entries into a separate subsection ("Derived structural identities") of Properties Introduced, or tag each K.δ-ID row with its derivation source (e.g., "derived from TA5(c)/(d) + T4b"). The promotion-to-named-handle is reasonable; the framing as "new property" is not.

## OUT_OF_SCOPE

### Topic 1: Span-level operations and named operations (INSERT, DELETE, COPY)
The Scope section explicitly excludes these. The ASN's elementary transitions operate per-V-position; span operations and named user-facing operations belong to a higher-layer ASN.

### Topic 2: Concurrent transition semantics
SequentialTransitionAxiom forbids interleaving by stipulation. The Scope section excludes operation atomicity and concurrency; concurrent semantics belong to a higher-layer ASN.

### Topic 3: Link withdrawal mechanism (tombstoning beyond suffix removal)
The Open Questions section catalogues this as future work. A separate mechanism (status flag on the link record, retraction-link convention, version-scoped membership) would be needed to reconcile Nelson's tombstoning design (LM 4/9) with D-CTG★/D-MIN★'s suffix-only contraction discipline. Not in this ASN's scope.

### Topic 4: Type-only and one-sided link semantics
K.λ admits empty endsets at slots e₁ and e₂ (one-sided links, type-only markers) per L4 (EndsetGenerality). Whether to narrow K.λ with `e₁ ∪ e₂ ≠ ∅` and how endset-iterating consumers should handle these cases is design-uncertain per Open Questions. Not in this ASN's scope.

### Topic 5: Node-allocation registry mechanism
NodeUniqueAllocation, NodeRegistryBootstrap, and the external registry are stated as axioms. Open Questions explicitly defers the registry's concrete mechanism (issuing protocol, persistence, concurrency) to a future ASN; this ASN treats the registry as a black box at the abstraction boundary.

VERDICT: REVISE
