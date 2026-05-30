# Review of ASN-0058

## REVISE

### Issue 1: Proof reasoning embedded in the Properties-table statement column

**ASN-0058, Properties Introduced table (rows C1a and M7-cov)**:
- C1a: "...in particular `M(d_s)|⟦σ⟧` admits a unique maximally merged decomposition, **since `dom(f) ⊆ dom(M(d_s))` lets it inherit S2, S8-fin, S8a, and S8-depth (m ≥ 2 via C0a and content reference well-formedness) directly**"
- M7-cov: "...`v₂ ≥ v₁ + n₁`; **proof reduces to M-int (TumblerIntervalCharacterization) plus the strict-`v₁ < v₂` exclusion of `k = 0`**"

**Problem**: The Properties table is a one-line-statement index. These two rows carry derivation methodology ("since … lets it inherit …", "proof reduces to … plus the … exclusion of k = 0"). A reader scanning the table for the claim must skip past justification that already lives in the proof bodies (C1a's "Extension of M11/M12" paragraph; M7-cov's proof). Essay content in a structural slot.

**Required**: Reduce both rows to the bare statement (the inheritance reasoning and proof-reduction note belong only in the proof bodies, where they already appear).

### Issue 2: ContentReference well-formedness paragraph forward-references and pre-derives C0a

**ASN-0058, Definition (ContentReference)**: "By C0a (below), prefix confinement gives `tⱼ = uⱼ` for all `j < m` for every `t ∈ ⟦σ⟧`; in particular `t₁ = u₁`, so `dom(M(d_s)) ∩ ⟦σ⟧ ⊆ V_{u₁}(d_s)`. By S8-depth, all V-positions in `V_{u₁}(d_s)` have depth `m`, and reach(σ) has depth m (S6), so the depth-m restriction is structurally guaranteed."

**Problem**: This is a forward reference to a lemma (C0a) stated several claims later, used here to pre-justify a "structurally guaranteed" remark that is not part of the definition's content. The same confinement fact is then properly established by C0a and reused at C1a and C2. The paragraph is justificatory scaffolding the reader must work around to reach the actual well-formedness condition.

**Required**: State the well-formedness condition (the depth-m subset inclusion) without the forward-referenced derivation; let C0a carry the confinement fact where it is proven.

### Issue 3: C1b disclaimer duplicated in body and table

**ASN-0058, C1b body vs. table row**:
- Body: "It is not a claim that the I-address values `a₁, ..., aₖ` themselves are increasing — they need not be …"
- Table: "…; claim is about list positions, not I-address values"

**Problem**: The same clarifying disclaimer ("about list positions, not I-address values") appears in both the C1b prose and its Properties-table row — two slots saying the same thing.

**Required**: Keep the disclaimer in one slot (the body, where the worked-example illustration also lives); trim the table row to the statement.

## OUT_OF_SCOPE

### Topic 1: Structure of the I-space discontinuity at a non-mergeable boundary
**Why out of scope**: The first Open Question (forward gap vs. arbitrary jump) concerns I-space discontinuity structure, which would be new territory built on this ASN's canonical decomposition, not a defect here.

VERDICT: REVISE
