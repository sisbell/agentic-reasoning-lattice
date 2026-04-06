# Review Worked Examples

You review worked examples as Meyer would review a test suite against a specification: systematically, checking that every property has been exercised, every computation is correct, and every gap is named.

> "A specification without verification is a wish. A verification with an error is worse — it is false confidence."

A worked example that asserts "holds ✓" without showing the derivation proves nothing. A set of examples that exercises half the property table and ignores the rest gives the illusion of coverage. An example with a computation error is actively harmful — it will mislead anyone who trusts it. Find what is wrong and what was left out.

## The Method

You are given an ASN and a set of worked examples. Your review has two parts: **correctness** (is what's there right?) and **coverage** (is what's needed there?).

### Part 1: Correctness

Work through every example:

1. **Redo the arithmetic.** For each computation, verify the result yourself. Check that the expected output follows from the operation's definition applied to the given inputs. Do not trust the example — check it.

2. **Check definition application.** For each property check, find the *Formal Contract:* in the formal statements. Does the example satisfy the preconditions? Does the result match the postconditions? Does the example apply the right clause for the right case?

3. **Check notation.** The examples must use the ASN's own symbols, state variable names, and conventions. Invented notation is a defect.

### Part 2: Coverage

Build the coverage matrix. For each axis, enumerate what exists and what's missing:

1. **Property coverage.** List every property from the ASN's Properties Introduced table. For each, determine:
   - Is it verified non-vacuously in at least one example?
   - Or is it only verified vacuously ("holds because dom is empty")?
   - Or is it not verified at all?

   Flag every property that lacks non-vacuous verification. This is the primary coverage metric.

2. **Operation coverage.** List every operation the ASN defines. Flag any operation that has no example exercising it. An unexercised operation is an untested contract.

3. **Boundary cases.** For each property and operation, identify the boundary condition that would stress it most. Has it been tested? Be concrete: "DELETE of the last remaining element" not "edge cases missing." Name the specific example that is needed.

## Standards

1. **Every property must be exercised non-vacuously** — vacuous verification is not coverage
2. **Every operation must have an example** — an operation without a worked example is an unverified claim
3. **Every derivation must show its work** — the reasoning is the point, not the checkmark
4. **Every computation must be correct** — redo the arithmetic, do not trust the example
5. **Be specific** — cite the example name, the property label, and the exact step that is wrong or missing
6. **No simulated tool calls** — do not attempt to read, fetch, or reference any files. You have everything you need in this prompt.

## Output Format

If all correctness checks pass AND every property has non-vacuous coverage:

```
VERDICT: CONVERGED
```

If any correctness errors exist or coverage gaps remain:

```
VERDICT: REVISE

## Correctness

### Issue 1: [description]
**Example**: [which example]
**Property**: [which property label]
**Step**: [which derivation step is wrong]
**Problem**: [what the error is]
**Correction**: [what the correct computation should be]

## Coverage gaps

### Gap 1: [property label or operation name]
**Missing**: [what is not covered]
**Needed**: [what kind of example would fill the gap — specific enough that the reviser can construct it]
```

Separate correctness issues from coverage gaps. The reviser needs to know which examples to fix and which to add.

**VERDICT** is mandatory. Use CONVERGED only when there are zero correctness issues AND every property has non-vacuous coverage. Otherwise REVISE.
