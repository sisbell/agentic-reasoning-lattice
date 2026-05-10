# Describe Claim

Write a 1-3 sentence description of what this claim establishes.
The description should be self-contained — a reader should understand
the claim's role and guarantees without needing to parse formal
notation or read the proof.

Good description: "In words: tumbler comparison requires only the two
addresses themselves — no external index, allocator state, or global
registry participates in the decision. The comparison examines at most
min(#a, #b) component pairs."

Bad description: "See T1 for details." / "This follows from the definition."

## Claim

{{claim}}

## Existing description

{{existing}}

## Output

Two-line response. The first line is the verdict, all caps:

- `UNCHANGED` — the existing description still accurately captures
  the current claim. Use only when there is an existing description
  above (i.e., `{{existing}}` is not `(none)`). Output the single
  line `UNCHANGED` and nothing else.

- `REVISED` — there is no existing description, or the existing one
  must be replaced. Line 1 is `REVISED`. Line 2 onward is the new
  1-3 sentence description, plain text only (no headers, no bullets,
  no code blocks, no formatting).

No preamble. No meta-commentary. No restating of the verdict.
The first character of your response is `U` or `R`.
