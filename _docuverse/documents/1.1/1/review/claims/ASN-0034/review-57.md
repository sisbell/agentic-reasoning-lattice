# Cone Review — ASN-0034/T8 (cycle 3)

*2026-04-15 21:49*

I'll read the ASN carefully, focusing on cross-property consistency, precondition chains, and term usage across the full document.

<tool_call>
{"name": "Read", "arguments": {"file_path": "/Users/shane/Documents/github/claude/xanadu-spec/docs/methodology.md", "offset": 0, "limit": 50}}
</tool_call>

Let me examine the memory for additional context on ASN-0034.

<tool_call>
{"name": "Read", "arguments": {"file_path": "/Users/shane/.claude-account2/projects/-Users-shane-Documents-github-claude-xanadu-spec/memory/project_blueprinting_asn34_status.md"}}
</tool_call>

<tool_call>
{"name": "Glob", "arguments": {"pattern": "properties/ASN-0034/**/*.yaml"}}
</tool_call>

<tool_call>
{"name": "Glob", "arguments": {"pattern": "vault/ASN-0034/**/*.yaml"}}
</tool_call>

<tool_call>
{"name": "Glob", "arguments": {"pattern": "**/ASN-0034/**"}}
</tool_call>

Now let me focus on the ASN content provided. I need to trace every dependency, every quantifier scope, every term definition, and every case analysis — looking specifically for issues NOT already captured in the Previous Findings.

Let me verify the key cross-property chains systematically.

<tool_call>
{"name": "Grep", "arguments": {"pattern": "T3.*Canonical", "path": "/Users/shane/Documents/github/claude/xanadu-spec"}}
</tool_call>

<tool_call>
{"name": "Grep", "arguments": {"pattern": "IntrinsicComparison", "path": "/Users/shane/Documents/github/claude/xanadu-spec"}}
</tool_call>

<tool_call>
{"name": "Grep", "arguments": {"pattern": "T2.*depends", "path": "/Users/shane/Documents/github/claude/xanadu-spec"}}
</tool_call>

Let me look at the T2 YAML metadata to check its declared dependencies.

<tool_call>
{"name": "Glob", "arguments": {"pattern": "**/T2*.yaml"}}
</tool_call>

<tool_call>
{"name": "Glob", "arguments": {"pattern": "**/T2*"}}
</tool_call>

<tool_call>
{"name": "Grep", "arguments": {"pattern": "IntrinsicComparison", "path": "/Users/shane/Documents/github/claude/xanadu-spec", "include": "*.yaml"}}
</tool_call>

<tool_call>
{"name": "Glob", "arguments": {"pattern": "vault/**/*.yaml"}}
</tool_call>

<tool_call>
{"name": "Bash", "arguments": {"command": "find /Users/shane/Documents/github/claude/xanadu-spec -name '*.yaml' | head -30"}}
</tool_call>

<tool_call>
{"name": "Bash", "arguments": {"command": "find /Users/shane/Documents/github/claude/xanadu-spec -path '*0034*' -type f | head -30"}}
</tool_call>

<tool_call>
{"name": "Bash", "arguments": {"command": "find /Users/shane/Documents/github/claude/xanadu-spec -name '*.yaml' -type f | head -30"}}
</tool_call>

<tool_call>
{"name": "Read", "arguments": {"file_path": "/Users/shane/Documents/github/claude/xanadu-spec/properties/T2-IntrinsicComparison.yaml"}}
</tool_call>

<tool_call>
{"name": "Bash", "arguments": {"command": "ls /Users/shane/Documents/github/claude/xanadu-spec/properties/ | grep -i 'T2\\|intrinsic'"}}
</tool_call>

<tool_call>
{"name": "Bash", "arguments": {"command": "ls /Users/shane/Documents/github/claude/xanadu-spec/properties/ | head -40"}}
</tool_call>

<tool_call>
{"name": "Bash", "arguments": {"command": "find /Users/shane/Documents/github/claude/xanadu-spec -type d | head -20"}}
</tool_call>

<tool_call>
{"name": "Bash", "arguments": {"command": "ls /Users/shane/Documents/github/claude/xanadu-spec/"}}
</tool_call>

<tool_call>
{"name": "Bash", "arguments": {"command": "ls /Users/shane/Documents/github/claude/xanadu-spec/asn/ASN-0034/"}}
</tool_call>

<tool_call>
{"name": "Bash", "arguments": {"command": "ls /Users/shane/Documents/github/claude/xanadu-spec/asn/ASN-0034/properties/ | head -40"}}
</tool_call>

<tool_call>
{"name": "Bash", "arguments": {"command": "cat /Users/shane/Documents/github/claude/xanadu-spec/asn/ASN-0034/properties/T2-IntrinsicComparison.yaml"}}
</tool_call>

Good — the YAML metadata declares `depends: [T1]` but NOT T3. Now let me verify the proof text to confirm T3 is explicitly invoked.

The ASN content I was given contains this in the T2 proof, Case 2:

> "if m = n, then T3 gives a = b"

T3 (CanonicalRepresentation) is explicitly invoked to bridge from component-wise agreement and equal length to tumbler equality. Without T3, the algorithm determines "all components match, same length" but cannot conclude `a = b` as tumblers — the postcondition "The ordering among a and b under T1 is determined" requires resolving the equality case, which needs T3.

This is exactly the same pattern that the previous finding identified for T1 (which has since been fixed — T1's contract now declares `Depends: T3`). T2 has the same gap but was not caught.

Let me verify nothing else is missing by checking a few more property files.

<tool_call>
{"name": "Bash", "arguments": {"command": "cat /Users/shane/Documents/github/claude/xanadu-spec/asn/ASN-0034/properties/TumblerSub-TumblerSub.yaml"}}
</tool_call>

<tool_call>
{"name": "Bash", "arguments": {"command": "cat /Users/shane/Documents/github/claude/xanadu-spec/asn/ASN-0034/properties/TA5-HierarchicalIncrement.yaml"}}
</tool_call>

<tool_call>
{"name": "Bash", "arguments": {"command": "cat /Users/shane/Documents/github/claude/xanadu-spec/asn/ASN-0034/properties/T10a-AllocatorDiscipline.yaml"}}
</tool_call>

Good — T10a YAML correctly declares all six foundations. Now let me verify the T2 issue is genuine and not already covered.

The previous findings list:
- T1 missing T3: **fixed** (contract now has Depends: T3)
- T4 missing T3: **fixed** (contract now has Preconditions referencing T3)
- T2 is **never mentioned** in previous findings

And the current ASN text for T2's formal contract:

> *Preconditions:* `a, b ∈ T` — two well-formed tumblers (finite sequences over ℕ with `#a ≥ 1` and `#b ≥ 1`, per T0).
> *Postconditions:* (a) The ordering among `a` and `b` under T1 is determined. (b) At most `min(#a, #b)` component pairs are examined. (c) The only values consulted are `{aᵢ : 1 ≤ i ≤ #a}`, `{bᵢ : 1 ≤ i ≤ #b}`, `#a`, and `#b`.
> *Frame:* No external data structure is read or modified — the comparison is a pure function of the two tumblers.

No Depends clause. The YAML declares `depends: [T1]` but not T3. The proof explicitly invokes T3.

---

### T2 formal contract and YAML metadata omit T3 (CanonicalRepresentation) as a dependency, despite the proof explicitly invoking it

**Foundation**: T3 (CanonicalRepresentation) — "tumblers with the same length and identical components at every position are equal"
**ASN**: T2 (IntrinsicComparison) proof, Case 2: "if m = n, then T3 gives a = b"; formal contract contains Preconditions, Postconditions, and Frame but no Depends clause; YAML metadata declares `depends: [T1]` only
**Issue**: The T2 proof's Case 2 (no divergence within the shared range, equal lengths) concludes `a = b` by invoking T3: the scan exhausts all `min(m, n) = m = n` positions without divergence, establishing `aᵢ = bᵢ` for all `1 ≤ i ≤ m` and `m = n`, and then bridges to tumbler equality via T3. Without T3, the proof establishes component-level agreement but cannot conclude the tumbler-level identity `a = b` — postcondition (a) ("The ordering among a and b under T1 is determined") requires resolving the equality case, which needs exactly this bridge. This is the same dependency pattern that T1's contract now correctly declares: "Depends: T3 (CanonicalRepresentation) — postcondition (b) requires the bridge from component-level agreement to tumbler equality." T2 uses T3 in the same way (bridging component agreement to tumbler equality) but neither the prose contract nor the YAML metadata records the dependency. The YAML declares only `depends: [T1]`, and the formal contract has no Depends clause at all. A contract reader — or a mechanical dependency checker — sees T2 depending only on T1, missing the T3 invocation that grounds the equality case.
**What needs resolving**: T2's formal contract must include a Depends clause declaring T3 (CanonicalRepresentation), consistent with T1's contract. The YAML metadata must add T3 to its `depends` list. Specifically, postcondition (a) requires T3 for the equality case: when all `min(m,n)` component pairs agree and `m = n`, T3 bridges component-level agreement to `a = b`.
