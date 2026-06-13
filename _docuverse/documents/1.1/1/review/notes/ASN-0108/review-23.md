# Review of ASN-0108

The note is, on its technical spine, strong: the W2 weakest-precondition analysis (identity vs. offset cursor), the W4 partition induction over a variable window schedule, the W9b per-link multiplicity bound for termination, and the W9c necessity counterexample are all correct and carefully bounded. The walks cover the mandated boundaries (empty matching set, first-window-short, exact-multiple terminator, orphaned cursor). My findings are one internal imprecision in a load-bearing proof sentence, plus several instances of the meta-prose / forward-reference accretion the anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: W5's coherence proof overstates `After(c, Σ')`
**ASN-0108, W5 (OrderStability), justification paragraph**: "conversely, with clause 1 holding, `After(c, Σ')` is exactly the not-yet-delivered matchers, and chaining the coherent steps delivers every still-matching tail link once."
**Problem**: This is internally inconsistent with W5's own caveat. A link `b` created (or resurrected) between calls with `κ_{Σ'}(b) <_K κ_{Σ'}(c)` is a not-yet-delivered matcher (`b ∈ Match(q, Σ')`, never delivered) but `b ∉ After(c, Σ')` — it is below the cut. So `After(c, Σ')` is *not* "exactly the not-yet-delivered matchers"; it is the not-yet-delivered matchers **above the cursor**. The same paragraph elsewhere acknowledges exactly these below-cursor new matchers: "Omission of a newly-created or newly-discoverable matcher that lands below the cursor is not a coherence failure but the separate W6 blind spot." The proof sentence contradicts that caveat.
**Required**: Qualify the identification to the tail — "`After(c, Σ')` is exactly the not-yet-delivered matchers lying above the cursor" (equivalently, the undelivered both-states tail matchers together with any above-cursor inflow) — so the sentence is consistent with the W6 blind-spot carve-out it sits beside. The conclusion drawn ("delivers every still-matching tail link once") is sound; only the intermediate set identity needs the qualifier.

### Issue 2: κ-definition closes with a downstream-consumer inventory
**ASN-0108, "What κ is, concretely"**: "The discrepancy is not a detail: it decides whether a newly created link appends at the tail or can be silently skipped (W6), and whether the cursor survives deletion of the content it marked (W8)."
**Problem**: This is the flagged pattern — a definition's introduction enumerating its downstream consumers (W6, W8) rather than advancing the meaning of `κ`. It is a roadmap sentence; the reader must skip it to reach the actual content (the non-injectivity caution that follows). W6 and W8 make their own dependence on the key explicit at their sites.
**Required**: Delete the forward-pointer inventory; the non-injectivity caution immediately following is the substantive content of this subsection.

### Issue 3: W9b table entry narrates superseded reasoning
**ASN-0108, Claims Introduced table, W9b row**: "a per-link multiplicity bound (deliveries ≤ |initial tail| + |inflow events|) **replaces the invalid 'no link consumed twice'**, and bounded instantaneous size is not sufficient".
**Problem**: "replaces the invalid 'no link consumed twice'" references a prior, wrong version of the argument — reviser-drift residue. The current note should state the correct bound; a reader does not need to be told which earlier claim it supersedes. (The W9b body states the bound cleanly without this editorializing.)
**Required**: Drop the "replaces the invalid …" clause; keep the bound itself.

### Issue 4: foreshadowing / provenance-defensive prose in the Match section
**ASN-0108, "State, the Matching Set, and What Windowing Operates On"**: "The asymmetry in (M-mut) is the source of every subtlety to come." and "Both are foundation results, not choices this note makes; we adopt the discoverability reading …"
**Problem**: "the source of every subtlety to come" is pure foreshadowing meta-narrative; "not choices this note makes" is a defensive justification of provenance. Neither advances the definition of `Match` or the statement of M-fin / M-mut. The substantive content (Match is finite by L-fin; non-monotone by D-NONMONO) stands without them.
**Required**: State M-fin and M-mut and their foundation sources directly; remove the narrative framing.

### Issue 5: dangling type-refinement clause
**ASN-0108, Match definition paragraph**: "reducing at full region to `{a ∈ dom(Σ.L) : discoverable_from(a, d_q, Σ)}` (F-FULL) and refined by the query's type part where present (ASN-0086)."
**Problem**: The "refined by the query's type part" clause is mentioned once and never used — every proof relies only on the imported M-fin and M-mut, never on type filtering. The note also declares "which region a query fixes" out of scope ("leaving … to query construction, outside this note"), and the type part is the same kind of query-construction detail. As stated it is an underspecified use-site mention that does not advance the abstract treatment.
**Required**: Either specify how the type part refines `Match` (if load-bearing) or drop the clause as query-construction already declared out of scope, leaving `Match` characterized solely by M-fin and M-mut.

## OUT_OF_SCOPE

The note's five Open Questions already capture the genuine future-ASN territory (multi-document enumeration without a global allocation-monotone key; guaranteed eventual delivery of created links under a non-monotone key; the cross-state completeness invariant; distinguishing empty-tail from irrecoverable-cursor; delivery-vs-progress-count correspondence). I have no additional out-of-scope topics to raise — the excluded operations (count-only, full-set/ASN-0099, MAKELINK, FOLLOWLINK, BEBE) are correctly absent from the body.

VERDICT: REVISE
