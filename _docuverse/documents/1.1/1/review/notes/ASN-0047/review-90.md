# Review of ASN-0047

## REVISE

### Issue 1: Path 2 freshness discharge undermines S4's universal claim
**ASN-0047, Foundation invariants block (S4 paragraph)**: "*S4 (Origin-based identity)* — distinct allocation events produce distinct addresses. ... *Path 2 (Direct inspection at the allocation event)*. Case (ii) ghost operands (`¬InEntityAllocatorDomain(t)`) — the K.δ precondition `e ∉ E` is verified against E directly at the allocation event"

**Problem**: The ExtendedReachableStateInvariants proof claims S4 holds for every reachable state. For K.δ ghost-base chains (Path 2), the proof relies on E-inspection at the allocation event. But the ASN's own Open Question explicitly states this is sound only "beyond the single-event sequential semantics this ASN assumes — what additional constraint (per-allocator serialization, transactional commit, or a global pre-commit uniqueness check) must hold". A proof that closes its obligations under an unstated and acknowledged-as-insufficient discipline is not closed.

**Required**: Either (a) state explicitly that single-event sequential semantics is a meta-axiom (and remove the discipline question from Open Questions, since it's then resolved by axiom), or (b) acknowledge in the S4 derivation that Path 2's freshness is contingent on a discipline deferred to a future ASN, and qualify ExtendedReachableStateInvariants accordingly.

### Issue 2: L1c chain construction silently depends on s_L = s_C + 1
**ASN-0047, Foundation invariants block (L1c paragraph)**: "The chain `t₀ = d, t₁ = inc(d, 2) = b_C(d), t₂ = inc(t₁, 0) = b_L(d), t₃ = inc(t₂, 1) = ℓ` is T10a-conforming"

**Problem**: `inc([d.0.s_C], 0)` advances the last component by 1, producing `[d.0.s_C + 1]`. This equals `b_L(d) = [d.0.s_L]` only because SubspaceConventionAxiom fixes `s_C = 1, s_L = 2`, making `s_L = s_C + 1` a numerical coincidence rather than a structural fact. If the convention were `s_C = 1, s_L = 3`, the chain would not connect `b_C(d)` to `b_L(d)` via `inc(·, 0)`. The same construction appears at "Allocator hierarchy under documents" claiming structural producibility.

**Required**: Either (a) make the `s_L = s_C + 1` dependency explicit (and discuss whether it's load-bearing), or (b) construct the chain to `b_L(d)` independently of `b_C(d)` — e.g., via `inc(d, 2)` followed by a fresh route to s_L. As written, the chain disguises a convention-dependent step as a tumbler-algebra theorem.

### Issue 3: SubAllocatorAxiom "namespace property" attribution conflates two distinct freshness sources
**ASN-0047, Foundation invariants block (S4 paragraph, first-link case)**: "the namespace property supplied by SubAllocatorAxiom at the activation site (every fresh emission of an activated content sub-allocator lies outside dom(C) under the cross-allocator disjointness chain) discharges a₃ ∉ dom(C₂) directly"

**Problem**: SubAllocatorAxiom has three sub-clauses: Subspace, FirstEmission, Namespace. FirstEmission commits only the *first* emission to `a ∉ dom(C) ∪ dom(L)`. Subsequent emissions get freshness from T10a's GlobalUniqueness on inc chains. The parenthetical phrase "every fresh emission of an activated content sub-allocator lies outside dom(C)" attributes to SubAllocatorAxiom a claim it does not make. This same conflation appears in the L1c first-link discharge ("supplies `ℓ ∉ dom(L)` directly") and the worked example Step 2.

**Required**: Distinguish the two routes explicitly in every freshness discharge. The first emission is closed by SubAllocatorAxiom.FirstEmission; subsequent emissions by GlobalUniqueness on the inc(·, 0) chain. The phrase "namespace property ... every fresh emission" is wrong as a characterization of SubAllocatorAxiom and should be removed.

### Issue 4: S8 for link subspace is claimed via D-SEQ★ but D-SEQ★ does not give correspondence runs
**ASN-0047, Class (a) per-state invariants paragraph**: "S8 in the extended state is established per-subspace: the content-subspace finite span by ASN-0036's S8 on the projection ... the link-subspace finite span by D-SEQ★(s_L)"

**Problem**: ASN-0036's S8 (SpanDecomposition) establishes the existence of correspondence runs `(v, a, n)` satisfying `M(d)(shift(v, k)) = shift(a, k)` for `0 ≤ k < n`. D-SEQ★ gives the per-subspace structural shape `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` — this is *not* a correspondence-run decomposition. Citing D-SEQ★ to discharge S8 for the link subspace skips the actual decomposition argument. The K.λ + K.μ⁺_L pattern produces inc-chain links at shift-related V-positions, so S8 should hold non-trivially, but this needs explicit demonstration.

**Required**: Either (a) prove that the link subspace under any reachable arrangement admits S8-style correspondence-run decomposition (a positive argument), or (b) acknowledge that S8 for the link subspace is not established in this ASN and explicitly state which weaker property D-SEQ★ provides.

### Issue 5: Empty F/G "type-only marker" admitted beyond consultation evidence
**ASN-0047, L3 paragraph (Semantics of empty F or G)**: "*Type-only marker (both F and G empty).* The link references no source or target span, only a type designation. ... Nelson did not explicitly address this case in the design; the udanax-green implementation accepts it without runtime error"

**Problem**: This is a substantive design extension beyond the consultation evidence. The ASN admits the case on the grounds of structural well-formedness and runtime-acceptance in udanax-green. But neither is a design endorsement — udanax-green's lack of a runtime guard could equally indicate an implementation oversight. The ASN's "follow-link returns request-failed by construction" reasoning is a property of one specific operation set; it does not validate the design.

**Required**: Either (a) restrict L3 to require `F ∪ G ≠ ∅` (admitting one-sided links per Nelson but excluding type-only markers), with documented rationale; or (b) state explicitly that the type-only marker is a design extension beyond consultation evidence and justify it on independent grounds (not "structurally admissible" — that's begging the question).

### Issue 6: Forward reference to undefined `endpoints(·)` accessor
**ASN-0047, L3 paragraph**: "Coverage of empty endsets in L4's `endpoints(·)`-style consumers and L8's `same_type` is by their natural inductive form"

**Problem**: ASN-0043's L4 (EndsetGenerality) does not define an `endpoints(·)` accessor. The phrase "L4's `endpoints(·)`-style consumers" references a hypothetical downstream form that does not exist. This is a forward reference to imaginary infrastructure.

**Required**: Either remove the reference to `endpoints(·)`, or replace it with the actual L4 content the ASN intends to consume.

### Issue 7: Structural sufficiency boundary is informally bounded
**ASN-0047, Elementary transitions section (closing paragraphs)**: "structurally sufficient for the modification kinds catalogued in this ASN ... The sufficiency claim above is bounded — it is structural, not exhaustive over the admissible-state-difference lattice."

**Problem**: The "modification kinds catalogued in this ASN" is left implicit. The link-withdrawal gap is named as one specific shortfall. But the boundary of the sufficiency claim is otherwise undefined: are there other categories of state change the elementary set cannot express? The ASN should not state a sufficiency claim and then disclaim it without enumerating what's covered and what isn't.

**Required**: Either (a) define precisely what "design enumeration" the elementary set covers (e.g., by enumerating the admissible state-change modes per component), or (b) enumerate every known gap rather than naming just the link-withdrawal one.

### Issue 8: K.α attributed to ASN-0036 in Properties Introduced table
**ASN-0047, Properties Introduced table (Local extensions block, K.α amendment row)**: "K.α amendment | Content-subspace restriction ... | Amendment to ASN-0036's K.α adding subspace constraint"

**Problem**: K.α is fully defined in this ASN's "Elementary transitions" section. ASN-0036's claim statements do not include K.α as a defined operation. Calling this an "amendment to ASN-0036's K.α" presumes K.α exists in ASN-0036, which is at best implicit through the C : T ⇀ Val component.

**Required**: Either (a) state in the table that K.α is introduced in this ASN (move it to the "New properties" block), with the amendment row reflecting the subsequent strengthening within this ASN; or (b) verify that ASN-0036 does define K.α (in prose not extracted into claim statements) and cite the location.

### Issue 9: Redundant deferred-to-version-contract notes
**ASN-0047, multiple sites**: The K.δ k=1 ghost-base case carries deferral notes in (a) the K.δ definition itself ("the richer version contract ... is deferred to a subsequent version-management ASN"), (b) the Foundation invariants block for S7d ("reconciliation with the literal foundation form is part of the deferred version contract"), and (c) the Open Questions section.

**Problem**: Three sites in the same document defer to the same downstream location. The K.δ definition's "Ghost-base versioning" paragraph already does the work; subsequent deferral notes add nothing.

**Required**: Consolidate to a single deferral statement at the K.δ definition site and remove the repeated notes in the Foundation invariants paragraph and the prose lead-in to the Open Question.

### Issue 10: "Frame extension (existing transitions)" paragraph duplicates per-transition frame content
**ASN-0047, Amendments to existing transitions section**: "In the extended state Σ = (C, L, E, M, R), each of K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.ρ extends its original frame with `L' = L`"

**Problem**: Each elementary transition already states its full frame in the extended state. The framing paragraph in *Amendments* repeats the L-in-frame fact. This is meta-prose explaining what the per-transition definitions already say.

**Required**: Remove the paragraph, or replace with a single-sentence note ("Each transition's frame holds L' = L unless explicitly noted") if needed for navigation.

## OUT_OF_SCOPE

### Topic 1: Version management discipline (k = 1 chain semantics, version DAG, ancestry indication)
**Why out of scope**: Version management has its own deferred ASN per the Open Questions; the ghost-base treatment here suffices to establish that K.δ admits the case without binding the version contract.

### Topic 2: Link-withdrawal mechanism (tombstones, status flags, retraction links)
**Why out of scope**: Acknowledged in the *Link-withdrawal gap* paragraph and recorded as an open question — this is new infrastructure deferred to a future ASN.

### Topic 3: Concurrency discipline for K.δ Path 2 freshness
**Why out of scope**: The Open Question records this. (Note: this overlaps with Issue 1 — the issue is that the *proof* claims completeness despite this open question, not that the open question itself is invalid.)

VERDICT: REVISE
