## Format Audit: ASN-0036

### 1. Table Structure

The table has three columns in the required order: `Label | Statement | Status`.

(none)

### 2. Status Vocabulary

All status values match standard patterns. Checked:
- `introduced`, `design requirement`, `axiom` — standard
- `from S0`, `from GlobalUniqueness, T3 (ASN-0034)`, `from S7a, S7b, S0, S4, T4, T3, GlobalUniqueness (ASN-0034)`, `from D-CTG, D-CTG-depth, D-MIN, S8-fin, S8-depth, T1 (ASN-0034)` — match `from LABEL1, LABEL2` pattern
- `from T4, S7b (ASN-0034)` — matches `from LABEL1, LABEL2 (ASN-NNNN)` pattern
- `consistent with S0, S1, S2, S3` — standard
- `corollary of D-CTG, S8-fin, S8-depth, T0(a), T1, T3 (ASN-0034)` — standard
- `theorem from S8-fin, S2, S8a, S8-depth, T1, T3, T5, T10, TA5 (ASN-0034)`, `theorem from S0` — standard

(none)

### 3. Header Format

All 22 bold headers have the required form `**LABEL (Name).**` or `**Definition (Name).**` with trailing period inside the bold closure.

(none)

### 4. Missing Table Entries

The correspondence run definition appears only inside the S8-depth Formal Contract block (`*Definition:* A *correspondence run* ...`) — not as a standalone `**Definition (CorrespondenceRun).**` header — so no table entry is required.

(none)

### 5. Missing Prose Sections

Every table label has a corresponding bold header in the prose:

| Table label | Prose header |
|---|---|
| Σ.C | `**Σ.C (ContentStore).**` |
| Σ.M(d) | `**Σ.M(d) (Arrangement).**` |
| S0–S9, S7a, S7b | each has `**SN (Name).**` |
| S8-fin, S8a, S8-depth | each has `**S8-x (Name).**` |
| D-CTG, D-MIN, D-CTG-depth, D-SEQ | each has `**D-X (Name).**` |
| ValidInsertionPosition | `**Definition (ValidInsertionPosition).**` |

(none)

### 6. Duplicate Labels

No label appears more than once in the table.

(none)

---

`RESULT: CLEAN`