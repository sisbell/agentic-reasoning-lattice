# Review of ASN-0026

Based on Alloy modeling-1

## SKIP

### Counterexamples: all expected outcomes of deliberate modeling design

Every SAT result on a `check` command falls into one of two categories — existence witnesses or necessity confirmations — neither of which indicates a spec defect.

**P5 — NonInjective (existence witnesses).** The two checks assert "injectivity always holds" as negated claims; counterexamples are the *desired* outcome, demonstrating that the model permits both self-transclusion and cross-document transclusion. These are existence witnesses confirming P5's permission, not violations.

**P2 — ReferentiallyComplete (independence confirmation).** The assertion tests whether P2 follows from structural well-formedness alone (`wellFormed[s] implies referentiallyComplete[s]`). The `wellFormed` predicate constrains only structural aspects (vspace scoped to docs, docs have positions) and deliberately excludes P2. The counterexample confirms P2 is an independent axiom — it must be actively maintained by operations, not derived from structure. This is the expected result; the ASN correctly states P2 as a standalone invariant.

**P9 (left) — LeftUnchanged (necessity confirmation).** The `Insert` predicate deliberately omits the prefix-unchanged clause (noted in model comments, line 44-45). The counterexample shows the other Insert constraints (suffix shift, new-span coverage, exact bounds) do not force prefix preservation. Confirms P9's left clause is a necessary postcondition — exactly what the model was designed to test.

**P9 (new) — FreshPositions (necessity confirmation).** `Insert` deliberately leaves new positions unconstrained as to *which* address they map to (noted line 43-44). The counterexample shows new positions could map to pre-existing addresses without the freshness constraint. Confirms P9's freshness clause is independently necessary.

**P9 (inj) — FreshInjective (necessity confirmation).** `Insert` includes freshness but deliberately omits injectivity across new positions (noted line 43). The counterexample shows two new positions could share the same fresh address. Confirms P9's injectivity clause is independently necessary.

### Passed properties (13)

P0, P1, NO-REUSE, P3, P4, +_ext, P7, P8, P9 (pre), P9 (length), P9 (right), P11, REF-STABILITY — all held within bounded scope (UNSAT on checks). Non-vacuity runs all SAT.

VERDICT: CONVERGED
