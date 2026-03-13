# Consultation Curation

A manual step that applies when drafting foundation ASNs. After consultation completes but before running discovery, you inspect the generated questions and answers and trim material that falls outside the ASN's scope.

This is not part of the automated pipeline. It applies when the ASN's scope boundary matters — particularly for ontology layers where out-of-scope material creates the kind of foundation gaps the [layer stack](foundations.md) is designed to prevent.

## When It Applies

Foundation ontology ASNs have strict scope boundaries defined by their layer. The decomposition agent explores broadly by design. An inquiry about link foundations will produce questions about link discovery, link versioning, and link operations — valid questions, but out of scope for a foundation ontology.

The `out_of_scope` field in `inquiries.yaml` reduces this automatically by telling the decomposition agent what topics to avoid. But exclusions are best-effort — some out-of-scope questions will still get through, and manual inspection remains necessary for foundation ASNs.

For operation ASNs or other work where scope is less critical, the normal pipeline flow (consult → discover) is fine.

## Process

### 1. Run consultation only

```bash
python scripts/draft.py --inquiries N consult
```

### 2. Inspect questions

Read `vault/experts/ASN-NNNN/consultation/questions.md`. For each question:

- **Keep** — questions about what the thing *is*: structural properties, permanence, identity, ownership, datatype definition.
- **Remove** — questions about operations on the thing, discovery/indexing, versioning, cross-layer interactions. These belong in later ASNs.

### 3. Trim answers to match

Remove corresponding answer blocks from `answers.md`. Note the trimming in the file header so it's visible.

### 4. Optionally revise questions

If the generated questions missed important angles, write new questions into `questions.md` and re-run consultation for the new questions.

### 5. Commit the curation

```bash
git add vault/experts/ASN-NNNN/consultation/
git commit -m "curate(asn): ASN-NNNN consultation — trim to foundation scope"
```

### 6. Resume at discover

```bash
python scripts/draft.py --inquiries N --resume discover
```

The `--resume discover` flag skips consultation and uses whatever is in the consultation directory.

## Example: ASN-0032 (Link Ontology)

Inquiry: "What is a link in the Xanadu system?"

Consultation generated 20 sub-questions. Trimmed to 10 — removed questions about link discovery and indexing (operations layer), link versioning (version semantics), and link operations (mutation layer). Kept questions about what links connect, link permanence, endset structure, ownership, and home document relationship.
