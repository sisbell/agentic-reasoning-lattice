# Promotion — Feeding the Pipeline

The promotion pipeline extracts new work from completed ASNs. As ASNs are written and reviewed, they generate open questions ("what about versioning?") and OUT_OF_SCOPE items ("link survival belongs to a different ASN"). Promotion evaluates these and turns the worthwhile ones into new inquiries.

## Purpose

The specification grows organically. Each ASN answers one inquiry but discovers adjacent questions that belong to other ASNs. Promotion is the mechanism that turns these discoveries into new pipeline work, keeping `inquiries.yaml` fed with the most productive next questions.

## Two Sources of New Work

### Open Questions

Every ASN has an "Open Questions" section — gaps discovered during derivation that the current ASN can't address. These are questions the discovery agent flagged while building the model.

Examples:
- "How does deletion interact with active transclusions?" (discovered while modeling DELETE)
- "What happens to links when their target document is deleted?" (discovered while modeling link semantics)

### OUT_OF_SCOPE Items

During review, the review agent identifies issues that belong to a different ASN's scope. These are marked OUT_OF_SCOPE in the review file and deferred.

Examples:
- "The versioning implications of DELETE belong to ASN-0009" (found in ASN-0005 review)
- "Concurrent modification semantics are outside the scope of content insertion" (found in ASN-0004 review)

## How It Works

### Questions Promotion

```
ASN open questions
     |
     v
check existing promotions    (avoid duplicates)
     |
     v
evaluate each question       (opus — is it worth a new inquiry?)
     |
     v
frame as inquiry             (title, description, rationale)
     |
     v
update inquiries.yaml        (append new entries)
     |
     v
write promotion record       (vault/1-promote/ASN-NNNN/)
```

The evaluation agent (opus) considers:
- Is this question already covered by an existing ASN or inquiry?
- Is it specific enough to produce a meaningful ASN?
- Does it address a gap that matters for the overall specification?
- Can it be answered from the available evidence sources (Nelson + Gregory)?

Questions that are too vague, already covered, or unlikely to yield useful properties are rejected with a brief rationale.

### Scope Promotion

```
review OUT_OF_SCOPE items
     |
     v
extract from all review files    (vault/2-review/ASN-NNNN/)
     |
     v
check existing promotions        (avoid duplicates)
     |
     v
evaluate each item               (opus — is it worth a new inquiry?)
     |
     v
frame as inquiry
     |
     v
update inquiries.yaml
     |
     v
write promotion record
```

Similar evaluation criteria, but OUT_OF_SCOPE items often have more context — the review explains why the item is out of scope and what ASN should address it.

## Artifacts

### Input

| Artifact | Location | Description |
|----------|----------|-------------|
| ASN | `vault/asns/ASN-NNNN-*.md` | Open Questions section |
| Review files | `vault/2-review/ASN-NNNN/review-*.md` | OUT_OF_SCOPE items |
| Existing inquiries | `vault/1-promote/inquiries.yaml` | Duplicate check |
| Existing promotions | `vault/1-promote/ASN-NNNN/` | Previous promotion records |

### Output

| Artifact | Location | Description |
|----------|----------|-------------|
| New inquiries | `vault/1-promote/inquiries.yaml` | Appended entries |
| Promotion record | `vault/1-promote/ASN-NNNN/` | Decisions and rationale |

## CLI Reference

```bash
# Evaluate open questions from ASN-0012
python scripts/promote.py questions 12

# Preview decisions without updating files
python scripts/promote.py questions 13 --dry-run

# Evaluate review OUT_OF_SCOPE items from ASN-0004
python scripts/promote.py scope 4

# Preview extracted OUT_OF_SCOPE items without invoking Claude
python scripts/promote.py scope 14 --dry-run
```

### Flags

| Flag | Description |
|------|-------------|
| `--dry-run` | Show decisions without updating `inquiries.yaml` or writing records |

## Inquiries.yaml

The master inquiry list that feeds the discovery pipeline:

```yaml
- id: 1
  title: "Tumbler Algebra"
  description: "What are the algebraic properties of tumblers..."
  source: "initial"

- id: 18
  title: "Link Survival Under Deletion"
  description: "What must the system guarantee about links when..."
  source: "promoted from ASN-0005 open question"
```

Each entry has:
- `id` — sequential number
- `title` — short descriptive title
- `description` — what to investigate
- `source` — where the inquiry came from (initial, promoted from ASN-NNNN)

## Design Decisions

**Why evaluate questions instead of promoting all?** Not every open question is worth an ASN. Some are too vague ("what about performance?"), already covered by existing ASNs, or touch on implementation details rather than design properties. Evaluation filters for questions that will produce productive specification work.

**Why separate `questions` and `scope`?** They come from different sources with different structure. Open questions are freeform text from the ASN author. OUT_OF_SCOPE items are structured findings from the review agent with specific scope rationale. The evaluation criteria and extraction logic differ.

**Why track promotion records?** To avoid re-evaluating the same questions on subsequent runs. The promotion record shows what was evaluated, what was promoted, and what was rejected (with rationale). This makes the pipeline idempotent — running promotion twice produces the same result.
