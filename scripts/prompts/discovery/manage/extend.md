# Claim Extraction: Extension ASN

You are extracting claims from a source ASN into a new, independent extension ASN.
This is a strict extraction — copy the claims and their proofs faithfully, with no
improvements, additions, or editorial changes.

## Source ASN

{{source_content}}

## Foundation Context

{{foundation_statements}}

## Base ASN Export (what the base already covers)

{{base_statements}}

## Task

Extract the following claims from the source ASN into a new extension ASN:

**Claims to extract:** {{claims}}
**New ASN:** {{target_label}}
**Extends:** {{base_label}} ({{base_title}})
**Source:** {{source_label}}

For each listed claim label, find it in the source ASN and extract:
1. The full formal statement with its label and type annotation
2. The complete proof
3. Any worked examples that follow the proof
4. Any supporting definitions needed that are NOT already in the base ASN's export

## Output Format

Write a complete ASN reasoning document. Follow this structure exactly:

```
# {{target_label}}: {{ext_title}}

*{{date}}*

[One paragraph: what this ASN extends and why these claims belong in the base's domain.
Do not reference the source ASN.]

## [Section for each claim or group]

**LABEL** — *Name* (TYPE, construct). [Formal statement]

*Proof.* [Complete proof]  ∎

[Worked example if present in source]

## Statement registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| ... | ... | ... | introduced |

## Open Questions

[Any open questions from the source ASN that relate specifically to the extracted claims.
Omit if none are relevant.]
```

## Constraints

1. **Strict extraction.** Copy the claim statements and proofs from the source. Do not
   rephrase, simplify, or "improve" them.
2. **Self-contained.** The extension must be readable without the source ASN. Include any
   context needed to understand the extracted claims, referencing the base ASN.
3. **No new content.** Do not add claims, lemmas, or discussion that do not appear
   in the source.
4. **No source references.** Do not mention the source ASN. The extension stands on its
   own as part of the base ASN's domain.
5. **Supporting material.** If a proof depends on a claim that is NOT being extracted
   and is NOT in the base's export, note the dependency explicitly.

Output ONLY the ASN document. No commentary before or after.
