# Motif Base Picker

You pick the base note that a new extension will hang off of. The
extension will be a new note containing the construct from the motif;
it will `extends` the base, and the motif's cited notes will end up
citing the extension.

## How to choose

Read the motif and the candidate notes. Each candidate is either one
of the motif's cited notes or a substrate dependency of one of them.

Pick the candidate that owns the construct's defining vocabulary —
the primitives the motif's construct actually requires — and sits as
deep in the dependency stack as possible while still containing
those primitives.

- If the construct's defining primitives already exist in one of the
  *cited notes themselves*, pick that cited note.
- Otherwise pick the deepest dep whose vocabulary covers the
  construct's primitives.

If no candidate cleanly owns the construct's defining vocabulary —
the abstract construct described by the motif sits above every
listed candidate — set `base` to `STANDALONE`. This is the honest
answer when the right home would have to be a new note rather than
an existing one.

## The motif

{{motif_finding}}

## Candidate notes (full bodies)

{{candidate_notes}}

## Output

Output a single YAML document — no prose, no code fences:

    base: ASN-0058      # or STANDALONE
    rationale: |
      One-paragraph rationale. Use literal-block (|) for multi-line.
