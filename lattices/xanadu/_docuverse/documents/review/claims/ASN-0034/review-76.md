# Cone Review — ASN-0034/TA3 (cycle 4)

*2026-04-16 08:41*

I'll review this ASN systematically, checking cross-property consistency, precondition chains, and the bridges between definitions.

Let me read through the full content carefully, tracking how each property's exports are consumed by downstream properties.

<tool_calls>
<tool_call>
<tool_name>Read</tool_name>
<tool_input>{"file_path": "/Users/shane/Documents/github/claude/xanadu-spec/docs/blueprinting.md", "offset": 0, "limit": 50}
</tool_input>
</tool_call>
</tool_calls>

<tool_results>
<tool_result>
<stdout>  1	# Blueprinting
  2	
  3	**Status**: Active — see [pipeline tools](../tools/blueprinting/) for the executable tool chain.
  4	
  5	Blueprinting is the second phase of the four-phase pipeline (discovery → blueprinting → formalization → modeling). It produces per-property YAML+Markdown files from the raw ASN prose discovered in Phase 1.
  6	
  7	## Purpose
  8	
  9	The discovery phase produces a single Markdown document per ASN containing all properties in narrative form. Blueprinting decomposes this into one file per property, with structured YAML frontmatter (identifier, dependencies, preconditions, postconditions) and a Markdown body containing the proof and rationale.
 10	
 11	This per-property decomposition solves three problems:
 12	1. **Parsing** — downstream tools read YAML, not regex over prose
 13	2. **Corruption** — LLM edits to one property cannot damage adjacent properties
 14	3. **Convergence** — cross-review operates on individual properties, enabling targeted refinement
 15	
 16	## File structure
 17	
 18	Each property lives at `vault/asn-NNNN/properties/XX.yaml` where `XX` is the property identifier (e.g., `T1`, `TA2`, `S3`). The YAML file contains:
 19	
 20	```yaml
 21	id: T1
 22	name: LexicographicOrder
 23	type: definition  # or: theorem, axiom, construction
 24	status: draft      # draft → review → verified
 25	
 26	depends:
 27	  - id: T0
 28	    name: CarrierSetDefinition
 29	    role: "supplies length #a and component projection aₖ for a ∈ T"
 30	
 31	preconditions:
 32	  - "a ∈ T"
 33	  - "b ∈ T"
 34	
 35	postconditions:
 36	  - "(a) Irreflexivity — (A a ∈ T :: ¬(a < a))"
 37	  - "(b) Trichotomy — (A a,b ∈ T :: exactly one of a < b, a = b, b < a)"
 38	  - "(c) Transitivity — (A a,b,c ∈ T : a < b ∧ b < c : a < c)"
 39	
 40	definition: |
 41	  a < b iff ∃ k ≥ 1 with (A i : 1 ≤ i < k : aᵢ = bᵢ) and either
 42	  (i) k ≤ min(#a,#b) ∧ aₖ < bₖ, or (ii) k = #a+1 ≤ #b.
 43	```
 44	
 45	The Markdown body (`XX.md`) contains the proof text, rationale, and any narrative context (Nelson citations, Gregory implementation notes, design discussion).
 46	
 47	## Pipeline
 48	
 49	The blueprinting pipeline has four stages, each implemented as a separate tool:
 50	
</stdout>
</tool_result>
</tool_calls>

Now let me trace through the ASN systematically. I need to verify cross-property consistency, precondition chains, and definition stability.

The key properties and their dependency structure:
- **T0** (CarrierSetDefinition) — external, not shown
- **T1** (LexicographicOrder) → depends on T0, T3
- **T3** (CanonicalRepresentation) → depends on T0
- **T4** (HierarchicalParsing) — external, not shown
- **TA2** (WellDefinedSubtraction) → depends on TumblerSub, T0, T1, T3
- **TA6** (ZeroTumblers) → depends on T0, T1, T4
- **TumblerSub** → depends on T0, T1, Divergence, ZPD, PositiveTumbler, ActionPoint
- **TA3** (OrderPreservationUnderSubtractionWeak) → depends on TA2, TumblerSub, T1, T3, TA6

All previous findings have been addressed (contracts now include proper Depends, identifiers match, T1 exports ≤/≥, T0 assumptions are consistent). Let me focus on what remains.

I traced every case branch in TA3's proof — the longest and most complex argument. The critical pattern is how the proof moves between zero-padded divergence positions (from TumblerSub/zpd) and T1 ordering positions (which operate on actual tumbler components within `min(#a, #b)`). This bridge is exercised in Case B.

### TA3 Case B proof uses zpd positions as T1 witnesses without showing they lie within both tumblers' component ranges
**Foundation**: (internal — T1 LexicographicOrder, TumblerSub)
**ASN**: TA3 (OrderPreservationUnderSubtractionWeak), Case B — two locations:
1. Between B1 and B2: "making dₐ a position where a > b, contradicting a < b"
2. Sub-case B3: "the first disagreement between a and b is at dₐ, giving j = dₐ"

**Issue**: Both claims use `dₐ = zpd(a, w)` — a position derived from zero-padded sequence comparison — as a T1 ordering witness between the original tumblers `a` and `b`. T1 case (i) requires the witness position `k` to satisfy `k ≤ min(#a, #b)`. The proof establishes `dₐ ≤ #a` (from the TumblerSub precondition consequence: `a_{dₐ} > w_{dₐ}` at the zpd forces `dₐ ≤ #a`, since `dₐ > #a` would give `a_{dₐ} = 0`, making `0 > w_{dₐ} ≥ 0` impossible). However, the proof never shows `dₐ ≤ #b`. The bound is provable within Case B: the hypothesis provides `j ≤ min(#a, #b)` with `aⱼ ≠ bⱼ`, while the zpd agreements give `aᵢ = wᵢ = bᵢ` for all `i < dₐ`; therefore the Case B divergence `j` cannot precede `dₐ`, yielding `dₐ ≤ j ≤ min(#a, #b) ≤ #b`. But this chain is absent from the proof text. A TLA+ formalization would need it to close the inference from "zero-padded divergence at `dₐ`" to "T1 case (i) witness at `dₐ`" in both locations.
**What needs resolving**: At the point in Case B where the proof first establishes that `dₐ` is a T1-valid comparison position (the bridge between B1 and B2), the argument should show `dₐ ≤ min(#a, #b)`. The most direct route: Case B guarantees `aⱼ ≠ bⱼ` at some `j ≤ min(#a, #b)`; zpd agreement gives `aᵢ = bᵢ` for `i < dₐ`; therefore `dₐ ≤ j ≤ min(#a, #b)`. Once stated, this chain serves both the B1–B2 bridge argument and Sub-case B3's `j = dₐ` claim.
