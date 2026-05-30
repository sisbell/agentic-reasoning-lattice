# Review of ASN-0042

## REVISE

### Issue 1: Forward-reference inventory in the opening predicate section

**ASN-0042, Ownership as a Structural Predicate**: "It does *not* realize the longest-match selector `ω` (O2) on which the load-bearing guarantees — exclusivity (O2), refinement (O3), irrevocable delegation (O8) — all rest, because `ω` requires arbitrating among multiple covering principals and the system never does so. Those guarantees are therefore abstract obligations that any faithful implementation must discharge, not properties the existing `tumbleraccounteq` already secures; the absence of any `ω`-realizing mechanism in udanax-green is a conformance gap, recorded in the Open Questions."

**Problem**: This paragraph sits before O2, O3, and O8 are stated and inventories them as downstream consumers ("the load-bearing guarantees ... all rest"), then defers downstream ("recorded in the Open Questions"). The Open Questions list already carries the identical conformance-gap point ("What must an implementation guarantee to realize the longest-match effective-owner selection `ω` (O2) on which exclusivity, refinement, and irrevocable delegation depend..."). This is the flagged pattern of a definition's introduction enumerating downstream consumers and deferring to a downstream location that restates the same content — meta-prose the reader must skip to reach the actual O1 definition.

**Required**: Reduce to the factual scope statement — `tumbleraccounteq` realizes `owns`/O1 (single-account containment), not `ω` — and delete the guarantee inventory and the Open-Questions defer, since the Open Question already records it.

### Issue 2: O7(c)'s "entry-state-only" caveat stated three times

**ASN-0042, O7**: The caveat that recursive delegation is established only at the entry state appears in (a) the O7 postcondition block — "we do not establish it at an arbitrary later delegation state, where an intervening delegation may interpose a more-specific cover of `p''` and falsify (ii)"; (b) the proof of (c) — "The recursive right is thus established for the entry state `Σ'`..."; and (c) the Formal Contract — "The claim is restricted to the entry state `Σ'`; satisfiability at an arbitrary later delegation state is not asserted."

**Problem**: The same hedge is restated in three slots in different words — the flagged "two paragraphs in the same document say the same thing" pattern, compounded.

**Required**: State the restriction once (in the proof, where the reason lives) and let the postcondition/Formal Contract carry the bare claim.

### Issue 3: Dangling "first equality" reference in O3

**ASN-0042, O3 (OwnershipRefinement) proof**: "`{π ∈ Π_Σ : pfx_Σ(π) ≼ a} = {π ∈ Π_{Σ'} ∩ Π_Σ : pfx_{Σ'}(π) ≼ a}` The first equality follows from O12 (`Π_Σ ⊆ Π_{Σ'}`) and O13 (`pfx_{Σ'} = pfx_Σ` on `Π_Σ`)."

**Problem**: Only one equality is displayed, but the text refers to "The first equality," implying a second that does not appear — residue of an earlier edit. A precise reader stops to hunt for the missing equation.

**Required**: Drop "first" (just "This equality follows..."), or restore the second equation if one was intended.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
The first Open Question (transfer semantics, divergence of provenance O6 from effective owner O2) is correctly deferred — transfer has no mechanism in the specified system, so it is future territory, not a gap in this ASN.

### Topic 2: `ω`-realizing implementation conformance
The conformance gap between account-level containment and longest-match `ω` selection is a genuine implementation-realization question; recording it as an Open Question (not a claim) is the right scope decision.

VERDICT: REVISE
