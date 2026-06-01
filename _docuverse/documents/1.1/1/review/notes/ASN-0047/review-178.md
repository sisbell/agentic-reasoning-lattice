# Review of ASN-0047

## REVISE

### Issue 1: Foundation typing override asserted but not demonstrated to transfer

**ASN-0047, *The state model*, Typing note (M total — overrides foundation)**: "This ASN deliberately *overrides* that typing: here M is *total* on T... This single identity translates every inherited foundation precondition and effect."

**Problem**: ASN-0093 (a foundation) types `M(d) : T ⇀ T` as *partial*, with `dom(M)` carrying the allocated-document role. ASN-0047 changes this to total and reroutes the document-set role to `E_doc` under `d ∈ dom(M) ⟺ d ∈ E_doc`. The claim that this "single identity translates every inherited foundation precondition and effect" is a blanket assertion, not a derivation. Foundation results phrased over `dom(M)` (ASN-0093's M1 monotonicity, the K.α/K.λ binding preconditions, SubAllocatorAxiom's activation tied to "the event placing d into dom(M)") each acquire a translated meaning, and the soundness of that translation is exactly the kind of derived guarantee the standards require to be shown, not stated. A reader cannot verify that no foundation lemma silently depends on M's partiality (e.g., `dom(M)` finiteness, or the distinction between "d unallocated" and "d allocated with empty arrangement").

**Required**: Either (a) enumerate the inherited foundation results phrased over `dom(M)` and show each survives the `dom(M) ⟺ E_doc` substitution, or (b) state explicitly which foundation results are *not* used and confine the override's transfer claim to the ones that are. The blanket "translates everything" is a one-sentence claim standing in for a multi-result transfer argument.

### Issue 2: Logical direction of the `e ∉ E` discharge is backwards / circular

**ASN-0047, *Elementary transitions* (K.δ) and *K.δ case (ii) discharge***: "the freshness conjunct `e ∉ E` is discharged per sub-case by the discharge route detailed in §K.δ case (ii)... GlobalUniqueness (ASN-0034) on the parent allocator's tracked domain... then delivers `e ∉ E`."

**Problem**: `e ∉ E` appears simultaneously as a case-level "where-clause conjunct" (a precondition) and as something "discharged" by GlobalUniqueness (a conclusion). These are incompatible epistemic statuses. For k=2, GlobalUniqueness gives only that *distinct* allocation events produce distinct addresses — it does not by itself give `e ∉ E` without the additional premise that the producing event of `e = inc(t,2)` has *not already fired*. That "not yet fired" premise is precisely what the caller-checked `e ∉ E` (equivalently the per-`(t,2)` at-most-once guard) supplies. So the actual primitive is the caller-checked freshness, and the allocator-discipline properties (per-`(t,k')` uniqueness, frontier status) are *enforced by* it, not the *source* of it. As written, the apparatus reads as if cross-event distinctness produces freshness, which is circular: the at-most-once property the discharge leans on is itself maintained only because `e ∉ E` is checked. For k=0 the FrontierEquivalence equivalence is fine (it relates two checkable forms), but the k=1/k=2 prose conflates the two directions.

**Required**: State, per sub-case, which conjunct is the caller-checked precondition (the operational guard, e.g., `inc(t,0) ∉ E` at k=0; `e ∉ E` at k=1/k=2) and which properties are *consequences* of always applying that guard plus `inc` determinism. Remove the framing that GlobalUniqueness "delivers `e ∉ E`"; GlobalUniqueness establishes invariant *preservation* (distinct events stay distinct), not the per-firing precondition.

### Issue 3: SubAllocatorAxiom prose explains clause provenance instead of advancing the axiom

**ASN-0047, *Allocator hierarchy under documents* (SubAllocatorAxiom)**: "Four of the five sub-clauses (Subspace, FirstEmission, Namespace, T10aConformance) are inherited from ASN-0093 without modification. The fifth, Disjointness, is *not* inherited verbatim — it is discharged here as a **local lemma**, because its conclusion is stated over ASN-0047's own anchor constructs... and its proof leans on the CrossDocDisjoint lemma (below) and T7..."

**Problem**: This paragraph is meta-prose about *why* one clause is a local lemma rather than inherited — provenance bookkeeping, not content. It does not advance what the axiom asserts; the precise reader must skip it to reach the operative clauses. This is the "new prose around an axiom explains why it is needed/sourced rather than what it says" pattern the forward-reference note directs me to flag, and it compounds with similar provenance prose elsewhere (the per-clause "(per ASN-0093)" tags already carry the inheritance information).

**Required**: State the five clauses directly. If Disjointness is locally proved, label it "(lemma, proof below)" inline and delete the paragraph explaining the inherited-vs-local distinction.

### Issue 4: K.δ k=0 discharge is restated near-verbatim across three sections

**ASN-0047**: the k=0 sibling discharge (FrontierEquivalence + T10a.6 dispatch + K.δ-ID identities) appears in (a) *Elementary transitions* K.δ case (ii) k=0, (b) *K.δ case (ii) discharge and parent-allocator activation* (first bullet), and (c) *Worked example: entity hierarchy* Step 4.

**Problem**: Sections (a) and (b) say the same thing in different words — both establish `inc(t,0) ∉ E` via FrontierEquivalence and route the owning allocator via ParentAllocatorDispatch/T10a.6. This is the "a paragraph looks like a prior finding's content relocated rather than removed" / "two paragraphs say the same thing" pattern. The worked example (c) is a legitimate concrete instance, but the two abstract restatements (a)/(b) are redundant and risk drift between distant copies.

**Required**: Consolidate the abstract k=0 discharge into one location and have the other reference it by name, rather than re-deriving FrontierEquivalence + dispatch in both the elementary catalogue and the dedicated discharge section.

### Issue 5: Presentation-justification prose in the K.μ~ precondition argument

**ASN-0047, *Decomposition of K.μ~*, Necessity and sufficiency of the precondition**: "The two directions enter the argument independently and are kept separate here so the reader sees what each consumes."

**Problem**: This sentence justifies the *presentation* (why the two directions are kept separate) rather than advancing the proof — the "prose justifies document ordering / presentation" pattern. The necessity and sufficiency arguments stand on their own; the reader does not need a meta-statement about why they are separated.

**Required**: Delete the justification sentence; let the two labeled sub-arguments (Necessity, Sufficiency) speak for themselves.

## OUT_OF_SCOPE

### Topic 1: Liveness / freshness availability
The ASN repeatedly *checks* `e ∉ E`, `a ∉ dom(C) ∪ dom(L)`, etc., but whether a fresh address is always *available* (no exhaustion within a document's sub-allocator) is a separate guarantee. It is correctly deferred (Open Questions already lists "Must the system guarantee that a fresh link address is always available... or can link allocation fail due to address space exhaustion?"). Not an error here.

**Why out of scope**: Address-space availability is a property of the allocator substrate / T0 unboundedness, not of the transition taxonomy this ASN defines.

VERDICT: REVISE
