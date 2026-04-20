You are extracting Nelson's design features from Xanadu ASN specifications.

You are given one or more ASN documents. Your task is to find every Nelson quote, reference, or paraphrase of design intent and extract the underlying design features.

IMPORTANT: Output ONLY the markdown features file. No commentary, no explanations, no preamble. Start your response with `# Nelson Design Features`.

## What to extract

Look for ALL of these patterns:
- Direct quotes: `"..."` attributed to Nelson
- Block quotes: `> "..." [LM x/y]`
- Inline citations: text followed by `[LM chapter/page]`
- Paraphrased intent: "Nelson states...", "Nelson requires...", "Nelson is explicit..."
- Design principles stated without attribution but clearly from Literary Machines

Each quote or reference expresses a **design feature** — something the system must do or guarantee.

## What to produce

1. **Identify features**: Each quote (or cluster of closely related quotes) expresses one feature. Extract the core feature as a concise requirement statement.

2. **Categorize**: Group features by system aspect. Use categories that emerge naturally:
   - Addressing (tumbler structure, permanence, allocation)
   - Content (storage, retrieval, immutability)
   - Documents (creation, ownership, modification)
   - Versioning (versions, history, backtrack)
   - Transclusion (virtual copies, content sharing)
   - Links (endsets, discovery, attachment)
   - Economics (royalties, publishing, rights)
   - Performance (scalability, retrieval speed)
   - Other categories as needed

3. **Assign feature numbers**: `F-ADDR-01`, `F-CONT-01`, `F-LINK-01`, etc. Short category code (3-4 chars).

4. **Deduplicate**: The same Nelson quote often appears across multiple ASNs. Each feature appears once; list all ASNs that reference it.

5. **Map to ASNs**: For each feature, list which ASNs reference it.

## Output format

```
# Nelson Design Features

## Category Name

### F-CODE-NN: Feature title

> "The exact Nelson quote" [LM x/y]

**Feature**: One-sentence statement of what the system must guarantee.

**ASNs**: ASN-0001, ASN-0004, ASN-0011

---

### F-CODE-NN: Next feature

...
```

Rules:
- Every feature MUST have at least one direct Nelson quote
- Include the [LM x/y] reference when available; some quotes lack explicit citations
- If multiple quotes support the same feature, include the most definitive one as the primary quote and list others as "See also: [LM x/y]"
- Feature statements should be requirements-style: "The system must..." or "Every X must..."
- Order features within each category by feature number
- Order categories alphabetically by category code

## Handling the existing features file

The existing features file is **authoritative**. It may contain manual edits.

- **NEVER** rewrite, reword, or restructure existing entries
- **NEVER** change existing feature numbers, titles, quotes, or descriptions
- **NEVER** change existing category assignments
- You may **add** an ASN to an existing feature's ASN list if the ASN references that feature
- You may **add** new features that are not yet represented, using the next available number in the appropriate category
- If a new feature overlaps with an existing one, do NOT add it — the existing entry takes precedence
- Reproduce the existing file exactly, with only additions

If no existing file is provided, produce the complete file from scratch.

## Existing features file

{{existing_features}}

## ASN content

{{asn_content}}
