# Extract Test Cases

You extract concrete, independent test cases from a worked example. Each test case isolates one property assertion with specific input values and an expected outcome.

> "A test case that exercises two properties at once tests neither properly." — Meyer

Read the scenario. Find every property assertion in the **Properties exercised** section. For each one, extract the concrete values from the scenario's Setup, Operation, and Result sections that are needed to verify that assertion independently.

## Principles

**One property, one assertion.** Each test case exercises exactly one property with one set of concrete inputs and one expected result. A scenario that exercises five properties produces (at least) five test cases.

**Given/Assert pattern.** Every test case has:
- **Given:** the concrete values needed — tumbler literals, sets, mappings, operation parameters
- **Assert:** the expected outcome — an ordering, equality, validity verdict, set membership, or computation result

**Self-contained.** Every value referenced in Assert must be defined in Given (or computable from Given values using the operation under test). A reader should be able to verify the assertion from the Given values alone, without reading the scenario narrative.

**Property traceability.** Each test case names the property label it exercises (T1, TA3, T6(d), etc.) and the specific case or clause if the property has multiple cases.

**Concrete values only.** Use the specific values from the scenario. No universally quantified variables, no "for all k". If the scenario demonstrates a general principle with a specific instance, extract the specific instance.

**Negative cases.** If the scenario demonstrates a property violation, a precondition failure, or a deliberate invalidity, extract that as a test case. Use assertions like:
- `Assert: ¬valid(x)` — address invalidity
- `Assert: undefined` — operation precondition violated
- `Assert: round-trip fails (result = r ≠ a)` — with the concrete failing values

**Operations are explicit.** When the test case involves an operation (⊕, ⊖, inc, fields), state the operation in Assert with its concrete inputs and expected output:
- `Assert: a ⊕ w = [1, 0, 3, 0, 2, 0, 1, 5]`
- `Assert: inc(u₁, 0) = [1, 0, 2]`
- `Assert: fields(a).doc = [2, 1]`

**Decompose compound assertions.** If a property check in the scenario verifies multiple things (e.g., "a₁ < a₂ < a₃"), split into separate test cases (a₁ < a₂, a₂ < a₃) unless the property explicitly requires the chain.

## Output Format

```markdown
# Test Cases — {ASN label} Scenario {N}: {scenario name}

Source: vault/5-examples/{ASN label}/examples-1.md, Scenario {N}

## TC-001: {short descriptive name}
**Property:** {label} ({case/clause})
**Given:** {concrete values, one per line if multiple}
**Assert:** {expected outcome}

## TC-002: {short descriptive name}
**Property:** {label}
**Given:** {values}
**Assert:** {outcome}
```

Number test cases sequentially within the scenario: TC-001, TC-002, etc.

**No simulated tool calls** — Do not attempt to read, fetch, or reference any files. You have everything you need in this prompt. Do not output XML tool-call markup.

## Input

The ASN text and a single scenario from the worked examples follow below.
