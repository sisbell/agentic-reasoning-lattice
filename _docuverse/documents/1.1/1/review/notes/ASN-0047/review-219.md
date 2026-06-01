# Review of ASN-0047

I reviewed the state model, the seven elementary transitions plus K.μ~, the coupling constraints, the D-SEQ★ derivation, and the worked examples. The core arithmetic and invariant-preservation arguments are sound — the D-SEQ★ derivation (both m=2 and m≥3 cases), the K.δ structural identities, the K.μ⁻ constructive/post-state equivalence, and the GlobalLineage inductions all hold up under inspection. The issues below are accreted meta-prose and reviser-drift patterns, which the anti-bloat classifier directs me to surface at source.

## REVISE

### Issue 1: Non-circularity meta-prose in the K.μ~ decomposition
**ASN-0047, *Decomposition of K.μ~***: "We record the non-circularity of the argument once, here: `S3★(Σ')` is established by Step (B), not assumed as a filter hypothesis. Step (A) derives subspace preservation from the decomposition's own preconditions; Step (B) recovers `S3★(Σ')` compositionally... Steps (A) and (B) below carry only their object-level content."

**Problem**: This paragraph argues *about* the structure of the proof (that it is not circular) rather than advancing it. A reader following Steps (A) and (B) does not need to be told in advance that S3★(Σ') is "established not assumed" — the steps either establish it or they do not. This is the flagged pattern "prose justifies... non-circular by Y argument" / "explains why rather than what." The same defensive content is echoed in the S3★ × K.μ~ verification-matrix cell ("...no appeal to S3★(Σ'); §*Decomposition of K.μ~*"), so the accretion already appears in two places.

**Required**: Delete the non-circularity preamble and the matrix cell's "no appeal to S3★(Σ')" clause. Let Steps (A)/(B) carry their object-level content directly.

### Issue 2: NodeBaptism axiom wrapped in provisioning rationale
**ASN-0047, *Elementary transitions* (NodeBaptism)**: "Node addresses are not minted by any docuverse transition; the operation set provides no `inc`-rule producing a node. This axiom records, over `Σ` alone, what the provisioning boundary commits at every K.δ node-allocation event..."

**Problem**: The normative content of the axiom is conditions (a) freshness and (b) bootstrap lineage. The surrounding sentences explain *why the axiom is needed* (nodes sit outside the inc-rule machinery, the boundary provisions them) rather than stating what it commits — the flagged "new prose around an axiom explains why the axiom is needed rather than what it says." The "records what the provisioning boundary commits" framing restates (a)/(b) in narrative form.

**Required**: Reduce to the axiom's two conditions plus the single frame fact that no transition mints a node; move the provisioning-boundary rationale to the existing Open Question that already asks what the boundary must guarantee.

### Issue 3: Three-form replacement partition stated twice
**ASN-0047, *Elementary transitions* (iii)**: "Replacement... takes three forms by composite shape... The forms are partitioned exhaustively by the new I-address's `dom(C)`/`R` membership..." and ***Worked example: prior-provenance and first-time-transcluded replacements* (Contrast)**: "The three forms partition by the (pre-state membership of `aₓ` in `dom(C)`, pre-state membership of `(aₓ, d)` in `R`) pair: (in C, in R) ⟹ two-step; (in C, not in R) ⟹ three-step; (not in C, not in R) ⟹ four-step."

**Problem**: The exhaustive partition by (dom(C), R) membership is stated abstractly in *Elementary transitions* and again concretely in the worked-example contrast — "two paragraphs in the same document say the same thing in different words." The elementary-section version also forward-defers the case split to the worked examples, so the partition lives in two slots with neither being self-contained.

**Required**: State the partition once (the concrete table belongs with the worked examples) and replace the elementary-section restatement with a bare pointer, or vice-versa — not both.

### Issue 4: FrontierEquivalence lemma carries downstream use-site prose
**ASN-0047, *Elementary transitions* (FrontierEquivalence)**: "The biconditional licenses K.δ's k = 0 guard `inc(t, 0) ∉ E` to be read either operationally ('the `(t, 0)` increment has not yet been consumed') or structurally ('`t` is the frontier of `A`'s chain')."

**Problem**: The lemma's content is the biconditional and its proof. This trailing sentence inventories how the result is consumed at the K.δ k=0 guard — the flagged "definition's introduction enumerates downstream consumers" pattern. The dual reading is already implicit in the biconditional itself.

**Required**: Drop the use-site sentence; the K.δ k=0 discharge that actually invokes the lemma is the natural place to note the operational/structural reading, and it already cites FrontierEquivalence.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The J4 fork composite leaves the forked document's link subspace empty and notes a link-inheritance mechanism "would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." This is correctly deferred (an Open Question already records it) — new territory, not a defect here.

### Topic 2: Tombstone / interior-link-withdrawal mechanism
D-CTG★/D-MIN★ confine K.μ⁻ to link-subspace suffix truncation, so interior link withdrawal needs a separate mechanism. This is flagged as an Open Question and belongs in a future ASN, not as a revision to this one.

VERDICT: REVISE
