### 1. Table Structure

The "Properties Introduced" table has the required three columns (Label, Statement, Status). (none)

---

### 2. Status Vocabulary

All 46 status values match standard patterns. (none)

---

### 3. Header Format

**Finding 1:** `**T0(a) (Unbounded component values).**`

The name "Unbounded component values" contains spaces. Must be PascalCase with no spaces. Should be:

```
**T0(a) (UnboundedComponentValues).**
```

---

### 4. Missing Table Entries

Every bold property header and every `**Definition (Name).**` header has a corresponding row in the Properties Introduced table. (none)

---

### 5. Missing Prose Sections

Every label in the Properties Introduced table has a corresponding bold header in the prose. (none)

---

### 6. Duplicate Labels

No label appears more than once in the table. (none)

---

### 7. Missing Boundary Markers

Every `##` and `###` section header is preceded by `---`. Every property and definition bold header (after the first) is preceded by `---`. T0(a) is the first property in the ASN and correctly has no `---` before it. Property-label sub-headers within the Worked Example section are correctly exempt. (none)

---

RESULT: 1 FINDING