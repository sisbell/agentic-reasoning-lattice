# Review of ASN-0084

## REVISE

### Issue 1: SUBCONF closes with a use-site inventory rather than the claim
**ASN-0084, "SUBCONF — Subspace confinement"**: "We cite this fact below as *SUBCONF* wherever a run, or a cut-relative shift, is shown to stay within one subspace."

**Problem**: This matches the flagged forward-reference pattern "a definition's introduction enumerates downstream consumers." The substantive content (`subspace(v + n) = subspace(v)` and the run-confinement corollary) is complete one sentence earlier; the trailing clause only catalogs where the label will reappear, which the reader must skip past. The same pattern recurs in "Extended Associativity": "We cite this identity below as *Extended Associativity*."

**Required**: Drop the use-site enumeration. Naming the result (`SUBCONF`, `Extended Associativity`) is fine; listing its future invocation contexts is not. End SUBCONF at "...so all share subspace(v)."

### Issue 2: Summary table over-attributes R-NS
**ASN-0084, "Properties Introduced" table, R-NS row**: "M'(d) = M(d) on non-S positions (NS-M); π fixes them pointwise by its definition"

**Problem**: The R-NS lemma statement and proof establish only (NS-M) — pointwise identity of M'(d) and M(d) on non-S positions. The clause "π fixes them pointwise" is a fact about π's *definition*, discharged in R-PPERM/R-SPERM (the non-S branch), not in R-NS. The table credits R-NS with a result it does not prove.

**Required**: Either restrict the table entry to NS-M, or attribute the π-fixing clause to R-PPERM/R-SPERM where it is actually established.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4, and composition of rearrangements
**Why out of scope**: The Open Questions correctly flag these as future territory. This ASN fixes n ∈ {3, 4} (CS1) and treats single operations; the generalization and the composition algebra are genuinely new content, not gaps in this note.

### Topic 2: Text subspace at depth m_1 > 2
**Why out of scope**: The depth-2 restriction is declared a scope boundary, not an omission. Lifting it (and re-checking the singleton-tumbler/ℕ identification at deeper ordinals) belongs to a later ASN.

Note on rigor (not a REVISE item): the proofs of R-PIV, R-SWP, R-PPERM, R-SPERM, R-COMM, R-BLK, and R-CANON are case-complete; Width positivity correctly derives w_α, w_β, w_μ ≥ 1 from CS2's strict ordering, foreclosing zero-width regions; the boundary (EXT-VAC, minimum V_S(d)) and non-S pass-through cases are exercised; and the six worked examples each cover a distinct edge (3-cut basic, three 4-cut μ sub-cases, empty exterior, non-S subspace). The forward/backward-extension arguments in R-CANON are sound at the actual run depth. The arithmetic in every traced example checks out.

VERDICT: REVISE
