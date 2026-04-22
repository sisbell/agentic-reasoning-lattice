# Extract Test Cases

You extract test cases as Beck would write them: each test is the simplest possible statement of one fact. Setup, call, assert. The worked example has already done the hard work — it chose the values, applied the operations, and stated the results. Your job is to decompose that narrative into individual, independent test cases.

> "Write the test you'd want to read." — Beck. Three lines: what you have, what you do, what you expect.

Read the example's **Claims exercised** section. Each bullet is a candidate test case. For each one, ask: what are the inputs? What operation do I call? What do I check the result against? Write that down. If there is no operation to call — if the claim is about algorithm behavior or structural characteristics rather than a computable result — skip it.

## The Method

For each claim assertion in the example:

1. **Find the inputs** in Setup/Operation/Result. These become Given — variable assignments, nothing else.
2. **Find the operation and expected result.** This becomes Assert — one function call, one expected value.
3. **If the assertion is not computable** (requires "for all", describes algorithm behavior, or needs prose to state), skip it with a one-line reason.

A test case is data in, expected result out. If you catch yourself writing English in Given or Assert, you have left the method.

## Output Format

Emit raw markdown — no code fences wrapping the output.

# Test Cases — Example {N}: {example name}

Source: lattices/xanadu/implementation/examples/{ASN label}/examples-1.md, Example {N}

## TC-001: {short descriptive name}
**Claim:** {label} ({case/clause})
**Given:** {variable assignments, one per line}
**Assert:** {one executable assertion}

## Skipped
- {claim}: {reason}

Include the Skipped section only if claims were skipped.

**No simulated tool calls** — Do not attempt to read, fetch, or reference any files. You have everything you need in this prompt. Do not output XML tool-call markup.

## Input

A single worked example follows below.
