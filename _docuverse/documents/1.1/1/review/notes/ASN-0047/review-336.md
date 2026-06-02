# Review of ASN-0047

## REVISE

### Issue 1: S8★ for K.μ~ is deferred to a section that does not establish it
**ASN-0047, *Decomposition of K.μ~* (clause (i) scope note) and *Extended reachable-state invariants* (K.μ~ shape-invariant discharge)**: Both say S8★ is established "by the K.μ⁻ + K.μ⁺ decomposition (*Decomposition of K.μ~*)." The clause-(i) scope paragraph: "S8★ (per-subspace span decomposition) by the K.μ⁻ + K.μ⁺ decomposition." The Class (a) prose: "S8★ is established at Σ' by the K.μ⁻ + K.μ⁺ decomposition (*Decomposition of K.μ~*)."

**Problem**: The *Decomposition of K.μ~* section proves S3★ explicitly (Step (B), result K.μ~-S3★) but contains no S8★ argument. Two paragraphs in different sections both point a reader to that section for S8★, and the section does not carry the result. The actual substantiation lives in the inherited K.μ⁺/K.μ⁻ matrix columns (s_C via ASN-0036's S8, s_L via the length-1 decomposition). This is precisely the "multiple paragraphs defer to the same downstream location" pattern, compounded by the location not substantiating the cited result.

**Required**: Point the S8★ deferral at the inherited matrix columns (where the argument actually is), or add an explicit S8★(s_C)/S8★(s_L) step to the decomposition section. As written, following either pointer leaves S8★(Σ') unestablished for K.μ~.

### Issue 2: Meta-labeling and "needs no proof" prose in the K.μ~ realisation steps
**ASN-0047, *Decomposition of K.μ~*, Steps (A)–(B)**: "We record this as the **full-clearance realisation claim** — *the full-clearance form realises every admissible π*"; Step (A) "discharging the produced-π half of the full-clearance realisation claim"; Step (B) "This step discharges that realisability half." Step (A) opens: "The only substantive claim is that the π produced ... is subspace-preserving and link-subspace fixing — hence admissible; that admissible π are subspace-preserving (iv) and link-fixing (v) is true by hypothesis and needs no proof."

**Problem**: The "claim / produced-π half / realisability half" naming is navigational meta-prose layered over what is just a two-direction argument; the "is true by hypothesis and needs no proof" sentence is a defensive justification of what is *not* being proved. A reader must skip past the half-labeling and the disclaimer to reach the actual content (the subspace/link-fixity case split). This is essay content in a proof slot, the kind of accretion the anti-bloat classifier targets.

**Required**: State the two directions as the case split they are (content positions go to K.μ⁺'s write set; link positions are LRP-fixed) and drop the "claim/half" scaffolding and the "needs no proof" disclaimer.

### Issue 3: Use-site inventory prose at ChildSpawnFreshness and FrontierEquivalence
**ASN-0047, *Elementary transitions*, ChildSpawnFreshness intro**: "This is the child-spawn analogue of FrontierEquivalence — it discharges, at the same standard, the freshness read the K.δ k = 1 and k = 2 sub-cases rely on."

**Problem**: This sentence inventories downstream consumers and asserts an equivalence-of-standard rather than advancing the lemma's statement; the lemma's content (the biconditional and its proof) stands on its own. It is a use-site enumeration in a definition slot.

**Required**: Remove the consumer inventory; let the K.δ sub-cases cite ChildSpawnFreshness at their use sites (they already do). The lemma should state what it proves, not which call sites depend on it.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link/content withdrawal
The ASN's K.μ⁻ models only suffix removal; interior withdrawal with compaction (DELETEVSPAN-style renumbering) is correctly deferred to a future ASN (also raised as an open question). This is named-operation territory, out of scope here.

### Topic 2: Concurrency / serialization of allocation under a shared home document
Raised in the open questions; concurrency is explicitly out of scope.

VERDICT: REVISE
