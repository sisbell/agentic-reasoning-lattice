# Review of ASN-0069

## REVISE

### Issue 1: V12(d) — defensive prose explaining why lemmas are needed
**ASN-0069, V12(d) derivation**: "V4 alone supplies equality on the restriction ... but leaves `dom(M'(d_new)) \ V_{s_C}(d_op)` unconstrained; equivalently, V4 alone gives only the unrestricted containment ... V4b is needed to close the reverse direction ..." and "P4★ ... is — unlike the per-state invariants this ASN otherwise cites — a *composite-boundary* property ... composites are sequenced boundary-to-boundary under ValidComposite★, so the start state of any composite is itself a boundary."

**Problem**: Both passages explain *why a cited lemma is needed / applicable* rather than advancing the derivation. The V4-vs-V4b discussion narrates the division of labor between two of the ASN's own lemmas; the P4★ passage is an essay justifying that the start state is a composite boundary. This is the "explains why the lemma is needed rather than what it says" accretion pattern.

**Required**: Reduce to the operative chain — `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)})` (V4 + V4b), `(a, d_op) ∈ Contains_C(Σ) ⊆ R` (P4★ at boundary Σ), carried forward by P2. Drop the role-narration.

### Issue 2: V8c — tautological derivation at length
**ASN-0069, V8c derivation**: "Conjunct (i) is invariant under swap because set intersection is commutative ... For conjunct (ii) ... symmetry of equality (a property of `=`, applied to the V8-supplied equality) gives the equivalent ..."

**Problem**: The lemma asserts a correspondence set is symmetric under swapping its two documents, and the proof spends a paragraph deriving that `∩` is commutative and `=` is symmetric. This belabors a tautology in a structural slot.

**Required**: State V8c as a one-line observation ("the corresponding-position set is defined by `∩` and `=`, both symmetric, so it is swap-invariant") or fold it into V8.

### Issue 3: V8b — derivation is tautological; "state-relative" not substantiated
**ASN-0069, V8b**: "(i) *Set bound.* `Π_g ⊆ F` at every reachable `Σ_g` ... since `F` is fixed ... and `Π_g` is its intersection with `Corr_g`."

**Problem**: `Π_g := F ∩ Corr_g ⊆ F` is true by the definition of `Π_g`; the "derivation" restates the definition. The lemma's title ("correspondence is state-relative") promises that the inherited correspondence genuinely varies (shrinks) across states, but nothing is proved to leave `Π_g` — only that it cannot exceed `F`. As written the lemma carries no content beyond V8's initial coverage.

**Required**: Either drop V8b, or make the claim non-trivial (e.g., monotone non-increase `Σ_g →* Σ_{g'} ⟹ Π_{g'} ⊆ Π_g`) and prove it — noting that any actual shrinkage mechanism (edit/delete) is out of scope, in which case the bound should be stated as a one-liner without the "state-relative" framing.

### Issue 4: Worked example — duplicated K.δ-alone walkthrough
**ASN-0069, "Empty source (V7)" and "Link-only source (V7 ...)" vignettes**

**Problem**: The two empty-arrangement vignettes traverse the same K.δ-alone composite (same V1/V2/V6/V9-vacuous/V12 reasoning), with the second adding only the CL-OWN link-preservation angle. Most of the second vignette restates the first in different words.

**Required**: Collapse to one empty-source vignette, appending a single sentence noting that a non-empty *link* subspace on the source is preserved by V5 and contributes nothing to the fork (the branching is on `V_{s_C}` emptiness alone).

### Issue 5: Dependency Audit — use-site inventory
**ASN-0069, Dependency Audit**: "entity allocation and frontier advancement run entirely through ASN-0047's K.δ, Allocator hierarchy, SubAllocatorBundle, SequentialTransitionAxiom, ChildSpawnFreshness, FrontierEquivalence, and ActivatedEmission, over ASN-0034's T10a family (T10a, T10a.4, T10a.6, T10a.7) ..."

**Problem**: The enumeration of every consuming mechanism is a use-site inventory. The audit's load-bearing conclusion is only "ASN-0040 has no use site; flag for removal"; the catalog of what *is* used does not advance that conclusion.

**Required**: Keep the ASN-0040 removal recommendation and the single re-derivation note; drop the mechanism catalog.

## OUT_OF_SCOPE

### Topic 1: Link discoverability apparatus (V6a parts ii, iii)
**Why out of scope**: Scope excludes link semantics. V6a introduces `coverage`, `project`, and `discoverable_from` as local definitions and proves projection-invariance across the fork. This is link-discoverability semantics, not a fork guarantee. The only fork-specific obligation here is V6a(i) (link store unchanged across the composite), which follows from the constituent frame clauses; parts (ii)/(iii) are corollaries of source isolation (V5) + link immutability (L12) and belong in a dedicated link-operations or link-discoverability ASN.

### Topic 2: Transitivity of the prefix order
**Why out of scope**: V11a re-derives transitivity of `≼` from the Prefix definition because the ASN-0034 Prefix contract does not list transitivity as a postcondition. This is a foundation property; it should be promoted to ASN-0034's Prefix (or a tumbler-algebra lemma) and then cited, rather than re-proved inside an operation ASN. This is a gap in the foundation, not an error in ASN-0069.

VERDICT: REVISE
