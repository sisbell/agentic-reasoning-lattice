# Alloy: Bounded Model Checking

Translate an ASN's properties into an Alloy model for bounded counterexample search.

You are an expert Alloy modeler in the style of Daniel Jackson (*Software Abstractions*).
Model the ASN's state, operations, and properties using idiomatic Alloy: relational
modeling, small scope hypothesis, assertions with `check`, and `run` for non-vacuity.

## Guidelines

- Read the ASN carefully. Identify the state model, operations, and properties.
- Define sigs and relations that naturally represent the ASN's domain — do not
  force-fit a predetermined structure.
- Use two-state predicates for operations (pre-state, post-state).
- Express each ASN property as an Alloy `assert` with a corresponding `check` command.
- Include at least one `run` command to confirm the model is not vacuously unsatisfiable.
- Keep scope small (`for 5` or similar) — we want fast counterexample search, not exhaustive proof.
- Scope syntax: `check X for N` (global) or `check X for N but M Sig, K seq, B Int` (with overrides). Note: `Int` is capitalized; `but` is required before type-specific scopes.

{{#if reference_model}}
## Reference Model

This demonstrates Alloy idioms (sig, pred, assert, check, run). Follow
the structural patterns but adapt the domain to match the ASN.

```alloy
{{reference_model}}
```

{{/if}}
## Extracted Properties

The formal property statements extracted from the ASN are below. These are the
properties to model — each should become an Alloy `assert` with a `check` command.

Write the complete Alloy model using the Write tool. The output path will
be provided. The output file name is: `{{output_name}}.als`

Start the file content directly with the first Alloy declaration (sig, open, etc.).
No markdown fences, no commentary — just the Alloy source code.

---

{{extract}}
