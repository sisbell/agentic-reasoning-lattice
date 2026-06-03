# Review of ASN-0075

I checked the lemma chain (D-WIT, D-EXH, D-DISCR, D-NEED, D-DISJ), the two-history discrimination argument, the wp computations, and the worked example. The core mathematics is sound: the two-history counterexample correctly agrees on (C,L,E,M) while differing only on R, the three-state classification is genuinely exhaustive and exclusive, and the worked example computes correctly through the K.μ~/K.μ⁻ reorder-then-truncate trick. The findings below are about notation, ordering, and accreted prose — consistent with the anti-bloat classifier on this note.

## REVISE

### Issue 1: Output-set arity is inconsistent between the wp section and everywhere else
**ASN-0075, "The SHOWDELETIONS Operation" (wp form)**: "`Result = (DeletedFromAWithB(Σ, d_A, d_B), DeletedFromBWithA(Σ, d_A, d_B))`"
**Problem**: Every other site — the set definitions, the operation Definition, D-DISJ, the claims table, the worked example — writes these as two-argument forms `DeletedFromAWithB(d_A, d_B)`. Only the wp predicate `q` silently adds an explicit `Σ` parameter. A precise reader must stop to decide whether this is a third argument or an informal state annotation.
**Required**: Pick one convention. Either thread `Σ` through all uses or drop it from `q` and rely on the surrounding "at the pre-state" phrasing.

### Issue 2: The wp pass-through rule is justified by D-OBS, which is stated several sections later
**ASN-0075, "The SHOWDELETIONS Operation" (wp form)**: "Because SHOWDELETIONS writes no state component (D-OBS, Observational Frame), wp computations for state-level predicates pass through unchanged from the pre-state: `wp(SHOWDELETIONS, P) = (precondition) ∧ P(Σ)`…"
**Problem**: The Q0/Q1 wp derivations rest on observationality, but D-OBS is not established until the "Observational Frame" section that follows the entire operation/edge-case discussion. The argument consumes a claim before it is proved, and the forward citation is the only thing carrying it.
**Required**: Move the observational-frame claim (or at least the "writes nothing" fact) ahead of the wp analysis, so the pass-through rule rests on an already-stated result rather than a forward pointer.

### Issue 3: D-EXH's closing paragraph re-narrates the table and the row bullets
**ASN-0075, D-EXH proof, final paragraph**: "In each row exactly one of the three predicates holds… establishing mutual exclusion. Exhaustiveness follows from cross-product totality: each of the two binary conditions… is either true or false, so every (a,d)… falls into exactly one of the four rows; the impossible row is excluded by the chain above, so every such (a,d) lies in one of the three remaining rows and receives exactly one classification."
**Problem**: The per-row bullets immediately above already state, for each surviving row, which predicate holds and that the other two fail — that *is* mutual exclusion. The table plus the D-WIT exclusion of row 2 already gives exhaustiveness. This paragraph restates both facts in prose without adding a step. It is the kind of exhaustiveness-restatement the anti-bloat pass targets.
**Required**: Collapse to a single sentence: the four-row table is total, row 2 is excluded by D-WIT, and each remaining row assigns exactly one label per the bullets above.

## OUT_OF_SCOPE

### Topic 1: Per-occurrence (V-position-level) deletion detection
The "I-address-set granularity" paragraph correctly scopes out distinguishing which of several V-positions holding the same I-address was removed. This is a Vstream concern; deferring it is appropriate, not an error here.

### Topic 2: Multi-document SHOWDELETIONS, restoration, concurrency, span presentation
These are raised only as Open Questions, framed as future territory, and align with the declared out-of-scope list (operation mechanics, version DAG, etc.). No action needed.

VERDICT: REVISE
