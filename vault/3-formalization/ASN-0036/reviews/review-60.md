# Cross-cutting Review — ASN-0036 (cycle 1)

*2026-04-12 23:05*

I'll read the ASN and foundation statements carefully, then systematically check cross-property consistency.

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>/Users/shane/Documents/github/claude/xanadu-spec/vault/project-model/ASN-0036/formal-statements.md</file_path>
<offset>0</offset>
<limit>50</limit>
</parameters>
</tool_call>

Let me check the current formal statements to verify the foundation properties match what's cited.

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>/Users/shane/Documents/github/claude/xanadu-spec/vault/project-model/ASN-0036/formal-statements.md</file_path>
</parameters>
</tool_call>

<tool_call>
<tool_name>Glob</tool_name>
<parameters>
<pattern>/Users/shane/Documents/github/claude/xanadu-spec/vault/project-model/ASN-0036/*</pattern>
</parameters>
</tool_call>

<tool_call>
<tool_name>Glob</tool_name>
<parameters>
<pattern>/Users/shane/Documents/github/claude/xanadu-spec/vault/project-model/ASN-0034/*</pattern>
</parameters>
</tool_call>

I have the complete ASN and foundation in the prompt. Let me now deliver my cross-review findings.

---

### S8-vdepth undeclared in Properties Introduced table

**Foundation**: N/A — this is an internal structural issue
**ASN**: The Properties Introduced table (top of ASN) lists S8-fin, S8a, S8-depth, and S8 but omits S8-vdepth. Yet S8-vdepth is formally defined later as a standalone section with its own axiom and formal contract: `(A d, v : v ∈ dom(Σ.M(d)) : #v ≥ 2)`.
**Issue**: S8-vdepth is a load-bearing design requirement cited by name in the proofs and formal contracts of D-SEQ ("m ≥ 2 (S8-vdepth)"), ValidInsertionPosition ("m ≥ 2 by S8-vdepth"), and the S8-depth discussion. Because it is absent from the properties table, it is invisible to any dependency-tracking process that reads only the table. A downstream ASN checking whether it has imported all of ASN-0036's axioms would miss S8-vdepth entirely.
**What needs resolving**: S8-vdepth must be added to the Properties Introduced table as a declared design requirement, with its dependencies and dependents recorded at the same level of detail as S8-fin, S8a, and S8-depth.

---

### D-SEQ dependency list omits S8-vdepth

**Foundation**: S8-vdepth (MinimalVPositionDepth) — `#v ≥ 2` for all V-positions
**ASN**: D-SEQ table entry says `from D-CTG, D-CTG-depth, D-MIN, S8-fin, S8-depth, T1 (ASN-0034)`. But D-SEQ's proof opens with "m ≥ 2 by S8-vdepth" and its formal contract lists `m ≥ 2 (S8-vdepth)` as a precondition.
**Issue**: The precondition m ≥ 2 is necessary for D-SEQ's derivation — the proof's Step 1 (Case m = 2) relies on it, and the proof explicitly states "The precondition m ≥ 2 is necessary: at m = 1 the tuple [S, 1, ..., 1, k] collapses to a single component where the subspace identifier S and the varying ordinal k occupy the same position." Without S8-vdepth, D-SEQ's proof has an unfounded assumption. The formal contract correctly records the dependency, but the summary table does not, making the dependency graph incomplete for any process that reads the table.
**What needs resolving**: D-SEQ's table entry must list S8-vdepth among its dependencies (which first requires S8-vdepth to appear in the properties table per the previous finding).

---

### S3 table entry cites NoDeallocation but proof derives from S1

**Foundation**: NoDeallocation (ASN-0034) — "The system defines no operation that removes an element from the set of allocated addresses." S1 (ASN-0036) — Store monotonicity, derived from S0.
**ASN**: S3 table entry: `design; uses NoDeallocation (ASN-0034)`. S3 formal contract: `Preconditions: S1 (store monotonicity); initial-state axiom (Σ.M(d)) establishing dom(Σ₀.M(d)) = ∅; per-operation verification obligation`. S3 proof inductive step: "By S1 (store monotonicity), dom(Σ.C) ⊆ dom(Σ'.C), whence Σ'.M(d)(v) = Σ.M(d)(v) ∈ dom(Σ'.C)."
**Issue**: The table claims S3 depends on NoDeallocation (an ASN-0034 foundation property), but the actual proof and formal contract depend on S1 (an ASN-0036 property derived from S0). NoDeallocation provides background motivation for why S0 is a reasonable axiom, but it does not appear anywhere in S3's derivation chain. The declared dependency path (S3 → NoDeallocation) differs from the actual dependency path (S3 → S1 → S0). This misattribution means the dependency graph incorrectly connects S3 to the foundation through NoDeallocation rather than through S0/S1, which could mislead verification of the cross-ASN dependency chain.
**What needs resolving**: S3's table entry must reflect the actual derivation: its formal dependency is on S1 (and transitively S0), not on NoDeallocation. If NoDeallocation's role as motivation for S0's reasonableness is worth recording, it should be noted in S0's entry rather than S3's.
