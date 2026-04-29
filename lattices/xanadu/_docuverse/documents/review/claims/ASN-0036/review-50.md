# Cone Review — ASN-0036/S8 (cycle 2)

*2026-04-13 16:22*

I'll read the full ASN carefully, tracing every dependency chain and checking cross-property interactions.

Let me start by examining the foundation statements and then work through each property systematically.

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>/Users/shane/Documents/github/claude/xanadu-spec/vault/project-model/ASN-0036/formal-statements.md</file_path>
</parameters>
</tool_call>

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>/Users/shane/Documents/github/claude/xanadu-spec/vault/project-model/ASN-0036/dependency-graph.yaml</file_path>
</parameters>
</tool_call>

<tool_call>
<tool_name>Glob</tool_name>
<parameters>
<pattern>vault/project-model/ASN-0034/formal-statements.md</pattern>
</parameters>
</tool_call>

<tool_call>
<tool_name>Grep</tool_name>
<parameters>
<pattern>TumblerAdd|PositionAdvance</pattern>
<path>/Users/shane/Documents/github/claude/xanadu-spec</path>
<include>*.md</include>
</parameters>
</tool_call>

After thorough review, here is my finding:

---

### S8-depth postconditions 2–4 cite TumblerAdd (not in foundation statements) while postcondition 1 cites OrdinalShift for the identical property

**Foundation**: OrdinalShift (ShiftDefinition, ASN-0034) — postconditions: `shift(v, n) ∈ T`, `#shift(v, n) = #v`, `shift(v, n)ᵢ = vᵢ` for `i < m`, `shift(v, n)ₘ = vₘ + n`

**ASN**: S8-depth formal contract postconditions:
- Postcondition 1: `"OrdinalShift's prefix rule copies the subspace identifier unchanged"`
- Postcondition 2: `"TumblerAdd produces a result of length #v"`
- Postcondition 3: `"TumblerAdd's prefix rule copies it unchanged"`
- Postcondition 4: `"TumblerAdd produces a result of length #a"`

Also in S8-depth prose: `"both v + k and a + k are ordinal displacements whose depth and prefix preservation follow from TumblerAdd's component-wise definition"`

**Issue**: The `v + k` notation is defined in terms of OrdinalShift: `"v + k = shift(v, k) for k ≥ 1."` The properties cited in postconditions 2–4 — length preservation (`#shift(v, k) = #v`) and prefix preservation (`shift(v, k)ᵢ = vᵢ` for `i < m`) — are postconditions of OrdinalShift, which is listed in the foundation statements. TumblerAdd (PositionAdvance, ASN-0034) is referenced as the justification but is absent from the foundation statements. Postcondition 1 correctly cites OrdinalShift for the same prefix-preservation property that postcondition 3 attributes to TumblerAdd. Within one formal contract, the same property is attributed to two different operations. The dependency chain from postconditions 2–4 passes through TumblerAdd, which is ungrounded in the declared foundations; the chain from postcondition 1 passes through OrdinalShift, which is grounded. Any downstream consumer of postconditions 2–4 inherits an unverifiable link.

**What needs resolving**: Either add TumblerAdd (PositionAdvance) to the foundation statements so the dependency chain is complete, or rewrite postconditions 2–4 to cite OrdinalShift — matching postcondition 1's citation — since OrdinalShift already provides both length preservation and prefix preservation as explicit postconditions.
