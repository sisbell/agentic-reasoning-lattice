# Literary Machines - Table of Contents

Edition 87.1, May 1987 by Theodor Holm Nelson

## Page Mapping

Raw page numbers (page-NNN) map to Nelson's chapter/page numbering (X/Y).

---

### Front Matter (pages 001-013)

| Raw Page | Content |
|----------|---------|
| 001 | (blank) |
| 002 | Epigraph (James Burke quote) |
| 003 | Introduction (The Daring Proposal) |
| 004 | Title page |
| 005 | Copyright |
| 006 | Edition 87.1 note |
| 007-008 | Plan of this book (hypertext structure) |
| 009 | 1981 Dedication (Eric Blair) |
| 010-011 | 1987 Dedication |
| 012-013 | Contents |

---

### Chapter Zero: Hyperworld (pages 014-026)

| Raw Page | Chapter Page |
|----------|--------------|
| 014-026 | 0/1-0/13 |

**Complete coverage**

---

### Chapters One: Introductions (pages 027-080)

Multiple introductory chapters. Nelson's page numbering: 1/1 - 1/54

| Raw Page | Chapter Page | Section |
|----------|--------------|---------|
| 027 | 1/1 | Chapters One title page |
| 028-040 | 1/2-1/14 | An Obvious Vision |
| 041-054 | 1/15-1/28 | The Sense of Wonderful Developments |
| 055-066 | 1/29-1/40 | Two Cultures Face the Future |
| 067-072 | 1/41-1/46 | Hypertext |
| 073-076 | 1/47-1/50 | The School Problem |
| 077-080 | 1/51-1/54 | A Brief History of the Xanadu Caper |

**Complete coverage**

---

### Chapter Two: The Proposal (pages 081-142)

The core proposal. Nelson's page numbering: 2/1 - 2/62

| Raw Page | Chapter Page | Section |
|----------|--------------|---------|
| 081-083 | 2/1-2/3 | Title & Plan of chapter |
| 084-090 | 2/4-2/10 | Section 1: Overview |
| 091-100 | 2/11-2/20 | Section 2: Documents |
| 101-105 | 2/21-2/25 | Section 3: Links |
| 106-114 | 2/26-2/34 | Section 4: Content addressing |
| 115 | 2/35 | (no marker detected) |
| 116-125 | 2/36-2/45 | Section 5: Addressing cont'd |
| 126-135 | 2/46-2/55 | Section 6-7: Versions, transclusion |
| 136-142 | 2/56-2/62 | Section 8-9: Summary |

**Complete coverage**

---

### Chapters Three (pages 143-167)

Technical background chapters. Nelson's page numbering: 3/1 - 3/25

| Raw Page | Chapter Page | Notes |
|----------|--------------|-------|
| 143-145 | 3/1-3/3 | |
| 146-159 | 3/4-3/17 | |
| 160 | 3/18 | (no marker detected) |
| 161-167 | 3/19-3/25 | |

**Complete coverage**

---

### Chapters Four: Technical Specifications (pages 168-246)

Nelson's page numbering: 4/1 - 4/79

| Raw Page | Chapter Page | Section |
|----------|--------------|---------|
| 168-181 | 4/1-4/14 | Overview, economics, performance |
| 182-194 | 4/15-4/27 | **Tumblers** (designer addresses) |
| 189 | 4/22 | (no marker detected) |
| 195-207 | 4/28-4/40 | Tumblers continued |
| 208-227 | 4/41-4/60 | **Links** (structure & types) |
| 228-246 | 4/61-4/79 | **Protocols** (FEBE & BEBE) |

**Complete coverage**

Key sections for specification work:
- **Tumblers**: pages 182-207 (4/15-4/40)
- **Links**: pages 208-227 (4/41-4/60)
- **Protocols**: pages 228-246 (4/61-4/79)

---

### Chapters Five: Business Aspects (pages 247-267)

Nelson's page numbering: 5/1 - 5/21

| Raw Page | Chapter Page | Notes |
|----------|--------------|-------|
| 247-250 | 5/1-5/4 | |
| 251 | 5/5 | (no marker detected) |
| 252-267 | 5/6-5/21 | |

**Complete coverage**

---

### Chapter Six: Appendices (pages 268-276)

Nelson's page numbering: 6/1 - 6/6+

| Raw Page | Chapter Page | Notes |
|----------|--------------|-------|
| 268-272 | 6/1-6/6 | |
| 273-276 | - | (no markers detected, likely index/back matter) |

**Complete coverage**

---

## Quick Reference by Chapter

| Chapter | Raw Pages | Chapter Pages | Pages |
|---------|-----------|---------------|-------|
| Front | 001-013 | - | 13 |
| 0 | 014-026 | 0/1-0/13 | 13 |
| 1 | 027-080 | 1/1-1/54 | 54 |
| 2 | 081-142 | 2/1-2/62 | 62 |
| 3 | 143-167 | 3/1-3/25 | 25 |
| 4 | 168-246 | 4/1-4/79 | 79 |
| 5 | 247-267 | 5/1-5/21 | 21 |
| 6 | 268-276 | 6/1-6/6+ | 9 |
| **Total** | **276** | | |

---

## Key Sections for Specification

| Topic | Chapter Pages | Raw Pages | Description |
|-------|---------------|-----------|-------------|
| Core Proposal | 2/1-2/62 | 081-142 | User-facing vision |
| Tumblers | 4/15-4/40 | 182-207 | Address system |
| Links | 4/41-4/60 | 208-227 | Link structure |
| Protocols | 4/61-4/79 | 228-246 | FEBE/BEBE interface |

---

## File Access

**Directory:** `resources/literary-machines/raw/`

**Files:**

- `page-NNN.png` - Scanned page image
- `page-NNN.txt` - OCR text extraction

**Find by chapter page:**

```bash
grep -l "LITERARY 4/15" raw/*.txt
# Returns: raw/page-182.txt
```

**Read OCR text:**

```bash
cat raw/page-182.txt
```

**View image (if OCR unclear):**

```bash
open raw/page-182.png
```
