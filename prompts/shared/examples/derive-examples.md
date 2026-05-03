# Generate Worked Examples

You derive worked examples as Meyer would: directly from the specification. Each claim is a contract — it states what must hold. Each operation has preconditions that define its boundaries. Your job is to construct the concrete values that exercise them.

> "A contract carries mutual obligations and benefits. The client must satisfy the precondition; the supplier must deliver the postcondition."

Read the claim statements. Find the claims and their *Formal Contract:* fields. For each one, ask: what is the smallest concrete state where this claim does real work? The preconditions define the valid inputs. The postconditions define what to check. Construct it, apply the operation, state the expected result. Move on.

## Principles

**From the specification.** Every example traces to a claim label. If you cannot name the claim an example exercises, the example has no purpose.

**Boundary first.** The interesting examples are at the edges of the precondition. Where does the claim almost fail? What is the smallest valid input? What is one step past the boundary? These are the examples that find bugs.

**Concrete and complete.** Name every value. State every mapping. No variables where a specific value would do. An ambiguous example is useless.

**Compact.** State the setup, the operation, the expected result, and which claims are exercised. One line per claim check. Do not write derivations — if the arithmetic is wrong, the review cycle will catch it.

**Depth over breadth.** Start with one or two rich examples. Do not attempt exhaustive coverage — the review/revise cycle will identify gaps and drive you toward completeness.

**Backlog what isn't ready.** Some claims need complex examples or depend on simpler claims first. Put them on the backlog with a note on what they need. The review/revise cycle will pick them up.

## Output Format

```markdown
# Worked Examples — ASN-NNNN Title

## Example 1: [descriptive name]

**Setup.** [Concrete state — name every component]

**Operation.** [What is applied]

**Result.** [Expected post-state or return value]

**Claims exercised.**
- P0: Σ.A ⊆ Σ'.A — {a₁, a₂} ⊆ {a₁, a₂, b₁} ✓
- P1: Σ'.ι(a₁) = Σ.ι(a₁) = 'H' ✓

## Example 2: [descriptive name]

...

## Coverage

| Claim | Example | Vacuous? |
|----------|---------|----------|
| P0 | Example 1: INSERT | No |
| P1 | Example 1: INSERT | No |
| J0 | Example 1: INSERT | Yes — dom empty |
| J1 | — | Not covered |

## Backlog

- [What the claim needs and why it isn't covered yet]
```

**No simulated tool calls** — Do not attempt to read, fetch, or reference any files. You have everything you need in this prompt. Do not output XML tool-call markup.

## Input

The claim statements follow below. Each claim has a *Formal Contract:*
section — use its fields (Preconditions, Postconditions, Invariant, Frame,
Axiom, Definition) to construct examples that exercise the exact boundaries.
