You are deciding which expert channels each review finding needs consulted before revision.

## Channels

- **Nelson** (theory channel) — Ted Nelson's design intent. What the system was *meant* to do, what semantic constraints the designer intended. Nelson has access to Literary Machines and Nelson's concept notes. Ask Nelson when the fix requires understanding design intent. Examples: "Was this operation intended to be total or partial?", "Does the design require this ordering to be strict?"

- **Gregory** (evidence channel) — the udanax-green implementation. What the code actually does, what constraints it enforces, what edge cases it handles. Gregory has access to the knowledge base synthesis and the udanax-green C source. Ask Gregory when the fix requires evidence from the implementation. Examples: "Does the allocator enforce single-depth increment?", "What does INSERT do when the span crosses a boundary?"

A finding may need Nelson, Gregory, both, or neither (if the fix is derivable from the ASN's own content — definitions, proofs, or reasoning already present).

## ASN Content

{asn_content}

## REVISE Items

{revise_section}

## Instructions

For each REVISE issue, output a block in exactly this format:

```
## Issue N: [title from review]
Reason: [1-2 sentences explaining which channels are needed and why — or why the fix is internal]
Nelson question: [one focused question]       (include only if Nelson is needed)
Gregory question: [one focused question]      (include only if Gregory is needed)
```

If the fix is derivable from the ASN alone, omit both question lines.

Output ONLY the issue blocks, nothing else.
