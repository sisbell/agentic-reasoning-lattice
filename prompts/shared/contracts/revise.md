# Revise Method Contract

You previously derived the Design-by-Contract spec for ONE Rust method. A Bertrand
Meyer validation found discrepancies. Produce the **corrected full contract** that
fixes EXACTLY those findings and nothing else. Everything you need is in this
prompt — do not read files or use tools.

## The method

Module: **{{module_id}}**
Method: **`{{method}}`**

## The method unit (algorithm + invariants)

{{unit}}

## Backing (the authoritative spec)

{{backing}}

## Contracts of the methods this one calls (compose / discharge against these)

{{callees}}

## Your prior contract

{{contract}}

## Validation findings to fix

{{findings}}

## Rules

- Fix EVERY listed finding. Change nothing the validation did not flag — correct
  content stays **verbatim** (do not reword, restructure, or "improve").
- Same output structure as the original: **1. Formal Contract**, **2. Rust
  annotation**, **3. Callee discharge**. Signature copied verbatim.
- For **TRANSCRIBE** backing: re-align the flagged clause to the Dafny
  `requires`/`ensures` exactly. For **DERIVE**: re-ground each flagged derived
  postcondition in a cited callee postcondition; for an `UNDISCHARGED_CALLEE`,
  either show the discharge concretely or emit the `INCONSISTENCY:` line.
- If a finding is **wrong** (the contract was actually correct), do NOT corrupt the
  contract to satisfy it — keep that part as-is and append a single
  `## Validator dissent` line at the very end naming the finding and why it is
  incorrect. Use this sparingly and only when you are certain.

## Output

The complete corrected contract as raw text, starting at `## 1. Formal Contract`.
No fences, no preamble, no commentary (except a `## Validator dissent` note if
genuinely warranted).
