# Review of ASN-0086

## REVISE

### Issue 1: Terminology overlap with T4 foundation
**ASN-0086, Definition — element-field depth (Setup section)**: "The element-field depth of a tumbler `t` relative to its prefix `s ≼ t` is `zeros(t) − zeros(s)`."

**Problem**: T4 (HierarchicalParsing, ASN-0034) already defines "field separator," "field components," and "field segment" for these concepts. The ASN's own disclaimer in the SharedDepthOneAllocator lemma acknowledges the divergence: "The term 'element-field' elsewhere in this note refers generically to any zero-delimited field, not specifically to T4's E-field." But T4b's E projection refers specifically to the fourth field. Using "element-field" to mean both is exactly the foundation-shadowing the standards call out.

**Required**: Use T4's existing "field segment" (or coin a fresh non-clashing name like "field-segment depth" / "zero-count depth") for the generic measure, reserving "element field" for T4b's E projection consistently.

### Issue 2: Asymmetric L-invariant verification in Worked Sketch
**ASN-0086, Worked Sketch, Steps 3/5.1/6 concrete**: Steps 1 and 2 include separate "L-invariant verification at the concrete b₁" / "L-invariant verification at the concrete a₂" paragraphs enumerating every relevant L-invariant. Step 3 (cross-document b₂), Step 5.1 (a₃), and Step 6 (b₃) omit equivalent explicit verification.

**Problem**: The cross-document case (b₂) is structurally distinct from the same-document case (different depth-1 allocator `A_{d'}`); skipping it leaves the most novel emission without invariant-by-invariant discharge. The Worked Sketch's stated purpose is to verify schematic claims concretely — the asymmetry undermines that purpose at the case that most needs verification.

**Required**: Add an "L-invariant verification at the concrete b₂" paragraph in Step 3 (at minimum), since L1a (LinkScopedAllocation) and L14 / L14a discharge there against a different home document; or explicitly state that the verification pattern from Steps 1-2 is intended to extend without restatement.

### Issue 3: R0 Step 4's home() description and element-field count under SharedDepthOneAllocator
**ASN-0086, R0 Step 4, L1a-preservation bullet**: "`home(a) = d ∈ dom(Σ.M)` by Step 2 and Step 1."

**Problem**: The L1a discharge says `home(a) = d`, but Step 2 Case A constructs `a = d.0.s_L.1` — a tumbler whose element-field is `[s_L, 1]` with `#E(a) = 2`. The L1c bullet refers to "the chain of Step 3" but Step 3 only collects the chain from Step 2 (no new content). This means Step 4 is forward-referencing a chain that hasn't been independently constructed in Step 3. The flow Step 1 → 2 → 3 → 4 is somewhat misleading: Step 3 is essentially empty.

**Required**: Either fold Step 3 into Step 2 (since Step 3 is just naming what Step 2 produced), or have Step 3 do additional work (e.g., explicitly state the chain witnesses every L1c clause).

### Issue 4: Repetition obscures the substantive content
**ASN-0086, throughout**: Setup-conditionality and discipline-conditionality are explained at the Setup section, the "Setup dependence at a glance" summary, the per-claim `[Setup-required]` / `[Setup-free, discipline-conditional]` tags, the Properties Introduced table, the Hypothesis dependency view table, and via inline remarks within proofs. R7a (proven) vs. R7b (stipulated) is similarly restated.

**Problem**: A reader reconstructing the dependency structure must assemble the same claim from multiple repetitions; this is presentation friction, not new information. The Hypothesis dependency view table is the most structured form and could subsume the redundant inline restatements.

**Required**: Consolidate hypothesis tracking to the Hypothesis dependency view table; reduce inline `[Setup-required]` / discipline-conditional restatements to single citations of that table.

## OUT_OF_SCOPE

### Topic 1: Higher-arity active subsets `A_K^{(n)}`
**Why out of scope**: The ASN restricts to standard-triple (arity-3) links by design and flags the higher-arity extension as future work in the Open Questions. Not a defect in this ASN.

### Topic 2: Concurrency / atomicity model for Emit and Observe
**Why out of scope**: The ASN explicitly defers concurrency questions to Open Questions; sequential semantics suffice for the substrate-level claims here.

### Topic 3: Slice-wise reformulation under L14's native scoped form
**Why out of scope**: Properly belongs in a future ASN that admits `s_L`-resident content; the Setup hypothesis confines this note to globally `s_C`-resident content as a stated commitment.

VERDICT: REVISE
