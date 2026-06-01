# Review of ASN-0047

## REVISE

### Issue 1: S8★ over-claims ASN-0036's S8 condition (b) for the link subspace
**ASN-0047, *Amendments to existing transitions*, S8★**: "the per-subspace arrangement `M(d)|_{V_S(d)}` decomposes into a finite set of correspondence runs `{(v_j, a_j, n_j)}` satisfying ASN-0036's S8 conditions (a) and (b)".

**Problem**: ASN-0036's S8 condition (b) literally reads "Well-defined label — `a = M(d)(v)` exists and is unique because `M(d)` is a function (S2), and `a ∈ dom(Σ.C)` by referential integrity (S3). Each lockstep image `shift(a, k)` ... likewise lies in `dom(Σ.C)`." For the link subspace, the labels lie in `dom(L)`, never in `dom(C)` (L14 makes them disjoint). The text later admits it "sidesteps the failed S3 (and S7b/C1b) preconditions ... entirely" and reduces (b) to the bare lockstep equality — but that is precisely *not* ASN-0036's condition (b), which carries a content-store-membership conjunct. The headline claim that the link-subspace decomposition satisfies "ASN-0036's S8 conditions (a) and (b)" is therefore false as stated against the foundation's fixed meaning of (b).

**Required**: State S8★(s_L) as satisfying a *modified* condition (b) — lockstep advance plus label membership in `dom(L)` (not `dom(C)`) — rather than claiming it satisfies ASN-0036's condition (b) verbatim. The substitution `dom(C) → dom(L)` in the inherited condition must be explicit, since it is the whole reason ASN-0036's S8 cannot be applied directly.

### Issue 2: Redundant double-derivation of `subspace(v) = s_C` in the P7a discharge
**ASN-0047, *Extended reachable-state invariants*, Class (b), P7a**: "The K.μ⁺ amendment forces `subspace(v) = s_C` directly at the moment the position is created ... We show the V-position `v` must be content-subspace by an independent chained derivation from J0 + S3★ + L14 — independent verification that no link-subspace V-position can carry a dom(C) target ... The derivation does not rely on the K.μ⁺ amendment".

**Problem**: The passage establishes the same fact (`subspace(v) = s_C`) twice — once "directly" by the K.μ⁺ amendment, then again by an explicitly-labeled "independent chained derivation" that narrates it "does not rely on the K.μ⁺ amendment." This is defensive meta-prose hedging on which premise carries the conclusion; the reader must reconcile two routes to one fact. Per the forward-reference-accretion guidance, this is reviser drift ("two paragraphs say the same thing in different words" plus narration of proof strategy).

**Required**: Keep the single rigorous route (the S3★ + L14 contradiction, which covers any `v` J0 supplies) and delete the meta-commentary about independence and non-reliance on the amendment.

### Issue 3: SubAllocatorAxiom sub-clauses carry deferral inventories rather than content
**ASN-0047, *Allocator hierarchy under documents*, SubAllocatorAxiom.Namespace / .T10aConformance**: "(Inherited from ASN-0093 ContentLinkSubAllocatorExistence; the T4-validity construction for the first emission and its preservation under subsequent `inc(·, 0)` steps are established there.)" and "(Inherited from ASN-0093; the T2-spawn activation, the anchors-as-virtual-roots structure, and the GlobalUniqueness/frontier mechanics governing subsequent emissions are established there.)"

**Problem**: These parentheticals are use-site/where-established inventories that do not advance the clause's meaning — they enumerate what is proved elsewhere. The same content is already recorded in the *Inherited from foundation* table (SubAllocatorAxiom row). This is the flagged pattern "a definition's introduction enumerates downstream consumers / defers to a downstream location," duplicated against the closing table.

**Required**: Reduce each sub-clause to its statement plus a single citation (`per ASN-0093`); drop the embedded enumerations of what ASN-0093 establishes. Let the foundation table carry the inheritance note once.

### Issue 4: K.μ⁻ admissible-shape equivalence reverse direction re-states its own hypothesis as a derivation
**ASN-0047, *K.μ⁻ admissible contraction shape*, reverse direction**: "D-SEQ★ fires from D-CTG★, D-MIN★, S8-depth, S8-fin, and S8a at Σ', drawn from two distinct sources: S8-depth, S8-fin, and S8a at Σ' are preserved from Σ by restriction ... while D-CTG★ and D-MIN★ at Σ' are part of the hypothesis being characterized — they are not preserved by arbitrary restriction ... but are supplied by the candidate-state hypothesis being shown equivalent."

**Problem**: The reverse direction is meant to show that any post-state satisfying the invariants takes the constructive form, yet the load-bearing step (D-SEQ★ at Σ') is obtained by feeding back D-CTG★/D-MIN★ that the paragraph then states are "part of the hypothesis." This is fine logically, but the surrounding prose spends a full paragraph justifying which constituents are "preserved" vs "supplied by the hypothesis" — a justification of proof bookkeeping that does not advance the equivalence. It reads as defensive narration inserted to pre-empt a circularity objection.

**Required**: Either compress to one sentence ("D-SEQ★ at Σ' follows from the candidate's D-CTG★/D-MIN★ (hypothesis) together with S8-depth/S8-fin/S8a (preserved by restriction)") or move the constituent-source bookkeeping out of the proof body.

## OUT_OF_SCOPE

### Topic 1: J4 (Fork) specifies CREATENEWVERSION-level operation semantics
**ASN-0047, *Coupling and isolation*, J4 / Definition (Fork)**: J4 gives a precondition (`d_src ∈ E_doc ∧ V_{s_C}(d_src) ≠ ∅`), a fixed step decomposition, the k = 1 restriction, and ancestry-by-address semantics — i.e., a specification of CREATENEWVERSION, which is on the named-operations exclusion list.

**Why out of scope**: The abstract taxonomy needs the *reordering/extension/contraction modes* and the composition machinery, but the concrete fork operation (its precondition, its k=1 restriction, its ancestry semantics) is a named-operation specification belonging to an operations ASN. The illustration that named operations compose from elementaries is in scope; pinning fork's precondition and dispatch is not.

VERDICT: REVISE
