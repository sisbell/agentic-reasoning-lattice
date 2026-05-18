# Review of ASN-0047

## REVISE

### Issue 1: D-CTG★/D-MIN★ strengthening abandons link-subspace exemption without justification
**ASN-0047, "Amendments to existing transitions" / "Link-withdrawal gap under D-CTG★ / D-MIN★"**: "ASN-0036's D-CTG and D-MIN have link-subspace exemptions for tombstoning; this ASN introduces strengthened forms D-CTG★ and D-MIN★ that apply uniformly across both subspaces"
**Problem**: The strengthening is asserted without explaining why uniform contiguity is preferred over Nelson's explicit tombstoning design (LM 4/9). The cost is significant — the gap section concedes that "withdrawing one interior link requires withdrawing every link allocated after it." The ASN-0036 exemption existed precisely to accommodate Nelson's design. Dropping it imposes a structural constraint that conflicts with the cited design source, and the ASN provides no positive reason for the trade.
**Required**: Either (a) restore the link-subspace exemption to match ASN-0036 and Nelson's design, or (b) supply an explicit positive justification for uniform contiguity that outweighs the lost expressivity. Acknowledging the gap is not the same as justifying the choice.

### Issue 2: S7d implicit weakening for ghost-base versioning
**ASN-0047, ExtendedReachableStateInvariants → Foundation invariants → "S7d (Document allocation discipline)"**: "every K.δ on `IsDocument(e)` that proceeds via Path 1 allocates under the T10a discipline... The k = 1 ghost-base sub-case relaxes the foundation's T10a-conformance clause to a tumbler-layer structural-validity clause"
**Problem**: ASN-0036's S7d states "every document tumbler `d`... is the result of an allocation event under T10a." The ghost-base case explicitly allocates without T10a-conformance for the version step, contradicting S7d as stated. The ASN nonetheless lists S7d as a conjunct of ExtendedReachableStateInvariants. This is an implicit weakening of a foundation invariant performed by relaxation in the proof rather than by amendment of the statement.
**Required**: Either (a) state an explicit S7d★ with the relaxed T10a-conformance clause and substitute it for S7d in ExtendedReachableStateInvariants, or (b) restrict K.δ to disallow ghost-base versioning, or (c) demonstrate that the relaxed S7d is what downstream consumers actually need. Currently the conjunct's meaning shifts silently.

### Issue 3: Anti-bloat in K.δ Path notation and sequentiality footnote
**ASN-0047, "K.δ (Entity creation)" → *Freshness discharge***: extensive paragraphs naming "Path 0", "Path 1", "Path 2", with a "Sequentiality contingency" sub-paragraph announcing that "Path 2's discharge of `e ∉ E` is *contingent* on the single-event sequential semantics this ASN assumes" and that the chain-wide propagation "propagates chain-wide because T10a's T2 spawning requires..."
**Problem**: The Path names elevate three case branches of one precondition obligation into named entities with their own sub-justifications. The "Sequentiality contingency" paragraph then defends Path 2 against a concurrency concern, ending by deferring to Open Questions. This is reviser drift — prose accumulated to defend a design choice rather than to advance the model. The same K.δ section also has the "Per-sub-case additional requirements" list whose content overlaps with the freshness discharge paragraph.
**Required**: Collapse the Path-named freshness discharge to one paragraph that identifies the three branches as cases of the K.δ precondition without naming them; move the sequentiality concern (if retained) into the Open Questions section where it belongs, not into a footnote-style paragraph buried in K.δ's text.

### Issue 4: Anti-bloat in L3 empty-F/G semantics
**ASN-0047, "Link store and extended system state" → L3**: "*Semantics of empty F or G.*" with sub-paragraphs "*One-sided link*", "*Type-only marker*", and nested *Operational consistency with udanax-green* and *Structural compatibility with the link-store invariants* defenses.
**Problem**: The discussion accumulates roughly half a page of prose defending the admissibility of `F = ∅` and `G = ∅`. The "design-uncertain" flag, the udanax-green file-and-line citations (do2.c:111-112, do1.c:195-221, sporgl.c:14-33, orglinks.c:75-134), and the "Structural compatibility" enumeration of which invariants are unaffected — all are meta-prose explaining *why the axiom is admissible*, not what L3 says or how it is used. Multiple paragraphs converge on the same conclusion: "the case is admissible by structural compatibility + operational consistency."
**Required**: Reduce to one short paragraph stating that L3 admits empty F and G with the standard one-sided-link reading from Nelson; defer extension-design discussion (whether to narrow K.λ further) to Open Questions if retained at all.

### Issue 5: S8 extended-state preservation hand-waved via "projection"
**ASN-0047, ExtendedReachableStateInvariants proof, paragraph beginning "S8 in the extended state is established per-subspace."**: "*Content subspace:* by ASN-0036's S8 applied to the projection `M(d')|_{V_{s_C}(d')} : V_{s_C}(d') → dom(C')` (S3★'s content clause is exactly S3 restricted to V_{s_C}(d')..."
**Problem**: ASN-0036's S8 is stated for the full arrangement, not for a per-subspace projection. The ASN asserts the foundation theorem "applies to the projection" but does not show the adaptation. The link-subspace case is treated by exhibiting a trivial length-1 decomposition (correct and shown), but the content-subspace case is dispatched in one clause with no construction. The K.μ⁺_L case in the elementary verification then cites the same hand-wave: "S8 at Σ' by the per-subspace decomposition above (content subspace frame-preserved, link subspace by the trivial length-1 decomposition)."
**Required**: Either (a) show the projection adaptation explicitly — what construction lifts ASN-0036's correspondence-run decomposition to V_{s_C}(d') — or (b) state and prove an extended-state S8★ that operates per-subspace, with the four-component S8 as the corollary at V_{s_L}(d') = ∅.

### Issue 6: K.μ~ link-subspace fixity proof requires reader assembly
**ASN-0047, "Decomposition of K.μ~" → "Link-subspace fixity"**: "Since K.μ⁺ (amended) cannot create link-subspace V-positions and K.μ⁻ leaves no room to remove any (by the bijection count above), `dom_L(M'(d)) = dom_L(M(d))` as sets and `M'(d)|_{dom_L} = M(d)|_{dom_L}` as functions; in particular `M'(d)(v) = ℓ`. CL-UNIQ at Σ' then gives `π(v) = v`."
**Problem**: The "bijection count above" referred to is K.μ~-FIX (`dom(M'(d)) = dom(M(d))`), but the inference chain from there to "K.μ⁻ leaves no room to remove any [link-subspace position]" is not laid out. The full argument requires: bijection preserves cardinality → subspace-preserving bijection preserves per-subspace cardinality → K.μ⁺ amendment plus equal post-K.μ⁻ cardinality forces K.μ⁻'s removal set X ⊆ dom_C → K.μ⁻'s frame on values combined with K.μ⁺'s frame on existing values gives pointwise preservation on dom_L. This is correct but the reader has to assemble each step.
**Required**: Spell out the inference: from bijection and subspace preservation, K.μ⁻ must remove only content-subspace positions; then dom_L is frame-preserved through both K.μ⁻ and K.μ⁺ steps; CL-UNIQ at Σ' then uniquely identifies the V-position mapping to ℓ as v.

### Issue 7: NodeUniqueAllocation as bare freshness axiom
**ASN-0047, "Worked example: entity hierarchy by K.δ" preamble / NodeUniqueAllocation definition**: "Every K.δ node-allocation event... produces an address fresh to the entity set: for any such e emitted at state Σ, `e ∉ Σ.E`."
**Problem**: This is precisely K.δ's `e ∉ E` precondition restated as an axiom for the node case. The axiom delegates to an unspecified protocol ("Nelson's hierarchical baptism / Gregory's single global granfilade") but provides no formalisation. Treating "the precondition is satisfied" as an axiom is circular for proof purposes — Path 0 of the freshness discharge cites NodeUniqueAllocation, but NodeUniqueAllocation is just the precondition. The protocol's actual mechanism (global allocation registry, query-and-increment, etc.) is what supplies freshness; an axiom that names "the protocol works" without naming what the protocol does adds no rigor.
**Required**: Either (a) describe the protocol minimally (a single uniqueness condition on the node-allocation registry that the protocol must satisfy), or (b) acknowledge that node allocation is outside this ASN's discharge layer and defer Path 0 to a node-allocation ASN, removing the "Path 0" label and discharge claim from this ASN's S4 proof. The current form gives the appearance of a proof step that on inspection is empty.

### Issue 8: K.δ Path 2 sequentiality assumption smuggled via footnote
**ASN-0047, "K.δ (Entity creation)" → *Freshness discharge* → *Sequentiality contingency***: "Path 2's discharge of `e ∉ E` is *contingent* on the single-event sequential semantics this ASN assumes — the inspection of E and the commit of `E' = E ∪ {e}` are an atomic, uninterruptible pair."
**Problem**: The ASN never explicitly assumes sequential semantics at the model level. The transition-system model `Σ → Σ'` does not specify concurrency discipline. A material assumption — "operations are sequentially executed and atomically committed" — is introduced via a footnote-style paragraph inside one precondition's discharge analysis. The S4 conjunct of ExtendedReachableStateInvariants then carries this assumption silently for every K.δ Path 2 transition. Other transitions (K.μ⁻ admissibility, K.μ~ decomposition) implicitly assume the same.
**Required**: State the sequential-semantics assumption as a model-level axiom at the head of the ASN where Σ → Σ' is introduced, or extend the transition-system model to make atomicity explicit. The footnote placement makes the assumption easy to miss when later sections cite ExtendedReachableStateInvariants.

### Issue 9: D-CTG-depth / D-SEQ★ chain — the inner-positions-fixed step requires a small case-split note
**ASN-0047, "Amendments to existing transitions" → D-SEQ★ derivation → Step 1**: "Suppose for contradiction that some v ∈ V_S(d) has v_j ≥ 2 at the *minimal* inner position j with `2 ≤ j ≤ m - 1`."
**Problem**: The derivation handles m = 2 by remarking "when m = 2 there are no inner positions and the claim is vacuous." But this note appears in the parenthetical statement of Step 1; the construction of u_M then proceeds without re-noting the m = 2 base case. For m = 3 (only one inner position j = 2), the u_M construction places M at position j + 1 = 3, which is the terminal position. This is correct but worth stating explicitly: the construction varies the terminal when the inner position is the rightmost-but-one.
**Required**: Add one sentence clarifying that for m = 2, the inner-positions-fixed claim is vacuous, and the V_S(d) ⊆ {[S, 1, ..., 1, k]} fact is immediate; for m ≥ 3, the u_M construction's placement of M may coincide with the terminal when j = m − 1.

## OUT_OF_SCOPE

### Topic 1: Link tombstoning / withdrawal mechanism
**Why out of scope**: The link-withdrawal gap induced by D-CTG★/D-MIN★ requires a separate mechanism (status flag, tombstone, retraction link); the ASN correctly defers this to a future ASN.

### Topic 2: Concurrency discipline for Path 2 freshness
**Why out of scope**: Multi-protocol entity allocation under concurrent execution is appropriately deferred to a future operations ASN; the current ASN's sequential semantics is a model-level choice for the elementary-transition layer.

### Topic 3: Operational details of node baptism / granfilade
**Why out of scope**: The actual node-allocation protocol is properly delegated to a node-allocation ASN; the present ASN can either axiomatise freshness (improved per Issue 7) or specify only what the protocol must guarantee.

### Topic 4: Version-management ASN content
**Why out of scope**: The "richer version contract — including arrangement invariants, provenance flow, and lineage acyclicity" is correctly deferred; ghost-base versioning at the elementary level is sufficient for this ASN's scope.

### Topic 5: Account-level depth-1 extension
**Why out of scope**: The Open Questions item correctly defers this to a future extension; ASN-0047's restriction to document versioning matches the consultation evidence.

### Topic 6: J4 fork operational shape (specific V-position bijection between source and new document)
**Why out of scope**: The ASN's "operation-specific" framing leaves the V-position correspondence for a future operations ASN, which is appropriate.

VERDICT: REVISE
