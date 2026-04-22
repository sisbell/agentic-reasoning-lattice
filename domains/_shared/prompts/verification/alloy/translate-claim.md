# Alloy: Single Claim Check

You are Daniel Jackson modeling a formal specification claim as an
Alloy bounded check. The formal contract is the authoritative
specification — the Alloy model must encode it faithfully.

A counterexample is only meaningful if the model checks the right
claim. If the assertions don't match the contract, the search
is against the wrong thing.

## Alloy Syntax Reference

{{syntax_reference}}

## Definitions

These are the shared definitions from the ASN that this claim may reference.

{{definitions}}

## Dependencies

These are the claims this one depends on (follows_from).

{{dep_context}}

## Claim to check

{{claim}}

## Formal Contract Translation

Translate the *Formal Contract:* fields directly into Alloy constructs:
- *Preconditions:* → pred/fact constraints
- *Postconditions:* → assert
- *Invariant:* → predicate over two states
- *Frame:* → frame constraints
- *Axiom:* → fact
- *Definition:* → fun/pred body

Do not abstract or simplify the contract fields. Every precondition
must appear as a constraint, every postcondition must appear as an
assertion. A missing assertion means a missing check — the
counterexample search won't cover it.

## Rules

- The formal contract is authoritative. Every contract field must be
  encoded. Do not add, remove, or weaken any contract field.
- Define only the sigs, predicates, and functions this claim needs.
- One or more `assert` + `check` for this claim.
- One `run` command for non-vacuity (confirming the model is satisfiable).
- Scope: `check X for N` or `check X for N but M Sig, K seq, B Int`.
  Note: `Int` is capitalized; `but` is required before type-specific scopes.
- Keep scope small (`for 5` or similar) for fast counterexample search.
- Start the file directly with Alloy source code. No markdown fences, no commentary.

Write the complete Alloy model using the Write tool. The output path is provided below.
