# Alloy: Single Property Check

Model the following property as an Alloy bounded check.
You are an expert Alloy modeler in the style of Daniel Jackson (*Software Abstractions*).

## Alloy Syntax Reference

{{syntax_reference}}

## Definitions

These are the shared definitions from the ASN that this property may reference.

{{definitions}}

## Property to check

{{property}}

## Rules

- Define only the sigs, predicates, and functions this property needs.
- One or more `assert` + `check` for this property.
- One `run` command for non-vacuity (confirming the model is satisfiable).
- Scope: `check X for N` or `check X for N but M Sig, K seq, B Int`.
  Note: `Int` is capitalized; `but` is required before type-specific scopes.
- Keep scope small (`for 5` or similar) for fast counterexample search.
- Start the file directly with Alloy source code. No markdown fences, no commentary.

Write the complete Alloy model using the Write tool. The output path is provided below.
