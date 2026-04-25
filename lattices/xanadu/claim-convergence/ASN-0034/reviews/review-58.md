# Cone Review — ASN-0034/T8 (cycle 4)

*2026-04-15 22:08*

Now I have the full picture. Let me trace the dependency declarations across the document.

**Summary of what I've verified:**
- T1 YAML: `depends: [T3]`, prose: `Depends: T3` — consistent
- T2 YAML: `depends: [T1]`, prose: `Depends: T3` — **split**
- TA5 YAML: `depends: [T1]`, prose: no Depends clause
- TumblerAdd YAML: `depends: [PositiveTumbler]`, prose: no Depends clause — **T1 missing from both**
- T10a YAML: `depends: [TA5, TA5a, T4, T1, T10, Prefix]`, prose: lists all six — consistent
- T8 YAML: `depends: [NoDeallocation]`, prose: `Depends: NoDeallocation` — consistent

---

### T2 YAML metadata omits T3, creating a prose/YAML dependency split where neither source is complete

**Foundation**: T3 (CanonicalRepresentation) — bridges component-level agreement to tumbler equality
**ASN**: T2 (IntrinsicComparison) proof, Case 2: "if `m = n`, then T3 gives `a = b`"; formal contract declares `Depends: T3`; YAML metadata declares `depends: [T1]`
**Issue**: The T2 proof explicitly invokes both T1 (the ordering whose computability it establishes — T1's case structure is used throughout) and T3 (for the equality case in Case 2, where the algorithm must bridge from component-wise agreement plus equal length to tumbler equality). The prose contract correctly declares T3 but not T1. The YAML metadata declares T1 but not T3. Neither source captures the complete dependency set {T1, T3}. A mechanical dependency checker reading the YAML will miss the T3 dependency entirely — it will not know that T2's equality case requires T3, even though the prose contract says so. This is the same dependency (T3 for the equality bridge) that T1's contract now correctly declares after a previous finding; T2 uses T3 in exactly the same way ("all components agree, same length → equal by T3") but the YAML was never updated to match.
**What needs resolving**: The YAML metadata must add T3 to its `depends` list, yielding `depends: [T1, T3]`. This brings the YAML in line with the prose contract's `Depends: T3` declaration and with the proof's explicit T3 invocation.

---

### TumblerAdd proof explicitly cites T1 case structure three times but neither prose contract nor YAML metadata declares T1 as a dependency

**Foundation**: T1 (LexicographicOrder) — the ordering used to establish TumblerAdd's two ordering postconditions
**ASN**: TumblerAdd (TumblerAdd) proof: "T1 case (i) with divergence position `k` — agreement on positions `1, ..., k - 1` and strict inequality `aₖ < rₖ` — yields `a < a ⊕ w`"; "so T1 case (i) gives `r > w`"; "T1 case (i) again gives `r > w`"; postconditions: `a ⊕ w > a (T1)`, `a ⊕ w ≥ w (T1)`. YAML metadata: `depends: [PositiveTumbler]`. Prose contract: no Depends clause.
**Issue**: The proof invokes T1's case (i) three times by name to establish both ordering postconditions. The YAML metadata declares only `depends: [PositiveTumbler]`, omitting T1. The prose contract has no Depends clause at all. This creates a gap in both the human-readable contract and the machine dependency graph. For comparison, TA5 (HierarchicalIncrement) uses T1 in exactly the same way — T1 case (i) for k = 0 and T1 case (ii) for k > 0 — and its YAML correctly declares `depends: [T1]`. The same proof pattern in two arithmetic properties produces different dependency metadata. Additionally, the equality sub-case of the `a ⊕ w ≥ w` postcondition concludes "the tumblers are equal" from component-wise agreement plus equal length — the same reasoning that T1's contract cites T3 for — without naming T3, leaving a second implicit dependency.
**What needs resolving**: TumblerAdd's YAML metadata must add T1 to its `depends` list (yielding at minimum `depends: [PositiveTumbler, T1]`), and the prose contract should include a Depends clause declaring T1, consistent with how TA5, T10a, and other properties in the same ASN handle their T1 dependency. The implicit T3 usage in the equality sub-case should either be cited explicitly in the proof (as T1's proof does) or declared in the contract.
