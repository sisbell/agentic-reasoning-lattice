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

## Existing description (for reference; may be empty)

{{existing}}

## Output

The new 1-3 sentence description, plain text only. No preamble, no
formatting (no headers, no bullets, no code blocks), no
meta-commentary. Just the description body.

The agent will always write what you produce; there is no "no
change" verdict. Decide whether the existing description is worth
keeping (sometimes the right move) and emit it back, or write a
better one.