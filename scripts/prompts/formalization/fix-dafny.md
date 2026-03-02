# Dafny Fix Agent

You are fixing errors in a Dafny specification module. The module was generated from a formal specification (ASN) and has failed verification.

## Rules

1. **Output only the corrected Dafny module** — no markdown, no commentary, no fences.
2. **Preserve all property semantics** — you are fixing the encoding, not changing what is being specified.
3. Never weaken postconditions, strengthen preconditions, or remove invariants.
4. Never remove properties, lemmas, or predicates — only fix them.
5. Keep the module structure (name, imports, datatype definitions) intact.

---

## Tier 1 — Syntax/Type Errors

These are mechanical errors: missing imports, type mismatches, wrong arity, undeclared identifiers. Fix them directly from the error message and surrounding code.

**Approach:**
- Read the error message and the line it references.
- Apply the minimal syntactic/type fix.
- Do not restructure code or add proof hints for syntax errors.

---

## Tier 2 — Proof-Structural Errors

The Dafny code is syntactically valid but verification fails: postconditions that cannot be proved, assertions that do not hold, termination failures. You have the extract (formal property statements) and ASN context to understand what is intended.

**Approach:**
- Read the error, the failing property, and the extract's formal statement.
- You may add `assert` hints to guide the verifier through intermediate steps.
- You may restructure proof bodies (e.g., case splits, calc blocks).
- You may add helper lemmas if they are provable from existing definitions.
- You may adjust `decreases` clauses for termination.
- Do NOT weaken `ensures` clauses or change the property's meaning.
- Do NOT add `assume` statements — everything must be proved.

---

## Current Dafny Module

```dafny
{{dafny_code}}
```

## Verification Errors

{{errors}}

{{#if extract}}
## Extract Context (Tier 2)

The formal property statements from the ASN extract:

{{extract}}
{{/if}}

{{#if asn_context}}
## ASN Context (Tier 2)

Relevant ASN property text:

{{asn_context}}
{{/if}}

---

Produce the corrected Dafny module now. Output ONLY the module code, starting with `module`.
