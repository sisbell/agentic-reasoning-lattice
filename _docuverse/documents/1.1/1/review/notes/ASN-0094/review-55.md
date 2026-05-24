# Review of ASN-0094

## REVISE

### Issue 1: Inconsistent qualifier in *Standalone admissibility* clause reference

**ASN-0094, "Resolution base templates exercised directly" subsection in *Additional Worked Examples***: "the standalone path (a Resolution registration with no `_via` consumer in scope) is admissible under Sh5(b), as the *Standalone admissibility (settled, not exhibited)* clause of the Resolution catalog walkthrough records."

**Problem**: The Resolution catalog walkthrough's clause is actually titled *Standalone admissibility (settled and exhibited)*, and that clause explicitly states: "Both regimes are exhibited in this document's worked examples... the standalone path at the 'Resolution base templates at a standalone K (no `_via` consumer in scope)' sub-walkthrough in Additional Worked Examples". The standalone path IS exhibited (in the next subsection), so the parenthetical "(settled, not exhibited)" contradicts the actual clause title and the document's structure.

**Required**: Change the reference to read "*Standalone admissibility (settled and exhibited)*" to match the actual clause title. Alternatively, if the intent was to convey that this particular subsection doesn't itself exhibit standalone use (it exercises Resolution under parametric consumption), then rephrase to avoid putting a contradictory qualifier on the referenced clause — e.g., "as the *Standalone admissibility* clause of the Resolution catalog walkthrough records (with the standalone path exhibited at the next sub-walkthrough below)."

## OUT_OF_SCOPE

No items beyond those already enumerated in the ASN's *Open Questions* section. The framework's explicit tagging of items as [design choice], [refinement candidate], and [scope boundary] handles the residual issues appropriately — including multi-process substrate concurrency (scope boundary), ghost-targeting slot semantics (design choice), composite shapes (refinement candidate), and the per-K opt-in registry as potential sixth shape component (design choice).

VERDICT: REVISE
