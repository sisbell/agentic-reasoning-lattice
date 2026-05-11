# Describe Claim

Write a 1-3 sentence description of what this claim establishes.
The description should be self-contained — a reader should understand
the claim's role and guarantees without needing to parse formal
notation or read the proof.

Guidance:
- Lead with the upshot — what the claim means or delivers — not with an enumeration of its parts. The synthesis sentence is usually the most valuable one and should come first, not last.
- Let the opening verb signal claim type: "Defines" / "Posits" for
  definitions and axioms; "Proves" / "Establishes" for theorems;
  "A named corollary exporting..." for claims that relabel another
  claim's postcondition without adding mathematical content.
- Keep dependency citations, proof-step references, and historical
  or implementation commentary out of the description — the formal
  contract and surrounding prose carry those.
- Length should track what the claim says, not the amount of design
  rationale around it. A load-bearing negative result may warrant
  more words than a routine closure axiom.

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