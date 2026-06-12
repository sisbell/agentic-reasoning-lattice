# Review of ASN-0129

## REVISE

### Issue 1: "A composite cannot convert between regimes" is asserted as fact, and the note's own constructions contradict it

**ASN-0129, "The atomic vocabulary," paragraph "Two argument regimes, inherited"**: "A composite cannot convert between regimes except where ASN-0128's own bridges license it (the D2 bridge; the targets_under recipe — which this note exhibits below as a PL term rather than an atom). V-TUP adds no conversion..."

**Problem**: This is a universal negative about all composites, stated flatly, with no proof — and it is false on the note's own evidence:

1. PC6's converse spells `Observe_K` as the QD filter `{x ∈ D_view : ⋀_{t ∈ F̂} t ∈ coverage_F(x) ∧ ...}`. The F̂-conjuncts are coverage tests **on the F slot** — coverage-keyed *forward* matching, for every registered K, through no bridge. AM keys forward matching by exact denotation; this composite keys it by coverage.
2. `⋃({x ∈ A_K : target ∈ coverage_G(x)}, addrs_F)` is a complete reverse lookup for *every* registered K — a QD filter over the tuple-valued base `A_K` with a V-TUP body, then a PC2a fold. Every form is admitted by this note. So D4's "reverse access is a behavior-conditional capability, deliberately opt-in" survives only at atom granularity; the algebra dissolves the fence, and the note never says so.
3. Even read narrowly as "denotation is not recoverable from coverage or vice versa," the claim fails for the address-denoting endsets the surface exclusively emits: by PrefixSpanCoverage, `t ∈ coverage(e) ⟺ (∃ x ∈ addrs(e) :: x ≼ t)` — the regimes are fully interconvertible there, which is exactly what the D2 bridge already records.

The note elsewhere holds inexpressibility claims to a strict standard — self-emit, parity, and reach are all explicitly *conjectures* with recorded proof obligations. This structurally identical negative gets asserted in passing. That is an inconsistency in the note's own epistemic discipline.

**Required**: Replace the sentence with the accurate statement: the *atoms* observe AD/AM; composites over QD's tuple-valued bases with V-TUP freely express coverage-keyed forward matching and reverse lookup for every type (PC6's Observe_K spelling being the canonical instance), so AM keying and BH3's opt-in gating are atom-level conventions, not properties the algebra inherits. If some genuine non-conversion claim is intended (e.g., `addrs(e)` is not recoverable from coverage tests alone when denoted addresses are not store-resident), state that precise claim and prove it, or give it the conjecture status its siblings receive.

### Issue 2: Five sites defer to Open Question 6, with the parity assessment stated twice

**ASN-0129, QD-audit / PC6 / C-reach / Open Question 6**: (a) QD-audit: "the proof obligation lives at Open Question 6"; (b) PC6, base definition: "(Whether some extensionally equal PL term exists is an inexpressibility question of C-reach's kind...)"; (c) PC6, relativization costs: "the proof obligation is recorded at Open Question 6 alongside C-reach and the self-emit conjecture"; (d) C-reach: "we record the proof obligation as Open Question 6 rather than discharge it by citation"; (e) OQ6 itself.

**Problem**: This is the flagged accretion pattern — multiple paragraphs in different sections deferring to the same downstream location, each repeating the status marker ("conjectured, not proven"). Worse, the parity candidate's plausibility assessment is given in full at PC6 ("a parity term would be a Boolean combination of comparisons among sums of counts and literals, and the fragment supplies no doubling or modular operator, no ℕ quantifier...") and then restated in compressed form at OQ6 ("separate even-cardinality from odd-cardinality states against every Boolean combination of comparisons among sums of counts and literals") — the same content twice, evidently the residue of the last cycle's "record parity conjecture at OQ-6" revision relocating rather than consolidating.

**Required**: Each of the three conjectures (self-emit, parity, reach) gets its substantive statement and assessment at exactly one site — either its origin or OQ6 — with a bare one-clause pointer at the other. Delete the duplicated parity assessment from whichever site loses it; collapse the repeated "conjectured, not proven" markers to the single statement site.

### Issue 3: Defensive, reviewer-facing prose and within-section duplication

**ASN-0129, multiple sections**:

- V-IDX, closing: "the vacuity is that condition evaluated at the constructible registries, not a new rule." — speaks to a reviewer about rule bookkeeping; the rule and its vacuity are already fully stated in the preceding sentences.
- QD-audit, closing: "With the arrangement and content domains outside QD's bases, no cardinality hypothesis attaches to either store: nothing in this note enumerates them." — answers an objection no claim raises; the exclusions were just established.
- PD0, closing: "— and the polarity typing is the price of saying so inductively." — rhetorical justification of the rule design, not content.
- PC6: "The stopping point is forced by the converse below, whose proof method is normalization — a PL spelling per leaf — which a raw arithmetic leaf would lack; the price is stated under *What the relativization costs* below." — this forward deferral duplicates the costs paragraph's own opening ("The *granularity* restriction is what forces the base's stopping point: an exposed arithmetic leaf ... has no PL spelling"): the same explanation twice within one section.
- The six-admissions inventory is stated twice: "plus this note's six fenced admissions (inventoried at V)" in the commitments block, and "This note's own additions are six, each fenced where introduced: ..." at V.

**Problem**: Each instance is prose the reader must skip past to follow the claim — defensive justification, duplicated explanation, or doubled inventory. These match the accretion patterns this note is flagged for.

**Required**: Delete the three defensive closers; keep the granularity explanation in one place (the costs paragraph, where it carries the full statement) with at most a bare pointer at the base definition; keep the admissions inventory in one place.

## OUT_OF_SCOPE

### Topic 1: Certified spellings for compound aggregates in PD0
PD0's aggregate rule covers `count(D) ≥ c` / `count(D) ≤ c` only, so the cross-type sum bounds PC2a promotes (`count(D₁) + count(D₂) ≥ c`) receive no direct verdict — though they are already certifiable under the existing rules via the equivalent finite disjunction `⋁_{c₁+c₂=c} (count(D₁) ≥ c₁ ∧ count(D₂) ≥ c₂)`, so no soundness gap exists.
**Why out of scope**: The classes are explicitly spelling-level, and the completeness of syntactic certification — which spellings a mechanical checker should normalize toward — is exactly Open Question 5's territory, not an error here.

META: not warranted — the note defines language, evaluation guarantees, and dynamics over abstract state, squarely in specification territory.

VERDICT: REVISE
