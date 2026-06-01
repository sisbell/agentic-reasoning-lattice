# Review of ASN-0086

The technical core is sound. I checked R0/R0a (both home cases), L-ContiguousPrefix's induction, R-Scope's antichain argument, the R7a `↝`→`→` decomposition (discharges 1–4), and the wp Case 2 derivation including both necessity witnesses — they hold, and the worked sketch correctly instantiates the postconditions. My findings are confined to the anti-bloat mandate this note carries.

## REVISE

### Issue 1: Verbatim caveat duplicated across two sections
**ASN-0086, wp Case 2 (load-bearingness)**: "Note the self-targeting span here is itself unit-depth, so the discipline does not exclude it — only the disjunction's collapse to falsity records it."
**ASN-0086, Worked Sketch, Step 4 (final parenthetical)**: "(Note that since the self-targeting span is unit-depth, the unit-depth retraction discipline does not exclude this call; only the disjunction's collapse to falsity records it.)"
**Problem**: Two near-verbatim statements of the same abstract observation. The Step 4 instance does no concrete work — it restates the wp caveat rather than deriving anything from the worked tumbler values, so it is not the permitted "concrete example" but a relocated restatement. Matches the "two paragraphs say the same thing in different words" pattern.
**Required**: Drop the Step 4 parenthetical (the wp paragraph already owns the abstract claim), or replace it with the concrete computation it elides.

### Issue 2: Conformance-containment relationship re-narrated at ≥3 sites
**ASN-0086, Definition — state-local-conforming state**: "the containment `{→*-reachable} ⊆ {substrate-conforming} ⊆ {state-local-conforming}` holds, and its rightmost inclusion is strict, witnessed by the NestedLinkWitness construction above."
**Problem**: The same containment-and-strictness fact is re-stated in L-ContiguousPrefix's extension step ("the containment `{→*-reachable} ⊆ {substrate-conforming}` is strict") and again in the wp Domain-restriction paragraph ("though the converse fails"). The relation is established once; the later sites repeat it rather than cite it. Compounding meta-prose across the conformance-definition cluster.
**Required**: State the containment and its strictness once (the definition), and have downstream sites cite it without re-arguing the inclusion.

### Issue 3: Defensive "what the proof does not appeal to" clause
**ASN-0086, Definition — `a_emit`**: "The max is the unique T1-extremum of a finite (L-fin, ASN-0043) non-empty set, by T1 (LexicographicOrder, ASN-0034) trichotomy alone — no contiguity or conformance appeal."
**Problem**: The "— no contiguity or conformance appeal" clause justifies which hypotheses are *not* used. This is defensive justification, not advancement of the definition; the positive statement ("unique T1-extremum by trichotomy") already carries the content.
**Required**: Delete the trailing clause.

## OUT_OF_SCOPE

### Topic 1: Tightening L1b's `#E ≥ 2` to `#E = 2`
L-ContiguousPrefix-Cor1 proves `#E(a) = 2` strictly at substrate-conforming states, while ASN-0043's L1b admits `#E ≥ 2` (and NestedLinkWitness exercises `#E = 3` at a merely state-local-conforming state). Whether the substrate admission should be tightened at source is a foundation-ASN revision, not a defect here.

META: not applicable — the note defines genuine derived state (the active/audit `nullified`/`A_K` distinction) with stability and monotonicity invariants, so it remains in specification territory.

VERDICT: REVISE
