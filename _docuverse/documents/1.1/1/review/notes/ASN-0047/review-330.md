# Review of ASN-0047

This is a large, carefully-constructed transition model. I checked the elementary transitions, the K.μ~ decomposition, the coupling derivations (J0/J1★/J1'★), the D-SEQ★ derivation (both `m = 2` and `m ≥ 3` cases), and the reachable-state induction. The correctness machinery is largely sound: the D-SEQ★ infinite-family contradiction is solid, the K.μ⁻ constructive/post-state equivalence holds in both directions, the orphan-link asymmetry is intentional and consistent, and the foundation citations (ASN-0034/0036/0043/0045/0093) are all to permitted foundation ASNs. I did not find a correctness defect.

The findings below are presentational, targeting the `review-mode.anti-bloat` patterns the note asks me to surface. They are REVISE items under "prose clarity," not structural-split requests.

## REVISE

### Issue 1: Anchor construction restated in three locations
**ASN-0047, *Allocator hierarchy under documents* / SubAllocatorBundle / FirstEmission**: The same anchor construction appears three times:
- *Allocator hierarchy*: "`b_C(d) = inc(d, 2) = [d.0.1]` (TA5(d) with k = 2), and `b_L(d) = inc(b_C(d), 0) = inc([d.0.1], 0) = [d.0.2]` (TA5(c))."
- *SubAllocatorBundle*: "anchors `b_C(d) = inc(d, 2)`, `b_L(d) = inc(b_C(d), 0)`, per ASN-0093's FirstEmission."
- Inherited FirstEmission (ASN-0093) already states: "anchor construction: `b_C(d) = inc(d, 2)` and `b_L(d) = inc(b_C(d), 0)`."

**Problem**: Two paragraphs in the same document say the same thing in different words (the anti-bloat "two paragraphs ... say the same thing" pattern), and a third copy lives in the inherited foundation claim. A reader tracing the anchors works through redundant restatements.
**Required**: State the construction once (the *Allocator hierarchy* section, with the TA5 citations), and have SubAllocatorBundle reference it by name rather than re-deriving it.

### Issue 2: Roadmap/meta sentences in proof slots
**ASN-0047, SSGU and ParentAllocatorDispatch**:
- SSGU opens: "This packages, once, the standard discharge used wherever an `inc`-produced address must be traced to its unique producing allocation event."
- ParentAllocatorDispatch opens: "T10a.6 supplies *uniqueness* of the owning allocator; the per-level analysis below supplies its *identification*."

**Problem**: These sentences describe the *role* of the surrounding argument rather than advancing it — meta-commentary on what the lemma is for and how the proof is organized. They are the kind of essay content in structural slots the note flags.
**Required**: Delete the role-description openers; begin each lemma with its statement and proof.

### Issue 3: Repeated deferrals to SubAllocatorFreshness
**ASN-0047, K.α / K.λ / worked examples**: K.α defers freshness with "is SubAllocFresh at x = C (Lemma SubAllocatorFreshness, *Allocator hierarchy under documents*, below)"; K.λ defers with "is SubAllocFresh at x = L (Lemma SubAllocatorFreshness, *Allocator hierarchy under documents*)"; the link-allocation and content-replacement worked examples re-cite the same lemma at multiple steps.

**Problem**: Multiple paragraphs in different sections defer to the same downstream location — the anti-bloat deferral pattern. The forward pointer is repeated with its locator ("*Allocator hierarchy under documents*, below") at each site.
**Required**: A single locator at first use; subsequent sites cite "SubAllocFresh" by name without re-pointing to the section.

### Issue 4: K.δ case (i) precondition restates the axiom that discharges it
**ASN-0047, K.δ case (i)**: "Required: `T4-valid(e) ∧ Node(e) ∧ e ∉ E ∧ n₀ ≼ e`. Both the freshness conjunct `e ∉ E` and the bootstrap-lineage conjunct `n₀ ≼ e` are discharged by NodeBaptism (a) and (b) respectively."

**Problem**: The precondition lists `e ∉ E` and `n₀ ≼ e`, which are verbatim NodeBaptism (a) and (b), then immediately notes they are discharged by NodeBaptism (a) and (b). For a case with no operand and no T10a discharge, the precondition *is* the axiom; restating both sides reads as filler.
**Required**: State the case-(i) precondition as "the conjuncts supplied directly by NodeBaptism (a)/(b)" without duplicating the conjuncts inline.

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement contraction with renumbering
The ASN's K.μ⁻ contracts each subspace by suffix removal only; interior link withdrawal with V-position compaction is correctly deferred (open question). This is new operational territory, not a defect in the present K.μ⁻.

### Topic 2: Link provenance and transitive-transclusion provenance guarantees
The provenance relation R grounds only content (P7), and link/transitive-sharing provenance is left to the open questions. This is future scope, not an error here.

VERDICT: REVISE
