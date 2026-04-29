### 1. Table Structure

(none)

---

### 2. Status Vocabulary

10 findings:

1. **S3**: `design; uses NoDeallocation (ASN-0034)` — not a recognized pattern. Use `design requirement` (dropping the `uses` clause) or `introduced; uses NoDeallocation (ASN-0034)`.
2. **S7a**: `design; uses Prefix, T4, T4c (ASN-0034)` — not a recognized pattern.
3. **S7b**: `design; uses T4 (ASN-0034)` — not a recognized pattern.
4. **S7c**: `design; uses S7b, T4, TA7a (ASN-0034)` — not a recognized pattern.
5. **S8a**: `axiom (V-positions are element-field tumblers); structural properties from T4 (ASN-0034)` — not a recognized pattern. Standard form is bare `axiom`.
6. **S8-depth**: `design; uses OrdinalShift, TumblerAdd (ASN-0034)` — not a recognized pattern.
7. **D-CTG**: `design; uses T0(a), T1, T3 (ASN-0034)` — not a recognized pattern.
8. **OrdAddHom**: `lemma from ord, w_ord, TumblerAdd, TA0 (ASN-0034)` — missing parentheses. Must be `lemma (from ...)`.
9. **OrdAddS8a**: `lemma from OrdAddHom, S8a, TumblerAdd (ASN-0034)` — missing parentheses. Must be `lemma (from ...)`.
10. **OrdShiftHom**: `corollary from OrdAddHom, OrdAddS8a, OrdinalShift, OrdinalDisplacement (ASN-0034)` — wrong preposition. Must be `corollary of ...`.

---

### 3. Header Format

22 findings:

**Non-PascalCase names in parentheses** (16):

1. `**S0 (Content immutability).**` → `**S0 (ContentImmutability).**`
2. `**S1 (Store monotonicity).**` → `**S1 (StoreMonotonicity).**`
3. `**S2 (Arrangement functionality).**` → `**S2 (ArrangementFunctionality).**`
4. `**S3 (Referential integrity).**` → `**S3 (ReferentialIntegrity).**`
5. `**S4 (Origin-based identity).**` → `**S4 (OriginBasedIdentity).**`
6. `**S5 (Unrestricted sharing).**` → `**S5 (UnrestrictedSharing).**`
7. `**S6 (Persistence independence).**` → `**S6 (PersistenceIndependence).**`
8. `**S7a (Document-scoped allocation).**` → `**S7a (DocumentScopedAllocation).**`
9. `**S7b (Element-level I-addresses).**` → `**S7b (ElementLevelIAddresses).**`
10. `**S7c (Element-field depth).**` → `**S7c (ElementFieldDepth).**`
11. `**S7 (Structural attribution).**` → `**S7 (StructuralAttribution).**`
12. `**S8-fin (Finite arrangement).**` → `**S8-fin (FiniteArrangement).**`
13. `**S8a (V-position well-formedness).**` → `**S8a (VPositionWellFormedness).**`
14. `**S8-depth (Fixed-depth V-positions).**` → `**S8-depth (FixedDepthVPositions).**`
15. `**S8 (Finite span decomposition).**` → `**S8 (FiniteSpanDecomposition).**`
16. `**S9 (Two-stream separation).**` → `**S9 (TwoStreamSeparation).**`

**Non-standard header format — em-dash/italic style** (6). All should use `**LABEL (PascalCaseName).**`:

17. `**ord(v)** — *OrdinalExtraction* (DEF, function).` → `**ord(v) (OrdinalExtraction).**`
18. `**vpos(S, o)** — *VPositionReconstruction* (DEF, function).` → `**vpos(S, o) (VPositionReconstruction).**`
19. `**w_ord** — *OrdinalDisplacementProjection* (DEF, function).` → `**w_ord (OrdinalDisplacementProjection).**`
20. `**OrdAddHom** — *OrdinalAdditionHomomorphism* (LEMMA).` → `**OrdAddHom (OrdinalAdditionHomomorphism).**`
21. `**OrdAddS8a** — *AdditionPreservesS8a* (LEMMA).` → `**OrdAddS8a (AdditionPreservesS8a).**`
22. `**OrdShiftHom** — *OrdinalShiftHomomorphism* (COROLLARY).` → `**OrdShiftHom (OrdinalShiftHomomorphism).**`

---

### 4. Missing Table Entries

(none)

---

### 5. Missing Prose Sections

(none)

---

### 6. Duplicate Labels

(none)

---

### 7. Missing Boundary Markers

45 findings. No `---` markers appear anywhere in the document.

**Section headers missing `---`** (17):

1. `## Two components of state`
2. `## The content store`
3. `## The arrangement and referential integrity`
4. `## Content identity`
5. `## Sharing`
6. `## Persistence independence`
7. `## Structural attribution`
8. `## Span decomposition`
9. `## V-position ordinal decomposition`
10. `## Arrangement contiguity`
11. `### Concrete example`
12. `## Valid insertion position`
13. `### Valid insertion position examples`
14. `## The separation theorem`
15. `## Worked example`
16. `## The document as arrangement`
17. `## Properties Introduced`
18. `## Open Questions`

(18 section headers)

**Property/definition headers missing `---`** (28, excluding the first `**Σ.C (ContentStore).**`):

`**Σ.M(d) (Arrangement).**`, `**S0 ...**`, `**S1 ...**`, `**S2 ...**`, `**S3 ...**`, `**S4 ...**`, `**S5 ...**`, `**S6 ...**`, `**S7a ...**`, `**S7b ...**`, `**S7c ...**`, `**S7 ...**`, `**S8-fin ...**`, `**S8a ...**`, `**S8-depth ...**`, `**S8 ...**`, `**ord(v) ...**`, `**vpos(S, o) ...**`, `**w_ord ...**`, `**OrdAddHom ...**`, `**OrdAddS8a ...**`, `**OrdShiftHom ...**`, `**D-CTG ...**`, `**D-MIN ...**`, `**D-CTG-depth ...**`, `**D-SEQ ...**`, `**Definition (ValidInsertionPosition).**`, `**S9 ...**`

---

`RESULT: 77 FINDINGS`