# Review of ASN-0094

I'll examine ASN-0094 for cross-ASN references, proof completeness, and meta-prose accretion (per the appended classifier).

## REVISE

### Issue 1: Cross-ASN references to non-foundation ASNs

**ASN-0094, Scope and Substrate Scaffolding / Definition — SubstrateConformingLayer**: "*ASN-0036 content/arrangement invariants:* S0, S1, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ. *ASN-0093 substrate invariants:* M0, M1, C0, C1, C1b, C1c, C-fin."

**Problem**: Per standard 7 (no cross-ASN references except foundation), only ASN-0034, ASN-0043, and ASN-0086 are foundation. ASN-0094 references ASN-0036 and ASN-0093 by number in multiple load-bearing places (the substrate-conforming-layer definition, the chain discipline catalog naming SubAllocatorAxiom/ChainMembershipForOrigin/etc., the scaffolding clauses' parenthetical "Content-side analog of L1, L1b, L1c on the link side", and the Case-A enumeration's "ASN-0093's structural chain").

**Required**: Either add ASN-0036/ASN-0093 to the foundation listing (if they are verified foundations), or inline the needed properties and remove the named cross-references. The scaffolding clauses already do this work locally — the references to ASN-0036/0093 in the substrate-conforming-layer definition appear redundant with the local scaffolding clauses.

### Issue 2: SubstrateConformingLayer definition overlaps with foundation

**ASN-0094, Scope and Substrate Scaffolding**: "*Substrate-conforming-layer scaffolding.* This ASN defines a *substrate-conforming layer* locally as any layer that satisfies the scaffolding clauses enumerated below."

**Problem**: ASN-0086 foundation already defines `SubstrateConformingLayer` with its own invariant/chain-discipline catalogs. ASN-0094 introduces a *different* local definition under the same name (just the scaffolding clauses, no L/S/M/C catalogs). Two definitions in play for one term invites readers to apply the wrong one.

**Required**: Either rename ASN-0094's local notion (e.g., "scaffolding-conforming layer") to disambiguate, or strengthen the local definition to match ASN-0086's exactly and cite it as foundation.

### Issue 3: "Sh-conf binds Emit_K, not K.λ" repeated multiple times

**ASN-0094, multiple sections**: The clarification "Sh-conf below binds `Emit_K`, not K.λ" (or variant) appears in: *Emit_K routing commitment*, *Sh-conf — ShapeConformanceAxiom*, and once more implicitly in the gate ordering.

**Problem**: Per the appended anti-bloat classifier, "two paragraphs in the same document say the same thing in different words" is reviser drift.

**Required**: State the binding scope once, at the Emit_K routing commitment, and let downstream sections reference it without restatement.

### Issue 4: Gate Ordering content appears in two locations

**ASN-0094, Named layer-discipline commitments**: "Gate positions index the five-gate ordering in the Sh-conf section below (0 catalog/home check, 1 SHCD, 2 Sh-conf canonical-form, 3 Sh4/FDD, 4 Sh-conf cardinality/target-domain)..."

**Problem**: The gate positions are previewed in the commitments table, then fully enumerated in the Sh-conf section's *Gate Ordering* subsection. The preview is a forward-reference essay rather than a tight cross-reference. Matches the anti-bloat pattern "multiple paragraphs in different sections defer to the same downstream location."

**Required**: Replace the parenthetical enumeration in the commitments table with a tight pointer ("see *Gate Ordering* in the Conformance Axiom section") or move the canonical enumeration earlier.

### Issue 5: Terminology inconsistency for layer disciplines

**ASN-0094, Named layer-discipline commitments table** and **per-discipline subsections**: Three of the four named disciplines are called "contract" (Sh4 idempotency contract, FDD functional-dependency contract, unit-depth retraction discipline), one is called "commitment" (single-home commitment). The table title is "*Named layer-discipline commitments*". The body alternates between "contract", "commitment", and "discipline" for the same kind of object.

**Problem**: Three terms for one structural notion forces the reader to track aliases. Anti-bloat pattern: meta-prose where stable vocabulary would do.

**Required**: Pick one term ("contract" is most precise for an axiomatic gate the layer must honor) and apply uniformly.

### Issue 6: Dead-content case in SHCD preservation

**ASN-0094, SingleHomeCoverageDiscipline preservation proof**: "*Step (Case C: `L_K^{Σ'} ⊆ L_K^Σ`)*. Impossible — L_K is monotone non-decreasing by R3. Skipped."

**Problem**: A case enumerated only to declare it impossible adds no content. Anti-bloat pattern: "a paragraph imagines a case the claim's carrier or precondition already excludes." The induction needs only Cases A and B because L_K is monotone; Case C should be absent rather than mentioned-and-skipped.

**Required**: Remove Case C; the case enumeration becomes "Case A (L_K unchanged) and Case B (L_K extends by one tuple)", matching the actual induction.

### Issue 7: Sh4HoldsAtFDDRegisteredK preconditions reference forward

**ASN-0094, Corollary — Sh4HoldsAtFDDRegisteredK**: "*Preconditions.* ... Σ reachable from `Σ_init` with FDD's preservation theorem (below) discharged on every step."

**Problem**: The corollary is stated mid-FDD-section, before FDD's preservation theorem is proved further down the same section. The "(below)" pointer is a forward reference inside one logically connected unit.

**Required**: Either move the corollary after FDD's preservation theorem, or drop the "(below)" parenthetical (the local structure makes it obvious the preservation theorem is in the same subsection).

### Issue 8: "Structural gates" prose duplicates Gate Ordering content

**ASN-0094, Conformance Axiom**: "*Structural gates.* Sh-conf's four clauses (a)–(d) partition into two structural gates in the Gate Ordering's execution sequence: clauses (a) and (b) jointly form the **canonical-form gate** at gate 2 (one gate, two operands — a non-canonical F (clause (a)) and a non-canonical G (clause (b)) are distinguishable as clause-level failures but both fall under gate 2); clauses (c) (cardinality) and (d) (target-domain) jointly form the **cardinality/target-domain gate** at gate 4."

**Problem**: This subsection re-explains the clause-to-gate mapping that Gate Ordering already specifies. The "essay content in a structural slot" pattern — explanatory prose where a citation would do.

**Required**: Delete the subsection or compress to a single cross-reference ("Sh-conf clauses (a)/(b) fire at gate 2; clauses (c)/(d) fire at gate 4; see *Gate Ordering*").

### Issue 9: Definitions section has scope-clarification meta-prose

**ASN-0094, Definition — TypedRelationCatalog**: "*Decidable membership.* Because `T_cat` is closed under `~` and finite at the quotient level, the predicate `K ∈ T_cat` is the coverage-class membership test... The test is decidable on arbitrary `K ∈ T_admissible` as the coverage-equivalence check `coverage(K) = coverage(K_rep)` against each of the finitely many registered representatives `K_rep` (not value-equality on the endset, which would reject coverage-equivalent endsets whose values differ from the listed representative)..."

**Problem**: The parenthetical "not value-equality, which would reject..." is a justification for why the chosen membership test is the right one. This is rationale prose, not specification content.

**Required**: State the decidable test, cite CoverageEqualityDecidability, and drop the contrastive parenthetical.

### Issue 10: Sh-conf rejection patterns numbered 1–5 don't match gate numbers

**ASN-0094, Sh-conf Rejection Patterns**: Patterns 1–5 are introduced, but they map to gates {2, 4, 4, 0, 0} respectively rather than gate ordering 0–4.

**Problem**: Two parallel numbering schemes for the same structural feature (gate-by-position vs. pattern-by-introduction). Confusing when walkthroughs cite "rejection pattern N" — the reader must mentally translate to gate N'.

**Required**: Number the rejection patterns by gate (Pattern-0a for `K ∉ T_cat`, Pattern-0b for `d ∉ dom(Σ.M)`, Pattern-2a/2b for canonical-form failures, Pattern-4a/4b for cardinality/target-domain), or drop the pattern numbering entirely and cite by gate + clause letter.

### Issue 11: CoverageEqualityDecidability proof has scope-justification prose

**ASN-0094, CoverageEqualityDecidability proof**: "Even the canonical unit-depth span `(x, δ(1, #x))`, whose alternative prefix-closure reading `{t : x ≼ t}` might *appear* unbounded, is in fact bounded above by `x ⊕ δ(1, #x) = shift(x, 1)` (OrdinalShift, ASN-0034) under the same T12-interval reading. The two characterizations name the same `coverage(·)` value definitionally..."

**Problem**: A defensive paragraph anticipating a reader's potential confusion (the "might *appear* unbounded" framing). Anti-bloat: "new prose around an axiom explains why the axiom is needed rather than what it says." The PrefixSpanCoverage axiom already states the equality between prefix-closure and the half-open interval; restating it here is meta-prose.

**Required**: Treat every span uniformly as a bounded T1-interval `[s_i, s_i ⊕ ℓ_i)` (which is correct by T12) and proceed with the algorithm. The PrefixSpanCoverage discussion belongs in the definitions, not in this proof.

## OUT_OF_SCOPE

### Topic 1: Multi-process semantics for Sh4/FDD/SHCD races

**Why out of scope**: Already explicitly noted in the Open Questions with the `[scope boundary]` tag. The Sh4 contract's "Scope: single-process substrate" clause is appropriate; a future ASN can address coordination protocols.

### Topic 2: Container-level link targeting (A_M symbol)

**Why out of scope**: Already in Open Questions with `[scope boundary]` tag. Nelson's metalink design is a distinct topic from shape restrictions.

### Topic 3: Composite shapes (relations constrained by other relations' content)

**Why out of scope**: Already in Open Questions with `[refinement candidate]` tag. The current 5-component shape tuple is the immediate framework; composite shapes belong to a later ASN.

### Topic 4: `(0, 0)` shapes (single-tuple existence flags)

**Why out of scope**: Already in Open Questions with `[refinement candidate]` tag. The current canonical catalog covers the productive shapes.

VERDICT: REVISE
