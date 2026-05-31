# Review of ASN-0047

This note carries the `review-mode.anti-bloat` classifier. My findings concentrate on forward-reference accretion and repeated meta-prose, plus one prose/correctness imprecision. I have deliberately avoided the previously-declined "split the ASN" findings — these are about specific prose to trim, not structural reorganization.

## REVISE

### Issue 1: FrontierEquivalence's three premises are fully restated in four separate sections

**ASN-0047, FrontierEquivalence lemma; K.δ case (ii) k=0; "K.δ case (ii) discharge" section; Worked example Step 4; Properties table**: The "three load-bearing premises" — (i) T10a chain-advancement uniqueness at `(t,0)`, (ii) P1 E-monotonicity, (iii) T10a GlobalUniqueness via T10a.6 — are stated in full in the lemma, then re-enumerated in the K.δ k=0 *Rationale*/*Freshness discharge*, again in the dedicated "K.δ case (ii) discharge and parent-allocator activation" k=0 bullet, and a fourth time in the entity-hierarchy worked example ("(i)… (ii)… (iii)…"), with a fifth condensed restatement in the Properties Introduced table.

**Problem**: This is the accretion pattern the classifier names ("two paragraphs in different sections say the same thing"). The lemma already proves the biconditional; downstream sites need only cite it by name. Each restatement forces the reader to re-verify that the premises match.

**Required**: State the three premises once in the lemma. At the K.δ discharge sites and the worked example, cite "FrontierEquivalence (forward direction)" without re-enumerating premises.

### Issue 2: Defensive justification accretion around the derived `(t,0)`-uniqueness handle

**ASN-0047, FrontierEquivalence premise (i); K.δ k=0 gloss; Properties table FrontierEquivalence row**: "T10a's *direct* per-`(t, k')` uniqueness axiom is stated for child-spawning `k' ∈ {1, 2}` only and does not cover the `k = 0` sibling-increment regime"; "T10a.7 (EnumerationInjectivity) plays only the framing role of identifying chain enumeration structure, not the determinism source."

**Problem**: This disclaimer — explaining *why* a derived form is needed and *which* axiom is not load-bearing — is repeated verbatim in substance at the lemma, the K.δ gloss, and the Properties table. It explains the provenance of a named handle rather than advancing any claim. New prose that explains why the construction is needed rather than what it establishes is exactly the flagged pattern.

**Required**: Keep the determinism-source clarification once at the lemma. Remove the restatements in the K.δ gloss and the Properties table row.

### Issue 3: K.μ~ necessity deferral and circular forward/backward pointers

**ASN-0047, "Decomposition of K.μ~" → Preconditions paragraph**: "*Necessity.* Necessity of the two-distinct-values condition is proved in *Decomposition* below."

**Problem**: This is a content-free deferral pointer. The same logical unit then contains Step (A)/Step (B) proved *above* the precondition list, the "*Decomposition*" subsection *below* it, and multiple "see *Decomposition of K.μ~*" pointers elsewhere (S3★ row, CL-UNIQ prose, S8★ cell) — multiple paragraphs deferring to one downstream location. The reader bounces between three positions to assemble one argument.

**Required**: Inline the necessity argument at the precondition where the condition is stated, or move the precondition statement adjacent to its proof. Remove the bare "proved in *Decomposition* below" pointer.

### Issue 4: Essay content in composite-boundary matrix cells

**ASN-0047, Class (b) composite-boundary verification matrix, P4a cell**: The P4a cell contains a multi-sentence essay ("ValidComposite★ does *not* enforce an ordering K.μ⁺ ⤳ K.ρ — orderings such as K.α → K.ρ → K.μ⁺ satisfy every elementary precondition… Restoration at the composite boundary is *not* by re-deriving from history but by the post-state itself…").

**Problem**: A matrix cell is a structural slot for a one-line load-bearing summary. A paragraph-length argument about transition ordering and structural-vs-temporal restoration belongs in prose. The same content is then partly re-stated in the per-property P4a paragraph below the matrix, compounding the duplication.

**Required**: Reduce the cell to its one-line discharge ("J1'★ supplies a content-subspace witness at Σ'; transiently fails if K.ρ precedes the matching K.μ⁺"). Keep the ordering essay in the per-property prose only.

### Issue 5: "decision-point lives at the invariant set" and "for downstream citation" meta-prose

**ASN-0047, Orphan links section**: "The wp analysis above shows the *form* of this design choice: it consists of *not* asserting a link-coverage invariant… The decision-point lives at the invariant set, not at the transition set." **And, SubAllocatorAxiom**: "The five sub-clauses are inherited from ASN-0093 without modification; we summarise them for downstream citation."

**Problem**: The first is essay reflection on the *shape* of a design choice that does not advance any invariant or transition claim. The second is a use-site/inventory announcement ("for downstream citation") preceding a full restatement of inherited foundation clauses — the inventory framing the classifier flags.

**Required**: Delete the "decision-point lives at the invariant set" sentence. Drop "we summarise them for downstream citation"; if the five clauses must be restated for narrative continuity, restate them without the inventory preamble.

### Issue 6: "content depth is supplied fresh per insertion" overstates the freedom S8-depth permits

**ASN-0047, LinkVPositionDepthAxiom *Design intent***: "content depth is supplied fresh per insertion (ASN-0036 ValidFirstInsertionPosition, any `m ≥ 2`)".

**Problem**: The phrase "per insertion" reads as though every content insertion may pick a depth. S8-depth forces a single common depth within `V_{s_C}(d)` once non-empty, so only the *first* insertion into an empty content subspace has the free choice; subsequent K.μ⁺ steps are pinned (and a mismatching depth fails K.μ⁺'s S8-depth precondition). The cited ValidFirstInsertionPosition is itself first-insertion-only, confirming the looseness.

**Required**: Rephrase to "content depth is supplied fresh at the first insertion into an empty content subspace (any `m ≥ 2`), then fixed by S8-depth" — matching the actual contrast with the per-document link-depth commitment.

## OUT_OF_SCOPE

### Topic 1: Link-withdrawal / tombstoning mechanism for interior links
**Why out of scope**: The ASN correctly records (Open Questions) that interior link withdrawal lies outside K.μ⁻'s suffix-only presentational-removal contract under D-CTG★/D-MIN★. A status-flag/tombstone mechanism is genuinely new state, belonging to a future ASN, not a defect here.

### Topic 2: Node-allocation registry protocol abstraction
**Why out of scope**: NodeUniqueAllocation and NodeRegistryBootstrap treat the registry as external to Σ. Whether to specify its issuing/persistence/concurrency protocol abstractly is a separate ASN's territory, as the ASN itself flags.

VERDICT: REVISE
