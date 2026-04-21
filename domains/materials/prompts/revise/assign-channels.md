You are deciding which expert channels each review finding needs consulted before revision.

## Channels

- **Theory** (theory channel) — classical mechanics and statistical mechanics. What the theory of this period predicts, what principles it invokes, what reasoning it uses — independent of specific measurements. Ask Theory when the fix requires understanding theoretical intent or what the theory would say. Examples: "What does equipartition predict for molar heat capacity?", "Does the theory require this proportionality to hold exactly?"

- **Evidence** (evidence channel) — measured heat-capacity and materials data. What the data actually shows, what values are reported, what substances and conditions are covered. Ask Evidence when the fix requires grounding in experimental results. Examples: "What values are reported for copper's specific heat in the corpus?", "Does the data span the high-temperature regime?"

A finding may need Theory, Evidence, both, or neither (if the fix is derivable from the note's own content — definitions, reasoning, or data already present).

## Note Content

{asn_content}

## REVISE Items

{revise_section}

## Instructions

For each REVISE issue, output a block in exactly this format:

```
## Issue N: [title from review]
Reason: [1-2 sentences explaining which channels are needed and why — or why the fix is internal]
Theory question: [one focused question]       (include only if Theory is needed)
Evidence question: [one focused question]      (include only if Evidence is needed)
```

If the fix is derivable from the note alone, omit both question lines.

Output ONLY the issue blocks, nothing else.
