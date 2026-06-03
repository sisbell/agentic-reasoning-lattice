# Review of ASN-0069

## REVISE

### Issue 1: V11a carries subsequent-fork machinery (j ≥ 1) that V11's chain premise excludes
**ASN-0069, V11a**: "whose value is `1 + j`, where `j ≥ 0` is the *subsequent-emission count* of `A_v(dⁱ⁻¹_new)` immediately prior to step `i`'s firing — `j = 0` covers V1's first-fork sub-case ... and `j ≥ 1` covers V1's subsequent-fork sub-case ... The two regimes exhaust `A_v(dⁱ⁻¹_new)`'s emission stream..."
**Problem**: V11a describes the *same* chain as V11, and V11's premise fixes "each step ... is the *first* fork of its immediate source." Under that premise every step uses K.δ at `k = 1`, so `A_v(dⁱ⁻¹_new)` has emitted nothing prior and `j = 0` at every step — the extension value is always `1`. The entire `j ≥ 1` / "subsequent-emission count" / "two regimes exhaust the stream" apparatus describes emissions this chain never produces. This is a paragraph imagining a case the carrying claim's precondition already excludes.
**Required**: Either restrict V11a's per-step characterization to the value `1` (matching V11's first-fork premise), or, if the general `1 + j` form is wanted for reuse, detach it from V11's chain notation and state it as an independent lemma with its own (non-first-fork-restricted) premise.

### Issue 2: The R' set-equality verification is stated three times
**ASN-0069, V0 Effects table / V0 prose / "The Fork Composite"**:
- Effects table: "`R' = R ∪ {(a, d_new) : ...}` (V9; set equality verified by sequential composition: `R^{(1)} = R` by K.δ frame; then `R^{(2)} = R^{(1)}` by K.μ⁺ frame; then `R^{(2+n)} = ...`)"
- V0 prose: "The R' line is a set equality... verified by the elementary decomposition: K.δ's frame condition gives `R^{(1)} = R`; K.μ⁺'s frame condition gives `R^{(2)} = R^{(1)}`; the K.ρ × n phase adds..."
- Verification: "Cumulative effect across the `n` K.ρ steps: `R^{(2+n)} = R^{(2)} ∪ {...}`"
**Problem**: The same K.δ-frame / K.μ⁺-frame / K.ρ-cumulative decomposition is written out in three places. Two paragraphs in the same document saying the same thing in different words.
**Required**: State the set-equality verification once (in "The Fork Composite"), and have the Effects table cite it rather than re-deriving inline.

### Issue 3: V5a wraps the lemma in use-site inventory and meta-commentary
**ASN-0069, V5a (closing paragraph)**: "We record it here because it is what makes the source-fork relationship semantically symmetric (Corollary 1...) and what underwrites the independence of sibling forks (Corollary 2)." and "V5a is not a property of the fork operation itself — it is a property of the transition system's per-document frame discipline."
**Problem**: This is downstream-consumer enumeration plus meta-commentary about what kind of property V5a is — neither advances the lemma's content. The use sites (V10(b), V11, V12) already cite V5a at their own points.
**Required**: Delete the use-site inventory and the "not a property of the fork operation" editorializing; keep the lemma statement, the two clauses, and the corollaries.

### Issue 4: V11's two "Remark on premise scope" paragraphs defend cases the premise already excludes
**ASN-0069, V11, "Remark on V11's premise scope — non-immediate-source modifications" and "— modifications M-targeted at `d_src` after step 1"**: e.g. "Arrangement modifications M-targeted at documents *other than* the current step's immediate source ... are therefore structurally outside the premise's scope at step `i`."
**Problem**: The premise is already scoped to each step's immediate source; both remarks then re-argue at length that modifications *outside* that scope are admissible. This is defensive accretion around a premise — explaining why the narrow scope is "fine" rather than advancing the proof, which consumes only the immediate-source values. A reader following the derivation does not need the excluded-case defense to verify the induction.
**Required**: Collapse both remarks to at most one sentence noting the premise is per-immediate-source and that out-of-scope edits are discharged operationally by V5a Cor. 2 / conclusion-anchoring at `Σ`. Drop the case-by-case walk-throughs.

### Issue 5: V0 "Composite structure" clause is a forward/backward cross-reference essay
**ASN-0069, V0, "Composite structure"**: "This uninterrupted-sequence requirement is what permits V4 (arrangement inheritance) and V5 (source isolation) to compose cleanly across the composite ... The inter-composite analogue is V11's premise that each step's source has its content-subspace arrangement unchanged..."
**Problem**: The operative content is "no other elementary transitions fire between the constituent steps." The remainder narrates which downstream claims rely on it and draws an analogy to V11 — meta-prose in a structural slot.
**Required**: Keep the requirement statement (uninterrupted sequence, no intervening K.μ⁻/K.μ~/K.μ⁺ on `d_op`); drop the "is what permits V4 and V5" inventory and the V11-analogue sentence.

### Issue 6: Dependency Audit contains self-referential citation-practice prose
**ASN-0069, Dependency Audit**: "every consumed claim is cited at its use site by ASN number and claim name; the per-claim citation map is the body itself, not re-tabulated here. No foundation claim is redeveloped where a citation would serve."
**Problem**: These sentences describe the document's own citation discipline rather than stating a dependency fact. The actionable content of this section is the single conclusion that ASN-0040 has no use site and should be dropped from `depends:`.
**Required**: Reduce the section to the ASN-0040-removal finding (and, if needed, the one note that the local `d_src ≼ d_new` re-derivation is retained for V11a's length by-product). Delete the citation-practice commentary.

### Issue 7: V9 is derived from a coupling *constraint* rather than the step that discharges it
**ASN-0069, V9 (derivation)**: "By J1★ applied to the composite `Σ →* Σ'`, every `a` such that [content-subspace-referenced ... and not previously] ... must satisfy `(a, d_new) ∈ R'`."
**Problem**: J1★ is a validity *requirement* on composites; the records that satisfy it are produced by the K.ρ × n phase. Deriving V9 from J1★ inverts the order — J1★'s satisfaction is itself established (in "The Fork Composite") by exhibiting those K.ρ records. The clean derivation points at the K.ρ effect; citing J1★ uses the obligation as if it were the generator.
**Required**: Derive V9 directly from the K.ρ × n cumulative effect (`R^{(2+n)} = R ∪ {(a, d_new) : a ∈ ran(M'(d_new))}`), and note J1★ is *discharged by* V9 rather than the reverse.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork-during-edit, descendant enumeration, snapshot-vs-living forks, transcludent sources
**Why out of scope**: These are the ASN's own Open Questions and correctly deferred — they require concurrency semantics, a discoverability/indexing operation, and transclusion machinery not defined here.

VERDICT: REVISE
