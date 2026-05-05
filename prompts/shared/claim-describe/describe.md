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

If an existing description is provided, evaluate whether it still
accurately describes the current claim. If yes, return it verbatim.
If the claim has changed in a way that the existing description no
longer captures, return a new description.

## Claim

{{claim}}

## Existing description

{{existing}}

## Output

The 1-3 sentence description, plain text only. No preamble, no
formatting (no headers, no bullets, no code blocks). Just the
description body.
