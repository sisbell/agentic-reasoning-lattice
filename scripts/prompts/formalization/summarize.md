# Summarize Claims

For each claim below, write a 1-3 sentence summary of what it
establishes. The summary should be self-contained — a reader should
understand the claim's role and guarantees without needing to parse
formal notation or read the proof.

Good summary: "In words: tumbler comparison requires only the two
addresses themselves — no external index, allocator state, or global
registry participates in the decision. The comparison examines at most
min(#a, #b) component pairs."

Bad summary: "See T1 for details." / "This follows from the definition."

## Claims

{{claims}}

## Output

One line per claim, in the same order as the input:

```
LABEL: summary text here
```

Do not include preamble, explanation, or formatting beyond the label and summary.
